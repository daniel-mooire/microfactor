# doc_micd_12_3_6

## 因子概览

- 类别：`momentum`
- 方向：`unspecified`
- 频率：`1d`
- 最小窗口：`28`
- 复权方式：`hfq`
- 实现状态：`approximate`

## 公式

```text
MTM=C-REF(C,1); MTMMA=SMA(MTM,12,1); DIF=MA(REF(MTMMA,1),3)-MA(REF(MTMMA,1),6); MICD=SMA(DIF,10,1)
```

输入字段：`close`

## 原理说明

通过价格和成交量的历史变化，概括趋势、波动或买卖力量。

## 来源

- 逻辑来源组：`广发多因子系列42-海量技术指标掘金Alpha因子-ebb746e4`
- 来源组指纹：`ebb746e4e36034e7bb654e15858c111028f0e23b67ecbaa72ca1d3677bba07bc`
- `JJJ643/量化因子挖掘思路475份/广发多因子系列42：海量技术指标掘金Alpha因子.pdf` — SHA-256 `ebb746e4e36034e7bb654e15858c111028f0e23b67ecbaa72ca1d3677bba07bc`
  - 归档副本：`../../sources/JJJ643/量化因子挖掘思路475份/广发多因子系列42：海量技术指标掘金Alpha因子.pdf`
- 来源页码：`82`

## 复现实现

- Python 实现：`microfactor.factors.document_indicators::doc_micd_12_3_6`
- 默认参数：`{"N":12,"N1":3,"N2":6,"signal_window":10}`
- 适配说明：原文公式将 MTM 误排为 MI 且未列 N/N1/N2 默认值；按 MTM 语义采用 12/3/6，并保留末级 10 日 SMA。

## 发布与评估

- Publication status: `published`
- Evaluation status: `rejected`
- 因子版本：`69f81f560f60790b56cb`
- 数据快照：`snapshot_e3e73aa97706fd71f27ad486`
- 评估批次：`20260917_231028_ee6693d0`
- 有效区间：`2016-02-17` 至 `2026-09-15`

### 核心指标

- Rank IC Mean：`-0.0212439852021`
- Rank ICIR：`-0.236789493533`
- Adjusted ICIR：`-0.236789493533`
- Long-short spread (bps)：`-10.0470839514`
- Monotonicity：`-0.393939393939`
- Coverage：`0.987047008547`
- Daily turnover (long)：`0.217912119887`
- Daily turnover (short)：`0.162518720074`
