# doc_arc_50

## 因子概览

- 类别：`momentum`
- 方向：`positive`
- 频率：`1d`
- 最小窗口：`101`
- 复权方式：`hfq`
- 实现状态：`approximate`

## 公式

```text
SMA(REF(C/REF(C,50),1),50,1)
```

输入字段：`close`

## 原理说明

通过价格和成交量的历史变化，概括趋势、波动或买卖力量。

## 来源

- 逻辑来源组：`广发多因子系列42-海量技术指标掘金Alpha因子-ebb746e4`
- 来源组指纹：`ebb746e4e36034e7bb654e15858c111028f0e23b67ecbaa72ca1d3677bba07bc`
- `JJJ643/量化因子挖掘思路475份/广发多因子系列42：海量技术指标掘金Alpha因子.pdf` — SHA-256 `ebb746e4e36034e7bb654e15858c111028f0e23b67ecbaa72ca1d3677bba07bc`
  - 归档副本：`../../sources/JJJ643/量化因子挖掘思路475份/广发多因子系列42：海量技术指标掘金Alpha因子.pdf`
- 来源页码：`38`

## 复现实现

- Python 实现：`microfactor.factors.document_indicators::doc_arc_50`
- 默认参数：`{"M":50}`
- 适配说明：采用报告图示的 50 日参数；SMA(X,N,1) 按递归 alpha=1/N 实现，并严格要求完整预热窗口。

## 发布与评估

- Publication status: `published`
- Evaluation status: `rejected`
- 因子版本：`ed7b344597167ca73bee`
- 数据快照：`snapshot_e3e73aa97706fd71f27ad486`
- 评估批次：`20260917_231028_ee6693d0`
- 有效区间：`2016-06-01` 至 `2026-09-15`

### 核心指标

- Rank IC Mean：`-0.0203503346377`
- Rank ICIR：`-0.186669066621`
- Adjusted ICIR：`-0.186669066621`
- Long-short spread (bps)：`-7.48821323913`
- Monotonicity：`-0.951515151515`
- Coverage：`0.944831267493`
- Daily turnover (long)：`0.0680861765937`
- Daily turnover (short)：`0.0606762681329`
