# doc_jq2025_gp_inverse_high_delta_sq_2d

## 因子概览

- 类别：`volatility`
- 方向：`unspecified`
- 频率：`1d`
- 最小窗口：`2`
- 复权方式：`qfq`
- 实现状态：`approximate`

## 公式

```text
square(delta(12 / adjusted_high, 1))
```

输入字段：`high`

## 原理说明

用过去一段时间的价格、成交量或换手率概括股票的交易行为。

## 来源

- 逻辑来源组：`40.基于遗传算法挖掘因子2-77c87a1f`
- 来源组指纹：`77c87a1fb7c854fbb2e6acc9b0a6caa1ab72212990382d05a83d1ca823d128a0`
- `2020-2026聚宽600条源码/2025年度精选策略/40.基于遗传算法挖掘因子2.txt` — SHA-256 `77c87a1fb7c854fbb2e6acc9b0a6caa1ab72212990382d05a83d1ca823d128a0`
  - 归档副本：`../../sources/2020-2026聚宽600条源码/2025年度精选策略/40.基于遗传算法挖掘因子2.txt`
- 来源页码：`未记录`

## 复现实现

- Python 实现：`microfactor.factors.document_extended:_compute/doc_jq2025_gp_inverse_high_delta_sq_2d`
- 默认参数：`{"constant":12.0,"difference_axis":"time","difference_lag":1,"power":2,"source_analysis_periods":[5,10],"source_evaluation_lookback":500,"source_index":"000906.XSHG"}`
- 适配说明：The notebook explicitly evaluates the squared time-axis difference of 12/high on CSI 800 stocks, but does not preserve the genetic-program output that links this hand-written expression to a selected best program. Its get_price adjustment is also not pinned. The implementation retains the literal scale and formula, uses qfq high, and exposes the daily signal under the common one-day evaluation contract rather than the source's 5/10-day analysis horizons.

## 发布与评估

- Publication status: `published`
- Evaluation status: `rejected`
- 因子版本：`76cd4e6cffef1d9b4752`
- 数据快照：`snapshot_e3e73aa97706fd71f27ad486`
- 评估批次：`20260917_231028_ee6693d0`
- 有效区间：`2016-01-05` 至 `2026-09-15`

### 核心指标

- Rank IC Mean：`-0.0280581184298`
- Rank ICIR：`-0.306283418612`
- Adjusted ICIR：`-0.306283418612`
- Long-short spread (bps)：`-9.03671667012`
- Monotonicity：`-0.163636363636`
- Coverage：`0.975142307692`
- Daily turnover (long)：`0.650469651273`
- Daily turnover (short)：`0.844084052252`
