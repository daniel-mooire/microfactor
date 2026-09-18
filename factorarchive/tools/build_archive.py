from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import re
import shutil
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any, Mapping

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
WORKSPACE_ROOT = PROJECT_ROOT.parent
MICROFACTOR_ROOT = WORKSPACE_ROOT / "microfactor"
FACTOREVAL_ROOT = WORKSPACE_ROOT / "factoreval"
SOURCE_ROOT = Path(r"D:\BaiduNetdiskDownload")
INVENTORY_PATH = (
    MICROFACTOR_ROOT
    / "research"
    / "document-factor-mining"
    / "output"
    / "source_inventory.csv"
)

EXPECTED_FACTOR_COUNT = 393
EXPECTED_EXACT_COUNT = 247
EXPECTED_APPROXIMATE_COUNT = 146
EXPECTED_PUBLISHED_COUNT = 332
EXPECTED_PASSED_COUNT = 84
EXPECTED_REJECTED_COUNT = 248
EXPECTED_UNPUBLISHED_COUNT = 61
EXPECTED_SOURCE_COUNT = 60
EXPECTED_SNAPSHOT_ID = "snapshot_e3e73aa97706fd71f27ad486"
EXPECTED_RUN_ID = "20260917_231028_ee6693d0"
EXPECTED_START = "2016-01-04"
EXPECTED_END = "2026-09-15"
EXPECTED_SOURCE_END = "2026-09-17"

ARXIV_ALPHA101 = (
    "JJJ643/量化因子挖掘思路475份/101 Formulaic Alphas - arXiv.org.pdf"
)
HUATAI_ALPHA101 = (
    "JJJ643/量化因子挖掘思路475份/"
    "华泰多因子系列11：单因子测试之海量技术因子.pdf"
)
BOHAI_ALPHA101 = (
    "JJJ643/量化因子挖掘思路475份/"
    "渤海多因子模型研究系列14：技术因子的再挖掘Alpha 101.pdf"
)
HUATAI_TURNOVER = (
    "JJJ643/量化因子挖掘思路475份/"
    "华泰多因子系列5：单因子测试之换手率类因子.pdf"
)
HUATAI_VOLATILITY = (
    "JJJ643/量化因子挖掘思路475份/"
    "华泰多因子系列6：单因子测试之波动率类因子.pdf"
)
HUATAI_COLLECTION = (
    SOURCE_ROOT / "JJJ643" / "量化因子挖掘思路475份" / "华泰多因子系列"
)

MANAGED_PATHS = (
    "archive.toml",
    "configs",
    "factors",
    "archives",
    "evaluations",
    "sources",
)

EVALUATION_PATH_COLUMNS = {
    "result_path",
    "report_path",
    "run_manifest_path",
    "run_report_path",
}


@dataclass(frozen=True)
class SourceFile:
    relative_path: str
    path: Path
    sha256: str
    inventory_sha256: str

    @property
    def inventory_matches(self) -> bool:
        return self.sha256 == self.inventory_sha256


@dataclass(frozen=True)
class SourceGroup:
    raw_source: str
    label: str
    source_id: str
    reference: str
    source_files: tuple[SourceFile, ...]
    factors: tuple[Any, ...]


@dataclass(frozen=True)
class ArchiveInputs:
    factors: tuple[Any, ...]
    basic: pd.DataFrame
    evaluation: pd.DataFrame
    run: Mapping[str, Any]
    run_config: Mapping[str, Any]
    inventory: Mapping[str, Mapping[str, str]]


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def toml_string(value: Any) -> str:
    return json.dumps(str(value), ensure_ascii=False)


def toml_string_list(values: Any) -> str:
    return json.dumps([str(value) for value in values], ensure_ascii=False)


