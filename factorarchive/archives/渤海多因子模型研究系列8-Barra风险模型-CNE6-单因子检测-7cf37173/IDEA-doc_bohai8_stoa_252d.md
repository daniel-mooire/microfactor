# doc_bohai8_stoa_252d

## 因子概览

- 类别：`liquidity`
- 方向：`negative`
- 频率：`1d`
- 最小窗口：`252`
- 复权方式：`none`
- 实现状态：`approximate`

## 公式

```text
ln(sum(turnover_fraction,252)/12)
```

输入字段：`turnover_percent`

## 原理说明

用过去一段时间的价格、成交量或换手率概括股票的交易行为。

## 来源

- 逻辑来源组：`渤海多因子模型研究系列8-Barra风险模型-CNE6-单因子检测-7cf37173`
- 来源组指纹：`7cf37173e8dc79a552b0139bd5f7706c1745b74a9193dad912e25c0a17b4e9c1`
- `JJJ643/量化因子挖掘思路475份/渤海多因子模型研究系列8：Barra风险模型（CNE6）单因子检测.pdf` — SHA-256 `7cf37173e8dc79a552b0139bd5f7706c1745b74a9193dad912e25c0a17b4e9c1`
  - 归档副本：`../../sources/JJJ643/量化因子挖掘思路475份/渤海多因子模型研究系列8：Barra风险模型（CNE6）单因子检测.pdf`
- 来源页码：`7, 19`

## 复现实现

- Python 实现：`microfactor.factors.document_extended:_compute/doc_bohai8_stoa_252d`
- 默认参数：`{"evaluation_sampling":"daily_rolling","source_factor":"STOA","source_months":12,"source_sampling":"monthly","turnover_formula_unit":"fraction","turnover_input_unit":"percentage_points","window_days":252}`
- 适配说明：The report evaluates monthly cross-sections. Microshare exposes turnover as percentage points, so the implementation divides by 100 before applying the report formula and exposes the same trailing 21-day month blocks daily for the common evaluation contract.

## 发布与评估

- Publication status: `published`
- Evaluation status: `rejected`
- 因子版本：`9a229ec7f21a07f070cb`
- 数据快照：`snapshot_e3e73aa97706fd71f27ad486`
- 评估批次：`20260917_231028_ee6693d0`
- 有效区间：`2017-01-12` 至 `2026-09-15`

### 核心指标

- Rank IC Mean：`-0.0166339643067`
- Rank ICIR：`-0.159788266519`
- Adjusted ICIR：`0.159788266519`
- Long-short spread (bps)：`5.15887729729`
- Monotonicity：`0.757575757576`
- Coverage：`0.482166382979`
- Daily turnover (long)：`0.0142613368674`
- Daily turnover (short)：`0.0169854474572`
