# alpha191_152

## 因子概览

- 类别：`price_volume`
- 方向：`unspecified`
- 频率：`1d`
- 最小窗口：`156`
- 复权方式：`none`
- 实现状态：`approximate`

## 公式

```text
sma(mean(delay(sma(delay(close / delay(close, 9), 1), 9, 1), 1), 12) - mean(delay(sma(delay(close / delay(close, 9), 1), 9, 1), 1), 26), 9, 1)
```

输入字段：`close`

## 原理说明

Smooths the difference between twelve- and twenty-six-day averages of a recursively smoothed nine-day close-price ratio.

## 来源

- 逻辑来源组：`Alpha191-9f867946`
- 来源组指纹：`9f867946daeec1a1a84d0e3e7edff93a96485a94effe240d85f0d8c3f3a3f13e`
- `量化Skills合集/joinquant-docs/data/Alpha191.md` — SHA-256 `9f867946daeec1a1a84d0e3e7edff93a96485a94effe240d85f0d8c3f3a3f13e`
  - 归档副本：`../../sources/量化Skills合集/joinquant-docs/data/Alpha191.md`
- 来源页码：`未记录`

## 复现实现

- Python 实现：`microfactor.factors.alpha191_document::alpha191_152`
- 默认参数：`{"alpha191_number":152,"normalization":"Removed whitespace that split the second DELAY token. JoinQuant publishes the recurrence but not its server-side seed; the implementation uses the first valid observation as the seed and suppresses the first 156 close observations so the outer recursion receives 120 valid inputs.","normalized_expression":"sma(mean(delay(sma(delay(close / delay(close, 9), 1), 9, 1), 1), 12) - mean(delay(sma(delay(close / delay(close, 9), 1), 9, 1), 1), 26), 9, 1)","recursive_stability_window":156,"source_expression":"SMA(MEAN(DELAY(SMA(DELAY(CLOSE/DELAY(CLOSE,9),1),9,1),1),12)-MEAN(DELAY(SMA(DELAY(CLOSE/DELAY (CLOSE,9),1),9,1),1),26),9,1)","source_fq":null}`
- 适配说明：The formula is evaluated in the source-supported fq=None mode so OHLC and VWAP remain in the same unadjusted price units. The signal uses information through the T-day close and is evaluated against the standard T+1 open return. Normalization audit: Removed whitespace that split the second DELAY token. JoinQuant publishes the recurrence but not its server-side seed; the implementation uses the first valid observation as the seed and suppresses the first 156 close observations so the outer recursion receives 120 valid inputs.

## 发布与评估

- Publication status: `unpublished`
- Evaluation status: `not_evaluated`
- 当前没有固化版本或正式评估记录；本归档不推断评估结论。
