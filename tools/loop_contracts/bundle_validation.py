from __future__ import annotations
from pathlib import Path
from .findings import Finding
from .loader import load_object, resolve_project_relative
from .schema_validation import validate_schema

FILES = {
    "capsule": ("loop-project-execution-capsule-v1.schema.json", None),
    "planning": ("loop-planning-lock-v1.schema.json", "planning_lock_path"),
    "visual": ("loop-visual-lock-v1.schema.json", "visual_lock_path"),
    "adapter": ("loop-runtime-adapter-v1.schema.json", "runtime_adapter_path"),
    "package": ("loop-implementation-package-v1.schema.json", "implementation_package_path"),
    "coverage": ("loop-requirement-coverage-ledger-v1.schema.json", "coverage_ledger_path"),
    "active": ("loop-active-run-v1.schema.json", "active_run_path"),
    "immutable": ("loop-immutable-run-v1.schema.json", "immutable_run_path"),
}


def validate_bundle(capsule_path: Path) -> list[Finding]:
    findings: list[Finding] = []
    root = capsule_path.parent.resolve(strict=True)
    try:
        capsule = load_object(capsule_path)
    except Exception as exc:
        return [Finding("CAPSULE_UNREADABLE", str(exc), str(capsule_path))]
    objects: dict[str, dict[str, object]] = {"capsule": capsule}
    paths: dict[str, str] = {"capsule": capsule_path.name}

    for role, (schema_name, key) in FILES.items():
        if role == "capsule":
            findings.extend(validate_schema(schema_name, capsule, capsule_path.name))
            continue
        relative = capsule.get(key)
        if not isinstance(relative, str):
            findings.append(Finding("CONTRACT_REFERENCE_MISSING", str(key), capsule_path.name))
            continue
        try:
            resolved = resolve_project_relative(root, relative)
            objects[role] = load_object(resolved)
            paths[role] = relative
            findings.extend(validate_schema(schema_name, objects[role], relative))
        except ValueError:
            findings.append(Finding("UNSAFE_PROJECT_PATH", relative, capsule_path.name))
        except Exception as exc:
            findings.append(Finding("CONTRACT_UNREADABLE", str(exc), relative))

    blocking = {"SCHEMA_INVALID", "CONTRACT_REFERENCE_MISSING", "CONTRACT_UNREADABLE", "UNSAFE_PROJECT_PATH"}
    if any(item.code in blocking for item in findings):
        return findings

    project_id = capsule["project_id"]
    for role, value in objects.items():
        if value.get("project_id") != project_id:
            findings.append(Finding("PROJECT_ID_MISMATCH", f"{role} project_id differs", paths[role]))

    source_sha = capsule["source_main_sha"]
    for role in ("planning", "visual", "package", "coverage", "active", "immutable"):
        source_key = "source_commit" if role in {"planning", "visual"} else "source_main_sha"
        if objects[role].get(source_key) != source_sha:
            findings.append(Finding("STALE_AUTHORITY", f"{role} source differs", paths[role]))

    planning_ids = {item["requirement_id"] for item in objects["planning"]["approved_requirements"]}
    package_ids = set(objects["package"]["requirement_ids"])
    coverage_items = objects["coverage"]["requirements"]
    coverage_ids = {item["requirement_id"] for item in coverage_items}

    for requirement_id in sorted(package_ids - planning_ids):
        findings.append(Finding("UNAPPROVED_REQUIREMENT", requirement_id, paths["package"]))
    for requirement_id in sorted(package_ids - coverage_ids):
        findings.append(Finding("UNMAPPED_REQUIREMENT", requirement_id, paths["coverage"]))
    for requirement_id in sorted(coverage_ids - package_ids):
        findings.append(Finding("UNAPPROVED_COVERAGE_ENTRY", requirement_id, paths["coverage"]))

    allowed_paths = set(objects["package"]["allowed_paths"])
    for item in coverage_items:
        if not item["tasks"] or not item["outputs"] or not item["tests"] or not item["evidence"]:
            findings.append(Finding("INCOMPLETE_COVERAGE", item["requirement_id"], paths["coverage"]))
        for output in item["outputs"]:
            if output not in allowed_paths:
                findings.append(Finding("UNAPPROVED_EXTRA_OUTPUT", output, paths["coverage"]))

    package = objects["package"]
    visual = objects["visual"]
    impact = package["visual_impact"]
    requirement = package["visual_lock_requirement"]
    if impact == "NEW_VISUAL_REQUIRED":
        findings.append(Finding("USER_DECISION_REQUIRED", "new visual design is not autonomous", paths["package"]))
    elif impact == "NONE" and (requirement != "VISUAL_NOT_APPLICABLE" or visual["status"] != "VISUAL_NOT_APPLICABLE"):
        findings.append(Finding("VISUAL_LOCK_MISMATCH", "NONE requires VISUAL_NOT_APPLICABLE", paths["package"]))
    elif impact == "EXISTING_LOCKED" and (requirement != "VISUAL_LOCKED" or visual["status"] != "VISUAL_LOCKED"):
        findings.append(Finding("VISUAL_LOCK_MISMATCH", "EXISTING_LOCKED requires VISUAL_LOCKED", paths["package"]))

    return findings


