# doc_jq2020_ma20_residual_zscore_60d

## 因子概览

- 类别：`mean_reversion`
- 方向：`negative`
- 频率：`1d`
- 最小窗口：`79`
- 复权方式：`qfq`
- 实现状态：`approximate`

## 公式

```text
zscore(adjusted_close-MA(adjusted_close,20),60,ddof=1)
```

输入字段：`adjusted_close`

## 原理说明

用过去一段时间的价格、成交量或换手率概括股票的交易行为。

## 来源

- 逻辑来源组：`18-均值回归策略分享-3cd29da8`
- 来源组指纹：`3cd29da86ab46708040d777560d8205b2968a50a00d056f2c97ab788beaf2886`
- `2020-2026聚宽600条源码/2020年度精选策略/18 均值回归策略分享.txt` — SHA-256 `3cd29da86ab46708040d777560d8205b2968a50a00d056f2c97ab788beaf2886`
  - 归档副本：`../../sources/2020-2026聚宽600条源码/2020年度精选策略/18 均值回归策略分享.txt`
  - 历史库存 SHA-256：`a9124561fda7a58b72f3519c8ed5755bdc34beb8c5db8adcb4682a45a4ea8a17`（当前文件内容已变化）
- 来源页码：`未记录`

## 复现实现

- Python 实现：`microfactor.factors.document_extended:_compute/doc_jq2020_ma20_residual_zscore_60d`
- 默认参数：`{"moving_average_window_days":20,"residual_std_ddof":1,"residual_zscore_window_days":60,"source_buy_threshold":-2,"source_sell_threshold":1,"source_stock_count":5}`
- 适配说明：The source trades a fixed five-stock list and applies buy/sell thresholds of -2 and 1. The implementation exposes the same rolling score across the current daily stock universe for cross-sectional evaluation. JoinQuant's historical-price adjustment is not pinned in the source, so the project uses its standard qfq technical-price convention.

## 发布与评估

- Publication status: `published`
- Evaluation status: `passed`
- 因子版本：`d85a2e47e0620a8e3306`
- 数据快照：`snapshot_e3e73aa97706fd71f27ad486`
- 评估批次：`20260917_231028_ee6693d0`
- 有效区间：`2016-04-29` 至 `2026-09-15`

### 核心指标

- Rank IC Mean：`-0.0446449842136`
- Rank ICIR：`-0.372062549844`
- Adjusted ICIR：`0.372062549844`
- Long-short spread (bps)：`27.1932220527`
- Monotonicity：`0.50303030303`
- Coverage：`0.698317875545`
- Daily turnover (long)：`0.252927143582`
- Daily turnover (short)：`0.342093427926`
