#!/usr/bin/env python3
"""Validate root design documents, skill routing, and human skill-map publications.

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
import hashlib
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


def file_digest(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


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


def check_skill_registry(root: Path, config: dict) -> tuple[list[str], set[str], dict]:
    errors: list[str] = []
    registry_name = str(config.get("skill_registry", "")).strip()
    enforce = bool(config.get("enforce_skill_registry", False))

    if not registry_name:
        return ((["skill_registry path is required"] if enforce else []), set(), {})

    registry_path = root / registry_name
    if not registry_path.exists():
        return (([f"Skill registry missing: {registry_name}"] if enforce else []), set(), {})

    try:
        registry = load_json(registry_path)
    except SystemExit as exc:
        return [str(exc)], set(), {}

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

    human = registry.get("human_presentation", {})
    if bool(config.get("enforce_skill_map_publication", False)):
        if not isinstance(human, dict):
            errors.append(f"{registry_name}: human_presentation must be an object")
            human = {}
        expected_human = {
            "primary_reading_format": "PROJECT_SKILL_MAP.pdf",
            "editable_derivative": "PROJECT_SKILL_MAP.docx",
            "diagram_directory": "PROJECT_SKILL_MAP.assets",
            "publication_manifest": "SKILL_MAP_PUBLICATION_MANIFEST.json",
            "source_of_truth": "SKILL_REGISTRY.json",
            "markdown_skill_map_allowed": False,
        }
        for field, expected in expected_human.items():
            if human.get(field) != expected:
                errors.append(
                    f"{registry_name}: human_presentation.{field} must be {expected!r}"
                )

    skills = registry.get("skills", [])
    if not isinstance(skills, list):
        return errors + [f"{registry_name}: skills must be a list"], set(), registry
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

    return errors, active_ids, registry


def check_file_header(path: Path, expected: bytes) -> bool:
    try:
        return path.read_bytes()[: len(expected)] == expected
    except OSError:
        return False


def resolve_manifest_path(manifest_path: Path, value: str) -> Path:
    candidate = Path(value)
    if candidate.is_absolute():
        return candidate
    return manifest_path.parent / candidate


def check_skill_map_publication(root: Path, config: dict, registry: dict) -> list[str]:
    errors: list[str] = []
    enforce = bool(config.get("enforce_skill_map_publication", False))
    manifest_name = str(config.get("skill_map_publication_manifest", "")).strip()
    forbidden_md = str(config.get("forbidden_markdown_skill_map", "")).strip()

    if forbidden_md and (root / forbidden_md).exists():
        errors.append(
            f"Markdown project skill map is forbidden: {forbidden_md}; "
            "edit SKILL_REGISTRY.json and regenerate DOCX/PDF"
        )

    if not manifest_name:
        return errors + (["skill_map_publication_manifest is required"] if enforce else [])

    manifest_path = root / manifest_name
    if not manifest_path.exists():
        return errors + ([f"Skill-map publication manifest missing: {manifest_name}"] if enforce else [])

    try:
        manifest = load_json(manifest_path)
    except SystemExit as exc:
        return errors + [str(exc)]

    registry_name = str(config.get("skill_registry", "")).strip()
    registry_path = root / registry_name
    if not registry_path.exists():
        return errors

    expected_registry_hash = file_digest(registry_path)
    if str(manifest.get("source_sha256", "")).lower() != expected_registry_hash:
        errors.append(
            f"{manifest_name}: registry input changed; expected source_sha256 "
            f"{expected_registry_hash}"
        )

    if manifest.get("role") != "human-readable-derivative":
        errors.append(f"{manifest_name}: role must be human-readable-derivative")
    if manifest.get("status") != "CURRENT":
        errors.append(f"{manifest_name}: status must be CURRENT")
    if manifest.get("automated_render_review") != "PASSED":
        errors.append(f"{manifest_name}: automated_render_review must be PASSED")
    if bool(config.get("require_human_skill_map_visual_review", False)) and manifest.get(
        "human_visual_review"
    ) != "PASSED":
        errors.append(f"{manifest_name}: human_visual_review must be PASSED")

    output_specs = [
        ("output_docx", "output_docx_sha256", b"PK", "DOCX"),
        ("output_pdf", "output_pdf_sha256", b"%PDF-", "PDF"),
    ]
    for path_field, digest_field, header, label in output_specs:
        relative = str(manifest.get(path_field, "")).strip()
        if not relative:
            errors.append(f"{manifest_name}: {path_field} is required")
            continue
        path = resolve_manifest_path(manifest_path, relative)
        if not path.is_file():
            errors.append(f"{manifest_name}: {label} missing: {relative}")
            continue
        if not check_file_header(path, header):
            errors.append(f"{manifest_name}: invalid {label} header: {relative}")
        expected = str(manifest.get(digest_field, "")).lower()
        actual = file_digest(path)
        if expected != actual:
            errors.append(f"{manifest_name}: {label} hash mismatch: {relative}")

    diagrams = manifest.get("diagram_paths", [])
    hashes = manifest.get("diagram_sha256", {})
    if not isinstance(diagrams, list) or not diagrams:
        errors.append(f"{manifest_name}: diagram_paths must contain at least one image")
        diagrams = []
    if not isinstance(hashes, dict):
        errors.append(f"{manifest_name}: diagram_sha256 must be an object")
        hashes = {}
    for relative_value in diagrams:
        relative = str(relative_value)
        path = resolve_manifest_path(manifest_path, relative)
        if not path.is_file():
            errors.append(f"{manifest_name}: diagram missing: {relative}")
            continue
        if path.suffix.lower() not in {".png", ".jpg", ".jpeg", ".webp"}:
            errors.append(f"{manifest_name}: unsupported diagram format: {relative}")
        expected = str(hashes.get(relative, "")).lower()
        if expected != file_digest(path):
            errors.append(f"{manifest_name}: diagram hash mismatch: {relative}")

    human = registry.get("human_presentation", {}) if isinstance(registry, dict) else {}
    if isinstance(human, dict):
        expected_names = {
            str(human.get("primary_reading_format", "")),
            str(human.get("editable_derivative", "")),
            str(human.get("publication_manifest", "")),
        }
        actual_names = {
            str(manifest.get("output_pdf", "")),
            str(manifest.get("output_docx", "")),
            manifest_path.name,
        }
        if expected_names != actual_names:
            errors.append(
                f"{manifest_name}: Registry human_presentation paths do not match publication outputs"
            )

    return errors


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
    generator_globs = config.get("skill_map_generator_globs", [])
    registry_name = str(config.get("skill_registry", "")).strip()
    skill_changed = any(matches_any(path, skill_globs) for path in changed)
    source_changed = skill_changed or registry_name in changed or any(
        matches_any(path, generator_globs) for path in changed
    )
    if not source_changed:
        return []

    errors: list[str] = []
    sync_paths = [str(path) for path in config.get("skill_map_sync_paths", [])]
    for path in sync_paths:
        if path not in changed:
            errors.append(f"Skill-map source changed; regenerate and update: {path}")

    if skill_changed:
        if registry_name and registry_name not in changed:
            errors.append(f"Skill contract changed; update registry: {registry_name}")
        learning_globs = config.get(
            "learning_log_globs",
            ["skills/**/LEARNING_LOG.md", "skills/**/SKILL_LEARNING_LOG.md"],
        )
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
    registry_errors, active_ids, registry = check_skill_registry(root, config)
    errors += registry_errors
    errors += check_skill_map_publication(root, config, registry)

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
