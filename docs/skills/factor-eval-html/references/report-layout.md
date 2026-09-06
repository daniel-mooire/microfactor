# Microfactor HTML Report Layout

This reference describes the stable layout implemented by
`microfactor.eval.reporting.HtmlReportRenderer`. Keep the markup simple so a
saved report remains inspectable as a local file.

## Page hierarchy

```text
main.report-shell
|- h1.page-title
|- section.threshold-panel
|  `- ul.thresholds
|- section.index-panel (run summary; one linked row per factor)
`- section.factor-section (one per factor, also retained below the index)
   |- div.factor-title + status badge + standalone-report link
   |- p.contract
   |- div.explain
   |  |- article: 计算公式
   |  |- article: 小白解读
   |  `- article: 本次样本中的原理
   |- div.cards
   |- h3 核心统计图表
   |  `- article.chart-card (one per retained chart)
   `- five-bucket summary + annual table
```

Each `factors/<factor_name>/report.html` contains the corresponding
`factor-section` in a standalone document and links back to the run summary.

The old top runtime-metadata card is intentionally absent. Run metadata stays
in `metadata.json` and `manifest.json`, while the HTML focuses on interpretation
and decision-useful results.

## Core charts

Retain these four chart files in the HTML, in this order:

| File | Caption | Meaning |
| --- | --- | --- |
| `daily_ic.png` | 每日 RankIC 散点图（含均值线） | Daily cross-sectional rank agreement; the mean line makes dispersion visible. |
| `cumulative_ic.png` | 累计 RankIC | Whether small daily signals accumulate over time. |
| `five_bucket_cumulative_1D.png` | 五档累计超额 | Long-term separation of equal-weight bucket excess returns. |
| `rolling_ic_63.png` | 63 日滚动 RankIC | Stability and regime changes after smoothing. |

Each chart needs an inline caption plus two short Chinese statements:
`图表含义` and `当前趋势`. The trend statement must be calculated from the
corresponding parquet artifact, not hard-coded.

Use responsive CSS with preserved aspect ratio, for example:

```css
.chart-card img {
  display: block;
  width: 100%;
  max-width: 100%;
  height: auto;
  aspect-ratio: 4 / 1;
  object-fit: contain;
}
```

## Metrics

Metric cards should prioritize the following fields when present:

- RankIC mean and standard deviation
- raw ICIR and HAC/adjusted t-statistic
- directional IC win rate and coverage
- quantile monotonicity
- long-short spread in bps
- annualized long-short return, Sharpe, and maximum drawdown
- final status (`通过` or `未通过`)

Do not expose the entire raw summary row as a wide HTML table. The source CSV
and parquet remain the machine-readable record.

## Five-bucket annual table

Build the annual table from `five_bucket_returns.parquet` by grouping dates by
calendar year and annualizing each bucket's equal-weight excess return. Render
the result as:

| 年份 | 第1档 | 第2档 | 第3档 | 第4档 | 第5档 |
| --- | ---: | ---: | ---: | ---: | ---: |
| 2016 | ... | ... | ... | ... | ... |

Use percentage formatting, centered numeric cells, a fixed minimum table width,
and `.table-wrap { overflow-x: auto; }` so narrow screens do not collapse the
columns.

## Content and language

The document must use UTF-8 and `lang="zh-CN"`. Formula text stays faithful to
the factor catalog. The three explanation blocks must be understandable to a
beginner and must distinguish:

1. the exact calculation;
2. what a high or low value means in plain language; and
3. what the current sample actually shows, including direction and the main
   risk.

Avoid unsupported causal claims. A backtest relationship is evidence of a
sample association, not proof that the factor causes returns.
