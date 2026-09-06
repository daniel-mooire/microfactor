from __future__ import annotations

from pathlib import Path

from microfactor.eval.plots import (
    plot_cumulative_ic,
    plot_daily_ic,
    plot_five_bucket_cumulative,
    plot_long_short_cumulative,
    plot_quantile_returns,
    plot_return_distribution,
    plot_rolling_ic,
)


class FactorFigureWriter:
    def write(self, result, *, rolling_ic_window: int) -> tuple[Path, ...]:
        if result.daily_ic is None:
            raise ValueError("daily_ic is required to write figures")
        if result.quantile_returns is None:
            raise ValueError("quantile_returns is required to write figures")
        if result.quantile_returns.empty or len(result.quantile_returns.columns) == 0:
            raise ValueError(f"{result.factor_name}: no quantile return periods")
        figures_dir = result.output_dir / "figures"
        for obsolete in (
            figures_dir / "long_short_cumulative.png",
            figures_dir / "return_distribution.png",
        ):
            obsolete.unlink(missing_ok=True)
        quantile_return_paths = tuple(
            plot_quantile_returns(
                result.quantile_returns,
                period=str(period),
                output_path=figures_dir / f"quantile_returns_{period}.png",
            )
            for period in result.quantile_returns.columns
        )
        paths = (
            plot_daily_ic(
                result.daily_ic,
                output_path=figures_dir / "daily_ic.png",
            ),
            plot_cumulative_ic(
                result.daily_ic,
                output_path=figures_dir / "cumulative_ic.png",
            ),
            plot_rolling_ic(
                result.daily_ic,
                window=rolling_ic_window,
                output_path=figures_dir / f"rolling_ic_{rolling_ic_window}.png",
            ),
        ) + quantile_return_paths
        if result.five_bucket_returns is not None and not result.five_bucket_returns.empty:
            paths += (
                plot_quantile_returns(
                    result.five_bucket_returns.mean().to_frame("1D"),
                    period="1D",
                    output_path=figures_dir / "quantile_returns_5_bucket_1D.png",
                ),
                plot_five_bucket_cumulative(
                    result.five_bucket_returns,
                    output_path=figures_dir / "five_bucket_cumulative_1D.png",
                ),
            )
        if result.portfolio_returns is not None and not result.portfolio_returns.empty:
            paths += (
                plot_long_short_cumulative(
                    result.portfolio_returns,
                    output_path=figures_dir / "long_short_cumulative.png",
                ),
                plot_return_distribution(
                    result.portfolio_returns,
                    output_path=figures_dir / "return_distribution.png",
                ),
            )
        return paths
