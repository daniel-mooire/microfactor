# doc_haitong18_vwap_close_20d

## 因子概览

- 类别：`price_shape`
- 方向：`positive`
- 频率：`1d`
- 最小窗口：`21`
- 复权方式：`hfq`
- 实现状态：`exact`

## 公式

```text
MEAN(log(vwap/close), i=t-20..t-1)
```

输入字段：`vwap, close, is_suspended`

## 原理说明

用过去一段时间的价格、成交量或换手率概括股票的交易行为。

## 来源

- 逻辑来源组：`海通选股因子系列研究18-价格形态选股因子-d695dd3c`
- 来源组指纹：`d695dd3c8ad7708faeff9fde0b7b5a434387df81b0b148f58b1210f0b94a71f0`
- `JJJ643/量化因子挖掘思路475份/海通选股因子系列研究18：价格形态选股因子.pdf` — SHA-256 `d695dd3c8ad7708faeff9fde0b7b5a434387df81b0b148f58b1210f0b94a71f0`
  - 归档副本：`../../sources/JJJ643/量化因子挖掘思路475份/海通选股因子系列研究18：价格形态选股因子.pdf`
- 来源页码：`5, 6`

## 复现实现

- Python 实现：`microfactor.factors.document_extended:_compute/doc_haitong18_vwap_close_20d`
- 默认参数：`{"minimum_valid_days":10,"window":20}`
- 适配说明：无。

## 发布与评估

- Publication status: `published`
- Evaluation status: `rejected`
- 因子版本：`a7ab3fb52971eb804e42`
- 数据快照：`snapshot_e3e73aa97706fd71f27ad486`
- 评估批次：`20260917_231028_ee6693d0`
- 有效区间：`2016-02-01` 至 `2026-09-15`

### 核心指标

- Rank IC Mean：`0.00055449682394`
- Rank ICIR：`0.00565409810315`
- Adjusted ICIR：`0.00565409810315`
- Long-short spread (bps)：`-3.52560175471`
- Monotonicity：`-0.672727272727`
- Coverage：`0.950504455637`
- Daily turnover (long)：`0.0264518871594`
- Daily turnover (short)：`0.0344389404617`
