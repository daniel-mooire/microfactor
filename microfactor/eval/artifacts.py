from __future__ import annotations

import hashlib
import json
from datetime import datetime
from pathlib import Path

import pandas as pd

from microfactor.eval.domain import EvaluationRunConfig


class EvaluationArtifactStore:
    def create_run(self, run) -> None:
        run.run_dir.mkdir(parents=True, exist_ok=False)

    def write_factor_artifacts(self, result) -> dict[str, Path]:
        if result.clean_factor_data is None:
            raise ValueError("clean_factor_data is required to write factor artifacts")
        if result.daily_ic is None:
            raise ValueError("daily_ic is required to write factor artifacts")
        if result.quantile_returns is None:
            raise ValueError("quantile_returns is required to write factor artifacts")
        return write_factor_artifacts(
            factor_dir=result.output_dir,
            clean_factor_data=result.clean_factor_data,
            daily_ic=result.daily_ic,
            quantile_returns=result.quantile_returns,
            quantile_returns_by_date=result.quantile_returns_by_date,
            five_bucket_returns=result.five_bucket_returns,
            portfolio_returns=result.portfolio_returns,
            summary=result.summary,
        )

    def write_run_summary(self, run, summary: pd.DataFrame) -> dict[str, Path]:
        return write_run_summary(
            run_dir=run.run_dir,
            summary=summary,
            config=run.config,
            run_id=run.run_id,
        )

    def write_run_manifest(self, run, summary: pd.DataFrame) -> Path:
        return write_run_manifest(run=run, summary=summary)


def create_run_directory(
    config: EvaluationRunConfig, run_id: str | None = None
) -> tuple[str, Path]:
    if run_id is None:
        run_id = datetime.now().strftime("%Y%m%d_%H%M%S")

    run_dir = config.output_dir / run_id
    run_dir.mkdir(parents=True, exist_ok=False)
    return run_id, run_dir


def write_factor_artifacts(
    *,
    factor_dir: str | Path,
    clean_factor_data: pd.DataFrame,
    daily_ic: pd.DataFrame,
    quantile_returns: pd.DataFrame,
    quantile_returns_by_date: pd.DataFrame | None = None,
    five_bucket_returns: pd.DataFrame | None = None,
    portfolio_returns: pd.DataFrame | None = None,
    summary: pd.DataFrame | None = None,
) -> dict[str, Path]:
    factor_dir = Path(factor_dir)
    factor_dir.mkdir(parents=True, exist_ok=True)

    paths = {
        "clean_factor_data": factor_dir / "clean_factor_data.parquet",
        "daily_ic": factor_dir / "daily_ic.parquet",
        "quantile_returns": factor_dir / "quantile_returns.parquet",
    }
    clean_factor_data.to_parquet(paths["clean_factor_data"])
    daily_ic.to_parquet(paths["daily_ic"])
    quantile_returns.to_parquet(paths["quantile_returns"])
    if summary is not None:
        paths["summary"] = factor_dir / "summary.csv"
        summary.to_csv(paths["summary"], index=False)
    optional_frames = {
        "quantile_returns_by_date": quantile_returns_by_date,
        "five_bucket_returns": five_bucket_returns,
        "portfolio_returns": portfolio_returns,
    }
    for name, frame in optional_frames.items():
        if frame is not None:
            path = factor_dir / f"{name}.parquet"
            frame.to_parquet(path)
            paths[name] = path
    return paths


def write_run_summary(
    *,
    run_dir: str | Path,
    summary: pd.DataFrame,
    config: EvaluationRunConfig,
    run_id: str,
) -> dict[str, Path]:
    run_dir = Path(run_dir)
    run_dir.mkdir(parents=True, exist_ok=True)

    paths = {
        "summary_csv": run_dir / "summary.csv",
        "summary_parquet": run_dir / "summary.parquet",
        "metadata": run_dir / "metadata.json",
    }
    summary.to_csv(paths["summary_csv"], index=False)
    summary.to_parquet(paths["summary_parquet"], index=False)
    metadata = _build_metadata(config=config, run_id=run_id)
    metadata["effective_end_date"] = _effective_end_date(summary)
    paths["metadata"].write_text(
        json.dumps(metadata, indent=2, default=str) + "\n"
    )
    return paths


