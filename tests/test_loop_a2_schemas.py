from __future__ import annotations

import json
from pathlib import Path
import unittest

from jsonschema import Draft202012Validator

from tests.test_loop_a2_protocol import valid_request

ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = ROOT / "schemas"


class SchemaTests(unittest.TestCase):
    def validate(self, name: str, value: dict[str, object]) -> list[str]:
        schema = json.loads((SCHEMAS / name).read_text(encoding="utf-8"))
        return [error.message for error in Draft202012Validator(schema).iter_errors(value)]

    def test_schemas_are_closed_draft_2020_12(self) -> None:
        for path in sorted(SCHEMAS.glob("loop-a2-*.schema.json")):
            with self.subTest(path=path.name):
                schema = json.loads(path.read_text(encoding="utf-8"))
                self.assertEqual(schema["$schema"], "https://json-schema.org/draft/2020-12/schema")
                self.assertFalse(schema["additionalProperties"])

    def test_request_schema_accepts_valid_and_rejects_authority_expansion(self) -> None:
        self.assertEqual(self.validate("loop-a2-run-request-v1.schema.json", valid_request()), [])
        errors = self.validate("loop-a2-run-request-v1.schema.json", valid_request() | {"merge": True})
        self.assertTrue(errors)

    def test_worker_and_review_schema_reject_hidden_reasoning(self) -> None:
        worker = {
            "schema_version": 1, "contract_role": "LOOP_A2_WORKER_RESULT",
            "project_id": "BLACKSMITH", "run_id": "RUN_001", "package_id": "PACKAGE_001",
            "expected_main_sha": "a" * 40, "role": "BUILDER", "status": "COMPLETED",
            "changed_paths": ["scripts/feature/a.gd"], "summary": "done",
            "usage": {"turns": 1}, "errors": [], "reasoning": "hidden",
        }
        review = {
            "schema_version": 1, "contract_role": "LOOP_A2_REVIEW_RESULT",
            "project_id": "BLACKSMITH", "run_id": "RUN_001", "package_id": "PACKAGE_001",
            "expected_main_sha": "a" * 40, "role": "CRITIC", "verdict": "PASS",
            "findings": [], "checked_requirement_ids": ["REQ_001"], "chain_of_thought": "hidden",
        }
        self.assertTrue(self.validate("loop-a2-worker-result-v1.schema.json", worker))
        self.assertTrue(self.validate("loop-a2-review-result-v1.schema.json", review))


if __name__ == "__main__":
    unittest.main()
