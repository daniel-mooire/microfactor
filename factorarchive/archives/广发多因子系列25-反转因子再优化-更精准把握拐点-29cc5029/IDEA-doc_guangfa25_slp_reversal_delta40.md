# doc_guangfa25_slp_reversal_delta40

## 因子概览

- 类别：`reversal`
- 方向：`negative`
- 频率：`1d`
- 最小窗口：`2`
- 复权方式：`hfq`
- 实现状态：`approximate`

## 公式

```text
(adjusted_close-P_last_confirmed_pivot)/(P_last_confirmed_pivot*days_since_pivot)
```

输入字段：`adjusted_close`

## 原理说明

用过去一段时间的价格、成交量或换手率概括股票的交易行为。

## 来源

- 逻辑来源组：`广发多因子系列25-反转因子再优化-更精准把握拐点-29cc5029`
- 来源组指纹：`29cc5029e1f0b82301afd2e652cdca408c8da8c7cd47ce3f460ad46e18236af6`
- `JJJ643/量化因子挖掘思路475份/广发多因子系列25：反转因子再优化，更精准把握拐点.pdf` — SHA-256 `29cc5029e1f0b82301afd2e652cdca408c8da8c7cd47ce3f460ad46e18236af6`
  - 归档副本：`../../sources/JJJ643/量化因子挖掘思路475份/广发多因子系列25：反转因子再优化，更精准把握拐点.pdf`
- 来源页码：`15, 18, 20, 21, 22, 24, 25, 27`

## 复现实现

- Python 实现：`microfactor.factors.document_extended:_compute/doc_guangfa25_slp_reversal_delta40`
- 默认参数：`{"pivot_confirmation":"causal_online","price":"adjusted_close_hfq","reversal_ratio":0.4,"slope_sign":"signed"}`
- 适配说明：报告未披露比例参数δP的数值；根据第18页与第21页示例中第15日尚未确认、第16日确认拐点的路径推断δP=0.40。使用后复权收盘价，并从每只股票首个有效观测初始化在线递推；不复刻报告的全市场20档、5日持有和0.3%费用回测。

## 发布与评估

- Publication status: `unpublished`
- Evaluation status: `not_evaluated`
- 当前没有固化版本或正式评估记录；本归档不推断评估结论。
