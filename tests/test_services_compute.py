import pandas as pd

from microfactor.core import Factor, FactorFrame, FactorSpec, to_factor_output
from microfactor.factors.builtin import MARKET_CAP_FACTORS, RETURN_FACTORS
from microfactor.services.compute import (
    FactorComputeService,
    ZScorePostProcess,
    compute_catalog_factors,
)
from microfactor.storage import FactorStorage


class FakeProvider:
    def history(self, fields, start_date, end_date, universe, adjust, progress=None):
        assert fields == ["close", "open"]
        assert start_date == "20240101"
        assert end_date == "20240103"
        assert universe == "000001.SZ"
        assert adjust == "hfq"
        if progress is not None:
            progress(0, 1, "")
            progress(1, 1, "000001.SZ")

        index = pd.date_range("2024-01-01", periods=3, freq="D")
        open_ = pd.DataFrame({"000001.SZ": [10.0, 11.0, 12.0]}, index=index)
        close = pd.DataFrame({"000001.SZ": [10.5, 12.0, 12.6]}, index=index)
        return FactorFrame({"open": open_, "close": close})


class FakeMarketCapProvider:
    def history(self, fields, start_date, end_date, universe, adjust, progress=None):
        assert fields == ["circ_mv", "total_mv"]
        assert start_date == "20240101"
        assert end_date == "20240102"
        assert universe == "000001.SZ,000002.SZ"
        assert adjust is None

        index = pd.date_range("2024-01-01", periods=2, freq="D")
        total_mv = pd.DataFrame(
            {"000001.SZ": [100.0, 110.0], "000002.SZ": [200.0, 220.0]},
            index=index,
        )
        circ_mv = pd.DataFrame(
            {"000001.SZ": [50.0, 55.0], "000002.SZ": [80.0, 88.0]},
            index=index,
        )
        return FactorFrame({"total_mv": total_mv, "circ_mv": circ_mv})


def test_compute_and_store_return_factors(tmp_path):
    storage = FactorStorage(tmp_path / "factors", tmp_path / "factor.duckdb")
    service = FactorComputeService(provider=FakeProvider(), storage=storage)

    row_counts = service.compute_and_store(
        RETURN_FACTORS,
        start_date="20240101",
        end_date="20240103",
        universe="000001.SZ",
    )

    assert row_counts == {
        "daily_return": 2,
        "open_return": 2,
        "intraday_return": 3,
        "overnight_return": 2,
    }
    assert storage.list_factors() == [
        "daily_return",
        "intraday_return",
        "open_return",
        "overnight_return",
    ]


def test_compute_and_store_market_cap_factors_writes_raw_and_zscored(tmp_path):
    storage = FactorStorage(tmp_path / "factors", tmp_path / "factor.duckdb")
    service = FactorComputeService(provider=FakeMarketCapProvider(), storage=storage)

    row_counts = service.compute_and_store(
        MARKET_CAP_FACTORS,
        start_date="20240101",
        end_date="20240102",
        universe="000001.SZ,000002.SZ",
        postprocess=ZScorePostProcess(storage),
    )

    assert row_counts == {
        "log_total_market_cap": 4,
        "log_circulating_market_cap": 4,
        "z_log_total_market_cap": 4,
        "z_log_circulating_market_cap": 4,
    }
    assert sorted(storage.list_factors()) == [
        "log_circulating_market_cap",
        "log_total_market_cap",
        "z_log_circulating_market_cap",
        "z_log_total_market_cap",
    ]

    z_total = storage.read("z_log_total_market_cap")
    assert sorted(z_total["trade_date"].astype(str).unique()) == ["20240101", "20240102"]
    assert z_total.groupby("trade_date")["value"].mean().abs().max() < 1e-12


class _BatchFactor(Factor):
    def __init__(self, name: str, failing: bool = False):
        self.spec = FactorSpec(
            name=name,
            inputs=("close",),
            min_window=1,
            adjust="hfq",
            status="candidate",
        )
        self.failing = failing

    def compute(self, data):
        if self.failing:
            raise RuntimeError("synthetic failure")
        return to_factor_output(data.close, self.spec.name)


class _BatchProvider:
    def __init__(self):
        self.calls = 0

    def history(self, fields, start_date, end_date, universe, adjust, progress=None):
        self.calls += 1
        index = pd.date_range("2024-01-01", periods=2, freq="D")
        return FactorFrame({"close": pd.DataFrame({"000001.SZ": [1.0, 2.0]}, index=index)})


def test_compute_catalog_factors_isolates_failure_and_writes_manifests(tmp_path):
    storage = FactorStorage(tmp_path / "factors", tmp_path / "factor.duckdb")
    provider = _BatchProvider()
    factors = (_BatchFactor("batch_ok"), _BatchFactor("batch_bad", failing=True))

    result = compute_catalog_factors(
        provider,
        storage,
        factors=factors,
        start_date="20240101",
        end_date="20240102",
        universe="000001.SZ",
        factor_dir=tmp_path / "factors",
        run_id="run_001",
    )

    assert provider.calls == 1
    assert result["batch_ok"]["status"] == "computed"
    assert result["batch_bad"]["status"] == "failed"
    assert storage.read("batch_ok").shape[0] == 2
    assert (tmp_path / "factors" / "batch_ok" / "compute_manifest.json").exists()
    assert (tmp_path / "factors" / "batch_bad" / "compute_manifest.json").exists()
    assert (tmp_path / "factors" / "_runs" / "run_001" / "manifest.json").exists()


def test_compute_catalog_factors_resume_skips_matching_output(tmp_path):
    storage = FactorStorage(tmp_path / "factors", tmp_path / "factor.duckdb")
    factor = _BatchFactor("batch_resume")
    provider = _BatchProvider()
    kwargs = dict(
        factors=(factor,),
        start_date="20240101",
        end_date="20240102",
        universe="000001.SZ",
        factor_dir=tmp_path / "factors",
    )

    compute_catalog_factors(provider, storage, run_id="run_001", **kwargs)
    compute_catalog_factors(provider, storage, run_id="run_002", resume=True, **kwargs)

    assert provider.calls == 1
