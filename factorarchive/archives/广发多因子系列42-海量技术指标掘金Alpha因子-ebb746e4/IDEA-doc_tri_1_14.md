# doc_tri_1_14

## 因子概览

- 类别：`volatility`
- 方向：`negative`
- 频率：`1d`
- 最小窗口：`28`
- 复权方式：`hfq`
- 实现状态：`approximate`

## 公式

```text
X1=IF(C>REF(C,1),1/(C-REF(C,1)),1); X2=X1-MIN(X1); TRI=EMA(X2/(H-L)*100,14)
```

输入字段：`high, low, close`

## 原理说明

通过价格和成交量的历史变化，概括趋势、波动或买卖力量。

## 来源

- 逻辑来源组：`广发多因子系列42-海量技术指标掘金Alpha因子-ebb746e4`
- 来源组指纹：`ebb746e4e36034e7bb654e15858c111028f0e23b67ecbaa72ca1d3677bba07bc`
- `JJJ643/量化因子挖掘思路475份/广发多因子系列42：海量技术指标掘金Alpha因子.pdf` — SHA-256 `ebb746e4e36034e7bb654e15858c111028f0e23b67ecbaa72ca1d3677bba07bc`
  - 归档副本：`../../sources/JJJ643/量化因子挖掘思路475份/广发多因子系列42：海量技术指标掘金Alpha因子.pdf`
- 来源页码：`112`

## 复现实现

- Python 实现：`microfactor.factors.document_indicators::doc_tri_1_14`
- 默认参数：`{"N":14,"T":1}`
- 适配说明：原文未限定 MIN(X1) 的回看范围；为保持因果性采用 N=14 的滚动最小值，并固定 T=1。

## 发布与评估

- Publication status: `published`
- Evaluation status: `rejected`
- 因子版本：`73e86624fef7746c38da`
- 数据快照：`snapshot_e3e73aa97706fd71f27ad486`
- 评估批次：`20260917_231028_ee6693d0`
- 有效区间：`2016-02-17` 至 `2026-09-15`

### 核心指标

- Rank IC Mean：`0.0258704681126`
- Rank ICIR：`0.370190838817`
- Adjusted ICIR：`-0.370190838817`
- Long-short spread (bps)：`-7.2361746348`
- Monotonicity：`-0.987878787879`
- Coverage：`0.975512820513`
- Daily turnover (long)：`0.146514052241`
- Daily turnover (short)：`0.116682615802`
