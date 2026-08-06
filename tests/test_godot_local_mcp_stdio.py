from __future__ import annotations

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


ROOT = Path(__file__).resolve().parents[1]
GATEWAY_ROOT = ROOT / "templates/project-operations/godot-local-mcp/gateway"
GATEWAY_SRC = GATEWAY_ROOT / "src"
EXPECTED_TOOLS = {
    "godot_doctor",
    "godot_status",
    "godot_catalog",
    "godot_scene_inspect",
    "godot_node_rename",
    "godot_task_status",
}


class GodotLocalMcpStdioTests(unittest.IsolatedAsyncioTestCase):
    def _write_profile(self, config_dir: Path, fingerprint: str) -> None:
        config_dir.mkdir(parents=True, exist_ok=True)
        path = config_dir / "codex.json"
        path.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "profile_id": "codex",
                    "enabled": True,
                    "credential_secret": "s" * 64,
                    "allowed_project_fingerprints": [fingerprint],
                    "allowed_capabilities": [
                        "editor.status",
                        "capabilities.list",
                        "scene.inspect",
                        "node.rename",
                        "task.status",
                    ],
                    "expires_at": "2099-01-01T00:00:00Z",
                }
            ),
            encoding="utf-8",
        )
        if os.name == "posix":
            path.chmod(0o600)

    async def test_real_stdio_process_initializes_and_lists_exact_tools(self) -> None:
        self.assertTrue((GATEWAY_SRC / "base_godot_mcp/__main__.py").is_file())
        self.assertTrue((GATEWAY_ROOT / "pyproject.toml").is_file())

        sys.path.insert(0, str(GATEWAY_SRC))
        self.addCleanup(lambda: sys.path.remove(str(GATEWAY_SRC)))
        from base_godot_mcp.project_identity import ProjectIdentity

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            project_root = root / "project"
            config_dir = root / "config"
            project_root.mkdir()
            (project_root / "project.godot").write_text(
                "[application]\nconfig/name=\"Stdio Test\"\n",
                encoding="utf-8",
            )
            identity = ProjectIdentity.from_root(project_root)
            self._write_profile(config_dir, identity.fingerprint)

            environment = {
                "PYTHONPATH": str(GATEWAY_SRC),
                "BASE_GODOT_MCP_PROFILE_ID": "codex",
                "BASE_GODOT_MCP_CONFIG_DIR": str(config_dir),
                "BASE_GODOT_PROJECT_ROOT": str(project_root),
                "PYTHONUNBUFFERED": "1",
            }
            parameters = StdioServerParameters(
                command=sys.executable,
                args=["-m", "base_godot_mcp"],
                env=environment,
                cwd=str(project_root),
            )
            async with stdio_client(parameters) as (read, write):
                async with ClientSession(read, write) as session:
                    await session.initialize()
                    tools = await session.list_tools()
                    doctor = await session.call_tool("godot_doctor", arguments={})
                    status = await session.call_tool("godot_status", arguments={})

        self.assertEqual({tool.name for tool in tools.tools}, EXPECTED_TOOLS)
        self.assertEqual(doctor.structured_content["code"], "OK")
        self.assertEqual(
            doctor.structured_content["data"]["project_fingerprint"],
            identity.fingerprint,
        )
        self.assertNotIn(str(project_root), str(doctor))
        self.assertEqual(status.structured_content["data"]["connected"], False)

    def test_project_metadata_pins_python_and_mcp_sdk(self) -> None:
        metadata = (GATEWAY_ROOT / "pyproject.toml").read_text(encoding="utf-8")
        self.assertIn('requires-python = "==3.12.*"', metadata)
        self.assertIn('"mcp==2.0.0"', metadata)
        self.assertIn('base-godot-mcp = "base_godot_mcp.__main__:main"', metadata)


if __name__ == "__main__":
    unittest.main()