def write_run_manifest(*, run, summary: pd.DataFrame) -> Path:
    config = run.config
    fingerprint_payload = json.dumps(
        {
            "factor_names": list(config.factor_names),
            "start_date": config.start_date,
            "end_date": config.end_date,
            "universe": config.universe,
            "periods": list(config.periods),
            "return_type": config.return_type,
            "quantiles": config.quantiles,
            "transaction_cost_bps": config.transaction_cost_bps,
        },
        sort_keys=True,
    ).encode("utf-8")
    factor_rows = []
    contracts = {}
    try:
        from microfactor.factors.catalog import load_catalog_metadata

        contracts = {
            item.name: {
                "inputs": list(item.inputs),
                "adjust": item.adjust,
                "category": item.category,
                "source": item.source,
                "implementation": item.implementation,
                "source_status": item.status,
            }
            for item in load_catalog_metadata()
        }
    except (ImportError, OSError):
        contracts = {}
    for factor_name in config.factor_names:
        rows = summary.loc[summary["factor_name"].astype(str) == factor_name]
        status = "insufficient_data" if rows.empty else "rejected"
        error = None
        if not rows.empty:
            row = rows.iloc[0]
            if str(row.get("status", "")) == "failed":
                status = "failed"
                error = str(row.get("error", ""))
            elif int(row.get("sample_count", 0) or 0) == 0:
                status = "insufficient_data"
            elif bool(row.get("passed", False)):
                status = "passed"
            metrics = {
                key: _native_metric(row[key])
                for key in (
                    "IC Mean",
                    "adjusted_ICIR",
                    "directional_IC>0 %",
                    "long_short_spread_bps",
                    "sample_count",
                )
                if key in row.index
            }
        else:
            metrics = {}
        factor_rows.append(
            {
                "factor_name": factor_name,
                "status": status,
                "metrics": metrics,
                "result_path": str(run.factor_dir(factor_name)),
                "error": error,
            }
        )
    payload = {
        "run_id": run.run_id,
        "factor_names": list(config.factor_names),
        "universe": config.universe,
        "start_date": config.start_date,
        "end_date": config.end_date,
        "effective_end_date": _effective_end_date(summary),
        "periods": list(config.periods),
        "quantiles": config.quantiles,
        "return_type": config.return_type,
        "max_loss": config.max_loss,
        "transaction_cost_bps": config.transaction_cost_bps,
        "input_fingerprint": hashlib.sha256(fingerprint_payload).hexdigest(),
        "factor_contracts": {
            name: contracts[name]
            for name in config.factor_names
            if name in contracts
        },
        "factors": factor_rows,
    }
    path = run.run_dir / "manifest.json"
    path.write_text(json.dumps(payload, indent=2, default=str) + "\n", encoding="utf-8")
    return path


def _effective_end_date(summary: pd.DataFrame) -> str | None:
    if summary.empty or "end_date" not in summary.columns:
        return None
    values = summary["end_date"].dropna().astype(str)
    return max(values) if not values.empty else None


def _native_metric(value: object) -> object:
    """Convert NumPy scalar values before serializing registry metadata."""
    return value.item() if hasattr(value, "item") else value


def _build_metadata(*, config: EvaluationRunConfig, run_id: str) -> dict[str, object]:
    return {
        "run_id": run_id,
        "factor_names": list(config.factor_names),
        "start_date": config.start_date,
        "end_date": config.end_date,
        "periods": list(config.periods),
        "quantiles": config.quantiles,
        "return_type": config.return_type,
        "max_loss": config.max_loss,
        "universe": config.universe,
        "rolling_ic_window": config.rolling_ic_window,
        "transaction_cost_bps": config.transaction_cost_bps,
    }
