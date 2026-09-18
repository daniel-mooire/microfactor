# doc_roc_25

## 因子概览

- 类别：`momentum`
- 方向：`unspecified`
- 频率：`1d`
- 最小窗口：`25`
- 复权方式：`hfq`
- 实现状态：`exact`

## 公式

```text
(C-Ref(C,25))/Ref(C,25)
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

- Python 实现：`microfactor.factors.document_extended:_compute/doc_roc_25`
- 默认参数：`{}`
- 适配说明：无。

## 发布与评估

- Publication status: `published`
- Evaluation status: `rejected`
- 因子版本：`2773c0b1f962e438b17b`
- 数据快照：`snapshot_e3e73aa97706fd71f27ad486`
- 评估批次：`20260917_231028_ee6693d0`
- 有效区间：`2016-02-15` 至 `2026-09-15`

### 核心指标

- Rank IC Mean：`-0.0543692134687`
- Rank ICIR：`-0.417957055347`
- Adjusted ICIR：`-0.417957055347`
- Long-short spread (bps)：`-33.0971426224`
- Monotonicity：`-0.939393939394`
- Coverage：`0.900780279503`
- Daily turnover (long)：`0.233217897832`
- Daily turnover (short)：`0.25537404879`
