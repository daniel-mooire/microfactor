# doc_haitong13_share_volume_3m

## 因子概览

- 类别：`liquidity`
- 方向：`unspecified`
- 频率：`1d`
- 最小窗口：`63`
- 复权方式：`none`
- 实现状态：`approximate`

## 公式

```text
mean over 3 completed months of daily volume/free_float_shares
```

输入字段：`turnover_percent`

## 原理说明

用过去一段时间的价格、成交量或换手率概括股票的交易行为。

## 来源

- 逻辑来源组：`海通选股因子系列研究13-因子大讲坛-056746cd`
- 来源组指纹：`056746cd34bd9546995868555b8418149e8519e10649c8c12365f99f77d1de4a`
- `JJJ643/量化因子挖掘思路475份/海通选股因子系列研究13：因子大讲坛.pdf` — SHA-256 `056746cd34bd9546995868555b8418149e8519e10649c8c12365f99f77d1de4a`
  - 归档副本：`../../sources/JJJ643/量化因子挖掘思路475份/海通选股因子系列研究13：因子大讲坛.pdf`
- 来源页码：`1, 7, 8`

## 复现实现

- Python 实现：`microfactor.factors.document_extended:_compute/doc_haitong13_share_volume_3m`
- 默认参数：`{"lookback_months":3,"proxy":"turnover_percent","signal_timing":"previous_completed_month_end"}`
- 适配说明：The report defines a month-end factor for next-month returns. The implementation uses completed calendar months in the available daily universe and carries the signal through the following month.

## 发布与评估

- Publication status: `published`
- Evaluation status: `rejected`
- 因子版本：`cd1264e6d728390a621a`
- 数据快照：`snapshot_e3e73aa97706fd71f27ad486`
- 评估批次：`20260917_231028_ee6693d0`
- 有效区间：`2016-04-01` 至 `2026-09-15`

### 核心指标

- Rank IC Mean：`-0.0228850866661`
- Rank ICIR：`-0.18044397282`
- Adjusted ICIR：`-0.18044397282`
- Long-short spread (bps)：`-7.46006180307`
- Monotonicity：`-0.842424242424`
- Coverage：`0.937162863887`
- Daily turnover (long)：`0.0364381379308`
- Daily turnover (short)：`0.0559416600624`
