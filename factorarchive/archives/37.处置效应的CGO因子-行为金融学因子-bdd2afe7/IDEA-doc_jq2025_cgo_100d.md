# doc_jq2025_cgo_100d

## 因子概览

- 类别：`behavioral`
- 方向：`negative`
- 频率：`1d`
- 最小窗口：`100`
- 复权方式：`none`
- 实现状态：`approximate`

## 公式

```text
close/RP100-1; RP100=sum(vwap_i*w_i)/sum(w_i), w_i=turn_i*product(1-turn_j, j=i+1..t)
```

输入字段：`vwap, close, turnover_percent, is_suspended, list_date`

## 原理说明

用过去一段时间的价格、成交量或换手率概括股票的交易行为。

## 来源

- 逻辑来源组：`37.处置效应的CGO因子-行为金融学因子-bdd2afe7`
- 来源组指纹：`bdd2afe74b8cb9c64406ca3652f79280747be21a75e467b608d68fe5675e15b4`
- `2020-2026聚宽600条源码/2025年度精选策略/37.处置效应的CGO因子（行为金融学因子）.txt` — SHA-256 `bdd2afe74b8cb9c64406ca3652f79280747be21a75e467b608d68fe5675e15b4`
  - 归档副本：`../../sources/2020-2026聚宽600条源码/2025年度精选策略/37.处置效应的CGO因子（行为金融学因子）.txt`
- 来源页码：`未记录`

## 复现实现

- Python 实现：`microfactor.factors.document_extended:_compute/doc_jq2025_cgo_100d`
- 默认参数：`{"maximum_suspended_days":50,"minimum_listing_age_days":220,"missing_suspension_is_suspended":false,"recent_limit_down_threshold":-0.095,"recent_limit_down_window":10,"window":100}`
- 适配说明：原策略每 5 个交易日调仓；当前输出每日滚动因子值供统一评估；停牌事件表缺失值按未停牌处理。

## 发布与评估

- Publication status: `published`
- Evaluation status: `passed`
- 因子版本：`f4ff3bd6bc70f98f86ff`
- 数据快照：`snapshot_e3e73aa97706fd71f27ad486`
- 评估批次：`20260917_231028_ee6693d0`
- 有效区间：`2016-05-31` 至 `2026-09-15`

### 核心指标

- Rank IC Mean：`-0.0467597547766`
- Rank ICIR：`-0.388698328541`
- Adjusted ICIR：`0.388698328541`
- Long-short spread (bps)：`29.2441973862`
- Monotonicity：`0.866666666667`
- Coverage：`0.939966027178`
- Daily turnover (long)：`0.169000660456`
- Daily turnover (short)：`0.304215949775`
