#!/usr/bin/env python3
"""Generate deterministic Base v9 machine-readable derivatives from the Skill Registry."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "skills/SKILL_REGISTRY.json"
FRONT_MATTER = re.compile(r"\A---\n(?P<body>.*?)\n---\n", re.DOTALL)
FIELD = re.compile(r"^(?P<key>[A-Za-z_][A-Za-z0-9_-]*):\s*(?P<value>.+?)\s*$", re.MULTILINE)
REQUIRED_ENTRY_FIELDS = (
    "skill_id",
    "discipline",
    "path",
    "status",
    "trigger_tags",
    "use_when",
    "do_not_use_when",
    "review_triggers",
)
OUTPUTS = {
    "plugin": ROOT / ".codex-plugin/plugin.json",
    "lock": ROOT / "base.lock.json",
    "snapshot": ROOT / "skills/BASE_V9_SKILL_SNAPSHOT.json",
    "summary": ROOT / "docs/generated/BASE_ACTIVE_SKILLS.md",
    "decisions": ROOT / "docs/operations/BASE_V9_DECISION_REGISTRY.json",
    "ledger": ROOT / "docs/operations/GITHUB_OBJECT_LEDGER.json",
    "adversarial": ROOT / "docs/operations/ADVERSARIAL_REVIEW_MANIFEST.json",
    "sheet": ROOT / "docs/operations/SHEET_CONTROL_CONTRACT.json",
}


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def canonical_json(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    match = FRONT_MATTER.search(text)
    if not match:
        return {}
    return {
        field.group("key"): field.group("value").strip().strip("'\"")
        for field in FIELD.finditer(match.group("body"))
    }


def require_nonempty_strings(value: Any, name: str, errors: list[str]) -> list[str]:
    if not isinstance(value, list) or not value or not all(isinstance(item, str) and item.strip() for item in value):
        errors.append(f"{name} must be a non-empty string list")
        return []
    return value


def load_active_skills() -> tuple[dict[str, Any], list[dict[str, Any]]]:
    registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    errors: list[str] = []
    if registry.get("registry_role") != "base-shared-skill-router":
        errors.append("unexpected registry_role")
    if not isinstance(registry.get("skills"), list):
        errors.append("skills must be a list")
    skills: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    seen_paths: set[str] = set()
    responsibility_ids: set[str] = set()
    for entry in registry.get("skills", []):
        if entry.get("status") != "ACTIVE":
            continue
        skill_id = entry.get("skill_id", "")
        for field in REQUIRED_ENTRY_FIELDS:
            if field not in entry:
                errors.append(f"{skill_id or '<unknown>'}: missing Registry field {field}")
        if skill_id in seen_ids:
            errors.append(f"duplicate active skill_id: {skill_id}")
        seen_ids.add(skill_id)
        path_value = entry.get("path", "")
        if path_value in seen_paths:
            errors.append(f"duplicate active skill path: {path_value}")
        seen_paths.add(path_value)
        skill_path = ROOT / path_value
        if not skill_path.is_file():
            errors.append(f"{skill_id}: missing Skill file {path_value}")
            continue
        fields = frontmatter(skill_path)
        if fields.get("name") != skill_id:
            errors.append(f"{skill_id}: frontmatter name mismatch")
        if not fields.get("description"):
            errors.append(f"{skill_id}: frontmatter description is missing")
        trigger_tags = require_nonempty_strings(entry.get("trigger_tags"), f"{skill_id}.trigger_tags", errors)
        use_when = require_nonempty_strings(entry.get("use_when"), f"{skill_id}.use_when", errors)
        do_not_use = require_nonempty_strings(entry.get("do_not_use_when"), f"{skill_id}.do_not_use_when", errors)
        review_triggers = require_nonempty_strings(entry.get("review_triggers"), f"{skill_id}.review_triggers", errors)
        responsibility_id = entry.get("responsibility_id", skill_id)
        if responsibility_id in responsibility_ids:
            errors.append(f"duplicate responsibility boundary: {responsibility_id}")
        responsibility_ids.add(responsibility_id)
        skills.append(
            {
                "skill_id": skill_id,
                "layer": entry.get("layer"),
                "discipline": entry.get("discipline"),
                "path": path_value,
                "frontmatter_description": fields.get("description"),
                "source_sha256": sha256_file(skill_path),
                "contract": {
                    "positive_trigger": "; ".join(trigger_tags),
                    "negative_trigger": "\n".join(do_not_use),
                    "owner": str(entry.get("discipline", "")),
                    "input": "\n".join(use_when),
                    "output": f"{skill_id} execution result with scope, evidence, and unresolved items.",
                    "failure": "\n".join(review_triggers),
                    "verification": "Validate the stated output against the approved contract and relevant evidence.",
                    "next_step": "Route the outcome through the applicable PLAN, BUILD, REVIEW, or handoff stage.",
                },
            }
        )
    if errors:
        raise ValueError("\n".join(errors))
    return registry, skills


def generated_summary(skills: list[dict[str, Any]], registry_hash: str) -> str:
    lines = [
        "# Current Active Base Skills",
        "",
        "> Generated from `skills/SKILL_REGISTRY.json`. Do not edit this derivative.",
        f"> Registry SHA-256: `{registry_hash}`",
        f"> Current active Skill count: `{len(skills)}`",
        "",
        "| Skill ID | Owner | Positive trigger | Negative trigger |",
        "| --- | --- | --- | --- |",
    ]
    for skill in skills:
        contract = skill["contract"]
        positive = contract["positive_trigger"].replace("|", "\\|")
        negative = contract["negative_trigger"].splitlines()[0].replace("|", "\\|")
        lines.append(f"| `{skill['skill_id']}` | {contract['owner']} | {positive} | {negative} |")
    return "\n".join(lines) + "\n"


def build_artifacts() -> dict[Path, bytes]:
    registry, skills = load_active_skills()
    registry_hash = sha256_file(REGISTRY_PATH)
    snapshot = {
        "schema_version": 1,
        "artifact_role": "deterministic-base-skill-snapshot",
        "source_of_truth": "skills/SKILL_REGISTRY.json",
        "registry_sha256": registry_hash,
        "active_skill_count": len(skills),
        "skills": skills,
    }
    snapshot_bytes = canonical_json(snapshot)
    snapshot_hash = sha256_bytes(snapshot_bytes)
    plugin = {
        "name": "base-v9",
        "version": "9.0.0",
        "description": "Base v9 shared game-development operating-system adapter.",
        "author": {"name": "alsdmlals4-eng"},
        "homepage": "https://github.com/alsdmlals4-eng/Base",
        "repository": "https://github.com/alsdmlals4-eng/Base",
        "keywords": ["godot", "game-development", "workflow", "skills"],
        "skills": "./skills/",
        "interface": {
            "displayName": "Base v9",
            "shortDescription": "Shared Godot game-development operating system.",
            "longDescription": "Registry-derived shared Skills, governance, and project adapter contracts for Godot game projects.",
            "developerName": "alsdmlals4-eng",
            "category": "Productivity",
            "capabilities": ["Read", "Write"],
        },
        "base_v9": {
            "source_of_truth": "skills/SKILL_REGISTRY.json",
            "registry_sha256": registry_hash,
            "snapshot": "skills/BASE_V9_SKILL_SNAPSHOT.json",
            "snapshot_sha256": snapshot_hash,
            "active_skill_count": len(skills),
            "project_adapter_contract": "docs/BASE_SHARED_SKILL_ADAPTER_CONTRACT.md",
        },
    }
    lock = {
        "schema_version": 1,
        "artifact_role": "base-release-lock",
        "release_line": "v9.0.0",
        "release_state": "BASE_RELEASE_PENDING_CI",
        "final_release": "v9.0.0",
        "final_release_state": "BASE_RELEASE_PENDING_CI",
        "project_adoption_state": "POST_RELEASE_PROJECT_ADOPTION_WAVE",
        "source_of_truth": "skills/SKILL_REGISTRY.json",
        "registry_sha256": registry_hash,
        "snapshot_sha256": snapshot_hash,
        "active_skill_count": len(skills),
        "generator": "tools/build_base_v9_artifacts.py",
    }
    decisions = {
        "schema_version": 1,
        "artifact_role": "base-v9-decision-registry",
        "decisions": [
            {"id": "BASE-V9-001", "status": "CONFIRMED", "decision": "Active Skill count is Registry-derived and not fixed."},
            {"id": "BASE-V9-002", "status": "CONFIRMED", "decision": "Google Sheets remain USER_FACING_GDD_WORKSPACE for projects; Base is BASE_EXCLUDED."},
            {"id": "BASE-V9-003", "status": "CONFIRMED", "decision": "Project adoption is a post-release wave and must not block the Base v9.0.0 release."},
        ],
    }
    ledger = {
        "schema_version": 1,
        "artifact_role": "github-object-ledger",
        "object_types": ["pr", "issue"],
        "objects": [
            {"type": "pr", "number": 5, "disposition": "REASSESS"},
            {"type": "pr", "number": 18, "disposition": "CONSOLIDATE_REVIEW"},
            {"type": "pr", "number": 28, "disposition": "ADOPT_AS_CONTRACT"},
            {"type": "pr", "number": 29, "disposition": "REASSESS_BOUNDARY"},
            {"type": "pr", "number": 30, "disposition": "ADOPT_AS_GATE"},
            {"type": "issue", "number": 54, "disposition": "IMPLEMENTATION_SOURCE"},
            {"type": "issue", "number": 55, "disposition": "POST_RELEASE_ADOPTION"},
        ],
    }
    adversarial = {
        "schema_version": 1,
        "artifact_role": "adversarial-review-manifest",
        "status": "REVIEWED_WITH_FOLLOWUP",
        "required_gate": "adversarial-gate",
        "scope": "Base v9.0.0 release contract only",
        "report": "docs/operations/BASE_V9_ADVERSARIAL_REVIEW_REPORT.md",
        "attacks": ["authority-drift", "generated-artifact-drift", "orphan-or-cycle", "duplicate-responsibility", "legacy-alias-loss", "release-overclaim"],
        "evidence_required": ["focused-tests", "full-regression", "generator-idempotence", "ci-evidence-or-not-run-status"],
    }
    sheet = {
        "schema_version": 1,
        "artifact_role": "sheet-control-contract",
        "base_sheet_status": "BASE_EXCLUDED",
        "external_sheet_writes_authorized": False,
        "project_sheet_role": "USER_FACING_GDD_WORKSPACE",
        "sheet_only_change_status": "PROPOSED_SHEET_CHANGE",
        "held_projects": [
            {"project": "Ten Paces: Hidden Moves", "status": "HOLD"},
            {"project": "Blacksmith", "status": "HOLD"},
            {"project": "OMENWARD", "status": "HOLD"},
            {"project": "urban-legend", "status": "HOLD"},
            {"project": "GRIMOIRE: 세계를 다시 쓰는 법", "status": "HOLD"},
        ],
        "resume_prerequisites": ["base-v9-final-lock", "repository-audit", "sheet-access", "user-approval", "verification-environment"],
    }
    return {
        OUTPUTS["plugin"]: canonical_json(plugin),
        OUTPUTS["lock"]: canonical_json(lock),
        OUTPUTS["snapshot"]: snapshot_bytes,
        OUTPUTS["summary"]: generated_summary(skills, registry_hash).encode("utf-8"),
        OUTPUTS["decisions"]: canonical_json(decisions),
        OUTPUTS["ledger"]: canonical_json(ledger),
        OUTPUTS["adversarial"]: canonical_json(adversarial),
        OUTPUTS["sheet"]: canonical_json(sheet),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true", help="write deterministic generated artifacts")
    mode.add_argument("--check", action="store_true", help="fail if generated artifacts differ")
    return parser.parse_args()


def main() -> int:
    options = parse_args()
    try:
        artifacts = build_artifacts()
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"Base v9 generation failed: {error}", file=sys.stderr)
        return 1
    mismatches = [path for path, content in artifacts.items() if not path.is_file() or path.read_bytes() != content]
    if options.check:
        if mismatches:
            print("Base v9 generated artifacts are stale:", file=sys.stderr)
            for path in mismatches:
                print(f"- {path.relative_to(ROOT).as_posix()}", file=sys.stderr)
            return 1
        print("Base v9 generated artifacts are current")
        return 0
    for path in mismatches:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(artifacts[path])
    print(f"Base v9 generated artifacts written: {len(mismatches)} changed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
