# doc_pvt_6

## 因子概览

- 类别：`price_volume`
- 方向：`unspecified`
- 频率：`1d`
- 最小窗口：`6`
- 复权方式：`hfq`
- 实现状态：`exact`

## 公式

```text
sum(delta(C)/Ref(C,1)*V,6)
```

输入字段：`close, volume`

## 原理说明

用过去一段时间的价格、成交量或换手率概括股票的交易行为。

## 来源

- 逻辑来源组：`广发多因子系列42-海量技术指标掘金Alpha因子-ebb746e4`
- 来源组指纹：`ebb746e4e36034e7bb654e15858c111028f0e23b67ecbaa72ca1d3677bba07bc`
- `JJJ643/量化因子挖掘思路475份/广发多因子系列42：海量技术指标掘金Alpha因子.pdf` — SHA-256 `ebb746e4e36034e7bb654e15858c111028f0e23b67ecbaa72ca1d3677bba07bc`
  - 归档副本：`../../sources/JJJ643/量化因子挖掘思路475份/广发多因子系列42：海量技术指标掘金Alpha因子.pdf`
- 来源页码：`未记录`

## 复现实现

- Python 实现：`microfactor.factors.document_extended:_compute/doc_pvt_6`
- 默认参数：`{}`
- 适配说明：无。

## 发布与评估

- Publication status: `published`
- Evaluation status: `rejected`
- 因子版本：`eae8cc7e278152651416`
- 数据快照：`snapshot_e3e73aa97706fd71f27ad486`
- 评估批次：`20260917_231028_ee6693d0`
- 有效区间：`2016-01-12` 至 `2026-09-15`

### 核心指标

- Rank IC Mean：`-0.0460106283319`
- Rank ICIR：`-0.396781756758`
- Adjusted ICIR：`-0.396781756758`
- Long-short spread (bps)：`-22.073050338`
- Monotonicity：`-0.490909090909`
- Coverage：`0.901355684008`
- Daily turnover (long)：`0.290074823708`
- Daily turnover (short)：`0.359148819775`
