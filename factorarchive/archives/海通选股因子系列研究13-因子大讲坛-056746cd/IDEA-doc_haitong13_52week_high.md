# doc_haitong13_52week_high

## 因子概览

- 类别：`technical`
- 方向：`unspecified`
- 频率：`1d`
- 最小窗口：`252`
- 复权方式：`hfq`
- 实现状态：`approximate`

## 公式

```text
completed_month_end_close / max(daily_close over 12 completed months)
```

输入字段：`adjusted_close`

## 原理说明

用过去一段时间的价格、成交量或换手率概括股票的交易行为。

## 来源

- 逻辑来源组：`海通选股因子系列研究13-因子大讲坛-056746cd`
- 来源组指纹：`056746cd34bd9546995868555b8418149e8519e10649c8c12365f99f77d1de4a`
- `JJJ643/量化因子挖掘思路475份/海通选股因子系列研究13：因子大讲坛.pdf` — SHA-256 `056746cd34bd9546995868555b8418149e8519e10649c8c12365f99f77d1de4a`
  - 归档副本：`../../sources/JJJ643/量化因子挖掘思路475份/海通选股因子系列研究13：因子大讲坛.pdf`
- 来源页码：`1, 7, 8`

## 复现实现

- Python 实现：`microfactor.factors.document_extended:_compute/doc_haitong13_52week_high`
- 默认参数：`{"lookback_months":12,"signal_timing":"previous_completed_month_end"}`
- 适配说明：The report defines a month-end factor for next-month returns. The implementation uses completed calendar months in the available daily universe and carries the signal through the following month.

## 发布与评估

- Publication status: `published`
- Evaluation status: `rejected`
- 因子版本：`5bc2dee925be1fee5c9d`
- 数据快照：`snapshot_e3e73aa97706fd71f27ad486`
- 评估批次：`20260917_231028_ee6693d0`
- 有效区间：`2017-01-03` 至 `2026-09-15`

### 核心指标

- Rank IC Mean：`-0.00503194870512`
- Rank ICIR：`-0.0476046462529`
- Adjusted ICIR：`-0.0476046462529`
- Long-short spread (bps)：`-7.56133668885`
- Monotonicity：`-0.975757575758`
- Coverage：`0.747630462452`
- Daily turnover (long)：`0.0599835707156`
- Daily turnover (short)：`0.0425831791953`
