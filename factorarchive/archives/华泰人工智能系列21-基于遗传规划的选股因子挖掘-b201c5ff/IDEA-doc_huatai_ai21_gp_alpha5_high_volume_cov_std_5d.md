# doc_huatai_ai21_gp_alpha5_high_volume_cov_std_5d

## 因子概览

- 类别：`price_volume`
- 方向：`positive`
- 频率：`1d`
- 最小窗口：`9`
- 复权方式：`hfq`
- 实现状态：`approximate`

## 公式

```text
-ts_sum(rank(covariance(high,volume,5)),5)*rank(ts_stddev(high,5))
```

输入字段：`high, volume`

## 原理说明

用过去一段时间的价格、成交量或换手率概括股票的交易行为。

## 来源

- 逻辑来源组：`华泰人工智能系列21-基于遗传规划的选股因子挖掘-b201c5ff`
- 来源组指纹：`b201c5ffae98c44a7d14c3cab40e031a9a925b74fc9315fbd00bb38310319073`
- `JJJ643/量化因子挖掘思路475份/华泰人工智能系列21：基于遗传规划的选股因子挖掘.pdf` — SHA-256 `b201c5ffae98c44a7d14c3cab40e031a9a925b74fc9315fbd00bb38310319073`
  - 归档副本：`../../sources/JJJ643/量化因子挖掘思路475份/华泰人工智能系列21：基于遗传规划的选股因子挖掘.pdf`
- 来源页码：`9, 11, 19`

## 复现实现

- Python 实现：`microfactor.factors.document_extended:_compute/doc_huatai_ai21_gp_alpha5_high_volume_cov_std_5d`
- 默认参数：`{"covariance_ddof":1,"covariance_window":5,"rank":"cross_sectional_average_percentile","rank_sum_window":5,"std_ddof":1}`
- 适配说明：The report does not pin price adjustment or the covariance/standard-deviation degrees of freedom. The implementation follows the existing Huatai formula family by using hfq prices and pandas sample estimators (ddof=1), exposes the raw daily formula without the report's industry and four-style neutralization, and uses the common one-day open_t1 evaluation instead of the source's 20-day target.

## 发布与评估

- Publication status: `published`
- Evaluation status: `passed`
- 因子版本：`2a00ab65b97c735258cb`
- 数据快照：`snapshot_e3e73aa97706fd71f27ad486`
- 评估批次：`20260917_231028_ee6693d0`
- 有效区间：`2016-01-14` 至 `2026-09-15`

### 核心指标

- Rank IC Mean：`0.0574498013074`
- Rank ICIR：`0.576847067254`
- Adjusted ICIR：`0.576847067254`
- Long-short spread (bps)：`19.4538507194`
- Monotonicity：`1`
- Coverage：`0.888931739298`
- Daily turnover (long)：`0.289125066112`
- Daily turnover (short)：`0.226477347365`
