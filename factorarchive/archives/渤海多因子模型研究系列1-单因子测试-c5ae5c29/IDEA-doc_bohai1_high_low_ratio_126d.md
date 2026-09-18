# doc_bohai1_high_low_ratio_126d

## 因子概览

- 类别：`volatility`
- 方向：`negative`
- 频率：`1d`
- 最小窗口：`126`
- 复权方式：`qfq`
- 实现状态：`approximate`

## 公式

```text
MAX(adjusted_high,126)/MIN(adjusted_low,126)
```

输入字段：`high, low`

## 原理说明

用过去一段时间的价格、成交量或换手率概括股票的交易行为。

## 来源

- 逻辑来源组：`渤海多因子模型研究系列1-单因子测试-c5ae5c29`
- 来源组指纹：`c5ae5c29e21e52e7c6c8d283c718f29cdb7e41cc5ed4eb08effb26b0ffebde75`
- `JJJ643/量化因子挖掘思路475份/渤海多因子模型研究系列1：单因子测试.pdf` — SHA-256 `c5ae5c29e21e52e7c6c8d283c718f29cdb7e41cc5ed4eb08effb26b0ffebde75`
  - 归档副本：`../../sources/JJJ643/量化因子挖掘思路475份/渤海多因子模型研究系列1：单因子测试.pdf`
- 来源页码：`7, 24`

## 复现实现

- Python 实现：`microfactor.factors.document_extended:_compute/doc_bohai1_high_low_ratio_126d`
- 默认参数：`{"evaluation_sampling":"daily_rolling","source_months":6,"source_sampling":"month_end","window_days":126}`
- 适配说明：The report evaluates the factor at month-end. The implementation uses the report's 21/63/126/252 trading-day month mapping and exposes the same trailing high/low ratio daily for the common evaluation contract. The source does not pin price adjustment, so qfq is used.

## 发布与评估

- Publication status: `published`
- Evaluation status: `rejected`
- 因子版本：`4cd1fa3a571254a013bb`
- 数据快照：`snapshot_e3e73aa97706fd71f27ad486`
- 评估批次：`20260917_231028_ee6693d0`
- 有效区间：`2016-07-08` 至 `2026-09-15`

### 核心指标

- Rank IC Mean：`-0.0252386237214`
- Rank ICIR：`-0.187426236863`
- Adjusted ICIR：`0.187426236863`
- Long-short spread (bps)：`3.93230210543`
- Monotonicity：`0.575757575758`
- Coverage：`0.622815831987`
- Daily turnover (long)：`0.0365418574696`
- Daily turnover (short)：`0.0384508346846`
