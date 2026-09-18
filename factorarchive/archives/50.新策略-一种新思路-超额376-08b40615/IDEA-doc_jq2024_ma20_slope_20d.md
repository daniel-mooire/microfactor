# doc_jq2024_ma20_slope_20d

## 因子概览

- 类别：`trend`
- 方向：`positive`
- 频率：`1d`
- 最小窗口：`40`
- 复权方式：`qfq`
- 实现状态：`approximate`

## 公式

```text
round(100*OLS_no_intercept(MA20[t-19:t]-MA20[t-19], x=0..19).slope, 1)
```

输入字段：`adjusted_close`

## 原理说明

用过去一段时间的价格、成交量或换手率概括股票的交易行为。

## 来源

- 逻辑来源组：`50.新策略-一种新思路-超额376-08b40615`
- 来源组指纹：`08b406153fe2f50a704f7f7b0d0a53f93c40510ec8c048b543752f50acecf490`
- `2020-2026聚宽600条源码/2024年度精选策略1/50.新策略，一种新思路，超额376%！.txt` — SHA-256 `08b406153fe2f50a704f7f7b0d0a53f93c40510ec8c048b543752f50acecf490`
  - 归档副本：`../../sources/2020-2026聚宽600条源码/2024年度精选策略1/50.新策略，一种新思路，超额376%！.txt`
- 来源页码：`未记录`

## 复现实现

- Python 实现：`microfactor.factors.document_extended:_compute/doc_jq2024_ma20_slope_20d`
- 默认参数：`{"history_count_days":40,"include_intercept":false,"moving_average_window_days":20,"round_digits":1,"scale":100,"slope_observation_count":20,"source_rebalance":"monthly","source_reject_threshold":-2,"subtract_first_moving_average":true}`
- 适配说明：The source requests 40 daily closes and applies the score as a monthly filter after fundamental selection. The implementation exposes the same rolling score across the current stock universe for cross-sectional evaluation. JoinQuant's history-price adjustment is not pinned, so the project uses its standard qfq technical-price convention.

## 发布与评估

- Publication status: `published`
- Evaluation status: `rejected`
- 因子版本：`a8b3b83d2f981d171d82`
- 数据快照：`snapshot_e3e73aa97706fd71f27ad486`
- 评估批次：`20260917_231028_ee6693d0`
- 有效区间：`2016-03-04` 至 `2026-09-15`

### 核心指标

- Rank IC Mean：`-0.0224363910053`
- Rank ICIR：`-0.202043329781`
- Adjusted ICIR：`-0.202043329781`
- Long-short spread (bps)：`-12.5888818933`
- Monotonicity：`-0.648484848485`
- Coverage：`0.783054644809`
- Daily turnover (long)：`0.0703783510987`
- Daily turnover (short)：`0.071775997372`
