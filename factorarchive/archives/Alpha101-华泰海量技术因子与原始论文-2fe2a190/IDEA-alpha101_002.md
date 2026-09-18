# alpha101_002

## 因子概览

- 类别：`technical`
- 方向：`unspecified`
- 频率：`1d`
- 最小窗口：`8`
- 复权方式：`none`
- 实现状态：`exact`

## 公式

```text
-1 * correlation(rank(delta(log(volume), 2)), rank((close - open) / open), 6)
```

输入字段：`open, close, volume`

## 原理说明

看成交量变化和当天涨跌是否经常反着走。

## 来源

- 逻辑来源组：`Alpha101-华泰海量技术因子与原始论文-2fe2a190`
- 来源组指纹：`2fe2a1906be2da0ebc22e655e652cbb495027a0b859b18a0284b9014cb04dc8e`
- `JJJ643/量化因子挖掘思路475份/101 Formulaic Alphas - arXiv.org.pdf` — SHA-256 `99801b7740f7b2e4b079be20278347fdcf0a8a6a7a491c957dbd4927af5bed27`
  - 归档副本：`../../sources/JJJ643/量化因子挖掘思路475份/101 Formulaic Alphas - arXiv.org.pdf`
- `JJJ643/量化因子挖掘思路475份/华泰多因子系列11：单因子测试之海量技术因子.pdf` — SHA-256 `7cc15277a8c4adfb2f196ba1f574f8b287eea8bf8765ddecb267cc9aa16e4d4c`
  - 归档副本：`../../sources/JJJ643/量化因子挖掘思路475份/华泰多因子系列11：单因子测试之海量技术因子.pdf`
- 来源页码：`8`

## 复现实现

- Python 实现：`microfactor.factors.alpha101_document::alpha101_002`
- 默认参数：`{"delay_sessions":1,"factor_number":2}`
- 适配说明：Formula copied from the Alpha101 report; raw daily OHLC/VWAP is used and the signal is evaluated after the T-day close.

## 发布与评估

- Publication status: `published`
- Evaluation status: `passed`
- 因子版本：`717d7b3badc95ebc710f`
- 数据快照：`snapshot_e3e73aa97706fd71f27ad486`
- 评估批次：`20260917_231028_ee6693d0`
- 有效区间：`2016-01-13` 至 `2026-09-15`

### 核心指标

- Rank IC Mean：`0.021351932035`
- Rank ICIR：`0.388426555274`
- Adjusted ICIR：`0.388426555274`
- Long-short spread (bps)：`5.87067607517`
- Monotonicity：`0.939393939394`
- Coverage：`0.894517733231`
- Daily turnover (long)：`0.442272129014`
- Daily turnover (short)：`0.435487120707`
