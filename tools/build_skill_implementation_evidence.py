#!/usr/bin/env python3
"""Build a deterministic evidence matrix for active Base Skills."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = Path("skills/SKILL_REGISTRY.json")
EVAL_PATHS = (
    Path("skills/SKILL_BEHAVIOR_EVALS.json"),
    Path("skills/SKILL_BEHAVIOR_COVERAGE_EVALS.json"),
)
EVIDENCE_INDEX_PATH = Path("skills/SKILL_IMPLEMENTATION_EVIDENCE.json")
OUTPUT_PATH = Path("docs/generated/BASE_SKILL_IMPLEMENTATION_EVIDENCE.md")
EXECUTABLE_KINDS = {"TEST", "TOOL", "WORKFLOW", "SCRIPT"}
ALLOWED_KINDS = EXECUTABLE_KINDS | {"CONTRACT"}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_cases(root: Path) -> tuple[list[dict[str, Any]], str]:
    cases: list[dict[str, Any]] = []
    model_run_status = "NOT_RUN"
    for relative in EVAL_PATHS:
        path = root / relative
        if not path.is_file():
            continue
        document = load_json(path)
        cases.extend(document.get("cases", []))
        if relative == EVAL_PATHS[0]:
            model_run_status = document.get("model_run_status", "NOT_RUN")
    return cases, model_run_status


def behavior_source_digest(root: Path) -> str:
    digest = hashlib.sha256()
    for relative in EVAL_PATHS:
        path = root / relative
        if not path.is_file():
            continue
        digest.update(relative.as_posix().encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes().replace(b"\r\n", b"\n"))
        digest.update(b"\0")
    return digest.hexdigest()


def behavior_coverage(
    active_ids: list[str],
    cases: list[dict[str, Any]],
) -> dict[str, dict[str, int]]:
    coverage = {
        skill_id: {"primary": 0, "supporting": 0, "forbidden": 0}
        for skill_id in active_ids
    }
    for case in cases:
        primary = case.get("expected_primary_skill")
        if primary in coverage:
            coverage[primary]["primary"] += 1
        for skill_id in case.get("expected_supporting_skills", []):
            if skill_id in coverage:
                coverage[skill_id]["supporting"] += 1
        for skill_id in case.get("forbidden_skills", []):
            if skill_id in coverage:
                coverage[skill_id]["forbidden"] += 1
    return coverage


def validate_evidence_index(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    try:
        registry = load_json(root / REGISTRY_PATH)
        index = load_json(root / EVIDENCE_INDEX_PATH)
        cases, _ = load_cases(root)
    except (OSError, json.JSONDecodeError) as error:
        return [f"evidence input unavailable or invalid: {error}"]

    if index.get("schema_version") != 1:
        errors.append("evidence index schema_version must be 1")
    if index.get("artifact_role") != "BASE_SKILL_IMPLEMENTATION_EVIDENCE_INDEX":
        errors.append(
            "evidence index artifact_role must be BASE_SKILL_IMPLEMENTATION_EVIDENCE_INDEX"
        )
    if not isinstance(index.get("entries"), list):
        errors.append("evidence index entries must be a list")
        return errors

    active = [
        entry
        for entry in registry.get("skills", [])
        if entry.get("status") == "ACTIVE"
    ]
    active_ids = [entry["skill_id"] for entry in active]
    indexed: dict[str, dict[str, Any]] = {}
    for entry in index.get("entries", []):
        skill_id = entry.get("skill_id")
        if not isinstance(skill_id, str):
            errors.append("evidence index entry requires a string skill_id")
            continue
        if skill_id in indexed:
            errors.append(f"duplicate evidence index entry: {skill_id}")
        indexed[skill_id] = entry

    for skill_id in active_ids:
        if skill_id not in indexed:
            errors.append(f"missing evidence index entry: {skill_id}")
    for skill_id in sorted(set(indexed) - set(active_ids)):
        errors.append(f"evidence index contains non-active Skill: {skill_id}")

    coverage = behavior_coverage(active_ids, cases)
    for registry_entry in active:
        skill_id = registry_entry["skill_id"]
        package = root / registry_entry["path"]
        if not package.is_file():
            errors.append(
                f"Skill package missing: {skill_id} -> {registry_entry['path']}"
            )
        counts = coverage[skill_id]
        if counts["primary"] == 0:
            errors.append(f"primary behavior evidence missing: {skill_id}")
        if counts["forbidden"] == 0:
            errors.append(f"non-selection behavior evidence missing: {skill_id}")
        evidence_entry = indexed.get(skill_id)
        if evidence_entry is None:
            continue
        evidence = evidence_entry.get("evidence")
        if not isinstance(evidence, list) or not evidence:
            errors.append(f"evidence paths missing: {skill_id}")
            continue
        for item in evidence:
            if not isinstance(item, dict):
                errors.append(f"invalid evidence record: {skill_id}")
                continue
            kind = item.get("kind")
            path = item.get("path")
            if kind not in ALLOWED_KINDS:
                errors.append(f"invalid evidence kind for {skill_id}: {kind}")
            if not isinstance(path, str) or not path:
                errors.append(f"invalid evidence path for {skill_id}")
            elif not (root / path).is_file():
                errors.append(f"evidence path missing for {skill_id}: {path}")
    return errors


def evidence_class(
    evidence_entry: dict[str, Any] | None,
    primary_count: int,
    forbidden_count: int,
    package_exists: bool,
) -> str:
    if (
        evidence_entry is None
        or not package_exists
        or primary_count == 0
        or forbidden_count == 0
        or not evidence_entry.get("evidence")
    ):
        return "MISSING_EVIDENCE"
    kinds = {
        item.get("kind")
        for item in evidence_entry.get("evidence", [])
        if isinstance(item, dict)
    }
    if kinds & EXECUTABLE_KINDS:
        return "EXECUTABLE_EVIDENCE"
    return "CONTRACT_EVIDENCE"


def build_evidence_markdown(root: Path = ROOT) -> str:
    errors = validate_evidence_index(root)
    if errors:
        raise ValueError("\n".join(errors))

    registry = load_json(root / REGISTRY_PATH)
    index = load_json(root / EVIDENCE_INDEX_PATH)
    cases, model_run_status = load_cases(root)
    behavior_digest = behavior_source_digest(root)
    active = [
        entry
        for entry in registry.get("skills", [])
        if entry.get("status") == "ACTIVE"
    ]
    active_ids = [entry["skill_id"] for entry in active]
    coverage = behavior_coverage(active_ids, cases)
    indexed = {entry["skill_id"]: entry for entry in index["entries"]}

    lines = [
        "# Base Skill Implementation Evidence",
        "",
        "> Generated from `skills/SKILL_REGISTRY.json`, behavior evaluation sets, and `skills/SKILL_IMPLEMENTATION_EVIDENCE.json`. Do not edit this derivative.",
        f"> Active Skill count: `{len(active)}`",
        f"> External model behavior run: `{model_run_status}`",
        f"> Behavior evaluation case count: `{len(cases)}`",
        f"> Behavior evaluation source SHA-256: `{behavior_digest}`",
        "",
        "`EXECUTABLE_EVIDENCE` means a repository test, tool, workflow, or package script is linked. It does not mean that evidence passed on the current commit. `CONTRACT_EVIDENCE` means only a contract or documentation consumer is linked. Actual model, runtime, device, and human validation remain separate.",
        "",
        "| Skill | Owner | Primary behavior | Non-selection behavior | Evidence class | Repository evidence |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for registry_entry in active:
        skill_id = registry_entry["skill_id"]
        counts = coverage[skill_id]
        evidence_entry = indexed[skill_id]
        classification = evidence_class(
            evidence_entry,
            counts["primary"],
            counts["forbidden"],
            (root / registry_entry["path"]).is_file(),
        )
        evidence_text = "<br>".join(
            f"{item['kind']}: `{item['path']}`"
            for item in evidence_entry["evidence"]
        )
        lines.append(
            f"| `{skill_id}` | {registry_entry['discipline']} | "
            f"{'PASS' if counts['primary'] else 'MISSING'} | "
            f"{'PASS' if counts['forbidden'] else 'MISSING'} | "
            f"{classification} | {evidence_text} |"
        )
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--output", type=Path, default=OUTPUT_PATH)
    parser.add_argument("--check", action="store_true")
    arguments = parser.parse_args()
    root = arguments.root.resolve()
    output = arguments.output
    if not output.is_absolute():
        output = root / output
    try:
        markdown = build_evidence_markdown(root)
    except ValueError as error:
        print("EVIDENCE_STATUS: FAIL")
        for message in str(error).splitlines():
            print(f"- {message}")
        return 1
    if arguments.check:
        if not output.is_file():
            print(f"EVIDENCE_STATUS: FAIL\n- generated evidence missing: {output}")
            return 1
        if output.read_text(encoding="utf-8") != markdown:
            print("EVIDENCE_STATUS: FAIL\n- generated evidence is stale")
            return 1
        print("EVIDENCE_STATUS: PASS")
        return 0
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(markdown, encoding="utf-8")
    print(f"EVIDENCE_STATUS: WRITTEN {output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
