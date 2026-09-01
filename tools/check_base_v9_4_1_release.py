#!/usr/bin/env python3
"""Fail-closed validation for the Base v9.4.1 compatibility release."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
LOCK_PATH = ROOT / "base-v9.4.1.lock.json"
LOCK_SCHEMA_PATH = ROOT / "schemas/base-v9-4-1-release-lock-v1.schema.json"
EVIDENCE_PATH = ROOT / "docs/operations/BASE_V9_4_1_RELEASE_EVIDENCE.json"
EVIDENCE_SCHEMA_PATH = ROOT / "schemas/base-v9-4-1-release-evidence-v1.schema.json"
PREDECESSOR_LOCK_PATH = ROOT / "base-v9.4.lock.json"
REGISTRY_PATH = ROOT / "skills/SKILL_REGISTRY.json"

EXPECTED_RELEASE_LINE = "v9.4.1"
EXPECTED_RELEASE_ISSUE = 139
EXPECTED_SOURCE_PR = 138
EXPECTED_PAYLOAD = "3f2c4a624d302b704c1b5322eb5c9f34ad55abb9"
EXPECTED_REGISTRY_SHA256 = "693a0dff3f054ecdd653079909e044211473838e73dd9aff07734d1ce5694c59"
EXPECTED_PREDECESSOR_PAYLOAD = "a728712cb776ec98f4875914a580fcf7d0156593"
EXPECTED_PREDECESSOR_EVIDENCE = "ef1fba11167e4da0b298123b0c85ebd268191a42"


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError(f"cannot read JSON {path.relative_to(ROOT)}: {error}") from error
    if not isinstance(value, dict):
        raise ValueError(f"JSON root must be an object: {path.relative_to(ROOT)}")
    return value


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def run_git(*arguments: str) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        ["git", "-C", str(ROOT), *arguments],
        capture_output=True,
        check=False,
    )


def resolve_commit(reference: str) -> str | None:
    result = run_git("rev-parse", "--verify", f"{reference}^{{commit}}")
    if result.returncode:
        return None
    value = result.stdout.decode("utf-8", errors="replace").strip()
    return value if re.fullmatch(r"[0-9a-f]{40}", value) else None


def commit_exists(commit: str) -> bool:
    return run_git("cat-file", "-e", f"{commit}^{{commit}}").returncode == 0


def is_ancestor(ancestor: str, descendant: str) -> bool:
    return run_git("merge-base", "--is-ancestor", ancestor, descendant).returncode == 0


def blob_at(commit: str, path: str) -> bytes | None:
    result = run_git("show", f"{commit}:{path}")
    return result.stdout if result.returncode == 0 else None


def working_tree_path_is_clean(path: Path) -> bool:
    relative_path = path.relative_to(ROOT).as_posix()
    return (
        run_git("diff", "--quiet", "--", relative_path).returncode == 0
        and run_git("diff", "--cached", "--quiet", "--", relative_path).returncode == 0
    )


def schema_errors(document: dict[str, Any], schema: dict[str, Any], label: str) -> list[str]:
    errors = sorted(Draft202012Validator(schema).iter_errors(document), key=lambda item: list(item.path))
    return [
        f"{label} {'.'.join(str(part) for part in error.path) or '<root>'}: {error.message}"
        for error in errors
    ]


def release_errors(trusted_history_reference: str) -> list[str]:
    errors: list[str] = []
    required_files = (
        LOCK_PATH,
        LOCK_SCHEMA_PATH,
        EVIDENCE_PATH,
        EVIDENCE_SCHEMA_PATH,
        PREDECESSOR_LOCK_PATH,
        REGISTRY_PATH,
    )
    missing = [path.relative_to(ROOT).as_posix() for path in required_files if not path.is_file()]
    if missing:
        return [f"missing required release files: {', '.join(missing)}"]

    try:
        lock = load_json(LOCK_PATH)
        lock_schema = load_json(LOCK_SCHEMA_PATH)
        evidence = load_json(EVIDENCE_PATH)
        evidence_schema = load_json(EVIDENCE_SCHEMA_PATH)
        predecessor = load_json(PREDECESSOR_LOCK_PATH)
    except ValueError as error:
        return [str(error)]

    errors.extend(schema_errors(lock, lock_schema, "release lock"))
    errors.extend(schema_errors(evidence, evidence_schema, "release evidence"))
    if errors:
        return errors

    if predecessor.get("release_line") != "v9.4.0":
        errors.append("predecessor release line is not v9.4.0")
    if predecessor.get("candidate_release_commit") != EXPECTED_PREDECESSOR_PAYLOAD:
        errors.append("released v9.4.0 payload identity changed")
    if predecessor.get("candidate_release_evidence_commit") != EXPECTED_PREDECESSOR_EVIDENCE:
        errors.append("released v9.4.0 evidence identity changed")
    predecessor_registry = predecessor.get("candidate_registry", {})
    if predecessor_registry.get("sha256") != EXPECTED_REGISTRY_SHA256:
        errors.append("released v9.4.0 Registry identity changed")

    if lock.get("release_line") != EXPECTED_RELEASE_LINE:
        errors.append("release line must be v9.4.1")
    if lock.get("release_issue") != EXPECTED_RELEASE_ISSUE:
        errors.append("release issue must remain #139")
    if lock.get("source_pr") != EXPECTED_SOURCE_PR:
        errors.append("source PR must remain #138")
    if lock.get("candidate_release_commit") != EXPECTED_PAYLOAD:
        errors.append("v9.4.1 payload commit does not match merged PR #138")

    predecessor_pointer = lock.get("predecessor", {})
    if predecessor_pointer.get("release_commit") != EXPECTED_PREDECESSOR_PAYLOAD:
        errors.append("v9.4.1 predecessor payload does not match released v9.4.0")
    if predecessor_pointer.get("release_evidence_commit") != EXPECTED_PREDECESSOR_EVIDENCE:
        errors.append("v9.4.1 predecessor evidence does not match released v9.4.0")

    registry_lock = lock.get("candidate_registry", {})
    if registry_lock.get("sha256") != EXPECTED_REGISTRY_SHA256:
        errors.append("v9.4.1 Registry SHA-256 must preserve released v9.4.0 bytes")

    if evidence.get("payload_commit") != EXPECTED_PAYLOAD:
        errors.append("release evidence payload does not match the v9.4.1 lock")
    if evidence.get("registry_sha256") != EXPECTED_REGISTRY_SHA256:
        errors.append("release evidence Registry SHA-256 does not match the v9.4.1 lock")
    if evidence.get("release_issue") != EXPECTED_RELEASE_ISSUE or evidence.get("source_pr") != EXPECTED_SOURCE_PR:
        errors.append("release evidence issue/PR identity does not match the lock")

    trusted_history = resolve_commit(trusted_history_reference)
    if trusted_history is None:
        errors.append(f"trusted history reference cannot be resolved: {trusted_history_reference}")
        return errors
    if not commit_exists(EXPECTED_PAYLOAD):
        errors.append(f"v9.4.1 payload commit is unavailable: {EXPECTED_PAYLOAD}")
    elif not is_ancestor(EXPECTED_PAYLOAD, trusted_history):
        errors.append("v9.4.1 payload is not in trusted history")

    registry_blob = blob_at(EXPECTED_PAYLOAD, "skills/SKILL_REGISTRY.json")
    if registry_blob is None:
        errors.append("Registry blob is unavailable at the v9.4.1 payload commit")
    elif sha256_bytes(registry_blob) != EXPECTED_REGISTRY_SHA256:
        errors.append("Registry blob at the v9.4.1 payload commit has the wrong SHA-256")

    for path in lock.get("released_validator_paths", []):
        if blob_at(EXPECTED_PAYLOAD, path) is None:
            errors.append(f"released validator path is unavailable at the payload commit: {path}")

    state = lock.get("release_state")
    evidence_commit = lock.get("candidate_release_evidence_commit")
    if state == "TRUSTED_EVIDENCE_PENDING":
        if evidence_commit is not None:
            errors.append("pending evidence state must keep the evidence pin null")
    elif state == "BASE_RELEASED":
        if not isinstance(evidence_commit, str) or not re.fullmatch(r"[0-9a-f]{40}", evidence_commit):
            errors.append("released state requires a full evidence commit SHA")
        elif not commit_exists(evidence_commit):
            errors.append(f"v9.4.1 evidence commit is unavailable: {evidence_commit}")
        else:
            if not is_ancestor(EXPECTED_PAYLOAD, evidence_commit):
                errors.append("v9.4.1 payload is not an ancestor of the evidence commit")
            if not is_ancestor(evidence_commit, trusted_history):
                errors.append("v9.4.1 evidence commit is not in trusted history")
            evidence_blob = blob_at(evidence_commit, "docs/operations/BASE_V9_4_1_RELEASE_EVIDENCE.json")
            working_tree_evidence = blob_at("HEAD", EVIDENCE_PATH.relative_to(ROOT).as_posix())
            if evidence_blob is None:
                errors.append("trusted evidence JSON is unavailable at the evidence commit")
            elif not working_tree_path_is_clean(EVIDENCE_PATH):
                errors.append("working tree evidence file is dirty")
            elif working_tree_evidence is None:
                errors.append("current commit evidence JSON is unavailable")
            elif evidence_blob != working_tree_evidence:
                errors.append("trusted evidence JSON bytes differ from the pinned evidence commit")
            pinned_registry = blob_at(evidence_commit, "skills/SKILL_REGISTRY.json")
            if pinned_registry is None or sha256_bytes(pinned_registry) != EXPECTED_REGISTRY_SHA256:
                errors.append("Registry blob at the evidence commit does not match the released SHA-256")
    else:
        errors.append(f"unsupported v9.4.1 release state: {state!r}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--trusted-history-commit", default="HEAD")
    arguments = parser.parse_args()
    errors = release_errors(arguments.trusted_history_commit)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("Base v9.4.1 compatibility release check passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
