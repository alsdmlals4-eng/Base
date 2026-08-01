#!/usr/bin/env python3
"""Patch Base integrity validation for the compatible v9.4 Registry authority."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "tools/check_base_v9_integrity.py"


def replace_once(text: str, old: str, new: str, label: str) -> str:
    if new in text:
        return text
    if old not in text:
        raise RuntimeError(f"Cannot locate integrity patch target: {label}")
    return text.replace(old, new, 1)


def main() -> int:
    text = TARGET.read_text(encoding="utf-8")

    text = replace_once(
        text,
        'V93_EVIDENCE_SCHEMA = ROOT / "schemas/base-v9-3-release-evidence-v1.schema.json"\n',
        'V93_EVIDENCE_SCHEMA = ROOT / "schemas/base-v9-3-release-evidence-v1.schema.json"\n'
        'V94_CANDIDATE_LOCK = ROOT / "base-v9.4.lock.json"\n'
        'V94_CANDIDATE_LOCK_SCHEMA = ROOT / "schemas/base-v9-4-candidate-lock-v1.schema.json"\n',
        "v9.4 constants",
    )

    old_head_check = '''    candidate_blob = subprocess.run(
        ["git", "-C", str(repository), "show", f"HEAD:{registry_path}"],
        capture_output=True,
        check=False,
    )
    if candidate_blob.returncode:
        errors.append("v9.3 candidate Registry Git blob is unavailable")
    elif hashlib.sha256(candidate_blob.stdout).hexdigest() != registry_hash:
        errors.append("v9.3 candidate Registry hash does not match Git raw bytes")

    state = candidate_lock.get("release_state")
    release_commit = candidate_lock.get("candidate_release_commit")
    evidence_commit = candidate_lock.get("candidate_release_evidence_commit")
    if state == "RELEASE_CANDIDATE":
'''
    new_head_check = '''    state = candidate_lock.get("release_state")
    release_commit = candidate_lock.get("candidate_release_commit")
    evidence_commit = candidate_lock.get("candidate_release_evidence_commit")
    if state == "RELEASE_CANDIDATE":
        candidate_blob = subprocess.run(
            ["git", "-C", str(repository), "show", f"HEAD:{registry_path}"],
            capture_output=True,
            check=False,
        )
        if candidate_blob.returncode:
            errors.append("v9.3 candidate Registry Git blob is unavailable")
        elif hashlib.sha256(candidate_blob.stdout).hexdigest() != registry_hash:
            errors.append("v9.3 candidate Registry hash does not match Git raw bytes")
'''
    text = replace_once(text, old_head_check, new_head_check, "released v9.3 HEAD authority")

    marker = "\ndef frozen_artifact_errors(repository: Path, candidate_lock: dict) -> list[str]:\n"
    function = '''
def v94_release_lock_errors(repository: Path, candidate_lock: dict, trusted_history_commit: str) -> list[str]:
    """Validate v9.4 as the current Registry authority without rewriting v9.3 history."""
    errors: list[str] = []
    try:
        schema = json.loads(V94_CANDIDATE_LOCK_SCHEMA.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        return [f"v9.4 candidate lock schema is unavailable: {error}"]
    for error in sorted(Draft202012Validator(schema).iter_errors(candidate_lock), key=lambda item: list(item.path)):
        location = ".".join(str(part) for part in error.path) or "<root>"
        errors.append(f"v9.4 candidate lock {location}: {error.message}")

    registry = candidate_lock.get("candidate_registry")
    if not isinstance(registry, dict):
        return errors + ["v9.4 candidate Registry authority is missing"]
    registry_path = registry.get("path")
    registry_hash = registry.get("sha256")
    if not isinstance(registry_path, str) or not isinstance(registry_hash, str):
        return errors + ["v9.4 candidate Registry path/hash is malformed"]

    state = candidate_lock.get("release_state")
    release_commit = candidate_lock.get("candidate_release_commit")
    evidence_commit = candidate_lock.get("candidate_release_evidence_commit")
    if state == "RELEASE_CANDIDATE":
        if release_commit is not None or evidence_commit is not None:
            errors.append("v9.4 release candidate must retain null release and evidence pins")
        blob = subprocess.run(
            ["git", "-C", str(repository), "show", f"HEAD:{registry_path}"],
            capture_output=True,
            check=False,
        )
        if blob.returncode:
            errors.append("v9.4 candidate Registry Git blob is unavailable")
        elif hashlib.sha256(blob.stdout).hexdigest() != registry_hash:
            errors.append("v9.4 candidate Registry hash does not match Git raw bytes")
        return errors

    if state != "BASE_RELEASED":
        return errors + [f"v9.4 release state is unsupported: {state}"]
    if _resolve_commit(repository, trusted_history_commit) != trusted_history_commit:
        return errors + [f"Trusted history commit is unavailable: {trusted_history_commit}"]
    if not isinstance(release_commit, str) or _resolve_commit(repository, release_commit) != release_commit:
        errors.append(f"v9.4 release payload commit is unavailable: {release_commit}")
    if not isinstance(evidence_commit, str) or _resolve_commit(repository, evidence_commit) != evidence_commit:
        errors.append(f"v9.4 release evidence commit is unavailable: {evidence_commit}")
    if errors:
        return errors
    for ancestor, descendant, message in (
        (release_commit, evidence_commit, "v9.4 release payload is not an ancestor of its evidence commit"),
        (evidence_commit, trusted_history_commit, "v9.4 release evidence is not an ancestor of trusted history"),
    ):
        result = subprocess.run(
            ["git", "-C", str(repository), "merge-base", "--is-ancestor", ancestor, descendant],
            capture_output=True,
            check=False,
        )
        if result.returncode:
            errors.append(message)
    payload_blob = subprocess.run(
        ["git", "-C", str(repository), "show", f"{release_commit}:{registry_path}"],
        capture_output=True,
        check=False,
    )
    if payload_blob.returncode:
        errors.append("v9.4 release payload Registry Git blob is unavailable")
    elif hashlib.sha256(payload_blob.stdout).hexdigest() != registry_hash:
        errors.append("v9.4 release payload Registry hash does not match the lock")
    return errors

'''
    if "def v94_release_lock_errors" not in text:
        if marker not in text:
            raise RuntimeError("Cannot locate v9.4 function insertion point")
        text = text.replace(marker, "\n" + function + marker.lstrip("\n"), 1)

    old_main = '''    try:
        v93_lock = json.loads(V93_CANDIDATE_LOCK.read_text(encoding="utf-8"))
        trusted_history, trusted_errors = resolve_trusted_history_commit(ROOT, options.trusted_history_commit)
        errors.extend(trusted_errors)
        if trusted_history is not None:
            errors.extend(v93_release_lock_errors(ROOT, v93_lock, trusted_history))
    except (OSError, json.JSONDecodeError) as error:
        errors.append(f"Base v9.3 candidate lock cannot be validated: {error}")
'''
    new_main = old_main + '''    if V94_CANDIDATE_LOCK.is_file():
        try:
            v94_lock = json.loads(V94_CANDIDATE_LOCK.read_text(encoding="utf-8"))
            trusted_history, trusted_errors = resolve_trusted_history_commit(ROOT, options.trusted_history_commit)
            errors.extend(trusted_errors)
            if trusted_history is not None:
                errors.extend(v94_release_lock_errors(ROOT, v94_lock, trusted_history))
        except (OSError, json.JSONDecodeError) as error:
            errors.append(f"Base v9.4 candidate lock cannot be validated: {error}")
'''
    text = replace_once(text, old_main, new_main, "v9.4 main validation")

    TARGET.write_text(text, encoding="utf-8", newline="\n")
    print("Base v9.4 integrity patch applied")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
