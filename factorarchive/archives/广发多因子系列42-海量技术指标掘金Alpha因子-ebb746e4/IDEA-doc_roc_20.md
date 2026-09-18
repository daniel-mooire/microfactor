# doc_roc_20

## 因子概览

- 类别：`momentum`
- 方向：`negative`
- 频率：`1d`
- 最小窗口：`21`
- 复权方式：`hfq`
- 实现状态：`approximate`

## 公式

```text
100*(C/REF(C,20)-1)
```

输入字段：`close`

## 原理说明

通过价格和成交量的历史变化，概括趋势、波动或买卖力量。

## 来源

- 逻辑来源组：`广发多因子系列42-海量技术指标掘金Alpha因子-ebb746e4`
- 来源组指纹：`ebb746e4e36034e7bb654e15858c111028f0e23b67ecbaa72ca1d3677bba07bc`
- `JJJ643/量化因子挖掘思路475份/广发多因子系列42：海量技术指标掘金Alpha因子.pdf` — SHA-256 `ebb746e4e36034e7bb654e15858c111028f0e23b67ecbaa72ca1d3677bba07bc`
  - 归档副本：`../../sources/JJJ643/量化因子挖掘思路475份/广发多因子系列42：海量技术指标掘金Alpha因子.pdf`
- 来源页码：`99, 100`

## 复现实现

- Python 实现：`microfactor.factors.document_indicators::doc_roc_20`
- 默认参数：`{"N":20}`
- 适配说明：报告正文提到 12/25 日，但结果图同时给出 20/6 日；这里按对应图表固定 N=20，并以百分比形式输出。

## 发布与评估

- Publication status: `published`
- Evaluation status: `passed`
- 因子版本：`2b81724c9d82e12b6eac`
- 数据快照：`snapshot_e3e73aa97706fd71f27ad486`
- 评估批次：`20260917_231028_ee6693d0`
- 有效区间：`2016-02-01` 至 `2026-09-15`

### 核心指标

- Rank IC Mean：`-0.0550755934543`
- Rank ICIR：`-0.426492955943`
- Adjusted ICIR：`0.426492955943`
- Long-short spread (bps)：`33.6562675454`
- Monotonicity：`0.963636363636`
- Coverage：`0.938872917474`
- Daily turnover (long)：`0.279375342842`
- Daily turnover (short)：`0.25577352939`
