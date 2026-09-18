# doc_kdj_d_9_3_3

## 因子概览

- 类别：`technical`
- 方向：`positive`
- 频率：`1d`
- 最小窗口：`9`
- 复权方式：`hfq`
- 实现状态：`approximate`

## 公式

```text
SMA3(K,1)
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

- Python 实现：`microfactor.factors.document_indicators::doc_kdj_d_9_3_3`
- 默认参数：`{}`
- 适配说明：以递归平滑近似平台 SMA(X,3,1)，参数固定为 9/3/3。

## 发布与评估

- Publication status: `published`
- Evaluation status: `rejected`
- 因子版本：`cc67191d0c663e1ba835`
- 数据快照：`snapshot_e3e73aa97706fd71f27ad486`
- 评估批次：`20260917_231028_ee6693d0`
- 有效区间：`2016-02-05` 至 `2026-09-15`

### 核心指标

- Rank IC Mean：`-0.0236163730917`
- Rank ICIR：`-0.234714035548`
- Adjusted ICIR：`-0.234714035548`
- Long-short spread (bps)：`-12.6808852223`
- Monotonicity：`-0.551515151515`
- Coverage：`0.980918121847`
- Daily turnover (long)：`0.221044304968`
- Daily turnover (short)：`0.19330843176`
