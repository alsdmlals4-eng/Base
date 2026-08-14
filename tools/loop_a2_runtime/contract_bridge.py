from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Callable, Iterable

from .protocol import Budgets, ProtocolError, RunRequest, normalize_contract_path


class ContractBridgeError(ValueError):
    pass


def _load_object(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ContractBridgeError(f"expected object: {path}")
    return value


def _resolve(root: Path, relative: str) -> Path:
    normalized = normalize_contract_path(relative, "contract_path")
    candidate = (root / normalized).resolve(strict=False)
    resolved_root = root.resolve(strict=True)
    if candidate != resolved_root and resolved_root not in candidate.parents:
        raise ContractBridgeError(f"path escapes project root: {relative}")
    return candidate


def _default_validator(capsule_path: Path) -> Iterable[Any]:
    from tools.loop_contracts.bundle_validation import validate_bundle
    return validate_bundle(capsule_path)


def build_request_from_capsule(
    *,
    project_root: Path,
    capsule_relative: str,
    run_id: str,
    provider_mode: str,
    budgets: Budgets,
    bundle_validator: Callable[[Path], Iterable[Any]] | None = None,
) -> RunRequest:
    root = project_root.resolve(strict=True)
    capsule_path = _resolve(root, capsule_relative)
    findings = list((bundle_validator or _default_validator)(capsule_path))
    if findings:
        codes = [getattr(item, "code", "CONTRACT_INVALID") for item in findings]
        raise ContractBridgeError(f"capsule bundle is not ready: {codes}")

    capsule = _load_object(capsule_path)
    package_relative = capsule.get("implementation_package_path")
    if not isinstance(package_relative, str):
        raise ContractBridgeError("capsule implementation_package_path is missing")
    package_path = _resolve(capsule_path.parent, package_relative)
    package = _load_object(package_path)

    if capsule.get("status") != "ADOPTED" or capsule.get("autonomy") != "A2_EXECUTE_ISOLATED":
        raise ContractBridgeError("capsule does not authorize bounded A2")
    if package.get("execution_gate") != "AUTONOMOUS_IMPLEMENTATION_READY":
        raise ContractBridgeError("package entry gate is not ready")
    if package.get("visual_impact") == "NEW_VISUAL_REQUIRED":
        raise ContractBridgeError("new visual design requires user decision")
    if package.get("project_id") != capsule.get("project_id"):
        raise ContractBridgeError("package project_id differs from capsule")
    if package.get("source_main_sha") != capsule.get("source_main_sha"):
        raise ContractBridgeError("package authority SHA differs from capsule")

    return RunRequest.from_dict({
        "schema_version": 1,
        "contract_role": "LOOP_A2_RUN_REQUEST",
        "project_id": capsule["project_id"],
        "run_id": run_id,
        "package_id": package["package_id"],
        "expected_main_sha": capsule["source_main_sha"],
        "capsule_path": normalize_contract_path(capsule_relative, "capsule_relative"),
        "package_path": normalize_contract_path(
            str(package_path.relative_to(root)).replace("\\", "/"), "package_path"
        ),
        "allowed_paths": package["allowed_paths"],
        "forbidden_paths": package["forbidden_paths"],
        "resource_locks": package["resource_locks"],
        "requirement_ids": package["requirement_ids"],
        "budgets": {
            "max_turns": budgets.max_turns,
            "max_repair_cycles": budgets.max_repair_cycles,
            "timeout_seconds": budgets.timeout_seconds,
        },
        "provider_mode": provider_mode,
    })
