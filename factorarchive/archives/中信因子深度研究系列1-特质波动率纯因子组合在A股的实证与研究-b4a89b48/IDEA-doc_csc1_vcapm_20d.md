# doc_csc1_vcapm_20d

## 因子概览

- 类别：`volatility`
- 方向：`negative`
- 频率：`1d`
- 最小窗口：`20`
- 复权方式：`hfq`
- 实现状态：`approximate`

## 公式

```text
sqrt(252)*STD20(residual of r_i on market return)
```

输入字段：`close_to_close_total_return_1d`

## 原理说明

用过去一段时间的价格、成交量或换手率概括股票的交易行为。

## 来源

- 逻辑来源组：`中信因子深度研究系列1-特质波动率纯因子组合在A股的实证与研究-b4a89b48`
- 来源组指纹：`b4a89b481293b596dcdf9b60aaf70a809665a607da4f4c347d2406a261ebe3e9`
- `JJJ643/量化因子挖掘思路475份/中信因子深度研究系列1：特质波动率纯因子组合在A股的实证与研究.pdf` — SHA-256 `b4a89b481293b596dcdf9b60aaf70a809665a607da4f4c347d2406a261ebe3e9`
  - 归档副本：`../../sources/JJJ643/量化因子挖掘思路475份/中信因子深度研究系列1：特质波动率纯因子组合在A股的实证与研究.pdf`
- 来源页码：`6, 7`

## 复现实现

- Python 实现：`microfactor.factors.document_extended:_compute/doc_csc1_vcapm_20d`
- 默认参数：`{"annualization":252,"window":20}`
- 适配说明：原报告市场收益使用中证全指；当前使用每日股票池等权收益作为市场代理。

## 发布与评估

- Publication status: `published`
- Evaluation status: `passed`
- 因子版本：`bf6313ffbbb06f10932a`
- 数据快照：`snapshot_e3e73aa97706fd71f27ad486`
- 评估批次：`20260917_231028_ee6693d0`
- 有效区间：`2016-02-01` 至 `2026-09-15`

### 核心指标

- Rank IC Mean：`-0.0669009884051`
- Rank ICIR：`-0.58387812529`
- Adjusted ICIR：`0.58387812529`
- Long-short spread (bps)：`22.5826532056`
- Monotonicity：`0.866666666667`
- Coverage：`0.839984889578`
- Daily turnover (long)：`0.117501984831`
- Daily turnover (short)：`0.0922662021196`
