# coin_team_intraday

## 因子概览

- 类别：`behavioral`
- 方向：`reversal`
- 频率：`1d`
- 最小窗口：`20`
- 复权方式：`hfq`
- 实现状态：`exact`

## 公式

```text
mean20(close/open-1) with low-volatility and low-turnover sign flips
```

输入字段：`open, close, turnover_rate`

## 原理说明

未提供。

## 来源

- 逻辑来源组：`75.-复现-个股动量效应的识别及球队硬币因子-332bb89e`
- 来源组指纹：`332bb89efd664a20d5d7ec86ac0a814c73d693a396aac9834b2201e3af56f820`
- `2020-2026聚宽600条源码/2024年度精选策略1/75.【复现】个股动量效应的识别及球队硬币因子.txt` — SHA-256 `332bb89efd664a20d5d7ec86ac0a814c73d693a396aac9834b2201e3af56f820`
  - 归档副本：`../../sources/2020-2026聚宽600条源码/2024年度精选策略1/75.【复现】个股动量效应的识别及球队硬币因子.txt`
- 来源页码：`未记录`

## 复现实现

- Python 实现：`microfactor.factors.document_factors::coin_team_intraday`
- 默认参数：`{}`
- 适配说明：The paper computes monthly-end values; this implementation emits the daily rolling value.

## 发布与评估

- Publication status: `published`
- Evaluation status: `passed`
- 因子版本：`af59c8819e6b6268cd90`
- 数据快照：`snapshot_e3e73aa97706fd71f27ad486`
- 评估批次：`20260917_231028_ee6693d0`
- 有效区间：`2016-02-01` 至 `2026-09-15`

### 核心指标

- Rank IC Mean：`-0.044481369232`
- Rank ICIR：`-0.560240386205`
- Adjusted ICIR：`0.560240386205`
- Long-short spread (bps)：`24.3189738237`
- Monotonicity：`0.987878787879`
- Coverage：`0.839972491282`
- Daily turnover (long)：`0.230040755656`
- Daily turnover (short)：`0.176352959934`
