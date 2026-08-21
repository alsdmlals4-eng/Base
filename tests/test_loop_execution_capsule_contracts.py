from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = ROOT / "schemas"
TEMPLATES = ROOT / "templates/project-operations/loop"
REQUIRED_SCHEMAS = (
    "loop-project-execution-capsule-v1.schema.json",
    "loop-planning-lock-v1.schema.json",
    "loop-visual-lock-v1.schema.json",
    "loop-runtime-adapter-v1.schema.json",
    "loop-implementation-package-v1.schema.json",
    "loop-requirement-coverage-ledger-v1.schema.json",
    "loop-active-run-v1.schema.json",
    "loop-immutable-run-v1.schema.json",
    "loop-verification-receipt-v1.schema.json",
)
REQUIRED_TEMPLATES = (
    "PROJECT_EXECUTION_CAPSULE.json",
    "PLANNING_LOCK.json",
    "VISUAL_LOCK.json",
    "RUNTIME_ADAPTER.json",
    "IMPLEMENTATION_PACKAGE.json",
    "REQUIREMENT_COVERAGE_LEDGER.json",
    "ACTIVE_LOOP_RUN.json",
    "VERIFICATION_RECEIPT.json",
    "runs/IMMUTABLE_RUN.json",
    "README.md",
)


def load_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def schema_errors(name: str, instance: dict[str, object]) -> list[str]:
    schema = load_json(SCHEMAS / name)
    return [error.message for error in Draft202012Validator(schema).iter_errors(instance)]


