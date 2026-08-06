from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
ALLOWED_DECISIONS = {"ADOPT", "ADAPT", "REJECT", "BLOCKED_UNVERIFIED"}
REQUIRED_FIELDS = {
    "source_repo",
    "source_commit",
    "registry_source",
    "registry_item",
    "registry_path",
    "component_path",
    "component_sha256",
    "license",
    "license_path",
    "license_blob_sha",
    "license_sha256",
    "declared_dependencies",
    "observed_import_packages",
    "scripts",
    "secrets",
    "files_added_or_replaced",
    "source_acquisition",
    "procurement_execution",
    "disposable_fixture",
    "installation",
    "decision",
    "reason_codes",
    "security_review",
    "accessibility_review",
    "runtime_review",
    "rollback",
}


def validate_receipt(receipt: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    missing = sorted(REQUIRED_FIELDS - receipt.keys())
    if missing:
        errors.append(f"missing fields: {missing}")

    if not COMMIT_RE.fullmatch(str(receipt.get("source_commit", ""))):
        errors.append("source_commit must be an exact 40-character lowercase hex commit")
    if not SHA256_RE.fullmatch(str(receipt.get("component_sha256", ""))):
        errors.append("component_sha256 must be a 64-character lowercase hex digest")
    if receipt.get("decision") not in ALLOWED_DECISIONS:
        errors.append(f"unsupported decision: {receipt.get('decision')!r}")

    for field in (
        "declared_dependencies",
        "observed_import_packages",
        "scripts",
        "secrets",
        "files_added_or_replaced",
        "reason_codes",
    ):
        if not isinstance(receipt.get(field), list):
            errors.append(f"{field} must be a list")

    reason_codes = set(receipt.get("reason_codes") or [])
    if receipt.get("source_acquisition") != "PASS":
        errors.append("pilot must prove exact source acquisition")
    if receipt.get("procurement_execution") != "PASS_DISPOSABLE_WEB_FIXTURE":
        errors.append("pilot must prove disposable Web procurement execution")
    fixture = receipt.get("disposable_fixture")
    if not isinstance(fixture, dict):
        errors.append("disposable_fixture must be an object")
    else:
        if fixture.get("procurement") != "PASS":
            errors.append("disposable fixture procurement must pass")
        if fixture.get("build") != "PASS":
            errors.append("disposable fixture build must pass")
        if not SHA256_RE.fullmatch(str(fixture.get("generated_component_sha256", ""))):
            errors.append("generated component must have an exact SHA-256 digest")
    if not COMMIT_RE.fullmatch(str(receipt.get("license_blob_sha", ""))):
        errors.append("license_blob_sha must be an exact Git blob SHA")
    if not SHA256_RE.fullmatch(str(receipt.get("license_sha256", ""))):
        errors.append("license_sha256 must be an exact SHA-256 digest")
    if "SOURCE_PACKAGE_VERSION_NOT_PUBLISHED" not in reason_codes:
        errors.append("unpublished source package version must remain explicit")
    if receipt.get("decision") != "BLOCKED_UNVERIFIED":
        errors.append("target-project adoption must remain BLOCKED_UNVERIFIED")
    if receipt.get("installation") != "NOT_RUN":
        errors.append("Base and target-project installation must remain NOT_RUN")
    if receipt.get("files_added_or_replaced") not in ([], None):
        errors.append("source-only pilot must not add or replace project files")
    if not str(receipt.get("rollback", "")).strip():
        errors.append("rollback must be non-empty")

    return {
        "valid": not errors,
        "decision": receipt.get("decision"),
        "errors": errors,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("receipt", type=Path)
    args = parser.parse_args()
    try:
        receipt = json.loads(args.receipt.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"valid": False, "decision": None, "errors": [str(exc)]}, ensure_ascii=False))
        return 1
    result = validate_receipt(receipt)
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
