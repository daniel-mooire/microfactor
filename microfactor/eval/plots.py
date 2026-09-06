from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False


def plot_quantile_returns(
    quantile_returns: pd.DataFrame, *, period: str, output_path: str | Path
) -> Path:
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(24, 6))
    try:
        quantile_returns[period].plot(kind="bar", ax=ax)
        ax.set_xlabel("分位档")
        ax.set_ylabel("平均收益")
        ax.set_title(f"分位档收益（{period}）")
        fig.tight_layout()
        fig.savefig(output_path)
    finally:
        plt.close(fig)
    return output_path


def plot_cumulative_ic(daily_ic: pd.DataFrame, *, output_path: str | Path) -> Path:
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(24, 6))
    try:
        daily_ic.cumsum().plot(ax=ax)
        ax.set_xlabel("日期")
        ax.set_ylabel("累计 RankIC")
        ax.set_title("累计 RankIC")
        fig.tight_layout()
        fig.savefig(output_path)
    finally:
        plt.close(fig)
    return output_path


def plot_rolling_ic(
    daily_ic: pd.DataFrame, *, window: int, output_path: str | Path
) -> Path:
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(24, 6))
    try:
        daily_ic.rolling(window=window).mean().plot(ax=ax)
        ax.set_xlabel("日期")
        ax.set_ylabel("RankIC")
        ax.set_title(f"{window} 日滚动 RankIC")
        fig.tight_layout()
        fig.savefig(output_path)
    finally:
        plt.close(fig)
    return output_path


def plot_daily_ic(daily_ic: pd.DataFrame, *, output_path: str | Path) -> Path:
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(24, 6))
    try:
        for column in daily_ic.columns:
            series = daily_ic[column].dropna()
            ax.scatter(series.index, series, s=7, alpha=0.35, label=str(column))
        mean_value = daily_ic.mean().mean()
        ax.axhline(
            mean_value,
            color="#d95f02",
            linewidth=1.8,
            linestyle="--",
            label=f"RankIC 均值 = {mean_value:.4f}",
        )
        ax.axhline(0, color="black", linewidth=0.8)
        ax.set_xlabel("日期")
        ax.set_ylabel("RankIC")
        ax.set_title("每日 RankIC 散点图")
        ax.legend(loc="upper right")
        fig.tight_layout()
        fig.savefig(output_path)
    finally:
        plt.close(fig)
    return output_path


def plot_long_short_cumulative(
    portfolio_returns: pd.DataFrame, *, output_path: str | Path
) -> Path:
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(24, 6))
    try:
        columns = [
            column
            for column in ("gross_long_short", "net_long_short")
            if column in portfolio_returns
        ]
        if columns:
            (1 + portfolio_returns[columns].fillna(0)).cumprod().sub(1).plot(ax=ax)
        ax.set_xlabel("日期")
        ax.set_ylabel("累计收益")
        ax.set_title("多空累计收益")
        fig.tight_layout()
        fig.savefig(output_path)
    finally:
        plt.close(fig)
    return output_path


def plot_return_distribution(
    portfolio_returns: pd.DataFrame, *, output_path: str | Path
) -> Path:
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(24, 6))
    try:
        columns = [
            column
            for column in ("gross_long_short", "net_long_short")
            if column in portfolio_returns
        ]
        if columns:
            portfolio_returns[columns].dropna().plot(kind="box", ax=ax)
        ax.set_ylabel("日收益")
        ax.set_title("多空收益分布")
        fig.tight_layout()
        fig.savefig(output_path)
    finally:
        plt.close(fig)
    return output_path


def plot_five_bucket_cumulative(
    five_bucket_returns: pd.DataFrame, *, output_path: str | Path
) -> Path:
    """Plot cumulative equal-weight returns for the five skill buckets."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(24, 6))
    try:
        cumulative = (1 + five_bucket_returns.fillna(0.0)).cumprod().sub(1)
        cumulative.plot(ax=ax)
        ax.set_xlabel("日期")
        ax.set_ylabel("累计超额收益")
        ax.set_title("五档累计超额")
        fig.tight_layout()
        fig.savefig(output_path)
    finally:
        plt.close(fig)
    return output_path
