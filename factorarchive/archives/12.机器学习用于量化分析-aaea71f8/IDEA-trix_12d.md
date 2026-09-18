# trix_12d

## 因子概览

- 类别：`technical`
- 方向：`positive`
- 频率：`1d`
- 最小窗口：`36`
- 复权方式：`hfq`
- 实现状态：`exact`

## 公式

```text
100*pct_change(EMA12(EMA12(EMA12(close))))
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

- Python 实现：`microfactor.factors.document_factors::trix_12d`
- 默认参数：`{}`
- 适配说明：无。

## 发布与评估

- Publication status: `published`
- Evaluation status: `rejected`
- 因子版本：`2215a1263880e95bf201`
- 数据快照：`snapshot_e3e73aa97706fd71f27ad486`
- 评估批次：`20260917_231028_ee6693d0`
- 有效区间：`2016-02-26` 至 `2026-09-15`

### 核心指标

- Rank IC Mean：`-0.0391137197364`
- Rank ICIR：`-0.311274691301`
- Adjusted ICIR：`-0.311274691301`
- Long-short spread (bps)：`-20.7683483165`
- Monotonicity：`-1`
- Coverage：`0.985395013635`
- Daily turnover (long)：`0.121038740841`
- Daily turnover (short)：`0.0925100726712`
