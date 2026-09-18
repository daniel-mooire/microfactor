# doc_coppock_14_11_10

## 因子概览

- 类别：`momentum`
- 方向：`positive`
- 频率：`1d`
- 最小窗口：`24`
- 复权方式：`hfq`
- 实现状态：`approximate`

## 公式

```text
WMA10((C/Ref(C,14)-1)*100+(C/Ref(C,11)-1)*100)
```

输入字段：`close`

## 原理说明

通过价格和成交量的历史变化，概括趋势、波动或买卖力量。

## 来源

- 逻辑来源组：`广发多因子系列42-海量技术指标掘金Alpha因子-ebb746e4`
- 来源组指纹：`ebb746e4e36034e7bb654e15858c111028f0e23b67ecbaa72ca1d3677bba07bc`
- `JJJ643/量化因子挖掘思路475份/广发多因子系列42：海量技术指标掘金Alpha因子.pdf` — SHA-256 `ebb746e4e36034e7bb654e15858c111028f0e23b67ecbaa72ca1d3677bba07bc`
  - 归档副本：`../../sources/JJJ643/量化因子挖掘思路475份/广发多因子系列42：海量技术指标掘金Alpha因子.pdf`
- 来源页码：`未记录`

## 复现实现

- Python 实现：`microfactor.factors.document_indicators::doc_coppock_14_11_10`
- 默认参数：`{}`
- 适配说明：报告正文未给出唯一参数表，采用常见 14/11/10 参数并保留在名称中。

## 发布与评估

- Publication status: `published`
- Evaluation status: `rejected`
- 因子版本：`b6059fc67cc27133d0a3`
- 数据快照：`snapshot_e3e73aa97706fd71f27ad486`
- 评估批次：`20260917_231028_ee6693d0`
- 有效区间：`2016-02-04` 至 `2026-09-15`

### 核心指标

- Rank IC Mean：`-0.0448924378449`
- Rank ICIR：`-0.356200889772`
- Adjusted ICIR：`-0.356200889772`
- Long-short spread (bps)：`-24.5623357329`
- Monotonicity：`-0.793939393939`
- Coverage：`0.830432117921`
- Daily turnover (long)：`0.121841232478`
- Daily turnover (short)：`0.119391451348`
