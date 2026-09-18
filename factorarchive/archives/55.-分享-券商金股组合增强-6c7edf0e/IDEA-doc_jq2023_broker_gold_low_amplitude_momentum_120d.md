# doc_jq2023_broker_gold_low_amplitude_momentum_120d

## 因子概览

- 类别：`momentum`
- 方向：`positive`
- 频率：`1d`
- 最小窗口：`121`
- 复权方式：`hfq`
- 实现状态：`exact`

## 公式

```text
SUM(return_1d*I[TSRANK(high/low-1,120)<=30%],120)
```

输入字段：`adjusted_close, high, low, is_suspended`

## 原理说明

用过去一段时间的价格、成交量或换手率概括股票的交易行为。

## 来源

- 逻辑来源组：`55.-分享-券商金股组合增强-6c7edf0e`
- 来源组指纹：`6c7edf0ef4bcee88cd335ade773e2edaf5aaf8617300d6b6c22804066a9aeacd`
- `2020-2026聚宽600条源码/2023年度精选策略/55.【分享】券商金股组合增强.txt` — SHA-256 `6c7edf0ef4bcee88cd335ade773e2edaf5aaf8617300d6b6c22804066a9aeacd`
  - 归档副本：`../../sources/2020-2026聚宽600条源码/2023年度精选策略/55.【分享】券商金股组合增强.txt`
- 来源页码：`未记录`

## 复现实现

- Python 实现：`microfactor.factors.document_extended:_compute/doc_jq2023_broker_gold_low_amplitude_momentum_120d`
- 默认参数：`{"fill_suspended_ohlc":"previous_close","low_amplitude_fraction":0.3,"rank":"time_series_average_percentile","window":120}`
- 适配说明：无。

## 发布与评估

- Publication status: `unpublished`
- Evaluation status: `not_evaluated`
- 当前没有固化版本或正式评估记录；本归档不推断评估结论。
