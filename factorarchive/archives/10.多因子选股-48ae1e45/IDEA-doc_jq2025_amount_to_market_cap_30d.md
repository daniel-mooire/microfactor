# doc_jq2025_amount_to_market_cap_30d

## 因子概览

- 类别：`liquidity`
- 方向：`unspecified`
- 频率：`1d`
- 最小窗口：`30`
- 复权方式：`none`
- 实现状态：`approximate`

## 公式

```text
SUM(amount,30)/(total_mv*10000)
```

输入字段：`amount, total_mv`

## 原理说明

用过去一段时间的价格、成交量或换手率概括股票的交易行为。

## 来源

- 逻辑来源组：`10.多因子选股-48ae1e45`
- 来源组指纹：`48ae1e45825a57fc52ba1b184201b065ad66940b2cdaaa8668cfa0bc7f583393`
- `2020-2026聚宽600条源码/2025年度精选策略/10.多因子选股.txt` — SHA-256 `48ae1e45825a57fc52ba1b184201b065ad66940b2cdaaa8668cfa0bc7f583393`
  - 归档副本：`../../sources/2020-2026聚宽600条源码/2025年度精选策略/10.多因子选股.txt`
- 来源页码：`未记录`

## 复现实现

- Python 实现：`microfactor.factors.document_extended:_compute/doc_jq2025_amount_to_market_cap_30d`
- 默认参数：`{"amount_unit":"CNY","source_cross_sectional_transforms":["within_industry_rank","within_industry_standardization"],"total_mv_unit":"ten_thousand_CNY","window":30}`
- 适配说明：The source sends the raw 30-day activity ratio into within-industry ranking and standardization. The implementation exposes the fully specified raw continuous ratio because the current contract has no point-in-time industry panel.

## 发布与评估

- Publication status: `published`
- Evaluation status: `rejected`
- 因子版本：`129c65c5d0e24cf44bb8`
- 数据快照：`snapshot_e3e73aa97706fd71f27ad486`
- 评估批次：`20260917_231028_ee6693d0`
- 有效区间：`2016-02-19` 至 `2026-09-15`

### 核心指标

- Rank IC Mean：`-0.0383634071796`
- Rank ICIR：`-0.28419460593`
- Adjusted ICIR：`-0.28419460593`
- Long-short spread (bps)：`-11.3880202439`
- Monotonicity：`-0.939393939394`
- Coverage：`0.810967729393`
- Daily turnover (long)：`0.0475542503585`
- Daily turnover (short)：`0.041716032227`
