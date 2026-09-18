# kdj_j_9d

## 因子概览

- 类别：`technical`
- 方向：`positive`
- 频率：`1d`
- 最小窗口：`9`
- 复权方式：`hfq`
- 实现状态：`exact`

## 公式

```text
J=3*K-2*D; RSV=100*(close-LLV9)/(HHV9-LLV9)
```

输入字段：`high, low, close`

## 原理说明

未提供。

## 来源

- 逻辑来源组：`12.机器学习用于量化分析-aaea71f8`
- 来源组指纹：`aaea71f8581f89cff4654e2f17d972152ca862b2ce2b4c7c1ff757f0d6d98874`
- `2020-2026聚宽600条源码/2025年度精选策略/12.机器学习用于量化分析.txt` — SHA-256 `aaea71f8581f89cff4654e2f17d972152ca862b2ce2b4c7c1ff757f0d6d98874`
  - 归档副本：`../../sources/2020-2026聚宽600条源码/2025年度精选策略/12.机器学习用于量化分析.txt`
- 来源页码：`未记录`

## 复现实现

- Python 实现：`microfactor.factors.document_factors::kdj_j_9d`
- 默认参数：`{}`
- 适配说明：无。

## 发布与评估

- Publication status: `published`
- Evaluation status: `rejected`
- 因子版本：`a77815f0b701821b95cd`
- 数据快照：`snapshot_e3e73aa97706fd71f27ad486`
- 评估批次：`20260917_231028_ee6693d0`
- 有效区间：`2016-01-14` 至 `2026-09-15`

### 核心指标

- Rank IC Mean：`-0.0320320710673`
- Rank ICIR：`-0.300101175472`
- Adjusted ICIR：`-0.300101175472`
- Long-short spread (bps)：`-23.8790869313`
- Monotonicity：`-0.466666666667`
- Coverage：`0.990340917856`
- Daily turnover (long)：`0.523202893912`
- Daily turnover (short)：`0.435248289642`
