# doc_huatai6_id2_std_umd_3m

## 因子概览

- 类别：`volatility`
- 方向：`negative`
- 频率：`1d`
- 最小窗口：`64`
- 复权方式：`none`
- 实现状态：`approximate`

## 公式

```text
id2_std_up_3m-id2_std_down_3m, epsilon from 63d OLS(return ~ 1 + market + size + bp)
```

输入字段：`close_to_close_total_return_1d, is_suspended, total_mv, pb`

## 原理说明

用过去一段时间的价格、成交量或换手率概括股票的交易行为。

## 来源

- 逻辑来源组：`华泰多因子系列6-单因子测试之波动率类因子-0e330946`
- 来源组指纹：`0e33094604f770bf8116b0006d1cfa16e70148b0b958ff9031aede526293ec78`
- `JJJ643/量化因子挖掘思路475份/华泰多因子系列6：单因子测试之波动率类因子.pdf` — SHA-256 `0e33094604f770bf8116b0006d1cfa16e70148b0b958ff9031aede526293ec78`
  - 归档副本：`../../sources/JJJ643/量化因子挖掘思路475份/华泰多因子系列6：单因子测试之波动率类因子.pdf`
- 来源页码：`5, 20, 21, 22`

## 复现实现

- Python 实现：`microfactor.factors.document_extended:_compute/doc_huatai6_id2_std_umd_3m`
- 默认参数：`{"characteristic_lag_days":1,"exclude_suspended_sessions":true,"include_intercept":true,"market_return":"available_stock_equal_weight","minimum_valid_days":63,"portfolio_tail_fraction":0.3,"residual_std_ddof":0,"size_characteristic":"total_mv","value_characteristic":"pb","window_days":63}`
- 适配说明：The report uses CSI All Share returns; the implementation uses the daily equal-weight return of available non-suspended stocks as a proxy. Three months is fixed at 63 trading days. Size and PB returns use the current available-stock panel, lagged characteristics, and bottom-30% minus top-30% equal-weight returns. Output requires a complete stock-return window, and residual standard deviation uses ddof=0.

## 发布与评估

- Publication status: `published`
- Evaluation status: `passed`
- 因子版本：`712d0b1987c43dcb3bfc`
- 数据快照：`snapshot_e3e73aa97706fd71f27ad486`
- 评估批次：`20260917_231028_ee6693d0`
- 有效区间：`2016-04-08` 至 `2026-09-15`

### 核心指标

- Rank IC Mean：`-0.0436156342743`
- Rank ICIR：`-0.490563038536`
- Adjusted ICIR：`0.490563038536`
- Long-short spread (bps)：`17.123232646`
- Monotonicity：`0.842424242424`
- Coverage：`0.727402679275`
- Daily turnover (long)：`0.0854980292589`
- Daily turnover (short)：`0.0789625002891`
