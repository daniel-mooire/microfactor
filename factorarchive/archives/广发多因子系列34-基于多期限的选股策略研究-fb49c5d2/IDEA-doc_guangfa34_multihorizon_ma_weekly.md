# doc_guangfa34_multihorizon_ma_weekly

## 因子概览

- 类别：`trend`
- 方向：`positive`
- 频率：`1d`
- 最小窗口：`430`
- 复权方式：`hfq`
- 实现状态：`approximate`

## 公式

```text
next-week expected return from 12 normalized moving-average horizons, 25-week mean cross-sectional OLS coefficients
```

输入字段：`adjusted_close, is_suspended, is_st, list_date`

## 原理说明

用过去一段时间的价格、成交量或换手率概括股票的交易行为。

## 来源

- 逻辑来源组：`广发多因子系列34-基于多期限的选股策略研究-fb49c5d2`
- 来源组指纹：`fb49c5d26099b31e1693d682df11f90df68e047ba14c1cca7c0b0c7179e49b83`
- `JJJ643/量化因子挖掘思路475份/广发多因子系列34：基于多期限的选股策略研究.pdf` — SHA-256 `fb49c5d26099b31e1693d682df11f90df68e047ba14c1cca7c0b0c7179e49b83`
  - 归档副本：`../../sources/JJJ643/量化因子挖掘思路475份/广发多因子系列34：基于多期限的选股策略研究.pdf`
- 来源页码：`1, 5, 6`

## 复现实现

- Python 实现：`microfactor.factors.document_extended:_compute/doc_guangfa34_multihorizon_ma_weekly`
- 默认参数：`{"coefficient_lookback_weeks":25,"exclude_current_st":true,"exclude_current_suspended":true,"horizons_days":[3,5,10,20,30,60,90,120,180,240,270,300],"include_intercept":true,"indicator":"ma","listing_age_days":365,"signal_frequency":"weekly","signal_timing":"previous_completed_week"}`
- 适配说明：The report uses all A shares, weekly portfolio formation, raw price history, and next-week returns. The implementation uses adjusted close in the available daily universe, calendar weeks ending Friday, the last available trading session as week-end, and carries each completed-week prediction through the following week. The report's one-year listing, current suspension, and ST filters are preserved.

## 发布与评估

- Publication status: `published`
- Evaluation status: `rejected`
- 因子版本：`79b07c39f41c4162ac96`
- 数据快照：`snapshot_e3e73aa97706fd71f27ad486`
- 评估批次：`20260917_231028_ee6693d0`
- 有效区间：`2017-09-25` 至 `2026-09-15`

### 核心指标

- Rank IC Mean：`0.035631440188`
- Rank ICIR：`0.31046946461`
- Adjusted ICIR：`0.31046946461`
- Long-short spread (bps)：`19.1389667418`
- Monotonicity：`0.927272727273`
- Coverage：`0.445929292929`
- Daily turnover (long)：`0.116954557348`
- Daily turnover (short)：`0.148277768605`
