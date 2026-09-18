# doc_guangfa4_float_to_total_market_cap_ratio

## 因子概览

- 类别：`size`
- 方向：`positive`
- 频率：`1d`
- 最小窗口：`1`
- 复权方式：`none`
- 实现状态：`approximate`

## 公式

```text
circ_mv/total_mv
```

输入字段：`circ_mv, total_mv`

## 原理说明

用过去一段时间的价格、成交量或换手率概括股票的交易行为。

## 来源

- 逻辑来源组：`广发多因子系列4-沪深300成份股的应用分析上-6622acfe`
- 来源组指纹：`6622acfe1b1bb78906aafce208a4d3f90a02f23be08556d8b852dba25d607569`
- `JJJ643/量化因子挖掘思路475份/广发多因子系列4：沪深300成份股的应用分析上.pdf` — SHA-256 `6622acfe1b1bb78906aafce208a4d3f90a02f23be08556d8b852dba25d607569`
  - 归档副本：`../../sources/JJJ643/量化因子挖掘思路475份/广发多因子系列4：沪深300成份股的应用分析上.pdf`
- 来源页码：`19, 30, 32, 61, 62`

## 复现实现

- Python 实现：`microfactor.factors.document_extended:_compute/doc_guangfa4_float_to_total_market_cap_ratio`
- 默认参数：`{"denominator":"total_market_cap","numerator":"circulating_market_cap","source_frequency":"month_end","source_sort":"descending","source_universe":"CSI300"}`
- 适配说明：The report evaluates the ratio at month-end within CSI 300 constituents. The implementation exposes the same raw point-in-time ratio daily across the current stock universe; portfolio frequency and membership remain the responsibility of the evaluation contract.

## 发布与评估

- Publication status: `published`
- Evaluation status: `rejected`
- 因子版本：`8b79f79579ae5918a300`
- 数据快照：`snapshot_e3e73aa97706fd71f27ad486`
- 评估批次：`20260917_231028_ee6693d0`
- 有效区间：`2016-01-04` 至 `2026-09-15`

### 核心指标

- Rank IC Mean：`0.00143959307756`
- Rank ICIR：`0.0186248778614`
- Adjusted ICIR：`0.0186248778614`
- Long-short spread (bps)：`4.0332448432`
- Monotonicity：`0.733333333333`
- Coverage：`0.998872356786`
- Daily turnover (long)：`0.0276906763042`
- Daily turnover (short)：`0.0312203365527`
