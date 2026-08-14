from __future__ import annotations

import copy
import re
from collections.abc import Mapping, Sequence
from typing import Any

from .models import Budgets, CoverageEntry, Finding, FindingCode, Reference, ShadowRequest
from .paths import UnsafePath, duplicate_normalized_paths, normalize_repo_path


_ID = re.compile(r"^[A-Z0-9][A-Z0-9_-]{2,63}$")
_SHA = re.compile(r"^[0-9a-f]{40}$")

_REQUIRED_FIELDS = {
    "schema_version",
    "contract_role",
    "project_id",
    "run_id",
    "package_id",
    "source_main_sha",
    "observed_main_sha",
    "planning_status",
    "visual_impact",
    "visual_status",
    "planning_drift",
    "visual_drift",
    "approved_requirements",
    "package_requirement_ids",
    "coverage",
    "allowed_paths",
    "changed_paths",
    "required_evidence",
    "resource_locks",
    "references",
    "budgets",
    "autonomy",
    "a3_auto_merge_allowlist",
    "scheduler_runtime_provider",
}

_COVERAGE_FIELDS = {"requirement_id", "tasks", "outputs", "tests", "evidence"}
_REFERENCE_FIELDS = {"project_id", "kind", "path"}
_BUDGET_FIELDS = {"max_transitions", "max_repeated_failures"}


def _finding(code: FindingCode, message: str, path: str | None = None) -> Finding:
    return Finding(code=code, message=message, path=path)


def _string(value: object, label: str, findings: list[Finding]) -> str | None:
    if not isinstance(value, str) or not value:
        findings.append(_finding(FindingCode.INVALID_CONTRACT, f"{label} must be a non-empty string", label))
        return None
    return value


def _id(value: object, label: str, findings: list[Finding]) -> str | None:
    parsed = _string(value, label, findings)
    if parsed is not None and _ID.fullmatch(parsed) is None:
        findings.append(_finding(FindingCode.INVALID_CONTRACT, f"{label} has an invalid identifier", label))
        return None
    return parsed


def _sha(value: object, label: str, findings: list[Finding]) -> str | None:
    parsed = _string(value, label, findings)
    if parsed is not None and _SHA.fullmatch(parsed) is None:
        findings.append(_finding(FindingCode.INVALID_CONTRACT, f"{label} must be a lowercase 40-character SHA", label))
        return None
    return parsed


def _string_tuple(
    value: object,
    label: str,
    findings: list[Finding],
    *,
    require_nonempty: bool = True,
    casefold_unique: bool = True,
) -> tuple[str, ...] | None:
    if not isinstance(value, list):
        findings.append(_finding(FindingCode.INVALID_CONTRACT, f"{label} must be an array", label))
        return None
    if require_nonempty and not value:
        findings.append(_finding(FindingCode.INVALID_CONTRACT, f"{label} must not be empty", label))
        return None
    if not all(isinstance(item, str) and item for item in value):
        findings.append(_finding(FindingCode.INVALID_CONTRACT, f"{label} entries must be non-empty strings", label))
        return None
    parsed = tuple(value)
    keys = [item.casefold() if casefold_unique else item for item in parsed]
    if len(keys) != len(set(keys)):
        findings.append(_finding(FindingCode.INVALID_CONTRACT, f"{label} contains duplicate values", label))
        return None
    return parsed


def _path_tuple(
    value: object,
    label: str,
    findings: list[Finding],
    *,
    require_nonempty: bool = True,
) -> tuple[str, ...] | None:
    raw = _string_tuple(
        value,
        label,
        findings,
        require_nonempty=require_nonempty,
        casefold_unique=False,
    )
    if raw is None:
        return None
    try:
        duplicates = duplicate_normalized_paths(list(raw))
        normalized = tuple(normalize_repo_path(item) for item in raw)
    except UnsafePath as error:
        findings.append(_finding(FindingCode.INVALID_CONTRACT, f"{label}: {error}", label))
        return None
    if duplicates:
        findings.append(
            _finding(
                FindingCode.DUPLICATE_NORMALIZED_PATH,
                f"{label} contains paths that collide after NFC/case/path normalization",
                label,
            )
        )
        return None
    return normalized


