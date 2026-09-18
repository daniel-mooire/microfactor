# doc_jq2022_price_position_250d

## 因子概览

- 类别：`momentum`
- 方向：`positive`
- 频率：`1d`
- 最小窗口：`250`
- 复权方式：`qfq`
- 实现状态：`approximate`

## 公式

```text
(close-MIN(low,250))/(MAX(high,250)-MIN(low,250))
```

输入字段：`high, low, close, is_suspended`

## 原理说明

用过去一段时间的价格、成交量或换手率概括股票的交易行为。

## 来源

- 逻辑来源组：`97.-涨停研究一-具有哪些因子的股票更容易涨停-9cd87e21`
- 来源组指纹：`9cd87e21efc53f85c9178c54bfeb78df28c32125c6c565744df21f76215698c8`
- `2020-2026聚宽600条源码/2022年度精选策略/97.【涨停研究一】具有哪些因子的股票更容易涨停.txt` — SHA-256 `9cd87e21efc53f85c9178c54bfeb78df28c32125c6c565744df21f76215698c8`
  - 归档副本：`../../sources/2020-2026聚宽600条源码/2022年度精选策略/97.【涨停研究一】具有哪些因子的股票更容易涨停.txt`
- 来源页码：`未记录`

## 复现实现

- Python 实现：`microfactor.factors.document_extended:_compute/doc_jq2022_price_position_250d`
- 默认参数：`{"fill_paused":true,"source_target":"next_day_limit_up","source_threshold":"cross_sectional_mean","window":250}`
- 适配说明：源码把该连续量与截面均值比较后作为次日涨停事件筛选条件，并叠加流通市值与历史涨停次数过滤；实现仅暴露完全披露的250日原始价格位置，统一评估未来open_t1收益，不把离散策略条件包装成因子。

## 发布与评估

- Publication status: `unpublished`
- Evaluation status: `not_evaluated`
- 当前没有固化版本或正式评估记录；本归档不推断评估结论。
