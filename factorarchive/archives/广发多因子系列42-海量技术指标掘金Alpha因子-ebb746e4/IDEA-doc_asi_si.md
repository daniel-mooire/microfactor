# doc_asi_si

## 因子概览

- 类别：`trend`
- 方向：`negative`
- 频率：`1d`
- 最小窗口：`2`
- 复权方式：`hfq`
- 实现状态：`approximate`

## 公式

```text
SI=16*X*MAX(AA,BB)/R
```

输入字段：`open, high, low, close`

## 原理说明

通过价格和成交量的历史变化，概括趋势、波动或买卖力量。

## 来源

- 逻辑来源组：`广发多因子系列42-海量技术指标掘金Alpha因子-ebb746e4`
- 来源组指纹：`ebb746e4e36034e7bb654e15858c111028f0e23b67ecbaa72ca1d3677bba07bc`
- `JJJ643/量化因子挖掘思路475份/广发多因子系列42：海量技术指标掘金Alpha因子.pdf` — SHA-256 `ebb746e4e36034e7bb654e15858c111028f0e23b67ecbaa72ca1d3677bba07bc`
  - 归档副本：`../../sources/JJJ643/量化因子挖掘思路475份/广发多因子系列42：海量技术指标掘金Alpha因子.pdf`
- 来源页码：`108`

## 复现实现

- Python 实现：`microfactor.factors.document_indicators::doc_asi_si`
- 默认参数：`{"component":"SI"}`
- 适配说明：报告图表命名为 ASI(SI)；此条目公开单日 SI 分量，不把累计 ASI（SUM(SI,0)）误作为同一个输出。

## 发布与评估

- Publication status: `published`
- Evaluation status: `passed`
- 因子版本：`30ef517f769d0befe9fe`
- 数据快照：`snapshot_e3e73aa97706fd71f27ad486`
- 评估批次：`20260917_231028_ee6693d0`
- 有效区间：`2016-01-05` 至 `2026-09-15`

### 核心指标

- Rank IC Mean：`-0.0381293061656`
- Rank ICIR：`-0.356500757913`
- Adjusted ICIR：`0.356500757913`
- Long-short spread (bps)：`23.7638881081`
- Monotonicity：`0.587878787879`
- Coverage：`0.975157692308`
- Daily turnover (long)：`0.652565426677`
- Daily turnover (short)：`0.693800924035`
