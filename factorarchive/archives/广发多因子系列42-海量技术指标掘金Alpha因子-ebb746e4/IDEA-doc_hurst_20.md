# doc_hurst_20

## 因子概览

- 类别：`technical`
- 方向：`unspecified`
- 频率：`1d`
- 最小窗口：`20`
- 复权方式：`hfq`
- 实现状态：`approximate`

## 公式

```text
(max(cumsum(C-mean(C)))-min(cumsum(C-mean(C))))/STD(C)
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

- Python 实现：`microfactor.factors.document_extended:_compute/doc_hurst_20`
- 默认参数：`{}`
- 适配说明：窗口固定为报告示例的 20 日，Hurst 这里保留原始 R/S 比值，不做 log-log 拟合。

## 发布与评估

- Publication status: `published`
- Evaluation status: `rejected`
- 因子版本：`209d0ba2c1e453f76e05`
- 数据快照：`snapshot_e3e73aa97706fd71f27ad486`
- 评估批次：`20260917_231028_ee6693d0`
- 有效区间：`2016-01-29` 至 `2026-09-15`

### 核心指标

- Rank IC Mean：`0.0107775816779`
- Rank ICIR：`0.137340582396`
- Adjusted ICIR：`0.137340582396`
- Long-short spread (bps)：`5.88814771941`
- Monotonicity：`0.842424242424`
- Coverage：`0.843429899303`
- Daily turnover (long)：`0.242838598296`
- Daily turnover (short)：`0.271607450436`
