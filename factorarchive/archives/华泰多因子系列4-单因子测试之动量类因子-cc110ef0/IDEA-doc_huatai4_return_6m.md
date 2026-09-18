# doc_huatai4_return_6m

## 因子概览

- 类别：`momentum`
- 方向：`negative`
- 频率：`1d`
- 最小窗口：`126`
- 复权方式：`none`
- 实现状态：`exact`

## 公式

```text
close_total_return_index/Ref(close_total_return_index,126)-1
```

输入字段：`close_total_return_index`

## 原理说明

用过去一段时间的价格、成交量或换手率概括股票的交易行为。

## 来源

- 逻辑来源组：`华泰多因子系列4-单因子测试之动量类因子-cc110ef0`
- 来源组指纹：`cc110ef024e02077528d3c5715af610b110d831c769ecf30e8a308a859f0c76a`
- `JJJ643/量化因子挖掘思路475份/华泰多因子系列4：单因子测试之动量类因子.pdf` — SHA-256 `cc110ef024e02077528d3c5715af610b110d831c769ecf30e8a308a859f0c76a`
  - 归档副本：`../../sources/JJJ643/量化因子挖掘思路475份/华泰多因子系列4：单因子测试之动量类因子.pdf`
- 来源页码：`1, 6, 40, 42, 43`

## 复现实现

- Python 实现：`microfactor.factors.document_extended:_compute/doc_huatai4_return_6m`
- 默认参数：`{"months":6,"return_type":"close_to_close_total_return","window_days":126}`
- 适配说明：无。

## 发布与评估

- Publication status: `published`
- Evaluation status: `passed`
- 因子版本：`4b86789532b5023c79e4`
- 数据快照：`snapshot_e3e73aa97706fd71f27ad486`
- 评估批次：`20260917_231028_ee6693d0`
- 有效区间：`2016-07-11` 至 `2026-09-15`

### 核心指标

- Rank IC Mean：`-0.0383587958632`
- Rank ICIR：`-0.345913969066`
- Adjusted ICIR：`0.345913969066`
- Long-short spread (bps)：`21.7529903292`
- Monotonicity：`1`
- Coverage：`0.831796363636`
- Daily turnover (long)：`0.148971138943`
- Daily turnover (short)：`0.156538471333`
