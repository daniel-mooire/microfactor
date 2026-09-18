# doc_cmo_10

## 因子概览

- 类别：`reversal`
- 方向：`unspecified`
- 频率：`1d`
- 最小窗口：`10`
- 复权方式：`hfq`
- 实现状态：`exact`

## 公式

```text
100*(SUM(up,10)-SUM(down,10))/(SUM(up,10)+SUM(down,10))
```

输入字段：`close`

## 原理说明

用过去一段时间的价格、成交量或换手率概括股票的交易行为。

## 来源

- 逻辑来源组：`广发多因子系列42-海量技术指标掘金Alpha因子-ebb746e4`
- 来源组指纹：`ebb746e4e36034e7bb654e15858c111028f0e23b67ecbaa72ca1d3677bba07bc`
- `JJJ643/量化因子挖掘思路475份/广发多因子系列42：海量技术指标掘金Alpha因子.pdf` — SHA-256 `ebb746e4e36034e7bb654e15858c111028f0e23b67ecbaa72ca1d3677bba07bc`
  - 归档副本：`../../sources/JJJ643/量化因子挖掘思路475份/广发多因子系列42：海量技术指标掘金Alpha因子.pdf`
- 来源页码：`未记录`

## 复现实现

- Python 实现：`microfactor.factors.document_extended:_compute/doc_cmo_10`
- 默认参数：`{}`
- 适配说明：无。

## 发布与评估

- Publication status: `published`
- Evaluation status: `rejected`
- 因子版本：`6092da1b6aa444fc38da`
- 数据快照：`snapshot_e3e73aa97706fd71f27ad486`
- 评估批次：`20260917_231028_ee6693d0`
- 有效区间：`2016-01-18` 至 `2026-09-15`

### 核心指标

- Rank IC Mean：`-0.0418464229737`
- Rank ICIR：`-0.341838364006`
- Adjusted ICIR：`-0.341838364006`
- Long-short spread (bps)：`-24.714953705`
- Monotonicity：`-0.551515151515`
- Coverage：`0.879537630259`
- Daily turnover (long)：`0.355647790308`
- Daily turnover (short)：`0.352948425014`
