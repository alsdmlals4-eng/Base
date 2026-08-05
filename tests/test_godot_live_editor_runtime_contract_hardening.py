from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
CAPABILITY_SCHEMA = ROOT / "schemas/godot-live-editor-capability-manifest-v1.schema.json"
OPERATION_SCHEMA = ROOT / "schemas/godot-live-editor-operation-envelope-v1.schema.json"
PILOT = ROOT / "examples/godot-live-editor-pilot"
MANIFEST = PILOT / "GODOT_LIVE_EDITOR_CAPABILITY_MANIFEST.json"
PLUGIN = PILOT / "addons/base_live_editor_pilot/plugin.gd"
READINESS = ROOT / "docs/knowledge/godot/GODOT_PRODUCTION_ADAPTER_READINESS.md"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


class GodotRuntimeContractHardeningTests(unittest.TestCase):
    def test_capability_schema_rejects_open_arguments_and_unsafe_idempotent_retry(self) -> None:
        validator = Draft202012Validator(load(CAPABILITY_SCHEMA))
        manifest = load(MANIFEST)

        open_arguments = copy.deepcopy(manifest)
        open_arguments["capabilities"][0]["arguments_schema"]["additionalProperties"] = True
        self.assertTrue(list(validator.iter_errors(open_arguments)))

        unsafe_retry = copy.deepcopy(manifest)
        capability = next(
            item for item in unsafe_retry["capabilities"]
            if item["capability_id"] == "state.write_marker"
        )
        capability["retry_policy"]["automatic"] = True
        capability["retry_policy"]["maximum_attempts"] = 2
        capability["timeout_policy"]["unknown_outcome"] = "RECONCILE_BEFORE_RETRY"
        self.assertTrue(list(validator.iter_errors(unsafe_retry)))

    def test_long_task_preflight_failure_is_representable_without_fake_task(self) -> None:
        validator = Draft202012Validator(load(OPERATION_SCHEMA))
        envelope = {
            "schema_version": 1,
            "artifact_role": "GODOT_LIVE_EDITOR_OPERATION_ENVELOPE",
            "operation_id": "op-preflight-failure",
            "project_fingerprint": "project-a",
            "capability_id": "task.start",
            "operation_class": "LONG_RUNNING_TASK",
            "request_hash": "a" * 64,
            "approval": {
                "state": "REQUIRED",
                "token_binding": None,
                "expires_at": None,
            },
            "task": {
                "task_id": None,
                "state": "NOT_STARTED",
                "result_binding": None,
            },
            "result": {
                "success": False,
                "code": "APPROVAL_REQUIRED",
                "message": "APPROVAL_REQUIRED",
                "data": {},
                "evidence": [],
            },
        }
        self.assertEqual([], list(validator.iter_errors(envelope)))

    def test_pilot_plugin_remains_no_network_and_production_gates_are_explicit(self) -> None:
        plugin = PLUGIN.read_text(encoding="utf-8")
        self.assertNotIn("TCPServer", plugin)
        self.assertNotIn("WebSocket", plugin)
        self.assertIn('"network_listener_enabled": false', plugin)

        combined = READINESS.read_text(encoding="utf-8")
        for term in (
            "EDITOR_MAIN_THREAD",
            "EditorUndoRedoManager",
            "additionalProperties: false",
            "single-use",
            "atomic",
            "STDIO",
            "OAuth 2.1",
            "PRODUCTION_ADAPTER_READY",
        ):
            self.assertIn(term, combined)


if __name__ == "__main__":
    unittest.main()
