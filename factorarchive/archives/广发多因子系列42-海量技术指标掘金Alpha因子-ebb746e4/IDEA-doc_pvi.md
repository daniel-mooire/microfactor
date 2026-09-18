# doc_pvi

## 因子概览

- 类别：`momentum`
- 方向：`unspecified`
- 频率：`1d`
- 最小窗口：`1`
- 复权方式：`hfq`
- 实现状态：`approximate`

## 公式

```text
PVI_t=IF(C_t>C_{t-1},C_t/C_{t-1}*PVI_{t-1},PVI_{t-1}); PVI_0=1000
```

输入字段：`close`

## 原理说明

通过价格和成交量的历史变化，概括趋势、波动或买卖力量。

## 来源

- 逻辑来源组：`广发多因子系列42-海量技术指标掘金Alpha因子-ebb746e4`
- 来源组指纹：`ebb746e4e36034e7bb654e15858c111028f0e23b67ecbaa72ca1d3677bba07bc`
- `JJJ643/量化因子挖掘思路475份/广发多因子系列42：海量技术指标掘金Alpha因子.pdf` — SHA-256 `ebb746e4e36034e7bb654e15858c111028f0e23b67ecbaa72ca1d3677bba07bc`
  - 归档副本：`../../sources/JJJ643/量化因子挖掘思路475份/广发多因子系列42：海量技术指标掘金Alpha因子.pdf`
- 来源页码：`20`

## 复现实现

- Python 实现：`microfactor.factors.document_indicators::doc_pvi`
- 默认参数：`{"initial_value":1000.0}`
- 适配说明：按 PDF 打印的收盘价上涨条件递推；原文未提供成交量门槛或初值，因此固定 PVI_0=1000，并在元数据中保留该适配。

## 发布与评估

- Publication status: `published`
- Evaluation status: `rejected`
- 因子版本：`f0307e97997c486d6329`
- 数据快照：`snapshot_e3e73aa97706fd71f27ad486`
- 评估批次：`20260917_231028_ee6693d0`
- 有效区间：`2016-01-04` 至 `2026-09-15`

### 核心指标

- Rank IC Mean：`-0.00793571681281`
- Rank ICIR：`-0.0999098904282`
- Adjusted ICIR：`-0.0999098904282`
- Long-short spread (bps)：`-1.53234344837`
- Monotonicity：`-0.151515151515`
- Coverage：`0.998898500577`
- Daily turnover (long)：`0.0303788312477`
- Daily turnover (short)：`0.0770334461794`
