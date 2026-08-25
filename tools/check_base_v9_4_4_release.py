#!/usr/bin/env python3
"""Fail-closed validation for the Base v9.4.4 compatibility release."""

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
LOCK_PATH = ROOT / "base-v9.4.4.lock.json"
LOCK_SCHEMA_PATH = ROOT / "schemas/base-v9-4-4-release-lock-v1.schema.json"
EVIDENCE_PATH = ROOT / "docs/operations/BASE_V9_4_4_RELEASE_EVIDENCE.json"
EVIDENCE_SCHEMA_PATH = ROOT / "schemas/base-v9-4-4-release-evidence-v1.schema.json"
PREDECESSOR_LOCK_PATH = ROOT / "base-v9.4.3.lock.json"

EXPECTED_PAYLOAD = "210ec78292fa12ed7563ba743b322dd36103ae4a"
EXPECTED_SOURCE_HEAD = "e9a081b0aa9d046bfdec819ef2b88b7d1f115ec8"
EXPECTED_PREDECESSOR_PAYLOAD = "7dd1a4f80388bc5faca767ff74a3eb32dc9d0ac8"
EXPECTED_PREDECESSOR_EVIDENCE = "da33a350d61b8adc52df97fccc7001708a933370"
EXPECTED_PREDECESSOR_REGISTRY = "693a0dff3f054ecdd653079909e044211473838e73dd9aff07734d1ce5694c59"
EXPECTED_RELEASED_PATHS = {
    "AGENTS.md",
    "START_HERE.md",
    "skills/managing-project-intake-and-work-contract/SKILL.md",
    "docs/knowledge/game-development/reuse/adoption/PROJECT_WORK_REUSE_HANDOFF.json",
    "tests/test_reuse_first_preflight_enforcement.py",
    "tests/test_reference_freshness.py",
}


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"JSON root must be an object: {path.relative_to(ROOT)}")
    return value


