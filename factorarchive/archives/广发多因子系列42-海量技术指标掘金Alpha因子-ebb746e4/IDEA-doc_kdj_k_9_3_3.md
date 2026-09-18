# doc_kdj_k_9_3_3

## 因子概览

- 类别：`technical`
- 方向：`positive`
- 频率：`1d`
- 最小窗口：`9`
- 复权方式：`hfq`
- 实现状态：`approximate`

## 公式

```text
SMA3(RSV,1), RSV=100*(C-LLV9)/(HHV9-LLV9)
```

输入字段：`high, low, close`

## 原理说明

通过价格和成交量的历史变化，概括趋势、波动或买卖力量。

## 来源

- 逻辑来源组：`广发多因子系列42-海量技术指标掘金Alpha因子-ebb746e4`
- 来源组指纹：`ebb746e4e36034e7bb654e15858c111028f0e23b67ecbaa72ca1d3677bba07bc`
- `JJJ643/量化因子挖掘思路475份/广发多因子系列42：海量技术指标掘金Alpha因子.pdf` — SHA-256 `ebb746e4e36034e7bb654e15858c111028f0e23b67ecbaa72ca1d3677bba07bc`
  - 归档副本：`../../sources/JJJ643/量化因子挖掘思路475份/广发多因子系列42：海量技术指标掘金Alpha因子.pdf`
- 来源页码：`未记录`

## 复现实现

- Python 实现：`microfactor.factors.document_indicators::doc_kdj_k_9_3_3`
- 默认参数：`{}`
- 适配说明：以递归平滑近似平台 SMA(X,3,1)，参数固定为 9/3/3。

## 发布与评估

- Publication status: `published`
- Evaluation status: `rejected`
- 因子版本：`5f64c9b20608e68596dc`
- 数据快照：`snapshot_e3e73aa97706fd71f27ad486`
- 评估批次：`20260917_231028_ee6693d0`
- 有效区间：`2016-01-26` 至 `2026-09-15`

### 核心指标

- Rank IC Mean：`-0.0294349955598`
- Rank ICIR：`-0.277165442601`
- Adjusted ICIR：`-0.277165442601`
- Long-short spread (bps)：`-18.2249381267`
- Monotonicity：`-0.551515151515`
- Coverage：`0.98445377176`
- Daily turnover (long)：`0.301597077231`
- Daily turnover (short)：`0.257681551089`