def canonical_value(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {
            str(key): canonical_value(item)
            for key, item in sorted(value.items(), key=lambda pair: str(pair[0]))
        }
    if isinstance(value, (list, tuple)):
        return [canonical_value(item) for item in value]
    if isinstance(value, set):
        return sorted(canonical_value(item) for item in value)
    if isinstance(value, Path):
        return str(value)
    if hasattr(value, "item"):
        return canonical_value(value.item())
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    return str(value)


def canonical_json(value: Any) -> str:
    return json.dumps(
        canonical_value(value),
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )


def normalize_relative_path(value: str) -> str:
    return value.replace("\\", "/").strip("/")


def format_date(value: Any) -> str:
    text = str(value).strip()
    digits = re.sub(r"\D", "", text)
    if len(digits) >= 8:
        digits = digits[:8]
        return f"{digits[:4]}-{digits[4:6]}-{digits[6:8]}"
    raise ValueError(f"cannot normalize date: {value!r}")


def clean_output(output_root: Path) -> None:
    output_root = output_root.resolve()
    if output_root == Path(output_root.anchor) or len(output_root.parts) < 3:
        raise ValueError(f"unsafe output directory: {output_root}")
    output_root.mkdir(parents=True, exist_ok=True)
    for relative in MANAGED_PATHS:
        target = (output_root / relative).resolve()
        if output_root not in target.parents:
            raise ValueError(f"managed path escapes output directory: {target}")
        if target.is_dir():
            shutil.rmtree(target)
        elif target.exists():
            target.unlink()


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(content)


def load_inventory() -> dict[str, Mapping[str, str]]:
    with INVENTORY_PATH.open("r", encoding="utf-8-sig", newline="") as handle:
        return {
            normalize_relative_path(row["relative_path"]): row
            for row in csv.DictReader(handle)
        }


def source_path_from_relative(relative_path: str) -> Path:
    return SOURCE_ROOT.joinpath(*PurePosixPath(relative_path).parts)


def direct_source_relative(raw_source: str) -> str:
    source_path = Path(raw_source.split(";", 1)[0].strip())
    return normalize_relative_path(str(source_path.relative_to(SOURCE_ROOT)))


def is_huatai_collection(raw_source: str) -> bool:
    raw = raw_source.replace("\\", "/").rstrip("/")
    expected = str(HUATAI_COLLECTION).replace("\\", "/").rstrip("/")
    return raw.casefold() == expected.casefold()


def group_source_relatives(raw_source: str) -> tuple[str, ...]:
    if is_huatai_collection(raw_source):
        return HUATAI_TURNOVER, HUATAI_VOLATILITY
    if "; 101 Formulaic Alphas" in raw_source:
        return direct_source_relative(raw_source), ARXIV_ALPHA101
    return (direct_source_relative(raw_source),)


def factor_source_relatives(factor: Any) -> tuple[str, ...]:
    raw_source = str(factor.metadata.source)
    if not is_huatai_collection(raw_source):
        return group_source_relatives(raw_source)
    name = factor.spec.name
    if name.startswith("doc_huatai_std_return_"):
        return (HUATAI_VOLATILITY,)
    return (HUATAI_TURNOVER,)


def source_label(raw_source: str) -> str:
    if is_huatai_collection(raw_source):
        return "华泰多因子系列基础换手率与波动率因子"
    primary = direct_source_relative(raw_source)
    if primary == HUATAI_ALPHA101:
        return "Alpha101-华泰海量技术因子与原始论文"
    if primary == BOHAI_ALPHA101:
        return "渤海系列14-Alpha101横截面调整"
    return PurePosixPath(primary).stem


def source_id(label: str, reference: str) -> str:
    safe = re.sub(r"[^\w.-]+", "-", label, flags=re.UNICODE)
    safe = re.sub(r"-+", "-", safe).strip(" .-_")
    safe = safe[:64].rstrip(" .-_") or "source"
    return f"{safe}-{reference[:8]}"


def load_source_file(
    relative_path: str,
    inventory: Mapping[str, Mapping[str, str]],
    cache: dict[str, SourceFile],
) -> SourceFile:
    relative_path = normalize_relative_path(relative_path)
    if relative_path in cache:
        return cache[relative_path]
    path = source_path_from_relative(relative_path)
    if not path.is_file():
        raise FileNotFoundError(path)
    actual_hash = sha256_file(path)
    inventory_row = inventory.get(relative_path)
    if inventory_row is None:
        raise KeyError(f"source missing from inventory: {relative_path}")
    inventory_hash = inventory_row.get("content_sha256", "")
    result = SourceFile(relative_path, path, actual_hash, inventory_hash)
    cache[relative_path] = result
    return result


def source_reference(source_files: tuple[SourceFile, ...]) -> str:
    if len(source_files) == 1:
        return source_files[0].sha256
    payload = "".join(
        f"{item.relative_path}\0{item.sha256}\n"
        for item in sorted(source_files, key=lambda source: source.relative_path)
    ).encode("utf-8")
    return sha256_bytes(payload)


def build_source_groups(
    factors: tuple[Any, ...],
    inventory: Mapping[str, Mapping[str, str]],
) -> tuple[SourceGroup, ...]:
    grouped: dict[str, list[Any]] = defaultdict(list)
    for factor in factors:
        grouped[str(factor.metadata.source)].append(factor)
    if len(grouped) != EXPECTED_SOURCE_COUNT:
        raise ValueError(f"expected 60 source groups, found {len(grouped)}")
    cache: dict[str, SourceFile] = {}
    groups: list[SourceGroup] = []
    for raw_source, items in sorted(grouped.items()):
        relatives = group_source_relatives(raw_source)
        source_files = tuple(
            sorted(
                (
                    load_source_file(relative, inventory, cache)
                    for relative in relatives
                ),
                key=lambda source: source.relative_path,
            )
        )
        reference = source_reference(source_files)
        label = source_label(raw_source)
        groups.append(
            SourceGroup(
                raw_source=raw_source,
                label=label,
                source_id=source_id(label, reference),
                reference=reference,
                source_files=source_files,
                factors=tuple(sorted(items, key=lambda factor: factor.spec.name)),
            )
        )
    ids = [group.source_id for group in groups]
    if len(ids) != len(set(ids)):
        raise ValueError("source identifiers are not unique")
    return tuple(sorted(groups, key=lambda group: group.source_id))


def metadata_adaptation(metadata: Any) -> str:
    return str(
        getattr(metadata, "adaptation_note", "")
        or getattr(metadata, "adaptation", "")
        or ""
    )


def metadata_pages(metadata: Any) -> tuple[int, ...]:
    pages = getattr(metadata, "source_pages", ()) or getattr(metadata, "pages", ())
    if pages:
        return tuple(int(page) for page in pages)
    paper_page = getattr(metadata, "paper_page", None)
    return (int(paper_page),) if paper_page else ()


def metadata_parameters(metadata: Any) -> Mapping[str, Any]:
    parameters = dict(getattr(metadata, "default_parameters", {}) or {})
    if not parameters:
        number = getattr(metadata, "number", None)
        delay = getattr(metadata, "delay", None)
        if number is not None:
            parameters["factor_number"] = int(number)
        if delay is not None:
            parameters["delay_sessions"] = int(delay)
    return parameters


def implementation_status(factor: Any) -> str:
    return str(getattr(factor.metadata, "implementation_status", "exact"))


def factor_contract(factor: Any, group: SourceGroup) -> dict[str, Any]:
    metadata = factor.metadata
    spec = factor.spec
    return {
        "version": 1,
        "name": spec.name,
        "frequency": spec.frequency,
        "formula": metadata.formula,
        "inputs": list(metadata.inputs),
        "min_window": int(metadata.min_window),
        "direction": metadata.direction,
        "category": metadata.category,
        "adjust": metadata.adjust if metadata.adjust is not None else "none",
        "implementation": spec.implementation,
        "implementation_status": implementation_status(factor),
        "status": getattr(metadata, "status", spec.status),
        "source_type": getattr(metadata, "source_type", "document"),
        "source_group": group.source_id,
        "reference": group.reference,
        "adaptation": metadata_adaptation(metadata),
        "tags": list(spec.tags),
        "parameters_json": canonical_json(metadata_parameters(metadata)),
    }


def render_qha(contract: Mapping[str, Any]) -> str:
    lines = [
        f"version = {contract['version']}",
        f"name = {toml_string(contract['name'])}",
        f"frequency = {toml_string(contract['frequency'])}",
        f"formula = {toml_string(contract['formula'])}",
        f"inputs = {toml_string_list(contract['inputs'])}",
        f"min_window = {contract['min_window']}",
        f"direction = {toml_string(contract['direction'])}",
        f"category = {toml_string(contract['category'])}",
        f"adjust = {toml_string(contract['adjust'])}",
        f"implementation = {toml_string(contract['implementation'])}",
        "implementation_status = "
        f"{toml_string(contract['implementation_status'])}",
        f"status = {toml_string(contract['status'])}",
        f"source_type = {toml_string(contract['source_type'])}",
        f"source_group = {toml_string(contract['source_group'])}",
        f"reference = {toml_string(contract['reference'])}",
        f"adaptation = {toml_string(contract['adaptation'])}",
        f"tags = {toml_string_list(contract['tags'])}",
        f"parameters_json = {toml_string(contract['parameters_json'])}",
    ]
    return "\n".join(lines) + "\n"


def display_value(value: Any) -> str:
    if value is None:
        return "n/a"
    try:
        if pd.isna(value):
            return "n/a"
    except (TypeError, ValueError):
        pass
    if isinstance(value, float):
        if not math.isfinite(value):
            return "n/a"
        return format(value, ".12g")
    return str(value)


def factor_source_files(
    factor: Any,
    group: SourceGroup,
) -> tuple[SourceFile, ...]:
    wanted = set(factor_source_relatives(factor))
    selected = tuple(
        source for source in group.source_files if source.relative_path in wanted
    )
    if len(selected) != len(wanted):
        raise ValueError(f"factor source mapping is incomplete: {factor.spec.name}")
    return selected


def copy_source_files(
    output_root: Path,
    groups: tuple[SourceGroup, ...],
) -> dict[str, SourceFile]:
    source_files: dict[str, SourceFile] = {}
    for group in groups:
        for source in group.source_files:
            existing = source_files.get(source.relative_path)
            if existing is not None and existing.sha256 != source.sha256:
                raise ValueError(f"conflicting source bytes: {source.relative_path}")
            source_files[source.relative_path] = source
    for relative_path, source in sorted(source_files.items()):
        target = output_root / "sources" / PurePosixPath(relative_path)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source.path, target)
        if sha256_file(target) != source.sha256:
            raise ValueError(f"copied source hash mismatch: {relative_path}")
    return source_files


