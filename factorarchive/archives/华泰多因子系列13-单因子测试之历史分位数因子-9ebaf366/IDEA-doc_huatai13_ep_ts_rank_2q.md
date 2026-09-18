# doc_huatai13_ep_ts_rank_2q

## 因子概览

- 类别：`valuation`
- 方向：`positive`
- 频率：`1d`
- 最小窗口：`126`
- 复权方式：`none`
- 实现状态：`approximate`

## 公式

```text
ts_rank(EP, 2 quarters), EP=1/pe_ttm
```

输入字段：`pe_ttm`

## 原理说明

用过去一段时间的价格、成交量或换手率概括股票的交易行为。

## 来源

- 逻辑来源组：`华泰多因子系列13-单因子测试之历史分位数因子-9ebaf366`
- 来源组指纹：`9ebaf366e928205cb406d3dca6f92e685e97121d14f9d1ac1a3c99f54ddd1072`
- `JJJ643/量化因子挖掘思路475份/华泰多因子系列13：单因子测试之历史分位数因子.pdf` — SHA-256 `9ebaf366e928205cb406d3dca6f92e685e97121d14f9d1ac1a3c99f54ddd1072`
  - 归档副本：`../../sources/JJJ643/量化因子挖掘思路475份/华泰多因子系列13：单因子测试之历史分位数因子.pdf`
- 来源页码：`5, 7, 16, 19, 20`

## 复现实现

- Python 实现：`microfactor.factors.document_extended:_compute/doc_huatai13_ep_ts_rank_2q`
- 默认参数：`{"percentile":true,"quarters":2,"rank_method":"average","trading_days":126}`
- 适配说明：原报告以过去2个季度的每日EP计算当前时序分位并按月调仓；当前以126个交易日近似2个季度，输出每日滚动值。统一评估未复现报告中的行业、市值、反转和原始EP中性化。

## 发布与评估

- Publication status: `published`
- Evaluation status: `rejected`
- 因子版本：`6d0fa1f1c986bd6deba6`
- 数据快照：`snapshot_e3e73aa97706fd71f27ad486`
- 评估批次：`20260917_231028_ee6693d0`
- 有效区间：`2016-07-08` 至 `2026-09-15`

### 核心指标

- Rank IC Mean：`0.042580838598`
- Rank ICIR：`0.470359925469`
- Adjusted ICIR：`0.470359925469`
- Long-short spread (bps)：`20.3912896611`
- Monotonicity：`0.963636363636`
- Coverage：`0.429763327948`
- Daily turnover (long)：`0.270233845294`
- Daily turnover (short)：`0.255684337622`
