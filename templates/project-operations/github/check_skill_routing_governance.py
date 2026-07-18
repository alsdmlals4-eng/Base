#!/usr/bin/env python3
"""Validate root design-document location and project skill routing governance.

Usage:
  python tools/check_skill_routing_governance.py \
    --config .github/documentation-governance.json \
    --base "$BASE_SHA" --head "$HEAD_SHA"

The checker uses only the Python standard library. Project-specific paths and
required disciplines belong in the JSON configuration.
"""

from __future__ import annotations

import argparse
import fnmatch
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Iterable


ACTIVE_STATUSES = {"ACTIVE", "SUPPORT"}
INACTIVE_STATUSES = {"HOLD", "BACKUP", "REMOVAL_CANDIDATE", "NOT_INSTALLED"}
ALLOWED_STATUSES = ACTIVE_STATUSES | INACTIVE_STATUSES


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config",
        default=".github/documentation-governance.json",
        help="Path to the JSON configuration.",
    )
    parser.add_argument("--base", default=os.environ.get("BASE_SHA", ""))
    parser.add_argument("--head", default=os.environ.get("HEAD_SHA", "HEAD"))
    return parser.parse_args()


def load_json(path: Path) -> dict:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise SystemExit(f"JSON file not found: {path}")
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON file {path}: {exc}")
    if not isinstance(data, dict):
        raise SystemExit(f"JSON root must be an object: {path}")
    return data


def check_design_root(root: Path, config: dict) -> list[str]:
    errors: list[str] = []
    raw = str(config.get("design_root", "")).strip()
    enforce_top_level = bool(config.get("enforce_top_level_design_root", False))

    if not raw:
        return ["design_root is required"]

    design_root = Path(raw)
    if design_root.is_absolute():
        errors.append(f"design_root must be repository-relative: {raw}")
        return errors

    if enforce_top_level and len(design_root.parts) != 1:
        errors.append(
            f"design_root must be directly under repository root, not nested: {raw}"
        )

    expected = root / design_root
    if not expected.is_dir():
        errors.append(f"Top-level design root missing: {raw}")

    if enforce_top_level:
        target_name = design_root.name
        expected_resolved = expected.resolve()
        for candidate in root.rglob("*"):
            if not candidate.is_dir() or candidate.name != target_name:
                continue
            if ".git" in candidate.parts:
                continue
            if candidate.resolve() == expected_resolved:
                continue
            relative = candidate.relative_to(root)
            errors.append(
                f"Nested duplicate design root is not allowed: {relative}; "
                f"use {design_root} as the active entrypoint"
            )

    return errors


def nonempty_string_list(value: object) -> bool:
    return (
        isinstance(value, list)
        and bool(value)
        and all(isinstance(item, str) and item.strip() for item in value)
    )


