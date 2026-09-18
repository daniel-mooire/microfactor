# doc_haitong15_mean_top5_return_monthly

## 因子概览

- 类别：`lottery`
- 方向：`negative`
- 频率：`1d`
- 最小窗口：`31`
- 复权方式：`hfq`
- 实现状态：`approximate`

## 公式

```text
mean(largest 5 daily close-to-close returns in previous calendar month)
```

输入字段：`close_to_close_total_return_1d`

## 原理说明

用过去一段时间的价格、成交量或换手率概括股票的交易行为。

## 来源

- 逻辑来源组：`海通选股因子系列研究15-博彩型-股票的预期收益-1a86ed21`
- 来源组指纹：`1a86ed21a9e36e9270880c9919081401dc1daeab3e05b1f5c9e53119bfc60427`
- `JJJ643/量化因子挖掘思路475份/海通选股因子系列研究15：“博彩型”股票的预期收益.pdf` — SHA-256 `1a86ed21a9e36e9270880c9919081401dc1daeab3e05b1f5c9e53119bfc60427`
  - 归档副本：`../../sources/JJJ643/量化因子挖掘思路475份/海通选股因子系列研究15：“博彩型”股票的预期收益.pdf`
- 来源页码：`5, 6`

## 复现实现

- Python 实现：`microfactor.factors.document_extended:_compute/doc_haitong15_mean_top5_return_monthly`
- 默认参数：`{"formation_period":"previous_calendar_month","top_n":5}`
- 适配说明：原报告仅在月末形成信号并持有一个月；当前严格按自然月聚合前5大日收益，将上月末形成值映射到下一自然月交易日供统一日频评估。

## 发布与评估

- Publication status: `published`
- Evaluation status: `rejected`
- 因子版本：`3cd691784fd34ee3e737`
- 数据快照：`snapshot_e3e73aa97706fd71f27ad486`
- 评估批次：`20260917_231028_ee6693d0`
- 有效区间：`2016-02-01` 至 `2026-09-15`

### 核心指标

- Rank IC Mean：`-0.0291125363964`
- Rank ICIR：`-0.255269888795`
- Adjusted ICIR：`0.255269888795`
- Long-short spread (bps)：`6.86702182127`
- Monotonicity：`0.393939393939`
- Coverage：`0.957928322356`
- Daily turnover (long)：`0.113803922755`
- Daily turnover (short)：`0.066115467598`
