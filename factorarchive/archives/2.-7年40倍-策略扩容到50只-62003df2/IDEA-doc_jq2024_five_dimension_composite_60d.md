# doc_jq2024_five_dimension_composite_60d

## 因子概览

- 类别：`composite`
- 方向：`positive`
- 频率：`1d`
- 最小窗口：`60`
- 复权方式：`none`
- 实现状态：`approximate`

## 公式

```text
-log(total_mv)-log(circ_mv)-1.6*log(close)-0.8*log(SUM(volume,5))-2.0*log(adjusted_close/Ref(adjusted_close,59))
```

输入字段：`total_mv, circ_mv, close, volume, adjusted_close`

## 原理说明

用过去一段时间的价格、成交量或换手率概括股票的交易行为。

## 来源

- 逻辑来源组：`2.-7年40倍-策略扩容到50只-62003df2`
- 来源组指纹：`62003df231c7c1ed97de76b6c3478e9fce87f5e6a30f3f5bd488784d6c6543ad`
- `2020-2026聚宽600条源码/2024年度精选策略1/2.“7年40倍”策略扩容到50只.txt` — SHA-256 `62003df231c7c1ed97de76b6c3478e9fce87f5e6a30f3f5bd488784d6c6543ad`
  - 归档副本：`../../sources/2020-2026聚宽600条源码/2024年度精选策略1/2.“7年40倍”策略扩容到50只.txt`
- 来源页码：`未记录`

## 复现实现

- Python 实现：`microfactor.factors.document_extended:_compute/doc_jq2024_five_dimension_composite_60d`
- 默认参数：`{"cross_sectional_minima":"rank_neutral_constants_omitted","price":"unadjusted_close","return_lag":59,"return_observations":60,"return_price":"adjusted_close","source_prefilter_limit":100,"source_prefilters_omitted":["positive_pb","positive_inc_return","positive_revenue_growth","positive_net_profit_growth"],"source_volume_bars":1200,"source_volume_frequency":"1m","volume_adaptation":"sum_daily_volume_5d","weights":[1.0,1.0,1.6,0.8,2.0]}`
- 适配说明：源码以各项截面最小值归一化后取对数；这些最小值只增加当日截面常数，实现删除常数并保留完全相同的排序。源码的当前分钟未复权价格映射为日频未复权close，1200根1分钟成交量映射为5个日频成交量之和，60日首尾收益使用独立adjusted_close的60个观测。实现暴露全市场连续原始分数，不复刻最小市值100只、PB为正及三项财务增长为正的策略预筛选。

## 发布与评估

- Publication status: `unpublished`
- Evaluation status: `not_evaluated`
- 当前没有固化版本或正式评估记录；本归档不推断评估结论。
