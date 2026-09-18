# doc_haitong37_imom1_12m

## 因子概览

- 类别：`momentum`
- 方向：`positive`
- 频率：`1d`
- 最小窗口：`1029`
- 复权方式：`hfq`
- 实现状态：`approximate`

## 公式

```text
sum(epsilon[t-12:t-1])/sqrt(sum((epsilon-mean(epsilon))^2)); epsilon from 36m market-model regression
```

输入字段：`close_total_return_index`

## 原理说明

用过去一段时间的价格、成交量或换手率概括股票的交易行为。

## 来源

- 逻辑来源组：`海通选股因子系列研究37-A股是否存在异质动量效应-2c87c85e`
- 来源组指纹：`2c87c85e608d686eb7f4416885c4e4628673013ca95cd9bef47583b0aa9b9264`
- `JJJ643/量化因子挖掘思路475份/海通选股因子系列研究37：A股是否存在异质动量效应.pdf` — SHA-256 `2c87c85e608d686eb7f4416885c4e4628673013ca95cd9bef47583b0aa9b9264`
  - 归档副本：`../../sources/JJJ643/量化因子挖掘思路475份/海通选股因子系列研究37：A股是否存在异质动量效应.pdf`
- 来源页码：`5, 8`

## 复现实现

- Python 实现：`microfactor.factors.document_extended:_compute/doc_haitong37_imom1_12m`
- 默认参数：`{"momentum_months":12,"regression_months":36}`
- 适配说明：采用报告明确展示的单市场因子 IMom_1 变体；市场收益使用股票池月度等权收益代理，每月信号映射至该月交易日。风险调整公式按报告引用的 Residual Momentum 原始定义补全。

## 发布与评估

- Publication status: `published`
- Evaluation status: `rejected`
- 因子版本：`fd4fc5365e4395280adf`
- 数据快照：`snapshot_e3e73aa97706fd71f27ad486`
- 评估批次：`20260917_231028_ee6693d0`
- 有效区间：`2020-02-03` 至 `2026-09-15`

### 核心指标

- Rank IC Mean：`-0.0212373882082`
- Rank ICIR：`-0.217264308948`
- Adjusted ICIR：`-0.217264308948`
- Long-short spread (bps)：`-4.60195829811`
- Monotonicity：`-0.418181818182`
- Coverage：`0.434832919255`
- Daily turnover (long)：`0.0602563888152`
- Daily turnover (short)：`0.0346440950992`
