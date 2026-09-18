# doc_williams_r_15

## 因子概览

- 类别：`reversal`
- 方向：`negative`
- 频率：`1d`
- 最小窗口：`15`
- 复权方式：`hfq`
- 实现状态：`exact`

## 公式

```text
-100*(HHV(H,15)-C)/(HHV(H,15)-LLV(L,15))
```

输入字段：`high, low, close`

## 原理说明

通过价格和成交量的历史变化，概括趋势、波动或买卖力量。

## 来源

- 逻辑来源组：`广发多因子系列42-海量技术指标掘金Alpha因子-ebb746e4`
- 来源组指纹：`ebb746e4e36034e7bb654e15858c111028f0e23b67ecbaa72ca1d3677bba07bc`
- `JJJ643/量化因子挖掘思路475份/广发多因子系列42：海量技术指标掘金Alpha因子.pdf` — SHA-256 `ebb746e4e36034e7bb654e15858c111028f0e23b67ecbaa72ca1d3677bba07bc`
  - 归档副本：`../../sources/JJJ643/量化因子挖掘思路475份/广发多因子系列42：海量技术指标掘金Alpha因子.pdf`
- 来源页码：`未记录`

## 复现实现

- Python 实现：`microfactor.factors.document_indicators::doc_williams_r_15`
- 默认参数：`{}`
- 适配说明：无。

## 发布与评估

- Publication status: `published`
- Evaluation status: `passed`
- 因子版本：`9a1be4bde80b87ae0815`
- 数据快照：`snapshot_e3e73aa97706fd71f27ad486`
- 评估批次：`20260917_231028_ee6693d0`
- 有效区间：`2016-01-22` 至 `2026-09-15`

### 核心指标

- Rank IC Mean：`-0.0372068062604`
- Rank ICIR：`-0.300139603504`
- Adjusted ICIR：`0.300139603504`
- Long-short spread (bps)：`26.9635972356`
- Monotonicity：`0.393939393939`
- Coverage：`0.862514495555`
- Daily turnover (long)：`0.436136006376`
- Daily turnover (short)：`0.525283665201`
