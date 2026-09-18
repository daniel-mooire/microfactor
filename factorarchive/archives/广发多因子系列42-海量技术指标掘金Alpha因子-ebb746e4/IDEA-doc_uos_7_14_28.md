# doc_uos_7_14_28

## 因子概览

- 类别：`volatility`
- 方向：`positive`
- 频率：`1d`
- 最小窗口：`29`
- 复权方式：`hfq`
- 实现状态：`approximate`

## 公式

```text
TH=MAX(H,REF(C,1)); TL=MIN(L,REF(C,1)); UOS=100*(ACC1*14*28+ACC2*7*28+ACC3*7*14)/(7*14+7*28+14*28)
```

输入字段：`high, low, close`

## 原理说明

通过价格和成交量的历史变化，概括趋势、波动或买卖力量。

## 来源

- 逻辑来源组：`广发多因子系列42-海量技术指标掘金Alpha因子-ebb746e4`
- 来源组指纹：`ebb746e4e36034e7bb654e15858c111028f0e23b67ecbaa72ca1d3677bba07bc`
- `JJJ643/量化因子挖掘思路475份/广发多因子系列42：海量技术指标掘金Alpha因子.pdf` — SHA-256 `ebb746e4e36034e7bb654e15858c111028f0e23b67ecbaa72ca1d3677bba07bc`
  - 归档副本：`../../sources/JJJ643/量化因子挖掘思路475份/广发多因子系列42：海量技术指标掘金Alpha因子.pdf`
- 来源页码：`115`

## 复现实现

- Python 实现：`microfactor.factors.document_indicators::doc_uos_7_14_28`
- 默认参数：`{"N1":7,"N2":14,"N3":28}`
- 适配说明：原文未列具体周期，采用常见 7/14/28 组合；TH/TL 按 MAX/MIN 的逐日定义计算，所有 SUM 均使用当日及历史可见窗口。

## 发布与评估

- Publication status: `published`
- Evaluation status: `rejected`
- 因子版本：`69e0a3094ffbced31de7`
- 数据快照：`snapshot_e3e73aa97706fd71f27ad486`
- 评估批次：`20260917_231028_ee6693d0`
- 有效区间：`2016-02-17` 至 `2026-09-15`

### 核心指标

- Rank IC Mean：`-0.0374089002564`
- Rank ICIR：`-0.338936850437`
- Adjusted ICIR：`-0.338936850437`
- Long-short spread (bps)：`-32.4722760975`
- Monotonicity：`-0.951515151515`
- Coverage：`0.817056721057`
- Daily turnover (long)：`0.350222191885`
- Daily turnover (short)：`0.348714253188`
