# doc_jq2024_ma90_bias_slope_20d

## 因子概览

- 类别：`trend`
- 方向：`positive`
- 频率：`1d`
- 最小窗口：`110`
- 复权方式：`qfq`
- 实现状态：`approximate`

## 公式

```text
10000*OLS_slope((adjusted_close/MA90)/first(adjusted_close/MA90), x=0..19)
```

输入字段：`adjusted_close`

## 原理说明

用过去一段时间的价格、成交量或换手率概括股票的交易行为。

## 来源

- 逻辑来源组：`10.多因子宽基ETF择时轮动改进版-高收益大资金低回撤-95faba69`
- 来源组指纹：`95faba69b82ac6b29bc9d7eb30ced65e02a17f6a4115969bd15818f1ad15bb4c`
- `2020-2026聚宽600条源码/2024年度精选策略1/10.多因子宽基ETF择时轮动改进版-高收益大资金低回撤.txt` — SHA-256 `95faba69b82ac6b29bc9d7eb30ced65e02a17f6a4115969bd15818f1ad15bb4c`
  - 归档副本：`../../sources/2020-2026聚宽600条源码/2024年度精选策略1/10.多因子宽基ETF择时轮动改进版-高收益大资金低回撤.txt`
- 来源页码：`未记录`

## 复现实现

- Python 实现：`microfactor.factors.document_extended:_compute/doc_jq2024_ma90_bias_slope_20d`
- 默认参数：`{"bias_moving_average_days":90,"excluded_holding_switch_multiplier":1.04,"history_count_days":110,"include_intercept":true,"normalize_by_first_bias":true,"slope_scale":10000.0,"slope_window_days":20,"source_asset_type":"broad_market_etf","source_sort":"descending"}`
- 适配说明：The source ranks a fixed broad-market ETF pool by this score descending. The implementation applies the same 90-day bias and 20-day normalized OLS slope to the current stock universe. It excludes the source's 1.04 holding switch multiplier, RSRS index timing, and intraday stop rules because those depend on portfolio state rather than the raw ranking score. JoinQuant's dynamic real-price history is represented by the project's qfq convention.

## 发布与评估

- Publication status: `published`
- Evaluation status: `rejected`
- 因子版本：`f5367bcd7b29bd582284`
- 数据快照：`snapshot_e3e73aa97706fd71f27ad486`
- 评估批次：`20260917_231028_ee6693d0`
- 有效区间：`2016-06-16` 至 `2026-09-15`

### 核心指标

- Rank IC Mean：`-0.0397820390425`
- Rank ICIR：`-0.337350040889`
- Adjusted ICIR：`-0.337350040889`
- Long-short spread (bps)：`-21.7114392003`
- Monotonicity：`-0.551515151515`
- Coverage：`0.646355537721`
- Daily turnover (long)：`0.124785381858`
- Daily turnover (short)：`0.116713714144`
