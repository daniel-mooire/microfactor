"""Compute factors from a data provider and persist them."""

from __future__ import annotations

import hashlib
import json
from collections.abc import Callable
from datetime import datetime
from pathlib import Path

import pandas as pd

from microfactor.core import Factor, run_factor
from microfactor.core.protocols import DataProvider
from microfactor.naming import FactorName
from microfactor.preprocess import FactorPreprocessPipeline, PreprocessConfig
from microfactor.storage import FactorStorage

ProgressFn = Callable[[int, int, str], None]
LogFn = Callable[[str], None]
PostProcessFn = Callable[[str, pd.DataFrame], dict[str, int]]


class ZScorePostProcess:
    """Post-compute strategy: store a z-scored variant alongside the raw factor."""

    def __init__(
        self,
        storage: FactorStorage,
        config: PreprocessConfig | None = None,
    ) -> None:
        self._storage = storage
        self._pipeline = FactorPreprocessPipeline(config or PreprocessConfig())

    def __call__(self, factor_name: str, raw: pd.DataFrame) -> dict[str, int]:
        z_name = FactorName.parse(factor_name).standardized
        z_scored = self._pipeline.transform(raw)
        self._storage.write(z_name, z_scored)
        return {z_name: len(z_scored)}


class FactorComputeService:
    def __init__(
        self,
        provider: DataProvider,
        storage: FactorStorage,
        *,
        log_info: LogFn | None = None,
    ) -> None:
        self._provider = provider
        self._storage = storage
        self._log: LogFn = log_info or (lambda message: None)

    def compute_and_store(
        self,
        factors: tuple[Factor, ...],
        *,
        start_date: str,
        end_date: str | None,
        universe: str,
        progress: ProgressFn | None = None,
        postprocess: PostProcessFn | None = None,
    ) -> dict[str, int]:
        fields = sorted({field for factor in factors for field in factor.spec.inputs})
        adjust_values = {factor.spec.adjust for factor in factors}
        if len(adjust_values) != 1:
            raise ValueError("factors with mixed adjust settings cannot share one data load")

        self._log(f"market_data_load_started fields={','.join(fields)}")
        data = self._provider.history(
            fields=fields,
            start_date=start_date,
            end_date=end_date,
            universe=universe,
            adjust=adjust_values.pop(),
            progress=progress,
        )
        self._log("market_data_load_finished")
        self._log("factor_write_stage_started")

        row_counts: dict[str, int] = {}
        batch_id = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        for factor in factors:
            name = factor.spec.name
            self._log(f"factor_write_started factor={name}")
            result = run_factor(factor, data)
            self._storage.publish_factor(
                name,
                result,
                contract=factor.spec,
                compute_run_id=batch_id,
                universe=universe,
            )
            row_counts[name] = len(result)
            self._log(f"factor_write_finished factor={name} rows={len(result)}")
            if postprocess is not None:
                row_counts.update(postprocess(name, result))
        return row_counts


