import hashlib
import json
import shutil
import tempfile
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

import duckdb
import pandas as pd
import pyarrow as pa
import pyarrow.dataset as ds
import pyarrow.parquet as pq


@dataclass(frozen=True)
class FactorStats:
    rows: int
    start_date: str
    end_date: str


@dataclass(frozen=True)
class FactorVersion:
    factor_name: str
    version_id: str
    publication_status: str
    start_date: str | None
    end_date: str | None
    row_count: int
    manifest_path: Path


class FactorDataIntegrityError(ValueError):
    """Raised when a published factor would silently change existing data."""


class FactorStorage:
    def __init__(self, factor_dir: Path, db_path: Path, init_db: bool = True):
        self._factor_dir = Path(factor_dir)
        self._db_path = Path(db_path)
        self._factor_dir.mkdir(parents=True, exist_ok=True)
        if init_db:
            self._db_path.parent.mkdir(parents=True, exist_ok=True)
            self._init_db()

    def _init_db(self):
        with duckdb.connect(str(self._db_path)) as con:
            con.execute("""
                CREATE TABLE IF NOT EXISTS factor_registry (
                    factor_name VARCHAR PRIMARY KEY,
                    last_updated TIMESTAMP DEFAULT now(),
                    version_id VARCHAR,
                    publication_status VARCHAR DEFAULT 'published',
                    source_status VARCHAR,
                    category VARCHAR,
                    formula VARCHAR,
                    direction VARCHAR,
                    source VARCHAR,
                    implementation VARCHAR,
                    inputs_json VARCHAR,
                    adjust VARCHAR,
                    storage_root VARCHAR,
                    manifest_path VARCHAR,
                    start_date VARCHAR,
                    end_date VARCHAR,
                    row_count BIGINT,
                    contract_fingerprint VARCHAR,
                    data_fingerprint VARCHAR,
                    latest_evaluation_status VARCHAR
                )
            """)
            con.execute("""
                CREATE TABLE IF NOT EXISTS factor_evaluation_registry (
                    run_id VARCHAR,
                    factor_name VARCHAR,
                    status VARCHAR NOT NULL,
                    metrics_json VARCHAR,
                    result_path VARCHAR,
                    error VARCHAR,
                    factor_version VARCHAR,
                    evaluation_config_json VARCHAR,
                    report_path VARCHAR,
                    recorded_at TIMESTAMP DEFAULT now(),
                    PRIMARY KEY (run_id, factor_name)
                )
            """)
            con.execute("""
                CREATE TABLE IF NOT EXISTS factor_versions (
                    factor_name VARCHAR,
                    version_id VARCHAR,
                    contract_fingerprint VARCHAR,
                    data_fingerprint VARCHAR,
                    source_status VARCHAR,
                    publication_status VARCHAR NOT NULL,
                    category VARCHAR,
                    formula VARCHAR,
                    direction VARCHAR,
                    source VARCHAR,
                    implementation VARCHAR,
                    inputs_json VARCHAR,
                    adjust VARCHAR,
                    storage_root VARCHAR,
                    manifest_path VARCHAR,
                    start_date VARCHAR,
                    end_date VARCHAR,
                    row_count BIGINT,
                    created_at TIMESTAMP DEFAULT now(),
                    published_at TIMESTAMP,
                    is_latest BOOLEAN DEFAULT false,
                    PRIMARY KEY (factor_name, version_id)
                )
            """)
            con.execute("""
                CREATE TABLE IF NOT EXISTS evaluation_runs (
                    run_id VARCHAR PRIMARY KEY,
                    status VARCHAR NOT NULL,
                    factor_count INTEGER,
                    completed_count INTEGER,
                    config_json VARCHAR,
                    manifest_path VARCHAR,
                    report_path VARCHAR,
                    started_at TIMESTAMP,
                    finished_at TIMESTAMP
                )
            """)

            # Existing databases predate the versioned schema. DuckDB supports
            # idempotent column additions, so an upgrade never drops data.
            factor_columns = {
                "version_id": "VARCHAR",
                "publication_status": "VARCHAR DEFAULT 'published'",
                "source_status": "VARCHAR",
                "category": "VARCHAR",
                "formula": "VARCHAR",
                "direction": "VARCHAR",
                "source": "VARCHAR",
                "implementation": "VARCHAR",
                "inputs_json": "VARCHAR",
                "adjust": "VARCHAR",
                "storage_root": "VARCHAR",
                "manifest_path": "VARCHAR",
                "start_date": "VARCHAR",
                "end_date": "VARCHAR",
                "row_count": "BIGINT",
                "contract_fingerprint": "VARCHAR",
                "data_fingerprint": "VARCHAR",
                "latest_evaluation_status": "VARCHAR",
            }
            for name, dtype in factor_columns.items():
                con.execute(f"ALTER TABLE factor_registry ADD COLUMN IF NOT EXISTS {name} {dtype}")
            eval_columns = {
                "factor_version": "VARCHAR",
                "evaluation_config_json": "VARCHAR",
                "report_path": "VARCHAR",
            }
            for name, dtype in eval_columns.items():
                con.execute(
                    "ALTER TABLE factor_evaluation_registry "
                    f"ADD COLUMN IF NOT EXISTS {name} {dtype}"
                )

    def register_evaluation(
        self,
        run_id: str,
        factor_name: str,
        status: str,
        *,
        metrics: dict[str, object] | None = None,
        result_path: str | Path | None = None,
        error: str | None = None,
        factor_version: str | None = None,
        evaluation_config: dict[str, object] | None = None,
        report_path: str | Path | None = None,
    ) -> None:
        with duckdb.connect(str(self._db_path)) as con:
            con.execute(
                """
                INSERT INTO factor_evaluation_registry
                    (run_id, factor_name, status, metrics_json, result_path, error,
                     factor_version, evaluation_config_json, report_path)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT (run_id, factor_name) DO UPDATE SET
                    status=excluded.status,
                    metrics_json=excluded.metrics_json,
                    result_path=excluded.result_path,
                    error=excluded.error,
                    factor_version=excluded.factor_version,
                    evaluation_config_json=excluded.evaluation_config_json,
                    report_path=excluded.report_path,
                    recorded_at=now()
                """,
                [
                    run_id,
                    factor_name,
                    status,
                    json.dumps(metrics or {}, default=str),
                    str(result_path) if result_path is not None else None,
                    error,
                    factor_version,
                    json.dumps(evaluation_config or {}, default=str),
                    str(report_path) if report_path is not None else None,
                ],
            )

    def evaluation_registry(self, run_id: str | None = None) -> pd.DataFrame:
        with duckdb.connect(str(self._db_path)) as con:
            query = "SELECT * FROM factor_evaluation_registry"
            params: list[object] = []
            if run_id is not None:
                query += " WHERE run_id = ?"
                params.append(run_id)
            query += " ORDER BY run_id, factor_name"
            return con.execute(query, params).fetchdf()

    def register_evaluation_run(
        self,
        run_id: str,
        *,
        status: str,
        factor_count: int,
        completed_count: int,
        config: dict[str, object] | None = None,
        manifest_path: str | Path | None = None,
        report_path: str | Path | None = None,
        started_at: datetime | None = None,
        finished_at: datetime | None = None,
    ) -> None:
        with duckdb.connect(str(self._db_path)) as con:
            con.execute(
                """
                INSERT INTO evaluation_runs
                    (run_id, status, factor_count, completed_count, config_json,
                     manifest_path, report_path, started_at, finished_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT (run_id) DO UPDATE SET
                    status=excluded.status,
                    factor_count=excluded.factor_count,
                    completed_count=excluded.completed_count,
                    config_json=excluded.config_json,
                    manifest_path=excluded.manifest_path,
                    report_path=excluded.report_path,
                    started_at=excluded.started_at,
                    finished_at=excluded.finished_at
                """,
                [
                    run_id,
                    status,
                    factor_count,
                    completed_count,
                    json.dumps(config or {}, default=str),
                    str(manifest_path) if manifest_path is not None else None,
                    str(report_path) if report_path is not None else None,
                    started_at,
                    finished_at,
                ],
            )
            con.execute(
                """
                UPDATE factor_registry AS f
                SET latest_evaluation_status = (
                    SELECT e.status
                    FROM factor_evaluation_registry AS e
                    JOIN evaluation_runs AS r ON r.run_id = e.run_id
                    WHERE e.factor_name = f.factor_name
                      AND r.status = 'completed'
                    ORDER BY e.run_id DESC
                    LIMIT 1
                )
                WHERE EXISTS (
                    SELECT 1
                    FROM factor_evaluation_registry AS e
                    JOIN evaluation_runs AS r ON r.run_id = e.run_id
                    WHERE e.factor_name = f.factor_name
                      AND r.status = 'completed'
                )
                """
            )

    def evaluation_runs(self) -> pd.DataFrame:
        with duckdb.connect(str(self._db_path)) as con:
            return con.execute("SELECT * FROM evaluation_runs ORDER BY run_id").fetchdf()

    def write_partitions(self, factor_name: str, df: pd.DataFrame) -> None:
        required = {"trade_date", "ts_code", "value"}
        if not required.issubset(df.columns):
            raise ValueError(f"DataFrame must have columns: {required}")

        factor_path = self._factor_dir / factor_name
        factor_path.mkdir(parents=True, exist_ok=True)
        if df.empty:
            for partition in factor_path.glob("date=*"):
                if partition.is_dir():
                    shutil.rmtree(partition)
            return
        frame = df[["ts_code", "value"]].reset_index(drop=True)
        frame["date"] = df["trade_date"].astype(str).to_numpy()
        ds.write_dataset(
            pa.Table.from_pandas(frame, preserve_index=False),
            base_dir=str(factor_path),
            format="parquet",
            partitioning=ds.partitioning(
                pa.schema([("date", pa.string())]), flavor="hive"
            ),
            existing_data_behavior="delete_matching",
            basename_template="data-{i}.parquet",
        )

    def register(self, factor_name: str) -> None:
        with duckdb.connect(str(self._db_path)) as con:
            con.execute("""
                INSERT INTO factor_registry (factor_name) VALUES (?)
                ON CONFLICT (factor_name) DO UPDATE SET last_updated = now()
            """, [factor_name])

    def write(self, factor_name: str, df: pd.DataFrame) -> None:
        self.write_partitions(factor_name, df)
        self.register(factor_name)

    def publish_factor(
        self,
        factor_name: str,
        df: pd.DataFrame,
        *,
        contract: object | dict[str, object] | None = None,
        compute_run_id: str | None = None,
        universe: str | None = None,
        input_fingerprint: str | None = None,
        new_version: bool = False,
    ) -> FactorVersion:
        """Publish an append-only factor version with conflict detection.

        Existing dates are never overwritten. Identical overlapping rows are
        treated as idempotent; differing values raise FactorDataIntegrityError.
        """
        required = {"trade_date", "ts_code", "value"}
        if not required.issubset(df.columns):
            raise ValueError(f"DataFrame must have columns: {required}")
        frame = df[["trade_date", "ts_code", "value"]].copy()
        frame["trade_date"] = frame["trade_date"].astype(str)
        frame["ts_code"] = frame["ts_code"].astype(str)
        if frame.duplicated(["trade_date", "ts_code"]).any():
            raise FactorDataIntegrityError(f"{factor_name}: duplicate factor keys")
        if frame["value"].isna().any():
            raise FactorDataIntegrityError(f"{factor_name}: factor contains NaN values")

        self._bootstrap_factor(factor_name)
        metadata = _normalize_contract(contract)
        contract_fingerprint = _contract_fingerprint(factor_name, metadata)
        current = self._latest_version_record(factor_name)
        if current is not None:
            current_contract = str(self._record_dict(current).get("contract_fingerprint") or "")
            if (
                current_contract
                and current_contract != contract_fingerprint
                and not new_version
            ):
                raise FactorDataIntegrityError(
                    f"{factor_name}: contract changed; pass "
                    "new_version=True to publish a new branch"
                )
            existing = self.read_versioned(factor_name, version="latest")
            if not new_version and not existing.empty and not frame.empty:
                overlap_keys = pd.MultiIndex.from_frame(
                    frame[["trade_date", "ts_code"]]
                ).intersection(
                    pd.MultiIndex.from_frame(existing[["trade_date", "ts_code"]])
                )
                if len(overlap_keys):
                    left = frame.set_index(["trade_date", "ts_code"]).loc[overlap_keys, "value"]
                    right = existing.set_index(["trade_date", "ts_code"]).loc[overlap_keys, "value"]
                    if not left.equals(right):
                        raise FactorDataIntegrityError(
                            f"{factor_name}: existing dates contain conflicting values"
                        )
                    frame_index = pd.MultiIndex.from_frame(frame[["trade_date", "ts_code"]])
                    frame = frame.loc[~frame_index.isin(overlap_keys)].reset_index(drop=True)
            if frame.empty and current is not None:
                return self._version_from_record(current)

        version_id = _make_version_id(
            factor_name,
            contract_fingerprint,
            frame,
            compute_run_id,
        )
        factor_path = self._factor_dir / factor_name
        if current is not None and new_version:
            root = factor_path / "versions" / version_id
        else:
            root = factor_path
        root.mkdir(parents=True, exist_ok=True)
        if not frame.empty:
            _write_partition_dataset(root, frame)

        old_manifest = (
            self._load_latest_manifest(factor_name)
            if current is not None and not new_version
            else None
        )
        partitions = list(old_manifest.get("partitions", [])) if old_manifest else []
        touched_dates = set(frame["trade_date"].astype(str)) if not frame.empty else set()
        partitions.extend(
            _partition_records(
                root,
                factor_path,
                dates=touched_dates or None,
                include_hash=True,
            )
        )
        partitions = _dedupe_partition_records(partitions)
        all_dates = [str(item["date"]) for item in partitions]
        data_fingerprint = _partition_fingerprint(partitions)
        payload = {
            "schema_version": 1,
            "factor_name": factor_name,
            "version_id": version_id,
            "contract_fingerprint": contract_fingerprint,
            "data_fingerprint": data_fingerprint,
            "compute_run_id": compute_run_id,
            "batch_run_id": compute_run_id,
            "formula": metadata.get("formula", ""),
            "inputs": metadata.get("inputs", []),
            "adjust": metadata.get("adjust"),
            "category": metadata.get("category", ""),
            "source_status": metadata.get("status", "candidate"),
            "source": metadata.get("source", ""),
            "direction": metadata.get("direction", "unspecified"),
            "implementation": metadata.get("implementation", ""),
            "universe": universe,
            "start_date": min(all_dates) if all_dates else None,
            "end_date": max(all_dates) if all_dates else None,
            "row_count": int(sum(int(item.get("row_count", 0)) for item in partitions)),
            "partitions": partitions,
            "input_fingerprint": input_fingerprint,
            "publication_status": "published",
            "status": "computed",
            "input_fields": metadata.get("inputs", []),
            "checks": _frame_checks(frame),
            "published_at": datetime.now().isoformat(timespec="seconds"),
        }
        manifests_dir = factor_path / "manifests"
        manifests_dir.mkdir(parents=True, exist_ok=True)
        manifest_path = manifests_dir / f"{version_id}.json"
        _atomic_write_json(manifest_path, payload)
        self._publish_version_record(payload, manifest_path, root)
        _atomic_write_json(
            factor_path / "latest.json",
            {"factor_name": factor_name, "version_id": version_id},
        )
        _atomic_write_json(factor_path / "compute_manifest.json", payload)
        return FactorVersion(
            factor_name=factor_name,
            version_id=version_id,
            publication_status="published",
            start_date=payload["start_date"],
            end_date=payload["end_date"],
            row_count=int(payload["row_count"]),
            manifest_path=manifest_path,
        )

    def read(
        self,
        factor_name: str,
        start_date: str | None = None,
        end_date: str | None = None,
    ) -> pd.DataFrame:
        factor_path = self._factor_dir / factor_name
        if not factor_path.exists():
            raise FileNotFoundError(f"Factor '{factor_name}' not found")
        if (factor_path / "latest.json").exists():
            return self.read_versioned(
                factor_name,
                start_date=start_date,
                end_date=end_date,
                version="latest",
            )

        pattern = str(factor_path / "date=*" / "*.parquet")
        if not list(factor_path.glob("date=*/*.parquet")):
            return pd.DataFrame(columns=["trade_date", "ts_code", "value"])
        where = []
        params: list = [pattern]
        if start_date:
            where.append("date >= ?")
            params.append(start_date)
        if end_date:
            where.append("date <= ?")
            params.append(end_date)

        sql = (
            "SELECT CAST(date AS VARCHAR) AS trade_date, ts_code, value"
            " FROM read_parquet(?, hive_partitioning=true)"
        )
        if where:
            sql += " WHERE " + " AND ".join(where)
        sql += " ORDER BY trade_date, ts_code"

        return duckdb.connect().execute(sql, params).fetchdf()

    def read_versioned(
        self,
        factor_name: str,
        start_date: str | None = None,
        end_date: str | None = None,
        *,
        version: str = "latest",
    ) -> pd.DataFrame:
        manifest = self._manifest_for(factor_name, version)
        partitions = [
            str(self._factor_dir / factor_name / item["path"])
            for item in manifest.get("partitions", [])
        ]
        if not partitions:
            return pd.DataFrame(columns=["trade_date", "ts_code", "value"])
        where = []
        params: list[Any] = [partitions]
        if start_date:
            where.append("date >= ?")
            params.append(str(start_date))
        if end_date:
            where.append("date <= ?")
            params.append(str(end_date))
        sql = (
            "SELECT CAST(date AS VARCHAR) AS trade_date, ts_code, value "
            "FROM read_parquet(?, hive_partitioning=true)"
        )
        if where:
            sql += " WHERE " + " AND ".join(where)
        sql += " ORDER BY trade_date, ts_code"
        return duckdb.connect().execute(sql, params).fetchdf()

    def factor_versions(self, factor_name: str | None = None) -> pd.DataFrame:
        with duckdb.connect(str(self._db_path)) as con:
            if factor_name is None:
                return con.execute(
                    "SELECT * FROM factor_versions ORDER BY factor_name, published_at"
                ).fetchdf()
            return con.execute(
                "SELECT * FROM factor_versions WHERE factor_name = ? ORDER BY published_at",
                [factor_name],
            ).fetchdf()

    def latest_version_id(self, factor_name: str) -> str | None:
        record = self._latest_version_record(factor_name)
        if record is None:
            return None
        return str(self._record_dict(record).get("version_id"))

    def migrate(self) -> None:
        """Bootstrap version manifests and evaluation runs from existing outputs."""
        factor_paths = [
            path
            for path in self._factor_dir.iterdir()
            if path.is_dir()
            and not path.name.startswith("_")
            and list(path.glob("date=*/*.parquet"))
        ]
        evaluations_dir = self._factor_dir.parent / "evaluations"
        evaluation_paths = (
            [path for path in evaluations_dir.iterdir() if (path / "manifest.json").exists()]
            if evaluations_dir.exists()
            else []
        )
        with duckdb.connect(str(self._db_path), read_only=True) as con:
            version_factor_count = con.execute(
                "SELECT count(DISTINCT factor_name) FROM factor_versions"
            ).fetchone()[0]
            evaluation_run_count = con.execute(
                "SELECT count(*) FROM evaluation_runs"
            ).fetchone()[0]
        if (
            len(factor_paths) == version_factor_count
            and len(evaluation_paths) == evaluation_run_count
        ):
            self._backfill_evaluation_versions()
            return
        for factor_path in sorted(factor_paths):
            self._bootstrap_factor(factor_path.name)
        if evaluations_dir.exists():
            existing_runs = set(
                self.evaluation_runs().get("run_id", pd.Series(dtype=str)).astype(str)
            )
            for run_dir in sorted(evaluations_dir.iterdir()):
                manifest_path = run_dir / "manifest.json"
                if not manifest_path.exists():
                    continue
                try:
                    payload = json.loads(manifest_path.read_text(encoding="utf-8"))
                except (OSError, json.JSONDecodeError):
                    continue
                run_id = str(payload.get("run_id", run_dir.name))
                rows = payload.get("factors", [])
                statuses = {str(item.get("status", "")) for item in rows}
                completed_count = sum(
                    str(item.get("status", "")) in {"passed", "rejected"}
                    for item in rows
                )
                run_status = "completed" if statuses.issubset({"passed", "rejected"}) else "partial"
                config = {
                    key: payload.get(key)
                    for key in (
                        "universe",
                        "start_date",
                        "end_date",
                        "periods",
                        "quantiles",
                        "return_type",
                        "transaction_cost_bps",
                    )
                }
                if run_id in existing_runs:
                    self.register_evaluation_run(
                        run_id,
                        status=run_status,
                        factor_count=len(rows),
                        completed_count=completed_count,
                        config=config,
                        manifest_path=manifest_path,
                        report_path=run_dir / "report.html",
                    )
                    continue
                self.register_evaluation_run(
                    run_id,
                    status=run_status,
                    factor_count=len(rows),
                    completed_count=completed_count,
                    config=config,
                    manifest_path=manifest_path,
                    report_path=run_dir / "report.html",
                )
                for row in rows:
                    name = str(row.get("factor_name", ""))
                    if not name:
                        continue
                    result_path = row.get("result_path")
                    result_dir = Path(result_path) if result_path else run_dir / "factors" / name
                    if not result_dir.is_absolute():
                        project_root = self._factor_dir.parent.parent
                        result_dir = project_root / result_dir
                    self.register_evaluation(
                        run_id,
                        name,
                        str(row.get("status", "rejected")),
                        metrics=row.get("metrics", {}),
                        result_path=result_dir,
                        report_path=result_dir / "report.html",
                    )
        self._backfill_evaluation_versions()

    def _backfill_evaluation_versions(self) -> None:
        with duckdb.connect(str(self._db_path)) as con:
            con.execute(
                """
                UPDATE factor_evaluation_registry AS e
                SET factor_version = f.version_id
                FROM factor_registry AS f
                WHERE e.factor_version IS NULL
                  AND e.factor_name = f.factor_name
                """
            )

    def _bootstrap_factor(self, factor_name: str) -> None:
        if self._latest_version_record(factor_name) is not None:
            return
        factor_path = self._factor_dir / factor_name
        partitions = _partition_records(factor_path, factor_path, include_hash=False)
        if not partitions:
            return
        raw_manifest = factor_path / "compute_manifest.json"
        metadata: dict[str, Any] = {}
        if raw_manifest.exists():
            try:
                metadata = json.loads(raw_manifest.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                metadata = {}
        contract = _normalize_contract(metadata)
        contract_fp = str(
            metadata.get("contract_fingerprint")
            or _contract_fingerprint(factor_name, contract)
        )
        data_fp = _partition_fingerprint(partitions)
        version_id = f"legacy_{data_fp[:12]}"
        payload = {
            "schema_version": 1,
            "factor_name": factor_name,
            "version_id": version_id,
            "contract_fingerprint": contract_fp,
            "data_fingerprint": data_fp,
            "compute_run_id": metadata.get("batch_run_id"),
            "formula": metadata.get("formula", ""),
            "inputs": metadata.get("inputs", []),
            "adjust": metadata.get("adjust"),
            "category": metadata.get("category", ""),
            "source_status": metadata.get("source_status", "candidate"),
            "source": metadata.get("source", ""),
            "direction": metadata.get("direction", "unspecified"),
            "implementation": metadata.get("implementation", ""),
            "universe": metadata.get("universe"),
            "start_date": min(item["date"] for item in partitions),
            "end_date": max(item["date"] for item in partitions),
            "row_count": int(sum(item["row_count"] for item in partitions)),
            "partitions": partitions,
            "checks": metadata.get("checks", {}),
            "publication_status": "published",
        }
        manifests_dir = factor_path / "manifests"
        manifests_dir.mkdir(parents=True, exist_ok=True)
        manifest_path = manifests_dir / f"{version_id}.json"
        _atomic_write_json(manifest_path, payload)
        self._publish_version_record(payload, manifest_path, factor_path)
        _atomic_write_json(
            factor_path / "latest.json",
            {"factor_name": factor_name, "version_id": version_id},
        )

    def _publish_version_record(
        self,
        payload: dict[str, Any],
        manifest_path: Path,
        root: Path,
    ) -> None:
        factor_name = str(payload["factor_name"])
        version_id = str(payload["version_id"])
        with duckdb.connect(str(self._db_path)) as con:
            con.execute("BEGIN TRANSACTION")
            con.execute(
                "UPDATE factor_versions SET is_latest=false WHERE factor_name=?",
                [factor_name],
            )
            con.execute(
                """
                INSERT INTO factor_versions
                    (factor_name, version_id, contract_fingerprint, data_fingerprint,
                     source_status, publication_status, category, formula, direction,
                     source, implementation, inputs_json, adjust, storage_root,
                     manifest_path, start_date, end_date, row_count, published_at, is_latest)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, now(), true)
                ON CONFLICT (factor_name, version_id) DO UPDATE SET
                    data_fingerprint=excluded.data_fingerprint,
                    publication_status=excluded.publication_status,
                    manifest_path=excluded.manifest_path,
                    end_date=excluded.end_date,
                    row_count=excluded.row_count,
                    published_at=now(),
                    is_latest=true
                """,
                [
                    factor_name,
                    version_id,
                    payload.get("contract_fingerprint"),
                    payload.get("data_fingerprint"),
                    payload.get("source_status"),
                    payload.get("publication_status", "published"),
                    payload.get("category"),
                    payload.get("formula"),
                    payload.get("direction"),
                    payload.get("source"),
                    payload.get("implementation"),
                    json.dumps(payload.get("inputs", []), ensure_ascii=False),
                    payload.get("adjust"),
                    str(root),
                    str(manifest_path),
                    payload.get("start_date"),
                    payload.get("end_date"),
                    int(payload.get("row_count", 0)),
                ],
            )
            con.execute(
                """
                INSERT INTO factor_registry
                    (factor_name, version_id, publication_status, source_status,
                     category, formula, direction, source, implementation, inputs_json,
                     adjust, storage_root, manifest_path, start_date, end_date,
                     row_count, contract_fingerprint, data_fingerprint, last_updated)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, now())
                ON CONFLICT (factor_name) DO UPDATE SET
                    version_id=excluded.version_id,
                    publication_status=excluded.publication_status,
                    source_status=excluded.source_status,
                    category=excluded.category,
                    formula=excluded.formula,
                    direction=excluded.direction,
                    source=excluded.source,
                    implementation=excluded.implementation,
                    inputs_json=excluded.inputs_json,
                    adjust=excluded.adjust,
                    storage_root=excluded.storage_root,
                    manifest_path=excluded.manifest_path,
                    start_date=excluded.start_date,
                    end_date=excluded.end_date,
                    row_count=excluded.row_count,
                    contract_fingerprint=excluded.contract_fingerprint,
                    data_fingerprint=excluded.data_fingerprint,
                    last_updated=now()
                """,
                [
                    factor_name,
                    version_id,
                    payload.get("publication_status", "published"),
                    payload.get("source_status"),
                    payload.get("category"),
                    payload.get("formula"),
                    payload.get("direction"),
                    payload.get("source"),
                    payload.get("implementation"),
                    json.dumps(payload.get("inputs", []), ensure_ascii=False),
                    payload.get("adjust"),
                    str(root),
                    str(manifest_path),
                    payload.get("start_date"),
                    payload.get("end_date"),
                    int(payload.get("row_count", 0)),
                    payload.get("contract_fingerprint"),
                    payload.get("data_fingerprint"),
                ],
            )
            con.execute("COMMIT")

    def _latest_version_record(self, factor_name: str):
        with duckdb.connect(str(self._db_path), read_only=False) as con:
            return con.execute(
                "SELECT * FROM factor_versions WHERE factor_name=? AND is_latest=true LIMIT 1",
                [factor_name],
            ).fetchone()

    def _record_dict(self, record) -> dict[str, Any]:
        columns = [
            item[0]
            for item in duckdb.connect(str(self._db_path)).execute(
                "DESCRIBE factor_versions"
            ).fetchall()
        ]
        return dict(zip(columns, record, strict=False))

    def _version_from_record(self, record) -> FactorVersion:
        row = self._record_dict(record)
        return FactorVersion(
            factor_name=str(row["factor_name"]),
            version_id=str(row["version_id"]),
            publication_status=str(row["publication_status"]),
            start_date=row.get("start_date"),
            end_date=row.get("end_date"),
            row_count=int(row.get("row_count") or 0),
            manifest_path=Path(str(row["manifest_path"])),
        )

    def _load_latest_manifest(self, factor_name: str) -> dict[str, Any] | None:
        pointer = self._factor_dir / factor_name / "latest.json"
        if not pointer.exists():
            return None
        try:
            version_id = json.loads(pointer.read_text(encoding="utf-8"))["version_id"]
            return self._manifest_for(factor_name, version_id)
        except (OSError, KeyError, json.JSONDecodeError):
            return None

    def _manifest_for(self, factor_name: str, version: str) -> dict[str, Any]:
        factor_path = self._factor_dir / factor_name
        if not factor_path.exists():
            raise FileNotFoundError(f"Factor '{factor_name}' not found")
        if version == "latest":
            manifest = self._load_latest_manifest(factor_name)
            if manifest is None:
                self._bootstrap_factor(factor_name)
                manifest = self._load_latest_manifest(factor_name)
        else:
            manifest = None
            path = factor_path / "manifests" / f"{version}.json"
            if path.exists():
                try:
                    manifest = json.loads(path.read_text(encoding="utf-8"))
                except (OSError, json.JSONDecodeError) as exc:
                    raise ValueError(f"invalid factor manifest: {path}") from exc
        if manifest is None:
            raise KeyError(f"unknown factor version: {factor_name}@{version}")
        if manifest.get("publication_status") != "published":
            raise ValueError(f"factor version is not published: {factor_name}@{version}")
        return manifest

    def list_factors(self) -> list[str]:
        with duckdb.connect(str(self._db_path)) as con:
            rows = con.execute(
                "SELECT factor_name FROM factor_registry ORDER BY factor_name"
            ).fetchall()
        return [r[0] for r in rows]

    def factor_stats(self, factor_name: str) -> FactorStats | None:
        factor_path = self._factor_dir / factor_name
        if not factor_path.exists():
            return None
        if (factor_path / "latest.json").exists():
            record = self._latest_version_record(factor_name)
            if record is None:
                return None
            values = self._record_dict(record)
            if not values.get("row_count"):
                return None
            return FactorStats(
                rows=int(values["row_count"]),
                start_date=str(values["start_date"]),
                end_date=str(values["end_date"]),
            )
        partitions = sorted(factor_path.glob("date=*/*.parquet"))
        if not partitions:
            return None
        dates = sorted({p.parent.name.split("=")[1] for p in partitions})
        start_date = dates[0]
        end_date = dates[-1]
        pattern = str(factor_path / "date=*" / "*.parquet")
        row = duckdb.connect().execute(
            "SELECT count(*) AS rows FROM read_parquet(?)",
            [pattern],
        ).fetchone()
        if row is None or row[0] == 0:
            return None
        return FactorStats(rows=int(row[0]), start_date=start_date, end_date=end_date)


def _normalize_contract(contract: object | dict[str, object] | None) -> dict[str, object]:
    if contract is None:
        return {}
    if isinstance(contract, dict):
        raw = dict(contract)
    else:
        raw = {
            key: getattr(contract, key)
            for key in (
                "name",
                "formula",
                "inputs",
                "adjust",
                "category",
                "status",
                "source",
                "direction",
                "implementation",
            )
            if hasattr(contract, key)
        }
    if "inputs" in raw and raw["inputs"] is not None:
        raw["inputs"] = list(raw["inputs"])
    return raw


def _contract_fingerprint(factor_name: str, contract: dict[str, object]) -> str:
    payload = {
        "factor_name": factor_name,
        "formula": contract.get("formula", ""),
        "inputs": list(contract.get("inputs", []) or []),
        "adjust": contract.get("adjust"),
        "implementation": contract.get("implementation", ""),
    }
    return hashlib.sha256(
        json.dumps(payload, ensure_ascii=False, sort_keys=True, default=str).encode("utf-8")
    ).hexdigest()


def _make_version_id(
    factor_name: str,
    contract_fingerprint: str,
    frame: pd.DataFrame,
    compute_run_id: str | None,
) -> str:
    digest = hashlib.sha256()
    digest.update(factor_name.encode("utf-8"))
    digest.update(contract_fingerprint.encode("ascii"))
    if compute_run_id:
        digest.update(str(compute_run_id).encode("utf-8"))
    if not frame.empty:
        ordered = frame.sort_values(["trade_date", "ts_code"], kind="stable")
        digest.update(
            pd.util.hash_pandas_object(ordered, index=False).to_numpy().tobytes()
        )
    return f"v{datetime.now().strftime('%Y%m%d%H%M%S')}_{digest.hexdigest()[:12]}"


def _write_partition_dataset(root: Path, frame: pd.DataFrame) -> None:
    prepared = frame[["ts_code", "value"]].reset_index(drop=True).copy()
    prepared["date"] = frame["trade_date"].astype(str).to_numpy()
    stage = Path(tempfile.mkdtemp(prefix=f"{root.name}.", dir=str(root.parent)))
    try:
        ds.write_dataset(
            pa.Table.from_pandas(prepared, preserve_index=False),
            base_dir=str(stage),
            format="parquet",
            partitioning=ds.partitioning(
                pa.schema([("date", pa.string())]), flavor="hive"
            ),
            existing_data_behavior="error",
            basename_template="data-{i}.parquet",
        )
        for staged_date in sorted(stage.glob("date=*")):
            target_date = root / staged_date.name
            if target_date.exists():
                old = pd.read_parquet(target_date)
                new = pd.read_parquet(staged_date)
                merged = pd.concat([old, new], ignore_index=True)
                merged = merged.drop_duplicates(["ts_code"], keep="last")
                merged_stage = Path(tempfile.mkdtemp(prefix="merge.", dir=str(root.parent)))
                try:
                    _write_partition_dataset(
                        merged_stage,
                        _with_trade_date(merged, staged_date.name),
                    )
                    shutil.rmtree(target_date)
                    shutil.move(str(merged_stage / staged_date.name), str(target_date))
                finally:
                    shutil.rmtree(merged_stage, ignore_errors=True)
            else:
                root.mkdir(parents=True, exist_ok=True)
                shutil.move(str(staged_date), str(target_date))
    finally:
        shutil.rmtree(stage, ignore_errors=True)


def _with_trade_date(frame: pd.DataFrame, partition_name: str) -> pd.DataFrame:
    result = frame.copy()
    result["trade_date"] = partition_name.split("=", 1)[1]
    return result[["trade_date", "ts_code", "value"]]


def _partition_records(
    root: Path,
    factor_root: Path,
    *,
    dates: set[str] | None = None,
    include_hash: bool = True,
) -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    for path in sorted(root.glob("date=*/*.parquet")):
        date = path.parent.name.split("=", 1)[1]
        if dates is not None and date not in dates:
            continue
        file_hash = hashlib.sha256(path.read_bytes()).hexdigest() if include_hash else None
        records.append(
            {
                "date": date,
                "path": path.relative_to(factor_root).as_posix(),
                "rows": int(pq.ParquetFile(path).metadata.num_rows),
                "row_count": int(pq.ParquetFile(path).metadata.num_rows),
                "bytes": int(path.stat().st_size),
                "sha256": file_hash,
            }
        )
    return records


def _dedupe_partition_records(records: list[dict[str, object]]) -> list[dict[str, object]]:
    unique: dict[str, dict[str, object]] = {}
    for record in records:
        unique[str(record["path"])] = record
    return [unique[key] for key in sorted(unique)]


def _partition_fingerprint(records: list[dict[str, object]]) -> str:
    payload = [
        {
            "path": item.get("path"),
            "date": item.get("date"),
            "rows": item.get("rows", item.get("row_count")),
            "bytes": item.get("bytes"),
            "sha256": item.get("sha256"),
        }
        for item in sorted(records, key=lambda value: str(value.get("path")))
    ]
    return hashlib.sha256(
        json.dumps(payload, sort_keys=True, ensure_ascii=False).encode("utf-8")
    ).hexdigest()


def _frame_checks(frame: pd.DataFrame) -> dict[str, object]:
    if frame.empty:
        return {
            "row_count": 0,
            "duplicate_keys": 0,
            "nan_values": 0,
            "unique_dates": 0,
            "daily_coverage": {},
        }
    counts = frame["trade_date"].astype(str).value_counts().sort_index()
    return {
        "row_count": int(len(frame)),
        "duplicate_keys": int(frame.duplicated(["trade_date", "ts_code"]).sum()),
        "nan_values": int(frame["value"].isna().sum()),
        "unique_dates": int(frame["trade_date"].nunique()),
        "daily_coverage": {str(key): int(value) for key, value in counts.items()},
    }


def _atomic_write_json(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, default=str) + "\n",
        encoding="utf-8",
    )
    temporary.replace(path)
