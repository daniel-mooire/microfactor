# bollinger_position_20d

## 因子概览

- 类别：`technical`
- 方向：`negative`
- 频率：`1d`
- 最小窗口：`20`
- 复权方式：`hfq`
- 实现状态：`exact`

## 公式

```text
(close-(MA20-2*STD20))/(4*STD20)
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

- Python 实现：`microfactor.factors.document_factors::bollinger_position_20d`
- 默认参数：`{}`
- 适配说明：无。

## 发布与评估

- Publication status: `published`
- Evaluation status: `passed`
- 因子版本：`da387b0ca498f51a9b9e`
- 数据快照：`snapshot_e3e73aa97706fd71f27ad486`
- 评估批次：`20260917_231028_ee6693d0`
- 有效区间：`2016-01-29` 至 `2026-09-15`

### 核心指标

- Rank IC Mean：`-0.0499674918738`
- Rank ICIR：`-0.382639664695`
- Adjusted ICIR：`0.382639664695`
- Long-short spread (bps)：`27.2816923947`
- Monotonicity：`0.478787878788`
- Coverage：`0.843429899303`
- Daily turnover (long)：`0.363684902526`
- Daily turnover (short)：`0.427782048819`
