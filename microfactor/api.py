"""Read-only query API for published Microfactor data and evaluations."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Literal, Sequence

import pandas as pd

from microfactor.config import load_config
from microfactor.storage import FactorStorage


class LocalFactor:
    """Query published factor versions, metadata, and evaluation results."""

    def __init__(self, storage: FactorStorage):
        self._storage = storage
        self._storage.migrate()

    def factor(
        self,
        factor_name: str | Sequence[str],
        *,
        start_date: str | None = None,
        end_date: str | None = None,
        ts_code: str | Sequence[str] | None = None,
        version: str = "latest",
        fields: Sequence[str] = ("trade_date", "ts_code", "value"),
        format: Literal["long", "wide"] = "long",
    ) -> pd.DataFrame:
        names = _names(factor_name)
        if format not in {"long", "wide"}:
            raise ValueError("format must be 'long' or 'wide'")
        requested = tuple(fields)
        if set(requested) - {"trade_date", "ts_code", "value"}:
            raise ValueError("factor fields must be trade_date, ts_code, and value")
        if set(requested) != {"trade_date", "ts_code", "value"}:
            raise ValueError("factor fields must include trade_date, ts_code, and value")
        if len(names) > 1 and format == "long":
            raise ValueError("multiple factors require format='wide'")
        codes = _codes(ts_code)
        frames: list[pd.DataFrame] = []
        for name in names:
            frame = self._storage.read_versioned(
                name,
                start_date=start_date,
                end_date=end_date,
                version=version,
            )
            if codes is not None:
                frame = frame[frame["ts_code"].isin(codes)]
            if frame.duplicated(["trade_date", "ts_code"]).any():
                raise ValueError(f"{name}: duplicate trade_date/ts_code keys")
            if frame["value"].isna().any():
                raise ValueError(f"{name}: factor contains NaN values")
            frame["trade_date"] = frame["trade_date"].astype(str)
            frame["ts_code"] = frame["ts_code"].astype(str)
            frame["factor_name"] = name
            frames.append(frame)
        if format == "long":
            return frames[0][["trade_date", "ts_code", "value"]].reset_index(drop=True)
        if not frames:
            return pd.DataFrame(columns=["trade_date", "ts_code"])
        result = frames[0][["trade_date", "ts_code", "value"]].rename(
            columns={"value": names[0]}
        )
        for name, frame in zip(names[1:], frames[1:], strict=False):
            values = frame[["trade_date", "ts_code", "value"]].rename(
                columns={"value": name}
            )
            result = result.merge(values, on=["trade_date", "ts_code"], how="outer")
        return result.sort_values(["trade_date", "ts_code"]).reset_index(drop=True)

    def factor_basic(
        self,
        factor_name: str | Sequence[str] | None = None,
        *,
        category: str | None = None,
        source_status: str | None = None,
        evaluation_status: str | None = None,
        version: str = "latest",
    ) -> pd.DataFrame:
        names = _names(factor_name) if factor_name is not None else None
        versions = self._storage.factor_versions()
        if versions.empty:
            return _empty_basic_frame()
        if version == "latest":
            versions = versions[versions["is_latest"] == True]  # noqa: E712
        else:
            versions = versions[versions["version_id"] == version]
        if names is not None:
            versions = versions[versions["factor_name"].isin(names)]
        if category is not None:
            versions = versions[versions["category"] == category]
        if source_status is not None:
            versions = versions[versions["source_status"] == source_status]
        if versions.empty:
            return _empty_basic_frame()
        versions = versions.sort_values(["factor_name", "published_at"])
        latest_eval = self._latest_evaluations()
        result = versions.merge(
            latest_eval[["factor_name", "status"]].rename(
                columns={"status": "evaluation_status"}
            ),
            on="factor_name",
            how="left",
        )
        result["inputs"] = result["inputs_json"].map(_parse_json_list)
        if evaluation_status is not None:
            result = result[result["evaluation_status"] == evaluation_status]
        columns = [
            "factor_name",
            "version_id",
            "publication_status",
            "source_status",
            "evaluation_status",
            "category",
            "formula",
            "direction",
            "source",
            "implementation",
            "inputs",
            "adjust",
            "start_date",
            "end_date",
            "row_count",
            "contract_fingerprint",
            "data_fingerprint",
            "manifest_path",
        ]
        return result[
            [column for column in columns if column in result.columns]
        ].reset_index(drop=True)

    def factor_evaluation(
        self,
        factor_name: str | Sequence[str] | None = None,
        *,
        run_id: str = "latest",
        status: str | None = None,
    ) -> pd.DataFrame:
        names = _names(factor_name) if factor_name is not None else None
        runs = self._storage.evaluation_runs()
        if run_id == "latest":
            runs = runs[runs["status"] == "completed"]
            if names is not None and not runs.empty:
                available = self._storage.evaluation_registry()
                available = available[available["run_id"].isin(runs["run_id"])]
                complete_ids = []
                for candidate in runs["run_id"].astype(str):
                    present = set(available.loc[available["run_id"] == candidate, "factor_name"])
                    if set(names).issubset(present):
                        complete_ids.append(candidate)
                runs = runs[runs["run_id"].astype(str).isin(complete_ids)]
            if runs.empty:
                return _empty_evaluation_frame()
            run_id = str(runs.sort_values("run_id").iloc[-1]["run_id"])
        elif not runs.empty and run_id not in set(runs["run_id"].astype(str)):
            # An exact historical run may predate the evaluation_runs table;
            # the registry is still authoritative for that explicit lookup.
            pass

        rows = self._storage.evaluation_registry(run_id)
        if rows.empty:
            return _empty_evaluation_frame()
        if names is not None:
            rows = rows[rows["factor_name"].isin(names)]
        if status is not None:
            rows = rows[rows["status"] == status]
        if rows.empty:
            return _empty_evaluation_frame()
        expanded = rows.apply(_expand_evaluation_row, axis=1, result_type="expand").reset_index(
            drop=True
        )
        result = pd.concat([rows.reset_index(drop=True), expanded], axis=1)
        run_rows = self._storage.evaluation_runs()
        if not run_rows.empty:
            run_row = run_rows[run_rows["run_id"].astype(str) == str(run_id)]
            if not run_row.empty:
                run_info = run_row.iloc[0]
                result["run_status"] = run_info.get("status")
                result["run_manifest_path"] = run_info.get("manifest_path")
                result["run_report_path"] = run_info.get("report_path")
                run_config = _parse_json_object(run_info.get("config_json"))
                for key, value in run_config.items():
                    column = f"evaluation_{key}"
                    if column not in result:
                        result[column] = (
                            [value] * len(result)
                            if isinstance(value, (list, dict, tuple))
                            else value
                        )
                result["factor_version"] = result["factor_version"].fillna(
                    result["factor_name"].map(self._storage.latest_version_id)
                )
        return result.reset_index(drop=True)

    def factor_runs(
        self,
        factor_name: str | None = None,
        *,
        status: str | None = None,
    ) -> pd.DataFrame:
        runs = self._storage.evaluation_runs()
        if runs.empty:
            return runs
        if factor_name is not None:
            registry = self._storage.evaluation_registry()
            ids = registry.loc[registry["factor_name"] == factor_name, "run_id"]
            runs = runs[runs["run_id"].isin(ids)]
        if status is not None:
            runs = runs[runs["status"] == status]
        return runs.reset_index(drop=True)

    def query(self, api_name: str, **kwargs) -> pd.DataFrame:
        methods = {
            "factor": self.factor,
            "factor_basic": self.factor_basic,
            "factor_evaluation": self.factor_evaluation,
            "factor_runs": self.factor_runs,
        }
        try:
            method = methods[api_name]
        except KeyError as exc:
            raise ValueError(f"unknown api: {api_name}") from exc
        return method(**kwargs)

    def _latest_evaluations(self) -> pd.DataFrame:
        rows = self._storage.evaluation_registry()
        if rows.empty:
            return pd.DataFrame(columns=["factor_name", "status"])
        runs = self._storage.evaluation_runs()
        if not runs.empty:
            completed = set(runs.loc[runs["status"] == "completed", "run_id"].astype(str))
            rows = rows[rows["run_id"].astype(str).isin(completed)]
        if rows.empty:
            return pd.DataFrame(columns=["factor_name", "status"])
        return rows.sort_values("run_id").drop_duplicates("factor_name", keep="last")


def factor_api(
    config_path: str | Path = "config/settings.toml",
    *,
    factor_dir: str | Path | None = None,
    db_path: str | Path | None = None,
) -> LocalFactor:
    config = load_config(Path(config_path))
    storage = FactorStorage(
        Path(factor_dir) if factor_dir is not None else config.factor_dir,
        Path(db_path) if db_path is not None else config.db_path,
    )
    return LocalFactor(storage)


def _names(value: str | Sequence[str] | None) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        values = value.split(",")
    else:
        values = list(value)
    names = [str(item).strip() for item in values if str(item).strip()]
    if not names:
        raise ValueError("factor_name must not be empty")
    return list(dict.fromkeys(names))


def _codes(value: str | Sequence[str] | None) -> set[str] | None:
    if value is None:
        return None
    if isinstance(value, str):
        values = value.split(",")
    else:
        values = value
    codes = {str(item).strip() for item in values if str(item).strip()}
    return codes or None


def _parse_json_list(value: object) -> list[object]:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return []
    if isinstance(value, list):
        return value
    try:
        parsed = json.loads(str(value))
    except (TypeError, json.JSONDecodeError):
        return []
    return parsed if isinstance(parsed, list) else []


def _expand_evaluation_row(row: pd.Series) -> pd.Series:
    metrics = _parse_json_object(row.get("metrics_json"))
    config = _parse_json_object(row.get("evaluation_config_json"))
    values = {str(key): value for key, value in metrics.items()}
    values.update({f"evaluation_{key}": value for key, value in config.items()})
    return pd.Series(values)


def _parse_json_object(value: object) -> dict[str, object]:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return {}
    try:
        parsed = json.loads(str(value))
    except (TypeError, json.JSONDecodeError):
        return {}
    return parsed if isinstance(parsed, dict) else {}


def _empty_basic_frame() -> pd.DataFrame:
    return pd.DataFrame(
        columns=[
            "factor_name",
            "version_id",
            "publication_status",
            "source_status",
            "evaluation_status",
            "category",
            "formula",
            "direction",
            "source",
            "implementation",
            "inputs",
            "adjust",
            "start_date",
            "end_date",
            "row_count",
            "contract_fingerprint",
            "data_fingerprint",
            "manifest_path",
        ]
    )


def _empty_evaluation_frame() -> pd.DataFrame:
    return pd.DataFrame(
        columns=[
            "run_id",
            "factor_name",
            "factor_version",
            "status",
            "metrics_json",
            "evaluation_config_json",
            "result_path",
            "report_path",
            "error",
        ]
    )


__all__ = ["LocalFactor", "factor_api"]
