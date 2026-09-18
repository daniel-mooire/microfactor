# alpha191_042

## 因子概览

- 类别：`price_volume`
- 方向：`unspecified`
- 频率：`1d`
- 最小窗口：`10`
- 复权方式：`none`
- 实现状态：`exact`

## 公式

```text
(-1 * rank(std(high, 10))) * corr(high, volume, 10)
```

输入字段：`high, volume`

## 原理说明

Combines high-price volatility rank with the ten-day high/volume correlation.

## 来源

- 逻辑来源组：`Alpha191-9f867946`
- 来源组指纹：`9f867946daeec1a1a84d0e3e7edff93a96485a94effe240d85f0d8c3f3a3f13e`
- `量化Skills合集/joinquant-docs/data/Alpha191.md` — SHA-256 `9f867946daeec1a1a84d0e3e7edff93a96485a94effe240d85f0d8c3f3a3f13e`
  - 归档副本：`../../sources/量化Skills合集/joinquant-docs/data/Alpha191.md`
- 来源页码：`未记录`

## 复现实现

- Python 实现：`microfactor.factors.alpha191_document::alpha191_042`
- 默认参数：`{"alpha191_number":42,"normalization":"Removed one unmatched closing parenthesis from the source.","normalized_expression":"(-1 * rank(std(high, 10))) * corr(high, volume, 10)","recursive_stability_window":null,"source_expression":"(-1*RANK(STD(HIGH,10)))*CORR(HIGH,VOLUME,10))","source_fq":null}`
- 适配说明：The formula is evaluated in the source-supported fq=None mode so OHLC and VWAP remain in the same unadjusted price units. The signal uses information through the T-day close and is evaluated against the standard T+1 open return. Normalization audit: Removed one unmatched closing parenthesis from the source.

## 发布与评估

- Publication status: `unpublished`
- Evaluation status: `not_evaluated`
- 当前没有固化版本或正式评估记录；本归档不推断评估结论。
