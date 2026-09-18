# doc_zhulu14_alpha158_corr_10d

## 因子概览

- 类别：`price_volume`
- 方向：`unspecified`
- 频率：`1d`
- 最小窗口：`10`
- 复权方式：`hfq`
- 实现状态：`exact`

## 公式

```text
Corr($close,Log($volume+1),10)
```

输入字段：`close, volume`

## 原理说明

用过去一段时间的价格、成交量或换手率概括股票的交易行为。

## 来源

- 逻辑来源组：`逐鹿Alpha专题报告14-基本面因子与量价因子融合模型-29829dcb`
- 来源组指纹：`29829dcbc80e322e00b0039b81ec7a08fec83fce344d5b74d284cdf3111ccd93`
- `JJJ643/量化因子挖掘思路475份/逐鹿Alpha专题报告14：基本面因子与量价因子融合模型.pdf` — SHA-256 `29829dcbc80e322e00b0039b81ec7a08fec83fce344d5b74d284cdf3111ccd93`
  - 归档副本：`../../sources/JJJ643/量化因子挖掘思路475份/逐鹿Alpha专题报告14：基本面因子与量价因子融合模型.pdf`
- 来源页码：`5`

## 复现实现

- Python 实现：`microfactor.factors.document_extended:_compute/doc_zhulu14_alpha158_corr_10d`
- 默认参数：`{"correlation":"pearson","window":10}`
- 适配说明：无。

## 发布与评估

- Publication status: `published`
- Evaluation status: `rejected`
- 因子版本：`0ced24fb0be6ae5d12d5`
- 数据快照：`snapshot_e3e73aa97706fd71f27ad486`
- 评估批次：`20260917_231028_ee6693d0`
- 有效区间：`2016-01-05` 至 `2026-09-15`

### 核心指标

- Rank IC Mean：`-0.0401106043092`
- Rank ICIR：`-0.489254173063`
- Adjusted ICIR：`-0.489254173063`
- Long-short spread (bps)：`-13.6384892551`
- Monotonicity：`-0.963636363636`
- Coverage：`0.994387692308`
- Daily turnover (long)：`0.348309784805`
- Daily turnover (short)：`0.35109885543`
