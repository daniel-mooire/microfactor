# doc_huatai_ai21_gp_alpha3_volume_std_5d

## 因子概览

- 类别：`liquidity`
- 方向：`positive`
- 频率：`1d`
- 最小窗口：`5`
- 复权方式：`hfq`
- 实现状态：`approximate`

## 公式

```text
-ts_stddev(volume,5)
```

输入字段：`volume`

## 原理说明

用过去一段时间的价格、成交量或换手率概括股票的交易行为。

## 来源

- 逻辑来源组：`华泰人工智能系列21-基于遗传规划的选股因子挖掘-b201c5ff`
- 来源组指纹：`b201c5ffae98c44a7d14c3cab40e031a9a925b74fc9315fbd00bb38310319073`
- `JJJ643/量化因子挖掘思路475份/华泰人工智能系列21：基于遗传规划的选股因子挖掘.pdf` — SHA-256 `b201c5ffae98c44a7d14c3cab40e031a9a925b74fc9315fbd00bb38310319073`
  - 归档副本：`../../sources/JJJ643/量化因子挖掘思路475份/华泰人工智能系列21：基于遗传规划的选股因子挖掘.pdf`
- 来源页码：`9, 11, 17`

## 复现实现

- Python 实现：`microfactor.factors.document_extended:_compute/doc_huatai_ai21_gp_alpha3_volume_std_5d`
- 默认参数：`{"std_ddof":1,"window":5}`
- 适配说明：The report does not pin price adjustment or the covariance/standard-deviation degrees of freedom. The implementation follows the existing Huatai formula family by using hfq prices and pandas sample estimators (ddof=1), exposes the raw daily formula without the report's industry and four-style neutralization, and uses the common one-day open_t1 evaluation instead of the source's 20-day target.

## 发布与评估

- Publication status: `published`
- Evaluation status: `passed`
- 因子版本：`797619a9d86f6de5e725`
- 数据快照：`snapshot_e3e73aa97706fd71f27ad486`
- 评估批次：`20260917_231028_ee6693d0`
- 有效区间：`2016-01-08` 至 `2026-09-15`

### 核心指标

- Rank IC Mean：`0.0574955884834`
- Rank ICIR：`0.506739167907`
- Adjusted ICIR：`0.506739167907`
- Long-short spread (bps)：`15.6246271312`
- Monotonicity：`0.987878787879`
- Coverage：`0.922290335002`
- Daily turnover (long)：`0.245613716644`
- Daily turnover (short)：`0.209708763059`
