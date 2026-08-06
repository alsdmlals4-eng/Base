from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BRIDGE_ROOT = (
    ROOT
    / "templates/project-operations/godot-local-mcp/addons/base_godot_mcp_bridge"
)
ADOPTION = (
    ROOT
    / "templates/project-operations/godot-local-mcp/GODOT_LOCAL_MCP_ADOPTION_MANIFEST.example.json"
)
REQUIRED_FILES = (
    "plugin.cfg",
    "plugin.gd",
    "bridge_codec.gd",
    "bridge_server.gd",
    "bridge_session.gd",
    "profile_store.gd",
    "descriptor_store.gd",
    "approval_store.gd",
    "approval_dock.gd",
    "README.md",
)
FORBIDDEN_SOURCE = (
    "0.0.0.0",
    '"::"',
    "WebSocket",
    "HTTPServer",
    "PacketPeerUDP",
    "OS.execute",
    "Expression.new",
    "GDScript.new",
    "_editor_transaction_executor",
    "approve_operation",
    "godot_approve",
)


class GodotLocalMcpEditorBridgeTests(unittest.TestCase):
    def test_required_bridge_files_exist(self) -> None:
        for name in REQUIRED_FILES:
            self.assertTrue((BRIDGE_ROOT / name).is_file(), name)
        self.assertTrue(ADOPTION.is_file())

    def test_plugin_extends_adapter_and_binds_ipv4_loopback_only(self) -> None:
        source = (BRIDGE_ROOT / "plugin.gd").read_text(encoding="utf-8")
        self.assertIn(
            'extends "res://addons/base_live_editor_adapter/plugin.gd"',
            source,
        )
        self.assertIn('const BIND_HOST := "127.0.0.1"', source)
        self.assertIn('const PROTOCOL := "BASE_GODOT_BRIDGE_V1"', source)
        self.assertIn("submit_validated_operation", source)
        self.assertIn("take_completed_result", source)
        self.assertIn("availability()", source)

    def test_bridge_has_no_remote_or_model_callable_approval_surface(self) -> None:
        combined = "\n".join(
            path.read_text(encoding="utf-8")
            for path in BRIDGE_ROOT.glob("*.gd")
            if path.is_file()
        )
        for marker in FORBIDDEN_SOURCE:
            self.assertNotIn(marker, combined)
        self.assertNotIn("MCPServer", combined)
        self.assertNotIn("tools/list", combined)
        self.assertNotIn("tools/call", combined)

    def test_adoption_manifest_is_closed_and_not_configured(self) -> None:
        payload = json.loads(ADOPTION.read_text(encoding="utf-8"))
        self.assertEqual(payload["schema_version"], 1)
        self.assertEqual(payload["artifact_role"], "GODOT_LOCAL_MCP_ADOPTION_MANIFEST")
        self.assertEqual(payload["configuration_state"], "NOT_CONFIGURED")
        self.assertEqual(payload["bridge_protocol"], "BASE_GODOT_BRIDGE_V1")
        self.assertEqual(payload["bind_host"], "127.0.0.1")
        self.assertEqual(payload["port_policy"], "EPHEMERAL")
        self.assertEqual(payload["allowed_profile_ids"], ["codex", "gpt-vscode"])
        self.assertEqual(
            payload["allowed_capabilities"],
            [
                "editor.status",
                "capabilities.list",
                "scene.inspect",
                "node.rename",
                "task.status",
            ],
        )
        self.assertFalse(payload["test_approval_broker"])
        self.assertFalse(payload["production_adapter_ready"])
        self.assertLessEqual(payload["max_frame_bytes"], 262_144)

    def test_descriptor_and_profile_stores_reject_project_local_roots(self) -> None:
        descriptor = (BRIDGE_ROOT / "descriptor_store.gd").read_text(encoding="utf-8")
        profile = (BRIDGE_ROOT / "profile_store.gd").read_text(encoding="utf-8")
        combined = descriptor + profile
        self.assertIn("BASE_GODOT_MCP_CONFIG_DIR", combined)
        self.assertIn("CONFIG_ROOT_PROJECT_LOCAL_FORBIDDEN", combined)
        self.assertIn("res://", combined)
        self.assertIn("user://", combined)
        self.assertIn("deepseek", profile)
        self.assertIn("MCP_CLIENT_PROFILE_DENIED", profile)

    def test_rename_is_stored_pending_and_not_submitted_before_human_approval(self) -> None:
        plugin = (BRIDGE_ROOT / "plugin.gd").read_text(encoding="utf-8")
        approval = (BRIDGE_ROOT / "approval_store.gd").read_text(encoding="utf-8")
        self.assertIn('"APPROVAL_REQUIRED"', plugin)
        self.assertIn('"PENDING_APPROVAL"', plugin)
        self.assertIn("store_pending", plugin)
        self.assertIn("human_approved", approval)
        rename_case = plugin.split('"node.rename"', 1)[1]
        rename_case = rename_case.split('"task.status"', 1)[0]
        self.assertNotIn("submit_validated_operation", rename_case)


if __name__ == "__main__":
    unittest.main()
