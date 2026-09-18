# doc_huatai_std_return_1

## 因子概览

- 类别：`volatility`
- 方向：`unspecified`
- 频率：`1d`
- 最小窗口：`21`
- 复权方式：`hfq`
- 实现状态：`exact`

## 公式

```text
STD(return,21)
```

输入字段：`close_to_close_total_return_1d`

## 原理说明

用过去一段时间的价格、成交量或换手率概括股票的交易行为。

## 来源

- 逻辑来源组：`华泰多因子系列基础换手率与波动率因子-a280d26b`
- 来源组指纹：`a280d26bc424b0eecfa985bfebf14a4a4a6d02c7e992eed3593ac476b1d20edc`
- `JJJ643/量化因子挖掘思路475份/华泰多因子系列6：单因子测试之波动率类因子.pdf` — SHA-256 `0e33094604f770bf8116b0006d1cfa16e70148b0b958ff9031aede526293ec78`
  - 归档副本：`../../sources/JJJ643/量化因子挖掘思路475份/华泰多因子系列6：单因子测试之波动率类因子.pdf`
- 来源页码：`未记录`

## 复现实现

- Python 实现：`microfactor.factors.document_extended:_compute/doc_huatai_std_return_1`
- 默认参数：`{}`
- 适配说明：无。

## 发布与评估

- Publication status: `published`
- Evaluation status: `rejected`
- 因子版本：`c5c7c67f816f4f33e780`
- 数据快照：`snapshot_e3e73aa97706fd71f27ad486`
- 评估批次：`20260917_231028_ee6693d0`
- 有效区间：`2016-02-02` 至 `2026-09-15`

### 核心指标

- Rank IC Mean：`-0.0534837920244`
- Rank ICIR：`-0.385854597602`
- Adjusted ICIR：`-0.385854597602`
- Long-short spread (bps)：`-17.0781517563`
- Monotonicity：`-0.551515151515`
- Coverage：`0.836594186047`
- Daily turnover (long)：`0.0943226591984`
- Daily turnover (short)：`0.11456454391`
