from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "skills/SKILL_REGISTRY.json"
COVERAGE = ROOT / "skills/SKILL_COVERAGE.json"
FRONT_NAME = re.compile(r"^name:\s*['\"]?([^'\"\n]+)", re.MULTILINE)

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

    for responsibility in coverage["responsibilities"]:
        if not responsibility["skills"]:
            errors.append(f"No skill target: {responsibility['id']}")
        for skill_id in responsibility["skills"]:
            if skill_id not in by_id:
                errors.append(f"Coverage target not active: {responsibility['id']} -> {skill_id}")

    for skill_id, item in by_id.items():
        path = ROOT / item["path"]
        if not path.is_file():
            errors.append(f"Missing skill file: {skill_id} -> {item['path']}")
            continue
        text = path.read_text(encoding="utf-8")
        match = FRONT_NAME.search(text)
        if not match or match.group(1).strip() != skill_id:
            errors.append(f"Front matter mismatch: {skill_id}")
        for required in ("##", "Output contract", "Quality gate", "Learning Log"):
            if required not in text:
                errors.append(f"Missing compact contract token {required!r}: {skill_id}")
        if skill_id in COMPACT_TARGETS and len(text.splitlines()) > 150:
            errors.append(f"Compact SKILL.md exceeds 150 lines: {skill_id} ({len(text.splitlines())})")

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
