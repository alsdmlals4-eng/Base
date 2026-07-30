#!/usr/bin/env python3
"""Check Base v9 Registry topology and deterministic generated-artifact freshness."""

from __future__ import annotations

import argparse
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
CANDIDATE_EVIDENCE_PATH = "docs/operations/BASE_V9_1_RELEASE_EVIDENCE.json"
CANDIDATE_EVIDENCE_SCHEMA = ROOT / "schemas/base-v9-1-release-evidence-v1.schema.json"
V93_CANDIDATE_LOCK = ROOT / "base-v9.3.lock.json"
V93_CANDIDATE_LOCK_SCHEMA = ROOT / "schemas/base-v9-3-candidate-lock-v1.schema.json"
V93_EVIDENCE_PATH = "docs/operations/BASE_V9_3_RELEASE_EVIDENCE.json"
V93_EVIDENCE_SCHEMA = ROOT / "schemas/base-v9-3-release-evidence-v1.schema.json"
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


def _resolve_commit(repository: Path, reference: str) -> str | None:
    result = subprocess.run(
        ["git", "-C", str(repository), "rev-parse", "--verify", f"{reference}^{{commit}}"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
    )
    resolved = result.stdout.strip()
    return resolved if not result.returncode and re.fullmatch(r"[0-9a-f]{40}", resolved) else None


def _commit_json(repository: Path, commit: str, relative: str) -> dict | None:
    result = subprocess.run(
        ["git", "-C", str(repository), "show", f"{commit}:{relative}"],
        capture_output=True,
        check=False,
    )
    if result.returncode:
        return None
    try:
        value = json.loads(result.stdout.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return None
    return value if isinstance(value, dict) else None


def resolve_trusted_history_commit(repository: Path, provided: str = "") -> tuple[str | None, list[str]]:
    if provided:
        if not re.fullmatch(r"[0-9a-f]{40}", provided) or _resolve_commit(repository, provided) != provided:
            return None, [f"Trusted history commit is not an exact available commit: {provided}"]
        return provided, []
    reference = "refs/remotes/origin/main"
    resolved = _resolve_commit(repository, reference)
    if resolved is None:
        return None, [f"Trusted history ref cannot be resolved: {reference}"]
    return resolved, []


def release_evidence_errors(
    repository: Path,
    candidate_lock: dict,
    trusted_history_commit: str,
) -> list[str]:
    errors: list[str] = []
    compatibility = candidate_lock.get("compatibility_base", {})
    evidence = compatibility.get("release_evidence_commit")
    release_commit = compatibility.get("release_commit")
    if _resolve_commit(repository, trusted_history_commit) != trusted_history_commit:
        return [f"Trusted history commit is unavailable: {trusted_history_commit}"]
    if not isinstance(evidence, str) or _resolve_commit(repository, evidence) != evidence:
        return [f"v9.0 release evidence commit is unavailable: {evidence}"]
    ancestry = subprocess.run(
        ["git", "-C", str(repository), "merge-base", "--is-ancestor", evidence, trusted_history_commit],
        capture_output=True,
        check=False,
    )
    if ancestry.returncode:
        errors.append("v9.0 release evidence is not an ancestor of trusted history")
    parent = _resolve_commit(repository, f"{evidence}^")
    parent_lock = _commit_json(repository, parent, "base.lock.json") if parent else None
    evidence_lock = _commit_json(repository, evidence, "base.lock.json")
    if parent_lock is None or evidence_lock is None:
        errors.append("v9.0 release transition boundary base.lock.json is unavailable or invalid")
        return errors
    if (
        parent_lock.get("release_state") != "BASE_RELEASE_PENDING_CI"
        or parent_lock.get("final_release_state") != "BASE_RELEASE_PENDING_CI"
    ):
        errors.append("v9.0 release evidence is not the exact pending-to-released transition boundary")
    if (
        evidence_lock.get("release_state") != "BASE_RELEASED"
        or evidence_lock.get("final_release_state") != "BASE_RELEASED"
        or evidence_lock.get("release_line") != "v9.0.0"
        or evidence_lock.get("release_commit") != release_commit
    ):
        errors.append("v9.0 release evidence base.lock.json does not match the released compatibility contract")
    if not isinstance(release_commit, str) or _resolve_commit(repository, release_commit) != release_commit:
        errors.append(f"v9.0 release commit is unavailable: {release_commit}")
    else:
        payload_ancestry = subprocess.run(
            ["git", "-C", str(repository), "merge-base", "--is-ancestor", release_commit, evidence],
            capture_output=True,
            check=False,
        )
        if payload_ancestry.returncode:
            errors.append("v9.0 release commit is not an ancestor of its evidence commit")
    return errors


def candidate_release_evidence_errors(
    repository: Path,
    candidate_lock: dict,
    trusted_history_commit: str,
) -> list[str]:
    """Verify v9.1 pins only against evidence that predates the PR trust boundary."""
    release_commit = candidate_lock.get("candidate_release_commit")
    evidence_commit = candidate_lock.get("candidate_release_evidence_commit")
    if release_commit is None and evidence_commit is None:
        return []
    errors: list[str] = []
    if _resolve_commit(repository, trusted_history_commit) != trusted_history_commit:
        return [f"Trusted history commit is unavailable: {trusted_history_commit}"]
    if not isinstance(release_commit, str) or _resolve_commit(repository, release_commit) != release_commit:
        errors.append(f"v9.1 release payload commit is unavailable: {release_commit}")
    if not isinstance(evidence_commit, str) or _resolve_commit(repository, evidence_commit) != evidence_commit:
        errors.append(f"v9.1 release evidence commit is unavailable: {evidence_commit}")
    if errors:
        return errors

    def is_ancestor(ancestor: str, descendant: str) -> bool:
        return not subprocess.run(
            ["git", "-C", str(repository), "merge-base", "--is-ancestor", ancestor, descendant],
            capture_output=True,
            check=False,
        ).returncode

    if not is_ancestor(release_commit, evidence_commit):
        errors.append("v9.1 release payload is not an ancestor of its evidence commit")
    if not is_ancestor(evidence_commit, trusted_history_commit):
        errors.append("v9.1 release evidence is not an ancestor of trusted history")

    evidence = _commit_json(repository, evidence_commit, CANDIDATE_EVIDENCE_PATH)
    if evidence is None:
        errors.append("v9.1 release evidence record is unavailable or invalid")
        return errors
    try:
        schema = json.loads(CANDIDATE_EVIDENCE_SCHEMA.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        errors.append(f"v9.1 release evidence schema is unavailable: {error}")
        return errors
    for error in sorted(Draft202012Validator(schema).iter_errors(evidence), key=lambda item: list(item.path)):
        location = ".".join(str(part) for part in error.path) or "<root>"
        errors.append(f"v9.1 release evidence record {location}: {error.message}")

    if evidence.get("release_payload_commit") != release_commit:
        errors.append("v9.1 release evidence payload does not match the candidate lock")
    registry = candidate_lock.get("candidate_registry")
    evidence_registry = evidence.get("candidate_registry")
    if not isinstance(registry, dict) or not isinstance(evidence_registry, dict):
        errors.append("v9.1 release evidence Registry authority is missing")
        return errors
    if evidence_registry != registry:
        errors.append("v9.1 release evidence Registry identity does not match the candidate lock")
    path = registry.get("path")
    expected_hash = registry.get("sha256")
    if not isinstance(path, str) or not isinstance(expected_hash, str):
        errors.append("v9.1 candidate Registry path/hash is malformed")
        return errors
    evidence_blob = subprocess.run(
        ["git", "-C", str(repository), "show", f"{evidence_commit}:{path}"],
        capture_output=True,
        check=False,
    )
    if evidence_blob.returncode:
        errors.append("v9.1 release evidence Registry Git blob is unavailable")
    elif hashlib.sha256(evidence_blob.stdout).hexdigest() != expected_hash:
        errors.append("v9.1 release evidence Registry hash does not match the candidate lock")
    parent = _resolve_commit(repository, f"{evidence_commit}^")
    if parent is None:
        errors.append("v9.1 release evidence has no readable parent boundary")
    else:
        parent_blob = subprocess.run(
            ["git", "-C", str(repository), "show", f"{parent}:{path}"],
            capture_output=True,
            check=False,
        )
        if parent_blob.returncode:
            errors.append("v9.1 evidence parent Registry Git blob is unavailable")
        elif not evidence_blob.returncode and parent_blob.stdout != evidence_blob.stdout:
            errors.append("v9.1 release evidence must not change the candidate Registry")
    return errors


def v93_evidence_record_errors(
    repository: Path,
    candidate_lock: dict,
    evidence: dict,
    trusted_history_commit: str,
) -> list[str]:
    """Validate v9.3 evidence against the candidate identity and trusted base history."""
    errors: list[str] = []
    try:
        evidence_schema = json.loads(V93_EVIDENCE_SCHEMA.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        return [f"v9.3 release evidence schema is unavailable: {error}"]
    for error in sorted(Draft202012Validator(evidence_schema).iter_errors(evidence), key=lambda item: list(item.path)):
        location = ".".join(str(part) for part in error.path) or "<root>"
        errors.append(f"v9.3 release evidence record {location}: {error.message}")
    if evidence.get("candidate_issue") != candidate_lock.get("github_issue"):
        errors.append("v9.3 release evidence candidate Issue does not match the candidate lock")
    release_commit = evidence.get("release_payload_commit")
    if not isinstance(release_commit, str) or _resolve_commit(repository, release_commit) != release_commit:
        return errors + [f"v9.3 release evidence payload commit is unavailable: {release_commit}"]
    if _resolve_commit(repository, trusted_history_commit) != trusted_history_commit:
        return errors + [f"Trusted history commit is unavailable: {trusted_history_commit}"]
    payload_ancestry = subprocess.run(
        ["git", "-C", str(repository), "merge-base", "--is-ancestor", release_commit, trusted_history_commit],
        capture_output=True,
        check=False,
    )
    if payload_ancestry.returncode:
        errors.append("v9.3 release evidence payload is not an ancestor of trusted history")
    registry = candidate_lock.get("candidate_registry")
    if evidence.get("candidate_registry") != registry:
        errors.append("v9.3 release evidence Registry identity does not match the candidate lock")
        return errors
    if not isinstance(registry, dict):
        return errors + ["v9.3 candidate Registry authority is missing"]
    registry_path = registry.get("path")
    registry_hash = registry.get("sha256")
    if not isinstance(registry_path, str) or not isinstance(registry_hash, str):
        return errors + ["v9.3 candidate Registry path/hash is malformed"]
    payload_blob = subprocess.run(
        ["git", "-C", str(repository), "show", f"{release_commit}:{registry_path}"],
        capture_output=True,
        check=False,
    )
    if payload_blob.returncode:
        errors.append("v9.3 release evidence payload Registry Git blob is unavailable")
    elif hashlib.sha256(payload_blob.stdout).hexdigest() != registry_hash:
        errors.append("v9.3 release evidence payload Registry hash does not match the candidate lock")
    return errors


def v93_release_lock_errors(repository: Path, candidate_lock: dict, trusted_history_commit: str) -> list[str]:
    """Validate v9.3 candidate and released pins without self-attesting a PR branch."""
    errors: list[str] = []
    try:
        schema = json.loads(V93_CANDIDATE_LOCK_SCHEMA.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        return [f"v9.3 candidate lock schema is unavailable: {error}"]
    for error in sorted(Draft202012Validator(schema).iter_errors(candidate_lock), key=lambda item: list(item.path)):
        location = ".".join(str(part) for part in error.path) or "<root>"
        errors.append(f"v9.3 candidate lock {location}: {error.message}")

    registry = candidate_lock.get("candidate_registry")
    if not isinstance(registry, dict):
        return errors + ["v9.3 candidate Registry authority is missing"]
    registry_path = registry.get("path")
    registry_hash = registry.get("sha256")
    if not isinstance(registry_path, str) or not isinstance(registry_hash, str):
        return errors + ["v9.3 candidate Registry path/hash is malformed"]
    current_registry = repository / registry_path
    if not current_registry.is_file():
        errors.append("v9.3 candidate Registry file is unavailable")
    elif hashlib.sha256(current_registry.read_bytes()).hexdigest() != registry_hash:
        errors.append("v9.3 candidate Registry hash does not match raw file bytes")

    state = candidate_lock.get("release_state")
    release_commit = candidate_lock.get("candidate_release_commit")
    evidence_commit = candidate_lock.get("candidate_release_evidence_commit")
    if state == "RELEASE_CANDIDATE":
        if release_commit is not None or evidence_commit is not None:
            errors.append("v9.3 release candidate must retain null release and evidence pins")
        evidence_path = repository / V93_EVIDENCE_PATH
        if evidence_path.is_file():
            try:
                current_evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError) as error:
                errors.append(f"v9.3 candidate evidence record cannot be read: {error}")
            else:
                errors.extend(
                    v93_evidence_record_errors(repository, candidate_lock, current_evidence, trusted_history_commit)
                )
        return errors
    if state != "BASE_RELEASED":
        return errors + [f"v9.3 release state is unsupported: {state}"]
    if _resolve_commit(repository, trusted_history_commit) != trusted_history_commit:
        return errors + [f"Trusted history commit is unavailable: {trusted_history_commit}"]
    if not isinstance(release_commit, str) or _resolve_commit(repository, release_commit) != release_commit:
        errors.append(f"v9.3 release payload commit is unavailable: {release_commit}")
    if not isinstance(evidence_commit, str) or _resolve_commit(repository, evidence_commit) != evidence_commit:
        errors.append(f"v9.3 release evidence commit is unavailable: {evidence_commit}")
    if errors:
        return errors

    def is_ancestor(ancestor: str, descendant: str) -> bool:
        return not subprocess.run(
            ["git", "-C", str(repository), "merge-base", "--is-ancestor", ancestor, descendant],
            capture_output=True,
            check=False,
        ).returncode

    if not is_ancestor(release_commit, evidence_commit):
        errors.append("v9.3 release payload is not an ancestor of its evidence commit")
    if not is_ancestor(evidence_commit, trusted_history_commit):
        errors.append("v9.3 release evidence is not an ancestor of trusted history")
    evidence = _commit_json(repository, trusted_history_commit, V93_EVIDENCE_PATH)
    if evidence is None:
        return errors + ["v9.3 release evidence is unavailable from trusted history"]
    errors.extend(v93_evidence_record_errors(repository, candidate_lock, evidence, trusted_history_commit))
    if evidence.get("release_payload_commit") != release_commit:
        errors.append("v9.3 release evidence payload does not match the candidate lock")
    if evidence_commit != trusted_history_commit:
        evidence_blob = subprocess.run(
            ["git", "-C", str(repository), "show", f"{evidence_commit}:{registry_path}"],
            capture_output=True,
            check=False,
        )
        if evidence_blob.returncode:
            errors.append("v9.3 release evidence Registry Git blob is unavailable")
        elif hashlib.sha256(evidence_blob.stdout).hexdigest() != registry_hash:
            errors.append("v9.3 release evidence Registry hash does not match the candidate lock")
    return errors


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
    """Verify v9.0 history and the current candidate or released v9.1 Registry."""
    errors: list[str] = []
    compatibility = candidate_lock.get("compatibility_base", {})
    historical = compatibility.get("historical_registry")
    current = candidate_lock.get("candidate_registry")
    evidence_commit = compatibility.get("release_evidence_commit")
    base_lock = _commit_json(repository, evidence_commit, "base.lock.json") if isinstance(evidence_commit, str) else None
    if base_lock is None:
        return ["Historical v9.0 evidence base.lock.json Git blob cannot be read"]
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
            candidate_evidence = candidate_lock.get("candidate_release_evidence_commit")
            if isinstance(candidate_evidence, str):
                target = None
                blob = subprocess.run(
                    ["git", "-C", str(repository), "show", f"{candidate_evidence}:{relative.as_posix()}"],
                    capture_output=True,
                    check=False,
                )
                if blob.returncode:
                    errors.append("Released v9.1 candidate Registry Git blob is unavailable")
                elif not isinstance(expected_hash, str) or hashlib.sha256(blob.stdout).hexdigest() != expected_hash:
                    errors.append("Released v9.1 candidate Registry Git blob hash mismatch")
                return errors
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
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--trusted-history-commit", default="")
    options = parser.parse_args()
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
        trusted_history, trusted_errors = resolve_trusted_history_commit(ROOT, options.trusted_history_commit)
        errors.extend(trusted_errors)
        if trusted_history is not None:
            errors.extend(release_evidence_errors(ROOT, candidate_lock, trusted_history))
            errors.extend(candidate_release_evidence_errors(ROOT, candidate_lock, trusted_history))
        errors.extend(frozen_artifact_errors(ROOT, candidate_lock))
        errors.extend(registry_authority_errors(ROOT, candidate_lock))
    except (OSError, json.JSONDecodeError) as error:
        errors.append(f"Base v9.1 candidate lock cannot be validated: {error}")
    try:
        v93_lock = json.loads(V93_CANDIDATE_LOCK.read_text(encoding="utf-8"))
        trusted_history, trusted_errors = resolve_trusted_history_commit(ROOT, options.trusted_history_commit)
        errors.extend(trusted_errors)
        if trusted_history is not None:
            errors.extend(v93_release_lock_errors(ROOT, v93_lock, trusted_history))
    except (OSError, json.JSONDecodeError) as error:
        errors.append(f"Base v9.3 candidate lock cannot be validated: {error}")
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
