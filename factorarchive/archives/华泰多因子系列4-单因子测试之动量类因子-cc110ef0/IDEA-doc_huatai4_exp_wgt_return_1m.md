# doc_huatai4_exp_wgt_return_1m

## 因子概览

- 类别：`momentum`
- 方向：`negative`
- 频率：`1d`
- 最小窗口：`21`
- 复权方式：`none`
- 实现状态：`exact`

## 公式

```text
sum(return*turnover*exp(-x/months/4),window)/sum(turnover*exp(-x/months/4),window)
```

输入字段：`close_to_close_total_return_1d, turnover_percent`

## 原理说明

用过去一段时间的价格、成交量或换手率概括股票的交易行为。

## 来源

- 逻辑来源组：`华泰多因子系列4-单因子测试之动量类因子-cc110ef0`
- 来源组指纹：`cc110ef024e02077528d3c5715af610b110d831c769ecf30e8a308a859f0c76a`
- `JJJ643/量化因子挖掘思路475份/华泰多因子系列4：单因子测试之动量类因子.pdf` — SHA-256 `cc110ef024e02077528d3c5715af610b110d831c769ecf30e8a308a859f0c76a`
  - 归档副本：`../../sources/JJJ643/量化因子挖掘思路475份/华泰多因子系列4：单因子测试之动量类因子.pdf`
- 来源页码：`1, 6, 40, 42, 43`

## 复现实现

- Python 实现：`microfactor.factors.document_extended:_compute/doc_huatai4_exp_wgt_return_1m`
- 默认参数：`{"distance_unit":"trading_day","minimum_valid_days":21,"months":1,"weight":"turnover_percent*exp(-x/months/4)","window_days":21}`
- 适配说明：无。

## 发布与评估

- Publication status: `published`
- Evaluation status: `passed`
- 因子版本：`7c0b1a6734424653f863`
- 数据快照：`snapshot_e3e73aa97706fd71f27ad486`
- 评估批次：`20260917_231028_ee6693d0`
- 有效区间：`2016-02-02` 至 `2026-09-15`

### 核心指标

- Rank IC Mean：`-0.0576351877307`
- Rank ICIR：`-0.454305230594`
- Adjusted ICIR：`0.454305230594`
- Long-short spread (bps)：`30.6321786862`
- Monotonicity：`0.745454545455`
- Coverage：`0.836581782946`
- Daily turnover (long)：`0.32129041655`
- Daily turnover (short)：`0.423715102116`
