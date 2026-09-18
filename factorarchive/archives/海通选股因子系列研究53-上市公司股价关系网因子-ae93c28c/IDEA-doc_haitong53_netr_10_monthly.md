# doc_haitong53_netr_10_monthly

## 因子概览

- 类别：`network_reversal`
- 方向：`negative`
- 频率：`1d`
- 最小窗口：`21`
- 复权方式：`none`
- 实现状态：`approximate`

## 公式

```text
mean available-session 20d compounded return of the top 10% peers ranked by absolute 20d daily-return correlation with at least 15 pairwise observations
```

输入字段：`close_total_return_index, is_suspended, is_st, list_date`

## 原理说明

用过去一段时间的价格、成交量或换手率概括股票的交易行为。

## 来源

- 逻辑来源组：`海通选股因子系列研究53-上市公司股价关系网因子-ae93c28c`
- 来源组指纹：`ae93c28c192c28488c8fbf5258e377ffdfc0af3f67a951420487239afa2da845`
- `JJJ643/量化因子挖掘思路475份/海通选股因子系列研究53：上市公司股价关系网因子.pdf` — SHA-256 `ae93c28c192c28488c8fbf5258e377ffdfc0af3f67a951420487239afa2da845`
  - 归档副本：`../../sources/JJJ643/量化因子挖掘思路475份/海通选股因子系列研究53：上市公司股价关系网因子.pdf`
- 来源页码：`1, 6, 7, 9`

## 复现实现

- Python 实现：`microfactor.factors.document_extended:_compute/doc_haitong53_netr_10_monthly`
- 默认参数：`{"correlation_selection":"largest_absolute","correlation_window_days":20,"exclude_current_limit_up":false,"exclude_current_st":true,"exclude_current_suspended":true,"minimum_listing_age_months":6,"minimum_valid_days":15,"missing_return_handling":"pairwise_complete","peer_fraction":0.1,"peer_return_window_days":20,"signal_frequency":"monthly","signal_timing":"previous_completed_month_end"}`
- 适配说明：The report uses all A shares and excludes current limit-up stocks. The implementation uses the available daily universe, adjusted total-return prices, current source-date suspension/ST filters, a calendar six-month listing-age filter, and pairwise-complete correlations with at least 15 of 20 daily returns. Peer 20-day returns compound the same available sessions. The top peer count is ceil(10% of eligible non-self peers); no limit-up field exists in the current FactorFrame contract. Each completed month-end signal is exposed throughout the following calendar month.

## 发布与评估

- Publication status: `published`
- Evaluation status: `rejected`
- 因子版本：`cc53ff1c2b34308b4289`
- 数据快照：`snapshot_e3e73aa97706fd71f27ad486`
- 评估批次：`20260917_231028_ee6693d0`
- 有效区间：`2016-03-01` 至 `2026-09-15`

### 核心指标

- Rank IC Mean：`-0.0217740844517`
- Rank ICIR：`-0.216163183797`
- Adjusted ICIR：`0.216163183797`
- Long-short spread (bps)：`9.70200101495`
- Monotonicity：`0.951515151515`
- Coverage：`0.865843664717`
- Daily turnover (long)：`0.054124080052`
- Daily turnover (short)：`0.060528538308`
