from __future__ import annotations

from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from loop_a2_local_executor.cli import build_parser


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


if __name__ == "__main__":
    unittest.main()
