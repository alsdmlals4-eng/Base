from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = ROOT / "templates/project-operations/loop"


def load_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: dict[str, object]) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


class LoopCompletionGateTests(unittest.TestCase):
    def _copy_bundle(self, destination: Path) -> Path:
        shutil.copytree(TEMPLATES, destination, dirs_exist_ok=True)
        return destination / "PROJECT_EXECUTION_CAPSULE.json"

    def test_readiness_accepts_mapped_requirement_but_completion_rejects_it(self) -> None:
        from tools.loop_contracts.bundle_validation import validate_bundle, validate_completion

        self.assertEqual(validate_bundle(TEMPLATES / "PROJECT_EXECUTION_CAPSULE.json"), [])
        codes = {item.code for item in validate_completion(TEMPLATES / "PROJECT_EXECUTION_CAPSULE.json")}
        self.assertIn("COMPLETION_REQUIREMENT_OPEN", codes)

    def test_required_not_run_and_stale_destination_block_completion(self) -> None:
        from tools.loop_contracts.bundle_validation import validate_completion

        with tempfile.TemporaryDirectory() as temporary:
            capsule_path = self._copy_bundle(Path(temporary) / "loop")
            ledger = load_json(capsule_path.parent / "REQUIREMENT_COVERAGE_LEDGER.json")
            ledger["status"] = "VERIFIED"
            ledger["requirements"][0]["status"] = "VERIFIED"
            write_json(capsule_path.parent / "REQUIREMENT_COVERAGE_LEDGER.json", ledger)

            receipt = load_json(capsule_path.parent / "VERIFICATION_RECEIPT.json")
            receipt["status"] = "VERIFIED"
            receipt["checks"] = [{
                "check_id": "CORE_TESTS",
                "required": True,
                "status": "NOT_RUN",
                "evidence_ref": "",
                "reason": "executor unavailable",
            }]
            receipt["destinations"] = [{
                "destination_id": "PROJECT_NOTION",
                "kind": "NOTION",
                "required": True,
                "expected_ref": "abc",
                "observed_ref": "def",
                "sync_state": "SYNCED",
                "evidence_ref": "notion-readback",
            }]
            write_json(capsule_path.parent / "VERIFICATION_RECEIPT.json", receipt)

            codes = {item.code for item in validate_completion(capsule_path)}
            self.assertIn("REQUIRED_CHECK_NOT_PASS", codes)
            self.assertIn("DESTINATION_REF_MISMATCH", codes)

    def test_fully_verified_receipt_can_close_completion(self) -> None:
        from tools.loop_contracts.bundle_validation import validate_completion

        with tempfile.TemporaryDirectory() as temporary:
            capsule_path = self._copy_bundle(Path(temporary) / "loop")
            ledger = load_json(capsule_path.parent / "REQUIREMENT_COVERAGE_LEDGER.json")
            ledger["status"] = "VERIFIED"
            ledger["requirements"][0]["status"] = "VERIFIED"
            write_json(capsule_path.parent / "REQUIREMENT_COVERAGE_LEDGER.json", ledger)

            receipt = load_json(capsule_path.parent / "VERIFICATION_RECEIPT.json")
            receipt["status"] = "VERIFIED"
            receipt["checks"] = [{
                "check_id": "CORE_TESTS",
                "required": True,
                "status": "PASS",
                "evidence_ref": "ci://run/123",
                "reason": "",
            }]
            receipt["destinations"] = [{
                "destination_id": "PROJECT_NOTION",
                "kind": "NOTION",
                "required": True,
                "expected_ref": "same-ref",
                "observed_ref": "same-ref",
                "sync_state": "SYNCED",
                "evidence_ref": "notion-readback",
            }]
            write_json(capsule_path.parent / "VERIFICATION_RECEIPT.json", receipt)

            self.assertEqual(validate_completion(capsule_path), [])

    def test_cli_completion_phase_uses_completion_validator(self) -> None:
        completed = subprocess.run(
            [
                sys.executable,
                str(ROOT / "tools/check_loop_execution_capsule.py"),
                str(TEMPLATES / "PROJECT_EXECUTION_CAPSULE.json"),
                "--phase",
                "completion",
                "--format",
                "json",
            ],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(completed.returncode, 1)
        self.assertIn("COMPLETION_REQUIREMENT_OPEN", completed.stdout)


if __name__ == "__main__":
    unittest.main()
