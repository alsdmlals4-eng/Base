from __future__ import annotations

import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas/godot-live-editor-operation-envelope-v1.schema.json"


class GodotIdempotentApprovalSchemaTests(unittest.TestCase):
    def test_approved_idempotent_mutation_has_representable_token_binding(self) -> None:
        validator = Draft202012Validator(json.loads(SCHEMA.read_text(encoding="utf-8")))
        request_hash = "a" * 64
        envelope = {
            "schema_version": 1,
            "artifact_role": "GODOT_LIVE_EDITOR_OPERATION_ENVELOPE",
            "operation_id": "op-idempotent-approved-001",
            "project_fingerprint": "godot-project-a",
            "capability_id": "state.write_marker",
            "operation_class": "IDEMPOTENT_MUTATION",
            "request_hash": request_hash,
            "approval": {
                "state": "APPROVED",
                "token_binding": {
                    "token_id": "approval-001",
                    "project_fingerprint": "godot-project-a",
                    "capability_id": "state.write_marker",
                    "request_hash": request_hash,
                    "operation_class": "IDEMPOTENT_MUTATION",
                },
                "expires_at": "2099-01-01T00:00:00Z",
            },
            "task": {
                "task_id": None,
                "state": "NOT_APPLICABLE",
                "result_binding": None,
            },
            "result": {
                "success": True,
                "code": "OK",
                "message": "Mutation completed.",
                "data": {},
                "evidence": [],
            },
        }

        self.assertEqual([], list(validator.iter_errors(envelope)))


if __name__ == "__main__":
    unittest.main()
