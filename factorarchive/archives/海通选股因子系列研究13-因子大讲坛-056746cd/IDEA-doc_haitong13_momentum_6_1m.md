# doc_haitong13_momentum_6_1m

## 因子概览

- 类别：`momentum`
- 方向：`unspecified`
- 频率：`1d`
- 最小窗口：`126`
- 复权方式：`hfq`
- 实现状态：`approximate`

## 公式

```text
month_end_TRI[t-1] / month_end_TRI[t-7] - 1
```

输入字段：`close_total_return_index`

## 原理说明

用过去一段时间的价格、成交量或换手率概括股票的交易行为。

## 来源

- 逻辑来源组：`海通选股因子系列研究13-因子大讲坛-056746cd`
- 来源组指纹：`056746cd34bd9546995868555b8418149e8519e10649c8c12365f99f77d1de4a`
- `JJJ643/量化因子挖掘思路475份/海通选股因子系列研究13：因子大讲坛.pdf` — SHA-256 `056746cd34bd9546995868555b8418149e8519e10649c8c12365f99f77d1de4a`
  - 归档副本：`../../sources/JJJ643/量化因子挖掘思路475份/海通选股因子系列研究13：因子大讲坛.pdf`
- 来源页码：`1, 7, 8`

## 复现实现

- Python 实现：`microfactor.factors.document_extended:_compute/doc_haitong13_momentum_6_1m`
- 默认参数：`{"signal_frequency":"monthly","signal_timing":"previous_completed_month_end"}`
- 适配说明：The report forms factors at month-end for next-month returns. The implementation uses completed calendar month-ends in the available daily universe and exposes each value throughout the following month.

## 发布与评估

- Publication status: `published`
- Evaluation status: `rejected`
- 因子版本：`6ac402e85c2a5fa2cd78`
- 数据快照：`snapshot_e3e73aa97706fd71f27ad486`
- 评估批次：`20260917_231028_ee6693d0`
- 有效区间：`2016-08-01` 至 `2026-09-15`

### 核心指标

- Rank IC Mean：`-0.0180440800151`
- Rank ICIR：`-0.17245692541`
- Adjusted ICIR：`-0.17245692541`
- Long-short spread (bps)：`-9.02670062963`
- Monotonicity：`-0.915151515152`
- Coverage：`0.804355691057`
- Daily turnover (long)：`0.0518238209968`
- Daily turnover (short)：`0.0478184199204`