def render_idea(
    factor: Any,
    group: SourceGroup,
    basic_row: Mapping[str, Any] | None,
    evaluation_row: Mapping[str, Any] | None,
) -> str:
    metadata = factor.metadata
    spec = factor.spec
    pages = metadata_pages(metadata)
    sources = factor_source_files(factor, group)
    explanation = str(getattr(metadata, "beginner_explanation", "") or "未提供。")
    adaptation = metadata_adaptation(metadata) or "无。"
    parameters = canonical_json(metadata_parameters(metadata))
    lines = [
        f"# {spec.name}",
        "",
        "## 因子概览",
        "",
        f"- 类别：`{metadata.category}`",
        f"- 方向：`{metadata.direction}`",
        f"- 频率：`{spec.frequency}`",
        f"- 最小窗口：`{metadata.min_window}`",
        f"- 复权方式：`{metadata.adjust if metadata.adjust is not None else 'none'}`",
        f"- 实现状态：`{implementation_status(factor)}`",
        "",
        "## 公式",
        "",
        "```text",
        str(metadata.formula),
        "```",
        "",
        f"输入字段：`{', '.join(metadata.inputs)}`",
        "",
        "## 原理说明",
        "",
        explanation,
        "",
        "## 来源",
        "",
        f"- 逻辑来源组：`{group.source_id}`",
        f"- 来源组指纹：`{group.reference}`",
    ]
    for source in sources:
        lines.append(
            f"- `{source.relative_path}` — SHA-256 `{source.sha256}`"
        )
        lines.append(f"  - 归档副本：`../../sources/{source.relative_path}`")
        if not source.inventory_matches:
            lines.append(
                "  - 历史库存 SHA-256："
                f"`{source.inventory_sha256}`（当前文件内容已变化）"
            )
    lines.extend(
        [
            f"- 来源页码：`{', '.join(map(str, pages)) if pages else '未记录'}`",
            "",
            "## 复现实现",
            "",
            f"- Python 实现：`{spec.implementation}`",
            f"- 默认参数：`{parameters}`",
            f"- 适配说明：{adaptation}",
            "",
            "## 发布与评估",
            "",
        ]
    )
    if basic_row is None or evaluation_row is None:
        lines.extend(
            [
                "- Publication status: `unpublished`",
                "- Evaluation status: `not_evaluated`",
                "- 当前没有固化版本或正式评估记录；本归档不推断评估结论。",
            ]
        )
    else:
        status = str(evaluation_row["status"])
        lines.extend(
            [
                "- Publication status: `published`",
                f"- Evaluation status: `{status}`",
                f"- 因子版本：`{basic_row['version_id']}`",
                f"- 数据快照：`{basic_row['snapshot_id']}`",
                f"- 评估批次：`{evaluation_row['run_id']}`",
                "- 有效区间："
                f"`{format_date(evaluation_row['start_date'])}` 至 "
                f"`{format_date(evaluation_row['end_date'])}`",
                "",
                "### 核心指标",
                "",
                f"- Rank IC Mean：`{display_value(evaluation_row.get('rank_ic_mean'))}`",
                f"- Rank ICIR：`{display_value(evaluation_row.get('rank_icir'))}`",
                f"- Adjusted ICIR：`{display_value(evaluation_row.get('adjusted_ICIR'))}`",
                "- Long-short spread (bps)："
                f"`{display_value(evaluation_row.get('long_short_spread_bps'))}`",
                f"- Monotonicity：`{display_value(evaluation_row.get('monotonicity'))}`",
                f"- Coverage：`{display_value(evaluation_row.get('coverage'))}`",
                "- Daily turnover (long)："
                f"`{display_value(evaluation_row.get('turnover_daily_long'))}`",
                "- Daily turnover (short)："
                f"`{display_value(evaluation_row.get('turnover_daily_short'))}`",
            ]
        )
    return "\n".join(lines) + "\n"


