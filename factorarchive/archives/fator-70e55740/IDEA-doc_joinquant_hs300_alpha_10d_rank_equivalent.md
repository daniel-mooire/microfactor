# doc_joinquant_hs300_alpha_10d_rank_equivalent

## 因子概览

- 类别：`momentum`
- 方向：`positive`
- 频率：`1d`
- 最小窗口：`10`
- 复权方式：`qfq`
- 实现状态：`approximate`

## 公式

```text
RANK_EQUIVALENT((C_t/C_{t-9}-1)-R_HS300,t)=C_t/C_{t-9}-1
```

输入字段：`adjusted_close`

## 原理说明

用过去一段时间的价格、成交量或换手率概括股票的交易行为。

## 来源

- 逻辑来源组：`fator-70e55740`
- 来源组指纹：`70e557409f69eedc0b33b308de901d04503b611aa94621b86e95ff08750dcf47`
- `量化Skills合集/joinquant-docs/fator.md` — SHA-256 `70e557409f69eedc0b33b308de901d04503b611aa94621b86e95ff08750dcf47`
  - 归档副本：`../../sources/量化Skills合集/joinquant-docs/fator.md`
- 来源页码：`未记录`

## 复现实现

- Python 实现：`microfactor.factors.document_extended:_compute/doc_joinquant_hs300_alpha_10d_rank_equivalent`
- 默认参数：`{"benchmark":"000300.XSHG","return_lag_sessions":9,"stored_value":"stock_return_leg","window_rows":10}`
- 适配说明：原式用10行收盘价计算个股收益并减去同期沪深300收益，即包含9个交易间隔。指数收益在同一截面是公共标量，不改变排序、分组、RankIC或Spearman去重结果；因此实现只保存个股收益腿，并使用项目可用的前复权收盘价。

## 发布与评估

- Publication status: `unpublished`
- Evaluation status: `not_evaluated`
- 当前没有固化版本或正式评估记录；本归档不推断评估结论。
