# doc_zhulu14_alpha158_rsqr_10d

## 因子概览

- 类别：`trend`
- 方向：`unspecified`
- 频率：`1d`
- 最小窗口：`10`
- 复权方式：`hfq`
- 实现状态：`exact`

## 公式

```text
Rsquare($close,10)
```

输入字段：`close`

## 原理说明

用过去一段时间的价格、成交量或换手率概括股票的交易行为。

## 来源

- 逻辑来源组：`逐鹿Alpha专题报告14-基本面因子与量价因子融合模型-29829dcb`
- 来源组指纹：`29829dcbc80e322e00b0039b81ec7a08fec83fce344d5b74d284cdf3111ccd93`
- `JJJ643/量化因子挖掘思路475份/逐鹿Alpha专题报告14：基本面因子与量价因子融合模型.pdf` — SHA-256 `29829dcbc80e322e00b0039b81ec7a08fec83fce344d5b74d284cdf3111ccd93`
  - 归档副本：`../../sources/JJJ643/量化因子挖掘思路475份/逐鹿Alpha专题报告14：基本面因子与量价因子融合模型.pdf`
- 来源页码：`4`

## 复现实现

- Python 实现：`microfactor.factors.document_extended:_compute/doc_zhulu14_alpha158_rsqr_10d`
- 默认参数：`{"window":10}`
- 适配说明：无。

## 发布与评估

- Publication status: `published`
- Evaluation status: `rejected`
- 因子版本：`5fde7db5fa10f578c561`
- 数据快照：`snapshot_e3e73aa97706fd71f27ad486`
- 评估批次：`20260917_231028_ee6693d0`
- 有效区间：`2016-01-05` 至 `2026-09-15`

### 核心指标

- Rank IC Mean：`-0.00232786332519`
- Rank ICIR：`-0.0260110882806`
- Adjusted ICIR：`-0.0260110882806`
- Long-short spread (bps)：`-4.26811266653`
- Monotonicity：`-0.878787878788`
- Coverage：`0.994387692308`
- Daily turnover (long)：`0.42973315969`
- Daily turnover (short)：`0.684978328405`
