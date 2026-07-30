#!/usr/bin/env python3
"""Check Base v9 Registry topology and deterministic generated-artifact freshness."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "skills/SKILL_REGISTRY.json"
GENERATOR = ROOT / "tools/build_base_v9_artifacts.py"
GENERATED_SUMMARY = ROOT / "docs/generated/BASE_ACTIVE_SKILLS.md"
CANDIDATE_LOCK = ROOT / "base-v9.1.lock.json"
CANDIDATE_LOCK_SCHEMA = ROOT / "schemas/base-v9-1-candidate-lock-v1.schema.json"
ENTRYPOINTS = (
    ROOT / "README.md",
    ROOT / "AGENTS.md",
    ROOT / "START_HERE.md",
    ROOT / "docs/OPERATING_MODEL.md",
    ROOT / "docs/DOCUMENTATION_MAP.md",
)
MARKDOWN_LINK = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
LOCAL_SUFFIXES = {".md", ".json", ".py", ".yml", ".yaml", ".pdf", ".docx", ".png", ".svg"}


def graph_errors(skills: list[dict]) -> list[str]:
    errors: list[str] = []
    active = [skill for skill in skills if skill.get("status") == "ACTIVE"]
    ids = {skill.get("skill_id") for skill in active}
    paths = {skill.get("path") for skill in active}
    discovered = {
        path.relative_to(ROOT).as_posix()
        for path in (ROOT / "skills").glob("*/SKILL.md")
    }
    if discovered != paths:
        missing = sorted(discovered - paths)
        orphaned = sorted(paths - discovered)
        if missing:
            errors.append(f"Skill package orphan(s) not registered: {', '.join(missing)}")
        if orphaned:
            errors.append(f"Registry Skill path(s) absent from package tree: {', '.join(orphaned)}")

    dependencies: dict[str, list[str]] = {}
    for skill in active:
        skill_id = skill.get("skill_id", "")
        declared = skill.get("depends_on", [])
        if not isinstance(declared, list):
            errors.append(f"{skill_id}: depends_on must be a list")
            declared = []
        if len(declared) != len(set(declared)):
            errors.append(f"{skill_id}: duplicate dependency")
        unknown = sorted(set(declared) - ids)
        if unknown:
            errors.append(f"{skill_id}: unknown dependency {', '.join(unknown)}")
        dependencies[skill_id] = [item for item in declared if item in ids]

    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(skill_id: str, trail: list[str]) -> None:
        if skill_id in visiting:
            cycle = trail[trail.index(skill_id):] + [skill_id]
            errors.append(f"Skill dependency cycle: {' -> '.join(cycle)}")
            return
        if skill_id in visited:
            return
        visiting.add(skill_id)
        for dependency in dependencies.get(skill_id, []):
            visit(dependency, trail + [dependency])
        visiting.remove(skill_id)
        visited.add(skill_id)

    for skill_id in sorted(dependencies):
        visit(skill_id, [skill_id])
    return errors


def documentation_link_errors() -> list[str]:
    errors: list[str] = []
    for document in ROOT.rglob("*.md"):
        if any(part in {".git", ".venv", "node_modules"} for part in document.parts):
            continue
        for raw_link in MARKDOWN_LINK.findall(document.read_text(encoding="utf-8", errors="replace")):
            target = raw_link.strip().split("#", 1)[0].split("?", 1)[0]
            if not target or target.startswith(("http://", "https://", "mailto:", "<")):
                continue
            if Path(target).suffix.lower() not in LOCAL_SUFFIXES:
                continue
            if not any(candidate.exists() for candidate in (document.parent / target, ROOT / target)):
                errors.append(f"Broken local documentation link: {document.relative_to(ROOT)} -> {raw_link}")
    return errors


def main() -> int:
    errors: list[str] = []
    try:
        registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        print(f"Base v9 integrity check failed: {error}", file=sys.stderr)
        return 1
    errors.extend(graph_errors(registry.get("skills", [])))
    errors.extend(documentation_link_errors())
    try:
        candidate_lock = json.loads(CANDIDATE_LOCK.read_text(encoding="utf-8"))
        candidate_schema = json.loads(CANDIDATE_LOCK_SCHEMA.read_text(encoding="utf-8"))
        for error in sorted(
            Draft202012Validator(candidate_schema).iter_errors(candidate_lock),
            key=lambda item: list(item.path),
        ):
            location = ".".join(str(part) for part in error.path) or "<root>"
            errors.append(f"Base v9.1 candidate lock {location}: {error.message}")
    except (OSError, json.JSONDecodeError) as error:
        errors.append(f"Base v9.1 candidate lock cannot be validated: {error}")
    if not GENERATED_SUMMARY.is_file():
        errors.append("Generated active-Skill summary is missing")
    for entrypoint in ENTRYPOINTS:
        if not entrypoint.is_file():
            errors.append(f"Missing entrypoint: {entrypoint.relative_to(ROOT)}")
            continue
        text = entrypoint.read_text(encoding="utf-8")
        if "BASE_ACTIVE_SKILLS.md" not in text:
            errors.append(f"Entrypoint does not route to generated active-Skill view: {entrypoint.relative_to(ROOT)}")
    generated = subprocess.run(
        [sys.executable, str(GENERATOR), "--check"],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        capture_output=True,
        check=False,
    )
    if generated.returncode:
        errors.append(generated.stderr.strip() or "Generated artifacts are stale")
    if errors:
        print("Base v9 integrity check failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print("Base v9 integrity check passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
