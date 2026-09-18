# doc_huatai_ai32_low_return_corr_10d

## 因子概览

- 类别：`price_volume`
- 方向：`unspecified`
- 频率：`1d`
- 最小窗口：`10`
- 复权方式：`hfq`
- 实现状态：`approximate`

## 公式

```text
ts_corr(low,return1,10)
```

输入字段：`low, close_to_close_total_return_1d`

## 原理说明

用过去一段时间的价格、成交量或换手率概括股票的交易行为。

## 来源

- 逻辑来源组：`华泰人工智能系列32-AlphaNet-因子挖掘神经网络-3ddfa830`
- 来源组指纹：`3ddfa83027df1c9a66f1c7af5c7c262eac6c1297cc7612d1fc5c17d7bc812858`
- `JJJ643/量化因子挖掘思路475份/华泰人工智能系列32：AlphaNet：因子挖掘神经网络.pdf` — SHA-256 `3ddfa83027df1c9a66f1c7af5c7c262eac6c1297cc7612d1fc5c17d7bc812858`
  - 归档副本：`../../sources/JJJ643/量化因子挖掘思路475份/华泰人工智能系列32：AlphaNet：因子挖掘神经网络.pdf`
- 来源页码：`8, 11, 12, 13, 17, 21`

## 复现实现

- Python 实现：`microfactor.factors.document_extended:_compute/doc_huatai_ai32_low_return_corr_10d`
- 默认参数：`{"correlation":"pearson","feature_stage":"pre_bn","free_turn":"turnover_rate_f","return1":"close_to_close_total_return_1d","std_ddof":1,"window":10}`
- 适配说明：The report exposes these transformations as AlphaNet-v1 intermediate features, then applies trainable batch normalization and a neural-network ensemble whose learned gamma, beta, batch moments, weights, and random seeds are not published. The implementation therefore publishes the transparent pre-BN daily feature as a standalone factor, maps return1 to close_to_close_total_return_1d and free_turn to turnover_rate_f, uses pandas Pearson correlation or sample standard deviation (ddof=1), and uses hfq high/low to avoid corporate-action discontinuities. It is not a reproduction of the AlphaNet composite prediction.

## 发布与评估

- Publication status: `unpublished`
- Evaluation status: `not_evaluated`
- 当前没有固化版本或正式评估记录；本归档不推断评估结论。
