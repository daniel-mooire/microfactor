# doc_rccd_12_3_6

## 因子概览

- 类别：`momentum`
- 方向：`unspecified`
- 频率：`1d`
- 最小窗口：`42`
- 复权方式：`hfq`
- 实现状态：`approximate`

## 公式

```text
RC=C/REF(C,12); ARC1=SMA(REF(RC,1),12,1); DIF=MA(REF(ARC1,1),3)-MA(REF(ARC1,1),6); RCCD=SMA(DIF,12,1)
```

输入字段：`close`

## 原理说明

通过价格和成交量的历史变化，概括趋势、波动或买卖力量。

## 来源

- 逻辑来源组：`广发多因子系列42-海量技术指标掘金Alpha因子-ebb746e4`
- 来源组指纹：`ebb746e4e36034e7bb654e15858c111028f0e23b67ecbaa72ca1d3677bba07bc`
- `JJJ643/量化因子挖掘思路475份/广发多因子系列42：海量技术指标掘金Alpha因子.pdf` — SHA-256 `ebb746e4e36034e7bb654e15858c111028f0e23b67ecbaa72ca1d3677bba07bc`
  - 归档副本：`../../sources/JJJ643/量化因子挖掘思路475份/广发多因子系列42：海量技术指标掘金Alpha因子.pdf`
- 来源页码：`94`

## 复现实现

- Python 实现：`microfactor.factors.document_indicators::doc_rccd_12_3_6`
- 默认参数：`{"m":12,"p1":3,"p2":6}`
- 适配说明：原文只给出 m、p1、p2 符号；采用 12/3/6，并按报告 SMA(X,N,1) 递归定义计算。

## 发布与评估

- Publication status: `published`
- Evaluation status: `rejected`
- 因子版本：`e03ad90f534705ee1e1d`
- 数据快照：`snapshot_e3e73aa97706fd71f27ad486`
- 评估批次：`20260917_231028_ee6693d0`
- 有效区间：`2016-03-08` 至 `2026-09-15`

### 核心指标

- Rank IC Mean：`-0.0196956982145`
- Rank ICIR：`-0.204398443778`
- Adjusted ICIR：`-0.204398443778`
- Long-short spread (bps)：`-9.78627375006`
- Monotonicity：`-0.406060606061`
- Coverage：`0.979120703125`
- Daily turnover (long)：`0.133493761811`
- Daily turnover (short)：`0.111722922467`
