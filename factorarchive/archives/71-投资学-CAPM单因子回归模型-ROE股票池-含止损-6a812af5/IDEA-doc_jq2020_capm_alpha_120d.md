# doc_jq2020_capm_alpha_120d

## 因子概览

- 类别：`momentum`
- 方向：`positive`
- 频率：`1d`
- 最小窗口：`120`
- 复权方式：`none`
- 实现状态：`approximate`

## 公式

```text
intercept from 120d OLS((stock_return-rf) ~ 1 + (market_return-rf))
```

输入字段：`close_to_close_total_return_1d`

## 原理说明

用过去一段时间的价格、成交量或换手率概括股票的交易行为。

## 来源

- 逻辑来源组：`71-投资学-CAPM单因子回归模型-ROE股票池-含止损-6a812af5`
- 来源组指纹：`6a812af5a6d5ef36b7893d4de3b3d61023a9bec85f257cfd3f815f67ca9127e5`
- `2020-2026聚宽600条源码/2020年度精选策略/71 【投资学】CAPM单因子回归模型+ROE股票池（含止损）.txt` — SHA-256 `6a812af5a6d5ef36b7893d4de3b3d61023a9bec85f257cfd3f815f67ca9127e5`
  - 归档副本：`../../sources/2020-2026聚宽600条源码/2020年度精选策略/71 【投资学】CAPM单因子回归模型+ROE股票池（含止损）.txt`
  - 历史库存 SHA-256：`5b13aeab9e2b04ee5c0f83bbbacb3f3a432187a52a879db1f32913471d94e057`（当前文件内容已变化）
- 来源页码：`未记录`

## 复现实现

- Python 实现：`microfactor.factors.document_extended:_compute/doc_jq2020_capm_alpha_120d`
- 默认参数：`{"annual_risk_free_rate":0.04,"daily_risk_free_rate":0.00015873015873015873,"include_intercept":true,"market_proxy":"available_stock_equal_weight","price_observations":121,"return_window_days":120,"source_index":"000300.XSHG","source_sort":"descending_alpha"}`
- 适配说明：The source uses 121 close prices for CSI 300 and each ROE-screened stock, subtracts 0.04/252 from each of the resulting 120 daily returns, and ranks the regression intercept descending. The current contract does not expose a CSI 300 return panel or point-in-time ROE, so the implementation exposes only the continuous intercept, uses close-to-close total returns, and uses the daily equal-weight return of the available stock universe as the market proxy.

## 发布与评估

- Publication status: `published`
- Evaluation status: `rejected`
- 因子版本：`afb1f2a87b4e42c9d4e2`
- 数据快照：`snapshot_e3e73aa97706fd71f27ad486`
- 评估批次：`20260917_231028_ee6693d0`
- 有效区间：`2016-07-01` 至 `2026-09-15`

### 核心指标

- Rank IC Mean：`-0.0402831804819`
- Rank ICIR：`-0.38095702532`
- Adjusted ICIR：`-0.38095702532`
- Long-short spread (bps)：`-23.1989950628`
- Monotonicity：`-0.975757575758`
- Coverage：`0.629990729545`
- Daily turnover (long)：`0.121197398752`
- Daily turnover (short)：`0.121380860981`