def sha256(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def git(*args: str) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(["git", "-C", str(ROOT), *args], capture_output=True, check=False)


def resolve_commit(ref: str) -> str | None:
    result = git("rev-parse", "--verify", f"{ref}^{{commit}}")
    value = result.stdout.decode(errors="replace").strip()
    return value if result.returncode == 0 and re.fullmatch(r"[0-9a-f]{40}", value) else None


def exists(commit: str) -> bool:
    return git("cat-file", "-e", f"{commit}^{{commit}}").returncode == 0


def ancestor(old: str, new: str) -> bool:
    return git("merge-base", "--is-ancestor", old, new).returncode == 0


def blob(commit: str, path: str) -> bytes | None:
    result = git("show", f"{commit}:{path}")
    return result.stdout if result.returncode == 0 else None


def schema_errors(document: dict[str, Any], schema: dict[str, Any], label: str) -> list[str]:
    return [
        f"{label} {'.'.join(str(part) for part in error.path) or '<root>'}: {error.message}"
        for error in sorted(Draft202012Validator(schema).iter_errors(document), key=lambda item: list(item.path))
    ]


def release_errors(trusted_ref: str) -> list[str]:
    errors: list[str] = []
    required = (
        LOCK_PATH,
        LOCK_SCHEMA_PATH,
        EVIDENCE_PATH,
        EVIDENCE_SCHEMA_PATH,
        PREDECESSOR_LOCK_PATH,
    )
    missing = [path.relative_to(ROOT).as_posix() for path in required if not path.is_file()]
    if missing:
        return [f"missing required release files: {', '.join(missing)}"]

    try:
        lock = load_json(LOCK_PATH)
        evidence = load_json(EVIDENCE_PATH)
        predecessor = load_json(PREDECESSOR_LOCK_PATH)
        errors.extend(schema_errors(lock, load_json(LOCK_SCHEMA_PATH), "release lock"))
        errors.extend(schema_errors(evidence, load_json(EVIDENCE_SCHEMA_PATH), "release evidence"))
    except (OSError, json.JSONDecodeError, ValueError) as error:
        return [str(error)]
    if errors:
        return errors

    if predecessor.get("release_line") != "v9.4.3" or predecessor.get("release_state") != "BASE_RELEASED":
        errors.append("predecessor release is not released v9.4.3")
    if predecessor.get("candidate_release_commit") != EXPECTED_PREDECESSOR_PAYLOAD:
        errors.append("released v9.4.3 payload identity changed")
    if predecessor.get("candidate_release_evidence_commit") != EXPECTED_PREDECESSOR_EVIDENCE:
        errors.append("released v9.4.3 evidence identity changed")
    if predecessor.get("candidate_registry", {}).get("sha256") != EXPECTED_PREDECESSOR_REGISTRY:
        errors.append("released v9.4.3 Registry identity changed")

    if lock.get("release_line") != "v9.4.4" or lock.get("release_issue") != 670 or lock.get("source_pr") != 669:
        errors.append("v9.4.4 issue/source identity is invalid")
    if lock.get("candidate_release_commit") != EXPECTED_PAYLOAD:
        errors.append("v9.4.4 payload commit does not match merged PR #669")
    pointer = lock.get("predecessor", {})
    if pointer.get("release_commit") != EXPECTED_PREDECESSOR_PAYLOAD or pointer.get("release_evidence_commit") != EXPECTED_PREDECESSOR_EVIDENCE:
        errors.append("v9.4.4 predecessor pointer does not match released v9.4.3")
    if set(lock.get("released_validator_paths", [])) != EXPECTED_RELEASED_PATHS:
        errors.append("v9.4.4 released validator path set is incomplete or changed")

    registry_sha = lock.get("candidate_registry", {}).get("sha256")
    if evidence.get("payload_commit") != EXPECTED_PAYLOAD or evidence.get("registry_sha256") != registry_sha:
        errors.append("release evidence identity does not match the lock")
    if evidence.get("verification", {}).get("source_exact_head") != EXPECTED_SOURCE_HEAD:
        errors.append("release evidence does not bind the reviewed source exact HEAD")

    trusted = resolve_commit(trusted_ref)
    if trusted is None:
        errors.append(f"trusted history reference cannot be resolved: {trusted_ref}")
        return errors
    if not exists(EXPECTED_PAYLOAD) or not ancestor(EXPECTED_PAYLOAD, trusted):
        errors.append("v9.4.4 payload is unavailable or outside trusted history")

    registry_at_payload = blob(EXPECTED_PAYLOAD, "skills/SKILL_REGISTRY.json")
    if registry_at_payload is None:
        errors.append("Registry blob is unavailable at the v9.4.4 payload")
    else:
        actual_registry_sha = sha256(registry_at_payload)
        if registry_sha != actual_registry_sha:
            errors.append(
                "Registry SHA-256 does not match the v9.4.4 payload: "
                f"lock={registry_sha!r}, actual={actual_registry_sha!r}"
            )

    for path in lock.get("released_validator_paths", []):
        if blob(EXPECTED_PAYLOAD, path) is None:
            errors.append(f"released path is unavailable at the payload commit: {path}")

    state = lock.get("release_state")
    evidence_commit = lock.get("candidate_release_evidence_commit")
    if state == "TRUSTED_EVIDENCE_PENDING":
        if evidence_commit is not None:
            errors.append("pending evidence state must keep the evidence pin null")
    elif state == "BASE_RELEASED":
        if not isinstance(evidence_commit, str) or not re.fullmatch(r"[0-9a-f]{40}", evidence_commit):
            errors.append("released state requires a full evidence commit SHA")
        elif not exists(evidence_commit):
            errors.append("v9.4.4 evidence commit is unavailable")
        else:
            if not ancestor(EXPECTED_PAYLOAD, evidence_commit) or not ancestor(evidence_commit, trusted):
                errors.append("v9.4.4 payload/evidence trusted-history ancestry is invalid")
            evidence_blob = blob(evidence_commit, "docs/operations/BASE_V9_4_4_RELEASE_EVIDENCE.json")
            if evidence_blob != EVIDENCE_PATH.read_bytes():
                errors.append("trusted evidence JSON differs from the pinned evidence commit")
            pinned_registry = blob(evidence_commit, "skills/SKILL_REGISTRY.json")
            if pinned_registry is None or sha256(pinned_registry) != registry_sha:
                errors.append("Registry blob at the evidence commit has the wrong SHA-256")
    else:
        errors.append(f"unsupported v9.4.4 release state: {state!r}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--trusted-history-commit", default="HEAD")
    args = parser.parse_args()
    errors = release_errors(args.trusted_history_commit)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("Base v9.4.4 compatibility release check passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
