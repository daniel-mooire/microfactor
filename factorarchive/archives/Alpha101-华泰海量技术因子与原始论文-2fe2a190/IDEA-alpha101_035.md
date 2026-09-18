# alpha101_035

## 因子概览

- 类别：`technical`
- 方向：`unspecified`
- 频率：`1d`
- 最小窗口：`32`
- 复权方式：`none`
- 实现状态：`exact`

## 公式

```text
Ts_Rank(volume, 32) * (1 - Ts_Rank((close + high) - low, 16)) * (1 - Ts_Rank(returns, 32))
```

输入字段：`high, low, close, volume, close_to_close_total_return_1d`

## 原理说明

同时考察成交量、价格位置和收益在各自历史窗口中的高低。

## 来源

- 逻辑来源组：`Alpha101-华泰海量技术因子与原始论文-2fe2a190`
- 来源组指纹：`2fe2a1906be2da0ebc22e655e652cbb495027a0b859b18a0284b9014cb04dc8e`
- `JJJ643/量化因子挖掘思路475份/101 Formulaic Alphas - arXiv.org.pdf` — SHA-256 `99801b7740f7b2e4b079be20278347fdcf0a8a6a7a491c957dbd4927af5bed27`
  - 归档副本：`../../sources/JJJ643/量化因子挖掘思路475份/101 Formulaic Alphas - arXiv.org.pdf`
- `JJJ643/量化因子挖掘思路475份/华泰多因子系列11：单因子测试之海量技术因子.pdf` — SHA-256 `7cc15277a8c4adfb2f196ba1f574f8b287eea8bf8765ddecb267cc9aa16e4d4c`
  - 归档副本：`../../sources/JJJ643/量化因子挖掘思路475份/华泰多因子系列11：单因子测试之海量技术因子.pdf`
- 来源页码：`10`

## 复现实现

- Python 实现：`microfactor.factors.alpha101_document::alpha101_035`
- 默认参数：`{"delay_sessions":1,"factor_number":35}`
- 适配说明：Formula copied from the Alpha101 report; raw daily OHLC/VWAP is used and the signal is evaluated after the T-day close. Returns use Microfactor's supplied total-return field under the same panel contract.

## 发布与评估

- Publication status: `published`
- Evaluation status: `rejected`
- 因子版本：`9b2c53c8eaa54108a23d`
- 数据快照：`snapshot_e3e73aa97706fd71f27ad486`
- 评估批次：`20260917_231028_ee6693d0`
- 有效区间：`2016-02-24` 至 `2026-09-15`

### 核心指标

- Rank IC Mean：`0.0204319644774`
- Rank ICIR：`0.219931980327`
- Adjusted ICIR：`0.219931980327`
- Long-short spread (bps)：`16.639029823`
- Monotonicity：`0.527272727273`
- Coverage：`0.802294667186`
- Daily turnover (long)：`0.705836082281`
- Daily turnover (short)：`0.76242356435`
