# salience_20d

## 因子概览

- 类别：`behavioral`
- 方向：`reversal`
- 频率：`1d`
- 最小窗口：`58`
- 复权方式：`hfq`
- 实现状态：`approximate`

## 公式

```text
cov20(weight20(salience), return); weight=0.7^rank / mean20(0.7^rank)
```

输入字段：`close, pre_close`

## 原理说明

未提供。

## 来源

- 逻辑来源组：`90.-复现-凸显度因子-7ad18e92`
- 来源组指纹：`7ad18e923eafb60adef1a9d7f7fb88cd1b9777e58089d026519694edcd277377`
- `2020-2026聚宽600条源码/2024年度精选策略1/90.【复现】凸显度因子.txt` — SHA-256 `7ad18e923eafb60adef1a9d7f7fb88cd1b9777e58089d026519694edcd277377`
  - 归档副本：`../../sources/2020-2026聚宽600条源码/2024年度精选策略1/90.【复现】凸显度因子.txt`
- 来源页码：`未记录`

## 复现实现

- Python 实现：`microfactor.factors.document_factors::salience_20d`
- 默认参数：`{}`
- 适配说明：The original benchmark return is unavailable; the point-in-time cross-sectional mean return is used.

## 发布与评估

- Publication status: `published`
- Evaluation status: `passed`
- 因子版本：`afc302a621e2fbf1a074`
- 数据快照：`snapshot_e3e73aa97706fd71f27ad486`
- 评估批次：`20260917_231028_ee6693d0`
- 有效区间：`2016-03-30` 至 `2026-09-15`

### 核心指标

- Rank IC Mean：`-0.0566432747825`
- Rank ICIR：`-0.635337091966`
- Adjusted ICIR：`0.635337091966`
- Long-short spread (bps)：`30.0516238124`
- Monotonicity：`0.987878787879`
- Coverage：`0.843196540881`
- Daily turnover (long)：`0.190833650953`
- Daily turnover (short)：`0.148407228189`