def parse_shadow_request(value: object) -> tuple[ShadowRequest | None, tuple[Finding, ...]]:
    findings: list[Finding] = []
    if not isinstance(value, Mapping):
        return None, (_finding(FindingCode.INVALID_CONTRACT, "request must be a JSON object"),)

    raw_mapping = dict(value)
    unknown = sorted(set(raw_mapping) - _REQUIRED_FIELDS)
    for key in unknown:
        findings.append(_finding(FindingCode.UNKNOWN_FIELD, f"unknown request field: {key}", key))
    missing = sorted(_REQUIRED_FIELDS - set(raw_mapping))
    for key in missing:
        findings.append(_finding(FindingCode.MISSING_FIELD, f"missing required request field: {key}", key))
    if missing:
        return None, tuple(findings)

    if raw_mapping.get("schema_version") != 1:
        findings.append(_finding(FindingCode.INVALID_CONTRACT, "schema_version must be 1", "schema_version"))
    if raw_mapping.get("contract_role") != "LOOP_SHADOW_REQUEST":
        findings.append(
            _finding(FindingCode.INVALID_CONTRACT, "contract_role must be LOOP_SHADOW_REQUEST", "contract_role")
        )

    project_id = _id(raw_mapping.get("project_id"), "project_id", findings)
    run_id = _id(raw_mapping.get("run_id"), "run_id", findings)
    package_id = _id(raw_mapping.get("package_id"), "package_id", findings)
    source_main_sha = _sha(raw_mapping.get("source_main_sha"), "source_main_sha", findings)
    observed_main_sha = _sha(raw_mapping.get("observed_main_sha"), "observed_main_sha", findings)

    planning_status = _string(raw_mapping.get("planning_status"), "planning_status", findings)
    visual_impact = _string(raw_mapping.get("visual_impact"), "visual_impact", findings)
    visual_status = _string(raw_mapping.get("visual_status"), "visual_status", findings)
    planning_drift = _string(raw_mapping.get("planning_drift"), "planning_drift", findings)
    visual_drift = _string(raw_mapping.get("visual_drift"), "visual_drift", findings)

    if planning_status not in {None, "PLANNING_LOCKED"}:
        findings.append(
            _finding(FindingCode.INVALID_CONTRACT, "planning_status must be PLANNING_LOCKED", "planning_status")
        )
    if visual_impact not in {None, "NONE", "EXISTING_LOCKED", "NEW_VISUAL_REQUIRED"}:
        findings.append(_finding(FindingCode.INVALID_CONTRACT, "visual_impact is unsupported", "visual_impact"))
    if visual_status not in {None, "VISUAL_NOT_APPLICABLE", "VISUAL_LOCKED", "VISUAL_UNAVAILABLE"}:
        findings.append(_finding(FindingCode.INVALID_CONTRACT, "visual_status is unsupported", "visual_status"))
    if planning_drift not in {None, "NO_DRIFT", "MINOR_TECHNICAL_DRIFT", "PLANNING_CONFLICT", "UNVERIFIED"}:
        findings.append(_finding(FindingCode.INVALID_CONTRACT, "planning_drift is unsupported", "planning_drift"))
    if visual_drift not in {None, "NOT_APPLICABLE", "NO_DRIFT", "MINOR_TECHNICAL_DRIFT", "VISUAL_CONFLICT", "UNVERIFIED"}:
        findings.append(_finding(FindingCode.INVALID_CONTRACT, "visual_drift is unsupported", "visual_drift"))

    approved_requirements = _string_tuple(
        raw_mapping.get("approved_requirements"), "approved_requirements", findings
    )
    package_requirement_ids = _string_tuple(
        raw_mapping.get("package_requirement_ids"), "package_requirement_ids", findings
    )
    required_evidence = _string_tuple(
        raw_mapping.get("required_evidence"), "required_evidence", findings
    )
    resource_locks = _string_tuple(
        raw_mapping.get("resource_locks"), "resource_locks", findings
    )
    allowed_paths = _path_tuple(raw_mapping.get("allowed_paths"), "allowed_paths", findings)
    changed_paths = _path_tuple(raw_mapping.get("changed_paths"), "changed_paths", findings)

    coverage_entries: list[CoverageEntry] = []
    coverage_raw = raw_mapping.get("coverage")
    if not isinstance(coverage_raw, list):
        findings.append(_finding(FindingCode.INVALID_CONTRACT, "coverage must be an array", "coverage"))
    else:
        seen_requirements: set[str] = set()
        for index, item in enumerate(coverage_raw):
            label = f"coverage[{index}]"
            if not isinstance(item, Mapping):
                findings.append(_finding(FindingCode.INVALID_CONTRACT, f"{label} must be an object", label))
                continue
            item_mapping = dict(item)
            unknown_item = sorted(set(item_mapping) - _COVERAGE_FIELDS)
            missing_item = sorted(_COVERAGE_FIELDS - set(item_mapping))
            for key in unknown_item:
                findings.append(_finding(FindingCode.UNKNOWN_FIELD, f"unknown {label} field: {key}", f"{label}.{key}"))
            for key in missing_item:
                findings.append(_finding(FindingCode.MISSING_FIELD, f"missing {label} field: {key}", f"{label}.{key}"))
            if missing_item:
                continue
            requirement_id = _id(item_mapping.get("requirement_id"), f"{label}.requirement_id", findings)
            tasks = _string_tuple(item_mapping.get("tasks"), f"{label}.tasks", findings, require_nonempty=False)
            outputs = _path_tuple(item_mapping.get("outputs"), f"{label}.outputs", findings, require_nonempty=False)
            tests = _string_tuple(item_mapping.get("tests"), f"{label}.tests", findings, require_nonempty=False)
            evidence = _string_tuple(item_mapping.get("evidence"), f"{label}.evidence", findings, require_nonempty=False)
            if requirement_id is not None:
                key = requirement_id.casefold()
                if key in seen_requirements:
                    findings.append(
                        _finding(FindingCode.INVALID_CONTRACT, f"duplicate coverage requirement: {requirement_id}", label)
                    )
                seen_requirements.add(key)
            if None not in (requirement_id, tasks, outputs, tests, evidence):
                coverage_entries.append(
                    CoverageEntry(
                        requirement_id=requirement_id,
                        tasks=tasks,
                        outputs=outputs,
                        tests=tests,
                        evidence=evidence,
                    )
                )

    references: list[Reference] = []
    references_raw = raw_mapping.get("references")
    if not isinstance(references_raw, list) or not references_raw:
        findings.append(_finding(FindingCode.INVALID_CONTRACT, "references must be a non-empty array", "references"))
    else:
        for index, item in enumerate(references_raw):
            label = f"references[{index}]"
            if not isinstance(item, Mapping):
                findings.append(_finding(FindingCode.INVALID_CONTRACT, f"{label} must be an object", label))
                continue
            item_mapping = dict(item)
            for key in sorted(set(item_mapping) - _REFERENCE_FIELDS):
                findings.append(_finding(FindingCode.UNKNOWN_FIELD, f"unknown {label} field: {key}", f"{label}.{key}"))
            for key in sorted(_REFERENCE_FIELDS - set(item_mapping)):
                findings.append(_finding(FindingCode.MISSING_FIELD, f"missing {label} field: {key}", f"{label}.{key}"))
            if _REFERENCE_FIELDS - set(item_mapping):
                continue
            reference_project = _id(item_mapping.get("project_id"), f"{label}.project_id", findings)
            kind = _string(item_mapping.get("kind"), f"{label}.kind", findings)
            path = item_mapping.get("path")
            if not isinstance(path, str) or not path:
                findings.append(_finding(FindingCode.INVALID_CONTRACT, f"{label}.path must be a string", f"{label}.path"))
                normalized_path = None
            else:
                try:
                    normalized_path = normalize_repo_path(path)
                except UnsafePath:
                    normalized_path = path
            if None not in (reference_project, kind, normalized_path):
                references.append(Reference(reference_project, kind, normalized_path))

    budgets_raw = raw_mapping.get("budgets")
    budgets: Budgets | None = None
    if not isinstance(budgets_raw, Mapping):
        findings.append(_finding(FindingCode.INVALID_CONTRACT, "budgets must be an object", "budgets"))
    else:
        budgets_mapping = dict(budgets_raw)
        for key in sorted(set(budgets_mapping) - _BUDGET_FIELDS):
            findings.append(_finding(FindingCode.UNKNOWN_FIELD, f"unknown budgets field: {key}", f"budgets.{key}"))
        for key in sorted(_BUDGET_FIELDS - set(budgets_mapping)):
            findings.append(_finding(FindingCode.MISSING_FIELD, f"missing budgets field: {key}", f"budgets.{key}"))
        max_transitions = budgets_mapping.get("max_transitions")
        max_repeated_failures = budgets_mapping.get("max_repeated_failures")
        if not isinstance(max_transitions, int) or isinstance(max_transitions, bool) or not 1 <= max_transitions <= 256:
            findings.append(_finding(FindingCode.INVALID_CONTRACT, "max_transitions must be 1..256", "budgets.max_transitions"))
        if (
            not isinstance(max_repeated_failures, int)
            or isinstance(max_repeated_failures, bool)
            or not 1 <= max_repeated_failures <= 32
        ):
            findings.append(
                _finding(
                    FindingCode.INVALID_CONTRACT,
                    "max_repeated_failures must be 1..32",
                    "budgets.max_repeated_failures",
                )
            )
        if isinstance(max_transitions, int) and isinstance(max_repeated_failures, int):
            budgets = Budgets(max_transitions=max_transitions, max_repeated_failures=max_repeated_failures)

    autonomy = _string(raw_mapping.get("autonomy"), "autonomy", findings)
    a3_value = raw_mapping.get("a3_auto_merge_allowlist")
    scheduler = _string(
        raw_mapping.get("scheduler_runtime_provider"), "scheduler_runtime_provider", findings
    )
    if autonomy not in {None, "A2_EXECUTE_ISOLATED"}:
        findings.append(_finding(FindingCode.UNSAFE_AUTONOMY, "autonomy must remain A2_EXECUTE_ISOLATED", "autonomy"))
    if not isinstance(a3_value, list) or a3_value:
        findings.append(_finding(FindingCode.UNSAFE_AUTONOMY, "A3 auto-merge allowlist must remain empty", "a3_auto_merge_allowlist"))
        a3_allowlist: tuple[str, ...] | None = None
    else:
        a3_allowlist = ()
    if scheduler not in {None, "NOT_CONFIGURED"}:
        findings.append(_finding(FindingCode.UNSAFE_AUTONOMY, "Scheduler must remain NOT_CONFIGURED", "scheduler_runtime_provider"))

    if findings:
        return None, tuple(findings)

    assert None not in (
        project_id,
        run_id,
        package_id,
        source_main_sha,
        observed_main_sha,
        planning_status,
        visual_impact,
        visual_status,
        planning_drift,
        visual_drift,
        approved_requirements,
        package_requirement_ids,
        allowed_paths,
        changed_paths,
        required_evidence,
        resource_locks,
        budgets,
        autonomy,
        a3_allowlist,
        scheduler,
    )

    normalized_raw = copy.deepcopy(raw_mapping)
    normalized_raw["allowed_paths"] = list(allowed_paths)
    normalized_raw["changed_paths"] = list(changed_paths)
    normalized_raw["coverage"] = [
        {
            "requirement_id": entry.requirement_id,
            "tasks": list(entry.tasks),
            "outputs": list(entry.outputs),
            "tests": list(entry.tests),
            "evidence": list(entry.evidence),
        }
        for entry in coverage_entries
    ]
    normalized_raw["references"] = [
        {"project_id": item.project_id, "kind": item.kind, "path": item.path}
        for item in references
    ]

    return (
        ShadowRequest(
            schema_version=1,
            contract_role="LOOP_SHADOW_REQUEST",
            project_id=project_id,
            run_id=run_id,
            package_id=package_id,
            source_main_sha=source_main_sha,
            observed_main_sha=observed_main_sha,
            planning_status=planning_status,
            visual_impact=visual_impact,
            visual_status=visual_status,
            planning_drift=planning_drift,
            visual_drift=visual_drift,
            approved_requirements=approved_requirements,
            package_requirement_ids=package_requirement_ids,
            coverage=tuple(coverage_entries),
            allowed_paths=allowed_paths,
            changed_paths=changed_paths,
            required_evidence=required_evidence,
            resource_locks=resource_locks,
            references=tuple(references),
            budgets=budgets,
            autonomy=autonomy,
            a3_auto_merge_allowlist=a3_allowlist,
            scheduler_runtime_provider=scheduler,
            raw=normalized_raw,
        ),
        (),
    )
