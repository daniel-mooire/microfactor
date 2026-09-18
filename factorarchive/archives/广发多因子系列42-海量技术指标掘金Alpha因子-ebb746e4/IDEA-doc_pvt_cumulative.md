# doc_pvt_cumulative

## 因子概览

- 类别：`price_volume`
- 方向：`negative`
- 频率：`1d`
- 最小窗口：`2`
- 复权方式：`hfq`
- 实现状态：`approximate`

## 公式

```text
SUM((C-REF(C,1))/REF(C,1)*V,0)
```

输入字段：`close, volume`

## 原理说明

通过价格和成交量的历史变化，概括趋势、波动或买卖力量。

## 来源

- 逻辑来源组：`广发多因子系列42-海量技术指标掘金Alpha因子-ebb746e4`
- 来源组指纹：`ebb746e4e36034e7bb654e15858c111028f0e23b67ecbaa72ca1d3677bba07bc`
- `JJJ643/量化因子挖掘思路475份/广发多因子系列42：海量技术指标掘金Alpha因子.pdf` — SHA-256 `ebb746e4e36034e7bb654e15858c111028f0e23b67ecbaa72ca1d3677bba07bc`
  - 归档副本：`../../sources/JJJ643/量化因子挖掘思路475份/广发多因子系列42：海量技术指标掘金Alpha因子.pdf`
- 来源页码：`91, 92, 93`

## 复现实现

- Python 实现：`microfactor.factors.document_indicators::doc_pvt_cumulative`
- 默认参数：`{"initial_value":0.0,"window":0}`
- 适配说明：采用报告 SUM(...,0) 的累计 PVT；首个有效观测初始化为 0，不与已有固定窗口 PVT 条目合并。

## 发布与评估

- Publication status: `published`
- Evaluation status: `rejected`
- 因子版本：`d790d54a3f2e4b4e8eda`
- 数据快照：`snapshot_e3e73aa97706fd71f27ad486`
- 评估批次：`20260917_231028_ee6693d0`
- 有效区间：`2016-01-04` 至 `2026-09-15`

### 核心指标

- Rank IC Mean：`-0.0147960287569`
- Rank ICIR：`-0.158592719923`
- Adjusted ICIR：`0.158592719923`
- Long-short spread (bps)：`3.87975002569`
- Monotonicity：`0.830303030303`
- Coverage：`0.998898500577`
- Daily turnover (long)：`0.0542072833541`
- Daily turnover (short)：`0.047555622934`
