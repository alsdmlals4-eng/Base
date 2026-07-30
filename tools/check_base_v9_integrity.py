#!/usr/bin/env python3
"""Check Base v9 Registry topology and deterministic generated-artifact freshness."""

from __future__ import annotations

import json
import hashlib
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
V9_GENERATED_OUTPUTS = {
    ".codex-plugin/plugin.json",
    "base.lock.json",
    "skills/BASE_V9_SKILL_SNAPSHOT.json",
    "docs/generated/BASE_ACTIVE_SKILLS.md",
    "docs/operations/BASE_V9_DECISION_REGISTRY.json",
    "docs/operations/GITHUB_OBJECT_LEDGER.json",
    "docs/operations/ADVERSARIAL_REVIEW_MANIFEST.json",
    "docs/operations/SHEET_CONTROL_CONTRACT.json",
}


def frozen_artifact_errors(repository: Path, candidate_lock: dict) -> list[str]:
    """Verify immutable identities for every declared v9.0 evidence-commit blob."""
    errors: list[str] = []
    compatibility = candidate_lock.get("compatibility_base", {})
    evidence_commit = compatibility.get("release_evidence_commit")
    frozen = compatibility.get("frozen_artifacts", [])
    if not isinstance(evidence_commit, str) or not evidence_commit:
        return ["v9.0 frozen artifacts require a release evidence commit"]
    if not isinstance(frozen, list) or not frozen:
        return ["v9.0 frozen artifact declaration is empty"]
    frozen_paths = [entry.get("path") for entry in frozen if isinstance(entry, dict)]
    frozen_set = {path for path in frozen_paths if isinstance(path, str)}
    if len(frozen_paths) != len(frozen) or len(frozen_paths) != len(frozen_set) or frozen_set != V9_GENERATED_OUTPUTS:
        missing = sorted(V9_GENERATED_OUTPUTS - frozen_set)
        extra = sorted(frozen_set - V9_GENERATED_OUTPUTS)
        errors.append(
            "v9.0 frozen artifact declaration must be the complete generated output set"
            f" (missing={missing}, extra={extra}, duplicates={len(frozen_paths) != len(frozen_set)})"
        )
    for entry in frozen:
        if not isinstance(entry, dict):
            errors.append(f"Invalid v9.0 frozen artifact identity: {entry}")
            continue
        value = entry.get("path")
        pinned_oid = entry.get("git_blob_oid")
        pinned_sha256 = entry.get("sha256")
        relative = Path(str(value))
        if relative.is_absolute() or ".." in relative.parts:
            errors.append(f"Unsafe v9.0 frozen artifact path: {value}")
            continue
        historical_oid = subprocess.run(
            ["git", "-C", str(repository), "rev-parse", f"{evidence_commit}:{relative.as_posix()}"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=False,
        )
        historical_blob = subprocess.run(
            ["git", "-C", str(repository), "show", f"{evidence_commit}:{relative.as_posix()}"],
            capture_output=True,
            check=False,
        )
        if historical_oid.returncode or historical_blob.returncode:
            errors.append(f"v9.0 frozen artifact historical blob is unavailable: {value}")
            continue
        actual_oid = historical_oid.stdout.strip()
        if not isinstance(pinned_oid, str) or pinned_oid != actual_oid:
            errors.append(f"v9.0 frozen artifact historical blob ID mismatch: {value}")
        actual_sha256 = hashlib.sha256(historical_blob.stdout).hexdigest()
        if not isinstance(pinned_sha256, str) or pinned_sha256 != actual_sha256:
            errors.append(f"v9.0 frozen artifact historical blob SHA-256 mismatch: {value}")
    return errors


def registry_authority_errors(repository: Path, candidate_lock: dict) -> list[str]:
    """Verify historical v9.0 Registry authority separately from the current v9.1 candidate."""
    errors: list[str] = []
    compatibility = candidate_lock.get("compatibility_base", {})
    historical = compatibility.get("historical_registry")
    current = candidate_lock.get("candidate_registry")
    try:
        base_lock = json.loads((repository / "base.lock.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        return [f"Historical v9.0 base lock cannot be read: {error}"]
    if not isinstance(historical, dict):
        errors.append("Historical v9.0 Registry authority is missing")
    else:
        commit = historical.get("commit")
        path = historical.get("path")
        expected_hash = historical.get("sha256")
        if commit != compatibility.get("release_evidence_commit"):
            errors.append("Historical v9.0 Registry commit must equal the compatibility evidence commit")
        if path != base_lock.get("source_of_truth") or expected_hash != base_lock.get("registry_sha256"):
            errors.append("Historical v9.0 Registry authority does not match frozen base.lock.json")
        if isinstance(commit, str) and isinstance(path, str) and isinstance(expected_hash, str):
            relative = Path(path)
            if relative.is_absolute() or ".." in relative.parts:
                errors.append(f"Unsafe historical v9.0 Registry path: {path}")
            else:
                blob = subprocess.run(
                    ["git", "-C", str(repository), "show", f"{commit}:{relative.as_posix()}"],
                    capture_output=True,
                    check=False,
                )
                if blob.returncode:
                    errors.append("Historical v9.0 Registry Git blob is unavailable")
                elif hashlib.sha256(blob.stdout).hexdigest() != expected_hash:
                    errors.append("Historical v9.0 Registry Git blob hash mismatch")
    if not isinstance(current, dict):
        errors.append("Current v9.1 candidate Registry authority is missing")
    else:
        path = current.get("path")
        expected_hash = current.get("sha256")
        relative = Path(str(path))
        if not isinstance(path, str) or relative.is_absolute() or ".." in relative.parts:
            errors.append(f"Unsafe current v9.1 candidate Registry path: {path}")
        else:
            target = repository / relative
            traversal = repository
            unsafe = False
            for part in relative.parts:
                traversal = traversal / part
                if traversal.is_symlink() or (
                    traversal.exists()
                    and getattr(traversal.stat(follow_symlinks=False), "st_file_attributes", 0) & 0x400
                ):
                    unsafe = True
                    break
            if unsafe:
                errors.append(f"Current v9.1 candidate Registry uses unsafe link traversal: {path}")
            elif not target.is_file():
                errors.append(f"Current v9.1 candidate Registry is missing: {path}")
            elif not isinstance(expected_hash, str) or hashlib.sha256(target.read_bytes()).hexdigest() != expected_hash:
                errors.append("Current v9.1 candidate Registry raw-byte hash mismatch")
    return errors


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
        errors.extend(frozen_artifact_errors(ROOT, candidate_lock))
        errors.extend(registry_authority_errors(ROOT, candidate_lock))
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
