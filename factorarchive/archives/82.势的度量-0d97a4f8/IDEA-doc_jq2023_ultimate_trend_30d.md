# doc_jq2023_ultimate_trend_30d

## 因子概览

- 类别：`trend`
- 方向：`positive`
- 频率：`1d`
- 最小窗口：`30`
- 复权方式：`qfq`
- 实现状态：`exact`

## 公式

```text
ultimate_score(normalize_compound(adjusted_close, MA=5), N=29); ultimate_score=absolute_score/N^(3/2)
```

输入字段：`adjusted_close`

## 原理说明

用过去一段时间的价格、成交量或换手率概括股票的交易行为。

## 来源

- 逻辑来源组：`82.势的度量-0d97a4f8`
- 来源组指纹：`0d97a4f872dd4e6c5973b618b9b9a2096d3a21afd49435bacb2ea6a94c4145be`
- `2020-2026聚宽600条源码/2023年度精选策略/82.势的度量.txt` — SHA-256 `0d97a4f872dd4e6c5973b618b9b9a2096d3a21afd49435bacb2ea6a94c4145be`
  - 归档副本：`../../sources/2020-2026聚宽600条源码/2023年度精选策略/82.势的度量.txt`
- 来源页码：`未记录`

## 复现实现

- Python 实现：`microfactor.factors.document_extended:_compute/doc_jq2023_ultimate_trend_30d`
- 默认参数：`{"moving_average_window":5,"normalization":"compound","score":"ultimate","window":30}`
- 适配说明：无。

## 发布与评估

- Publication status: `published`
- Evaluation status: `rejected`
- 因子版本：`3352e49e8902305d88b6`
- 数据快照：`snapshot_e3e73aa97706fd71f27ad486`
- 评估批次：`20260917_231028_ee6693d0`
- 有效区间：`2016-02-19` 至 `2026-09-15`

### 核心指标

- Rank IC Mean：`5.50294906115e-05`
- Rank ICIR：`0.000932496253522`
- Adjusted ICIR：`0.000932496253522`
- Long-short spread (bps)：`-1.44379486443`
- Monotonicity：`-0.551515151515`
- Coverage：`0.810980171073`
- Daily turnover (long)：`0.139519205951`
- Daily turnover (short)：`0.183593557119`
