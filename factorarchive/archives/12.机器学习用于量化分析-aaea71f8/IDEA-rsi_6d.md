# rsi_6d

## 因子概览

- 类别：`technical`
- 方向：`positive`
- 频率：`1d`
- 最小窗口：`6`
- 复权方式：`hfq`
- 实现状态：`exact`

## 公式

```text
100 - 100/(1 + SMA6(gain)/SMA6(loss))
```

输入字段：`close`

## 原理说明

未提供。

## 来源

- 逻辑来源组：`12.机器学习用于量化分析-aaea71f8`
- 来源组指纹：`aaea71f8581f89cff4654e2f17d972152ca862b2ce2b4c7c1ff757f0d6d98874`
- `2020-2026聚宽600条源码/2025年度精选策略/12.机器学习用于量化分析.txt` — SHA-256 `aaea71f8581f89cff4654e2f17d972152ca862b2ce2b4c7c1ff757f0d6d98874`
  - 归档副本：`../../sources/2020-2026聚宽600条源码/2025年度精选策略/12.机器学习用于量化分析.txt`
- 来源页码：`未记录`

## 复现实现

- Python 实现：`microfactor.factors.document_factors::rsi_6d`
- 默认参数：`{}`
- 适配说明：无。

## 发布与评估

- Publication status: `published`
- Evaluation status: `rejected`
- 因子版本：`a5645d9ea7a31c4bd549`
- 数据快照：`snapshot_e3e73aa97706fd71f27ad486`
- 评估批次：`20260917_231028_ee6693d0`
- 有效区间：`2016-01-12` 至 `2026-09-15`

### 核心指标

- Rank IC Mean：`-0.04020643197`
- Rank ICIR：`-0.333790710691`
- Adjusted ICIR：`-0.333790710691`
- Long-short spread (bps)：`-24.6126147716`
- Monotonicity：`-0.636363636364`
- Coverage：`0.901355684008`
- Daily turnover (long)：`0.438569480489`
- Daily turnover (short)：`0.438664475787`
