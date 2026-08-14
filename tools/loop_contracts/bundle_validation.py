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

    blocking = {"SCHEMA_INVALID","CONTRACT_REFERENCE_MISSING","CONTRACT_UNREADABLE","UNSAFE_PROJECT_PATH"}
    if any(item.code in blocking for item in findings):
        return findings

    project_id = capsule["project_id"]
    for role, value in objects.items():
        if value.get("project_id") != project_id:
            findings.append(Finding("PROJECT_ID_MISMATCH", f"{role} project_id differs", paths[role]))

    source_sha = capsule["source_main_sha"]
    for role in ("planning","visual","package","coverage","active","immutable"):
        source_key = "source_commit" if role in {"planning","visual"} else "source_main_sha"
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
