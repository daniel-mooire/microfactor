# doc_huatai_turn_3

## 因子概览

- 类别：`liquidity`
- 方向：`unspecified`
- 频率：`1d`
- 最小窗口：`63`
- 复权方式：`hfq`
- 实现状态：`exact`

## 公式

```text
MEAN(turnover_percent,63)
```

输入字段：`turnover_percent`

## 原理说明

用过去一段时间的价格、成交量或换手率概括股票的交易行为。

## 来源

- 逻辑来源组：`华泰多因子系列基础换手率与波动率因子-a280d26b`
- 来源组指纹：`a280d26bc424b0eecfa985bfebf14a4a4a6d02c7e992eed3593ac476b1d20edc`
- `JJJ643/量化因子挖掘思路475份/华泰多因子系列5：单因子测试之换手率类因子.pdf` — SHA-256 `9a5a628f98b71d850e73e3ef3f15a783fa3cd73fe8d0e47c67c75631e57cc109`
  - 归档副本：`../../sources/JJJ643/量化因子挖掘思路475份/华泰多因子系列5：单因子测试之换手率类因子.pdf`
- 来源页码：`未记录`

## 复现实现

- Python 实现：`microfactor.factors.document_extended:_compute/doc_huatai_turn_3`
- 默认参数：`{}`
- 适配说明：无。

## 发布与评估

- Publication status: `published`
- Evaluation status: `rejected`
- 因子版本：`146ac00914c5a9df9065`
- 数据快照：`snapshot_e3e73aa97706fd71f27ad486`
- 评估批次：`20260917_231028_ee6693d0`
- 有效区间：`2016-01-06` 至 `2026-09-15`

### 核心指标

- Rank IC Mean：`-0.05915124218`
- Rank ICIR：`-0.443035674397`
- Adjusted ICIR：`-0.443035674397`
- Long-short spread (bps)：`-22.7542882927`
- Monotonicity：`-0.842424242424`
- Coverage：`0.954805309735`
- Daily turnover (long)：`0.16778400604`
- Daily turnover (short)：`0.170657921123`
