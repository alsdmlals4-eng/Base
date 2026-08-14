from __future__ import annotations

from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

import loop_a2_local_executor.cli as cli
from loop_a2_local_executor.cli import build_parser


class _FakeService:
    def __init__(self) -> None:
        self.preflights = 0
        self.once_calls = 0

    def preflight(self):
        self.preflights += 1
        return {"status": "READY", "code": "GH_CONTROL_PLANE_READY"}

    def once(self):
        self.once_calls += 1
        return {"status": "IDLE", "code": "NO_ELIGIBLE_JOB"}


class _RecordingLock:
    def __init__(self, path: Path, entered: list[Path]) -> None:
        self.path = Path(path)
        self.entered = entered

    def __enter__(self):
        self.entered.append(self.path)
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


class EntrypointTests(unittest.TestCase):
    def test_cli_has_preflight_once_and_bounded_daemon_modes(self) -> None:
        parser = build_parser()
        self.assertEqual(parser.parse_args(["preflight"]).command, "preflight")
        self.assertEqual(parser.parse_args(["once"]).command, "once")
        daemon = parser.parse_args(["daemon", "--poll-seconds", "15"])
        self.assertEqual(daemon.command, "daemon")
        self.assertEqual(daemon.poll_seconds, 15)
        with self.assertRaises(SystemExit):
            parser.parse_args(["daemon", "--poll-seconds", "14"])

    def test_windows_entrypoint_exists_and_contains_no_powershell_or_shell_true(self) -> None:
        entry = SRC / "loop_a2_local_executor" / "windows_entry.pyw"
        self.assertTrue(entry.is_file())
        text = entry.read_text(encoding="utf-8")
        self.assertIn("from loop_a2_local_executor.cli import main", text)
        self.assertNotIn("powershell", text.casefold())
        self.assertNotIn("shell=True", text.replace(" ", ""))

    def test_package_installs_named_console_command(self) -> None:
        pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
        self.assertIn('[project.scripts]', pyproject)
        self.assertIn('loop-a2-local-executor = "loop_a2_local_executor.cli:main"', pyproject)

    def test_once_and_daemon_lock_then_preflight_before_processing(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            state_root = Path(temp).resolve()
            for command in (("once",), ("daemon", "--poll-seconds", "15")):
                with self.subTest(command=command):
                    entered: list[Path] = []
                    service = _FakeService()
                    lock_factory = lambda path: _RecordingLock(path, entered)
                    with (
                        patch.object(cli, "InstanceLock", side_effect=lock_factory),
                        patch.object(cli, "build_service", return_value=service),
                        patch.object(cli.time, "sleep", side_effect=KeyboardInterrupt),
                    ):
                        result = cli.main(["--state-root", str(state_root), *command])
                    self.assertEqual(result, 0)
                    self.assertEqual(entered, [state_root / "executor.lock"])
                    self.assertEqual(service.preflights, 1)
                    self.assertEqual(service.once_calls, 1)


if __name__ == "__main__":
    unittest.main()
