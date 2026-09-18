# alpha101_078

## 因子概览

- 类别：`technical`
- 方向：`unspecified`
- 频率：`1d`
- 最小窗口：`25`
- 复权方式：`none`
- 实现状态：`exact`

## 公式

```text
rank(correlation(sum((low * 0.352233) + (vwap * (1 - 0.352233)), 19.7428), sum(adv40, 19.7428), 6.83313)) ^ rank(correlation(rank(vwap), rank(volume), 5.77492))
```

输入字段：`low, volume, amount`

## 原理说明

把低价/VWAP组合与成交均值的相关排名，用VWAP和成交量相关排名加权。

## 来源

- 逻辑来源组：`Alpha101-华泰海量技术因子与原始论文-2fe2a190`
- 来源组指纹：`2fe2a1906be2da0ebc22e655e652cbb495027a0b859b18a0284b9014cb04dc8e`
- `JJJ643/量化因子挖掘思路475份/101 Formulaic Alphas - arXiv.org.pdf` — SHA-256 `99801b7740f7b2e4b079be20278347fdcf0a8a6a7a491c957dbd4927af5bed27`
  - 归档副本：`../../sources/JJJ643/量化因子挖掘思路475份/101 Formulaic Alphas - arXiv.org.pdf`
- `JJJ643/量化因子挖掘思路475份/华泰多因子系列11：单因子测试之海量技术因子.pdf` — SHA-256 `7cc15277a8c4adfb2f196ba1f574f8b287eea8bf8765ddecb267cc9aa16e4d4c`
  - 归档副本：`../../sources/JJJ643/量化因子挖掘思路475份/华泰多因子系列11：单因子测试之海量技术因子.pdf`
- 来源页码：`13`

## 复现实现

- Python 实现：`microfactor.factors.alpha101_document::alpha101_078`
- 默认参数：`{"delay_sessions":1,"factor_number":78}`
- 适配说明：Formula copied from the Alpha101 report; raw daily OHLC/VWAP is used and the signal is evaluated after the T-day close.

## 发布与评估

- Publication status: `published`
- Evaluation status: `rejected`
- 因子版本：`7224a3ea7d1a27fad772`
- 数据快照：`snapshot_e3e73aa97706fd71f27ad486`
- 评估批次：`20260917_231028_ee6693d0`
- 有效区间：`2016-04-07` 至 `2026-09-15`

### 核心指标

- Rank IC Mean：`0.00541828827149`
- Rank ICIR：`0.0842254027474`
- Adjusted ICIR：`0.0842254027474`
- Long-short spread (bps)：`-1.16538252305`
- Monotonicity：`0.430303030303`
- Coverage：`0.729363528948`
- Daily turnover (long)：`0.464703059619`
- Daily turnover (short)：`0.369385258822`