def compute_catalog_factors(
    provider: DataProvider,
    storage: FactorStorage,
    *,
    start_date: str,
    end_date: str | None,
    universe: str,
    factors: tuple[Factor, ...] | None = None,
    log_info: LogFn | None = None,
    resume: bool = False,
    factor_dir: Path | None = None,
    run_id: str | None = None,
) -> dict[str, dict[str, object]]:
    """Compute catalog factors in bounded groups with durable per-factor state.

    The provider is called once per exact ``(adjust, inputs)`` group.  A failed
    factor or data group is recorded and does not discard factors completed
    earlier in the same run.  ``resume`` only reuses a matching successful
    manifest and an existing non-empty storage partition.
    """

    from microfactor.factors.catalog import catalog_factors

    selected = tuple(sorted(factors or catalog_factors(), key=lambda item: item.spec.name))
    grouped: dict[tuple[str | None, tuple[str, ...]], list[Factor]] = {}
    for factor in selected:
        key = (factor.spec.adjust, tuple(sorted(factor.spec.inputs)))
        grouped.setdefault(key, []).append(factor)

    results: dict[str, dict[str, object]] = {}
    root = Path(factor_dir or getattr(storage, "_factor_dir", Path("data/factors")))
    batch_id = run_id or datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    batch_dir = root / "_runs" / batch_id
    batch_dir.mkdir(parents=True, exist_ok=True)
    batch_manifest = batch_dir / "manifest.json"

    def persist_batch() -> None:
        payload = {
            "run_id": batch_id,
            "factor_names": [factor.spec.name for factor in selected],
            "start_date": start_date,
            "end_date": end_date,
            "universe": universe,
            "results": results,
        }
        batch_manifest.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2, default=str) + "\n",
            encoding="utf-8",
        )

    persist_batch()
    for (adjust, fields), group in grouped.items():
        pending = []
        for factor in group:
            previous = _load_resumable_manifest(
                root / factor.spec.name / "compute_manifest.json",
                factor=factor,
                start_date=start_date,
                end_date=end_date,
                universe=universe,
                storage=storage,
            )
            if resume and previous is not None:
                results[factor.spec.name] = previous
                continue
            pending.append(factor)
        if not pending:
            persist_batch()
            continue

        try:
            data = provider.history(
                fields=fields,
                start_date=start_date,
                end_date=end_date,
                universe=universe,
                adjust=adjust,
            )
            input_fingerprint = _frame_fingerprint(data, fields)
        except Exception as exc:
            for factor in pending:
                result = {
                    "status": "failed",
                    "rows": 0,
                    "error": f"{type(exc).__name__}: {exc}",
                    "fields": list(fields),
                    "adjust": adjust,
                }
                results[factor.spec.name] = result
                write_compute_manifest(
                    factor=factor,
                    factor_dir=root / factor.spec.name,
                    row_count=0,
                    start_date=start_date,
                    end_date=end_date,
                    universe=universe,
                    status="failed",
                    error=result["error"],
                    input_fingerprint=None,
                    batch_run_id=batch_id,
                    input_fields=fields,
                )
            persist_batch()
            continue

        for factor in pending:
            try:
                output = run_factor(factor, data)
                _validate_factor_output(output, factor.spec.name)
                storage.publish_factor(
                    factor.spec.name,
                    output,
                    contract=factor.spec,
                    compute_run_id=batch_id,
                    universe=universe,
                    input_fingerprint=input_fingerprint,
                )
                status = "computed" if not output.empty else "insufficient_data"
                error = None if not output.empty else "factor produced no finite values"
                result = {
                    "status": status,
                    "rows": len(output),
                    "fields": list(fields),
                    "adjust": adjust,
                    "input_fingerprint": input_fingerprint,
                }
                if error:
                    result["error"] = error
                results[factor.spec.name] = result
                # publish_factor writes the versioned and compatibility manifests.
                if log_info is not None:
                    log_info(
                        f"catalog_factor_computed factor={factor.spec.name} "
                        f"rows={len(output)}"
                    )
            except Exception as exc:  # one factor must not discard completed outputs
                result = {
                    "status": "failed",
                    "rows": 0,
                    "error": f"{type(exc).__name__}: {exc}",
                    "fields": list(fields),
                    "adjust": adjust,
                }
                results[factor.spec.name] = result
                write_compute_manifest(
                    factor=factor,
                    factor_dir=root / factor.spec.name,
                    row_count=0,
                    start_date=start_date,
                    end_date=end_date,
                    universe=universe,
                    status="failed",
                    error=result["error"],
                    input_fingerprint=None,
                    batch_run_id=batch_id,
                    input_fields=fields,
                )
                if log_info is not None:
                    log_info(f"catalog_factor_failed factor={factor.spec.name} error={exc}")
            persist_batch()
    persist_batch()
    return results


