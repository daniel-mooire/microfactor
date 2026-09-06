# microfactor 环境设计

## 背景

microfactor 是基于 microshare 数据源的 A 股因子投研 lab，覆盖因子计算 → 因子评价 → 组合构建全流程。

数据来源：[microshare](../../../microshare)（本地 Parquet + DuckDB，Tushare Pro 行情数据）

参考项目：alphalens-reloaded、pyfolio-reloaded、AlphaPurify

---

## 架构决策

### 数据存储（A2 方案）

microshare 保持只读，不暴露因子写入接口。microfactor 自维护因子存储，复用相同的 Parquet 分区 + DuckDB 模式，物理隔离。

### microshare 接入

通过 `loader.py` 单点封装 `pro_api()` 调用。所有因子模块只调用 `MarketLoader`，不直接依赖 microshare 内部模块，换数据源只改一处。

---

## 项目结构

```
microfactor/
├── config/
│   ├── settings.example.toml
│   └── settings.toml            # gitignore
├── data/
│   └── factors/
│       ├── momentum/
│       │   ├── date=20240101/data.parquet
│       │   └── ...
│       └── value/
│           └── ...
├── db/
│   └── factor_meta.duckdb
├── notebooks/
├── src/
│   ├── config.py
│   ├── loader.py                # microshare 行情数据接入层
│   ├── factor/                  # 因子计算
│   ├── eval/                    # 因子评价（IC/IR、分组回测）
│   ├── portfolio/               # 组合构建
│   └── storage.py               # 因子 Parquet + DuckDB 写入
├── tests/
├── pyproject.toml
└── main.py
```

---

## 依赖配置

### 数据层
- `polars` — 高性能 DataFrame
- `duckdb` — 因子元数据查询
- `pyarrow` — Parquet 读写

### 研究层
- `alphalens-reloaded` — 因子 IC / 分组分析
- `pyfolio-reloaded` — 组合绩效归因
- `jupyter` + `ipykernel` — 研究笔记本
- `plotly` — 交互式可视化

### 工程层
- `loguru` — 日志
- `click` — CLI 入口

### dev 依赖
- `pytest`、`pytest-cov`、`ruff`

### microshare 路径依赖
```toml
[tool.uv.sources]
microshare = { path = "../microshare" }
```

---

## 配置（settings.toml）

```toml
[microshare]
project_dir = "../microshare"

[paths]
factor_dir = "data/factors"
db_path    = "db/factor_meta.duckdb"
log_path   = "logs/factor.log"

[factor]
universe   = "all"      # all / hs300 / zz500
start_date = "20160101"
end_date   = ""         # 空 = 最新交易日
```

---

## loader.py 接口

```python
from microshare.src import pro_api

class MarketLoader:
    def __init__(self, cfg): ...
    def get_daily(self, start_date, end_date, adj="qfq") -> pl.DataFrame: ...
    def get_universe(self, date) -> list[str]: ...
```
