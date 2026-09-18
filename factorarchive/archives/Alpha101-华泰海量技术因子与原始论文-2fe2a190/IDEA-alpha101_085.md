# alpha101_085

## 因子概览

- 类别：`technical`
- 方向：`unspecified`
- 频率：`1d`
- 最小窗口：`17`
- 复权方式：`none`
- 实现状态：`exact`

## 公式

```text
rank(correlation((high * 0.876703) + (close * (1 - 0.876703)), adv30, 9.61331)) ^ rank(correlation(Ts_Rank((high + low) / 2, 3.70596), Ts_Rank(volume, 10.1595), 7.11408))
```

输入字段：`high, low, close, volume`

## 原理说明

把高价/收盘组合的成交相关排名，与中间价和成交量历史位置关系组合。

## 来源

- 逻辑来源组：`Alpha101-华泰海量技术因子与原始论文-2fe2a190`
- 来源组指纹：`2fe2a1906be2da0ebc22e655e652cbb495027a0b859b18a0284b9014cb04dc8e`
- `JJJ643/量化因子挖掘思路475份/101 Formulaic Alphas - arXiv.org.pdf` — SHA-256 `99801b7740f7b2e4b079be20278347fdcf0a8a6a7a491c957dbd4927af5bed27`
  - 归档副本：`../../sources/JJJ643/量化因子挖掘思路475份/101 Formulaic Alphas - arXiv.org.pdf`
- `JJJ643/量化因子挖掘思路475份/华泰多因子系列11：单因子测试之海量技术因子.pdf` — SHA-256 `7cc15277a8c4adfb2f196ba1f574f8b287eea8bf8765ddecb267cc9aa16e4d4c`
  - 归档副本：`../../sources/JJJ643/量化因子挖掘思路475份/华泰多因子系列11：单因子测试之海量技术因子.pdf`
- 来源页码：`13`

## 复现实现

- Python 实现：`microfactor.factors.alpha101_document::alpha101_085`
- 默认参数：`{"delay_sessions":1,"factor_number":85}`
- 适配说明：Formula copied from the Alpha101 report; raw daily OHLC/VWAP is used and the signal is evaluated after the T-day close.

## 发布与评估

- Publication status: `published`
- Evaluation status: `rejected`
- 因子版本：`b2f51868d2efc1963483`
- 数据快照：`snapshot_e3e73aa97706fd71f27ad486`
- 评估批次：`20260917_231028_ee6693d0`
- 有效区间：`2016-03-02` 至 `2026-09-15`

### 核心指标

- Rank IC Mean：`-0.000705503311162`
- Rank ICIR：`-0.01068249449`
- Adjusted ICIR：`-0.01068249449`
- Long-short spread (bps)：`-4.83413935571`
- Monotonicity：`-0.539393939394`
- Coverage：`0.773579173167`
- Daily turnover (long)：`0.410287329047`
- Daily turnover (short)：`0.382567745263`
