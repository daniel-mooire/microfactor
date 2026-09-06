# 因子数据库 API

`microfactor` 将因子值、因子契约和评估结果统一保存到 Parquet + DuckDB，并提供只读 Python 查询接口：

```python
from microfactor import factor_api

api = factor_api()
```

## 因子值

```python
api.factor(
    "momentum",
    start_date="20240101",
    end_date="20241231",
    ts_code="000001.SZ",
)
```

单因子长表固定为 `trade_date`、`ts_code`、`value`。多个因子使用 `format="wide"`：

```python
api.factor(
    ["momentum", "inverse_pb"],
    start_date="20240101",
    end_date="20241231",
    format="wide",
)
```

宽表固定包含 `trade_date`、`ts_code`，其余列为因子名。默认读取 `version="latest"`，也可以传入具体版本号读取历史版本。

`passed` 和 `rejected` 因子的值都可以读取。若模型只使用通过门槛的因子，应先查询：

```python
names = api.factor_basic(evaluation_status="passed")["factor_name"].tolist()
```

## 元数据和评估

```python
api.factor_basic()
api.factor_basic(category="price")
api.factor_evaluation("momentum", run_id="latest")
api.factor_runs(factor_name="momentum", status="completed")
```

`factor_evaluation(run_id="latest")` 只选择完整批次；部分运行不会被隐式当作最新结果。返回结果包含评估状态、版本、股票池、样本区间、收益口径、交易成本、核心指标以及汇总/单因子报告路径。

## 版本和增量发布

因子文件按日期分区保存：

```text
data/factors/<factor_name>/date=YYYYMMDD/*.parquet
data/factors/<factor_name>/manifests/<version_id>.json
data/factors/<factor_name>/latest.json
```

计算服务使用 `FactorStorage.publish_factor()` 发布版本：

```python
storage.publish_factor(
    "new_factor",
    frame,
    contract=factor.spec,
    compute_run_id="run_20260906",
    universe="hushen_mainboard_previous_day_bottom1000",
)
```

发布规则：

- 新日期追加并生成新的不可变版本清单。
- 已存在日期且值完全一致时幂等成功。
- 已存在日期但值冲突时抛出 `FactorDataIntegrityError`，禁止静默覆盖。
- 公式、输入字段或复权模式变化时，必须显式传入 `new_version=True`，新数据写入独立版本目录。
- 只有写入完成、质量检查通过并登记到 DuckDB 的版本才能成为 `latest`。

现有 65 个非模型因子首次使用 API 时会自动完成版本清单和评估批次引导；该过程不复制原有 Parquet 数据。
