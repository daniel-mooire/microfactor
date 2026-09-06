"""Local implementations of the 65 non-model quant-hive catalog factors.

The catalog YAML files are copied into this project as provenance snapshots.  The
runtime implementation below only consumes :class:`FactorFrame`; it never imports
quant-hive or reaches through to a data source.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import yaml

from microfactor.core import Factor, FactorFrame, FactorSpec, to_factor_output

CATALOG_DIR = Path(__file__).resolve().parents[1] / "catalog"


_INPUTS: dict[str, tuple[str, ...]] = {
    "alpha101_007": ("close", "volume"),
    "alpha101_016": ("high", "volume"),
    "alpha101_040": ("high", "volume"),
    "alpha101_044": ("high", "volume"),
    "alpha101_050": ("volume", "vwap"),
    "csc14_alpha158_cord_20d": ("close", "volume"),
    "csc14_alpha158_high0": ("high", "open"),
    "csc14_alpha158_imxd_20d": ("high", "low"),
    "csc14_alpha158_klen": ("high", "low", "open"),
    "csc14_alpha158_min_20d": ("low", "close"),
    "csc14_alpha158_qtld_60d": ("close",),
    "csc14_alpha158_qtlu_60d": ("close",),
    "csc14_alpha158_resi_60d": ("close",),
    "csc14_alpha158_std_5d": ("close",),
    "csc14_alpha158_vma_60d": ("volume",),
    "csc14_alpha158_vsumd_60d": ("volume",),
    "guangfa42_ar_20d": ("high", "low", "open", "close", "pre_close"),
    "guangfa42_bias_6d": ("close",),
    "guangfa42_price_slope_6d": ("close",),
    "guangfa42_roc_6d": ("close",),
    "guangfa42_si_1d": ("high", "low", "open", "close", "pre_close"),
    "haitong18_price_shape_high_open_10d": ("high", "open"),
    "haitong47_return_2m_daily_adapted": ("close_total_return_index",),
    "haitong58_return_9m_daily_adapted": ("close_total_return_index",),
    "huatai28_a1_vwap_high_corr_10d": ("vwap", "high"),
    "huatai28_a2_rank_high_low_corr_sum_20d": ("high", "low"),
    "huatai28_alpha125_open_free_turn_corr_10d": ("open", "close", "turnover_percent"),
    "huatai4_exp_wgt_return_6m": ("close_to_close_total_return_1d", "turnover_percent"),
    "huatai5_bias_std_turn_1m": ("turnover_percent",),
    "huatai5_bias_turn_1m": ("turnover_percent",),
    "huatai5_std_turn_1m": ("turnover_percent",),
    "huatai5_turn_1m": ("turnover_percent",),
    "huatai6_high_r_std_1m": ("high", "pre_close", "close", "adjusted_close"),
    "huatai6_high_r_std_4m": ("high", "pre_close", "close", "adjusted_close"),
    "huatai6_hml_r_std_5m": ("high", "low", "pre_close", "close", "adjusted_close"),
    "huatai6_std_4m": ("close_to_close_total_return_1d",),
    "hz2025_amount_previous_completed_6calm": ("amount",),
    "inverse_pb": ("pb",),
    "inverse_pe_ttm": ("pe_ttm",),
    "jq_arbr_26d": ("high", "low", "open", "close", "adjusted_close", "is_suspended"),
    "jq_davol20": ("turnover_percent",),
    "jq_mac120": ("adjusted_close",),
    "jq_mfi14": ("high", "low", "close", "adjusted_close", "volume"),
    "jq_price_no_fq": ("close",),
    "jq_price1y": ("adjusted_close",),
    "jq_single_day_vpt": ("adjusted_close", "volume"),
    "jq_tvma6": ("amount",),
    "jq_vol120": ("turnover_percent",),
    "jq_vol5": ("turnover_percent",),
    "jq_vol60": ("turnover_percent",),
    "jq_vroc6": ("volume",),
    "jq_wvad_6d": ("open", "high", "low", "adjusted_close", "volume", "close"),
    "log_amount_20": ("amount",),
    "long_momentum2": (
        "high",
        "low",
        "pre_close",
        "close_total_return_index",
        "close_to_close_total_return_1d",
    ),
    "momentum": ("close_total_return_index",),
    "pe_change_60d": ("pe_ttm",),
    "price_volume_corr_20d": ("close_total_return_index", "volume"),
    "reversal": ("close_total_return_index",),
    "turnover_20": ("turnover_percent",),
    "turnover_stability_20d": ("turnover_percent",),
    "volatility": ("close_to_close_total_return_1d",),
    "vwap_volume_pressure_3d": ("vwap", "close", "volume"),
    "xibu2026_maxret_21d_monthly_adapted": ("close_to_close_total_return_1d",),
    "xibu2026_rev_21d_monthly_adapted": ("close_to_close_total_return_1d",),
    "xinghuo5_momentum_12m_skip1m_daily_adapted": ("close_total_return_index",),
}


_WINDOWS: dict[str, int] = {
    "momentum": 20,
    "reversal": 5,
    "volatility": 20,
    "turnover_20": 20,
    "turnover_stability_20d": 20,
}


def _clean(frame: pd.DataFrame) -> pd.DataFrame:
    return frame.replace([np.inf, -np.inf], np.nan)


def _rolling(frame: pd.DataFrame, window: int, op: str = "mean") -> pd.DataFrame:
    rolling = frame.rolling(window=window, min_periods=window)
    return getattr(rolling, op)()


def _corr(left: pd.DataFrame, right: pd.DataFrame, window: int) -> pd.DataFrame:
    return pd.DataFrame(
        {
            code: left[code].rolling(window, min_periods=window).corr(right[code])
            for code in left.columns
        },
        index=left.index,
    )


def _slope(frame: pd.DataFrame, window: int) -> pd.DataFrame:
    x = np.arange(window, dtype=float)
    x = x - x.mean()
    denom = float(np.dot(x, x))
    return frame.rolling(window, min_periods=window).apply(
        lambda values: float(np.dot(x, values - values.mean()) / denom), raw=True
    )


def _tri(data: FactorFrame) -> pd.DataFrame:
    if "close_total_return_index" in data.fields:
        return data.close_total_return_index
    if "adjusted_close" in data.fields:
        first = data.adjusted_close.bfill().iloc[0].replace(0, np.nan)
        return data.adjusted_close.div(first, axis="columns")
    if "close" in data.fields:
        return data.close
    return getattr(data, data.fields[0])


def _adjusted_ohlc(
    data: FactorFrame,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    close = data.close
    adjusted_close = data.adjusted_close if "adjusted_close" in data.fields else close
    ratio = adjusted_close.div(close.where(close > 0)).replace([np.inf, -np.inf], np.nan)
    return data.open * ratio, data.high * ratio, data.low * ratio, adjusted_close


def _compute(name: str, data: FactorFrame) -> pd.DataFrame:
    tri = _tri(data)
    close = data.close if "close" in data.fields else tri
    volume = (
        data.volume
        if "volume" in data.fields
        else pd.DataFrame(index=tri.index, columns=tri.columns)
    )
    if "turnover_percent" in data.fields:
        turnover = data.turnover_percent
    elif "turnover_rate" in data.fields:
        turnover = data.turnover_rate
    else:
        turnover = pd.DataFrame(index=tri.index, columns=tri.columns, dtype=float)
    returns = (
        data.close_to_close_total_return_1d
        if "close_to_close_total_return_1d" in data.fields
        else tri.pct_change(fill_method=None)
    )

    if name == "momentum":
        return tri / tri.shift(20) - 1
    if name == "reversal":
        return -(tri / tri.shift(5) - 1)
    if name == "volatility":
        return _rolling(returns, 20, "std")
    if name == "turnover_20":
        return _rolling(turnover, 20)
    if name == "turnover_stability_20d":
        return _rolling(turnover, 20, "std")
    if name == "inverse_pe_ttm":
        values = data.pe_ttm.where(data.pe_ttm > 0)
        return 1.0 / values
    if name == "inverse_pb":
        values = data.pb.where(data.pb > 0)
        return 1.0 / values
    if name == "pe_change_60d":
        earnings_yield = 1.0 / data.pe_ttm.where(data.pe_ttm > 0)
        return earnings_yield - earnings_yield.shift(60)
    if name == "log_amount_20":
        return np.log(_rolling(data.amount.where(data.amount > 0), 20))
    if name == "price_volume_corr_20d":
        return _corr(np.log(tri.where(tri > 0)).diff(), np.log(volume.where(volume > 0)).diff(), 20)
    if name == "vwap_volume_pressure_3d":
        return _rolling((data.vwap - close).div(close.where(close != 0)) * volume, 3)
    if name == "jq_price_no_fq":
        return close.where(close > 0)
    if name == "jq_price1y":
        return data.adjusted_close / _rolling(data.adjusted_close, 250) - 1
    if name == "jq_mac120":
        return _rolling(data.adjusted_close, 120) / data.adjusted_close
    if name in {"jq_vol5", "jq_vol60", "jq_vol120"}:
        return _rolling(turnover, int(name[6:]))
    if name == "jq_davol20":
        return _rolling(turnover, 20) / _rolling(turnover, 120)
    if name == "jq_tvma6":
        return _rolling(data.amount, 6)
    if name == "jq_vroc6":
        return 100 * (volume / volume.shift(6) - 1)
    if name == "jq_single_day_vpt":
        return (data.adjusted_close / data.adjusted_close.shift(1) - 1) * volume
    if name == "jq_wvad_6d":
        high, low = data.high, data.low
        numerator = data.adjusted_close - data.open
        return _rolling(numerator.div((high - low).replace(0, np.nan)) * volume, 6)
    if name == "jq_mfi14":
        ratio = data.adjusted_close.div(data.close.where(data.close > 0))
        high = data.high * ratio
        low = data.low * ratio
        adjusted_close = data.adjusted_close
        tp = (high + low + adjusted_close) / 3
        money = tp * volume
        direction = tp.diff()
        positive = money.where(direction > 0, 0.0)
        negative = money.where(direction < 0, 0.0).abs()
        ratio = _rolling(positive, 14, "sum") / _rolling(negative, 14, "sum")
        return 100 - 100 / (1 + ratio)
    if name == "jq_arbr_26d":
        adjusted_open, high, low, adjusted_close = _adjusted_ohlc(data)
        prev = adjusted_close.shift(1)
        ar = (
            _rolling(high - adjusted_open, 26, "sum")
            / _rolling(adjusted_open - low, 26, "sum")
            * 100
        )
        br = (
            _rolling((high - prev).clip(lower=0), 26, "sum")
            / _rolling((prev - low).clip(lower=0), 26, "sum")
            * 100
        )
        return ar - br
    if name.startswith("csc14_alpha158_"):
        if name.endswith("high0"):
            return data.high / data.open
        if name.endswith("klen"):
            return (data.high - data.low) / data.open
        if name.endswith("imxd_20d"):
            return (_rolling(data.high, 20, "max") - _rolling(data.low, 20, "min")) / 20
        if name.endswith("min_20d"):
            return _rolling(data.low, 20, "min") / close
        if name.endswith("qtld_60d"):
            return data.close.rolling(60, min_periods=60).quantile(0.2) / close
        if name.endswith("qtlu_60d"):
            return data.close.rolling(60, min_periods=60).quantile(0.8) / close
        if name.endswith("resi_60d"):
            fitted = _slope(data.close, 60)
            return data.close - (_rolling(data.close, 60) - fitted * 59 / 2)
        if name.endswith("std_5d"):
            return _rolling(close, 5, "std") / close
        if name.endswith("vma_60d"):
            return _rolling(volume, 60) / (volume + 1e-12)
        if name.endswith("vsumd_60d"):
            diff = volume.diff()
            numerator = _rolling(diff.clip(lower=0), 60, "sum")
            numerator -= _rolling((-diff).clip(lower=0), 60, "sum")
            return numerator / (_rolling(diff.abs(), 60, "sum") + 1e-12)
        if name.endswith("cord_20d"):
            left = np.log(close.where(close > 0)).diff()
            right = np.log(volume.where(volume > 0) + 1).diff()
            return _corr(left, right, 20)
    if name.startswith("alpha101_"):
        if name.endswith("007"):
            adv = _rolling(volume, 20)
            move = close - close.shift(7)
            valid = volume.notna() & adv.notna() & move.notna()
            signal = -_ts_rank(move.abs(), 60) * np.sign(move)
            return signal.where(valid & (volume > adv)).mask(
                valid & ~(volume > adv), -1
            )
        if name.endswith("016"):
            return -_rank(_corr(_rank(data.high), _rank(volume), 5))
        if name.endswith("040"):
            return -_rank(_rolling(data.high, 10, "std")) * _corr(data.high, volume, 10)
        if name.endswith("044"):
            return -_corr(data.high, _rank(volume), 5)
        if name.endswith("050"):
            return -_rolling(_rank(_corr(_rank(volume), _rank(data.vwap), 5)), 5, "max")
    if name.startswith("guangfa42_"):
        if name.endswith("ar_20d"):
            ar = (
                _rolling(data.high - data.open, 20, "sum")
                / _rolling(data.open - data.low, 20, "sum")
                * 100
            )
            prev = data.close.shift(1)
            br = (
                _rolling((data.high - prev).clip(lower=0), 20, "sum")
                / _rolling((prev - data.low).clip(lower=0), 20, "sum")
                * 100
            )
            return ar - br
        if name.endswith("bias_6d"):
            return 100 * (close / _rolling(close, 6) - 1)
        if name.endswith("price_slope_6d"):
            return _slope(close, 6)
        if name.endswith("roc_6d"):
            return 100 * (close / close.shift(6) - 1)
        return (close - data.pre_close) / data.pre_close
    if name == "haitong18_price_shape_high_open_10d":
        return _rolling(np.log(data.high / data.open), 10)
    if name == "haitong47_return_2m_daily_adapted":
        return tri / tri.shift(42) - 1
    if name == "haitong58_return_9m_daily_adapted":
        return tri / tri.shift(189) - 1
    if name == "huatai28_a1_vwap_high_corr_10d":
        return _corr(data.vwap / data.high, data.high, 10)
    if name == "huatai28_a2_rank_high_low_corr_sum_20d":
        return _rolling(_rank(_corr(data.high, data.low, 20)), 20, "sum")
    if name == "huatai28_alpha125_open_free_turn_corr_10d":
        return _corr(data.open - turnover, data.close, 10)
    if name == "huatai4_exp_wgt_return_6m":
        return _rolling(returns * turnover, 126) / _rolling(turnover, 126)
    if name.startswith("huatai5_"):
        current = _rolling(turnover, 21, "std" if "std" in name else "mean")
        if "bias" in name:
            baseline = _rolling(turnover, 504, "std" if "std" in name else "mean")
            return current / baseline - 1
        return current
    if name.startswith("huatai6_"):
        if name.endswith("std_4m"):
            return _rolling(returns, 84, "std")
        ratio = data.adjusted_close.div(data.close.where(data.close > 0))
        high_return = (data.high * ratio) / data.adjusted_close.shift(1) - 1
        high_std = _rolling(high_return, 21 if name.endswith("1m") else 84, "std")
        if "hml" in name:
            low_return = (data.low * ratio) / data.adjusted_close.shift(1) - 1
            low_std = _rolling(low_return, 105, "std")
            return high_std - low_std
        return high_std
    if name == "hz2025_amount_previous_completed_6calm":
        return _rolling(data.amount, 126)
    if name == "long_momentum2":
        amplitude = (data.high - data.low) / data.pre_close
        return _rolling(amplitude * returns, 160)
    if name == "xibu2026_maxret_21d_monthly_adapted":
        return returns.shift(1).rolling(21, min_periods=21).max()
    if name == "xibu2026_rev_21d_monthly_adapted":
        return -returns.shift(1).rolling(21, min_periods=21).sum()
    if name == "xinghuo5_momentum_12m_skip1m_daily_adapted":
        return tri / tri.shift(231) - 1
    raise KeyError(f"no local implementation for catalog factor {name}")


def _rank(frame: pd.DataFrame) -> pd.DataFrame:
    return frame.rank(axis=1, pct=True)


def _ts_rank(frame: pd.DataFrame, window: int) -> pd.DataFrame:
    return frame.rolling(window, min_periods=window).apply(
        lambda values: float(pd.Series(values).rank().iloc[-1]), raw=False
    )


@dataclass(frozen=True)
class CatalogMetadata:
    name: str
    category: str
    status: str
    formula: str
    direction: str
    source: str
    implementation: str
    tags: tuple[str, ...]
    inputs: tuple[str, ...]
    min_window: int
    adjust: str | None


class CatalogFactor(Factor):
    def __init__(self, metadata: CatalogMetadata):
        self.metadata = metadata
        self.spec = FactorSpec(
            name=metadata.name,
            inputs=metadata.inputs,
            min_window=metadata.min_window,
            adjust=metadata.adjust,
            category=metadata.category,
            status=metadata.status,
            formula=metadata.formula,
            direction=metadata.direction,
            source=metadata.source,
            implementation=metadata.implementation,
            tags=metadata.tags,
        )

    def compute(self, data: FactorFrame) -> pd.DataFrame:
        return to_factor_output(_clean(_compute(self.spec.name, data)), self.spec.name)


def _load_yaml(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        value = yaml.safe_load(handle)
    return value if isinstance(value, dict) else {}


def _lookback(name: str, expression: str) -> int:
    if name in _WINDOWS:
        return _WINDOWS[name]
    values = [int(value) for value in re.findall(r"(?:_|,|\b)(\d{1,3})(?:d|m)?\b", expression)]
    return max(values, default=1)


def load_catalog_metadata(catalog_dir: Path | str = CATALOG_DIR) -> tuple[CatalogMetadata, ...]:
    result: list[CatalogMetadata] = []
    for path in sorted(Path(catalog_dir).glob("*.yaml")):
        raw = _load_yaml(path)
        name = str(raw.get("id", path.stem))
        if name.startswith("model_") or name not in _INPUTS:
            continue
        implementation = raw.get("implementation") or {}
        direction = raw.get("direction") or {}
        source_rows = raw.get("research_sources") or []
        source = ""
        if source_rows:
            source = str(source_rows[0].get("title") or source_rows[0].get("local_path") or "")
        expression = str((raw.get("formula") or {}).get("expression", ""))
        result.append(
            CatalogMetadata(
                name=name,
                category=str(raw.get("category", "technical")),
                status=str(raw.get("status", "candidate")),
                formula=expression,
                direction=str(direction.get("expected", "unspecified")),
                source=source,
                implementation=(
                    f"{implementation.get('path', '')}::"
                    f"{implementation.get('callable', '')}"
                ),
                tags=tuple(str(tag) for tag in raw.get("tags", []) or []),
                inputs=_INPUTS[name],
                min_window=_lookback(name, expression),
                adjust=(
                    "none"
                    if name
                    in {
                        "alpha101_007",
                        "jq_price_no_fq",
                        "csc14_alpha158_high0",
                        "csc14_alpha158_klen",
                    }
                    else "hfq"
                ),
            )
        )
    return tuple(result)


def catalog_factors(catalog_dir: Path | str = CATALOG_DIR) -> tuple[CatalogFactor, ...]:
    return tuple(CatalogFactor(metadata) for metadata in load_catalog_metadata(catalog_dir))


def get_catalog_factor(name: str, catalog_dir: Path | str = CATALOG_DIR) -> CatalogFactor:
    for factor in catalog_factors(catalog_dir):
        if factor.spec.name == name:
            return factor
    raise KeyError(f"unknown catalog factor: {name}")


__all__ = [
    "CATALOG_DIR",
    "CatalogFactor",
    "CatalogMetadata",
    "catalog_factors",
    "get_catalog_factor",
    "load_catalog_metadata",
]
