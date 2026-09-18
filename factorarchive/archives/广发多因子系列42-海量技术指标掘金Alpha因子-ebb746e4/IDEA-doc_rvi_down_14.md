# doc_rvi_down_14

## 因子概览

- 类别：`volatility`
- 方向：`positive`
- 频率：`1d`
- 最小窗口：`27`
- 复权方式：`hfq`
- 实现状态：`approximate`

## 公式

```text
ADOWN=SMA(IF(C<=REF(C,1),STD(C,14),0),14,1)
```

输入字段：`close`

## 原理说明

通过价格和成交量的历史变化，概括趋势、波动或买卖力量。

## 来源

- 逻辑来源组：`广发多因子系列42-海量技术指标掘金Alpha因子-ebb746e4`
- 来源组指纹：`ebb746e4e36034e7bb654e15858c111028f0e23b67ecbaa72ca1d3677bba07bc`
- `JJJ643/量化因子挖掘思路475份/广发多因子系列42：海量技术指标掘金Alpha因子.pdf` — SHA-256 `ebb746e4e36034e7bb654e15858c111028f0e23b67ecbaa72ca1d3677bba07bc`
  - 归档副本：`../../sources/JJJ643/量化因子挖掘思路475份/广发多因子系列42：海量技术指标掘金Alpha因子.pdf`
- 来源页码：`104, 105, 106`

## 复现实现

- Python 实现：`microfactor.factors.document_indicators::doc_rvi_down_14`
- 默认参数：`{"N":14}`
- 适配说明：结果图未重复列出 N；采用常见 N=14，并按报告的递归 SMA(X,N,1) 及样本标准差实现。

## 发布与评估

- Publication status: `published`
- Evaluation status: `rejected`
- 因子版本：`a4632df48a58f0d61669`
- 数据快照：`snapshot_e3e73aa97706fd71f27ad486`
- 评估批次：`20260917_231028_ee6693d0`
- 有效区间：`2016-02-16` 至 `2026-09-15`

### 核心指标

- Rank IC Mean：`-0.0178424211811`
- Rank ICIR：`-0.213968077506`
- Adjusted ICIR：`-0.213968077506`
- Long-short spread (bps)：`-4.139382571`
- Monotonicity：`-0.878787878788`
- Coverage：`0.976442330097`
- Daily turnover (long)：`0.101416914115`
- Daily turnover (short)：`0.101060316479`
