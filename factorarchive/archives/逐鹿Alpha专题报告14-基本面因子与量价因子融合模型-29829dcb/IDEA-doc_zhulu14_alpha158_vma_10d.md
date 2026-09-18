# doc_zhulu14_alpha158_vma_10d

## 因子概览

- 类别：`liquidity`
- 方向：`unspecified`
- 频率：`1d`
- 最小窗口：`10`
- 复权方式：`hfq`
- 实现状态：`exact`

## 公式

```text
Mean($volume,10)/($volume+1e-12)
```

输入字段：`volume`

## 原理说明

用过去一段时间的价格、成交量或换手率概括股票的交易行为。

## 来源

- 逻辑来源组：`逐鹿Alpha专题报告14-基本面因子与量价因子融合模型-29829dcb`
- 来源组指纹：`29829dcbc80e322e00b0039b81ec7a08fec83fce344d5b74d284cdf3111ccd93`
- `JJJ643/量化因子挖掘思路475份/逐鹿Alpha专题报告14：基本面因子与量价因子融合模型.pdf` — SHA-256 `29829dcbc80e322e00b0039b81ec7a08fec83fce344d5b74d284cdf3111ccd93`
  - 归档副本：`../../sources/JJJ643/量化因子挖掘思路475份/逐鹿Alpha专题报告14：基本面因子与量价因子融合模型.pdf`
- 来源页码：`5`

## 复现实现

- Python 实现：`microfactor.factors.document_extended:_compute/doc_zhulu14_alpha158_vma_10d`
- 默认参数：`{"window":10}`
- 适配说明：无。

## 发布与评估

- Publication status: `published`
- Evaluation status: `rejected`
- 因子版本：`f115e071ebe3a3ef2853`
- 数据快照：`snapshot_e3e73aa97706fd71f27ad486`
- 评估批次：`20260917_231028_ee6693d0`
- 有效区间：`2016-01-04` 至 `2026-09-15`

### 核心指标

- Rank IC Mean：`0.0302769240144`
- Rank ICIR：`0.355992416316`
- Adjusted ICIR：`0.355992416316`
- Long-short spread (bps)：`12.2069903624`
- Monotonicity：`0.115151515152`
- Coverage：`0.998898500577`
- Daily turnover (long)：`0.537590368317`
- Daily turnover (short)：`0.622090174922`
