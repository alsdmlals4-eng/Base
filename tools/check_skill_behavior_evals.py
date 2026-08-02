#!/usr/bin/env python3
"""Validate Base Skill behavior fixtures and score externally produced routing results."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = Path("skills/SKILL_REGISTRY.json")
EVAL_PATH = Path("skills/SKILL_BEHAVIOR_EVALS.json")
COVERAGE_EVAL_PATH = Path("skills/SKILL_BEHAVIOR_COVERAGE_EVALS.json")
SCHEMA_PATH = Path("schemas/skill-behavior-eval-v1.schema.json")
RESULT_SCHEMA_PATH = Path("schemas/skill-behavior-results-v1.schema.json")


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def evaluation_paths(root: Path = ROOT) -> list[Path]:
    paths = [EVAL_PATH]
    if (root / COVERAGE_EVAL_PATH).is_file():
        paths.append(COVERAGE_EVAL_PATH)
    return paths


def evaluation_sha256(root: Path = ROOT) -> str:
    hasher = hashlib.sha256()
    for relative in evaluation_paths(root):
        hasher.update(relative.as_posix().encode("utf-8"))
        hasher.update(b"\0")
        hasher.update((root / relative).read_bytes())
        hasher.update(b"\0")
    return hasher.hexdigest()


def current_commit(root: Path = ROOT) -> str | None:
    try:
        return subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=root,
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        ).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def validate_result_identity(root: Path, results: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    try:
        schema = load_json(root / RESULT_SCHEMA_PATH)
    except (OSError, json.JSONDecodeError) as error:
        return [f"result schema unavailable or invalid: {error}"]
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    for error in sorted(
        validator.iter_errors(results),
        key=lambda item: list(item.path),
    ):
        location = ".".join(str(part) for part in error.path) or "<root>"
        errors.append(f"result schema {location}: {error.message}")
    if errors:
        return errors
    if results.get("run_status") != "COMPLETED":
        errors.append("result run_status must be COMPLETED for scoring")
    model = results.get("model", {})
    review = results.get("review", {})
    required_metadata = [
        model.get("provider"),
        model.get("model"),
        model.get("version"),
        review.get("author_context_id"),
        review.get("reviewer_context_id"),
    ]
    if any(
        isinstance(value, str) and value.strip().casefold() == "unset"
        for value in required_metadata
    ):
        errors.append("completed result contains placeholder model metadata")
    commit = current_commit(root)
    if commit is None:
        errors.append("current repository commit is unavailable")
    elif results.get("commit_sha") != commit:
        errors.append("result commit SHA does not match current repository HEAD")
    source = results.get("source_identity", {})
    registry_path = root / REGISTRY_PATH
    if source.get("registry_sha256") != file_sha256(registry_path):
        errors.append("result registry SHA-256 does not match current source")
    expected_eval_paths = [path.as_posix() for path in evaluation_paths(root)]
    if source.get("evaluation_paths") != expected_eval_paths:
        errors.append("result evaluation paths do not match current sources")
    if source.get("evaluation_sha256") != evaluation_sha256(root):
        errors.append("result evaluation SHA-256 does not match current source")
    if (
        not review.get("independent")
        or review.get("author_context_id") == review.get("reviewer_context_id")
    ):
        errors.append("result review context is not independent")
    return errors


def validate_eval_documents(
    root: Path,
    schema: dict[str, Any],
) -> tuple[list[dict[str, Any]], list[str]]:
    documents: list[dict[str, Any]] = []
    errors: list[str] = []
    validator = Draft202012Validator(schema)
    for relative in evaluation_paths(root):
        try:
            document = load_json(root / relative)
        except (OSError, json.JSONDecodeError) as error:
            errors.append(f"{relative.as_posix()}: unavailable or invalid: {error}")
            continue
        documents.append(document)
        for error in sorted(
            validator.iter_errors(document),
            key=lambda item: list(item.path),
        ):
            location = ".".join(str(part) for part in error.path) or "<root>"
            errors.append(f"{relative.as_posix()} {location}: {error.message}")
    return documents, errors


def load_eval_set(root: Path = ROOT) -> dict[str, Any]:
    core = load_json(root / EVAL_PATH)
    cases = list(core.get("cases", []))
    coverage_path = root / COVERAGE_EVAL_PATH
    if coverage_path.is_file():
        coverage = load_json(coverage_path)
        cases.extend(coverage.get("cases", []))
    merged = dict(core)
    merged["cases"] = cases
    return merged


def behavior_coverage(
    entries: dict[str, dict[str, Any]],
    cases: list[dict[str, Any]],
) -> dict[str, dict[str, int]]:
    coverage = {
        skill_id: {"primary": 0, "supporting": 0, "forbidden": 0}
        for skill_id in entries
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


def validate_contract(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    try:
        registry = load_json(root / REGISTRY_PATH)
        evals = load_eval_set(root)
        schema = load_json(root / SCHEMA_PATH)
    except (OSError, json.JSONDecodeError) as error:
        return [f"contract file unavailable or invalid: {error}"]

    _, document_errors = validate_eval_documents(root, schema)
    errors.extend(document_errors)

    entries = {
        entry["skill_id"]: entry
        for entry in registry.get("skills", [])
        if entry.get("status") == "ACTIVE"
    }
    case_ids: set[str] = set()
    prompts: set[str] = set()
    case_types: set[str] = set()
    cases = evals.get("cases", [])
    for case in cases:
        case_id = case.get("case_id", "<unknown>")
        prompt = case.get("prompt", "")
        if case_id in case_ids:
            errors.append(f"duplicate case_id: {case_id}")
        case_ids.add(case_id)
        if prompt in prompts:
            errors.append(f"duplicate prompt: {case_id}")
        prompts.add(prompt)
        case_types.add(case.get("case_type", ""))

        mentioned = [skill_id for skill_id in entries if skill_id in prompt]
        if mentioned or re.search(r"\bSkill Mode\b", prompt):
            errors.append(f"{case_id}: prompt leaks routing labels: {mentioned}")

        primary = case.get("expected_primary_skill")
        supporting = case.get("expected_supporting_skills", [])
        forbidden = case.get("forbidden_skills", [])
        selected = [primary, *supporting]
        for skill_id in [*selected, *forbidden]:
            if skill_id not in entries:
                errors.append(f"{case_id}: unknown active Skill {skill_id}")
        if len(selected) != len(set(selected)):
            errors.append(f"{case_id}: primary/supporting Skills must be unique")
        overlap = sorted(set(selected) & set(forbidden))
        if overlap:
            errors.append(f"{case_id}: selected and forbidden Skills overlap: {overlap}")

        combined_bodies = "\n".join(
            (root / entries[skill_id]["path"]).read_text(encoding="utf-8")
            for skill_id in selected
            if skill_id in entries and (root / entries[skill_id]["path"]).is_file()
        )
        for mode in case.get("expected_skill_modes", []):
            if not re.search(
                rf"(?<![A-Za-z0-9-]){re.escape(mode)}(?![A-Za-z0-9-])",
                combined_bodies,
            ):
                errors.append(
                    f"{case_id}: expected Skill mode is not discoverable in selected packages: {mode}"
                )

    required_types = {"positive", "negative", "boundary", "cross-skill"}
    if case_types != required_types:
        errors.append(
            f"case type coverage must equal {sorted(required_types)}; got {sorted(case_types)}"
        )
    if len(case_ids) < 8:
        errors.append("at least eight behavior evaluation cases are required")

    coverage = behavior_coverage(entries, cases)
    for skill_id, counts in sorted(coverage.items()):
        if counts["primary"] == 0:
            errors.append(f"{skill_id}: missing primary behavior coverage")
        if counts["forbidden"] == 0:
            errors.append(f"{skill_id}: missing non-selection behavior coverage")
    return errors


def _result_by_case(results: Any) -> tuple[dict[str, dict[str, Any]], list[str]]:
    indexed: dict[str, dict[str, Any]] = {}
    errors: list[str] = []
    if not isinstance(results, dict):
        return {}, ["result document must be an object"]
    values = results.get("results")
    if not isinstance(values, list):
        return {}, ["results must be a list"]
    for value in values:
        if not isinstance(value, dict) or not isinstance(value.get("case_id"), str):
            errors.append("each result must contain a string case_id")
            continue
        case_id = value["case_id"]
        if case_id in indexed:
            errors.append(f"duplicate result case: {case_id}")
        indexed[case_id] = value
    return indexed, errors


def _string_list(
    value: Any,
    case_id: str,
    field: str,
    errors: list[str],
) -> list[str]:
    if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
        errors.append(f"{case_id}: {field} must contain only strings")
        return []
    return value


def score_results(root: Path, results_path: Path) -> list[str]:
    errors = validate_contract(root)
    if errors:
        return errors
    try:
        evals = load_eval_set(root)
        results = load_json(results_path)
    except (OSError, json.JSONDecodeError) as error:
        return [f"result file unavailable or invalid: {error}"]

    identity_errors = validate_result_identity(root, results)
    if identity_errors:
        return identity_errors

    indexed, result_errors = _result_by_case(results)
    errors.extend(result_errors)
    expected_ids = {case["case_id"] for case in evals["cases"]}
    actual_ids = set(indexed)
    missing = sorted(expected_ids - actual_ids)
    extra = sorted(actual_ids - expected_ids)
    if missing:
        errors.append(f"missing result cases: {missing}")
    if extra:
        errors.append(f"unknown result cases: {extra}")

    for case in evals["cases"]:
        case_id = case["case_id"]
        result = indexed.get(case_id)
        if result is None:
            continue
        if result.get("work_mode") != case["expected_work_mode"]:
            errors.append(f"{case_id}: wrong Work Mode")
        primary = result.get("primary_skill")
        if primary != case["expected_primary_skill"]:
            errors.append(f"{case_id}: wrong primary Skill")
        if not isinstance(primary, str):
            primary = None

        supporting = _string_list(
            result.get("supporting_skills", []),
            case_id,
            "supporting_skills",
            errors,
        )
        if set(supporting) != set(case["expected_supporting_skills"]):
            errors.append(f"{case_id}: supporting Skills differ from the expected set")
        selected = {primary, *supporting}
        forbidden = sorted(selected & set(case["forbidden_skills"]))
        if forbidden:
            errors.append(f"{case_id}: forbidden Skills selected: {forbidden}")

        modes = _string_list(
            result.get("skill_modes", []),
            case_id,
            "skill_modes",
            errors,
        )
        missing_modes = sorted(set(case["expected_skill_modes"]) - set(modes))
        if missing_modes:
            errors.append(f"{case_id}: missing Skill modes: {missing_modes}")

        evidence = _string_list(
            result.get("evidence", []),
            case_id,
            "evidence",
            errors,
        )
        evidence_text = "\n".join(evidence)
        missing_evidence = [
            token
            for token in case["required_evidence"]
            if token.casefold() not in evidence_text.casefold()
        ]
        if missing_evidence:
            errors.append(f"{case_id}: missing required evidence: {missing_evidence}")
        if result.get("user_decision_state") != case["expected_user_decision_state"]:
            errors.append(f"{case_id}: wrong user decision state")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--results", type=Path)
    arguments = parser.parse_args()
    root = arguments.root.resolve()

    contract_errors = validate_contract(root)
    if contract_errors:
        print("CONTRACT_STATUS: FAIL")
        print("MODEL_RUN_STATUS: NOT_RUN")
        for error in contract_errors:
            print(f"- {error}")
        return 1

    registry = load_json(root / REGISTRY_PATH)
    evals = load_eval_set(root)
    entries = {
        entry["skill_id"]: entry
        for entry in registry.get("skills", [])
        if entry.get("status") == "ACTIVE"
    }
    coverage = behavior_coverage(entries, evals.get("cases", []))
    print("CONTRACT_STATUS: PASS")
    print(
        f"ACTIVE_SKILL_COVERAGE: {len(coverage)}/{len(entries)} primary, "
        f"{len(coverage)}/{len(entries)} non-selection"
    )
    if arguments.results is None:
        print("MODEL_RUN_STATUS: NOT_RUN")
        print("Behavior fixtures are valid; no external model result file was scored.")
        return 0

    result_errors = score_results(root, arguments.results.resolve())
    if result_errors:
        print("MODEL_RUN_STATUS: FAIL")
        for error in result_errors:
            print(f"- {error}")
        return 1
    print("MODEL_RUN_STATUS: PASS")
    print("All behavior-evaluation cases matched the expected routing and evidence contract.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
