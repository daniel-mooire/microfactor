# doc_ddi_diz_13

## 因子概览

- 类别：`trend`
- 方向：`negative`
- 频率：`1d`
- 最小窗口：`14`
- 复权方式：`hfq`
- 实现状态：`approximate`

## 公式

```text
DIZ=SUM(DMZ,13)/(SUM(DMZ,13)+SUM(DMF,13))
```

输入字段：`high, low`

## 原理说明

通过价格和成交量的历史变化，概括趋势、波动或买卖力量。

## 来源

- 逻辑来源组：`广发多因子系列42-海量技术指标掘金Alpha因子-ebb746e4`
- 来源组指纹：`ebb746e4e36034e7bb654e15858c111028f0e23b67ecbaa72ca1d3677bba07bc`
- `JJJ643/量化因子挖掘思路475份/广发多因子系列42：海量技术指标掘金Alpha因子.pdf` — SHA-256 `ebb746e4e36034e7bb654e15858c111028f0e23b67ecbaa72ca1d3677bba07bc`
  - 归档副本：`../../sources/JJJ643/量化因子挖掘思路475份/广发多因子系列42：海量技术指标掘金Alpha因子.pdf`
- 来源页码：`65, 66, 67`

## 复现实现

- Python 实现：`microfactor.factors.document_indicators::doc_ddi_diz_13`
- 默认参数：`{"N":13,"movement_branch":"2021"}`
- 适配说明：DMZ/DMF 采用报告 2021 版分支，比较当日高低价和昨日高低价之和，并以昨日最低价计算两项移动幅度。

## 发布与评估

- Publication status: `published`
- Evaluation status: `passed`
- 因子版本：`02e9d086edb0e8adffc4`
- 数据快照：`snapshot_e3e73aa97706fd71f27ad486`
- 评估批次：`20260917_231028_ee6693d0`
- 有效区间：`2016-01-20` 至 `2026-09-15`

### 核心指标

- Rank IC Mean：`-0.0356870378635`
- Rank ICIR：`-0.368355267399`
- Adjusted ICIR：`0.368355267399`
- Long-short spread (bps)：`18.5870301583`
- Monotonicity：`0.854545454545`
- Coverage：`0.995125531093`
- Daily turnover (long)：`0.313841736229`
- Daily turnover (short)：`0.337854249143`
