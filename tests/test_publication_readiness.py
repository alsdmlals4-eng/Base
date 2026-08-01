from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import time
import unittest
from dataclasses import replace
from pathlib import Path
from unittest import mock

from tools import publication_readiness as readiness


ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "tools/check_publication_environment.py"


@unittest.skipIf(os.name == "nt", "POSIX executable fixtures are exercised on Ubuntu")
class PublicationReadinessTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.counter = 0
        self.regular = self.root / "regular.ttf"
        self.bold = self.root / "bold.ttf"
        self.regular.write_bytes(b"regular-font-fixture")
        self.bold.write_bytes(b"bold-font-fixture")
        self.working_libreoffice = self.executable(
            """import pathlib
import sys

arguments = sys.argv[1:]
output_directory = pathlib.Path(arguments[arguments.index("--outdir") + 1])
source = pathlib.Path(arguments[-1])
(output_directory / f"{source.stem}.pdf").write_bytes(b"%PDF-1.4\\n%%EOF\\n")
"""
        )
        self.working_pdftoppm = self.executable(
            """import sys

print("pdftoppm version fixture", file=sys.stderr)
"""
        )

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def executable(self, body: str) -> str:
        self.counter += 1
        path = self.root / f"tool-{self.counter}"
        path.write_text(f"#!{sys.executable}\n{body}", encoding="utf-8")
        path.chmod(0o755)
        return str(path)

    def working_tools(self) -> readiness.PublicationTools:
        return readiness.PublicationTools(
            libreoffice=self.working_libreoffice,
            pdftoppm=self.working_pdftoppm,
            mermaid_cli=None,
            chrome=None,
            node=None,
            pnpm=None,
            font_regular=str(self.regular),
            font_bold=str(self.bold),
        )

    def test_existing_libreoffice_wrapper_without_pdf_is_not_ready(self) -> None:
        broken = self.executable("raise SystemExit(0)\n")
        report = readiness.probe_publication_readiness(
            replace(self.working_tools(), libreoffice=broken)
        )

        self.assertFalse(report.ready)
        self.assertIn("libreoffice", report.probe_failures)
        self.assertIn("valid PDF", report.probe_failures["libreoffice"])

    def test_existing_poppler_wrapper_that_fails_is_not_ready(self) -> None:
        broken = self.executable("raise SystemExit(9)\n")
        report = readiness.probe_publication_readiness(
            replace(self.working_tools(), pdftoppm=broken)
        )

        self.assertFalse(report.ready)
        self.assertIn("pdftoppm", report.probe_failures)

    def test_version_probe_times_out_and_fails_closed(self) -> None:
        slow = self.executable("import time\ntime.sleep(5)\n")

        version, error = readiness._command_version(
            slow,
            ["--version"],
            timeout=1,
        )

        self.assertIsNone(version)
        self.assertIn("timed out", error or "")

    def test_timeout_is_bounded_when_a_descendant_inherits_probe_pipes(self) -> None:
        descendant = self.executable(
            """import subprocess
import sys

subprocess.Popen([sys.executable, "-c", "import time; time.sleep(4)"])
"""
        )

        started = time.monotonic()
        version, error = readiness._command_version(
            descendant,
            ["--version"],
            timeout=1,
        )
        elapsed = time.monotonic() - started

        self.assertIsNone(version)
        self.assertIn("timed out", error or "")
        self.assertLess(elapsed, 3.0)

    def test_missing_regular_or_bold_font_is_not_ready(self) -> None:
        for missing_name in ("font_regular", "font_bold"):
            with self.subTest(missing_name=missing_name):
                report = readiness.probe_publication_readiness(
                    replace(self.working_tools(), **{missing_name: None})
                )

                self.assertFalse(report.ready)
                self.assertIn(missing_name, report.missing)

    def test_working_basic_tools_and_both_fonts_are_ready(self) -> None:
        report = readiness.probe_publication_readiness(self.working_tools())

        self.assertTrue(report.ready, report.skip_reason)
        self.assertEqual((), report.missing)
        self.assertEqual({}, report.probe_failures)

    def test_mermaid_readiness_does_not_launch_the_chrome_gui_directly(self) -> None:
        chrome = self.root / "chrome-gui-fixture"
        chrome.write_bytes(b"path-only Chrome fixture")
        version_tool = self.executable('print("tool version fixture")\n')
        report = readiness.probe_publication_readiness(
            replace(
                self.working_tools(),
                mermaid_cli=version_tool,
                chrome=str(chrome),
                node=version_tool,
                pnpm=version_tool,
            ),
            require_mermaid=True,
        )

        self.assertTrue(report.ready, report.skip_reason)
        self.assertIsNone(report.versions["chrome"])

    def test_cached_readiness_rechecks_changed_environment_overrides(self) -> None:
        environment = {
            "BASE_LIBREOFFICE": self.working_libreoffice,
            "BASE_PDFTOPPM": self.working_pdftoppm,
            "BASE_FONT_REGULAR": str(self.regular),
            "BASE_FONT_BOLD": str(self.bold),
        }
        with mock.patch.dict(os.environ, environment, clear=False):
            ready = readiness.publication_readiness(self.root)
            replacement_bold = self.root / "replacement-bold.ttf"
            os.environ["BASE_FONT_BOLD"] = str(replacement_bold)
            broken = readiness.publication_readiness(self.root)
            replacement_bold.write_bytes(b"replacement-bold-font-fixture")
            repaired = readiness.publication_readiness(self.root)

        self.assertTrue(ready.ready, ready.skip_reason)
        self.assertFalse(broken.ready)
        self.assertIn("font_bold", broken.missing)
        self.assertTrue(repaired.ready, repaired.skip_reason)

    def test_preflight_cli_requires_the_configured_bold_font(self) -> None:
        missing_bold = self.root / "missing-bold.ttf"
        environment = dict(os.environ)
        environment.update(
            {
                "BASE_LIBREOFFICE": self.working_libreoffice,
                "BASE_PDFTOPPM": self.working_pdftoppm,
                "BASE_FONT_REGULAR": str(self.regular),
                "BASE_FONT_BOLD": str(missing_bold),
            }
        )

        result = subprocess.run(
            [sys.executable, str(CHECKER)],
            cwd=ROOT,
            env=environment,
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=False,
        )

        self.assertNotEqual(0, result.returncode)
        report = json.loads(result.stdout)
        self.assertIn("font_bold", report["missing"])
        self.assertFalse(report["ready"])


class PublicationWrapperCommandTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def test_windows_wrapper_command_uses_the_existing_safe_runner(self) -> None:
        wrapper = self.root / "pdftoppm.cmd"
        wrapper.write_text("@exit /b 0\n", encoding="utf-8")
        command_processor = str(self.root / "cmd.exe")

        with mock.patch.dict(os.environ, {"COMSPEC": command_processor}):
            command = readiness._probe_command(str(wrapper), ["-v"])

        self.assertEqual(
            [
                command_processor,
                "/d",
                "/s",
                "/c",
                "call",
                str(wrapper.resolve()),
                "-v",
            ],
            command,
        )

    def test_windows_wrapper_metacharacters_become_a_probe_failure(self) -> None:
        wrapper = self.root / "pdftoppm.cmd"
        wrapper.write_text("@exit /b 0\n", encoding="utf-8")

        version, error = readiness._command_version(
            str(wrapper),
            ["-v & whoami"],
            timeout=1,
        )

        self.assertIsNone(version)
        self.assertIn("metacharacters", error or "")


@unittest.skipUnless(os.name == "nt", "real command-wrapper execution requires Windows")
class WindowsPublicationWrapperExecutionTests(unittest.TestCase):
    def test_real_cmd_wrapper_version_probe_succeeds(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            wrapper = Path(temporary) / "pdftoppm.cmd"
            wrapper.write_text(
                "@echo pdftoppm Windows wrapper fixture 1>&2\r\n@exit /b 0\r\n",
                encoding="utf-8",
            )

            version, error = readiness._command_version(
                str(wrapper),
                ["-v"],
                timeout=5,
            )

        self.assertIsNone(error)
        self.assertIn("Windows wrapper fixture", version or "")


if __name__ == "__main__":
    unittest.main()
