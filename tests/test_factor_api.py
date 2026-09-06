from pathlib import Path

import pandas as pd
import pytest

from microfactor.api import LocalFactor
from microfactor.storage import FactorDataIntegrityError, FactorStorage


def _frame(values=(1.0, 2.0)):
    return pd.DataFrame(
        {
            "trade_date": ["20240101", "20240102"],
            "ts_code": ["000001.SZ", "000001.SZ"],
            "value": list(values),
        }
    )


def _contract(name: str):
    return {
        "name": name,
        "formula": f"{name} formula",
        "inputs": ["close"],
        "adjust": "hfq",
        "category": "price",
        "status": "candidate",
        "source": "test",
        "direction": "positive",
        "implementation": "tests",
    }


def test_local_factor_returns_long_and_wide_data(tmp_path: Path):
    storage = FactorStorage(tmp_path / "factors", tmp_path / "meta.duckdb")
    storage.publish_factor("momentum", _frame(), contract=_contract("momentum"))
    storage.publish_factor(
        "inverse_pb",
        _frame((3.0, 4.0)),
        contract=_contract("inverse_pb"),
    )
    api = LocalFactor(storage)

    long = api.factor("momentum", ts_code="000001.SZ", start_date="20240102")
    assert long.to_dict("records") == [
        {"trade_date": "20240102", "ts_code": "000001.SZ", "value": 2.0}
    ]

    wide = api.query(
        "factor",
        factor_name=["momentum", "inverse_pb"],
        format="wide",
    )
    assert wide.columns.tolist() == ["trade_date", "ts_code", "momentum", "inverse_pb"]
    assert wide["inverse_pb"].tolist() == [3.0, 4.0]


def test_local_factor_evaluation_uses_latest_complete_run(tmp_path: Path):
    storage = FactorStorage(tmp_path / "factors", tmp_path / "meta.duckdb")
    storage.publish_factor("momentum", _frame(), contract=_contract("momentum"))
    storage.register_evaluation_run(
        "run_partial",
        status="partial",
        factor_count=1,
        completed_count=0,
    )
    storage.register_evaluation(
        "run_partial",
        "momentum",
        "failed",
        metrics={"IC Mean": 0.0},
    )
    storage.register_evaluation_run(
        "run_complete",
        status="completed",
        factor_count=1,
        completed_count=1,
    )
    storage.register_evaluation(
        "run_complete",
        "momentum",
        "rejected",
        metrics={"IC Mean": 0.03},
        factor_version=storage.latest_version_id("momentum"),
    )
    api = LocalFactor(storage)

    result = api.factor_evaluation("momentum")
    assert len(result) == 1
    assert result.loc[0, "run_id"] == "run_complete"
    assert result.loc[0, "status"] == "rejected"
    assert result.loc[0, "IC Mean"] == pytest.approx(0.03)

    assert api.factor_evaluation("momentum", status="passed").empty


def test_publish_factor_rejects_conflicting_overlap(tmp_path: Path):
    storage = FactorStorage(tmp_path / "factors", tmp_path / "meta.duckdb")
    storage.publish_factor("momentum", _frame(), contract=_contract("momentum"))

    with pytest.raises(FactorDataIntegrityError, match="conflicting values"):
        storage.publish_factor(
            "momentum",
            _frame((9.0, 2.0)),
            contract=_contract("momentum"),
        )


def test_local_factor_bootstraps_legacy_partitions(tmp_path: Path):
    storage = FactorStorage(tmp_path / "factors", tmp_path / "meta.duckdb")
    storage.write("legacy_factor", _frame())

    api = LocalFactor(storage)
    basic = api.factor_basic("legacy_factor")
    assert len(basic) == 1
    assert basic.loc[0, "version_id"].startswith("legacy_")
    assert api.factor("legacy_factor").shape[0] == 2
