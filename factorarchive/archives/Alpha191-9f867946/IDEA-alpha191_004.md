# alpha191_004

## 因子概览

- 类别：`price_volume`
- 方向：`unspecified`
- 频率：`1d`
- 最小窗口：`20`
- 复权方式：`none`
- 实现状态：`exact`

## 公式

```text
(((sum(close, 8) / 8) + std(close, 8)) < (sum(close, 2) / 2)) ? -1 : (((sum(close, 2) / 2) < ((sum(close, 8) / 8) - std(close, 8))) ? 1 : (((1 < (volume / mean(volume, 20))) || ((volume / mean(volume, 20)) == 1)) ? 1 : -1))
```

输入字段：`close, volume`

## 原理说明

Discrete trend-versus-volume regime signal from 2-, 8-, and 20-day windows.

## 来源

- 逻辑来源组：`Alpha191-9f867946`
- 来源组指纹：`9f867946daeec1a1a84d0e3e7edff93a96485a94effe240d85f0d8c3f3a3f13e`
- `量化Skills合集/joinquant-docs/data/Alpha191.md` — SHA-256 `9f867946daeec1a1a84d0e3e7edff93a96485a94effe240d85f0d8c3f3a3f13e`
  - 归档副本：`../../sources/量化Skills合集/joinquant-docs/data/Alpha191.md`
- 来源页码：`未记录`

## 复现实现

- Python 实现：`microfactor.factors.alpha191_document::alpha191_004`
- 默认参数：`{"alpha191_number":4,"normalization":"Only case, whitespace, and redundant literal multiplication were normalized.","normalized_expression":"(((sum(close, 8) / 8) + std(close, 8)) < (sum(close, 2) / 2)) ? -1 : (((sum(close, 2) / 2) < ((sum(close, 8) / 8) - std(close, 8))) ? 1 : (((1 < (volume / mean(volume, 20))) || ((volume / mean(volume, 20)) == 1)) ? 1 : -1))","recursive_stability_window":null,"source_expression":"((((SUM(CLOSE,8)/8)+STD(CLOSE,8))<(SUM(CLOSE,2)/2))?(-1):(((SUM(CLOSE,2)/2)<((SUM(CLOSE,8)/8)-STD(CLOSE,8)))?1:(((1<(VOLUME/MEAN(VOLUME,20)))||((VOLUME/MEAN(VOLUME,20))==1))?1:-1)))","source_fq":null}`
- 适配说明：The formula is evaluated in the source-supported fq=None mode so OHLC and VWAP remain in the same unadjusted price units. The signal uses information through the T-day close and is evaluated against the standard T+1 open return. Normalization audit: Only case, whitespace, and redundant literal multiplication were normalized.

## 发布与评估

- Publication status: `unpublished`
- Evaluation status: `not_evaluated`
- 当前没有固化版本或正式评估记录；本归档不推断评估结论。
