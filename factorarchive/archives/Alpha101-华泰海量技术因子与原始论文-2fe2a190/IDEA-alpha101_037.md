# alpha101_037

## 因子概览

- 类别：`technical`
- 方向：`unspecified`
- 频率：`1d`
- 最小窗口：`201`
- 复权方式：`none`
- 实现状态：`exact`

## 公式

```text
rank(correlation(delay(open - close, 1), close, 200)) + rank(open - close)
```

输入字段：`open, close`

## 原理说明

结合长期日内涨跌与收盘价关系，以及当天日内弱强。

## 来源

- 逻辑来源组：`Alpha101-华泰海量技术因子与原始论文-2fe2a190`
- 来源组指纹：`2fe2a1906be2da0ebc22e655e652cbb495027a0b859b18a0284b9014cb04dc8e`
- `JJJ643/量化因子挖掘思路475份/101 Formulaic Alphas - arXiv.org.pdf` — SHA-256 `99801b7740f7b2e4b079be20278347fdcf0a8a6a7a491c957dbd4927af5bed27`
  - 归档副本：`../../sources/JJJ643/量化因子挖掘思路475份/101 Formulaic Alphas - arXiv.org.pdf`
- `JJJ643/量化因子挖掘思路475份/华泰多因子系列11：单因子测试之海量技术因子.pdf` — SHA-256 `7cc15277a8c4adfb2f196ba1f574f8b287eea8bf8765ddecb267cc9aa16e4d4c`
  - 归档副本：`../../sources/JJJ643/量化因子挖掘思路475份/华泰多因子系列11：单因子测试之海量技术因子.pdf`
- 来源页码：`10`

## 复现实现

- Python 实现：`microfactor.factors.alpha101_document::alpha101_037`
- 默认参数：`{"delay_sessions":1,"factor_number":37}`
- 适配说明：Formula copied from the Alpha101 report; raw daily OHLC/VWAP is used and the signal is evaluated after the T-day close.

## 发布与评估

- Publication status: `published`
- Evaluation status: `rejected`
- 因子版本：`a393d0bd920053d097ed`
- 数据快照：`snapshot_e3e73aa97706fd71f27ad486`
- 评估批次：`20260917_231028_ee6693d0`
- 有效区间：`2016-11-01` 至 `2026-09-15`

### 核心指标

- Rank IC Mean：`0.0324464627167`
- Rank ICIR：`0.370424997885`
- Adjusted ICIR：`0.370424997885`
- Long-short spread (bps)：`20.1607231255`
- Monotonicity：`0.927272727273`
- Coverage：`0.531443565181`
- Daily turnover (long)：`0.677706738695`
- Daily turnover (short)：`0.665280864089`
