from __future__ import annotations

import csv
import json
import tempfile
import tomllib
from collections import Counter
from pathlib import Path
from typing import Any

import build_archive as builder

TOOLS_ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = TOOLS_ROOT.parent

MANIFEST_KEYS = {
    "version",
    "name",
    "snapshot",
    "reference",
    "contract",
    "start",
    "end",
    "factors",
}
FACTOR_ENTRY_KEYS = {"name", "formula", "idea"}
QHA_KEYS = {
    "version",
    "name",
    "frequency",
    "formula",
    "inputs",
    "min_window",
    "direction",
    "category",
    "adjust",
    "implementation",
    "implementation_status",
    "status",
    "source_type",
    "source_group",
    "reference",
    "adaptation",
    "tags",
    "parameters_json",
}


def load_toml(path: Path) -> dict[str, Any]:
    with path.open("rb") as handle:
        return tomllib.load(handle)


def managed_files(root: Path) -> dict[str, bytes]:
    result: dict[str, bytes] = {}
    for relative in builder.MANAGED_PATHS:
        path = root / relative
        if path.is_file():
            result[relative] = path.read_bytes()
        elif path.is_dir():
            for file_path in sorted(item for item in path.rglob("*") if item.is_file()):
                result[file_path.relative_to(root).as_posix()] = file_path.read_bytes()
    return result


