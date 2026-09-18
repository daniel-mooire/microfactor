# doc_haitong12_price_turn_corr_10d

## 因子概览

- 类别：`price_volume`
- 方向：`negative`
- 频率：`1d`
- 最小窗口：`10`
- 复权方式：`hfq`
- 实现状态：`exact`

## 公式

```text
CORR(adjusted_close, turnover_percent, 10)
```

输入字段：`adjusted_close, turnover_percent`

## 原理说明

用过去一段时间的价格、成交量或换手率概括股票的交易行为。

## 来源

- 逻辑来源组：`海通选股因子系列研究12-量-与-价-的结合-905efca3`
- 来源组指纹：`905efca3c8b04870074e3a90a0c46f185f46ec58fb663dfee03d70faf28646b0`
- `JJJ643/量化因子挖掘思路475份/海通选股因子系列研究12：“量”与“价”的结合.pdf` — SHA-256 `905efca3c8b04870074e3a90a0c46f185f46ec58fb663dfee03d70faf28646b0`
  - 归档副本：`../../sources/JJJ643/量化因子挖掘思路475份/海通选股因子系列研究12：“量”与“价”的结合.pdf`
- 来源页码：`5, 6`

## 复现实现

- Python 实现：`microfactor.factors.document_extended:_compute/doc_haitong12_price_turn_corr_10d`
- 默认参数：`{"correlation":"pearson","window":10}`
- 适配说明：无。

## 发布与评估

- Publication status: `published`
- Evaluation status: `passed`
- 因子版本：`9e0d3bec7522a15008b1`
- 数据快照：`snapshot_e3e73aa97706fd71f27ad486`
- 评估批次：`20260917_231028_ee6693d0`
- 有效区间：`2016-01-15` 至 `2026-09-15`

### 核心指标

- Rank IC Mean：`-0.0441523681778`
- Rank ICIR：`-0.526047063877`
- Adjusted ICIR：`0.526047063877`
- Long-short spread (bps)：`17.4078878528`
- Monotonicity：`1`
- Coverage：`0.884021604938`
- Daily turnover (long)：`0.323418761557`
- Daily turnover (short)：`0.327127512736`