def write_compute_manifest(
    *,
    factor,
    factor_dir,
    row_count: int,
    start_date: str,
    end_date: str | None,
    universe: str,
    frame: pd.DataFrame | None = None,
    status: str = "computed",
    error: str | None = None,
    input_fingerprint: str | None = None,
    batch_run_id: str | None = None,
    input_fields: tuple[str, ...] | list[str] | None = None,
) -> None:
    """Persist the computation contract and lightweight data-quality checks."""
    factor_dir = Path(factor_dir)
    factor_dir.mkdir(parents=True, exist_ok=True)
    checks = {"row_count": int(row_count)}
    if frame is not None:
        daily_counts = frame["trade_date"].value_counts().sort_index()
        checks.update(
            {
                "duplicate_keys": int(frame.duplicated(["trade_date", "ts_code"]).sum()),
                "nan_values": int(frame["value"].isna().sum()),
                "unique_dates": int(frame["trade_date"].nunique()),
                "unique_assets": int(frame["ts_code"].nunique()),
                "first_value_date": str(frame["trade_date"].min()) if not frame.empty else None,
                "last_value_date": str(frame["trade_date"].max()) if not frame.empty else None,
                "daily_coverage": {str(key): int(value) for key, value in daily_counts.items()},
            }
        )
    payload = {
        "factor_name": factor.spec.name,
        "formula": factor.spec.formula,
        "inputs": list(factor.spec.inputs),
        "adjust": factor.spec.adjust,
        "category": factor.spec.category,
        "source_status": factor.spec.status,
        "source": factor.spec.source,
        "implementation": factor.spec.implementation,
        "start_date": start_date,
        "end_date": end_date,
        "universe": universe,
        "status": status,
        "error": error,
        "batch_run_id": batch_run_id,
        "input_fields": list(input_fields or factor.spec.inputs),
        "input_fingerprint": input_fingerprint,
        "checks": checks,
    }
    (factor_dir / "compute_manifest.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, default=str) + "\n",
        encoding="utf-8",
    )


def _validate_factor_output(frame: pd.DataFrame, factor_name: str) -> None:
    required = {"trade_date", "ts_code", "value"}
    missing = required.difference(frame.columns)
    if missing:
        raise ValueError(f"{factor_name}: output missing columns {sorted(missing)}")
    if frame.duplicated(["trade_date", "ts_code"]).any():
        raise ValueError(f"{factor_name}: duplicate trade_date/ts_code keys")
    if frame["value"].isna().any():
        raise ValueError(f"{factor_name}: output contains NaN values")


def _frame_fingerprint(data, fields: tuple[str, ...]) -> str:
    digest = hashlib.sha256()
    for field in fields:
        frame = getattr(data, field)
        digest.update(field.encode("utf-8"))
        digest.update(pd.util.hash_pandas_object(frame, index=True).to_numpy().tobytes())
    return digest.hexdigest()


def _load_resumable_manifest(path: Path, *, factor, start_date, end_date, universe, storage):
    if not path.exists():
        return None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
        if payload.get("status") != "computed":
            return None
        if payload.get("factor_name") != factor.spec.name:
            return None
        if payload.get("start_date") != start_date or payload.get("end_date") != end_date:
            return None
        if payload.get("universe") != universe:
            return None
        stats = storage.factor_stats(factor.spec.name)
        checks = payload.get("checks", {})
        if stats is None or int(checks.get("row_count", 0)) != stats.rows:
            return None
        if "daily_coverage" not in checks:
            frame = storage.read(factor.spec.name, start_date=start_date, end_date=end_date)
            write_compute_manifest(
                factor=factor,
                factor_dir=path.parent,
                row_count=len(frame),
                start_date=start_date,
                end_date=end_date,
                universe=universe,
                frame=frame,
                status="computed",
                input_fingerprint=payload.get("input_fingerprint"),
                batch_run_id=payload.get("batch_run_id"),
                input_fields=payload.get("input_fields"),
            )
        return {
            "status": "computed",
            "rows": stats.rows,
            "input_fingerprint": payload.get("input_fingerprint"),
            "resumed": True,
        }
    except (OSError, ValueError, TypeError, KeyError, json.JSONDecodeError):
        return None
