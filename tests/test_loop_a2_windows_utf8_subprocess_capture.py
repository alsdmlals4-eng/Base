from __future__ import annotations

import json
from pathlib import Path
import subprocess
import unittest

from tools.loop_a2_runtime.codex_cli_transport import CodexCliProcess
from tools.loop_a2_runtime.provider_gate import subscription_codex_cli_gate


class RecordingRunner:
    def __init__(self, responses: list[subprocess.CompletedProcess[str]]) -> None:
        self.responses = list(responses)
        self.calls: list[tuple[tuple[str, ...], dict[str, object]]] = []

    def __call__(self, argv, **kwargs):
        self.calls.append((tuple(str(item) for item in argv), dict(kwargs)))
        return self.responses.pop(0)


class CodexExecRunner:
    def __init__(self) -> None:
        self.calls: list[tuple[tuple[str, ...], dict[str, object]]] = []

    def __call__(self, argv, **kwargs):
        argv = tuple(str(item) for item in argv)
        self.calls.append((argv, dict(kwargs)))
        output_path = Path(argv[argv.index("--output-last-message") + 1])
        output_path.write_text(json.dumps({"status": "COMPLETED"}), encoding="utf-8")
        return subprocess.CompletedProcess(argv, 0, stdout="", stderr="")


class WindowsUtf8SubprocessCaptureTests(unittest.TestCase):
    def test_subscription_login_capture_is_explicit_utf8_replace(self) -> None:
        runner = RecordingRunner([
            subprocess.CompletedProcess([], 0, stdout="Logged in using ChatGPT\n", stderr=""),
        ])

        result = subscription_codex_cli_gate(run_command=runner)

        self.assertEqual(result["status"], "READY")
        kwargs = runner.calls[0][1]
        self.assertIs(kwargs["text"], True)
        self.assertEqual(kwargs["encoding"], "utf-8")
        self.assertEqual(kwargs["errors"], "replace")
        self.assertIs(kwargs["shell"], False)

    def test_codex_exec_capture_is_explicit_utf8_replace(self) -> None:
        runner = CodexExecRunner()

        CodexCliProcess(run_command=runner).invoke(
            instructions="Return bounded JSON only.",
            input_text="{}",
            schema={"type": "object"},
            timeout_seconds=30,
        )

        kwargs = runner.calls[0][1]
        self.assertIs(kwargs["text"], True)
        self.assertEqual(kwargs["encoding"], "utf-8")
        self.assertEqual(kwargs["errors"], "replace")
        self.assertIs(kwargs["shell"], False)


if __name__ == "__main__":
    unittest.main()
