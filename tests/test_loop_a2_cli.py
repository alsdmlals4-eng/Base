from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from tests.test_loop_a2_protocol import valid_request

ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "tools/loop_a2.py"


class CliTests(unittest.TestCase):
    def test_fake_fixture_burnin_three_runs(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            request_path = Path(temp) / "request.json"
            request_path.write_text(json.dumps(valid_request()), encoding="utf-8")
            completed = subprocess.run(
                [sys.executable, str(CLI), "burn-in-fixture", str(request_path),
                 "--observed-main-sha", "0123456789abcdef0123456789abcdef01234567",
                 "--runs", "3"],
                cwd=ROOT, text=True, capture_output=True, check=False,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)
            result = json.loads(completed.stdout)
            self.assertEqual(result["status"], "FAKE_PROVIDER_BURNIN_GREEN")
            self.assertEqual(result["consecutive_runs"], 3)

    def test_fixture_command_cannot_request_real_provider(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            value = valid_request()
            value["provider_mode"] = "REAL"
            request_path = Path(temp) / "request.json"
            request_path.write_text(json.dumps(value), encoding="utf-8")
            completed = subprocess.run(
                [sys.executable, str(CLI), "burn-in-fixture", str(request_path),
                 "--observed-main-sha", value["expected_main_sha"]],
                cwd=ROOT, text=True, capture_output=True, check=False,
            )
            self.assertEqual(completed.returncode, 2)
            self.assertEqual(json.loads(completed.stdout)["status"], "CONTRACT_INVALID")


if __name__ == "__main__":
    unittest.main()
