# doc_jq2024_large_cap_five_dimension_composite_60d

## 因子概览

- 类别：`composite`
- 方向：`positive`
- 频率：`1d`
- 最小窗口：`60`
- 复权方式：`none`
- 实现状态：`approximate`

## 公式

```text
-4*log(total_mv)-4*log(circ_mv)-2*log(close)-log(SUM(volume,5))-log(adjusted_close/Ref(adjusted_close,59))
```

输入字段：`total_mv, circ_mv, close, volume, adjusted_close`

## 原理说明

用过去一段时间的价格、成交量或换手率概括股票的交易行为。

## 来源

- 逻辑来源组：`32.非线性市值-非小市值-组合4只-e3bb3402`
- 来源组指纹：`e3bb3402afe70b0933d40f6962edda66c595cf2aed33ba256eae3314752eb970`
- `2020-2026聚宽600条源码/2024年度精选策略1/32.非线性市值（非小市值）组合4只.txt` — SHA-256 `e3bb3402afe70b0933d40f6962edda66c595cf2aed33ba256eae3314752eb970`
  - 归档副本：`../../sources/2020-2026聚宽600条源码/2024年度精选策略1/32.非线性市值（非小市值）组合4只.txt`
- 来源页码：`未记录`

## 复现实现

- Python 实现：`microfactor.factors.document_extended:_compute/doc_jq2024_large_cap_five_dimension_composite_60d`
- 默认参数：`{"cross_sectional_minima":"rank_neutral_constants_omitted","price":"unadjusted_close","return_lag":59,"return_observations":60,"return_price":"adjusted_close","source_large_cap_fraction":0.7,"source_prefilters_omitted":["positive_pe","positive_pb","positive_inc_return","positive_revenue_growth","positive_net_profit_growth","ffscore_above_7"],"volume_window":5,"weight_order":["close","volume_5d","gross_return_60d","circ_mv","total_mv"],"weights":[2.0,1.0,1.0,4.0,4.0]}`
- 适配说明：源码在正PE/PB与三项正增长样本中先保留总市值最大的70%，再经FFScore筛选；实现只复现其后公开的连续五维分数，不复刻财务与大市值预筛。各项截面最小值只增加当日常数，删除后排序不变。源码的当前分钟价格映射为日频未复权close，60日收益使用adjusted_close的60个观测。

## 发布与评估

- Publication status: `unpublished`
- Evaluation status: `not_evaluated`
- 当前没有固化版本或正式评估记录；本归档不推断评估结论。
