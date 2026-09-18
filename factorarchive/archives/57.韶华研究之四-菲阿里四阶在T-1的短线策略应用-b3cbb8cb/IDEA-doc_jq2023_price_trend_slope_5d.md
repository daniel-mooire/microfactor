# doc_jq2023_price_trend_slope_5d

## 因子概览

- 类别：`momentum`
- 方向：`positive`
- 频率：`1d`
- 最小窗口：`5`
- 复权方式：`qfq`
- 实现状态：`approximate`

## 公式

```text
round(OLS_slope(adjusted_close[t-4:t] ~ 1 + day), 3)
```

输入字段：`adjusted_close`

## 原理说明

用过去一段时间的价格、成交量或换手率概括股票的交易行为。

## 来源

- 逻辑来源组：`57.韶华研究之四-菲阿里四阶在T-1的短线策略应用-b3cbb8cb`
- 来源组指纹：`b3cbb8cb957298328a09e4fa9f632d907d27956644634640bec5015a253eb974`
- `2020-2026聚宽600条源码/2023年度精选策略/57.韶华研究之四-菲阿里四阶在T+1的短线策略应用.txt` — SHA-256 `b3cbb8cb957298328a09e4fa9f632d907d27956644634640bec5015a253eb974`
  - 归档副本：`../../sources/2020-2026聚宽600条源码/2023年度精选策略/57.韶华研究之四-菲阿里四阶在T+1的短线策略应用.txt`
- 来源页码：`未记录`

## 复现实现

- Python 实现：`microfactor.factors.document_extended:_compute/doc_jq2023_price_trend_slope_5d`
- 默认参数：`{"dependent_variable":"adjusted_close","include_intercept":true,"round_decimals":3,"source_keep_threshold":2.0,"source_prefilter_min_slope":0.0,"source_prefilter_window_days":60,"source_sort":"descending_raw_slope","window_days":5}`
- 适配说明：The source first applies tradability, listing-age, price, market-cap, PE, PB, and positive 60-day raw-slope filters, then keeps stocks whose rounded 5-day raw close-price slope exceeds 2. The implementation exposes only the explicit rounded 5-day continuous score across the current daily universe; it does not reproduce the upstream filters or the T+1 limit-order strategy.

## 发布与评估

- Publication status: `published`
- Evaluation status: `rejected`
- 因子版本：`6ec8f258d8286142539a`
- 数据快照：`snapshot_e3e73aa97706fd71f27ad486`
- 评估批次：`20260917_231028_ee6693d0`
- 有效区间：`2016-01-08` 至 `2026-09-15`

### 核心指标

- Rank IC Mean：`-0.0400992776805`
- Rank ICIR：`-0.335813657117`
- Adjusted ICIR：`-0.335813657117`
- Long-short spread (bps)：`-27.0377994744`
- Monotonicity：`-0.454545454545`
- Coverage：`0.922290335002`
- Daily turnover (long)：`0.371060052303`
- Daily turnover (short)：`0.383931788898`
