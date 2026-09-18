# alpha101_068

## 因子概览

- 类别：`technical`
- 方向：`unspecified`
- 频率：`1d`
- 最小窗口：`21`
- 复权方式：`none`
- 实现状态：`exact`

## 公式

```text
(Ts_Rank(correlation(rank(high), rank(adv15), 8.91644), 13.9333) < rank(delta((close * 0.518371) + (low * (1 - 0.518371)), 1.06157))) * -1
```

输入字段：`high, low, close, volume`

## 原理说明

比较高价与成交均值相关性的历史位置，以及收盘/低价组合的短期变化。

## 来源

- 逻辑来源组：`Alpha101-华泰海量技术因子与原始论文-2fe2a190`
- 来源组指纹：`2fe2a1906be2da0ebc22e655e652cbb495027a0b859b18a0284b9014cb04dc8e`
- `JJJ643/量化因子挖掘思路475份/101 Formulaic Alphas - arXiv.org.pdf` — SHA-256 `99801b7740f7b2e4b079be20278347fdcf0a8a6a7a491c957dbd4927af5bed27`
  - 归档副本：`../../sources/JJJ643/量化因子挖掘思路475份/101 Formulaic Alphas - arXiv.org.pdf`
- `JJJ643/量化因子挖掘思路475份/华泰多因子系列11：单因子测试之海量技术因子.pdf` — SHA-256 `7cc15277a8c4adfb2f196ba1f574f8b287eea8bf8765ddecb267cc9aa16e4d4c`
  - 归档副本：`../../sources/JJJ643/量化因子挖掘思路475份/华泰多因子系列11：单因子测试之海量技术因子.pdf`
- 来源页码：`12`

## 复现实现

- Python 实现：`microfactor.factors.alpha101_document::alpha101_068`
- 默认参数：`{"delay_sessions":1,"factor_number":68}`
- 适配说明：Formula copied from the Alpha101 report; raw daily OHLC/VWAP is used and the signal is evaluated after the T-day close.

## 发布与评估

- Publication status: `published`
- Evaluation status: `rejected`
- 因子版本：`6702b3a80777f36c6e7f`
- 数据快照：`snapshot_e3e73aa97706fd71f27ad486`
- 评估批次：`20260917_231028_ee6693d0`
- 有效区间：`2016-02-25` 至 `2026-09-15`

### 核心指标

- Rank IC Mean：`0.0125031789808`
- Rank ICIR：`0.175839599683`
- Adjusted ICIR：`0.175839599683`
- Long-short spread (bps)：`-0.0219415636408`
- Monotonicity：`0.478787878788`
- Coverage：`0.798375`
- Daily turnover (long)：`0.364305464196`
- Daily turnover (short)：`0.380665435004`
