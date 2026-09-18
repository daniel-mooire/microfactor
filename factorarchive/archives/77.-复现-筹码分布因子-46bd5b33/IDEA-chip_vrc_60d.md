# chip_vrc_60d

## 因子概览

- 类别：`microstructure`
- 方向：`negative`
- 频率：`1d`
- 最小窗口：`61`
- 复权方式：`hfq`
- 实现状态：`approximate`

## 公式

```text
sum(n*TR_W_n*(RC_n-ARC)^2)/(n-1)
```

输入字段：`vwap, turnover_rate`

## 原理说明

未提供。

## 来源

- 逻辑来源组：`77.-复现-筹码分布因子-46bd5b33`
- 来源组指纹：`46bd5b33db08d587a0887ea9af57c944677a65ebba14ac824ae3902d6307b427`
- `2020-2026聚宽600条源码/2024年度精选策略1/77.【复现】筹码分布因子.txt` — SHA-256 `46bd5b33db08d587a0887ea9af57c944677a65ebba14ac824ae3902d6307b427`
  - 归档副本：`../../sources/2020-2026聚宽600条源码/2024年度精选策略1/77.【复现】筹码分布因子.txt`
- 来源页码：`未记录`

## 复现实现

- Python 实现：`microfactor.factors.document_factors::chip_vrc_60d`
- 默认参数：`{}`
- 适配说明：Uses the documented turnover-decay proxy, not the unavailable CYQ triangle engine.

## 发布与评估

- Publication status: `published`
- Evaluation status: `rejected`
- 因子版本：`181099d0b4245413f801`
- 数据快照：`snapshot_e3e73aa97706fd71f27ad486`
- 评估批次：`20260917_231028_ee6693d0`
- 有效区间：`2016-04-05` 至 `2026-09-15`

### 核心指标

- Rank IC Mean：`-0.000918043567371`
- Rank ICIR：`-0.00826322151467`
- Adjusted ICIR：`0.00826322151467`
- Long-short spread (bps)：`-6.29398265785`
- Monotonicity：`-0.975757575758`
- Coverage：`0.73381227863`
- Daily turnover (long)：`0.0616895395287`
- Daily turnover (short)：`0.0616835035373`
