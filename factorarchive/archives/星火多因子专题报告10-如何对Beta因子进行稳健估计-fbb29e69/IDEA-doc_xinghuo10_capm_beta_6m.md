# doc_xinghuo10_capm_beta_6m

## 因子概览

- 类别：`beta`
- 方向：`unspecified`
- 频率：`1d`
- 最小窗口：`126`
- 复权方式：`none`
- 实现状态：`approximate`

## 公式

```text
beta from equal-weight OLS: stock_return ~ 1 + market_return
```

输入字段：`close_to_close_total_return_1d, circ_mv, is_suspended`

## 原理说明

用过去一段时间的价格、成交量或换手率概括股票的交易行为。

## 来源

- 逻辑来源组：`星火多因子专题报告10-如何对Beta因子进行稳健估计-fbb29e69`
- 来源组指纹：`fbb29e6962ff6a40a588beca87626866b36177d11dd7e9b0a8511d5bded3e36d`
- `JJJ643/量化因子挖掘思路475份/星火多因子专题报告10：如何对Beta因子进行稳健估计？.pdf` — SHA-256 `fbb29e6962ff6a40a588beca87626866b36177d11dd7e9b0a8511d5bded3e36d`
  - 归档副本：`../../sources/JJJ643/量化因子挖掘思路475份/星火多因子专题报告10：如何对Beta因子进行稳健估计？.pdf`
- 来源页码：`1, 5, 6, 10, 11, 12, 13`

## 复现实现

- Python 实现：`microfactor.factors.document_extended:_compute/doc_xinghuo10_capm_beta_6m`
- 默认参数：`{"clip":[-3.0,3.0],"exclude_suspended_sessions":true,"half_life_days":null,"market_return":"lagged_circ_mv_weighted_available_universe","minimum_valid_days":100,"signal_frequency":"monthly","signal_timing":"previous_completed_month_end","weighting":"capm","window_days":126}`
- 适配说明：The report uses Wind All A free-float-cap-weighted market returns. The implementation uses lagged circ_mv weights within the available daily universe because free_share is outside the FactorFrame contract. Historical suspended sessions are removed, at least 100 valid sessions are required, beta is clipped to [-3,3], and each completed month-end estimate is exposed throughout the following calendar month.

## 发布与评估

- Publication status: `published`
- Evaluation status: `rejected`
- 因子版本：`8f9f02f470142206fd61`
- 数据快照：`snapshot_e3e73aa97706fd71f27ad486`
- 评估批次：`20260917_231028_ee6693d0`
- 有效区间：`2016-08-01` 至 `2026-09-15`

### 核心指标

- Rank IC Mean：`-0.00398529833373`
- Rank ICIR：`-0.0309568110387`
- Adjusted ICIR：`-0.0309568110387`
- Long-short spread (bps)：`4.08761196348`
- Monotonicity：`0.636363636364`
- Coverage：`0.790833333333`
- Daily turnover (long)：`0.0322300742958`
- Daily turnover (short)：`0.0306212393992`
