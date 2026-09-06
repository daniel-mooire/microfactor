---
name: factor-eval-html
description: Use when generating or reviewing Microfactor factor-evaluation HTML reports and their archived charts, metrics, and tables.
---

# Factor Eval HTML

## Purpose

Standardize the standalone HTML report produced for every evaluated factor in
Microfactor. The report is a research archive: it must be readable by a
non-specialist, reproducible from saved artifacts, and usable when opened as a
local file without network access.

This skill covers report rendering and validation only. It does not define
factor formulas, data-provider behavior, or model-training chains.

Every evaluation run produces one run-level summary page at `report.html` and
one standalone page at `factors/<factor_name>/report.html` for each factor.
The summary page is the index of record: it lists every factor, its status and
key metrics, and links to the corresponding standalone page. Each standalone
page must link back to the run summary.

## Required workflow

1. Load the evaluation run summary and the factor artifact directory. Keep the
   evaluation semantics explicit: signal at T close, `open_t1` return at T+1
   open, the configured holding period, quantiles, universe, and transaction
   cost.
2. Render the current layout through the project's `HtmlReportRenderer` (or a
   compatible renderer). Read [references/report-layout.md](references/report-layout.md)
   before changing markup or styles.
3. Keep every page self-contained: UTF-8, `lang="zh-CN"`, inline CSS, and chart
   images embedded as base64. Do not add CDN fonts, JavaScript chart libraries,
   or external image URLs.
4. Preserve the factor's formula, source, input fields, adjustment mode,
   beginner explanation, sample-specific interpretation, status, and all
   artifact paths. Do not infer missing values or silently change the
   evaluation period.
5. Validate the generated HTML and the saved artifacts before reporting
   completion. A single factor failure must remain visible as a failed or
   insufficient-data result, not remove the rest of the run.

## Non-negotiable layout rules

- Use the hierarchy: report title, threshold panel, factor index, then factor
  sections.
- Put an index table near the top of the run summary. Every factor name in the
  table must be a relative link to `factors/<factor_name>/report.html`.
- Standalone factor pages must include a visible relative link back to
  `../../report.html` and retain the same factor contract, metrics and charts.
- Do not render the deleted runtime-metadata card (run id, universe, date
  range, return type, cost) at the top of the page.
- Keep `计算公式`, `小白解读`, and `本次样本中的原理` as three vertically
  stacked sections.
- Show compact metric cards instead of a wide raw "完整指标" table.
- Do not add the verbose `口径与可交易性诊断` section; the chosen return
  semantics belong in the factor contract or concise chart notes.
- Show the four core charts in vertical order: daily RankIC scatter with mean
  line, cumulative RankIC, five-bucket cumulative excess, and 63-day rolling
  RankIC. Charts must adapt to the available width while preserving their
  aspect ratio and must not be stretched by a fixed height.
- The annual five-bucket table uses one row per year and columns `第1档` to
  `第5档`; wrap it in an overflow container for narrow screens.

## Acceptance checklist

- `report.html` exists, is valid UTF-8, is non-empty, and opens without network
  access.
- The summary index contains one link for every factor, every linked
  `factors/<factor_name>/report.html` exists, and each standalone page links
  back to the summary.
- Exactly the intended core chart images are embedded and each has a caption,
  a plain-language meaning, and a data-derived trend statement.
- The HTML contains the formula and both Chinese interpretation sections, but
  does not contain the deleted metadata card, `完整指标`, or
  `口径与可交易性诊断`.
- Metric cards expose RankIC mean/std, raw ICIR, HAC t-stat, IC win rate,
  coverage, monotonicity, long-short spread, annualized return, Sharpe, and
  drawdown when the source summary provides them.
- The annual table has a `年份` column and five bucket columns with percentage
  formatting; no bucket or year is silently dropped.
- Run the project's focused report test, `ruff`, and the full pytest suite.
  On Windows use a repository-local pytest base directory when the system temp
  directory is not writable.

## Project entry points

- Renderer: `microfactor/eval/reporting.py`
- Plot generation: `microfactor/eval/plots.py` and `microfactor/eval/figures.py`
- Report refresh: `uv run python main.py evaluate-summary --run-dir <run_dir>`
- Report tests: `tests/test_eval_reporting.py`
