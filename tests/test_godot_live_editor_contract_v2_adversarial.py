from __future__ import annotations

import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from tests.test_godot_live_editor_contract_v2 import (
    V1_PILOT_MANIFEST,
    make_valid_manifest,
    make_valid_operation,
)
from tools.validate_godot_live_editor_contract_v2 import (
    canonical_json_sha256,
    operation_request_material,
    validate_contract_pair,
    validate_manifest_semantics,
    validate_operation_semantics,
)


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "tools/validate_godot_live_editor_contract_v2.py"


class GodotLiveEditorContractV2AdversarialTests(unittest.TestCase):
    maxDiff = None

    def test_terminal_task_hash_mismatch_is_not_misclassified_as_stale_identity(self) -> None:
        manifest = make_valid_manifest()
        capability = manifest["capabilities"][0]
        capability["execution_mode"] = "LONG_RUNNING_TASK"
        capability["retry_policy"]["requires_ledger"] = True
        capability["timeout_policy"]["unknown_outcome"] = "RESUME_BY_TASK_ID"

        operation = make_valid_operation(manifest)
        operation["result"]["result_hash"] = canonical_json_sha256(
            operation["result"]["data"]
        )
        operation["task"] = {
            "task_id": "task-1",
            "state": "COMPLETED",
            "created_at": "2026-08-05T00:00:00Z",
            "last_updated_at": "2026-08-05T00:00:01Z",
            "ttl_ms": 60000,
            "poll_interval_ms": 1000,
            "cancellation_policy": "NOT_SUPPORTED",
            "result_binding": {
                "operation_id": operation["operation_id"],
                "project_identity": copy.deepcopy(operation["project_identity"]),
                "automation_service_instance_id": operation["instance_identity"][
                    "automation_service_instance_id"
                ],
                "task_id": "task-1",
                "result_hash": "0" * 64,
            },
        }
        operation["request_hash"] = canonical_json_sha256(
            operation_request_material(operation)
        )

        errors = validate_operation_semantics(manifest, operation)
        self.assertIn("TASK_RESULT_HASH_MISMATCH", errors)
        self.assertNotIn("TASK_RESULT_STALE", errors)

    def test_v1_audit_rejects_invalid_v1_shape(self) -> None:
        errors = validate_contract_pair({"schema_version": 1}, mode="AUDIT")
        self.assertEqual(["V1_AUDIT_SCHEMA_INVALID"], errors)

    def test_cli_malformed_json_returns_one_stable_result_without_traceback(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            manifest = Path(temporary) / "bad.json"
            manifest.write_text("{not-json", encoding="utf-8")
            result = subprocess.run(
                [
                    sys.executable,
                    str(VALIDATOR),
                    "--manifest",
                    str(manifest),
                    "--mode",
                    "AUDIT",
                ],
                cwd=ROOT,
                check=False,
                text=True,
                capture_output=True,
            )

        self.assertEqual(1, result.returncode)
        self.assertEqual(
            {"status": "FAIL", "errors": ["INPUT_JSON_INVALID"]},
            json.loads(result.stdout),
        )
        self.assertEqual("", result.stderr)

    def test_project_defined_transport_requires_a_safe_local_profile(self) -> None:
        manifest = make_valid_manifest()
        manifest["transport"] = {
            "kind": "PROJECT_DEFINED",
            "enabled": True,
            "bind_host": None,
            "endpoint_identity": "project-local-ipc",
            "protocol_profile": "GENERIC",
            "protocol_version": "1.0",
            "access_control": {
                "authentication_mode": "OS_PEER_CREDENTIAL",
                "origin_policy": "NOT_APPLICABLE",
                "session_binding": "NOT_APPLICABLE",
                "os_access_control": "CURRENT_USER_ONLY",
            },
        }
        self.assertNotIn(
            "TRANSPORT_SECURITY_PROFILE_INVALID",
            validate_manifest_semantics(manifest),
        )

        unsafe = copy.deepcopy(manifest)
        unsafe["transport"]["bind_host"] = "0.0.0.0"
        self.assertIn(
            "TRANSPORT_SECURITY_PROFILE_INVALID",
            validate_manifest_semantics(unsafe),
        )

    def test_v1_pilot_remains_audit_readable(self) -> None:
        pilot = json.loads(V1_PILOT_MANIFEST.read_text(encoding="utf-8"))
        self.assertEqual([], validate_contract_pair(pilot, mode="AUDIT"))


if __name__ == "__main__":
    unittest.main()
