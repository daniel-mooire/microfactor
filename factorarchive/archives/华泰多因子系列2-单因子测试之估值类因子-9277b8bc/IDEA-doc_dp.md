# doc_dp

## 因子概览

- 类别：`value`
- 方向：`positive`
- 频率：`1d`
- 最小窗口：`1`
- 复权方式：`none`
- 实现状态：`exact`

## 公式

```text
dv_ttm
```

输入字段：`dv_ttm`

## 原理说明

用过去一段时间的价格、成交量或换手率概括股票的交易行为。

## 来源

- 逻辑来源组：`华泰多因子系列2-单因子测试之估值类因子-9277b8bc`
- 来源组指纹：`9277b8bc329a0057a0b96249c3108b6ccfff36023e4ecee5638078edc6fab5dc`
- `JJJ643/量化因子挖掘思路475份/华泰多因子系列2：单因子测试之估值类因子.pdf` — SHA-256 `9277b8bc329a0057a0b96249c3108b6ccfff36023e4ecee5638078edc6fab5dc`
  - 归档副本：`../../sources/JJJ643/量化因子挖掘思路475份/华泰多因子系列2：单因子测试之估值类因子.pdf`
- 来源页码：`1, 5, 11`

## 复现实现

- Python 实现：`microfactor.factors.document_extended:_compute/doc_dp`
- 默认参数：`{}`
- 适配说明：无。

## 发布与评估

- Publication status: `published`
- Evaluation status: `rejected`
- 因子版本：`b7cbc52891f870b3d922`
- 数据快照：`snapshot_e3e73aa97706fd71f27ad486`
- 评估批次：`20260917_231028_ee6693d0`
- 有效区间：`2016-01-04` 至 `2026-09-15`

### 核心指标

- Rank IC Mean：`0.0151569483308`
- Rank ICIR：`0.197649709873`
- Adjusted ICIR：`0.197649709873`
- Long-short spread (bps)：`4.10361866791`
- Monotonicity：`0.830303030303`
- Coverage：`0.592528258362`
- Daily turnover (long)：`0.0464445221324`
- Daily turnover (short)：`0.0466952103298`
