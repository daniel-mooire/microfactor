# doc_guangfa45_semibeta_mn_60d

## 因子概览

- 类别：`volatility`
- 方向：`negative`
- 频率：`1d`
- 最小窗口：`60`
- 复权方式：`hfq`
- 实现状态：`approximate`

## 公式

```text
-SUM60(max(r_i,0)*min(r_m,0))/SUM60(r_m^2)
```

输入字段：`close_to_close_total_return_1d`

## 原理说明

用过去一段时间的价格、成交量或换手率概括股票的交易行为。

## 来源

- 逻辑来源组：`广发多因子系列45-基于SemiBeta的因子研究-868965b9`
- 来源组指纹：`868965b9f7b42007aab42343529990f582f45d4d8c2e1e0e337c6e395554bad9`
- `JJJ643/量化因子挖掘思路475份/广发多因子系列45：基于SemiBeta的因子研究.pdf` — SHA-256 `868965b9f7b42007aab42343529990f582f45d4d8c2e1e0e337c6e395554bad9`
  - 归档副本：`../../sources/JJJ643/量化因子挖掘思路475份/广发多因子系列45：基于SemiBeta的因子研究.pdf`
- 来源页码：`9, 10`

## 复现实现

- Python 实现：`microfactor.factors.document_extended:_compute/doc_guangfa45_semibeta_mn_60d`
- 默认参数：`{"market_proxy":"equal_weight_universe","semibeta":"MN","window":60}`
- 适配说明：原报告使用宽基指数收益；当前使用每日股票池等权收益作为市场代理。

## 发布与评估

- Publication status: `published`
- Evaluation status: `passed`
- 因子版本：`13e878cd09d0437c5f9b`
- 数据快照：`snapshot_e3e73aa97706fd71f27ad486`
- 评估批次：`20260917_231028_ee6693d0`
- 有效区间：`2016-04-05` 至 `2026-09-15`

### 核心指标

- Rank IC Mean：`-0.0449664026112`
- Rank ICIR：`-0.501073318852`
- Adjusted ICIR：`0.501073318852`
- Long-short spread (bps)：`18.0634345507`
- Monotonicity：`1`
- Coverage：`0.733823297914`
- Daily turnover (long)：`0.0650810953967`
- Daily turnover (short)：`0.0534973755714`
