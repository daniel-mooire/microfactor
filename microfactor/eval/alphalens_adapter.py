from __future__ import annotations

import pandas as pd

from microfactor.eval.domain import ReturnType


def _require_columns(data: pd.DataFrame, columns: set[str]) -> None:
    missing = columns.difference(data.columns)
    if missing:
        missing_columns = ", ".join(sorted(missing))
        raise ValueError(f"missing required columns: {missing_columns}")


def _parse_trade_date(values: pd.Series) -> pd.Series:
    normalized = values.map(_normalize_trade_date)
    return pd.to_datetime(normalized, format="%Y%m%d", errors="raise")


def _normalize_trade_date(value: object) -> object:
    if pd.isna(value):
        return value
    try:
        numeric_value = float(value)
    except (TypeError, ValueError):
        return str(value)
    if numeric_value.is_integer():
        return str(int(numeric_value))
    return str(value)


def factor_long_to_alphalens_series(factor: pd.DataFrame) -> pd.Series:
    _require_columns(factor, {"trade_date", "ts_code", "value"})

    normalized = pd.DataFrame(
        {
            "date": _parse_trade_date(factor["trade_date"]),
            "asset": factor["ts_code"],
            "factor": factor["value"],
        }
    )
    if normalized.duplicated(subset=["date", "asset"]).any():
        raise ValueError("duplicate date/asset rows in factor data")

    result = normalized.set_index(["date", "asset"])["factor"].sort_index()
    result.name = "factor"
    return result


def build_price_matrix(price_data: pd.DataFrame, return_type: ReturnType) -> pd.DataFrame:
    if return_type == "open_t1":
        value_column = "open"
        shift_periods = -1
    elif return_type == "close_t0":
        value_column = "close"
        shift_periods = 0
    else:
        raise ValueError(f"unknown return_type: {return_type}")

    _require_columns(price_data, {"trade_date", "ts_code", value_column})
    normalized = pd.DataFrame(
        {
            "date": _parse_trade_date(price_data["trade_date"]),
            "asset": price_data["ts_code"],
            "price": price_data[value_column].where(price_data[value_column] > 0),
        }
    )
    if normalized.duplicated(subset=["date", "asset"]).any():
        raise ValueError("duplicate date/asset rows in price data")

    matrix = normalized.pivot(index="date", columns="asset", values="price")
    matrix = matrix.sort_index().sort_index(axis=1)
    if shift_periods:
        matrix = matrix.shift(shift_periods)
    return matrix


def filter_factor_by_universe(
    factor: pd.Series, universe: pd.DataFrame | None
) -> pd.Series:
    if universe is None:
        return factor

    membership = pd.Series(
        (
            pd.notna(universe.at[date, asset]) and bool(universe.at[date, asset])
            if date in universe.index and asset in universe.columns
            else False
        )
        for date, asset in factor.index
    )
    return factor[membership.to_numpy()]


def filter_factor_by_tradability(
    factor: pd.Series,
    tradability: pd.DataFrame | None,
) -> tuple[pd.Series, dict[str, int]]:
    """Filter T-day signals whose T+1 open cannot be traded.

    ``tradability`` is indexed by ``(signal_date, asset)`` and contains the
    boolean ``eligible`` flag plus reason columns.  Missing diagnostics are
    treated as eligible so test and custom providers remain backwards
    compatible; the real Microshare loader supplies all reason columns.
    """
    if tradability is None or tradability.empty:
        return factor, {}
    if not isinstance(tradability.index, pd.MultiIndex):
        raise ValueError("tradability must use a (signal_date, asset) index")
    aligned = tradability.reindex(factor.index)
    eligible = aligned["eligible"].fillna(True).astype(bool)
    kept = factor[eligible.to_numpy()]
    counts = {
        column: int(aligned[column].fillna(False).astype(bool).sum())
        for column in (
            "missing_open_t1",
            "suspended_t1",
            "st_t1",
            "up_limit_t1",
            "down_limit_t1",
        )
        if column in aligned.columns
    }
    counts["ineligible_t1"] = int((~eligible).sum())
    counts["eligible_t1"] = int(eligible.sum())
    return kept, counts
