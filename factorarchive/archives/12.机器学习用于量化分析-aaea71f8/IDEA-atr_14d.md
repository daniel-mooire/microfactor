# atr_14d

## 因子概览

- 类别：`technical`
- 方向：`negative`
- 频率：`1d`
- 最小窗口：`14`
- 复权方式：`hfq`
- 实现状态：`exact`

## 公式

```text
SMA14(max(high-low, abs(high-Ref(close,1)), abs(low-Ref(close,1))))
```

输入字段：`high, low, close, pre_close`

## 原理说明

未提供。

## 来源

- 逻辑来源组：`12.机器学习用于量化分析-aaea71f8`
- 来源组指纹：`aaea71f8581f89cff4654e2f17d972152ca862b2ce2b4c7c1ff757f0d6d98874`
- `2020-2026聚宽600条源码/2025年度精选策略/12.机器学习用于量化分析.txt` — SHA-256 `aaea71f8581f89cff4654e2f17d972152ca862b2ce2b4c7c1ff757f0d6d98874`
  - 归档副本：`../../sources/2020-2026聚宽600条源码/2025年度精选策略/12.机器学习用于量化分析.txt`
- 来源页码：`未记录`

## 复现实现

- Python 实现：`microfactor.factors.document_factors::atr_14d`
- 默认参数：`{}`
- 适配说明：无。

## 发布与评估

- Publication status: `published`
- Evaluation status: `passed`
- 因子版本：`6657d1aa5685a5798921`
- 数据快照：`snapshot_e3e73aa97706fd71f27ad486`
- 评估批次：`20260917_231028_ee6693d0`
- 有效区间：`2016-01-21` 至 `2026-09-15`

### 核心指标

- Rank IC Mean：`-0.0391420615888`
- Rank ICIR：`-0.443299433751`
- Adjusted ICIR：`0.443299433751`
- Long-short spread (bps)：`13.8428177702`
- Monotonicity：`0.987878787879`
- Coverage：`0.866644899536`
- Daily turnover (long)：`0.0478886162884`
- Daily turnover (short)：`0.068326160075`
