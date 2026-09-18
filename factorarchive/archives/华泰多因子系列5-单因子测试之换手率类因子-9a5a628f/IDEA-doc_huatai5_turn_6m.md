# doc_huatai5_turn_6m

## 因子概览

- 类别：`liquidity`
- 方向：`negative`
- 频率：`1d`
- 最小窗口：`126`
- 复权方式：`none`
- 实现状态：`exact`

## 公式

```text
mean(turnover_percent[t-125:t])
```

输入字段：`turnover_percent`

## 原理说明

用过去一段时间的价格、成交量或换手率概括股票的交易行为。

## 来源

- 逻辑来源组：`华泰多因子系列5-单因子测试之换手率类因子-9a5a628f`
- 来源组指纹：`9a5a628f98b71d850e73e3ef3f15a783fa3cd73fe8d0e47c67c75631e57cc109`
- `JJJ643/量化因子挖掘思路475份/华泰多因子系列5：单因子测试之换手率类因子.pdf` — SHA-256 `9a5a628f98b71d850e73e3ef3f15a783fa3cd73fe8d0e47c67c75631e57cc109`
  - 归档副本：`../../sources/JJJ643/量化因子挖掘思路475份/华泰多因子系列5：单因子测试之换手率类因子.pdf`
- 来源页码：`1, 6, 42, 43, 44`

## 复现实现

- Python 实现：`microfactor.factors.document_extended:_compute/doc_huatai5_turn_6m`
- 默认参数：`{"baseline_months":null,"baseline_window":null,"recent_months":6,"recent_window":126}`
- 适配说明：无。

## 发布与评估

- Publication status: `published`
- Evaluation status: `rejected`
- 因子版本：`9692abd739625a5cc9ac`
- 数据快照：`snapshot_e3e73aa97706fd71f27ad486`
- 评估批次：`20260917_231028_ee6693d0`
- 有效区间：`2016-07-08` 至 `2026-09-15`

### 核心指标

- Rank IC Mean：`-0.0233495486144`
- Rank ICIR：`-0.199894690931`
- Adjusted ICIR：`0.199894690931`
- Long-short spread (bps)：`8.60874406175`
- Monotonicity：`0.987878787879`
- Coverage：`0.622808966074`
- Daily turnover (long)：`0.0173360781847`
- Daily turnover (short)：`0.0202602171512`
