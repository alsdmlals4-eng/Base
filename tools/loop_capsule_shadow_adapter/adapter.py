from __future__ import annotations

from pathlib import Path
from typing import Any

from tools.loop_contracts import validate_bundle
from tools.loop_contracts.loader import load_object, resolve_project_relative
from tools.loop_shadow_kernel.contract import parse_shadow_request
from tools.loop_shadow_kernel.paths import normalize_repo_path


class AdapterError(ValueError):
    pass


def _error(code: str, message: str) -> AdapterError:
    return AdapterError(f"{code}: {message}")


def _load_referenced(root: Path, capsule: dict[str, Any], key: str) -> dict[str, Any]:
    relative = capsule.get(key)
    if not isinstance(relative, str):
        raise _error("CONTRACT_REFERENCE_MISSING", key)
    try:
        return load_object(resolve_project_relative(root, relative))
    except Exception as exc:
        raise _error("CONTRACT_UNREADABLE", f"{key}: {exc}") from exc


def _raise_m2_findings(capsule_path: Path) -> None:
    findings = validate_bundle(capsule_path)
    if not findings:
        return
    rendered = "; ".join(
        f"{getattr(item, 'code', 'M2_FINDING')}:{getattr(item, 'message', str(item))}"
        for item in findings
    )
    raise AdapterError(rendered)


def _normalized_changed_paths(coverage: dict[str, Any]) -> list[str]:
    outputs: set[str] = set()
    for item in coverage.get("requirements", []):
        if not isinstance(item, dict):
            continue
        for output in item.get("outputs", []):
            if isinstance(output, str):
                outputs.add(normalize_repo_path(output))
    return sorted(outputs, key=lambda item: (item.casefold(), item))


def _validate_runtime_drift(
    *,
    visual_impact: str,
    planning_drift: str,
    visual_drift: str,
) -> None:
    if planning_drift in {"PLANNING_CONFLICT", "UNVERIFIED"}:
        raise _error(
            "PLANNING_DRIFT_BLOCKED",
            f"planning drift must be verified before SHADOW translation: {planning_drift}",
        )
    if visual_impact == "NONE":
        if visual_drift != "NOT_APPLICABLE":
            raise _error(
                "VISUAL_DRIFT_BLOCKED",
                "visual impact NONE requires NOT_APPLICABLE drift",
            )
    elif visual_impact == "EXISTING_LOCKED":
        if visual_drift not in {"NO_DRIFT", "MINOR_TECHNICAL_DRIFT"}:
            raise _error(
                "VISUAL_DRIFT_BLOCKED",
                f"locked visual work requires verified drift: {visual_drift}",
            )
    elif visual_impact == "NEW_VISUAL_REQUIRED":
        raise _error(
            "USER_DECISION_REQUIRED",
            "new visual design cannot be translated into autonomous SHADOW work",
        )


def build_shadow_request(
    capsule_path: Path | str,
    *,
    run_id: str,
    observed_main_sha: str,
    planning_drift: str,
    visual_drift: str,
) -> dict[str, Any]:
    """Translate one valid M2 Capsule bundle into one closed M3 SHADOW request.

    The function is read-only. Authority-bearing values come only from the
    validated M2 documents. Runtime observations are deliberately limited to
    run identity, observed main SHA, and planning/visual drift observations.
    """

    path = Path(capsule_path)
    _raise_m2_findings(path)
    root = path.parent.resolve(strict=True)
    capsule = load_object(path)
    planning = _load_referenced(root, capsule, "planning_lock_path")
    visual = _load_referenced(root, capsule, "visual_lock_path")
    package = _load_referenced(root, capsule, "implementation_package_path")
    coverage = _load_referenced(root, capsule, "coverage_ledger_path")

    source_main_sha = capsule.get("source_main_sha")
    if observed_main_sha != source_main_sha:
        raise _error(
            "STALE_MAIN_SHA",
            "observed main SHA differs from the validated Capsule source_main_sha",
        )

    visual_impact = str(package["visual_impact"])
    _validate_runtime_drift(
        visual_impact=visual_impact,
        planning_drift=planning_drift,
        visual_drift=visual_drift,
    )

    project_id = str(capsule["project_id"])
    approved_requirements = [
        str(item["requirement_id"])
        for item in planning["approved_requirements"]
    ]
    package_requirement_ids = [str(item) for item in package["requirement_ids"]]

    coverage_entries: list[dict[str, Any]] = []
    for item in coverage["requirements"]:
        coverage_entries.append(
            {
                "requirement_id": str(item["requirement_id"]),
                "tasks": [str(value) for value in item["tasks"]],
                "outputs": [str(value) for value in item["outputs"]],
                "tests": [str(value) for value in item["tests"]],
                "evidence": [str(value) for value in item["evidence"]],
            }
        )

    references = [
        {
            "project_id": project_id,
            "kind": "CANON",
            "path": str(source["path"]),
        }
        for source in planning["authority_sources"]
    ]

    request: dict[str, Any] = {
        "schema_version": 1,
        "contract_role": "LOOP_SHADOW_REQUEST",
        "project_id": project_id,
        "run_id": run_id,
        "package_id": str(package["package_id"]),
        "source_main_sha": str(source_main_sha),
        "observed_main_sha": observed_main_sha,
        "planning_status": str(planning["status"]),
        "visual_impact": visual_impact,
        "visual_status": str(visual["status"]),
        "planning_drift": planning_drift,
        "visual_drift": visual_drift,
        "approved_requirements": approved_requirements,
        "package_requirement_ids": package_requirement_ids,
        "coverage": coverage_entries,
        "allowed_paths": [str(value) for value in package["allowed_paths"]],
        "changed_paths": _normalized_changed_paths(coverage),
        "required_evidence": [str(value) for value in package["required_evidence_levels"]],
        "resource_locks": [str(value) for value in package["resource_locks"]],
        "references": references,
        "budgets": {
            "max_transitions": 16,
            "max_repeated_failures": 2,
        },
        "autonomy": str(capsule["autonomy"]),
        "a3_auto_merge_allowlist": list(capsule["a3_auto_merge_allowlist"]),
        "scheduler_runtime_provider": str(capsule["scheduler_runtime_provider"]),
    }

    parsed, findings = parse_shadow_request(request)
    if parsed is None:
        rendered = "; ".join(
            f"{getattr(item.code, 'value', item.code)}:{item.message}"
            for item in findings
        )
        raise AdapterError(rendered)

    # M3 normalizes paths and other closed values. Returning the normalized raw
    # object ensures callers cannot retain alternate separator/Unicode spellings.
    return dict(parsed.raw)
