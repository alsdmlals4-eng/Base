from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
GATEWAY_SRC = ROOT / "templates/project-operations/godot-local-mcp/gateway/src"
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
                    "project_path": "/private/project",
                    "credential_secret": "must-not-leak",
                    "unbounded_internal_state": {"ignored": True},
                },
            }
        if method == "capabilities.list":
            return {
                "success": True,
                "code": "OK",
                "data": {
                    "capabilities": [
                        "scene.inspect",
                        "node.rename",
                        "task.status",
                        "shell.exec",
                        "arbitrary.gdscript",
                    ],
                },
            }
        if method == "node.rename":
            return {
                "success": False,
                "code": "APPROVAL_REQUIRED",
                "data": {
                    "operation_id": "op-rename-1",
                    "request_hash": "a" * 64,
                    "approval_token": "must-not-leak",
                    "internal_request": payload,
                },
            }
        return {"success": True, "code": "OK", "data": payload}


class GodotLocalMcpServerTests(unittest.IsolatedAsyncioTestCase):
    @classmethod
    def setUpClass(cls) -> None:
        sys.path.insert(0, str(GATEWAY_SRC))

    @classmethod
    def tearDownClass(cls) -> None:
        sys.path.remove(str(GATEWAY_SRC))

    def _require_server_module(self) -> None:
        self.assertTrue(
            SERVER_MODULE.is_file(),
            "Godot MCP Gateway server module is not implemented",
        )

    def _build_server(self, bridge: _FakeBridge):
        from base_godot_mcp.profile_store import ClientProfile
        from base_godot_mcp.project_identity import ProjectIdentity
        from base_godot_mcp.server import GatewayDependencies, build_server

        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        project_root = Path(temporary.name)
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
            GatewayDependencies(profile=profile, project=project, bridge=bridge)
        )
        return server, project

    async def test_exact_six_tool_surface(self) -> None:
        self._require_server_module()
        from mcp import Client

        server, _ = self._build_server(_FakeBridge())
        async with Client(server) as client:
            result = await client.list_tools()

        self.assertEqual({tool.name for tool in result.tools}, EXPECTED_TOOLS)

    async def test_status_redacts_bridge_internal_fields(self) -> None:
        from mcp import Client

        server, project = self._build_server(_FakeBridge())
        async with Client(server) as client:
            result = await client.call_tool("godot_status", {})

        self.assertFalse(result.is_error)
        self.assertEqual(
            result.structured_content,
            {
                "success": True,
                "code": "OK",
                "data": {
                    "connected": True,
                    "active_scene_path": "res://main.tscn",
                    "dirty_state": "CLEAN",
                    "project_fingerprint": project.fingerprint,
                },
            },
        )
        self.assertNotIn("/private/project", str(result))
        self.assertNotIn("must-not-leak", str(result))

    async def test_catalog_intersects_bridge_with_authorized_capabilities(self) -> None:
        from mcp import Client

        server, _ = self._build_server(_FakeBridge())
        async with Client(server) as client:
            result = await client.call_tool("godot_catalog", {})

        self.assertEqual(
            result.structured_content,
            {
                "success": True,
                "code": "OK",
                "data": {
                    "capabilities": ["node.rename", "scene.inspect", "task.status"]
                },
            },
        )

    async def test_scene_inspect_binds_profile_and_project_identity(self) -> None:
        from mcp import Client

        bridge = _FakeBridge()
        server, project = self._build_server(bridge)
        async with Client(server) as client:
            result = await client.call_tool(
                "godot_scene_inspect",
                {"scene_path": "res://main.tscn", "node_path": "Root/Camera"},
            )

        self.assertFalse(result.is_error)
        method, payload = bridge.requests[-1]
        self.assertEqual(method, "scene.inspect")
        self.assertEqual(payload["client_profile_id"], "codex")
        self.assertEqual(
            payload["project_identity"]["project_fingerprint"],
            project.fingerprint,
        )
        self.assertNotIn("normalized_root", payload["project_identity"])
        self.assertEqual(payload["scene_path"], "res://main.tscn")
        self.assertEqual(payload["node_path"], "Root/Camera")

    async def test_rename_maps_bridge_approval_to_pending_without_token(self) -> None:
        from mcp import Client

        server, _ = self._build_server(_FakeBridge())
        async with Client(server) as client:
            result = await client.call_tool(
                "godot_node_rename",
                {
                    "scene_path": "res://main.tscn",
                    "node_path": "Target",
                    "new_name": "Renamed",
                    "save_mode": "KEEP_DIRTY",
                },
            )

        self.assertFalse(result.is_error)
        self.assertEqual(
            result.structured_content,
            {
                "success": False,
                "code": "APPROVAL_PENDING",
                "data": {
                    "operation_id": "op-rename-1",
                    "request_hash": "a" * 64,
                },
            },
        )
        self.assertNotIn("approval_token", str(result))
        self.assertNotIn("internal_request", str(result))

    async def test_invalid_scene_path_fails_before_bridge_call(self) -> None:
        from mcp import Client

        bridge = _FakeBridge()
        server, _ = self._build_server(bridge)
        async with Client(server) as client:
            result = await client.call_tool(
                "godot_scene_inspect",
                {"scene_path": "../outside.tscn", "node_path": "."},
            )

        self.assertTrue(result.is_error)
        self.assertEqual(bridge.requests, [])

    async def test_no_model_callable_approval_tool(self) -> None:
        self._require_server_module()
        source = SERVER_MODULE.read_text(encoding="utf-8")
        self.assertNotIn("approve_operation", source)
        self.assertNotIn("godot_approve", source)


if __name__ == "__main__":
    unittest.main()
