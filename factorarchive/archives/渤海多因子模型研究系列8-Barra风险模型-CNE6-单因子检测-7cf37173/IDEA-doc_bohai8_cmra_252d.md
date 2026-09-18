# doc_bohai8_cmra_252d

## 因子概览

- 类别：`volatility`
- 方向：`negative`
- 频率：`1d`
- 最小窗口：`253`
- 复权方式：`none`
- 实现状态：`approximate`

## 公式

```text
max_T(sum_{tau=1..T}(ln(1+r_tau)))-min_T(...), T=1..12, 21d/month
```

输入字段：`close_total_return_index`

## 原理说明

用过去一段时间的价格、成交量或换手率概括股票的交易行为。

## 来源

- 逻辑来源组：`渤海多因子模型研究系列8-Barra风险模型-CNE6-单因子检测-7cf37173`
- 来源组指纹：`7cf37173e8dc79a552b0139bd5f7706c1745b74a9193dad912e25c0a17b4e9c1`
- `JJJ643/量化因子挖掘思路475份/渤海多因子模型研究系列8：Barra风险模型（CNE6）单因子检测.pdf` — SHA-256 `7cf37173e8dc79a552b0139bd5f7706c1745b74a9193dad912e25c0a17b4e9c1`
  - 归档副本：`../../sources/JJJ643/量化因子挖掘思路475份/渤海多因子模型研究系列8：Barra风险模型（CNE6）单因子检测.pdf`
- 来源页码：`6, 16, 17`

## 复现实现

- Python 实现：`microfactor.factors.document_extended:_compute/doc_bohai8_cmra_252d`
- 默认参数：`{"evaluation_cross_section":"raw","evaluation_sampling":"daily_rolling","horizons_days":[21,42,63,84,105,126,147,168,189,210,231,252],"months":12,"return_type":"close_total_return","source_cross_section":"industry_and_size_neutralized","source_sampling":"monthly","trading_days_per_month":21}`
- 适配说明：The report evaluates monthly industry- and size-neutralized cross-sections. The implementation preserves the report's twelve 21-trading-day cumulative log-return horizons but exposes the raw trailing range daily for the common evaluation contract.

## 发布与评估

- Publication status: `published`
- Evaluation status: `rejected`
- 因子版本：`404da2ea0139686f45a1`
- 数据快照：`snapshot_e3e73aa97706fd71f27ad486`
- 评估批次：`20260917_231028_ee6693d0`
- 有效区间：`2017-01-13` 至 `2026-09-15`

### 核心指标

- Rank IC Mean：`-0.0146333802356`
- Rank ICIR：`-0.144084611749`
- Adjusted ICIR：`0.144084611749`
- Long-short spread (bps)：`-0.768244233072`
- Monotonicity：`-0.163636363636`
- Coverage：`0.608593869732`
- Daily turnover (long)：`0.239381012631`
- Daily turnover (short)：`0.185641180191`
