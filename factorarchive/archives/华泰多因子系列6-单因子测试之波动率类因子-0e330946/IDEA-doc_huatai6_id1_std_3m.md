# doc_huatai6_id1_std_3m

## 因子概览

- 类别：`volatility`
- 方向：`negative`
- 频率：`1d`
- 最小窗口：`64`
- 复权方式：`none`
- 实现状态：`approximate`

## 公式

```text
std(epsilon, ddof=0), epsilon from 63d OLS(return ~ 1 + market)
```

输入字段：`close_to_close_total_return_1d, is_suspended`

## 原理说明

用过去一段时间的价格、成交量或换手率概括股票的交易行为。

## 来源

- 逻辑来源组：`华泰多因子系列6-单因子测试之波动率类因子-0e330946`
- 来源组指纹：`0e33094604f770bf8116b0006d1cfa16e70148b0b958ff9031aede526293ec78`
- `JJJ643/量化因子挖掘思路475份/华泰多因子系列6：单因子测试之波动率类因子.pdf` — SHA-256 `0e33094604f770bf8116b0006d1cfa16e70148b0b958ff9031aede526293ec78`
  - 归档副本：`../../sources/JJJ643/量化因子挖掘思路475份/华泰多因子系列6：单因子测试之波动率类因子.pdf`
- 来源页码：`5, 17`

## 复现实现

- Python 实现：`microfactor.factors.document_extended:_compute/doc_huatai6_id1_std_3m`
- 默认参数：`{"exclude_suspended_sessions":true,"include_intercept":true,"market_return":"available_stock_equal_weight","minimum_valid_days":63,"residual_std_ddof":0,"window_days":63}`
- 适配说明：The report uses CSI All Share returns; the implementation uses the daily equal-weight return of available non-suspended stocks as a proxy. Three months is fixed at 63 trading days, output requires a complete stock-return window, and residual standard deviation uses ddof=0.

## 发布与评估

- Publication status: `published`
- Evaluation status: `passed`
- 因子版本：`5d3374ae23e703fdad1f`
- 数据快照：`snapshot_e3e73aa97706fd71f27ad486`
- 评估批次：`20260917_231028_ee6693d0`
- 有效区间：`2016-04-08` 至 `2026-09-15`

### 核心指标

- Rank IC Mean：`-0.0498251692582`
- Rank ICIR：`-0.425770183927`
- Adjusted ICIR：`0.425770183927`
- Long-short spread (bps)：`15.2931548869`
- Monotonicity：`0.963636363636`
- Coverage：`0.727402679275`
- Daily turnover (long)：`0.047082644419`
- Daily turnover (short)：`0.0443840127554`
