# doc_guosheng8_corr_rank_volume_intraday_6d

## 因子概览

- 类别：`price_volume`
- 方向：`positive`
- 频率：`1d`
- 最小窗口：`7`
- 复权方式：`none`
- 实现状态：`approximate`

## 公式

```text
-corr(rank(delta(log(volume),1)),rank((close-open)/open),6)
```

输入字段：`open, close, volume`

## 原理说明

把成交量变化和日内涨跌方向分别排序，再观察它们最近几天是否同向；负相关越强，信号值越高。

## 来源

- 逻辑来源组：`国盛多因子系列8-日间量价模型研究-aec2c2d8`
- 来源组指纹：`aec2c2d80cd1d97b5eba4e25ffbf1eaffb50d58bf89a5a5b797c163739cb5392`
- `JJJ643/量化因子挖掘思路475份/国盛多因子系列8：日间量价模型研究.pdf` — SHA-256 `aec2c2d80cd1d97b5eba4e25ffbf1eaffb50d58bf89a5a5b797c163739cb5392`
  - 归档副本：`../../sources/JJJ643/量化因子挖掘思路475份/国盛多因子系列8：日间量价模型研究.pdf`
- 来源页码：`8`

## 复现实现

- Python 实现：`microfactor.factors.document_indicators::doc_guosheng8_corr_rank_volume_intraday_6d`
- 默认参数：`{}`
- 适配说明：源报告收益使用开盘前 30 分钟 VWAP；当前日频契约改用 open_t1 评估，公式本身保持日频。

## 发布与评估

- Publication status: `published`
- Evaluation status: `passed`
- 因子版本：`3d6d0fd9c03331384ad9`
- 数据快照：`snapshot_e3e73aa97706fd71f27ad486`
- 评估批次：`20260917_231028_ee6693d0`
- 有效区间：`2016-01-12` 至 `2026-09-15`

### 核心指标

- Rank IC Mean：`0.0278401968922`
- Rank ICIR：`0.449814799377`
- Adjusted ICIR：`0.449814799377`
- Long-short spread (bps)：`7.97183676859`
- Monotonicity：`0.890909090909`
- Coverage：`0.901346050096`
- Daily turnover (long)：`0.406108015708`
- Daily turnover (short)：`0.410571349004`
