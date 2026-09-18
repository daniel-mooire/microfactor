# doc_jq2024_sparse_ma_gap_2000d

## 因子概览

- 类别：`mean_reversion`
- 方向：`negative`
- 频率：`1d`
- 最小窗口：`2000`
- 复权方式：`hfq`
- 实现状态：`approximate`

## 公式

```text
MEAN(SAMPLE(adjusted_close,20,2000)[-18:]+adjusted_close[t-19]+adjusted_close[t])-MEAN(SAMPLE(adjusted_close,20,2000)+adjusted_close[t-19]+adjusted_close[t])
```

输入字段：`adjusted_close`

## 原理说明

用过去一段时间的价格、成交量或换手率概括股票的交易行为。

## 来源

- 逻辑来源组：`40.14年初到23年7月-年化37-夏普1.25-稳健高收益-2b2871e4`
- 来源组指纹：`2b2871e404aea9cd8590c5c6656ef28db8d5fb05f621b7307836f3cd72d7a7b0`
- `2020-2026聚宽600条源码/2024年度精选策略1/40.14年初到23年7月，年化37，夏普1.25，稳健高收益！.txt` — SHA-256 `2b2871e404aea9cd8590c5c6656ef28db8d5fb05f621b7307836f3cd72d7a7b0`
  - 归档副本：`../../sources/2020-2026聚宽600条源码/2024年度精选策略1/40.14年初到23年7月，年化37，夏普1.25，稳健高收益！.txt`
- 来源页码：`未记录`

## 复现实现

- Python 实现：`microfactor.factors.document_extended:_compute/doc_jq2024_sparse_ma_gap_2000d`
- 默认参数：`{"append_current":true,"duplicated_lag":19,"history_observations":2000,"recent_sampled_observations":18,"sampled_observations":100,"sampling_step":20,"source_buy_condition":"short_sparse_mean_minus_long_sparse_mean_below_zero","source_prefilters_omitted":["roe_above_4","lowest_100_pb","highest_50_net_profit_growth"]}`
- 适配说明：源码将2000个日频收盘价每隔20个观测抽样，并重复加入距今19个观测的价格和当前价格；所谓20日均线实际是该102点序列最后20点的均值。实现严格保留抽样与重复点，但输出全市场连续均线差，不复刻ROE、PB、利润增速筛选和周度持仓规则。

## 发布与评估

- Publication status: `unpublished`
- Evaluation status: `not_evaluated`
- 当前没有固化版本或正式评估记录；本归档不推断评估结论。
