from __future__ import annotations

import json
from collections.abc import Callable
from dataclasses import dataclass

import numpy as np
import pandas as pd

from microfactor.eval.alphalens_adapter import (
    build_price_matrix,
    factor_long_to_alphalens_series,
    filter_factor_by_tradability,
    filter_factor_by_universe,
)
from microfactor.eval.domain import EvaluationRun, FactorEvaluationResult
from microfactor.eval.metrics import build_portfolio_returns


@dataclass(frozen=True)
class EvaluationSharedData:
    price_data: pd.DataFrame | None = None
    universe_panel: pd.DataFrame | None = None
    tradability: pd.DataFrame | None = None


class FactorEvaluator:
    def __init__(
        self,
        *,
        data_loader,
        metric_calculator,
        artifact_store,
        figure_writer,
        log_info: Callable[[str], None] | None = None,
    ):
        self.data_loader = data_loader
        self.metric_calculator = metric_calculator
        self.artifact_store = artifact_store
        self.figure_writer = figure_writer
        self.log_info = log_info

    def evaluate(
        self,
        factor_name: str,
        run: EvaluationRun,
        shared_data: EvaluationSharedData | None = None,
    ) -> FactorEvaluationResult:
        config = run.config
        shared_data = shared_data or EvaluationSharedData()

        if factor_name not in config.factor_names:
            raise ValueError("factor_name must be included in config.factor_names")

        factor_data = self.data_loader.load_factor(
            factor_name,
            start_date=config.start_date,
            end_date=config.end_date,
        )
        if factor_data.empty:
            raise ValueError(f"{factor_name}: no factor data")
        self._log(
            f"evaluation_factor_load_finished factor={factor_name} rows={len(factor_data)}"
        )

        factor = factor_long_to_alphalens_series(factor_data)
        factor = filter_factor_by_universe(factor, shared_data.universe_panel)
        factor, tradability_counts = filter_factor_by_tradability(
            factor, shared_data.tradability
        )
        if factor.empty:
            raise ValueError(f"{factor_name}: no factor data after universe filtering")

        price_data = shared_data.price_data
        if price_data is None:
            price_end_date = config.end_date or self.data_loader.max_factor_trade_date(
                (factor_name,),
                start_date=config.start_date,
            )
            price_data = self.data_loader.load_prices(
                start_date=config.start_date,
                end_date=price_end_date,
                periods=config.periods,
                universe_name=config.universe,
            )
        prices = build_price_matrix(price_data, config.return_type)

        self._log(f"evaluation_clean_factor_started factor={factor_name}")
        tie_broken_rows = 0
        factor_for_binning = factor
        try:
            clean_factor_data = self.metric_calculator.clean_factor_and_forward_returns(
                factor,
                prices,
                quantiles=config.quantiles,
                periods=config.periods,
                max_loss=config.max_loss,
            )
        except Exception as exc:
            if "max_loss" not in str(exc):
                raise
            tie_broken = _break_factor_ties(factor)
            factor_for_binning = tie_broken
            clean_factor_data = self.metric_calculator.clean_factor_and_forward_returns(
                tie_broken,
                prices,
                quantiles=config.quantiles,
                periods=config.periods,
                max_loss=config.max_loss,
            )
            original = factor.reindex(clean_factor_data.index)
            tie_broken_rows = int((original != tie_broken.reindex(clean_factor_data.index)).sum())
            clean_factor_data["factor"] = original.to_numpy()
        if clean_factor_data.empty:
            raise ValueError(f"{factor_name}: no clean factor data")
        self._log(
            f"evaluation_clean_factor_finished factor={factor_name} rows={len(clean_factor_data)}"
        )

        daily_ic = self.metric_calculator.calculate_daily_ic(clean_factor_data)
        quantile_returns = self.metric_calculator.calculate_quantile_returns(
            clean_factor_data
        )
        if quantile_returns.empty or len(quantile_returns.columns) == 0:
            raise ValueError(f"{factor_name}: no quantile return periods")
        self._log(
            "evaluation_metrics_finished "
            f"factor={factor_name} periods={len(quantile_returns.columns)}"
        )

        index_returns = self.data_loader.load_benchmark_returns(
            ts_code=config.benchmark_index,
            start_date=config.start_date,
            end_date=config.end_date,
        )
        period_sample_counts = self.metric_calculator.calculate_period_sample_counts(
            factor_for_binning,
            prices,
            quantiles=config.quantiles,
            periods=config.periods,
            max_loss=config.max_loss,
        )
        summary = self.metric_calculator.build_factor_summary(
            factor_name=factor_name,
            return_type=config.return_type,
            clean_factor_data_sample_count=len(clean_factor_data),
            clean_factor_data_start=clean_factor_data.index.get_level_values("date").min(),
            clean_factor_data_end=clean_factor_data.index.get_level_values("date").max(),
            quantiles=config.quantiles,
            daily_ic=daily_ic,
            quantile_returns=quantile_returns,
            clean_factor_data=clean_factor_data,
            index_returns=index_returns,
            transaction_cost_bps=config.transaction_cost_bps,
            period_sample_counts=period_sample_counts,
        )

        universe_count = None
        if shared_data.universe_panel is not None:
            universe_count = int(shared_data.universe_panel.to_numpy(dtype=bool).sum())
        if universe_count:
            summary["coverage"] = float(len(factor) / universe_count)
        if {"IC Mean", "IC Std"}.issubset(summary.columns):
            summary["raw_ICIR"] = summary["IC Mean"] / summary["IC Std"]
        for key, value in tradability_counts.items():
            summary[key] = value
        summary["tie_broken_rows"] = tie_broken_rows
        if tradability_counts:
            diagnostics_path = run.factor_dir(factor_name) / "tradability_summary.json"
            diagnostics_path.parent.mkdir(parents=True, exist_ok=True)
            diagnostics_path.write_text(
                json.dumps(tradability_counts, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
        factor_direction = int(summary.iloc[0].get("factor_direction", 1))
        calculate_by_date = getattr(
            self.metric_calculator, "calculate_quantile_returns_by_date", None
        )
        calculate_five = getattr(self.metric_calculator, "calculate_five_bucket_returns", None)
        quantile_returns_by_date = (
            calculate_by_date(clean_factor_data) if calculate_by_date else pd.DataFrame()
        )
        five_bucket_returns = (
            calculate_five(clean_factor_data) if calculate_five else pd.DataFrame()
        )
        portfolio_returns = (
            build_portfolio_returns(
                clean_factor_data,
                direction=factor_direction,
                transaction_cost_bps=config.transaction_cost_bps,
                turnover_long=float(summary.iloc[0].get("turnover_daily_long", 0.0) or 0.0),
                turnover_short=float(summary.iloc[0].get("turnover_daily_short", 0.0) or 0.0),
            )
            if "factor_quantile" in clean_factor_data.columns
            else pd.DataFrame()
        )

        result = FactorEvaluationResult(
            factor_name=factor_name,
            summary=summary,
            output_dir=run.factor_dir(factor_name),
            clean_factor_data=clean_factor_data,
            daily_ic=daily_ic,
            quantile_returns=quantile_returns,
            quantile_returns_by_date=quantile_returns_by_date,
            five_bucket_returns=five_bucket_returns,
            portfolio_returns=portfolio_returns,
        )
        self.artifact_store.write_factor_artifacts(result)
        figure_paths = self.figure_writer.write(
            result,
            rolling_ic_window=config.rolling_ic_window,
        )
        result = FactorEvaluationResult(
            factor_name=result.factor_name,
            summary=result.summary,
            output_dir=result.output_dir,
            clean_factor_data=result.clean_factor_data,
            daily_ic=result.daily_ic,
            quantile_returns=result.quantile_returns,
            quantile_returns_by_date=result.quantile_returns_by_date,
            five_bucket_returns=result.five_bucket_returns,
            portfolio_returns=result.portfolio_returns,
            figure_paths=figure_paths,
        )
        self._log(
            f"evaluation_artifacts_written factor={factor_name} output_dir={result.output_dir}"
        )
        return result

    def _log(self, message: str) -> None:
        if self.log_info is not None:
            self.log_info(message)


def _break_factor_ties(factor: pd.Series) -> pd.Series:
    """Add a deterministic sub-ulp ordering only for quantile assignment."""
    if not isinstance(factor.index, pd.MultiIndex) or "date" not in factor.index.names:
        return factor
    dates = factor.index.get_level_values("date")
    ordinal = factor.groupby(dates, sort=False).cumcount().astype(float) + 1.0
    scale = factor.abs().groupby(dates, sort=False).transform("max").fillna(1.0)
    scale = scale.clip(lower=1.0)
    epsilon = np.finfo(float).eps * 1024
    return factor.astype(float) + ordinal * scale * epsilon
