# alpha101_032

## 因子概览

- 类别：`technical`
- 方向：`unspecified`
- 频率：`1d`
- 最小窗口：`235`
- 复权方式：`none`
- 实现状态：`exact`

## 公式

```text
scale((sum(close, 7) / 7) - close) + (20 * scale(correlation(vwap, delay(close, 5), 230)))
```

输入字段：`close, volume, amount`

## 原理说明

结合价格偏离7日均线的反转，以及VWAP与滞后价格的长期关系。

## 来源

- 逻辑来源组：`Alpha101-华泰海量技术因子与原始论文-2fe2a190`
- 来源组指纹：`2fe2a1906be2da0ebc22e655e652cbb495027a0b859b18a0284b9014cb04dc8e`
- `JJJ643/量化因子挖掘思路475份/101 Formulaic Alphas - arXiv.org.pdf` — SHA-256 `99801b7740f7b2e4b079be20278347fdcf0a8a6a7a491c957dbd4927af5bed27`
  - 归档副本：`../../sources/JJJ643/量化因子挖掘思路475份/101 Formulaic Alphas - arXiv.org.pdf`
- `JJJ643/量化因子挖掘思路475份/华泰多因子系列11：单因子测试之海量技术因子.pdf` — SHA-256 `7cc15277a8c4adfb2f196ba1f574f8b287eea8bf8765ddecb267cc9aa16e4d4c`
  - 归档副本：`../../sources/JJJ643/量化因子挖掘思路475份/华泰多因子系列11：单因子测试之海量技术因子.pdf`
- 来源页码：`10`

## 复现实现

- Python 实现：`microfactor.factors.alpha101_document::alpha101_032`
- 默认参数：`{"delay_sessions":1,"factor_number":32}`
- 适配说明：Formula copied from the Alpha101 report; raw daily OHLC/VWAP is used and the signal is evaluated after the T-day close.

## 发布与评估

- Publication status: `published`
- Evaluation status: `rejected`
- 因子版本：`b4023ef6cfba1043442f`
- 数据快照：`snapshot_e3e73aa97706fd71f27ad486`
- 评估批次：`20260917_231028_ee6693d0`
- 有效区间：`2016-12-19` 至 `2026-09-15`

### 核心指标

- Rank IC Mean：`0.0203665038217`
- Rank ICIR：`0.241676506017`
- Adjusted ICIR：`0.241676506017`
- Long-short spread (bps)：`14.0622393912`
- Monotonicity：`0.939393939394`
- Coverage：`0.497633713561`
- Daily turnover (long)：`0.215087898565`
- Daily turnover (short)：`0.139700947013`
