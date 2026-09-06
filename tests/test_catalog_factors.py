import numpy as np
import pandas as pd

from microfactor.core import FactorFrame
from microfactor.factors.catalog import catalog_factors, load_catalog_metadata


def _frame() -> FactorFrame:
    index = pd.date_range("2020-01-01", periods=300)
    columns = ["000001.SZ", "000002.SZ", "000003.SZ"]
    rng = np.random.default_rng(7)
    close = pd.DataFrame(10 + rng.random((300, 3)).cumsum(axis=0), index, columns)
    volume = pd.DataFrame(100 + rng.random((300, 3)) * 10, index, columns)
    fields = {name: close.copy() for name in ("open", "high", "low", "pre_close")}
    fields["high"] = close + 1
    fields["low"] = close - 1
    fields["pre_close"] = close.shift(1).bfill()
    fields.update(
        {
            "close": close,
            "volume": volume,
            "amount": close * volume,
            "turnover_percent": pd.DataFrame(1.0, index=index, columns=columns),
            "adjusted_close": close,
            "close_total_return_index": close / close.iloc[0],
            "close_to_close_total_return_1d": (close / close.iloc[0]).pct_change(fill_method=None),
            "pe_ttm": close,
            "pb": close,
            "vwap": close,
            "is_suspended": pd.DataFrame(False, index=index, columns=columns),
        }
    )
    return FactorFrame(fields)


def test_catalog_contains_exactly_65_non_model_factors():
    metadata = load_catalog_metadata()
    assert len(metadata) == 65
    assert all(not item.name.startswith("model_") for item in metadata)
    assert {item.status for item in metadata} == {"evaluated", "candidate", "rejected"}


def test_every_catalog_factor_emits_standard_output():
    frame = _frame()
    for factor in catalog_factors():
        result = factor.compute(frame)
        assert tuple(result.columns) == ("trade_date", "ts_code", "value")
        assert result["trade_date"].is_monotonic_increasing


def test_huatai6_factors_use_only_declared_fields():
    frame = _frame()
    for name in (
        "huatai6_high_r_std_1m",
        "huatai6_high_r_std_4m",
        "huatai6_std_4m",
    ):
        factor = next(item for item in catalog_factors() if item.spec.name == name)
        declared = FactorFrame({field: getattr(frame, field) for field in factor.spec.inputs})
        result = factor.compute(declared)
        assert tuple(result.columns) == ("trade_date", "ts_code", "value")


def test_every_catalog_factor_respects_declared_input_contract():
    frame = _frame()
    for factor in catalog_factors():
        declared = FactorFrame(
            {field: getattr(frame, field) for field in factor.spec.inputs}
        )
        result = factor.compute(declared)
        assert tuple(result.columns) == ("trade_date", "ts_code", "value")
