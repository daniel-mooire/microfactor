# doc_jq2025_volume_to_float_30d

## 因子概览

- 类别：`liquidity`
- 方向：`unspecified`
- 频率：`1d`
- 最小窗口：`30`
- 复权方式：`none`
- 实现状态：`approximate`

## 公式

```text
SUM(volume,30)/(circ_mv*10000/close)
```

输入字段：`volume, circ_mv, close`

## 原理说明

用过去一段时间的价格、成交量或换手率概括股票的交易行为。

## 来源

- 逻辑来源组：`10.多因子选股-48ae1e45`
- 来源组指纹：`48ae1e45825a57fc52ba1b184201b065ad66940b2cdaaa8668cfa0bc7f583393`
- `2020-2026聚宽600条源码/2025年度精选策略/10.多因子选股.txt` — SHA-256 `48ae1e45825a57fc52ba1b184201b065ad66940b2cdaaa8668cfa0bc7f583393`
  - 归档副本：`../../sources/2020-2026聚宽600条源码/2025年度精选策略/10.多因子选股.txt`
- 来源页码：`未记录`

## 复现实现

- Python 实现：`microfactor.factors.document_extended:_compute/doc_jq2025_volume_to_float_30d`
- 默认参数：`{"circ_mv_unit":"ten_thousand_CNY","circulating_shares":"circ_mv*10000/close","source_cross_sectional_transforms":["within_industry_rank","within_industry_standardization"],"source_denominator_timing":"window_end","volume_unit":"shares","window":30}`
- 适配说明：The source uses window-end circulating shares and then applies within-industry ranking and standardization. The implementation derives the same point-in-time share count from circ_mv/close and exposes the raw continuous ratio because no audited industry panel is available.

## 发布与评估

- Publication status: `published`
- Evaluation status: `rejected`
- 因子版本：`fbddeb0a6804b37c58df`
- 数据快照：`snapshot_e3e73aa97706fd71f27ad486`
- 评估批次：`20260917_231028_ee6693d0`
- 有效区间：`2016-02-19` 至 `2026-09-15`

### 核心指标

- Rank IC Mean：`-0.038930623545`
- Rank ICIR：`-0.292366735164`
- Adjusted ICIR：`-0.292366735164`
- Long-short spread (bps)：`-14.5084312653`
- Monotonicity：`-0.975757575758`
- Coverage：`0.810967729393`
- Daily turnover (long)：`0.0406586127222`
- Daily turnover (short)：`0.0355053566912`