class LoopExecutionCapsuleContractTests(unittest.TestCase):
    def test_schema_inventory_is_fail_closed(self) -> None:
        for name in REQUIRED_SCHEMAS:
            with self.subTest(name=name):
                schema = load_json(SCHEMAS / name)
                self.assertEqual(schema["$schema"], "https://json-schema.org/draft/2020-12/schema")
                self.assertEqual(schema["type"], "object")
                self.assertFalse(schema["additionalProperties"])

    def test_templates_are_complete_and_schema_valid(self) -> None:
        mapping = {
            "PROJECT_EXECUTION_CAPSULE.json": "loop-project-execution-capsule-v1.schema.json",
            "PLANNING_LOCK.json": "loop-planning-lock-v1.schema.json",
            "VISUAL_LOCK.json": "loop-visual-lock-v1.schema.json",
            "RUNTIME_ADAPTER.json": "loop-runtime-adapter-v1.schema.json",
            "IMPLEMENTATION_PACKAGE.json": "loop-implementation-package-v1.schema.json",
            "REQUIREMENT_COVERAGE_LEDGER.json": "loop-requirement-coverage-ledger-v1.schema.json",
            "ACTIVE_LOOP_RUN.json": "loop-active-run-v1.schema.json",
            "VERIFICATION_RECEIPT.json": "loop-verification-receipt-v1.schema.json",
            "runs/IMMUTABLE_RUN.json": "loop-immutable-run-v1.schema.json",
        }
        for relative in REQUIRED_TEMPLATES:
            self.assertTrue((TEMPLATES / relative).is_file(), relative)
        for relative, schema_name in mapping.items():
            self.assertEqual(schema_errors(schema_name, load_json(TEMPLATES / relative)), [])

    def test_immutable_receipt_requires_digest_and_allows_stopped_state(self) -> None:
        receipt = load_json(TEMPLATES / "runs/IMMUTABLE_RUN.json")
        self.assertEqual(schema_errors("loop-immutable-run-v1.schema.json", receipt), [])
        self.assertEqual(len(str(receipt["receipt_sha256"])), 64)
        receipt["state"] = "STOPPED"
        self.assertEqual(schema_errors("loop-immutable-run-v1.schema.json", receipt), [])
        receipt.pop("receipt_sha256")
        self.assertTrue(schema_errors("loop-immutable-run-v1.schema.json", receipt))

    def test_minimal_bundle_is_valid(self) -> None:
        from tools.loop_contracts.bundle_validation import validate_bundle
        self.assertEqual(validate_bundle(TEMPLATES / "PROJECT_EXECUTION_CAPSULE.json"), [])

    def test_direct_cli_validates_template_bundle(self) -> None:
        completed = subprocess.run(
            [
                sys.executable,
                str(ROOT / "tools/check_loop_execution_capsule.py"),
                str(TEMPLATES / "PROJECT_EXECUTION_CAPSULE.json"),
                "--format",
                "json",
            ],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(json.loads(completed.stdout), [])

    def test_project_mismatch_and_stale_authority_fail(self) -> None:
        from tools.loop_contracts.bundle_validation import validate_bundle
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._copy_bundle(root)
            planning = load_json(root / "PLANNING_LOCK.json")
            planning["project_id"] = "OTHER_PROJECT"
            (root / "PLANNING_LOCK.json").write_text(json.dumps(planning, indent=2) + "\n", encoding="utf-8")
            self.assertIn("PROJECT_ID_MISMATCH", {item.code for item in validate_bundle(root / "PROJECT_EXECUTION_CAPSULE.json")})
            self._copy_bundle(root)
            package = load_json(root / "IMPLEMENTATION_PACKAGE.json")
            package["source_main_sha"] = "1" * 40
            (root / "IMPLEMENTATION_PACKAGE.json").write_text(json.dumps(package, indent=2) + "\n", encoding="utf-8")
            self.assertIn("STALE_AUTHORITY", {item.code for item in validate_bundle(root / "PROJECT_EXECUTION_CAPSULE.json")})

    def test_visual_and_coverage_gates_fail_closed(self) -> None:
        from tools.loop_contracts.bundle_validation import validate_bundle
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._copy_bundle(root)
            package = load_json(root / "IMPLEMENTATION_PACKAGE.json")
            package["visual_impact"] = "NEW_VISUAL_REQUIRED"
            package["visual_lock_requirement"] = "VISUAL_LOCKED"
            (root / "IMPLEMENTATION_PACKAGE.json").write_text(json.dumps(package, indent=2) + "\n", encoding="utf-8")
            self.assertIn("USER_DECISION_REQUIRED", {item.code for item in validate_bundle(root / "PROJECT_EXECUTION_CAPSULE.json")})
            self._copy_bundle(root)
            ledger = load_json(root / "REQUIREMENT_COVERAGE_LEDGER.json")
            ledger["requirements"][0]["requirement_id"] = "REQ_OTHER"
            (root / "REQUIREMENT_COVERAGE_LEDGER.json").write_text(json.dumps(ledger, indent=2) + "\n", encoding="utf-8")
            self.assertIn("UNMAPPED_REQUIREMENT", {item.code for item in validate_bundle(root / "PROJECT_EXECUTION_CAPSULE.json")})
            self._copy_bundle(root)
            ledger = load_json(root / "REQUIREMENT_COVERAGE_LEDGER.json")
            ledger["requirements"][0]["outputs"].append("scripts/unapproved.gd")
            (root / "REQUIREMENT_COVERAGE_LEDGER.json").write_text(json.dumps(ledger, indent=2) + "\n", encoding="utf-8")
            self.assertIn("UNAPPROVED_EXTRA_OUTPUT", {item.code for item in validate_bundle(root / "PROJECT_EXECUTION_CAPSULE.json")})

    def test_cross_project_paths_are_rejected_independent_of_host_os(self) -> None:
        from tools.loop_contracts.bundle_validation import validate_bundle
        for unsafe in ("../OTHER/PLANNING_LOCK.json", "..\\OTHER\\PLANNING_LOCK.json"):
            with self.subTest(unsafe=unsafe), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                self._copy_bundle(root)
                capsule = load_json(root / "PROJECT_EXECUTION_CAPSULE.json")
                capsule["planning_lock_path"] = unsafe
                (root / "PROJECT_EXECUTION_CAPSULE.json").write_text(json.dumps(capsule, indent=2) + "\n", encoding="utf-8")
                self.assertIn("UNSAFE_PROJECT_PATH", {item.code for item in validate_bundle(root / "PROJECT_EXECUTION_CAPSULE.json")})

    def _copy_bundle(self, destination: Path) -> None:
        destination.mkdir(parents=True, exist_ok=True)
        for relative in REQUIRED_TEMPLATES:
            source = TEMPLATES / relative
            target = destination / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(source.read_bytes())


if __name__ == "__main__":
    unittest.main()
