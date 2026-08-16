from __future__ import annotations

from pathlib import Path
import subprocess
import sys
import unittest


PACKAGE_ROOT = Path(__file__).resolve().parents[1]
SRC = PACKAGE_ROOT / "src"
sys.path.insert(0, str(SRC))

from loop_a2_local_executor.runtime import LocalA2Runtime


INSTALLER = PACKAGE_ROOT / "windows" / "Base_Loop_A2_Local_Executor_Installer_v4.cmd"


class CaptureRunner:
    def __init__(self) -> None:
        self.calls: list[dict[str, object]] = []

    def __call__(self, argv, **kwargs):
        self.calls.append({"argv": tuple(argv), **kwargs})
        return subprocess.CompletedProcess(
            list(argv),
            0,
            stdout="sha256:" + "e" * 64 + "\n",
            stderr="",
        )


class WindowsUtf8PreflightRetryTests(unittest.TestCase):
    def test_runtime_capture_is_explicit_utf8_and_decode_errors_are_bounded(self) -> None:
        runner = CaptureRunner()
        runtime = LocalA2Runtime(
            store=object(),
            runner=runner,
            python_executable="trusted-python",
            docker_executable="trusted-docker",
        )

        result = runtime.preflight()

        self.assertEqual(result["status"], "READY")
        self.assertEqual(len(runner.calls), 1)
        call = runner.calls[0]
        self.assertEqual(call.get("encoding"), "utf-8")
        self.assertEqual(call.get("errors"), "replace")
        self.assertTrue(call.get("text"))
        self.assertTrue(call.get("capture_output"))
        self.assertFalse(call.get("shell"))

    def test_installer_runs_shared_preflight_twice_without_reentering_batch_label(self) -> None:
        text = INSTALLER.read_text(encoding="utf-8")
        preflight_command = (
            '"!VENV!\\Scripts\\loop-a2-local-executor.exe" '
            '--state-root "!STATE_ROOT!" preflight >"!PREFLIGHT_FILE!" 2>&1'
        )

        self.assertNotIn("call :capture_preflight", text)
        self.assertNotIn("\n:capture_preflight\n", text)
        self.assertEqual(text.count(preflight_command), 2)
        self.assertGreaterEqual(text.count('type "!PREFLIGHT_FILE!" >>"!LOG!"'), 2)
        self.assertGreaterEqual(text.count('type "!PREFLIGHT_FILE!"'), 4)

        first = text.index("[7/8] Executor shared preflight")
        pull = text.index('"!DOCKER_CMD!" pull "!IMAGE_REF!"')
        second = text.index("Executor shared preflight after exact image pull")
        self.assertLess(first, pull)
        self.assertLess(pull, second)


if __name__ == "__main__":
    unittest.main()
