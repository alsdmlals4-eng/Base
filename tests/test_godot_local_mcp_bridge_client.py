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
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
GATEWAY_SRC = ROOT / "templates/project-operations/godot-local-mcp/gateway/src"


def _mac(secret: str, payload: dict[str, Any]) -> str:
    from base_godot_mcp.framing import canonical_json_bytes

    return hmac.new(
        secret.encode("utf-8"),
        canonical_json_bytes(payload),
        hashlib.sha256,
    ).hexdigest()


class GodotLocalMcpBridgeClientTests(unittest.IsolatedAsyncioTestCase):
    @classmethod
    def setUpClass(cls) -> None:
        sys.path.insert(0, str(GATEWAY_SRC))

    @classmethod
    def tearDownClass(cls) -> None:
        sys.path.remove(str(GATEWAY_SRC))

    def _identity_and_profile(self, root: Path):
        from base_godot_mcp.profile_store import ClientProfile
        from base_godot_mcp.project_identity import ProjectIdentity

        project_root = root / "project"
        project_root.mkdir()
        (project_root / "project.godot").write_text(
            "[application]\nconfig/name=\"Bridge Test\"\n",
            encoding="utf-8",
        )
        project = ProjectIdentity.from_root(project_root)
        profile = ClientProfile(
            profile_id="codex",
            enabled=True,
            allowed_project_fingerprints=(project.fingerprint,),
            allowed_capabilities=("editor.status",),
            credential_secret="s" * 64,
        )
        return project, profile

    def _write_descriptor(
        self,
        path: Path,
        *,
        port: int,
        project_fingerprint: str,
        host: str = "127.0.0.1",
        profile_id: str = "codex",
        expires_at: str = "2099-01-01T00:00:00Z",
    ) -> None:
        path.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "protocol": "BASE_GODOT_BRIDGE_V1",
                    "host": host,
                    "port": port,
                    "bridge_instance_id": "bridge-test-1",
                    "descriptor_nonce": "n" * 64,
                    "profile_id": profile_id,
                    "project_fingerprint": project_fingerprint,
                    "expires_at": expires_at,
                }
            ),
            encoding="utf-8",
        )
        if os.name == "posix":
            path.chmod(0o600)

    async def test_authenticated_request_round_trip(self) -> None:
        from base_godot_mcp.bridge_client import AuthenticatedBridge
        from base_godot_mcp.bridge_descriptor import load_bridge_descriptor
        from base_godot_mcp.framing import read_frame, write_frame

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            project, profile = self._identity_and_profile(root)
            observed: list[dict[str, Any]] = []

            async def handler(
                reader: asyncio.StreamReader,
                writer: asyncio.StreamWriter,
            ) -> None:
                try:
                    hello = await read_frame(reader)
                    hello_mac = hello.pop("mac")
                    self.assertTrue(hmac.compare_digest(hello_mac, _mac(profile.credential_secret, hello)))
                    self.assertEqual(hello["project_fingerprint"], project.fingerprint)
                    ack = {
                        "type": "HELLO_ACK",
                        "protocol": "BASE_GODOT_BRIDGE_V1",
                        "bridge_instance_id": "bridge-test-1",
                        "session_id": "session-test-1",
                        "client_nonce": hello["client_nonce"],
                        "server_nonce": secrets.token_hex(32),
                    }
                    await write_frame(writer, {**ack, "mac": _mac(profile.credential_secret, ack)})

                    request = await read_frame(reader)
                    request_mac = request.pop("mac")
                    self.assertTrue(hmac.compare_digest(request_mac, _mac(profile.credential_secret, request)))
                    observed.append(request)
                    response = {
                        "type": "RESPONSE",
                        "protocol": "BASE_GODOT_BRIDGE_V1",
                        "session_id": "session-test-1",
                        "request_id": request["request_id"],
                        "result": {
                            "success": True,
                            "code": "OK",
                            "data": {
                                "connected": True,
                                "active_scene_path": "res://main.tscn",
                                "dirty_state": "CLEAN",
                            },
                        },
                    }
                    await write_frame(
                        writer,
                        {**response, "mac": _mac(profile.credential_secret, response)},
                    )
                finally:
                    writer.close()
                    await writer.wait_closed()

            server = await asyncio.start_server(handler, "127.0.0.1", 0)
            try:
                port = server.sockets[0].getsockname()[1]
                descriptor_path = root / "bridge.json"
                self._write_descriptor(
                    descriptor_path,
                    port=port,
                    project_fingerprint=project.fingerprint,
                )
                descriptor = load_bridge_descriptor(
                    descriptor_path,
                    profile=profile,
                    project=project,
                    now=datetime(2026, 8, 6, tzinfo=timezone.utc),
                )
                bridge = AuthenticatedBridge(
                    profile=profile,
                    project=project,
                    descriptor=descriptor,
                    timeout_seconds=2,
                )
                result = await bridge.request("editor.status", {"probe": True})
            finally:
                server.close()
                await server.wait_closed()

        self.assertEqual(result["code"], "OK")
        self.assertEqual(observed[0]["method"], "editor.status")
        self.assertEqual(observed[0]["payload"], {"probe": True})

    def test_descriptor_denies_non_loopback_expiry_and_identity_mismatch(self) -> None:
        from base_godot_mcp.bridge_descriptor import BridgeDescriptorError, load_bridge_descriptor

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            project, profile = self._identity_and_profile(root)
            path = root / "bridge.json"

            cases = [
                {"host": "0.0.0.0"},
                {"expires_at": "2026-08-05T00:00:00Z"},
                {"profile_id": "gpt-vscode"},
                {"project_fingerprint": "0" * 64},
            ]
            for overrides in cases:
                values = {
                    "port": 43567,
                    "project_fingerprint": project.fingerprint,
                    **overrides,
                }
                self._write_descriptor(path, **values)
                with self.assertRaises(BridgeDescriptorError):
                    load_bridge_descriptor(
                        path,
                        profile=profile,
                        project=project,
                        now=datetime(2026, 8, 6, tzinfo=timezone.utc),
                    )

    @unittest.skipUnless(os.name == "posix", "POSIX permission contract")
    def test_descriptor_must_be_owner_private(self) -> None:
        from base_godot_mcp.bridge_descriptor import BridgeDescriptorError, load_bridge_descriptor

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            project, profile = self._identity_and_profile(root)
            path = root / "bridge.json"
            self._write_descriptor(
                path,
                port=43567,
                project_fingerprint=project.fingerprint,
            )
            path.chmod(0o644)
            with self.assertRaisesRegex(
                BridgeDescriptorError,
                "BRIDGE_DESCRIPTOR_PERMISSION_INVALID",
            ):
                load_bridge_descriptor(
                    path,
                    profile=profile,
                    project=project,
                    now=datetime(2026, 8, 6, tzinfo=timezone.utc),
                )


if __name__ == "__main__":
    unittest.main()
