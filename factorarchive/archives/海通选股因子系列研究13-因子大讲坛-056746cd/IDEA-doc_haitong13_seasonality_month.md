# doc_haitong13_seasonality_month

## 因子概览

- 类别：`seasonality`
- 方向：`unspecified`
- 频率：`1d`
- 最小窗口：`252`
- 复权方式：`hfq`
- 实现状态：`approximate`

## 公式

```text
historical point-in-time mean return of the next calendar month
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

- Python 实现：`microfactor.factors.document_extended:_compute/doc_haitong13_seasonality_month`
- 默认参数：`{"estimator":"expanding_same_calendar_month_mean","signal_timing":"previous_completed_month_end"}`
- 适配说明：The report says to use the historical average return of the same calendar month but does not prescribe a fixed sample start or minimum history. The implementation uses an expanding point-in-time mean from the available data.

## 发布与评估

- Publication status: `published`
- Evaluation status: `rejected`
- 因子版本：`b362b72b0824fc36d9be`
- 数据快照：`snapshot_e3e73aa97706fd71f27ad486`
- 评估批次：`20260917_231028_ee6693d0`
- 有效区间：`2017-02-03` 至 `2026-09-15`

### 核心指标

- Rank IC Mean：`0.00102006884091`
- Rank ICIR：`0.0193236711553`
- Adjusted ICIR：`0.0193236711553`
- Long-short spread (bps)：`-0.00409228497542`
- Monotonicity：`0.0545454545455`
- Coverage：`0.87550748183`
- Daily turnover (long)：`0.0812584345067`
- Daily turnover (short)：`0.0801415793279`
