# doc_jq2025_ma_dispersion_alignment_90d

## 因子概览

- 类别：`trend`
- 方向：`negative`
- 频率：`1d`
- 最小窗口：`90`
- 复权方式：`qfq`
- 实现状态：`approximate`

## 公式

```text
SUM(RMS((MA10,MA20,MA30,MA60)/MEDIAN-1),lags=1..30)-SUM(IF(MA10>=MA20>=MA30>=MA60,SUM(adjacent_MA_spreads),0),lags=0..4)
```

输入字段：`adjusted_close`

## 原理说明

用过去一段时间的价格、成交量或换手率概括股票的交易行为。

## 来源

- 逻辑来源组：`96.分享一个简单的选股器-9f157db1`
- 来源组指纹：`9f157db1512273a91515b8fbcb0f9b8386651fee5412ab2fe558b09363b1e0de`
- `2020-2026聚宽600条源码/2025年度精选策略/96.分享一个简单的选股器.txt` — SHA-256 `9f157db1512273a91515b8fbcb0f9b8386651fee5412ab2fe558b09363b1e0de`
  - 归档副本：`../../sources/2020-2026聚宽600条源码/2025年度精选策略/96.分享一个简单的选股器.txt`
- 来源页码：`未记录`

## 复现实现

- Python 实现：`microfactor.factors.document_extended:_compute/doc_jq2025_ma_dispersion_alignment_90d`
- 默认参数：`{"alignment_lags":[0,1,2,3,4],"dispersion_center":"cross_ma_median","dispersion_lags":[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30],"moving_average_windows":[10,20,30,60],"source_sort":"ascending"}`
- 适配说明：The source applies the score after turnover, listing-age, price-volume, moving-average, and candlestick filters, then keeps the lowest scores. The implementation exposes the same continuous rolling score across the current stock universe. The source does not pin price adjustment, so the project uses its standard qfq technical-price convention.

## 发布与评估

- Publication status: `published`
- Evaluation status: `rejected`
- 因子版本：`f547fa385342b329c4d2`
- 数据快照：`snapshot_e3e73aa97706fd71f27ad486`
- 评估批次：`20260917_231028_ee6693d0`
- 有效区间：`2016-05-17` 至 `2026-09-15`

### 核心指标

- Rank IC Mean：`0.00242927083873`
- Rank ICIR：`0.0214778791196`
- Adjusted ICIR：`-0.0214778791196`
- Long-short spread (bps)：`-9.06061463448`
- Monotonicity：`-0.490909090909`
- Coverage：`0.678715764331`
- Daily turnover (long)：`0.0837374697626`
- Daily turnover (short)：`0.0526169927196`
