from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
PILOT = ROOT / "examples/godot-live-editor-pilot"
MANIFEST = PILOT / "GODOT_LIVE_EDITOR_CAPABILITY_MANIFEST.json"
EVIDENCE = PILOT / "RUNTIME_EVIDENCE.json"
REPORT = ROOT / "docs/knowledge/godot/evidence/2026-08-05-godot-4-7-1-runtime-pilot.md"
CAPABILITY_SCHEMA = ROOT / "schemas/godot-live-editor-capability-manifest-v1.schema.json"
OPERATION_SCHEMA = ROOT / "schemas/godot-live-editor-operation-envelope-v1.schema.json"


class GodotLiveEditorRuntimePilotTests(unittest.TestCase):

    def _godot_bin(self) -> Path:
        raw = os.environ.get("GODOT_BIN")
        if not raw:
            self.skipTest("GODOT_BIN is not configured")
        path = Path(raw)
        self.assertTrue(path.is_file(), raw)
        return path

    def setUp(self) -> None:
        artifacts = PILOT / "artifacts"
        if artifacts.exists():
            shutil.rmtree(artifacts)
        artifacts.mkdir(parents=True)

    def _run_cli(
        self,
        command: str,
        request: dict | None = None,
        expected_returncode: int = 0,
    ) -> dict:
        args = [
            str(self._godot_bin()),
            "--headless",
            "--path",
            str(PILOT),
            "--script",
            "res://tools/live_editor_cli.gd",
            "--",
            command,
        ]
        if request is not None:
            request_path = PILOT / "artifacts/request.json"
            request_path.write_text(json.dumps(request, ensure_ascii=False), encoding="utf-8")
            args.append("res://artifacts/request.json")
        completed = subprocess.run(
            args,
            text=True,
            capture_output=True,
            timeout=30,
            check=False,
        )
        self.assertEqual(
            expected_returncode,
            completed.returncode,
            f"stdout:\n{completed.stdout}\nstderr:\n{completed.stderr}",
        )
        prefix = "BASE_GODOT_RESULT="
        lines = [line for line in completed.stdout.splitlines() if line.startswith(prefix)]
        self.assertEqual(1, len(lines), completed.stdout)
        return json.loads(lines[0][len(prefix):])


    def _project_fingerprint(self) -> str:
        ignore = (PILOT / ".gitignore").read_text(encoding="utf-8")
        for ignored in (".godot/", "artifacts/", "*.uid"):
            self.assertIn(ignored, ignore)

        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        return manifest["project_identity"]["project_fingerprint"]

    @staticmethod
    def _mutation_request_hash(operation_id: str, marker: str, idempotency_key: str) -> str:
        normalized = f"marker={marker}|idempotency_key={idempotency_key}|operation_id={operation_id}"
        return hashlib.sha256(normalized.encode("utf-8")).hexdigest()

    def _mutation_request(
        self,
        *,
        approved: bool,
        operation_id: str = "op-marker-001",
        marker: str = "runtime-pilot-green",
        idempotency_key: str = "marker-key-001",
        token_id: str = "approval-marker-001",
        expires_at: str = "2099-01-01T00:00:00Z",
    ) -> dict:
        request_hash = self._mutation_request_hash(operation_id, marker, idempotency_key)
        approval = {"state": "REQUIRED", "token_binding": None, "expires_at": None}
        if approved:
            approval = {
                "state": "APPROVED",
                "token_binding": {
                    "token_id": token_id,
                    "project_fingerprint": self._project_fingerprint(),
                    "capability_id": "state.write_marker",
                    "request_hash": request_hash,
                    "operation_class": "IDEMPOTENT_MUTATION",
                },
                "expires_at": expires_at,
            }
        return {
            "operation_id": operation_id,
            "marker": marker,
            "idempotency_key": idempotency_key,
            "request_hash": request_hash,
            "approval": approval,
        }


    @staticmethod
    def _task_request_hash(capability_id: str, operation_id: str, task_id: str | None = None) -> str:
        normalized = f"operation_id={operation_id}|capability_id={capability_id}"
        if task_id is not None:
            normalized += f"|task_id={task_id}"
        return hashlib.sha256(normalized.encode("utf-8")).hexdigest()

    def _task_request(self, capability_id: str, *, task_id: str | None = None) -> dict:
        operation_id = "op-task-001"
        request_hash = self._task_request_hash(capability_id, operation_id, task_id)
        request = {
            "operation_id": operation_id,
            "request_hash": request_hash,
            "approval": {
                "state": "APPROVED",
                "token_binding": {
                    "token_id": f"approval-{capability_id}",
                    "project_fingerprint": self._project_fingerprint(),
                    "capability_id": capability_id,
                    "request_hash": request_hash,
                    "operation_class": "LONG_RUNNING_TASK",
                },
                "expires_at": "2099-01-01T00:00:00Z",
            },
        }
        if task_id is not None:
            request["task_id"] = task_id
        return request





    def _assert_operation_schema_valid(self, envelope: dict) -> None:
        validator = Draft202012Validator(
            json.loads(OPERATION_SCHEMA.read_text(encoding="utf-8"))
        )
        errors = list(validator.iter_errors(envelope))
        self.assertEqual([], [error.message for error in errors])



    def test_manifest_capability_schemas_are_closed_and_retry_semantics_are_consistent(self) -> None:
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        for capability in manifest["capabilities"]:
            with self.subTest(capability=capability["capability_id"]):
                arguments_schema = capability["arguments_schema"]
                Draft202012Validator.check_schema(arguments_schema)
                self.assertEqual("object", arguments_schema.get("type"))
                self.assertIs(False, arguments_schema.get("additionalProperties"))
                if capability["retry_policy"]["automatic"]:
                    self.assertEqual(
                        "SAFE_TO_RETRY",
                        capability["timeout_policy"]["unknown_outcome"],
                    )

        mutation = next(
            item for item in manifest["capabilities"]
            if item["capability_id"] == "state.write_marker"
        )
        self.assertFalse(mutation["retry_policy"]["automatic"])
        self.assertLessEqual(mutation["retry_policy"]["maximum_attempts"], 1)

    def test_long_task_preflight_failure_is_not_started_without_fake_task(self) -> None:
        missing_request = self._run_cli("task.start", expected_returncode=2)
        self.assertEqual("REQUEST_INVALID", missing_request["result"]["code"])
        self.assertEqual("NOT_STARTED", missing_request["task"]["state"])
        self.assertIsNone(missing_request["task"]["task_id"])
        self.assertIsNone(missing_request["task"]["result_binding"])
        self._assert_operation_schema_valid(missing_request)

    def test_expired_and_reused_approval_tokens_fail_closed(self) -> None:
        expired = self._run_cli(
            "state.write_marker",
            self._mutation_request(
                approved=True,
                operation_id="op-expired-001",
                idempotency_key="expired-key-001",
                token_id="approval-expired-001",
                expires_at="2000-01-01T00:00:00Z",
            ),
            expected_returncode=2,
        )
        self.assertEqual("APPROVAL_EXPIRED", expired["result"]["code"])
        self.assertEqual("EXPIRED", expired["approval"]["state"])

        first = self._run_cli(
            "state.write_marker",
            self._mutation_request(
                approved=True,
                operation_id="op-token-first",
                marker="first",
                idempotency_key="token-first-key",
                token_id="single-use-token",
            ),
        )
        self.assertEqual("OK", first["result"]["code"])

        reused = self._run_cli(
            "state.write_marker",
            self._mutation_request(
                approved=True,
                operation_id="op-token-second",
                marker="second",
                idempotency_key="token-second-key",
                token_id="single-use-token",
            ),
            expected_returncode=2,
        )
        self.assertEqual("APPROVAL_TOKEN_REUSED", reused["result"]["code"])
        self.assertEqual("REJECTED", reused["approval"]["state"])

    def test_mutation_request_schema_and_ledger_fail_closed(self) -> None:
        request = self._mutation_request(approved=True)
        request["unexpected"] = "not allowed"
        invalid = self._run_cli(
            "state.write_marker", request, expected_returncode=2
        )
        self.assertEqual("REQUEST_SCHEMA_INVALID", invalid["result"]["code"])

        state_path = PILOT / "artifacts/pilot_state.json"
        state_path.mkdir()
        try:
            failed = self._run_cli(
                "state.write_marker",
                self._mutation_request(
                    approved=True,
                    operation_id="op-state-failure",
                    marker="will-not-write",
                    idempotency_key="state-failure-key",
                    token_id="state-failure-token",
                ),
                expected_returncode=2,
            )
            self.assertEqual("STATE_WRITE_FAILED", failed["result"]["code"])
            ledger = json.loads(
                (PILOT / "artifacts/operation_ledger.json").read_text(encoding="utf-8")
            )
            record = ledger["operations"]["op-state-failure"]
            self.assertEqual("FAILED", record["state"])
            self.assertEqual("state.write_marker", record["capability_id"])
            self.assertEqual("state-failure-token", record["approval_token_id"])
            self.assertEqual("STATE_WRITE_FAILED", record["result_code"])
        finally:
            state_path.rmdir()

    def test_doctor_fails_closed_when_catalog_hash_is_stale(self) -> None:
        original_text = MANIFEST.read_text(encoding="utf-8")
        manifest = json.loads(original_text)
        manifest["capabilities"][0]["description"] += " tampered"
        MANIFEST.write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        try:
            stale = self._run_cli("doctor", expected_returncode=2)
            self.assertEqual("CATALOG_STALE", stale["result"]["code"])
            self._assert_operation_schema_valid(stale)
        finally:
            MANIFEST.write_text(original_text, encoding="utf-8")

    def test_long_task_failure_envelopes_remain_schema_valid(self) -> None:
        missing_request = self._run_cli(
            "task.start",
            request=None,
            expected_returncode=2,
        )
        self.assertEqual("REQUEST_INVALID", missing_request["result"]["code"])
        self._assert_operation_schema_valid(missing_request)

        approval_missing = self._task_request("task.start")
        approval_missing["approval"] = {
            "state": "REQUIRED",
            "token_binding": None,
            "expires_at": None,
        }
        rejected = self._run_cli(
            "task.start",
            approval_missing,
            expected_returncode=2,
        )
        self.assertEqual("APPROVAL_REQUIRED", rejected["result"]["code"])
        self._assert_operation_schema_valid(rejected)

        started = self._run_cli("task.start", self._task_request("task.start"))
        wrong_task_id = "task-wrong-0001"
        stale = self._run_cli(
            "task.resume",
            self._task_request("task.resume", task_id=wrong_task_id),
            expected_returncode=2,
        )
        self.assertEqual("TASK_RESULT_STALE", stale["result"]["code"])
        self._assert_operation_schema_valid(stale)
        self.assertNotEqual(started["task"]["task_id"], wrong_task_id)

    def test_manifest_and_captured_runtime_envelopes_validate_against_base_schemas(self) -> None:
        capability_validator = Draft202012Validator(
            json.loads(CAPABILITY_SCHEMA.read_text(encoding="utf-8"))
        )
        operation_validator = Draft202012Validator(
            json.loads(OPERATION_SCHEMA.read_text(encoding="utf-8"))
        )
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        self.assertEqual([], list(capability_validator.iter_errors(manifest)))

        evidence_text = EVIDENCE.read_text(encoding="utf-8")
        self.assertNotIn("/mnt/data/", evidence_text)
        evidence = json.loads(evidence_text)
        failures = []
        for capture in evidence["pilot"]["representative_operations"]:
            errors = list(operation_validator.iter_errors(capture["envelope"]))
            if errors:
                failures.append(
                    {
                        "command": capture["command"],
                        "errors": [error.message for error in errors],
                    }
                )
        self.assertEqual([], failures)
        self.assertEqual(18, evidence["pilot"]["captured_operation_count"])
        self.assertEqual(18, len(evidence["pilot"]["result_code_sequence"]))
        self.assertEqual(18, len(evidence["pilot"]["operation_envelope_sha256"]))
        self.assertGreaterEqual(len(evidence["pilot"]["representative_operations"]), 8)

    def test_runtime_evidence_preserves_uploaded_input_and_unverified_boundaries(self) -> None:
        self.assertTrue(EVIDENCE.is_file())
        self.assertTrue(REPORT.is_file())
        evidence = json.loads(EVIDENCE.read_text(encoding="utf-8"))
        self.assertEqual("GODOT_4_7_1_RUNTIME_PILOT_EVIDENCE", evidence["artifact_role"])
        self.assertEqual("4.7.1.stable.official.a13da4feb", evidence["engine"]["version"])
        self.assertEqual(
            "c7ff14fd28472c8d4f193043de30278dcf7e5241a1dcf7566b02e27addaa33ba",
            evidence["engine"]["archive_sha256"],
        )
        self.assertEqual(
            "32f8d7596c4b41185512b1c49d69f2da3be018fd784a53e349fa92a98a97bcde",
            evidence["engine"]["executable_sha256"],
        )
        self.assertEqual(
            {"Blacksmith", "urban-legend", "새 게임 프로젝트", "십보강호: 전투 POC"},
            {item["project_name"] for item in evidence["uploaded_project_configs"]},
        )
        self.assertTrue(all(item["configuration_parse_state"] == "EXECUTION_PASS" for item in evidence["uploaded_project_configs"]))
        self.assertTrue(all(item["runtime_state"] == "NOT_RUN" for item in evidence["uploaded_project_configs"]))
        self.assertEqual("RUNTIME_PASS", evidence["pilot"]["cli_headless_state"])
        self.assertEqual("RUNTIME_PASS", evidence["pilot"]["editor_plugin_state"])
        self.assertEqual("NOT_IMPLEMENTED", evidence["boundaries"]["network_mcp_transport"])
        self.assertEqual("NOT_IMPLEMENTED", evidence["boundaries"]["runtime_debugger_bridge"])
        self.assertEqual("NOT_RUN", evidence["boundaries"]["physical_input_validation"])
        self.assertEqual("HUMAN_NOT_RUN", evidence["boundaries"]["human_editor_usability"])

        report = REPORT.read_text(encoding="utf-8")
        for term in (
            "Blacksmith",
            "urban-legend",
            "새 게임 프로젝트",
            "십보강호: 전투 POC",
            "NOT_RUN",
            "NOT_PROVIDED",
            "GODOT_SILENCE_ROOT_WARNING",
        ):
            self.assertIn(term, report)

    def test_headless_editor_loads_no_network_pilot_plugin(self) -> None:
        completed = subprocess.run(
            [
                str(self._godot_bin()),
                "--headless",
                "--editor",
                "--path",
                str(PILOT),
                "--quit-after",
                "5",
            ],
            text=True,
            capture_output=True,
            timeout=30,
            check=False,
        )
        self.assertEqual(
            0,
            completed.returncode,
            f"stdout:\n{completed.stdout}\nstderr:\n{completed.stderr}",
        )
        marker_path = PILOT / "artifacts/editor_plugin_loaded.json"
        self.assertTrue(marker_path.is_file(), completed.stdout + completed.stderr)
        marker = json.loads(marker_path.read_text(encoding="utf-8"))
        self.assertEqual("base_live_editor_pilot", marker["plugin_id"])
        self.assertEqual("LOADED", marker["state"])
        self.assertFalse(marker["network_listener_enabled"])
        self.assertEqual("examples/godot-live-editor-pilot", marker["project_path"])

    def test_long_task_starts_once_and_resumes_same_record(self) -> None:
        started = self._run_cli("task.start", self._task_request("task.start"))
        self.assertTrue(started["result"]["success"])
        self.assertEqual("TASK_PENDING", started["result"]["code"])
        self.assertEqual("PENDING", started["task"]["state"])
        task_id = started["task"]["task_id"]
        self.assertTrue(task_id)

        repeated = self._run_cli("task.start", self._task_request("task.start"))
        self.assertEqual("TASK_PENDING", repeated["result"]["code"])
        self.assertEqual(task_id, repeated["task"]["task_id"])

        resumed = self._run_cli(
            "task.resume",
            self._task_request("task.resume", task_id=task_id),
        )
        self.assertTrue(resumed["result"]["success"])
        self.assertEqual("OK", resumed["result"]["code"])
        self.assertEqual("COMPLETED", resumed["task"]["state"])
        binding = resumed["task"]["result_binding"]
        self.assertEqual(self._project_fingerprint(), binding["project_fingerprint"])
        self.assertEqual("task.resume", binding["capability_id"])
        self.assertEqual("op-task-001", binding["operation_id"])
        self.assertEqual(task_id, binding["task_id"])
        self.assertEqual(64, len(binding["result_hash"]))

        ledger = json.loads((PILOT / "artifacts/operation_ledger.json").read_text(encoding="utf-8"))
        self.assertEqual(1, len(ledger["tasks"]))
        self.assertEqual("COMPLETED", ledger["tasks"]["op-task-001"]["state"])

    def test_marker_mutation_requires_bound_approval_and_replays_idempotently(self) -> None:
        rejected = self._run_cli(
            "state.write_marker",
            self._mutation_request(approved=False),
            expected_returncode=2,
        )
        self.assertFalse(rejected["result"]["success"])
        self.assertEqual("APPROVAL_REQUIRED", rejected["result"]["code"])
        self.assertFalse((PILOT / "artifacts/pilot_state.json").exists())

        accepted = self._run_cli("state.write_marker", self._mutation_request(approved=True))
        self.assertTrue(accepted["result"]["success"])
        self.assertEqual("OK", accepted["result"]["code"])
        state = json.loads((PILOT / "artifacts/pilot_state.json").read_text(encoding="utf-8"))
        self.assertEqual("runtime-pilot-green", state["marker"])

        replay = self._run_cli("state.write_marker", self._mutation_request(approved=True))
        self.assertTrue(replay["result"]["success"])
        self.assertEqual("IDEMPOTENT_REPLAY", replay["result"]["code"])
        ledger = json.loads((PILOT / "artifacts/operation_ledger.json").read_text(encoding="utf-8"))
        self.assertEqual(1, len(ledger["idempotency"]))

    def test_uploaded_engine_runs_expected_version(self) -> None:
        completed = subprocess.run(
            [str(self._godot_bin()), "--version"],
            text=True,
            capture_output=True,
            timeout=10,
            check=False,
        )
        self.assertEqual(0, completed.returncode, completed.stderr)
        self.assertEqual("4.7.1.stable.official.a13da4feb", completed.stdout.strip())

    def test_read_only_cli_commands_return_stable_envelopes(self) -> None:
        expected_codes = {
            "doctor": "OK",
            "status": "OK",
            "catalog.compact": "OK",
            "scene.inspect": "OK",
        }
        for command, expected_code in expected_codes.items():
            with self.subTest(command=command):
                envelope = self._run_cli(command)
                self.assertEqual(command, envelope["capability_id"])
                self.assertEqual("READ_ONLY", envelope["operation_class"])
                self.assertTrue(envelope["result"]["success"])
                self.assertEqual(expected_code, envelope["result"]["code"])

    def test_fixture_declares_bounded_configured_capabilities(self) -> None:
        required = (
            PILOT / ".gitignore",
            PILOT / "project.godot",
            PILOT / "main.tscn",
            PILOT / "scripts/pilot_main.gd",
            MANIFEST,
        )
        self.assertEqual([], [str(path.relative_to(ROOT)) for path in required if not path.is_file()])

        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        self.assertEqual("CONFIGURED", manifest["configuration_state"])
        self.assertTrue(manifest["transport"]["enabled"])
        self.assertEqual("CLI", manifest["transport"]["kind"])
        self.assertIsNone(manifest["transport"]["bind_host"])
        self.assertEqual(
            {
                "doctor",
                "status",
                "catalog.compact",
                "scene.inspect",
                "state.write_marker",
                "task.start",
                "task.resume",
            },
            {item["capability_id"] for item in manifest["capabilities"]},
        )


if __name__ == "__main__":
    unittest.main()
