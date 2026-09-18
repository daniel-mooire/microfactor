# doc_etf_slope_10

## 因子概览

- 类别：`momentum`
- 方向：`positive`
- 频率：`1d`
- 最小窗口：`10`
- 复权方式：`qfq`
- 实现状态：`approximate`

## 公式

```text
100*OLS_slope(C[t-9:t]/C[t-9], 0..9)
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

- Python 实现：`microfactor.factors.document_extended:_compute/doc_etf_slope_10`
- 默认参数：`{}`
- 适配说明：原资料在四只 ETF 上计算归一化收盘价线性回归斜率；当前按同一公式适配为个股日频因子，使用 T 日可见的窗口，并采用 qfq 价格契约。

## 发布与评估

- Publication status: `published`
- Evaluation status: `rejected`
- 因子版本：`29736de446d15c867cae`
- 数据快照：`snapshot_e3e73aa97706fd71f27ad486`
- 评估批次：`20260917_231028_ee6693d0`
- 有效区间：`2016-01-15` 至 `2026-09-15`

### 核心指标

- Rank IC Mean：`-0.0430870041877`
- Rank ICIR：`-0.33996941439`
- Adjusted ICIR：`-0.33996941439`
- Long-short spread (bps)：`-25.8872920127`
- Monotonicity：`-0.587878787879`
- Coverage：`0.88403742284`
- Daily turnover (long)：`0.215776924207`
- Daily turnover (short)：`0.230304455972`