def validate_completion(capsule_path: Path) -> list[Finding]:
    """Validate that an already-ready Loop package may be reported complete.

    Readiness and completion are deliberately separate. `validate_bundle()`
    continues to allow MAPPED/IMPLEMENTED work so an approved package can
    start. This function adds fail-closed closure, execution-evidence, and
    destination-readback requirements without changing readiness semantics.
    """

    readiness_findings = validate_bundle(capsule_path)
    if readiness_findings:
        return readiness_findings

    root = capsule_path.parent.resolve(strict=True)
    capsule = load_object(capsule_path)

    package_relative = capsule["implementation_package_path"]
    coverage_relative = capsule["coverage_ledger_path"]
    package = load_object(resolve_project_relative(root, package_relative))
    coverage = load_object(resolve_project_relative(root, coverage_relative))

    receipt_relative = capsule.get("verification_receipt_path")
    if not isinstance(receipt_relative, str) or not receipt_relative:
        return [
            Finding(
                "COMPLETION_RECEIPT_MISSING",
                "completion requires verification_receipt_path",
                capsule_path.name,
            )
        ]

    try:
        receipt_path = resolve_project_relative(root, receipt_relative)
        receipt = load_object(receipt_path)
    except ValueError:
        return [Finding("UNSAFE_PROJECT_PATH", receipt_relative, capsule_path.name)]
    except Exception as exc:
        return [Finding("COMPLETION_RECEIPT_UNREADABLE", str(exc), receipt_relative)]

    findings = validate_schema(
        "loop-verification-receipt-v1.schema.json",
        receipt,
        receipt_relative,
    )
    if findings:
        return findings

    if receipt.get("project_id") != capsule.get("project_id"):
        findings.append(
            Finding(
                "COMPLETION_PROJECT_MISMATCH",
                "receipt project_id differs from capsule",
                receipt_relative,
            )
        )
    if receipt.get("source_main_sha") != capsule.get("source_main_sha"):
        findings.append(
            Finding(
                "COMPLETION_SOURCE_MISMATCH",
                "receipt source_main_sha differs from capsule",
                receipt_relative,
            )
        )
    if receipt.get("package_id") != package.get("package_id"):
        findings.append(
            Finding(
                "COMPLETION_PACKAGE_MISMATCH",
                "receipt package_id differs from implementation package",
                receipt_relative,
            )
        )

    exact_head_sha = str(receipt.get("exact_head_sha", "")).strip()
    if exact_head_sha == "0" * 40:
        findings.append(
            Finding(
                "COMPLETION_HEAD_PLACEHOLDER",
                "verification receipt exact_head_sha is still the template placeholder",
                receipt_relative,
            )
        )

    checks = receipt["checks"]
    destinations = receipt["destinations"]
    if not any(check["required"] for check in checks):
        findings.append(
            Finding(
                "REQUIRED_CHECK_MISSING",
                "completion requires at least one required verification check",
                receipt_relative,
            )
        )
    if not any(destination["required"] for destination in destinations):
        findings.append(
            Finding(
                "REQUIRED_DESTINATION_MISSING",
                "completion requires at least one required destination readback",
                receipt_relative,
            )
        )

    if coverage.get("status") != "VERIFIED":
        findings.append(
            Finding(
                "COMPLETION_COVERAGE_OPEN",
                f"coverage ledger status is {coverage.get('status')!r}, expected 'VERIFIED'",
                coverage_relative,
            )
        )

    closed_requirement_states = {"VERIFIED", "DEFERRED_APPROVED"}
    for item in coverage["requirements"]:
        status = item["status"]
        if status not in closed_requirement_states:
            findings.append(
                Finding(
                    "COMPLETION_REQUIREMENT_OPEN",
                    f"{item['requirement_id']} is {status}; expected VERIFIED or DEFERRED_APPROVED",
                    coverage_relative,
                )
            )

    if receipt.get("status") != "VERIFIED":
        findings.append(
            Finding(
                "COMPLETION_RECEIPT_OPEN",
                f"verification receipt status is {receipt.get('status')!r}, expected 'VERIFIED'",
                receipt_relative,
            )
        )

    for check in checks:
        status = check["status"]
        check_id = check["check_id"]
        reason = str(check.get("reason", "")).strip()
        evidence_ref = str(check.get("evidence_ref", "")).strip()

        if status != "PASS" and not reason:
            findings.append(
                Finding(
                    "CHECK_REASON_MISSING",
                    f"{check_id} is {status} without a reason",
                    receipt_relative,
                )
            )
        if check["required"] and status != "PASS":
            findings.append(
                Finding(
                    "REQUIRED_CHECK_NOT_PASS",
                    f"required check {check_id} is {status}",
                    receipt_relative,
                )
            )
        if check["required"] and status == "PASS" and not evidence_ref:
            findings.append(
                Finding(
                    "CHECK_EVIDENCE_MISSING",
                    f"required PASS check {check_id} has no evidence_ref",
                    receipt_relative,
                )
            )

    for destination in destinations:
        destination_id = destination["destination_id"]
        expected_ref = str(destination.get("expected_ref", "")).strip()
        observed_ref = str(destination.get("observed_ref", "")).strip()
        sync_state = destination["sync_state"]
        evidence_ref = str(destination.get("evidence_ref", "")).strip()

        if sync_state == "SYNCED" and expected_ref != observed_ref:
            findings.append(
                Finding(
                    "DESTINATION_REF_MISMATCH",
                    f"{destination_id} is marked SYNCED but expected_ref != observed_ref",
                    receipt_relative,
                )
            )

        if destination["required"]:
            if not expected_ref or not observed_ref:
                findings.append(
                    Finding(
                        "DESTINATION_READBACK_MISSING",
                        f"required destination {destination_id} lacks expected/observed readback",
                        receipt_relative,
                    )
                )
            elif expected_ref != observed_ref and sync_state != "SYNCED":
                findings.append(
                    Finding(
                        "DESTINATION_REF_MISMATCH",
                        f"required destination {destination_id} expected_ref != observed_ref",
                        receipt_relative,
                    )
                )
            if sync_state != "SYNCED":
                findings.append(
                    Finding(
                        "DESTINATION_NOT_SYNCED",
                        f"required destination {destination_id} is {sync_state}",
                        receipt_relative,
                    )
                )
            if not evidence_ref:
                findings.append(
                    Finding(
                        "DESTINATION_EVIDENCE_MISSING",
                        f"required destination {destination_id} has no evidence_ref",
                        receipt_relative,
                    )
                )

    return findings