def compute_manifest_snapshot(
    records: list[tuple[str, bytes, bytes]],
) -> str:
    payload = b"".join(
        (
            name.encode("utf-8")
            + b"\0"
            + sha256_bytes(qha_bytes).encode("ascii")
            + b"\0"
            + sha256_bytes(idea_bytes).encode("ascii")
            + b"\n"
        )
        for name, qha_bytes, idea_bytes in sorted(records)
    )
    return sha256_bytes(payload)


def render_manifest(group: SourceGroup, snapshot: str) -> str:
    lines = [
        "version = 1",
        f"name = {toml_string(group.source_id + '-v1')}",
        f"snapshot = {toml_string(snapshot)}",
        f"reference = {toml_string(group.reference)}",
        'contract = "../../configs/evaluation/daily-v1.toml"',
        f"start = {toml_string(EXPECTED_START)}",
        f"end = {toml_string(EXPECTED_END)}",
    ]
    for factor in group.factors:
        name = factor.spec.name
        lines.extend(
            [
                "",
                "[[factors]]",
                f"name = {toml_string(name)}",
                f"formula = {toml_string('../../factors/daily/' + name + '.qha')}",
                f"idea = {toml_string('IDEA-' + name + '.md')}",
            ]
        )
    return "\n".join(lines) + "\n"


