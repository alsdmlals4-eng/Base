from __future__ import annotations

import asyncio
import hashlib
import hmac
import json
import os
import secrets
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


ROOT = Path(__file__).resolve().parents[1]
GATEWAY_SRC = ROOT / "templates/project-operations/godot-local-mcp/gateway/src"
SECRET = "s" * 64


def _mac(payload: dict[str, Any]) -> str:
    from base_godot_mcp.framing import canonical_json_bytes

    return hmac.new(
        SECRET.encode("utf-8"),
        canonical_json_bytes(payload),
        hashlib.sha256,
    ).hexdigest()


def _signed(payload: dict[str, Any]) -> dict[str, Any]:
    return {**payload, "mac": _mac(payload)}


def _verify(frame: dict[str, Any]) -> dict[str, Any]:
    received = frame.get("mac")
    unsigned = dict(frame)
    unsigned.pop("mac", None)
    if not isinstance(received, str) or not hmac.compare_digest(received, _mac(unsigned)):
        raise AssertionError("invalid test Bridge MAC")
    return unsigned


class GodotLocalMcpAuthenticatedStdioTests(unittest.IsolatedAsyncioTestCase):
    @classmethod
    def setUpClass(cls) -> None:
        sys.path.insert(0, str(GATEWAY_SRC))

    @classmethod
    def tearDownClass(cls) -> None:
        sys.path.remove(str(GATEWAY_SRC))

    async def test_stdio_gateway_round_trips_all_bridge_backed_tools(self) -> None:
        from base_godot_mcp.framing import read_frame, write_frame
        from base_godot_mcp.project_identity import ProjectIdentity

        observed_methods: list[str] = []
        handler_errors: list[BaseException] = []

        async def handler(
            reader: asyncio.StreamReader,
            writer: asyncio.StreamWriter,
        ) -> None:
            try:
                hello = _verify(await read_frame(reader))
                client_nonce = hello["client_nonce"]
                session_id = f"session-{len(observed_methods) + 1}"
                ack = {
                    "type": "HELLO_ACK",
                    "protocol": "BASE_GODOT_BRIDGE_V1",
                    "bridge_instance_id": "bridge-e2e-1",
                    "session_id": session_id,
                    "client_nonce": client_nonce,
                    "server_nonce": secrets.token_hex(32),
                }
                await write_frame(writer, _signed(ack))

                request = _verify(await read_frame(reader))
                method = request["method"]
                payload = request["payload"]
                observed_methods.append(method)

                if method == "editor.status":
                    result = {
                        "success": True,
                        "code": "OK",
                        "data": {
                            "connected": True,
                            "active_scene_path": "res://main.tscn",
                            "dirty_state": "CLEAN",
                            "credential_secret": "must-not-leak",
                        },
                    }
                elif method == "capabilities.list":
                    result = {
                        "success": True,
                        "code": "OK",
                        "data": {
                            "capabilities": [
                                "scene.inspect",
                                "node.rename",
                                "task.status",
                                "shell.exec",
                            ]
                        },
                    }
                elif method == "scene.inspect":
                    result = {
                        "success": True,
                        "code": "OK",
                        "data": {
                            "scene_path": payload["scene_path"],
                            "node_path": payload["node_path"],
                            "node_name": "Camera",
                            "node_type": "Camera2D",
                            "child_count": 0,
                            "target_content_sha256": "b" * 64,
                        },
                    }
                elif method == "node.rename":
                    result = {
                        "success": False,
                        "code": "APPROVAL_REQUIRED",
                        "data": {
                            "operation_id": "op-e2e-rename-1",
                            "request_hash": "c" * 64,
                            "approval_token": "must-not-leak",
                        },
                    }
                elif method == "task.status":
                    result = {
                        "success": True,
                        "code": "OK",
                        "data": {
                            "operation_id": payload["operation_id"],
                            "state": "PENDING_APPROVAL",
                            "request_hash": "c" * 64,
                        },
                    }
                else:
                    raise AssertionError(f"unexpected method: {method}")

                response = {
                    "type": "RESPONSE",
                    "protocol": "BASE_GODOT_BRIDGE_V1",
                    "session_id": request["session_id"],
                    "request_id": request["request_id"],
                    "result": result,
                }
                await write_frame(writer, _signed(response))
            except BaseException as exc:
                handler_errors.append(exc)
            finally:
                writer.close()
                try:
                    await writer.wait_closed()
                except (OSError, ConnectionError):
                    pass

        server = await asyncio.start_server(handler, "127.0.0.1", 0)
        try:
            port = server.sockets[0].getsockname()[1]
            with tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                project_root = root / "project"
                config_dir = root / "config"
                project_root.mkdir()
                config_dir.mkdir()
                (project_root / "project.godot").write_text(
                    "[application]\nconfig/name=\"Authenticated Stdio Test\"\n",
                    encoding="utf-8",
                )
                identity = ProjectIdentity.from_root(project_root)

                profile_path = config_dir / "codex.json"
                profile_path.write_text(
                    json.dumps(
                        {
                            "schema_version": 1,
                            "profile_id": "codex",
                            "enabled": True,
                            "credential_secret": SECRET,
                            "allowed_project_fingerprints": [identity.fingerprint],
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
                descriptor_path = root / "bridge.json"
                descriptor_path.write_text(
                    json.dumps(
                        {
                            "schema_version": 1,
                            "protocol": "BASE_GODOT_BRIDGE_V1",
                            "host": "127.0.0.1",
                            "port": port,
                            "bridge_instance_id": "bridge-e2e-1",
                            "descriptor_nonce": "n" * 64,
                            "profile_id": "codex",
                            "project_fingerprint": identity.fingerprint,
                            "expires_at": "2099-01-01T00:00:00Z",
                        }
                    ),
                    encoding="utf-8",
                )
                if os.name == "posix":
                    profile_path.chmod(0o600)
                    descriptor_path.chmod(0o600)

                parameters = StdioServerParameters(
                    command=sys.executable,
                    args=["-m", "base_godot_mcp"],
                    env={
                        "PYTHONPATH": str(GATEWAY_SRC),
                        "PYTHONUNBUFFERED": "1",
                        "BASE_GODOT_MCP_PROFILE_ID": "codex",
                        "BASE_GODOT_MCP_CONFIG_DIR": str(config_dir),
                        "BASE_GODOT_PROJECT_ROOT": str(project_root),
                        "BASE_GODOT_MCP_BRIDGE_DESCRIPTOR": str(descriptor_path),
                    },
                    cwd=str(project_root),
                )
                async with stdio_client(parameters) as (read, write):
                    async with ClientSession(read, write) as session:
                        await session.initialize()
                        doctor = await session.call_tool("godot_doctor", arguments={})
                        status = await session.call_tool("godot_status", arguments={})
                        catalog = await session.call_tool("godot_catalog", arguments={})
                        inspect = await session.call_tool(
                            "godot_scene_inspect",
                            arguments={
                                "scene_path": "res://main.tscn",
                                "node_path": "Root/Camera",
                            },
                        )
                        rename = await session.call_tool(
                            "godot_node_rename",
                            arguments={
                                "scene_path": "res://main.tscn",
                                "node_path": "Root/Camera",
                                "new_name": "GameplayCamera",
                                "save_mode": "KEEP_DIRTY",
                            },
                        )
                        task = await session.call_tool(
                            "godot_task_status",
                            arguments={"operation_id": "op-e2e-rename-1"},
                        )
        finally:
            server.close()
            await server.wait_closed()

        self.assertEqual(handler_errors, [])
        self.assertEqual(
            observed_methods,
            [
                "editor.status",
                "capabilities.list",
                "scene.inspect",
                "node.rename",
                "task.status",
            ],
        )
        self.assertEqual(doctor.structured_content["code"], "OK")
        self.assertTrue(status.structured_content["data"]["connected"])
        self.assertNotIn("must-not-leak", str(status))
        self.assertEqual(
            catalog.structured_content["data"]["capabilities"],
            ["node.rename", "scene.inspect", "task.status"],
        )
        self.assertEqual(inspect.structured_content["data"]["node_type"], "Camera2D")
        self.assertEqual(rename.structured_content["code"], "APPROVAL_PENDING")
        self.assertNotIn("approval_token", str(rename))
        self.assertEqual(task.structured_content["data"]["state"], "PENDING_APPROVAL")


if __name__ == "__main__":
    unittest.main()
