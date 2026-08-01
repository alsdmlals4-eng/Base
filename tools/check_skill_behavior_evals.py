#!/usr/bin/env python3
"""Validate Base Skill behavior fixtures and score externally produced routing results."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = Path("skills/SKILL_REGISTRY.json")
EVAL_PATH = Path("skills/SKILL_BEHAVIOR_EVALS.json")
SCHEMA_PATH = Path("schemas/skill-behavior-eval-v1.schema.json")


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_contract(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    try:
        registry = load_json(root / REGISTRY_PATH)
        evals = load_json(root / EVAL_PATH)
        schema = load_json(root / SCHEMA_PATH)
    except (OSError, json.JSONDecodeError) as error:
        return [f"contract file unavailable or invalid: {error}"]

    for error in sorted(Draft202012Validator(schema).iter_errors(evals), key=lambda item: list(item.path)):
        location = ".".join(str(part) for part in error.path) or "<root>"
        errors.append(f"schema {location}: {error.message}")

    entries = {entry["skill_id"]: entry for entry in registry.get("skills", []) if entry.get("status") == "ACTIVE"}
    case_ids: set[str] = set()
    prompts: set[str] = set()
    case_types: set[str] = set()
    for case in evals.get("cases", []):
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
            if not re.search(rf"(?<![A-Za-z0-9-]){re.escape(mode)}(?![A-Za-z0-9-])", combined_bodies):
                errors.append(f"{case_id}: expected Skill mode is not discoverable in selected packages: {mode}")

    required_types = {"positive", "negative", "boundary", "cross-skill"}
    if case_types != required_types:
        errors.append(f"case type coverage must equal {sorted(required_types)}; got {sorted(case_types)}")
    if len(case_ids) < 8:
        errors.append("at least eight behavior evaluation cases are required")
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


def _string_list(value: Any, case_id: str, field: str, errors: list[str]) -> list[str]:
    if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
        errors.append(f"{case_id}: {field} must contain only strings")
        return []
    return value


def score_results(root: Path, results_path: Path) -> list[str]:
    errors = validate_contract(root)
    if errors:
        return errors
    try:
        evals = load_json(root / EVAL_PATH)
        results = load_json(results_path)
    except (OSError, json.JSONDecodeError) as error:
        return [f"result file unavailable or invalid: {error}"]

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

        supporting = _string_list(result.get("supporting_skills", []), case_id, "supporting_skills", errors)
        if set(supporting) != set(case["expected_supporting_skills"]):
            errors.append(f"{case_id}: supporting Skills differ from the expected set")
        selected = {primary, *supporting}
        forbidden = sorted(selected & set(case["forbidden_skills"]))
        if forbidden:
            errors.append(f"{case_id}: forbidden Skills selected: {forbidden}")

        modes = _string_list(result.get("skill_modes", []), case_id, "skill_modes", errors)
        missing_modes = sorted(set(case["expected_skill_modes"]) - set(modes))
        if missing_modes:
            errors.append(f"{case_id}: missing Skill modes: {missing_modes}")

        evidence = _string_list(result.get("evidence", []), case_id, "evidence", errors)
        evidence_text = "\n".join(evidence)
        missing_evidence = [token for token in case["required_evidence"] if token.casefold() not in evidence_text.casefold()]
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

    print("CONTRACT_STATUS: PASS")
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
