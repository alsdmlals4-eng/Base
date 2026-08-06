from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
GATEWAY_SRC = (
    ROOT
    / "templates/project-operations/godot-local-mcp/gateway/src"
)
SERVER_MODULE = GATEWAY_SRC / "base_godot_mcp/server.py"

EXPECTED_TOOLS = {
    "godot_doctor",
    "godot_status",
    "godot_catalog",
    "godot_scene_inspect",
    "godot_node_rename",
    "godot_task_status",
}


class _FakeBridge:
    def __init__(self) -> None:
        self.requests: list[tuple[str, dict[str, Any]]] = []

    async def request(self, method: str, payload: dict[str, Any]) -> dict[str, Any]:
        self.requests.append((method, payload))
        if method == "editor.status":
            return {
                "success": True,
                "code": "OK",
                "data": {
                    "connected": True,
                    "active_scene_path": "res://main.tscn",
                    "dirty_state": "CLEAN",
                },
            }
        if method == "capabilities.list":
            return {
                "success": True,
                "code": "OK",
                "data": {
                    "capabilities": ["scene.inspect", "node.rename", "task.status"],
                },
            }
        return {"success": True, "code": "OK", "data": payload}


class GodotLocalMcpServerTests(unittest.IsolatedAsyncioTestCase):
    def _require_server_module(self) -> None:
        self.assertTrue(
            SERVER_MODULE.is_file(),
            "Godot MCP Gateway server module is not implemented",
        )

    async def test_exact_six_tool_surface(self) -> None:
        self._require_server_module()
        sys.path.insert(0, str(GATEWAY_SRC))
        self.addCleanup(lambda: sys.path.remove(str(GATEWAY_SRC)))

        from mcp import Client
        from base_godot_mcp.profile_store import ClientProfile
        from base_godot_mcp.project_identity import ProjectIdentity
        from base_godot_mcp.server import GatewayDependencies, build_server

        with tempfile.TemporaryDirectory() as temporary:
            project_root = Path(temporary)
            (project_root / "project.godot").write_text(
                "[application]\nconfig/name=\"MCP Test\"\n",
                encoding="utf-8",
            )
            project = ProjectIdentity.from_root(project_root)
            profile = ClientProfile(
                profile_id="codex",
                enabled=True,
                allowed_project_fingerprints=(project.fingerprint,),
                allowed_capabilities=(
                    "editor.status",
                    "capabilities.list",
                    "scene.inspect",
                    "node.rename",
                    "task.status",
                ),
            )
            server = build_server(
                GatewayDependencies(
                    profile=profile,
                    project=project,
                    bridge=_FakeBridge(),
                )
            )
            async with Client(server) as client:
                result = await client.list_tools()

        self.assertEqual({tool.name for tool in result.tools}, EXPECTED_TOOLS)

    async def test_no_model_callable_approval_tool(self) -> None:
        self._require_server_module()
        source = SERVER_MODULE.read_text(encoding="utf-8")
        self.assertNotIn("approve_operation", source)
        self.assertNotIn("godot_approve", source)


if __name__ == "__main__":
    unittest.main()
