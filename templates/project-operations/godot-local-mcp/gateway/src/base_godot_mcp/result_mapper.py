from __future__ import annotations

import re
from typing import Any, Iterable

from .project_identity import ProjectIdentity


_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$")
_TOOL_CAPABILITIES = frozenset({"scene.inspect", "node.rename", "task.status"})


class BridgeResultError(ValueError):
    """Raised when the Bridge returns a malformed or unsafe result."""


def _bounded_string(value: Any, *, maximum: int = 512) -> str | None:
    if not isinstance(value, str) or not value or len(value) > maximum:
        return None
    if "\x00" in value or "\r" in value:
        return None
    return value


def _operation_id(value: Any) -> str | None:
    text = _bounded_string(value, maximum=128)
    return text if text is not None and _ID_RE.fullmatch(text) else None


def _sha256(value: Any) -> str | None:
    return value if isinstance(value, str) and _SHA256_RE.fullmatch(value) else None


def _base_result(result: Any) -> tuple[bool, str, dict[str, Any]]:
    if not isinstance(result, dict):
        raise BridgeResultError("BRIDGE_RESULT_INVALID")
    success = result.get("success")
    code = _bounded_string(result.get("code"), maximum=128)
    data = result.get("data")
    if not isinstance(success, bool) or code is None or not isinstance(data, dict):
        raise BridgeResultError("BRIDGE_RESULT_INVALID")
    return success, code, data


def _copy_if_string(
    source: dict[str, Any],
    destination: dict[str, Any],
    key: str,
    *,
    maximum: int = 512,
) -> None:
    value = _bounded_string(source.get(key), maximum=maximum)
    if value is not None:
        destination[key] = value


def _status_result(
    success: bool,
    code: str,
    data: dict[str, Any],
    project: ProjectIdentity,
) -> dict[str, Any]:
    safe: dict[str, Any] = {
        "connected": data.get("connected") is True,
        "active_scene_path": None,
        "dirty_state": "UNKNOWN",
        "project_fingerprint": project.fingerprint,
    }
    scene = data.get("active_scene_path")
    if isinstance(scene, str) and scene.startswith("res://") and len(scene) <= 512:
        safe["active_scene_path"] = scene
    dirty = data.get("dirty_state")
    if dirty in {"CLEAN", "DIRTY", "UNKNOWN"}:
        safe["dirty_state"] = dirty
    for key in (
        "adapter_version",
        "editor_instance_id",
        "bridge_instance_id",
        "engine_version",
    ):
        _copy_if_string(data, safe, key, maximum=128)
    return {"success": success, "code": code, "data": safe}


def _catalog_result(
    success: bool,
    code: str,
    data: dict[str, Any],
    allowed_capabilities: Iterable[str],
) -> dict[str, Any]:
    reported = data.get("capabilities")
    reported_set = {
        value
        for value in reported
        if isinstance(value, str)
    } if isinstance(reported, list) else set()
    allowed = set(allowed_capabilities) & _TOOL_CAPABILITIES
    return {
        "success": success,
        "code": code,
        "data": {"capabilities": sorted(reported_set & allowed)},
    }


def _rename_result(
    success: bool,
    code: str,
    data: dict[str, Any],
) -> dict[str, Any]:
    safe: dict[str, Any] = {}
    operation_id = _operation_id(data.get("operation_id"))
    if operation_id is not None:
        safe["operation_id"] = operation_id
    request_hash = _sha256(data.get("request_hash"))
    if request_hash is not None:
        safe["request_hash"] = request_hash
    for key in ("saved_scene_sha256", "target_content_sha256", "result_hash"):
        digest = _sha256(data.get(key))
        if digest is not None:
            safe[key] = digest
    for key in ("state", "ledger_state", "dirty_state"):
        _copy_if_string(data, safe, key, maximum=64)
    normalized_code = "APPROVAL_PENDING" if code == "APPROVAL_REQUIRED" else code
    return {"success": success, "code": normalized_code, "data": safe}


def _inspect_result(
    success: bool,
    code: str,
    data: dict[str, Any],
) -> dict[str, Any]:
    safe: dict[str, Any] = {}
    for key in (
        "scene_path",
        "node_path",
        "node_name",
        "node_type",
        "dirty_state",
        "target_revision",
    ):
        _copy_if_string(data, safe, key)
    for key in ("target_content_sha256", "result_hash"):
        digest = _sha256(data.get(key))
        if digest is not None:
            safe[key] = digest
    child_count = data.get("child_count")
    if isinstance(child_count, int) and 0 <= child_count <= 100_000:
        safe["child_count"] = child_count
    return {"success": success, "code": code, "data": safe}


def _task_result(
    success: bool,
    code: str,
    data: dict[str, Any],
) -> dict[str, Any]:
    safe: dict[str, Any] = {}
    operation_id = _operation_id(data.get("operation_id"))
    if operation_id is not None:
        safe["operation_id"] = operation_id
    for key in ("state", "terminal_code", "message"):
        _copy_if_string(data, safe, key)
    for key in ("result_hash", "request_hash"):
        digest = _sha256(data.get(key))
        if digest is not None:
            safe[key] = digest
    return {"success": success, "code": code, "data": safe}


def normalize_bridge_result(
    method: str,
    result: Any,
    *,
    project: ProjectIdentity,
    allowed_capabilities: Iterable[str],
) -> dict[str, Any]:
    """Map one Bridge result to a bounded MCP result using a method allowlist."""

    success, code, data = _base_result(result)
    if method == "editor.status":
        return _status_result(success, code, data, project)
    if method == "capabilities.list":
        return _catalog_result(success, code, data, allowed_capabilities)
    if method == "node.rename":
        return _rename_result(success, code, data)
    if method == "scene.inspect":
        return _inspect_result(success, code, data)
    if method == "task.status":
        return _task_result(success, code, data)
    raise BridgeResultError("BRIDGE_METHOD_UNSUPPORTED")
