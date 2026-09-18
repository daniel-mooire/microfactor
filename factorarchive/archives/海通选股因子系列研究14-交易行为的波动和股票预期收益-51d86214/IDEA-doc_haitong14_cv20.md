# doc_haitong14_cv20

## 因子概览

- 类别：`liquidity`
- 方向：`negative`
- 频率：`1d`
- 最小窗口：`15`
- 复权方式：`hfq`
- 实现状态：`approximate`

## 公式

```text
STD(turnover_rate,20)/MEAN(turnover_rate,20)
```

输入字段：`turnover_percent, list_date, is_suspended`

## 原理说明

用过去一段时间的价格、成交量或换手率概括股票的交易行为。

## 来源

- 逻辑来源组：`海通选股因子系列研究14-交易行为的波动和股票预期收益-51d86214`
- 来源组指纹：`51d862144c612132d6144f1c05aa8e8b2b36c63347cee014a4ef9872f983ee4e`
- `JJJ643/量化因子挖掘思路475份/海通选股因子系列研究14：交易行为的波动和股票预期收益.pdf` — SHA-256 `51d862144c612132d6144f1c05aa8e8b2b36c63347cee014a4ef9872f983ee4e`
  - 归档副本：`../../sources/JJJ643/量化因子挖掘思路475份/海通选股因子系列研究14：交易行为的波动和股票预期收益.pdf`
- 来源页码：`未记录`

## 复现实现

- Python 实现：`microfactor.factors.document_extended:_compute/doc_haitong14_cv20`
- 默认参数：`{}`
- 适配说明：保留上市满 12 个月、窗口至少 15 个有效日且窗口末未停牌的样本限制。

## 发布与评估

- Publication status: `published`
- Evaluation status: `passed`
- 因子版本：`6203df8c708ed5574bec`
- 数据快照：`snapshot_e3e73aa97706fd71f27ad486`
- 评估批次：`20260917_231028_ee6693d0`
- 有效区间：`2016-01-22` 至 `2026-09-15`

### 核心指标

- Rank IC Mean：`-0.0435054805378`
- Rank ICIR：`-0.567996982899`
- Adjusted ICIR：`0.567996982899`
- Long-short spread (bps)：`17.1632773228`
- Monotonicity：`1`
- Coverage：`0.884200618477`
- Daily turnover (long)：`0.17399643317`
- Daily turnover (short)：`0.138706903974`
