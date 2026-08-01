#!/usr/bin/env python3
"""Apply the approved Base v9.4 trusted-evidence validation patch."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "tools/check_base_v9_integrity.py"


def replace_once(text: str, old: str, new: str, label: str) -> str:
    if new in text:
        return text
    if old not in text:
        raise RuntimeError(f"Cannot locate patch target: {label}")
    return text.replace(old, new, 1)


def main() -> int:
    text = TARGET.read_text(encoding="utf-8")

    text = replace_once(
        text,
        'V94_CANDIDATE_LOCK_SCHEMA = ROOT / "schemas/base-v9-4-candidate-lock-v1.schema.json"\n',
        'V94_CANDIDATE_LOCK_SCHEMA = ROOT / "schemas/base-v9-4-candidate-lock-v1.schema.json"\n'
        'V94_EVIDENCE_PATH = "docs/operations/BASE_V9_4_RELEASE_EVIDENCE.json"\n'
        'V94_EVIDENCE_SCHEMA = ROOT / "schemas/base-v9-4-release-evidence-v1.schema.json"\n',
        "v9.4 evidence constants",
    )

    function_marker = "\ndef v94_release_lock_errors(repository: Path, candidate_lock: dict, trusted_history_commit: str) -> list[str]:\n"
    function = '''
def v94_evidence_record_errors(candidate_lock: dict, evidence: dict, schema: dict) -> list[str]:
    """Validate trusted v9.4 evidence against the exact candidate identity."""
    errors: list[str] = []
    for error in sorted(Draft202012Validator(schema).iter_errors(evidence), key=lambda item: list(item.path)):
        location = ".".join(str(part) for part in error.path) or "<root>"
        errors.append(f"v9.4 release evidence record {location}: {error.message}")

    if evidence.get("payload_commit") != candidate_lock.get("candidate_release_commit"):
        errors.append("v9.4 release evidence payload does not match the candidate lock")
    if evidence.get("candidate_issue") != candidate_lock.get("github_issue"):
        errors.append("v9.4 release evidence candidate Issue does not match the candidate lock")
    if evidence.get("linked_issue") != candidate_lock.get("linked_issue"):
        errors.append("v9.4 release evidence linked Issue does not match the candidate lock")

    registry = candidate_lock.get("candidate_registry")
    expected_hash = registry.get("sha256") if isinstance(registry, dict) else None
    if evidence.get("registry_sha256") != expected_hash:
        errors.append("v9.4 release evidence Registry does not match the candidate lock")
    return errors


'''
    if "def v94_evidence_record_errors" not in text:
        if function_marker not in text:
            raise RuntimeError("Cannot locate v9.4 evidence function insertion point")
        text = text.replace(function_marker, "\n" + function + function_marker.lstrip("\n"), 1)

    old_release_block = '''        if result.returncode:
            errors.append(message)
    payload_blob = subprocess.run(
        ["git", "-C", str(repository), "show", f"{release_commit}:{registry_path}"],
'''
    new_release_block = '''        if result.returncode:
            errors.append(message)

    evidence = _commit_json(repository, evidence_commit, V94_EVIDENCE_PATH)
    if evidence is None:
        errors.append("v9.4 release evidence record is unavailable or invalid")
    else:
        try:
            evidence_schema = json.loads(V94_EVIDENCE_SCHEMA.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as error:
            errors.append(f"v9.4 release evidence schema is unavailable: {error}")
        else:
            errors.extend(v94_evidence_record_errors(candidate_lock, evidence, evidence_schema))

    payload_blob = subprocess.run(
        ["git", "-C", str(repository), "show", f"{release_commit}:{registry_path}"],
'''
    text = replace_once(text, old_release_block, new_release_block, "v9.4 released evidence validation")

    TARGET.write_text(text, encoding="utf-8", newline="\n")
    print("Base v9.4 evidence validation patch applied")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
