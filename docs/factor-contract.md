# 因子契约

本文档描述 `microfactor` 的标准因子接口：因子代码能读什么数据、必须输出什么格式、结果落盘在哪里。

## 因子接口

一个标准因子由 `FactorSpec`（声明）和 `compute()`（计算）组成：

```python
import pandas as pd

from microfactor.core import Factor, FactorFrame, FactorSpec, to_factor_output


class Ret20_0(Factor):
    spec = FactorSpec(
        name="ret20_0",
        inputs=["close"],
        min_window=20,
        frequency="1d",
        adjust="hfq",
    )

    def compute(self, data: FactorFrame) -> pd.DataFrame:
        value = data.close / data.close.shift(20) - 1
        return to_factor_output(value, self.spec.name)
```

约束：

- 因子代码只应该访问 `FactorFrame`，不要自己读文件、查 DuckDB、或者直接调用 `microshare`；
- `inputs` 里声明用到的字段，provider 只提供声明过的数据；
- `min_window` 声明计算所需的最小回看窗口。

## 标准字段

`FactorFrame` 暴露的字段和 `microshare` 来源的对应关系：

| microfactor 字段 | microshare 来源 | 说明 |
|---|---|---|
| `open` | `open` | provider 负责复权 |
| `high` | `high` | provider 负责复权 |
| `low` | `low` | provider 负责复权 |
| `close` | `close` | provider 负责复权 |
| `volume` | `vol` | 统一改名，方便因子代码阅读 |
| `amount` | `amount` | 成交额 |
| `return_` | `pct_chg` 或计算收益率 | 避开 Python 关键字 `return` |
| `pre_close` | `pre_close` | 前一交易日收盘价 |
| `adjusted_close` | `pro_bar(adj=...)` | 复权收盘价 |
| `close_total_return_index` | `pro_bar` + 前复权基准 | 总回报指数 |
| `close_to_close_total_return_1d` | 总回报指数日变化 | 点时日收益 |
| `total_mv`, `circ_mv` | `daily_basic` | 总市值 / 流通市值 |
| `pe_ttm`, `pb`, `ps_ttm`, `dv_ttm` | `daily_basic` | 点时估值字段 |
| `turnover_rate`, `turnover_percent` | `daily_basic.turnover_rate` | 统一为百分比口径 |
| `is_suspended`, `is_st` | `suspend_d`, `stock_st` | 状态布尔面板 |
| `list_date` | `stock_basic` | 上市日期静态面板 |
| `up_limit`, `down_limit` | `stk_limit` | 涨跌停价 |
| `vwap` | `amount / vol` | 成交量非零时计算 |

默认使用后复权：`hfq`。

微盘因子计算和评估使用 `hushen_mainboard_previous_day_bottom1000`。成员关系
通过 `MicroshareDataProvider` 调用 `pro.universe(...)` 获得，并在每日截面上掩码；
不会直接读取股票池 Parquet，也不会用未来成员关系。评估的 `open_t1` 是 T 日收盘
生成信号、T+1 开盘成交的收益。

## 输出格式

因子结果必须是三列：

```text
trade_date, ts_code, value
```

`to_factor_output()` 会把宽表面板转成这个格式。

## 因子存储

因子值按日期分区写入 Parquet，元数据注册在 DuckDB：

```text
data/factors/
└── ret20_0/
    ├── date=20240102/data.parquet
    └── date=20240103/data.parquet

db/
└── factor_meta.duckdb
```
