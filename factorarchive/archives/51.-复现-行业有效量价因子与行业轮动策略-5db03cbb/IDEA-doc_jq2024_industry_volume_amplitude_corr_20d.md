# doc_jq2024_industry_volume_amplitude_corr_20d

## 因子概览

- 类别：`price_volume`
- 方向：`unspecified`
- 频率：`1d`
- 最小窗口：`20`
- 复权方式：`qfq`
- 实现状态：`approximate`

## 公式

```text
CORR(CS_RANK(volume/Ref(volume,1)-1),CS_RANK(high/low-1),20)
```

输入字段：`high, low, volume`

## 原理说明

用过去一段时间的价格、成交量或换手率概括股票的交易行为。

## 来源

- 逻辑来源组：`51.-复现-行业有效量价因子与行业轮动策略-5db03cbb`
- 来源组指纹：`5db03cbbdddd5cf6077e6cac313ad8d6c8768a5a5d4a8ebff772fd4bde1bd7d6`
- `2020-2026聚宽600条源码/2024年度精选策略1/51.【复现】行业有效量价因子与行业轮动策略.txt` — SHA-256 `5db03cbbdddd5cf6077e6cac313ad8d6c8768a5a5d4a8ebff772fd4bde1bd7d6`
  - 归档副本：`../../sources/2020-2026聚宽600条源码/2024年度精选策略1/51.【复现】行业有效量价因子与行业轮动策略.txt`
- 来源页码：`未记录`

## 复现实现

- Python 实现：`microfactor.factors.document_extended:_compute/doc_jq2024_industry_volume_amplitude_corr_20d`
- 默认参数：`{"correlation":"pearson","rank":"daily_cross_sectional_average_percentile","source_asset_type":"industry_etf","source_windows":[5,10,20,60,120,180],"window_days":20}`
- 适配说明：The source applies these formulas to industry ETFs and lists 5/10/20/60/120/180-day windows, but the external VolumePriceFactor192 generator is absent. The implementation publishes only the explicitly listed 20-day formula as an individual-stock daily signal, uses qfq OHLC to avoid corporate-action jumps, and evaluates future one-day open returns instead of the source model's t+2 close versus t+1 open label.

## 发布与评估

- Publication status: `unpublished`
- Evaluation status: `not_evaluated`
- 当前没有固化版本或正式评估记录；本归档不推断评估结论。
