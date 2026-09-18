# doc_jq2023_ma_dispersion_alignment_75d

## 因子概览

- 类别：`trend`
- 方向：`negative`
- 频率：`1d`
- 最小窗口：`75`
- 复权方式：`qfq`
- 实现状态：`approximate`

## 公式

```text
SUM(RMS((MA13,MA21,MA55)/MEDIAN-1),lags=1..20)-SUM(IF(MA13>=MA21>=MA55,(MA13-MA21)/MA21+(MA21-MA55)/MA55,0),lags=0..4)
```

输入字段：`adjusted_close`

## 原理说明

用过去一段时间的价格、成交量或换手率概括股票的交易行为。

## 来源

- 逻辑来源组：`49.-7日趋势-交易策略-4a9e21d0`
- 来源组指纹：`4a9e21d05fb014d129ea24928cec287311511cfadc6c5ff8c308e26b52277989`
- `2020-2026聚宽600条源码/2023年度精选策略/49.【7日趋势】交易策略.txt` — SHA-256 `4a9e21d05fb014d129ea24928cec287311511cfadc6c5ff8c308e26b52277989`
  - 归档副本：`../../sources/2020-2026聚宽600条源码/2023年度精选策略/49.【7日趋势】交易策略.txt`
- 来源页码：`未记录`

## 复现实现

- Python 实现：`microfactor.factors.document_extended:_compute/doc_jq2023_ma_dispersion_alignment_75d`
- 默认参数：`{"alignment_lags":[0,1,2,3,4],"dispersion_center":"cross_ma_median","dispersion_lags":[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20],"moving_average_windows":[13,21,55],"source_keep_threshold":0.005,"source_sort":"ascending"}`
- 适配说明：The source ranks the score ascending after turnover, market-cap, listing-age, moving-average, and volume filters, but then keeps only scores above 0.005. The implementation exposes the continuous rolling score across the current stock universe and does not resolve that source-level ranking/threshold conflict.

## 发布与评估

- Publication status: `published`
- Evaluation status: `rejected`
- 因子版本：`e4fc5008b232ee9dbb87`
- 数据快照：`snapshot_e3e73aa97706fd71f27ad486`
- 评估批次：`20260917_231028_ee6693d0`
- 有效区间：`2016-04-25` 至 `2026-09-15`

### 核心指标

- Rank IC Mean：`0.00932745426786`
- Rank ICIR：`0.0867275443318`
- Adjusted ICIR：`-0.0867275443318`
- Long-short spread (bps)：`-11.5364907721`
- Monotonicity：`-0.781818181818`
- Coverage：`0.70581875742`
- Daily turnover (long)：`0.0983114474258`
- Daily turnover (short)：`0.0694798423327`
