from __future__ import annotations

import json
from pathlib import Path
import unittest

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = json.loads(
    (ROOT / "schemas/loop-a2-worker-result-v1.schema.json").read_text(encoding="utf-8")
)


def worker(*, status: str, errors: list[dict[str, str]]) -> dict[str, object]:
    return {
        "schema_version": 1,
        "contract_role": "LOOP_A2_WORKER_RESULT",
        "project_id": "BLACKSMITH",
        "run_id": "RUN_001",
        "package_id": "PACKAGE_001",
        "expected_main_sha": "a" * 40,
        "role": "BUILDER",
        "status": status,
        "changed_paths": ["scripts/feature/a.gd"] if status == "COMPLETED" else [],
        "summary": status,
        "usage": {"turns": 1},
        "errors": errors,
    }


class WorkerSchemaInvariantTests(unittest.TestCase):
    def errors(self, value: dict[str, object]) -> list[str]:
        return [error.message for error in Draft202012Validator(SCHEMA).iter_errors(value)]

    def test_completed_requires_no_errors(self) -> None:
        self.assertEqual(self.errors(worker(status="COMPLETED", errors=[])), [])
        self.assertTrue(
            self.errors(
                worker(
                    status="COMPLETED",
                    errors=[{"code": "FAILED_ANYWAY", "message": "contradiction"}],
                )
            )
        )

    def test_failed_or_blocked_requires_error_evidence(self) -> None:
        for status in ("FAILED", "BLOCKED"):
            with self.subTest(status=status):
                self.assertTrue(self.errors(worker(status=status, errors=[])))
                self.assertEqual(
                    self.errors(
                        worker(
                            status=status,
                            errors=[{"code": "PROVIDER_FAILURE", "message": "bounded failure"}],
                        )
                    ),
                    [],
                )


if __name__ == "__main__":
    unittest.main()