def validate_archive(root: Path) -> dict[str, Any]:
    root = root.resolve()
    inputs = builder.load_inputs()
    groups = builder.build_source_groups(inputs.factors, inputs.inventory)
    group_by_id = {group.source_id: group for group in groups}
    factor_by_name = {factor.spec.name: factor for factor in inputs.factors}

    index = load_toml(root / "archive.toml")
    if index["factor_count"] != builder.EXPECTED_FACTOR_COUNT:
        raise ValueError("root factor count is incorrect")
    if index["source_count"] != builder.EXPECTED_SOURCE_COUNT:
        raise ValueError("root source count is incorrect")
    if len(index["archives"]) != builder.EXPECTED_SOURCE_COUNT:
        raise ValueError("root archive list is incomplete")

    source_files = {
        source.relative_path: source
        for group in groups
        for source in group.source_files
    }
    if index["source_file_count"] != len(source_files):
        raise ValueError("root source file count is incorrect")
    expected_source_bytes = sum(
        source.path.stat().st_size for source in source_files.values()
    )
    if index["source_bytes"] != expected_source_bytes:
        raise ValueError("root source byte count is incorrect")
    copied_source_root = root / index["sources"]
    for relative_path, source in source_files.items():
        copied = copied_source_root.joinpath(*Path(relative_path).parts)
        if not copied.is_file():
            raise ValueError(f"copied source is missing: {relative_path}")
        if builder.sha256_file(copied) != source.sha256:
            raise ValueError(f"copied source hash mismatch: {relative_path}")
        if copied.stat().st_mtime_ns != source.path.stat().st_mtime_ns:
            raise ValueError(f"copied source timestamp mismatch: {relative_path}")

    contract_path = root / index["contract"]
    evaluation_path = root / index["evaluation"]
    contract_bytes = contract_path.read_bytes()
    evaluation_bytes = evaluation_path.read_bytes()
    if builder.sha256_bytes(contract_bytes) != index["contract_sha256"]:
        raise ValueError("contract hash mismatch")
    if builder.sha256_bytes(evaluation_bytes) != index["evaluation_sha256"]:
        raise ValueError("evaluation CSV hash mismatch")

    contract = load_toml(contract_path)
    if contract["snapshot_id"] != builder.EXPECTED_SNAPSHOT_ID:
        raise ValueError("contract snapshot mismatch")
    if contract["evaluation_run_id"] != builder.EXPECTED_RUN_ID:
        raise ValueError("contract run mismatch")
    if contract["effective_start"] != builder.EXPECTED_START:
        raise ValueError("contract start mismatch")
    if contract["effective_end"] != builder.EXPECTED_END:
        raise ValueError("contract end mismatch")

    with evaluation_path.open("r", encoding="utf-8", newline="") as handle:
        evaluation_rows = list(csv.DictReader(handle))
    if len(evaluation_rows) != builder.EXPECTED_PUBLISHED_COUNT:
        raise ValueError("evaluation CSV row count mismatch")
    evaluation_status = Counter(row["status"] for row in evaluation_rows)
    if evaluation_status != Counter(
        passed=builder.EXPECTED_PASSED_COUNT,
        rejected=builder.EXPECTED_REJECTED_COUNT,
    ):
        raise ValueError(f"evaluation CSV status mismatch: {evaluation_status}")
    if {row["run_id"] for row in evaluation_rows} != {builder.EXPECTED_RUN_ID}:
        raise ValueError("evaluation CSV run mismatch")
    if {row["snapshot_id"] for row in evaluation_rows} != {
        builder.EXPECTED_SNAPSHOT_ID
    }:
        raise ValueError("evaluation CSV snapshot mismatch")

    manifest_records: list[dict[str, Any]] = []
    factor_names: list[str] = []
    publication_status = Counter()
    evaluation_idea_status = Counter()
    for archive_entry in index["archives"]:
        manifest_path = root / archive_entry["manifest"]
        manifest = load_toml(manifest_path)
        if set(manifest) != MANIFEST_KEYS:
            raise ValueError(f"unexpected manifest keys: {manifest_path}")
        if manifest["contract"] != "../../configs/evaluation/daily-v1.toml":
            raise ValueError(f"manifest contract mismatch: {manifest_path}")
        if manifest["start"] != builder.EXPECTED_START:
            raise ValueError(f"manifest start mismatch: {manifest_path}")
        if manifest["end"] != builder.EXPECTED_END:
            raise ValueError(f"manifest end mismatch: {manifest_path}")
        source_id = manifest_path.parent.name
        group = group_by_id.get(source_id)
        if group is None:
            raise ValueError(f"unknown source group: {source_id}")
        if manifest["reference"] != group.reference:
            raise ValueError(f"source reference mismatch: {source_id}")
        if archive_entry["reference"] != group.reference:
            raise ValueError(f"root source reference mismatch: {source_id}")
        if len(manifest["factors"]) != archive_entry["factor_count"]:
            raise ValueError(f"factor count mismatch: {source_id}")

        artifact_records: list[tuple[str, bytes, bytes]] = []
        for factor_entry in manifest["factors"]:
            if set(factor_entry) != FACTOR_ENTRY_KEYS:
                raise ValueError(f"unexpected factor entry keys: {source_id}")
            name = factor_entry["name"]
            if "\\_" in name:
                raise ValueError(f"escaped underscore in factor name: {name}")
            factor = factor_by_name.get(name)
            if factor is None:
                raise ValueError(f"unknown archived factor: {name}")
            qha_path = (manifest_path.parent / factor_entry["formula"]).resolve()
            idea_path = (manifest_path.parent / factor_entry["idea"]).resolve()
            qha_bytes = qha_path.read_bytes()
            idea_bytes = idea_path.read_bytes()
            qha = load_toml(qha_path)
            if set(qha) != QHA_KEYS:
                raise ValueError(f"unexpected QHA keys: {qha_path}")
            expected_contract = builder.factor_contract(factor, group)
            for key, expected in expected_contract.items():
                if qha[key] != expected:
                    raise ValueError(f"QHA mismatch for {name}: {key}")
            idea = idea_bytes.decode("utf-8")
            if "Publication status: `published`" in idea:
                publication_status["published"] += 1
            elif "Publication status: `unpublished`" in idea:
                publication_status["unpublished"] += 1
            else:
                raise ValueError(f"missing publication status: {idea_path}")
            matched_evaluation_status = False
            for status in ("passed", "rejected", "not_evaluated"):
                if f"Evaluation status: `{status}`" in idea:
                    evaluation_idea_status[status] += 1
                    matched_evaluation_status = True
                    break
            if not matched_evaluation_status:
                raise ValueError(f"missing evaluation status: {idea_path}")
            artifact_records.append((name, qha_bytes, idea_bytes))
            factor_names.append(name)

        snapshot = builder.compute_manifest_snapshot(artifact_records)
        if snapshot != manifest["snapshot"]:
            raise ValueError(f"manifest snapshot mismatch: {source_id}")
        if archive_entry["snapshot"] != snapshot:
            raise ValueError(f"root manifest snapshot mismatch: {source_id}")
        manifest_records.append(
            {
                "source_id": source_id,
                "reference": group.reference,
                "snapshot": snapshot,
            }
        )

    if len(factor_names) != builder.EXPECTED_FACTOR_COUNT:
        raise ValueError("archived factor count mismatch")
    if len(set(factor_names)) != builder.EXPECTED_FACTOR_COUNT:
        raise ValueError("duplicate archived factors")
    if set(factor_names) != set(factor_by_name):
        raise ValueError("archive factor set does not match registry")
    if publication_status != Counter(
        published=builder.EXPECTED_PUBLISHED_COUNT,
        unpublished=builder.EXPECTED_UNPUBLISHED_COUNT,
    ):
        raise ValueError(f"IDEA publication status mismatch: {publication_status}")
    if evaluation_idea_status != Counter(
        passed=builder.EXPECTED_PASSED_COUNT,
        rejected=builder.EXPECTED_REJECTED_COUNT,
        not_evaluated=builder.EXPECTED_UNPUBLISHED_COUNT,
    ):
        raise ValueError(f"IDEA evaluation status mismatch: {evaluation_idea_status}")

    expected_reference = builder.compute_root_reference(groups)
    if index["reference"] != expected_reference:
        raise ValueError("root reference mismatch")
    expected_snapshot = builder.compute_root_snapshot(
        contract_bytes,
        evaluation_bytes,
        manifest_records,
    )
    if index["snapshot"] != expected_snapshot:
        raise ValueError("root snapshot mismatch")
    return {
        "factor_count": len(factor_names),
        "source_count": len(index["archives"]),
        "source_file_count": len(source_files),
        "source_bytes": expected_source_bytes,
        "publication_status": dict(publication_status),
        "evaluation_status": dict(evaluation_idea_status),
        "snapshot": expected_snapshot,
        "reference": expected_reference,
    }


def validate_determinism(root: Path) -> None:
    with tempfile.TemporaryDirectory(prefix="factorarchive-a-") as first_dir:
        with tempfile.TemporaryDirectory(prefix="factorarchive-b-") as second_dir:
            first = Path(first_dir)
            second = Path(second_dir)
            builder.build_archive(first, quiet=True)
            builder.build_archive(second, quiet=True)
            first_files = managed_files(first)
            second_files = managed_files(second)
            actual_files = managed_files(root)
            if first_files != second_files:
                raise ValueError("two temporary builds are not byte-identical")
            if actual_files != first_files:
                raise ValueError("checked-in archive differs from a fresh build")


def main() -> None:
    summary = validate_archive(PROJECT_ROOT)
    validate_determinism(PROJECT_ROOT)
    summary["deterministic_rebuild"] = True
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
