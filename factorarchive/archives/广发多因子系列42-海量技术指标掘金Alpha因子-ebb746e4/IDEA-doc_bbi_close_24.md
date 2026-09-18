# doc_bbi_close_24

## 因子概览

- 类别：`trend`
- 方向：`positive`
- 频率：`1d`
- 最小窗口：`24`
- 复权方式：`hfq`
- 实现状态：`approximate`

## 公式

```text
((MA(C,3)+MA(C,6)+MA(C,12)+MA(C,24))/4)/C
```

输入字段：`close`

## 原理说明

通过价格和成交量的历史变化，概括趋势、波动或买卖力量。

## 来源

- 逻辑来源组：`广发多因子系列42-海量技术指标掘金Alpha因子-ebb746e4`
- 来源组指纹：`ebb746e4e36034e7bb654e15858c111028f0e23b67ecbaa72ca1d3677bba07bc`
- `JJJ643/量化因子挖掘思路475份/广发多因子系列42：海量技术指标掘金Alpha因子.pdf` — SHA-256 `ebb746e4e36034e7bb654e15858c111028f0e23b67ecbaa72ca1d3677bba07bc`
  - 归档副本：`../../sources/JJJ643/量化因子挖掘思路475份/广发多因子系列42：海量技术指标掘金Alpha因子.pdf`
- 来源页码：`46`

## 复现实现

- Python 实现：`microfactor.factors.document_indicators::doc_bbi_close_24`
- 默认参数：`{"M1":3,"M2":6,"M3":12,"M4":24}`
- 适配说明：报告正文定义 BBI，图表另列 BBI_Close；这里明确采用 BBI/收盘价，并以 3/6/12/24 日等权均线复现图表因子。

## 发布与评估

- Publication status: `published`
- Evaluation status: `passed`
- 因子版本：`f526c938ee769449e5eb`
- 数据快照：`snapshot_e3e73aa97706fd71f27ad486`
- 评估批次：`20260917_231028_ee6693d0`
- 有效区间：`2016-02-04` 至 `2026-09-15`

### 核心指标

- Rank IC Mean：`0.0591636981566`
- Rank ICIR：`0.420582090977`
- Adjusted ICIR：`0.420582090977`
- Long-short spread (bps)：`36.065171985`
- Monotonicity：`0.963636363636`
- Coverage：`0.829921644686`
- Daily turnover (long)：`0.359159080481`
- Daily turnover (short)：`0.42343849577`
