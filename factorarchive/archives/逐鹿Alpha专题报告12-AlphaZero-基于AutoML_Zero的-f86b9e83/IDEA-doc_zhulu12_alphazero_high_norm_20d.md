# doc_zhulu12_alphazero_high_norm_20d

## 因子概览

- 类别：`mean_reversion`
- 方向：`negative`
- 频率：`1d`
- 最小窗口：`20`
- 复权方式：`qfq`
- 实现状态：`approximate`

## 公式

```text
TS_ZSCORE(CS_ZSCORE(high),20)
```

输入字段：`high`

## 原理说明

用过去一段时间的价格、成交量或换手率概括股票的交易行为。

## 来源

- 逻辑来源组：`逐鹿Alpha专题报告12-AlphaZero-基于AutoML_Zero的-f86b9e83`
- 来源组指纹：`f86b9e838809d9e78b39a587a3cbcdaaf4dc52ed90ab3ee0c3be1d04db081e14`
- `JJJ643/量化因子挖掘思路475份/逐鹿Alpha专题报告12：AlphaZero，基于AutoML_Zero的.pdf` — SHA-256 `f86b9e838809d9e78b39a587a3cbcdaaf4dc52ed90ab3ee0c3be1d04db081e14`
  - 归档副本：`../../sources/JJJ643/量化因子挖掘思路475份/逐鹿Alpha专题报告12：AlphaZero，基于AutoML_Zero的.pdf`
- 来源页码：`6, 12, 13`

## 复现实现

- Python 实现：`microfactor.factors.document_extended:_compute/doc_zhulu12_alphazero_high_norm_20d`
- 默认参数：`{"cross_sectional_standardization":"sample_zscore","standard_deviation_ddof":1,"time_series_standardization":"rolling_sample_zscore","window_days":20}`
- 适配说明：报告明确将公式解释为最高价横截面标准化后的20日时序标准化，但算子表漏列ts_norm且未声明价格复权、标准差自由度；实现采用样本z-score和项目统一的qfq技术价格口径。

## 发布与评估

- Publication status: `unpublished`
- Evaluation status: `not_evaluated`
- 当前没有固化版本或正式评估记录；本归档不推断评估结论。
