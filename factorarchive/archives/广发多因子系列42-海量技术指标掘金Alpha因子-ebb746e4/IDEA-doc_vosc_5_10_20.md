# doc_vosc_5_10_20

## 因子概览

- 类别：`price_volume`
- 方向：`positive`
- 频率：`1d`
- 最小窗口：`20`
- 复权方式：`hfq`
- 实现状态：`approximate`

## 公式

```text
100*(MA5(V)-MA10(V))/MA20(V)
```

输入字段：`volume`

## 原理说明

通过价格和成交量的历史变化，概括趋势、波动或买卖力量。

## 来源

- 逻辑来源组：`广发多因子系列42-海量技术指标掘金Alpha因子-ebb746e4`
- 来源组指纹：`ebb746e4e36034e7bb654e15858c111028f0e23b67ecbaa72ca1d3677bba07bc`
- `JJJ643/量化因子挖掘思路475份/广发多因子系列42：海量技术指标掘金Alpha因子.pdf` — SHA-256 `ebb746e4e36034e7bb654e15858c111028f0e23b67ecbaa72ca1d3677bba07bc`
  - 归档副本：`../../sources/JJJ643/量化因子挖掘思路475份/广发多因子系列42：海量技术指标掘金Alpha因子.pdf`
- 来源页码：`未记录`

## 复现实现

- Python 实现：`microfactor.factors.document_indicators::doc_vosc_5_10_20`
- 默认参数：`{}`
- 适配说明：报告仅给出 M/P/S 符号，采用短/中/长 5/10/20 并写入名称。

## 发布与评估

- Publication status: `published`
- Evaluation status: `rejected`
- 因子版本：`453127c7e59e039abf3e`
- 数据快照：`snapshot_e3e73aa97706fd71f27ad486`
- 评估批次：`20260917_231028_ee6693d0`
- 有效区间：`2016-01-29` 至 `2026-09-15`

### 核心指标

- Rank IC Mean：`-0.0316298186784`
- Rank ICIR：`-0.389791842864`
- Adjusted ICIR：`-0.389791842864`
- Long-short spread (bps)：`-15.3878042276`
- Monotonicity：`-0.321212121212`
- Coverage：`0.843429899303`
- Daily turnover (long)：`0.275138153088`
- Daily turnover (short)：`0.316455816562`
