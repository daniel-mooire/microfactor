# doc_price_slope_6

## 因子概览

- 类别：`trend`
- 方向：`negative`
- 频率：`1d`
- 最小窗口：`6`
- 复权方式：`hfq`
- 实现状态：`exact`

## 公式

```text
OLS_slope(C[t-5:t],1..6)
```

输入字段：`close`

## 原理说明

通过价格和成交量的历史变化，概括趋势、波动或买卖力量。

## 来源

- 逻辑来源组：`广发多因子系列42-海量技术指标掘金Alpha因子-ebb746e4`
- 来源组指纹：`ebb746e4e36034e7bb654e15858c111028f0e23b67ecbaa72ca1d3677bba07bc`
- `JJJ643/量化因子挖掘思路475份/广发多因子系列42：海量技术指标掘金Alpha因子.pdf` — SHA-256 `ebb746e4e36034e7bb654e15858c111028f0e23b67ecbaa72ca1d3677bba07bc`
  - 归档副本：`../../sources/JJJ643/量化因子挖掘思路475份/广发多因子系列42：海量技术指标掘金Alpha因子.pdf`
- 来源页码：`60, 61`

## 复现实现

- Python 实现：`microfactor.factors.document_indicators::doc_price_slope_6`
- 默认参数：`{"N":6}`
- 适配说明：无。

## 发布与评估

- Publication status: `published`
- Evaluation status: `passed`
- 因子版本：`3b404cb1c11b92c9543a`
- 数据快照：`snapshot_e3e73aa97706fd71f27ad486`
- 评估批次：`20260917_231028_ee6693d0`
- 有效区间：`2016-01-11` 至 `2026-09-15`

### 核心指标

- Rank IC Mean：`-0.0410127892006`
- Rank ICIR：`-0.363443679313`
- Adjusted ICIR：`0.363443679313`
- Long-short spread (bps)：`26.5955068477`
- Monotonicity：`0.587878787879`
- Coverage：`0.909828197227`
- Daily turnover (long)：`0.337295628595`
- Daily turnover (short)：`0.322073779539`
