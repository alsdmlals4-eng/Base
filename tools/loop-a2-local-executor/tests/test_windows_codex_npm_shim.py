from __future__ import annotations

import os
from pathlib import Path
import tempfile
import unittest

from tools.loop_a2_runtime.codex_cli_transport import CodexCliProcess, CodexCliTransportError
from tools.loop_a2_runtime.provider_gate import subscription_codex_cli_gate


@unittest.skipUnless(os.name == "nt", "Windows npm shim execution contract")
class WindowsCodexNpmShimTests(unittest.TestCase):
    def _with_shim_environment(self, root: Path) -> tuple[Path, dict[str, str | None]]:
        roaming = root / "AppData" / "Roaming"
        npm = roaming / "npm"
        npm.mkdir(parents=True)
        shim = npm / "codex.cmd"
        shim.write_text(
            "@echo off\r\n"
            "if /I \"%~1\"==\"login\" if /I \"%~2\"==\"status\" (\r\n"
            "  echo Logged in using ChatGPT\r\n"
            "  exit /b 0\r\n"
            ")\r\n"
            "set \"OUTPUT=\"\r\n"
            ":scan\r\n"
            "if \"%~1\"==\"\" goto done\r\n"
            "if /I \"%~1\"==\"--output-last-message\" (\r\n"
            "  shift\r\n"
            "  set \"OUTPUT=%~1\"\r\n"
            ")\r\n"
            "shift\r\n"
            "goto scan\r\n"
            ":done\r\n"
            "if not defined OUTPUT exit /b 7\r\n"
            ">\"%OUTPUT%\" echo {\"ok\":true}\r\n"
            "exit /b 0\r\n",
            encoding="utf-8",
        )
        old = {
            "APPDATA": os.environ.get("APPDATA"),
            "PATH": os.environ.get("PATH"),
        }
        os.environ["APPDATA"] = str(roaming)
        os.environ["PATH"] = str(npm) + os.pathsep + (old["PATH"] or "")
        return shim, old

    def _restore_environment(self, old: dict[str, str | None]) -> None:
        for key, value in old.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value

    def test_subscription_gate_uses_windows_npm_codex_cmd(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            _, old = self._with_shim_environment(Path(temp))
            try:
                result = subscription_codex_cli_gate()
            finally:
                self._restore_environment(old)
        self.assertEqual(result["status"], "READY")
        self.assertEqual(result["code"], "CODEX_CHATGPT_AUTH_READY")

    def test_codex_exec_uses_same_windows_npm_codex_cmd(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            _, old = self._with_shim_environment(Path(temp))
            try:
                try:
                    output = CodexCliProcess().invoke(
                        instructions="Return the required object.",
                        input_text="{}",
                        schema={
                            "type": "object",
                            "properties": {"ok": {"type": "boolean"}},
                            "required": ["ok"],
                            "additionalProperties": False,
                        },
                        timeout_seconds=10,
                    )
                except CodexCliTransportError as exc:
                    self.fail(f"Windows npm codex.cmd must execute through the REAL transport: {exc.code}")
            finally:
                self._restore_environment(old)
        self.assertEqual(output.strip(), '{"ok":true}')


if __name__ == "__main__":
    unittest.main()
