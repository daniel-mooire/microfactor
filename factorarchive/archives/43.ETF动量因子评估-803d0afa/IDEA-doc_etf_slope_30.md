# doc_etf_slope_30

## 因子概览

- 类别：`momentum`
- 方向：`positive`
- 频率：`1d`
- 最小窗口：`30`
- 复权方式：`qfq`
- 实现状态：`approximate`

## 公式

```text
100*OLS_slope(C[t-29:t]/C[t-29], 0..29)
```

输入字段：`close`

## 原理说明

用过去一段时间的价格、成交量或换手率概括股票的交易行为。

## 来源

- 逻辑来源组：`43.ETF动量因子评估-803d0afa`
- 来源组指纹：`803d0afa67862c0ab4060ed88de841463120c7d8f26989d4a68c0c5b09d2e057`
- `2020-2026聚宽600条源码/2022年度精选策略/43.ETF动量因子评估.txt` — SHA-256 `803d0afa67862c0ab4060ed88de841463120c7d8f26989d4a68c0c5b09d2e057`
  - 归档副本：`../../sources/2020-2026聚宽600条源码/2022年度精选策略/43.ETF动量因子评估.txt`
- 来源页码：`未记录`

## 复现实现

- Python 实现：`microfactor.factors.document_extended:_compute/doc_etf_slope_30`
- 默认参数：`{}`
- 适配说明：原资料在四只 ETF 上计算归一化收盘价线性回归斜率；当前按同一公式适配为个股日频因子，使用 T 日可见的窗口，并采用 qfq 价格契约。

## 发布与评估

- Publication status: `published`
- Evaluation status: `rejected`
- 因子版本：`476155fadf5cb2fbbe7d`
- 数据快照：`snapshot_e3e73aa97706fd71f27ad486`
- 评估批次：`20260917_231028_ee6693d0`
- 有效区间：`2016-02-19` 至 `2026-09-15`

### 核心指标

- Rank IC Mean：`-0.0412658412165`
- Rank ICIR：`-0.329704573536`
- Adjusted ICIR：`-0.329704573536`
- Long-short spread (bps)：`-22.1135781433`
- Monotonicity：`-0.951515151515`
- Coverage：`0.810980171073`
- Daily turnover (long)：`0.0886348810786`
- Daily turnover (short)：`0.0938983195846`