def render_contract(inputs: ArchiveInputs) -> str:
    run = inputs.run
    config = inputs.run_config
    lines = [
        "version = 1",
        'name = "daily-v1"',
        f"requested_start = {toml_string(format_date(config['start_date']))}",
        f"effective_start = {toml_string(EXPECTED_START)}",
        f"effective_end = {toml_string(EXPECTED_END)}",
        f"source_data_end = {toml_string(EXPECTED_SOURCE_END)}",
        f"snapshot_id = {toml_string(EXPECTED_SNAPSHOT_ID)}",
        f"evaluation_run_id = {toml_string(EXPECTED_RUN_ID)}",
        f"metrics_version = {toml_string(run['metrics_version'])}",
        f"whitelist_fingerprint = {toml_string(run['whitelist_fingerprint'])}",
        f"universe = {toml_string(config['universe'])}",
        f"period = {int(config['period'])}",
        f"quantiles = {int(config['quantiles'])}",
        f"return_type = {toml_string(config['return_type'])}",
        f"transaction_cost_bps = {float(config['transaction_cost_bps'])}",
        f"max_loss = {float(config['max_loss'])}",
        f"rolling_ic_window = {int(config['rolling_ic_window'])}",
        f"autocorrelation_lag = {int(config['autocorrelation_lag'])}",
        f"factor_count = {EXPECTED_PUBLISHED_COUNT}",
        f"passed_count = {EXPECTED_PASSED_COUNT}",
        f"rejected_count = {EXPECTED_REJECTED_COUNT}",
    ]
    return "\n".join(lines) + "\n"