def check_skill_registry(root: Path, config: dict) -> tuple[list[str], set[str]]:
    errors: list[str] = []
    registry_name = str(config.get("skill_registry", "")).strip()
    enforce = bool(config.get("enforce_skill_registry", False))

    if not registry_name:
        return (["skill_registry path is required"] if enforce else []), set()

    registry_path = root / registry_name
    if not registry_path.exists():
        return ([f"Skill registry missing: {registry_name}"] if enforce else []), set()

    try:
        registry = load_json(registry_path)
    except SystemExit as exc:
        return [str(exc)], set()

    routing = registry.get("routing_policy", {})
    if not isinstance(routing, dict):
        errors.append(f"{registry_name}: routing_policy must be an object")
        routing = {}

    if routing.get("load_all_skills") is not False:
        errors.append(f"{registry_name}: routing_policy.load_all_skills must be false")
    if routing.get("default_selection") != "none":
        errors.append(f"{registry_name}: routing_policy.default_selection must be 'none'")
    if routing.get("require_trigger_match") is not True:
        errors.append(f"{registry_name}: routing_policy.require_trigger_match must be true")

    skills = registry.get("skills", [])
    if not isinstance(skills, list):
        return errors + [f"{registry_name}: skills must be a list"], set()
    if enforce and not skills:
        errors.append(f"{registry_name}: at least one active project skill is required")

    seen_ids: set[str] = set()
    active_ids: set[str] = set()

    for index, item in enumerate(skills):
        label = f"{registry_name}: skills[{index}]"
        if not isinstance(item, dict):
            errors.append(f"{label} must be an object")
            continue

        skill_id = str(item.get("skill_id", "")).strip()
        if not skill_id:
            errors.append(f"{label}.skill_id is required")
            continue
        if skill_id in seen_ids:
            errors.append(f"Duplicate skill_id: {skill_id}")
        seen_ids.add(skill_id)

        status = str(item.get("status", "")).strip().upper()
        if status not in ALLOWED_STATUSES:
            errors.append(f"{skill_id}: unsupported status: {status}")

        if status not in ACTIVE_STATUSES:
            continue

        active_ids.add(skill_id)
        path_value = str(item.get("path", "")).strip()
        if not path_value:
            errors.append(f"{skill_id}: active skill path is required")
        elif not (root / path_value).is_file():
            errors.append(f"{skill_id}: active skill path missing: {path_value}")

        if item.get("load_by_default") is not False:
            errors.append(f"{skill_id}: load_by_default must be false")

        for field in ("trigger_tags", "use_when", "do_not_use_when", "review_triggers"):
            if not nonempty_string_list(item.get(field)):
                errors.append(f"{skill_id}: {field} must be a non-empty string list")

        learning_log = str(item.get("learning_log", "")).strip()
        if not learning_log:
            errors.append(f"{skill_id}: learning_log is required")
        elif not (root / learning_log).is_file():
            errors.append(f"{skill_id}: learning_log missing: {learning_log}")

        if not str(item.get("last_reviewed_at", "")).strip():
            errors.append(f"{skill_id}: last_reviewed_at is required")
        if not str(item.get("last_reviewed_commit", "")).strip():
            errors.append(f"{skill_id}: last_reviewed_commit is required")
        if not str(item.get("knowledge_state", "")).strip():
            errors.append(f"{skill_id}: knowledge_state is required")

    entrypoints = registry.get("discipline_entrypoints", {})
    if not isinstance(entrypoints, dict):
        errors.append(f"{registry_name}: discipline_entrypoints must be an object")
        entrypoints = {}

    for discipline in config.get("required_skill_disciplines", []):
        ids = entrypoints.get(discipline)
        if not nonempty_string_list(ids):
            errors.append(f"Missing active skill entrypoint for discipline: {discipline}")
            continue
        for skill_id in ids:
            if skill_id not in active_ids:
                errors.append(
                    f"Discipline entrypoint '{discipline}' references inactive or missing skill: "
                    f"{skill_id}"
                )

    return errors, active_ids


def git_changed_files(root: Path, base: str, head: str) -> list[str]:
    if not base or set(base) == {"0"}:
        return []
    result = subprocess.run(
        ["git", "diff", "--name-only", base, head],
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "git diff failed")
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def matches_any(path: str, globs: Iterable[str]) -> bool:
    return any(fnmatch.fnmatch(path, pattern) for pattern in globs)


def check_skill_change_sync(changed: list[str], config: dict) -> list[str]:
    if not changed:
        return []

    skill_globs = config.get("skill_change_globs", ["skills/**/SKILL.md"])
    if not any(matches_any(path, skill_globs) for path in changed):
        return []

    errors: list[str] = []
    registry_name = str(config.get("skill_registry", "")).strip()
    skill_map = str(config.get("skill_map", "")).strip()
    learning_globs = config.get(
        "learning_log_globs",
        ["skills/**/LEARNING_LOG.md", "skills/**/SKILL_LEARNING_LOG.md"],
    )

    if registry_name and registry_name not in changed:
        errors.append(f"Skill contract changed; update registry: {registry_name}")
    if skill_map and skill_map not in changed:
        errors.append(f"Skill contract changed; update skill map: {skill_map}")
    if learning_globs and not any(matches_any(path, learning_globs) for path in changed):
        errors.append(
            "Skill contract changed; update at least one Learning Log matching: "
            + ", ".join(learning_globs)
        )

    return errors


def main() -> int:
    args = parse_args()
    root = Path.cwd()
    config = load_json(root / args.config)

    errors: list[str] = []
    errors += check_design_root(root, config)
    registry_errors, active_ids = check_skill_registry(root, config)
    errors += registry_errors

    try:
        changed = git_changed_files(root, args.base, args.head)
    except RuntimeError as exc:
        errors.append(f"Unable to inspect changed files: {exc}")
        changed = []

    errors += check_skill_change_sync(changed, config)

    if errors:
        print("Skill routing governance failed:\n")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Skill routing governance passed.")
    print(f"Checked {len(active_ids)} active skill(s).")
    if changed:
        print(f"Checked {len(changed)} changed file(s) for skill synchronization.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
