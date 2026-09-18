# doc_haitong13_amihud_12m

## 因子概览

- 类别：`liquidity`
- 方向：`unspecified`
- 频率：`1d`
- 最小窗口：`252`
- 复权方式：`hfq`
- 实现状态：`approximate`

## 公式

```text
mean over 12 completed months of abs(daily_return)/daily_share_volume
```

输入字段：`close_to_close_total_return_1d, volume`

## 原理说明

用过去一段时间的价格、成交量或换手率概括股票的交易行为。

## 来源

- 逻辑来源组：`海通选股因子系列研究13-因子大讲坛-056746cd`
- 来源组指纹：`056746cd34bd9546995868555b8418149e8519e10649c8c12365f99f77d1de4a`
- `JJJ643/量化因子挖掘思路475份/海通选股因子系列研究13：因子大讲坛.pdf` — SHA-256 `056746cd34bd9546995868555b8418149e8519e10649c8c12365f99f77d1de4a`
  - 归档副本：`../../sources/JJJ643/量化因子挖掘思路475份/海通选股因子系列研究13：因子大讲坛.pdf`
- 来源页码：`1, 7, 8`

## 复现实现

- Python 实现：`microfactor.factors.document_extended:_compute/doc_haitong13_amihud_12m`
- 默认参数：`{"lookback_months":12,"signal_timing":"previous_completed_month_end","volume_unit":"shares"}`
- 适配说明：The report defines a month-end factor for next-month returns. The implementation uses completed calendar months in the available daily universe and carries the signal through the following month.

## 发布与评估

- Publication status: `published`
- Evaluation status: `rejected`
- 因子版本：`6aa7d006bde7449ca1d8`
- 数据快照：`snapshot_e3e73aa97706fd71f27ad486`
- 评估批次：`20260917_231028_ee6693d0`
- 有效区间：`2017-01-03` 至 `2026-09-15`

### 核心指标

- Rank IC Mean：`0.00287149533115`
- Rank ICIR：`0.0267488071528`
- Adjusted ICIR：`0.0267488071528`
- Long-short spread (bps)：`-1.79071888659`
- Monotonicity：`-0.975757575758`
- Coverage：`0.76061264319`
- Daily turnover (long)：`0.0263092110704`
- Daily turnover (short)：`0.0342232110488`
