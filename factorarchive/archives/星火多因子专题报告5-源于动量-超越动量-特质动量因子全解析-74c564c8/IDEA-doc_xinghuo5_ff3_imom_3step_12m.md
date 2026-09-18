# doc_xinghuo5_ff3_imom_3step_12m

## 因子概览

- 类别：`momentum`
- 方向：`positive`
- 频率：`1d`
- 最小窗口：`1029`
- 复权方式：`hfq`
- 实现状态：`approximate`

## 公式

```text
(prod(1+epsilon[t-12:t-1])-1)/(sqrt(12)*std(epsilon[t-12:t-1])); epsilon from rolling 36m no-intercept FF3 exposure
```

输入字段：`close_total_return_index, total_mv, pb, is_suspended`

## 原理说明

用过去一段时间的价格、成交量或换手率概括股票的交易行为。

## 来源

- 逻辑来源组：`星火多因子专题报告5-源于动量-超越动量-特质动量因子全解析-74c564c8`
- 来源组指纹：`74c564c8dca402dac3c4d0c24ad8e290eefd2b6f6b2daee62be643fed9bf4f92`
- `JJJ643/量化因子挖掘思路475份/星火多因子专题报告5：源于动量，超越动量，特质动量因子全解析.pdf` — SHA-256 `74c564c8dca402dac3c4d0c24ad8e290eefd2b6f6b2daee62be643fed9bf4f92`
  - 归档副本：`../../sources/JJJ643/量化因子挖掘思路475份/星火多因子专题报告5：源于动量，超越动量，特质动量因子全解析.pdf`
- 来源页码：`12, 18, 19, 21`

## 复现实现

- Python 实现：`microfactor.factors.document_extended:_compute/doc_xinghuo5_ff3_imom_3step_12m`
- 默认参数：`{"include_intercept":false,"minimum_momentum_months":3,"minimum_monthly_trading_days":10,"momentum_months":12,"regression_months":36}`
- 适配说明：按报告50%市值与30/40/30账面市值比分组、市值加权构造月度FF3；当前用点时total_mv与BP=1/pb，在可用股票面板内构造MKT/SMB/HML，月度信号映射到下一形成月内的交易日。

## 发布与评估

- Publication status: `published`
- Evaluation status: `rejected`
- 因子版本：`1faaa5a94c8646cf3716`
- 数据快照：`snapshot_e3e73aa97706fd71f27ad486`
- 评估批次：`20260917_231028_ee6693d0`
- 有效区间：`2019-04-01` 至 `2026-09-15`

### 核心指标

- Rank IC Mean：`-0.0135535240414`
- Rank ICIR：`-0.16269461556`
- Adjusted ICIR：`-0.16269461556`
- Long-short spread (bps)：`-4.42007937475`
- Monotonicity：`-0.793939393939`
- Coverage：`0.912895695364`
- Daily turnover (long)：`0.0624202936509`
- Daily turnover (short)：`0.0350355780611`
