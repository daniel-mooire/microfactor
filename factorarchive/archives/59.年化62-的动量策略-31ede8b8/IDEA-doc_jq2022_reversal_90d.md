# doc_jq2022_reversal_90d

## 因子概览

- 类别：`reversal`
- 方向：`negative`
- 频率：`1d`
- 最小窗口：`91`
- 复权方式：`qfq`
- 实现状态：`approximate`

## 公式

```text
adjusted_close/Ref(adjusted_close,90)-1
```

输入字段：`adjusted_close`

## 原理说明

用过去一段时间的价格、成交量或换手率概括股票的交易行为。

## 来源

- 逻辑来源组：`59.年化62-的动量策略-31ede8b8`
- 来源组指纹：`31ede8b8c288864c2315ab32addd7efde4ca88031ef8832b170731d03ec7639c`
- `2020-2026聚宽600条源码/2022年度精选策略/59.年化62%的动量策略.txt` — SHA-256 `31ede8b8c288864c2315ab32addd7efde4ca88031ef8832b170731d03ec7639c`
  - 归档副本：`../../sources/2020-2026聚宽600条源码/2022年度精选策略/59.年化62%的动量策略.txt`
- 来源页码：`未记录`

## 复现实现

- Python 实现：`microfactor.factors.document_extended:_compute/doc_jq2022_reversal_90d`
- 默认参数：`{"alternative_source":"2024年度精选策略1/49.年化62%的动量策略.txt","price_observations":91,"return_lag_days":90,"source_minimum_price":5.0,"source_sort":"ascending","source_stock_count":10}`
- 适配说明：The source calls the score momentum but sorts it ascending and buys the ten lowest values, so its effective direction is 90-day reversal. The implementation exposes the continuous return across the current stock universe and leaves the source's price-above-5 and listing-age filters to the common universe contract. JoinQuant's dynamic real-price history is represented by the project's qfq convention.

## 发布与评估

- Publication status: `published`
- Evaluation status: `passed`
- 因子版本：`b3e4338a4795bd8218e5`
- 数据快照：`snapshot_e3e73aa97706fd71f27ad486`
- 评估批次：`20260917_231028_ee6693d0`
- 有效区间：`2016-05-18` 至 `2026-09-15`

### 核心指标

- Rank IC Mean：`-0.042998451047`
- Rank ICIR：`-0.35749710399`
- Adjusted ICIR：`0.35749710399`
- Long-short spread (bps)：`24.666877236`
- Monotonicity：`0.975757575758`
- Coverage：`0.871997212266`
- Daily turnover (long)：`0.186765045536`
- Daily turnover (short)：`0.169238496953`
