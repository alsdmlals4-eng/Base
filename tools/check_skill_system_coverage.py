from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "skills/SKILL_REGISTRY.json"
COVERAGE = ROOT / "skills/SKILL_COVERAGE.json"
FRONT_NAME = re.compile(r"^name:\s*['\"]?([^'\"\n]+)", re.MULTILINE)
ALLOWED_COVERAGE_STATUSES = {"COVERED", "COVERED_EXISTING"}

COMPACT_TARGETS = {
    "identifying-project-core",
    "establishing-project-core",
    "running-adversarial-review-and-refinement",
    "evolving-project-discipline-skills",
    "analyzing-and-refining-game-concepts",
    "refactoring-with-contract-preservation",
    "simplifying-skill-bodies",
    "pruning-stale-and-nonfunctional-material",
    "synchronizing-local-and-github-state",
    "maintaining-long-running-task-continuity",
    "governing-game-user-research-coverage",
    "creating-user-learning-notes",
    "building-project-visual-dashboards",
    "diagnosing-game-engine-runtime-failures",
}


def validate() -> list[str]:
    errors: list[str] = []
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    coverage = json.loads(COVERAGE.read_text(encoding="utf-8"))
    by_id = {item["skill_id"]: item for item in registry["skills"]}

    responsibility_ids: set[str] = set()
    for responsibility in coverage["responsibilities"]:
        responsibility_id = responsibility["id"]
        if responsibility_id in responsibility_ids:
            errors.append(f"Duplicate responsibility id: {responsibility_id}")
        responsibility_ids.add(responsibility_id)

        if responsibility.get("status") not in ALLOWED_COVERAGE_STATUSES:
            errors.append(
                f"Invalid coverage status: {responsibility_id} -> {responsibility.get('status')}"
            )
        targets = responsibility.get("skills", [])
        if not targets:
            errors.append(f"No skill target: {responsibility_id}")
        if len(targets) != len(set(targets)):
            errors.append(f"Duplicate skill target: {responsibility_id}")
        for skill_id in targets:
            entry = by_id.get(skill_id)
            if entry is None:
                errors.append(f"Coverage target not registered: {responsibility_id} -> {skill_id}")
            elif entry["status"] != "ACTIVE":
                errors.append(f"Coverage target not active: {responsibility_id} -> {skill_id}")

    for skill_id in sorted(COMPACT_TARGETS):
        if skill_id not in by_id:
            errors.append(f"Compact target not registered: {skill_id}")

    for skill_id, item in by_id.items():
        path = ROOT / item["path"]
        if not path.is_file():
            errors.append(f"Missing skill file: {skill_id} -> {item['path']}")
            continue
        text = path.read_text(encoding="utf-8")
        match = FRONT_NAME.search(text)
        if not match or match.group(1).strip() != skill_id:
            errors.append(f"Front matter mismatch: {skill_id}")
        if skill_id in COMPACT_TARGETS:
            for required in ("##", "Output contract", "Quality gate", "Learning Log"):
                if required not in text:
                    errors.append(f"Missing compact contract token {required!r}: {skill_id}")
            if len(text.splitlines()) > 150:
                errors.append(
                    f"Compact SKILL.md exceeds 150 lines: {skill_id} ({len(text.splitlines())})"
                )

    for obsolete in (
        ROOT / "tools/apply_skill_system_expansion.py",
        ROOT / ".github/workflows/agent-expand-and-optimize-skill-system.yml",
    ):
        if obsolete.exists():
            errors.append(f"Temporary expansion artifact remains: {obsolete.relative_to(ROOT)}")

    return errors


def main() -> int:
    errors = validate()
    if errors:
        print("Skill system coverage check failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Skill system coverage check passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
