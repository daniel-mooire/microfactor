# doc_bohai8_stom_21d

## 因子概览

- 类别：`liquidity`
- 方向：`negative`
- 频率：`1d`
- 最小窗口：`21`
- 复权方式：`none`
- 实现状态：`approximate`

## 公式

```text
ln(sum(turnover_fraction,21)/1)
```

输入字段：`turnover_percent`

## 原理说明

用过去一段时间的价格、成交量或换手率概括股票的交易行为。

## 来源

- 逻辑来源组：`渤海多因子模型研究系列8-Barra风险模型-CNE6-单因子检测-7cf37173`
- 来源组指纹：`7cf37173e8dc79a552b0139bd5f7706c1745b74a9193dad912e25c0a17b4e9c1`
- `JJJ643/量化因子挖掘思路475份/渤海多因子模型研究系列8：Barra风险模型（CNE6）单因子检测.pdf` — SHA-256 `7cf37173e8dc79a552b0139bd5f7706c1745b74a9193dad912e25c0a17b4e9c1`
  - 归档副本：`../../sources/JJJ643/量化因子挖掘思路475份/渤海多因子模型研究系列8：Barra风险模型（CNE6）单因子检测.pdf`
- 来源页码：`6, 19`

## 复现实现

- Python 实现：`microfactor.factors.document_extended:_compute/doc_bohai8_stom_21d`
- 默认参数：`{"evaluation_sampling":"daily_rolling","source_factor":"STOM","source_months":1,"source_sampling":"monthly","turnover_formula_unit":"fraction","turnover_input_unit":"percentage_points","window_days":21}`
- 适配说明：The report evaluates monthly cross-sections. Microshare exposes turnover as percentage points, so the implementation divides by 100 before applying the report formula and exposes the same trailing 21-day month blocks daily for the common evaluation contract.

## 发布与评估

- Publication status: `published`
- Evaluation status: `passed`
- 因子版本：`220cd97d52ba29106c85`
- 数据快照：`snapshot_e3e73aa97706fd71f27ad486`
- 评估批次：`20260917_231028_ee6693d0`
- 有效区间：`2016-02-01` 至 `2026-09-15`

### 核心指标

- Rank IC Mean：`-0.0427859113952`
- Rank ICIR：`-0.317102085207`
- Adjusted ICIR：`0.317102085207`
- Long-short spread (bps)：`16.0516609039`
- Monotonicity：`0.987878787879`
- Coverage：`0.839972491282`
- Daily turnover (long)：`0.0427193861546`
- Daily turnover (short)：`0.0492983801931`
