# doc_huatai_ai21_gp_alpha4_high_volume_cov_std_10d

## 因子概览

- 类别：`price_volume`
- 方向：`positive`
- 频率：`1d`
- 最小窗口：`10`
- 复权方式：`hfq`
- 实现状态：`approximate`

## 公式

```text
-rank(covariance(high,volume,10))*rank(ts_stddev(high,10))
```

输入字段：`high, volume`

## 原理说明

用过去一段时间的价格、成交量或换手率概括股票的交易行为。

## 来源

- 逻辑来源组：`华泰人工智能系列21-基于遗传规划的选股因子挖掘-b201c5ff`
- 来源组指纹：`b201c5ffae98c44a7d14c3cab40e031a9a925b74fc9315fbd00bb38310319073`
- `JJJ643/量化因子挖掘思路475份/华泰人工智能系列21：基于遗传规划的选股因子挖掘.pdf` — SHA-256 `b201c5ffae98c44a7d14c3cab40e031a9a925b74fc9315fbd00bb38310319073`
  - 归档副本：`../../sources/JJJ643/量化因子挖掘思路475份/华泰人工智能系列21：基于遗传规划的选股因子挖掘.pdf`
- 来源页码：`9, 11, 18`

## 复现实现

- Python 实现：`microfactor.factors.document_extended:_compute/doc_huatai_ai21_gp_alpha4_high_volume_cov_std_10d`
- 默认参数：`{"covariance_ddof":1,"rank":"cross_sectional_average_percentile","std_ddof":1,"window":10}`
- 适配说明：The report does not pin price adjustment or the covariance/standard-deviation degrees of freedom. The implementation follows the existing Huatai formula family by using hfq prices and pandas sample estimators (ddof=1), exposes the raw daily formula without the report's industry and four-style neutralization, and uses the common one-day open_t1 evaluation instead of the source's 20-day target.

## 发布与评估

- Publication status: `published`
- Evaluation status: `passed`
- 因子版本：`690020a4b78ddfbc1f4a`
- 数据快照：`snapshot_e3e73aa97706fd71f27ad486`
- 评估批次：`20260917_231028_ee6693d0`
- 有效区间：`2016-01-15` 至 `2026-09-15`

### 核心指标

- Rank IC Mean：`0.0541521287777`
- Rank ICIR：`0.549190106396`
- Adjusted ICIR：`0.549190106396`
- Long-short spread (bps)：`20.1245901078`
- Monotonicity：`0.963636363636`
- Coverage：`0.88403742284`
- Daily turnover (long)：`0.23686325463`
- Daily turnover (short)：`0.159422046133`
