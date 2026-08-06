from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Literal, Protocol

from mcp.server import MCPServer

from .profile_store import ClientProfile
from .project_identity import ProjectIdentity


_MAX_PATH_CHARS = 512
_MAX_NAME_CHARS = 128
_OPERATION_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$")


class BridgeProtocol(Protocol):
    async def request(self, method: str, payload: dict[str, Any]) -> dict[str, Any]: ...


@dataclass(frozen=True, slots=True)
class GatewayDependencies:
    profile: ClientProfile
    project: ProjectIdentity
    bridge: BridgeProtocol


def _validate_res_path(value: str, *, field: str) -> str:
    if not value.startswith("res://"):
        raise ValueError(f"{field.upper()}_MUST_BE_RES_PATH")
    relative = value.removeprefix("res://")
    if not relative or len(value) > _MAX_PATH_CHARS:
        raise ValueError(f"{field.upper()}_INVALID")
    if any(part in {"", ".", ".."} for part in relative.replace("\\", "/").split("/")):
        raise ValueError(f"{field.upper()}_INVALID")
    return value


def _validate_node_path(value: str) -> str:
    if not value or len(value) > _MAX_PATH_CHARS or "\n" in value or "\r" in value:
        raise ValueError("NODE_PATH_INVALID")
    if value.startswith("/") or ".." in value.replace("\\", "/").split("/"):
        raise ValueError("NODE_PATH_INVALID")
    return value


def _validate_new_name(value: str) -> str:
    if not value or len(value) > _MAX_NAME_CHARS:
        raise ValueError("NEW_NAME_INVALID")
    if any(token in value for token in ("/", "\\", "\n", "\r", ":")):
        raise ValueError("NEW_NAME_INVALID")
    return value


def _validate_operation_id(value: str) -> str:
    if not _OPERATION_ID_RE.fullmatch(value):
        raise ValueError("OPERATION_ID_INVALID")
    return value


def build_server(dependencies: GatewayDependencies) -> MCPServer:
    """Build the closed six-tool Godot MCP server."""

    dependencies.profile.require_project(dependencies.project.fingerprint)
    mcp = MCPServer("Base Godot MCP Gateway")

    async def bridge_request(
        capability: str,
        method: str,
        payload: dict[str, Any],
    ) -> dict[str, Any]:
        dependencies.profile.require_capability(capability)
        request_payload = {
            "client_profile_id": dependencies.profile.profile_id,
            "project_identity": dependencies.project.public_summary(),
            **payload,
        }
        result = await dependencies.bridge.request(method, request_payload)
        if not isinstance(result, dict):
            raise ValueError("BRIDGE_RESULT_INVALID")
        return result

    @mcp.tool()
    async def godot_doctor() -> dict[str, Any]:
        """Validate the selected profile and exact Godot project identity."""
        return {
            "success": True,
            "code": "OK",
            "data": {
                **dependencies.project.public_summary(),
                "client_profile_id": dependencies.profile.profile_id,
                "mcp_transport": "stdio",
            },
        }

    @mcp.tool()
    async def godot_status() -> dict[str, Any]:
        """Return bounded status for the authorized Godot Editor Bridge."""
        return await bridge_request("editor.status", "editor.status", {})

    @mcp.tool()
    async def godot_catalog() -> dict[str, Any]:
        """List the typed Godot capabilities available to this profile."""
        return await bridge_request("capabilities.list", "capabilities.list", {})

    @mcp.tool()
    async def godot_scene_inspect(
        scene_path: str,
        node_path: str = ".",
    ) -> dict[str, Any]:
        """Inspect one Scene or Node through the registered read-only capability."""
        return await bridge_request(
            "scene.inspect",
            "scene.inspect",
            {
                "scene_path": _validate_res_path(scene_path, field="scene_path"),
                "node_path": _validate_node_path(node_path),
            },
        )

    @mcp.tool()
    async def godot_node_rename(
        scene_path: str,
        node_path: str,
        new_name: str,
        save_mode: Literal["KEEP_DIRTY", "SAVE_CURRENT_SCENE"] = "KEEP_DIRTY",
    ) -> dict[str, Any]:
        """Request one guarded Node rename; human approval remains outside MCP."""
        return await bridge_request(
            "node.rename",
            "node.rename",
            {
                "scene_path": _validate_res_path(scene_path, field="scene_path"),
                "node_path": _validate_node_path(node_path),
                "new_name": _validate_new_name(new_name),
                "save_mode": save_mode,
            },
        )

    @mcp.tool()
    async def godot_task_status(operation_id: str) -> dict[str, Any]:
        """Read one operation or long-running task result by exact identity."""
        return await bridge_request(
            "task.status",
            "task.status",
            {"operation_id": _validate_operation_id(operation_id)},
        )

    return mcp
