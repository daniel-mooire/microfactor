# doc_sp

## 因子概览

- 类别：`value`
- 方向：`positive`
- 频率：`1d`
- 最小窗口：`1`
- 复权方式：`none`
- 实现状态：`exact`

## 公式

```text
1/ps_ttm
```

输入字段：`ps_ttm`

## 原理说明

用过去一段时间的价格、成交量或换手率概括股票的交易行为。

## 来源

- 逻辑来源组：`华泰多因子系列2-单因子测试之估值类因子-9277b8bc`
- 来源组指纹：`9277b8bc329a0057a0b96249c3108b6ccfff36023e4ecee5638078edc6fab5dc`
- `JJJ643/量化因子挖掘思路475份/华泰多因子系列2：单因子测试之估值类因子.pdf` — SHA-256 `9277b8bc329a0057a0b96249c3108b6ccfff36023e4ecee5638078edc6fab5dc`
  - 归档副本：`../../sources/JJJ643/量化因子挖掘思路475份/华泰多因子系列2：单因子测试之估值类因子.pdf`
- 来源页码：`1, 5, 11`

## 复现实现

- Python 实现：`microfactor.factors.document_extended:_compute/doc_sp`
- 默认参数：`{}`
- 适配说明：无。

## 发布与评估

- Publication status: `published`
- Evaluation status: `rejected`
- 因子版本：`bc5d415735f3278af70e`
- 数据快照：`snapshot_e3e73aa97706fd71f27ad486`
- 评估批次：`20260917_231028_ee6693d0`
- 有效区间：`2016-01-04` 至 `2026-09-15`

### 核心指标

- Rank IC Mean：`0.0175825862343`
- Rank ICIR：`0.234345258863`
- Adjusted ICIR：`0.234345258863`
- Long-short spread (bps)：`6.57361242752`
- Monotonicity：`0.975757575758`
- Coverage：`0.998202229912`
- Daily turnover (long)：`0.041533846004`
- Daily turnover (short)：`0.0642283779647`
