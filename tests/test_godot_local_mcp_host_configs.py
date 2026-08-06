from __future__ import annotations

import json
import tomllib
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MCP_ROOT = ROOT / "templates/project-operations/godot-local-mcp"
HOSTS = MCP_ROOT / "hosts"
README = MCP_ROOT / "README.md"
EXPECTED_TOOLS = [
    "godot_doctor",
    "godot_status",
    "godot_catalog",
    "godot_scene_inspect",
    "godot_node_rename",
    "godot_task_status",
]


class GodotLocalMcpHostConfigTests(unittest.TestCase):
    def test_codex_config_is_project_scoped_example_with_exact_tools(self) -> None:
        path = HOSTS / "codex.config.toml.example"
        self.assertTrue(path.is_file())
        payload = tomllib.loads(path.read_text(encoding="utf-8"))
        server = payload["mcp_servers"]["godot_local"]

        self.assertEqual(server["command"], "python")
        self.assertEqual(server["args"], ["-m", "base_godot_mcp"])
        self.assertTrue(server["enabled"])
        self.assertTrue(server["required"])
        self.assertEqual(server["enabled_tools"], EXPECTED_TOOLS)
        self.assertEqual(server["default_tools_approval_mode"], "prompt")
        self.assertEqual(server["env"]["BASE_GODOT_MCP_PROFILE_ID"], "codex")
        self.assertNotIn("credential_secret", path.read_text(encoding="utf-8"))

    def test_vscode_config_uses_user_profile_shape_and_exact_environment(self) -> None:
        path = HOSTS / "vscode.user.mcp.json.example"
        self.assertTrue(path.is_file())
        payload = json.loads(path.read_text(encoding="utf-8"))
        server = payload["servers"]["godotLocal"]

        self.assertEqual(server["type"], "stdio")
        self.assertEqual(server["command"], "python")
        self.assertEqual(server["args"], ["-m", "base_godot_mcp"])
        self.assertEqual(server["cwd"], "${workspaceFolder}")
        self.assertEqual(server["env"]["BASE_GODOT_MCP_PROFILE_ID"], "gpt-vscode")
        self.assertEqual(
            server["env"]["BASE_GODOT_PROJECT_ROOT"],
            "${workspaceFolder}",
        )
        self.assertNotIn("credential_secret", path.read_text(encoding="utf-8"))

    def test_readme_covers_install_identity_profiles_and_verification(self) -> None:
        self.assertTrue(README.is_file())
        text = README.read_text(encoding="utf-8")
        for marker in (
            "mcp==2.0.0",
            "Python 3.12",
            "project.godot",
            "codex",
            "gpt-vscode",
            "deepseek",
            "codex mcp list",
            "MCP: List Servers",
            "godot_doctor",
            "BRIDGE_NOT_CONNECTED",
            "APPROVAL_PENDING",
            "production_adapter_ready: false",
        ):
            self.assertIn(marker, text)

    def test_examples_do_not_create_active_workspace_host_configuration(self) -> None:
        self.assertFalse((ROOT / ".vscode/mcp.json").exists())
        self.assertFalse((ROOT / ".codex/config.toml").exists())
        self.assertFalse((MCP_ROOT / ".vscode/mcp.json").exists())
        self.assertFalse((MCP_ROOT / ".codex/config.toml").exists())


if __name__ == "__main__":
    unittest.main()
