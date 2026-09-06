from __future__ import annotations

from datetime import datetime, timedelta
from typing import Iterable

import pandas as pd


class EvaluationDataLoader:
    def __init__(self, storage, pro):
        self.storage = storage
        self.pro = pro

    def load_factor(
        self, factor_name: str, *, start_date: str, end_date: str | None
    ) -> pd.DataFrame:
        return self.storage.read(factor_name, start_date=start_date, end_date=end_date)

    def load_prices(
        self,
        *,
        start_date: str,
        end_date: str | None,
        periods: tuple[int, ...],
        universe_name: str | None = None,
    ) -> pd.DataFrame:
        extended_end = _extend_end_date(end_date or start_date, max(periods) * 3 + 10)
        ts_code: str | None = None
        if universe_name:
            members = self.pro.universe(
                universe=universe_name,
                start_date=start_date,
                end_date=extended_end,
                fields="trade_date,universe,ts_code",
            )
            if members.empty:
                return pd.DataFrame(columns=["trade_date", "ts_code", "open", "close"])
            codes = sorted(members["ts_code"].dropna().astype(str).unique())
            ts_code = ",".join(codes)
        return self.pro.pro_bar(
            ts_code=ts_code,
            start_date=start_date,
            end_date=extended_end,
            adj=None,
        )

    def load_universe(
        self, *, universe_name: str | None, start_date: str, end_date: str | None
    ) -> pd.DataFrame | None:
        if universe_name is None:
            return None

        universe = self.pro.universe(
            universe=universe_name,
            start_date=start_date,
            end_date=end_date,
            fields="trade_date,universe,ts_code",
        )
        return _universe_to_panel(universe)

    def load_tradability(
        self, *, start_date: str, end_date: str | None, universe_name: str | None
    ) -> pd.DataFrame | None:
        """Load T+1 entry diagnostics aligned to each T-day signal.

        The optional method keeps the evaluation stack compatible with fake or
        custom providers.  LocalPro supplies all five diagnostics used by the
        real run: missing open, suspension, ST, up-limit and down-limit.
        """
        required = ("universe", "pro_bar", "stock_st", "suspend_d", "stk_limit")
        if universe_name is None or any(not hasattr(self.pro, name) for name in required):
            return None
        members = self.pro.universe(
            universe=universe_name,
            start_date=start_date,
            end_date=end_date,
            fields="trade_date,universe,ts_code",
        )
        if members.empty:
            return pd.DataFrame()
        member_rows = members.loc[:, ["trade_date", "ts_code"]].dropna().drop_duplicates()
        member_rows["signal_date"] = pd.to_datetime(
            member_rows.pop("trade_date"), format="%Y%m%d"
        )
        member_rows["ts_code"] = member_rows["ts_code"].astype(str)
        codes = sorted(member_rows["ts_code"].unique())
        extended_end = _extend_end_date(end_date or start_date, 10)
        code_arg = ",".join(codes)
        bars = self.pro.pro_bar(
            ts_code=code_arg,
            start_date=start_date,
            end_date=extended_end,
            adj=None,
        )
        next_rows = _next_day_rows(bars, codes)
        for name, loader in (("st_t1", self.pro.stock_st), ("suspended_t1", self.pro.suspend_d)):
            raw = loader(ts_code=code_arg, start_date=start_date, end_date=extended_end)
            keys = _flag_keys(raw)
            if not keys.empty:
                next_rows = next_rows.merge(
                    keys.assign(**{name: True}),
                    on=["trade_date_t1", "ts_code"],
                    how="left",
                )
        limits = self.pro.stk_limit(
            ts_code=code_arg, start_date=start_date, end_date=extended_end
        )
        if not limits.empty:
            limit_cols = [
                column
                for column in ("trade_date", "ts_code", "up_limit", "down_limit")
                if column in limits
            ]
            limit_rows = limits.loc[:, limit_cols].copy()
            limit_rows["trade_date_t1"] = pd.to_datetime(
                limit_rows.pop("trade_date"), format="%Y%m%d"
            )
            next_rows = next_rows.merge(
                limit_rows, on=["trade_date_t1", "ts_code"], how="left"
            )
        diagnostics = member_rows.merge(
            next_rows, on=["signal_date", "ts_code"], how="left"
        )
        diagnostics["missing_open_t1"] = diagnostics["next_open"].isna() | (
            pd.to_numeric(diagnostics["next_open"], errors="coerce") <= 0
        )
        for column in ("st_t1", "suspended_t1"):
            values = diagnostics[column] if column in diagnostics else pd.Series(
                False, index=diagnostics.index
            )
            diagnostics[column] = values.astype("boolean").fillna(False).astype(bool)
        next_open = pd.to_numeric(diagnostics["next_open"], errors="coerce")
        up_limit = pd.to_numeric(
            diagnostics["up_limit"]
            if "up_limit" in diagnostics
            else pd.Series(index=diagnostics.index, dtype=float),
            errors="coerce",
        )
        down_limit = pd.to_numeric(
            diagnostics["down_limit"]
            if "down_limit" in diagnostics
            else pd.Series(index=diagnostics.index, dtype=float),
            errors="coerce",
        )
        diagnostics["up_limit_t1"] = up_limit.notna() & (next_open >= up_limit - 1e-8)
        diagnostics["down_limit_t1"] = down_limit.notna() & (next_open <= down_limit + 1e-8)
        diagnostics["eligible"] = ~diagnostics[
            [
                "missing_open_t1",
                "suspended_t1",
                "st_t1",
                "up_limit_t1",
                "down_limit_t1",
            ]
        ].any(axis=1)
        return diagnostics.set_index(["signal_date", "ts_code"]).sort_index()

    def load_benchmark_returns(
        self, *, ts_code: str | None, start_date: str, end_date: str | None
    ) -> pd.Series | None:
        if ts_code is None:
            return None

        df = self.pro.index_daily(
            ts_code=ts_code,
            start_date=start_date,
            end_date=end_date,
            fields="trade_date,pct_chg",
        )
        if df.empty:
            return pd.Series(dtype=float, name=ts_code)

        result = (
            df[["trade_date", "pct_chg"]]
            .dropna(subset=["pct_chg"])
            .drop_duplicates(subset=["trade_date"], keep="last")
            .assign(date=lambda d: pd.to_datetime(d["trade_date"], format="%Y%m%d"))
            .set_index("date")["pct_chg"]
            / 100
        )
        result.name = ts_code
        return result.sort_index()

    def max_factor_trade_date(
        self, factor_names: Iterable[str], *, start_date: str
    ) -> str:
        max_dates = []
        for factor_name in factor_names:
            factor_data = self.load_factor(
                factor_name,
                start_date=start_date,
                end_date=None,
            )
            if not factor_data.empty:
                max_dates.append(max_factor_trade_date(factor_data))
        if not max_dates:
            return start_date
        return max(max_dates)