def evaluation_csv_bytes(evaluation: pd.DataFrame) -> bytes:
    columns = [
        column
        for column in evaluation.columns
        if column not in EVALUATION_PATH_COLUMNS
    ]
    clean = evaluation.loc[:, columns].sort_values("factor_name").reset_index(drop=True)
    text = clean.to_csv(index=False, lineterminator="\n", float_format="%.17g")
    return text.encode("utf-8")


def compute_root_reference(groups: tuple[SourceGroup, ...]) -> str:
    payload = "".join(
        f"{group.source_id}\0{group.reference}\n" for group in groups
    ).encode("utf-8")
    return sha256_bytes(payload)


def compute_root_snapshot(
    contract_bytes: bytes,
    evaluation_bytes: bytes,
    archives: list[Mapping[str, Any]],
) -> str:
    payload = (
        f"contract\0{sha256_bytes(contract_bytes)}\n"
        f"evaluation\0{sha256_bytes(evaluation_bytes)}\n"
        + "".join(
            f"{item['source_id']}\0{item['reference']}\0{item['snapshot']}\n"
            for item in sorted(archives, key=lambda archive: archive["source_id"])
        )
    ).encode("utf-8")
    return sha256_bytes(payload)


def render_archive_index(
    root_snapshot: str,
    root_reference: str,
    contract_bytes: bytes,
    evaluation_bytes: bytes,
    archives: list[Mapping[str, Any]],
    source_files: Mapping[str, SourceFile],
) -> str:
    lines = [
        "version = 1",
        'name = "document-factors-v1"',
        f"snapshot = {toml_string(root_snapshot)}",
        f"reference = {toml_string(root_reference)}",
        'contract = "configs/evaluation/daily-v1.toml"',
        f"contract_sha256 = {toml_string(sha256_bytes(contract_bytes))}",
        'evaluation = "evaluations/factor-evaluation.csv"',
        f"evaluation_sha256 = {toml_string(sha256_bytes(evaluation_bytes))}",
        'sources = "sources"',
        f"source_file_count = {len(source_files)}",
        "source_bytes = "
        f"{sum(source.path.stat().st_size for source in source_files.values())}",
        f"evaluation_run_id = {toml_string(EXPECTED_RUN_ID)}",
        f"factor_snapshot_id = {toml_string(EXPECTED_SNAPSHOT_ID)}",
        f"start = {toml_string(EXPECTED_START)}",
        f"end = {toml_string(EXPECTED_END)}",
        f"factor_count = {EXPECTED_FACTOR_COUNT}",
        f"source_count = {EXPECTED_SOURCE_COUNT}",
        f"exact_count = {EXPECTED_EXACT_COUNT}",
        f"approximate_count = {EXPECTED_APPROXIMATE_COUNT}",
        f"published_count = {EXPECTED_PUBLISHED_COUNT}",
        f"passed_count = {EXPECTED_PASSED_COUNT}",
        f"rejected_count = {EXPECTED_REJECTED_COUNT}",
        f"unpublished_count = {EXPECTED_UNPUBLISHED_COUNT}",
    ]
    for item in sorted(archives, key=lambda archive: archive["source_id"]):
        lines.extend(
            [
                "",
                "[[archives]]",
                f"name = {toml_string(item['name'])}",
                f"manifest = {toml_string(item['manifest'])}",
                f"factor_count = {item['factor_count']}",
                f"snapshot = {toml_string(item['snapshot'])}",
                f"reference = {toml_string(item['reference'])}",
            ]
        )
    return "\n".join(lines) + "\n"


