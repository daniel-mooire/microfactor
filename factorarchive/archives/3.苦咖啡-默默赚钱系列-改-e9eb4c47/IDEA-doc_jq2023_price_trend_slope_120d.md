# doc_jq2023_price_trend_slope_120d

## 因子概览

- 类别：`momentum`
- 方向：`positive`
- 频率：`1d`
- 最小窗口：`120`
- 复权方式：`qfq`
- 实现状态：`approximate`

## 公式

```text
OLS_slope(adjusted_close[t-119:t] ~ 1 + day)
```

输入字段：`adjusted_close`

## 原理说明

用过去一段时间的价格、成交量或换手率概括股票的交易行为。

## 来源

- 逻辑来源组：`3.苦咖啡-默默赚钱系列-改-e9eb4c47`
- 来源组指纹：`e9eb4c47cdbd819d9d6200d1ecae58837ca81aa7cc78ec061eac5afd600e7cd3`
- `2020-2026聚宽600条源码/2023年度精选策略/3.苦咖啡-默默赚钱系列-改.txt` — SHA-256 `e9eb4c47cdbd819d9d6200d1ecae58837ca81aa7cc78ec061eac5afd600e7cd3`
  - 归档副本：`../../sources/2020-2026聚宽600条源码/2023年度精选策略/3.苦咖啡-默默赚钱系列-改.txt`
- 来源页码：`未记录`

## 复现实现

- Python 实现：`microfactor.factors.document_extended:_compute/doc_jq2023_price_trend_slope_120d`
- 默认参数：`{"dependent_variable":"adjusted_close","include_intercept":true,"source_correlation_threshold":0.9,"source_index":"000300.XSHG","source_normalized_slope_threshold":0.005,"source_sort":"descending_raw_slope","window_days":120}`
- 适配说明：The source ranks raw 120-day close-price slopes descending only after CSI 300 membership, tradability, price, recent-high, volume-ratio, normalized-slope, and correlation filters. The implementation exposes only that explicit continuous ranking score across the current daily stock universe. JoinQuant's dynamic real-price adjustment is not pinned, so the project uses qfq adjusted close.

## 发布与评估

- Publication status: `published`
- Evaluation status: `rejected`
- 因子版本：`ca62cbc66194537271bc`
- 数据快照：`snapshot_e3e73aa97706fd71f27ad486`
- 评估批次：`20260917_231028_ee6693d0`
- 有效区间：`2016-06-30` 至 `2026-09-15`

### 核心指标

- Rank IC Mean：`-0.0154998944954`
- Rank ICIR：`-0.150376939474`
- Adjusted ICIR：`-0.150376939474`
- Long-short spread (bps)：`-6.23314847497`
- Monotonicity：`-0.709090909091`
- Coverage：`0.631442385173`
- Daily turnover (long)：`0.0296558094278`
- Daily turnover (short)：`0.0285579022572`
