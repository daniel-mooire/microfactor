# doc_huatai_ai23_gp_alpha2

## 因子概览

- 类别：`price_volume`
- 方向：`negative`
- 频率：`1d`
- 最小窗口：`9`
- 复权方式：`none`
- 实现状态：`approximate`

## 公式

```text
-ts_cov(delay(volume,5),vwap,4)
```

输入字段：`volume, vwap`

## 原理说明

用过去一段时间的价格、成交量或换手率概括股票的交易行为。

## 来源

- 逻辑来源组：`华泰人工智能系列23-再探基于遗传规划的选股因子挖掘-bd8a7160`
- 来源组指纹：`bd8a7160e81d27798a5ac9a18ae35085b947abe0cd4ee708c67cb5d83d26667e`
- `JJJ643/量化因子挖掘思路475份/华泰人工智能系列23：再探基于遗传规划的选股因子挖掘.pdf` — SHA-256 `bd8a7160e81d27798a5ac9a18ae35085b947abe0cd4ee708c67cb5d83d26667e`
  - 归档副本：`../../sources/JJJ643/量化因子挖掘思路475份/华泰人工智能系列23：再探基于遗传规划的选股因子挖掘.pdf`
- 来源页码：`9, 12, 16`

## 复现实现

- Python 实现：`microfactor.factors.document_extended:_compute/doc_huatai_ai23_gp_alpha2`
- 默认参数：`{"covariance_ddof":1,"free_turn":"turnover_rate_f","rank":"cross_sectional_average_percentile","std_ddof":1,"ts_zscore":"rolling_mean_divided_by_sample_std","turn":"turnover_rate"}`
- 适配说明：The report fully specifies the formulas and distinguishes ordinary turnover from free-float turnover. The implementation maps them to Tushare turnover_rate and turnover_rate_f, uses pandas sample covariance and standard deviation (ddof=1), and reproduces the raw daily formulas without the report's cross-sectional winsorization, industry/style neutralization, nonlinear transformation, or 20-day prediction target. Price adjustment is not pinned for the raw OHLC inputs; formulas containing return1 use hfq bars, while the other formulas use unadjusted bars.

## 发布与评估

- Publication status: `published`
- Evaluation status: `rejected`
- 因子版本：`da5af5abebaee500a3ee`
- 数据快照：`snapshot_e3e73aa97706fd71f27ad486`
- 评估批次：`20260917_231028_ee6693d0`
- 有效区间：`2016-01-14` 至 `2026-09-15`

### 核心指标

- Rank IC Mean：`-0.00599982707549`
- Rank ICIR：`-0.102575629968`
- Adjusted ICIR：`0.102575629968`
- Long-short spread (bps)：`0.251125277768`
- Monotonicity：`0.0909090909091`
- Coverage：`0.890472811415`
- Daily turnover (long)：`0.479037941012`
- Daily turnover (short)：`0.462181942373`