def load_inputs() -> ArchiveInputs:
    sys.path.insert(0, str(MICROFACTOR_ROOT))
    sys.path.insert(0, str(FACTOREVAL_ROOT / "src"))
    from factoreval import factor_api
    from microfactor.factors.document_factors import document_all_factors

    factors = tuple(document_all_factors())
    names = [factor.spec.name for factor in factors]
    if len(factors) != EXPECTED_FACTOR_COUNT or len(set(names)) != len(names):
        raise ValueError("document factor registry is not the expected 393 unique factors")
    status_counts = Counter(implementation_status(factor) for factor in factors)
    if status_counts != Counter(
        exact=EXPECTED_EXACT_COUNT,
        approximate=EXPECTED_APPROXIMATE_COUNT,
    ):
        raise ValueError(f"unexpected implementation status counts: {status_counts}")

    api = factor_api(FACTOREVAL_ROOT / "config" / "settings.toml")
    basic = api.factor_basic()
    evaluation = api.factor_evaluation(run_id=EXPECTED_RUN_ID)
    runs = api.factor_runs()
    run_rows = runs[runs["run_id"] == EXPECTED_RUN_ID]
    if len(run_rows) != 1:
        raise ValueError(f"expected one evaluation run {EXPECTED_RUN_ID}")
    run = run_rows.iloc[0].to_dict()
    if run["status"] != "completed":
        raise ValueError(f"evaluation run is not completed: {run['status']}")
    if len(basic) != EXPECTED_PUBLISHED_COUNT:
        raise ValueError(f"expected 332 published factors, found {len(basic)}")
    if len(evaluation) != EXPECTED_PUBLISHED_COUNT:
        raise ValueError(f"expected 332 evaluations, found {len(evaluation)}")
    snapshot_ids = set(basic["snapshot_id"].dropna().astype(str))
    if snapshot_ids != {EXPECTED_SNAPSHOT_ID}:
        raise ValueError(f"unexpected current snapshot: {snapshot_ids}")
    if str(run["snapshot_id"]) != EXPECTED_SNAPSHOT_ID:
        raise ValueError(f"run snapshot changed: {run['snapshot_id']}")
    evaluation_runs = set(basic["evaluation_run_id"].dropna().astype(str))
    if evaluation_runs != {EXPECTED_RUN_ID}:
        raise ValueError(f"unexpected evaluation run linkage: {evaluation_runs}")
    status_counts = Counter(evaluation["status"].astype(str))
    if status_counts != Counter(
        passed=EXPECTED_PASSED_COUNT,
        rejected=EXPECTED_REJECTED_COUNT,
    ):
        raise ValueError(f"unexpected evaluation status counts: {status_counts}")
    if format_date(evaluation["start_date"].min()) != EXPECTED_START:
        raise ValueError("evaluation start date changed")
    if format_date(evaluation["end_date"].max()) != EXPECTED_END:
        raise ValueError("evaluation end date changed")
    if format_date(basic["end_date"].max()) != EXPECTED_SOURCE_END:
        raise ValueError("source data end date changed")
    registry_names = set(names)
    published_names = set(basic["factor_name"].astype(str))
    evaluation_names = set(evaluation["factor_name"].astype(str))
    if not published_names <= registry_names or evaluation_names != published_names:
        raise ValueError("published/evaluated factors do not match the document registry")
    if len(registry_names - published_names) != EXPECTED_UNPUBLISHED_COUNT:
        raise ValueError("unexpected unpublished factor count")
    run_config = json.loads(str(run["config_json"]))
    return ArchiveInputs(
        factors=factors,
        basic=basic,
        evaluation=evaluation,
        run=run,
        run_config=run_config,
        inventory=load_inventory(),
    )


