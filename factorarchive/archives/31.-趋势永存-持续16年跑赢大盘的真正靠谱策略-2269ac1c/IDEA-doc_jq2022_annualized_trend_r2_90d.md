# doc_jq2022_annualized_trend_r2_90d

## 因子概览

- 类别：`momentum`
- 方向：`positive`
- 频率：`1d`
- 最小窗口：`90`
- 复权方式：`qfq`
- 实现状态：`approximate`

## 公式

```text
(exp(250*OLS_slope(log(close),x=0..89))-1)*OLS_R2
```

输入字段：`adjusted_close`

## 原理说明

用过去一段时间的价格、成交量或换手率概括股票的交易行为。

## 来源

- 逻辑来源组：`31.-趋势永存-持续16年跑赢大盘的真正靠谱策略-2269ac1c`
- 来源组指纹：`2269ac1c706a04e9fdb0867c31c81f7975a6ae1de521de35d6e7e4d095261bd2`
- `2020-2026聚宽600条源码/2022年度精选策略/31.《趋势永存》持续16年跑赢大盘的真正靠谱策略.txt` — SHA-256 `2269ac1c706a04e9fdb0867c31c81f7975a6ae1de521de35d6e7e4d095261bd2`
  - 归档副本：`../../sources/2020-2026聚宽600条源码/2022年度精选策略/31.《趋势永存》持续16年跑赢大盘的真正靠谱策略.txt`
- 来源页码：`未记录`

## 复现实现

- Python 实现：`microfactor.factors.document_extended:_compute/doc_jq2022_annualized_trend_r2_90d`
- 默认参数：`{"annualization_days":250,"dependent_variable":"log_adjusted_close","include_intercept":true,"source_index":"399300.XSHE","source_rebalance":"weekly","window_days":90}`
- 适配说明：The source ranks CSI 300 constituents weekly, then applies a 100-day price filter, a two-day gap filter, a 200-day index regime filter, and ATR-based position sizing. The implementation exposes only the source's transparent 90-day continuous score across the current daily stock universe. JoinQuant's attribute_history price adjustment is not pinned, so the project uses qfq.

## 发布与评估

- Publication status: `published`
- Evaluation status: `rejected`
- 因子版本：`f04c0e2d65aead141d30`
- 数据快照：`snapshot_e3e73aa97706fd71f27ad486`
- 评估批次：`20260917_231028_ee6693d0`
- 有效区间：`2016-05-17` 至 `2026-09-15`

### 核心指标

- Rank IC Mean：`-0.0231828275407`
- Rank ICIR：`-0.204514135458`
- Adjusted ICIR：`-0.204514135458`
- Long-short spread (bps)：`-10.9894882049`
- Monotonicity：`-0.878787878788`
- Coverage：`0.678715764331`
- Daily turnover (long)：`0.0379480806682`
- Daily turnover (short)：`0.0415289970766`
