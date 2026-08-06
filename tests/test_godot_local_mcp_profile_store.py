from __future__ import annotations

import json
import os
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GATEWAY_SRC = ROOT / "templates/project-operations/godot-local-mcp/gateway/src"


class GodotLocalMcpProfileStoreTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        sys.path.insert(0, str(GATEWAY_SRC))

    @classmethod
    def tearDownClass(cls) -> None:
        sys.path.remove(str(GATEWAY_SRC))

    def _write_profile(
        self,
        directory: Path,
        *,
        profile_id: str = "codex",
        enabled: bool = True,
        expires_at: str | None = "2099-01-01T00:00:00Z",
        mode: int = 0o600,
    ) -> tuple[Path, str]:
        secret = "s" * 64
        payload = {
            "schema_version": 1,
            "profile_id": profile_id,
            "enabled": enabled,
            "credential_secret": secret,
            "allowed_project_fingerprints": ["f" * 64],
            "allowed_capabilities": [
                "editor.status",
                "capabilities.list",
                "scene.inspect",
                "node.rename",
                "task.status",
            ],
            "expires_at": expires_at,
        }
        directory.mkdir(parents=True, exist_ok=True)
        path = directory / f"{profile_id}.json"
        path.write_text(json.dumps(payload), encoding="utf-8")
        if os.name == "posix":
            path.chmod(mode)
        return path, secret

    def test_codex_profile_loads_without_exposing_secret(self) -> None:
        from base_godot_mcp.profile_store import load_profile

        with tempfile.TemporaryDirectory() as temporary:
            config_dir = Path(temporary)
            _, secret = self._write_profile(config_dir)
            profile = load_profile(
                "codex",
                config_dir=config_dir,
                now=datetime(2026, 8, 6, tzinfo=timezone.utc),
            )

        self.assertEqual(profile.profile_id, "codex")
        self.assertNotIn(secret, repr(profile))
        self.assertEqual(profile.credential_secret, secret)

    def test_gpt_vscode_profile_loads(self) -> None:
        from base_godot_mcp.profile_store import load_profile

        with tempfile.TemporaryDirectory() as temporary:
            config_dir = Path(temporary)
            self._write_profile(config_dir, profile_id="gpt-vscode")
            profile = load_profile(
                "gpt-vscode",
                config_dir=config_dir,
                now=datetime(2026, 8, 6, tzinfo=timezone.utc),
            )

        self.assertEqual(profile.profile_id, "gpt-vscode")

    def test_deepseek_is_denied_before_profile_file_lookup(self) -> None:
        from base_godot_mcp.profile_store import ProfileError, load_profile

        with tempfile.TemporaryDirectory() as temporary:
            with self.assertRaisesRegex(ProfileError, "MCP_CLIENT_PROFILE_DENIED"):
                load_profile(
                    "deepseek",
                    config_dir=Path(temporary) / "missing",
                    now=datetime(2026, 8, 6, tzinfo=timezone.utc),
                )

    def test_disabled_profile_is_denied(self) -> None:
        from base_godot_mcp.profile_store import ProfileError, load_profile

        with tempfile.TemporaryDirectory() as temporary:
            config_dir = Path(temporary)
            self._write_profile(config_dir, enabled=False)
            with self.assertRaisesRegex(ProfileError, "MCP_CLIENT_PROFILE_DISABLED"):
                load_profile(
                    "codex",
                    config_dir=config_dir,
                    now=datetime(2026, 8, 6, tzinfo=timezone.utc),
                )

    def test_expired_profile_is_denied(self) -> None:
        from base_godot_mcp.profile_store import ProfileError, load_profile

        with tempfile.TemporaryDirectory() as temporary:
            config_dir = Path(temporary)
            self._write_profile(config_dir, expires_at="2026-08-05T00:00:00Z")
            with self.assertRaisesRegex(ProfileError, "MCP_CLIENT_PROFILE_EXPIRED"):
                load_profile(
                    "codex",
                    config_dir=config_dir,
                    now=datetime(2026, 8, 6, tzinfo=timezone.utc),
                )

    @unittest.skipUnless(os.name == "posix", "POSIX permission contract")
    def test_group_or_world_readable_profile_is_denied(self) -> None:
        from base_godot_mcp.profile_store import ProfileError, load_profile

        with tempfile.TemporaryDirectory() as temporary:
            config_dir = Path(temporary)
            self._write_profile(config_dir, mode=0o644)
            with self.assertRaisesRegex(
                ProfileError,
                "MCP_CLIENT_PROFILE_PERMISSION_INVALID",
            ):
                load_profile(
                    "codex",
                    config_dir=config_dir,
                    now=datetime(2026, 8, 6, tzinfo=timezone.utc),
                )


if __name__ == "__main__":
    unittest.main()
