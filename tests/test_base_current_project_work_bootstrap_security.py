from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

from tests.test_base_current_project_work_bootstrap import (
    _active_receipt,
    _git,
    _init_project,
    _run,
)


ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools/run_project_work_gate.py"
REQUIRED_BASE_FILES = (
    "tools/run_project_work_gate.py",
    "tools/validate_work_contract_receipt.py",
    "tools/project_work_tracking.py",
)


class BaseCurrentProjectWorkBootstrapSecurityTests(unittest.TestCase):
    def test_receipt_path_must_be_a_regular_file(self) -> None:
        if not hasattr(os, "mkfifo"):
            self.skipTest("named pipes are unavailable on this platform")

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            project = root / "project"
            source = _init_project(project)
            fifo = root / "receipt.pipe"
            os.mkfifo(fifo)
            payload = json.dumps(_active_receipt(source))
            writer = subprocess.Popen(
                [
                    sys.executable,
                    "-c",
                    "from pathlib import Path; "
                    f"Path({str(fifo)!r}).open('w', encoding='utf-8').write({payload!r})",
                ],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            try:
                result = _run(
                    sys.executable,
                    "-I",
                    str(TOOL),
                    "--expected-base-sha",
                    _git(ROOT, "rev-parse", "HEAD"),
                    "--project-root",
                    str(project),
                    "--project-source-sha",
                    source,
                    "--receipt",
                    str(fifo),
                    "--phase",
                    "start",
                )
            finally:
                if writer.poll() is None:
                    writer.terminate()
                try:
                    writer.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    writer.kill()
                    writer.wait(timeout=5)

            self.assertNotEqual(0, result.returncode, result.stdout + result.stderr)
            self.assertIn("regular file", result.stdout)

    def test_git_replace_cannot_substitute_the_trusted_base_commit(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            base = root / "base"
            project = root / "project"
            base.mkdir()
            for relative in REQUIRED_BASE_FILES:
                destination = base / relative
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(ROOT / relative, destination)

            for args in (
                ("init", "-q"),
                ("config", "user.email", "bootstrap-security@example.invalid"),
                ("config", "user.name", "bootstrap security"),
                ("add", "tools"),
                ("commit", "-qm", "trusted Base snapshot"),
            ):
                _git(base, *args)
            trusted = _git(base, "rev-parse", "HEAD")

            _git(base, "checkout", "-qb", "replacement")
            replacement_tool = base / "tools/run_project_work_gate.py"
            replacement_tool.write_text(
                replacement_tool.read_text(encoding="utf-8")
                + "\n# replacement-object attack fixture\n",
                encoding="utf-8",
            )
            _git(base, "add", "tools/run_project_work_gate.py")
            _git(base, "commit", "-qm", "replacement snapshot")
            replacement = _git(base, "rev-parse", "HEAD")
            replacement_bytes = subprocess.check_output(
                ["git", "-C", str(base), "show", f"{replacement}:tools/run_project_work_gate.py"]
            )

            _git(base, "checkout", "-q", "--detach", trusted)
            _git(base, "replace", trusted, replacement)
            replacement_tool.write_bytes(replacement_bytes)

            source = _init_project(project)
            receipt = root / "receipt.json"
            receipt.write_text(json.dumps(_active_receipt(source)), encoding="utf-8")
            result = _run(
                sys.executable,
                "-I",
                str(replacement_tool),
                "--expected-base-sha",
                trusted,
                "--project-root",
                str(project),
                "--project-source-sha",
                source,
                "--receipt",
                str(receipt),
                "--phase",
                "start",
            )

            self.assertNotEqual(0, result.returncode, result.stdout + result.stderr)
            self.assertIn("Base bootstrap executable bytes differ", result.stdout)


if __name__ == "__main__":
    unittest.main()
