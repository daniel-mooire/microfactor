# doc_dbcd_5_3_3

## 因子概览

- 类别：`reversal`
- 方向：`negative`
- 频率：`1d`
- 最小窗口：`10`
- 复权方式：`hfq`
- 实现状态：`approximate`

## 公式

```text
BIAS=(C-MA(C,5))/MA(C,5); DIF=BIAS-REF(BIAS,3); DBCD=SMA(DIF,3,1)
```

输入字段：`close`

## 原理说明

通过价格和成交量的历史变化，概括趋势、波动或买卖力量。

## 来源

- 逻辑来源组：`广发多因子系列42-海量技术指标掘金Alpha因子-ebb746e4`
- 来源组指纹：`ebb746e4e36034e7bb654e15858c111028f0e23b67ecbaa72ca1d3677bba07bc`
- `JJJ643/量化因子挖掘思路475份/广发多因子系列42：海量技术指标掘金Alpha因子.pdf` — SHA-256 `ebb746e4e36034e7bb654e15858c111028f0e23b67ecbaa72ca1d3677bba07bc`
  - 归档副本：`../../sources/JJJ643/量化因子挖掘思路475份/广发多因子系列42：海量技术指标掘金Alpha因子.pdf`
- 来源页码：`64`

## 复现实现

- Python 实现：`microfactor.factors.document_indicators::doc_dbcd_5_3_3`
- 默认参数：`{"N":3,"P":5,"W":3}`
- 适配说明：原文给出 P、N、W 符号但未给测算参数；按图表复现约定采用 5/3/3，SMA(X,3,1) 使用递归平滑。

## 发布与评估

- Publication status: `published`
- Evaluation status: `rejected`
- 因子版本：`26eae6941203f6c5d3d3`
- 数据快照：`snapshot_e3e73aa97706fd71f27ad486`
- 评估批次：`20260917_231028_ee6693d0`
- 有效区间：`2016-01-15` 至 `2026-09-15`

### 核心指标

- Rank IC Mean：`-0.0270680868637`
- Rank ICIR：`-0.284794944229`
- Adjusted ICIR：`0.284794944229`
- Long-short spread (bps)：`19.0711267886`
- Monotonicity：`0.442424242424`
- Coverage：`0.989758101852`
- Daily turnover (long)：`0.389795420839`
- Daily turnover (short)：`0.398356883151`
