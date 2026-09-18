# doc_guangfa3_momentum_accel_21d

## 因子概览

- 类别：`momentum`
- 方向：`positive`
- 频率：`1d`
- 最小窗口：`273`
- 复权方式：`qfq`
- 实现状态：`approximate`

## 公式

```text
abs(price_trend_tstat_252d[t] - price_trend_tstat_252d[t-21])
```

输入字段：`adjusted_close`

## 原理说明

用过去一段时间的价格、成交量或换手率概括股票的交易行为。

## 来源

- 逻辑来源组：`广发多因子系列3-估值与动量结合的选股模型-ef6222b7`
- 来源组指纹：`ef6222b786240a355dfacabffb1639a91d2f987f8c50f92af8ce7d2b56cabc3b`
- `JJJ643/量化因子挖掘思路475份/广发多因子系列3：估值与动量结合的选股模型.pdf` — SHA-256 `ef6222b786240a355dfacabffb1639a91d2f987f8c50f92af8ce7d2b56cabc3b`
  - 归档副本：`../../sources/JJJ643/量化因子挖掘思路475份/广发多因子系列3：估值与动量结合的选股模型.pdf`
- 来源页码：`8, 9`

## 复现实现

- Python 实现：`microfactor.factors.document_extended:_compute/doc_guangfa3_momentum_accel_21d`
- 默认参数：`{"comparison_lag":21,"difference":"absolute","trend_window":252}`
- 适配说明：原报告按月比较当月与上月的一年趋势线t值；当前以21个交易日近似一个月，并输出每日滚动值供统一评估。

## 发布与评估

- Publication status: `published`
- Evaluation status: `rejected`
- 因子版本：`53f32e9ba385bd00fb88`
- 数据快照：`snapshot_e3e73aa97706fd71f27ad486`
- 评估批次：`20260917_231028_ee6693d0`
- 有效区间：`2017-02-17` 至 `2026-09-15`

### 核心指标

- Rank IC Mean：`-0.00411965875874`
- Rank ICIR：`-0.0535775511517`
- Adjusted ICIR：`-0.0535775511517`
- Long-short spread (bps)：`-3.57758491363`
- Monotonicity：`-0.6`
- Coverage：`0.463969944182`
- Daily turnover (long)：`0.0580178388934`
- Daily turnover (short)：`0.143122120705`