def _universe_to_panel(universe: pd.DataFrame) -> pd.DataFrame:
    if universe.empty:
        return pd.DataFrame(dtype=bool)

    missing_columns = {"trade_date", "ts_code"}.difference(universe.columns)
    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"universe data must contain columns: {missing}")

    universe = universe.dropna(subset=["trade_date", "ts_code"])
    if universe.empty:
        return pd.DataFrame(dtype=bool)

    normalized = pd.DataFrame(
        {
            "date": pd.to_datetime(universe["trade_date"], format="%Y%m%d"),
            "ts_code": universe["ts_code"],
            "member": True,
        }
    )
    panel = normalized.pivot_table(
        index="date",
        columns="ts_code",
        values="member",
        aggfunc="any",
        fill_value=False,
    )
    return panel.astype(bool).sort_index().sort_index(axis=1)


def _next_day_rows(bars: pd.DataFrame, codes: list[str]) -> pd.DataFrame:
    columns = ["signal_date", "trade_date_t1", "ts_code", "next_open"]
    if bars is None or bars.empty or not {"trade_date", "ts_code", "open"}.issubset(bars.columns):
        return pd.DataFrame(columns=columns)
    frame = bars.loc[:, ["trade_date", "ts_code", "open"]].copy()
    frame["ts_code"] = frame["ts_code"].astype(str)
    frame["trade_date_t1"] = pd.to_datetime(frame.pop("trade_date"), format="%Y%m%d")
    frame = frame[frame["ts_code"].isin(codes)].sort_values(["ts_code", "trade_date_t1"])
    frame["signal_date"] = frame.groupby("ts_code")["trade_date_t1"].shift(1)
    frame = frame.dropna(subset=["signal_date"])
    frame = frame.rename(columns={"open": "next_open"})
    return frame.loc[:, columns].drop_duplicates(["signal_date", "ts_code"])


def _flag_keys(raw: pd.DataFrame) -> pd.DataFrame:
    if raw is None or raw.empty or not {"trade_date", "ts_code"}.issubset(raw.columns):
        return pd.DataFrame(columns=["trade_date_t1", "ts_code"])
    result = raw.loc[:, ["trade_date", "ts_code"]].dropna().drop_duplicates()
    result["trade_date_t1"] = pd.to_datetime(result.pop("trade_date"), format="%Y%m%d")
    result["ts_code"] = result["ts_code"].astype(str)
    return result


def max_factor_trade_date(factor_data: pd.DataFrame) -> str:
    raw_dates = factor_data["trade_date"]
    if pd.api.types.is_numeric_dtype(raw_dates):
        normalized = raw_dates.astype("Int64").astype(str)
    else:
        numeric_dates = pd.to_numeric(raw_dates, errors="coerce")
        if numeric_dates.notna().all():
            normalized = numeric_dates.astype("Int64").astype(str)
        else:
            normalized = raw_dates.astype(str)
    dates = pd.to_datetime(normalized, format="%Y%m%d")
    return dates.max().strftime("%Y%m%d")


def _extend_end_date(base_date: str, days: int) -> str:
    parsed = datetime.strptime(base_date, "%Y%m%d")
    return (parsed + timedelta(days=days)).strftime("%Y%m%d")