def build_archive(output_root: Path, quiet: bool = False) -> Mapping[str, Any]:
    output_root = output_root.resolve()
    inputs = load_inputs()
    groups = build_source_groups(inputs.factors, inputs.inventory)
    basic_rows = {
        str(row["factor_name"]): row
        for row in inputs.basic.to_dict(orient="records")
    }
    evaluation_rows = {
        str(row["factor_name"]): row
        for row in inputs.evaluation.to_dict(orient="records")
    }
    clean_output(output_root)
    source_files = copy_source_files(output_root, groups)

    contract = render_contract(inputs).encode("utf-8")
    evaluation_bytes = evaluation_csv_bytes(inputs.evaluation)
    write_text(
        output_root / "configs" / "evaluation" / "daily-v1.toml",
        contract.decode("utf-8"),
    )
    write_text(
        output_root / "evaluations" / "factor-evaluation.csv",
        evaluation_bytes.decode("utf-8"),
    )

    archives: list[Mapping[str, Any]] = []
    written_names: set[str] = set()
    for group in groups:
        artifact_records: list[tuple[str, bytes, bytes]] = []
        group_dir = output_root / "archives" / group.source_id
        for factor in group.factors:
            name = factor.spec.name
            if name in written_names:
                raise ValueError(f"factor appears in multiple source groups: {name}")
            written_names.add(name)
            qha = render_qha(factor_contract(factor, group)).encode("utf-8")
            idea = render_idea(
                factor,
                group,
                basic_rows.get(name),
                evaluation_rows.get(name),
            ).encode("utf-8")
            write_text(
                output_root / "factors" / "daily" / f"{name}.qha",
                qha.decode("utf-8"),
            )
            write_text(
                group_dir / f"IDEA-{name}.md",
                idea.decode("utf-8"),
            )
            artifact_records.append((name, qha, idea))
        snapshot = compute_manifest_snapshot(artifact_records)
        manifest = render_manifest(group, snapshot)
        write_text(group_dir / "manifest.toml", manifest)
        archives.append(
            {
                "source_id": group.source_id,
                "name": group.source_id + "-v1",
                "manifest": f"archives/{group.source_id}/manifest.toml",
                "factor_count": len(group.factors),
                "snapshot": snapshot,
                "reference": group.reference,
            }
        )
    if len(written_names) != EXPECTED_FACTOR_COUNT:
        raise ValueError(f"expected 393 written factors, found {len(written_names)}")

    root_reference = compute_root_reference(groups)
    root_snapshot = compute_root_snapshot(contract, evaluation_bytes, archives)
    index = render_archive_index(
        root_snapshot,
        root_reference,
        contract,
        evaluation_bytes,
        archives,
        source_files,
    )
    write_text(output_root / "archive.toml", index)
    summary = {
        "output": str(output_root),
        "factor_count": len(written_names),
        "source_count": len(groups),
        "source_file_count": len(source_files),
        "source_bytes": sum(
            source.path.stat().st_size for source in source_files.values()
        ),
        "published_count": len(basic_rows),
        "passed_count": EXPECTED_PASSED_COUNT,
        "rejected_count": EXPECTED_REJECTED_COUNT,
        "unpublished_count": EXPECTED_UNPUBLISHED_COUNT,
        "snapshot": root_snapshot,
        "reference": root_reference,
    }
    if not quiet:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    return summary


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build the fixed document factor archive.")
    parser.add_argument("--output", type=Path, default=PROJECT_ROOT)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    build_archive(args.output)


if __name__ == "__main__":
    main()
