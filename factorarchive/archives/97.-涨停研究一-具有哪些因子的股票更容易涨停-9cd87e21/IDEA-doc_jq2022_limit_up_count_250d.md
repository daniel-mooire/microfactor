# doc_jq2022_limit_up_count_250d

## 因子概览

- 类别：`event`
- 方向：`positive`
- 频率：`1d`
- 最小窗口：`250`
- 复权方式：`none`
- 实现状态：`approximate`

## 公式

```text
SUM(close==up_limit,250)
```

输入字段：`close, up_limit, is_suspended`

## 原理说明

用过去一段时间的价格、成交量或换手率概括股票的交易行为。

## 来源

- 逻辑来源组：`97.-涨停研究一-具有哪些因子的股票更容易涨停-9cd87e21`
- 来源组指纹：`9cd87e21efc53f85c9178c54bfeb78df28c32125c6c565744df21f76215698c8`
- `2020-2026聚宽600条源码/2022年度精选策略/97.【涨停研究一】具有哪些因子的股票更容易涨停.txt` — SHA-256 `9cd87e21efc53f85c9178c54bfeb78df28c32125c6c565744df21f76215698c8`
  - 归档副本：`../../sources/2020-2026聚宽600条源码/2022年度精选策略/97.【涨停研究一】具有哪些因子的股票更容易涨停.txt`
- 来源页码：`未记录`

## 复现实现

- Python 实现：`microfactor.factors.document_extended:_compute/doc_jq2022_limit_up_count_250d`
- 默认参数：`{"source_target":"next_day_limit_up","source_threshold_multiple":5.0,"suspended_session_event":0,"window":250}`
- 适配说明：源码要求历史涨停次数高于全市场均值的5倍，并与价格位置和流通市值共同筛选次日涨停候选；实现仅暴露完全披露的250日原始计数，统一评估未来open_t1收益。

## 发布与评估

- Publication status: `unpublished`
- Evaluation status: `not_evaluated`
- 当前没有固化版本或正式评估记录；本归档不推断评估结论。
