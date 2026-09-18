# doc_bohai14_adj_alpha025

## 因子概览

- 类别：`technical`
- 方向：`positive`
- 频率：`1d`
- 最小窗口：`1`
- 复权方式：`none`
- 实现状态：`exact`

## 公式

```text
-(alpha101_025 - cross_section_median(alpha101_025))^2
```

输入字段：`high, close, volume, amount, close_to_close_total_return_1d`

## 原理说明

Prefer stocks whose original Alpha101 exposure is near the daily cross-sectional median and penalize both extreme tails.

## 来源

- 逻辑来源组：`渤海系列14-Alpha101横截面调整-4bb9ed92`
- 来源组指纹：`4bb9ed92da9a96e8e7729b94346898cc4b14c6adede3d1dc1535331c69479fe9`
- `JJJ643/量化因子挖掘思路475份/101 Formulaic Alphas - arXiv.org.pdf` — SHA-256 `99801b7740f7b2e4b079be20278347fdcf0a8a6a7a491c957dbd4927af5bed27`
  - 归档副本：`../../sources/JJJ643/量化因子挖掘思路475份/101 Formulaic Alphas - arXiv.org.pdf`
- `JJJ643/量化因子挖掘思路475份/渤海多因子模型研究系列14：技术因子的再挖掘Alpha 101.pdf` — SHA-256 `7fbecfc8ee23a918b3829a05ad3026c734868e34fa411fac4d0a8e88f7ecffbf`
  - 归档副本：`../../sources/JJJ643/量化因子挖掘思路475份/渤海多因子模型研究系列14：技术因子的再挖掘Alpha 101.pdf`
- 来源页码：`12`

## 复现实现

- Python 实现：`microfactor.factors.alpha101_document::doc_bohai14_adj_alpha025`
- 默认参数：`{"delay_sessions":1,"factor_number":25}`
- 适配说明：Bohai series 14 page 12 applies the negative squared distance from the same-day cross-sectional median to the published Alpha101 value. The median is computed only from stocks available in the supplied point-in-time universe.

## 发布与评估

- Publication status: `unpublished`
- Evaluation status: `not_evaluated`
- 当前没有固化版本或正式评估记录；本归档不推断评估结论。
