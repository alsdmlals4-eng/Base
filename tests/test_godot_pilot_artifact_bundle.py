from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from tools import godot_multi_project_pilot as runner
from tools import godot_project_pilot_evidence as evidence
from tools.godot_project_pilot_evidence import VerifiedRuntimeEvidence


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class GodotPilotArtifactBundleTests(unittest.TestCase):
    def test_failed_runtime_result_is_redacted_before_terminal_verification(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            workspace = root / "workspace"
            output = root / "output"
            runtime_result = workspace / "artifacts/godot-project-pilot/runtime-result.json"
            runtime_result.parent.mkdir(parents=True)
            runtime_result.write_text(
                json.dumps(
                    {
                        "status": "FAIL",
                        "token": "secret-value",
                        "nested": {"authorization": "Bearer secret-value"},
                    }
                )
                + "\n",
                encoding="utf-8",
            )

            preserved = evidence.preserve_runtime_failure_diagnostics(
                workspace,
                runtime_result,
                output,
                attempt_id="run-1-attempt-1",
            )

            payload = json.loads(preserved.read_text(encoding="utf-8"))
            self.assertEqual("FAIL", payload["status"])
            self.assertEqual("[REDACTED]", payload["token"])
            self.assertEqual("[REDACTED]", payload["nested"]["authorization"])
            self.assertEqual("run-1-attempt-1", payload["diagnostic_attempt_id"])
            with self.assertRaisesRegex(
                evidence.EvidenceVerificationError,
                "RUNTIME_EVIDENCE_FAILED",
            ):
                evidence.verify_runtime_evidence(workspace, runtime_result)

    def test_failure_diagnostics_keep_attempts_separate(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            workspace = root / "workspace"
            output = root / "output"
            runtime_result = workspace / "runtime-result.json"
            runtime_result.parent.mkdir(parents=True)
            runtime_result.write_text('{"status":"FAIL"}\n', encoding="utf-8")

            first = evidence.preserve_runtime_failure_diagnostics(
                workspace,
                runtime_result,
                output,
                attempt_id="run-1-attempt-1",
            )
            second = evidence.preserve_runtime_failure_diagnostics(
                workspace,
                runtime_result,
                output,
                attempt_id="run-1-attempt-2",
            )

            self.assertNotEqual(first, second)
            self.assertTrue(first.is_file())
            self.assertTrue(second.is_file())

    def test_failure_diagnostic_rejects_escaped_and_oversized_runtime_results(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            workspace = root / "workspace"
            outside = root / "outside.json"
            workspace.mkdir()
            outside.write_text('{"status":"FAIL"}\n', encoding="utf-8")
            with self.assertRaisesRegex(evidence.EvidenceVerificationError, "EVIDENCE_PATH_ESCAPE"):
                evidence.preserve_runtime_failure_diagnostics(
                    workspace,
                    outside,
                    root / "output",
                    attempt_id="run-1-attempt-1",
                )

            oversized = workspace / "runtime-result.json"
            oversized.write_bytes(b"{" + b"x" * (1024 * 1024) + b"}")
            with self.assertRaisesRegex(evidence.EvidenceVerificationError, "oversized"):
                evidence.preserve_runtime_failure_diagnostics(
                    workspace,
                    oversized,
                    root / "output",
                    attempt_id="run-1-attempt-2",
                )

    def test_failure_diagnostic_rejects_nested_payloads_before_recursive_redaction(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            workspace = root / "workspace"
            runtime_result = workspace / "runtime-result.json"
            workspace.mkdir()
            payload: dict[str, object] = {"status": "FAIL"}
            for _ in range(800):
                payload = {"nested": payload}
            runtime_result.write_text(json.dumps(payload), encoding="utf-8")

            with self.assertRaisesRegex(evidence.EvidenceVerificationError, "nested"):
                evidence.preserve_runtime_failure_diagnostics(
                    workspace,
                    runtime_result,
                    root / "output",
                    attempt_id="run-1-attempt-1",
                )

    def test_failure_diagnostic_rejects_serialized_snapshot_that_exceeds_limit(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            workspace = root / "workspace"
            runtime_result = workspace / "runtime-result.json"
            workspace.mkdir()
            prefix = b'{"status":"FAIL","padding":"'
            suffix = b'"}'
            runtime_result.write_bytes(
                prefix
                + b"x" * (1024 * 1024 - len(prefix) - len(suffix))
                + suffix
            )

            with self.assertRaisesRegex(evidence.EvidenceVerificationError, "oversized"):
                evidence.preserve_runtime_failure_diagnostics(
                    workspace,
                    runtime_result,
                    root / "output",
                    attempt_id="run-1-attempt-1",
                )

    def test_failure_diagnostic_converts_excessive_nesting_to_fail_closed_error(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            workspace = root / "workspace"
            runtime_result = workspace / "runtime-result.json"
            workspace.mkdir()
            runtime_result.write_text(
                "{\"nested\":" * 1000 + '{\"status\":\"FAIL\"}' + "}" * 1000,
                encoding="utf-8",
            )

            with self.assertRaisesRegex(evidence.EvidenceVerificationError, "nested"):
                evidence.preserve_runtime_failure_diagnostics(
                    workspace,
                    runtime_result,
                    root / "output",
                    attempt_id="run-1-attempt-1",
                )

    def test_exported_bundle_contains_reverifiable_runtime_bytes(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            workspace = root / "workspace"
            output = root / "output"
            scene = workspace / ".godot-live-editor-pilot/scratch.tscn"
            runtime_result = workspace / "artifacts/godot-project-pilot/runtime-result.json"
            scene.parent.mkdir(parents=True)
            runtime_result.parent.mkdir(parents=True)
            scene.write_text("[gd_scene format=3]\n", encoding="utf-8")
            runtime_result.write_text(
                json.dumps({"status": "PASS"}, sort_keys=True) + "\n",
                encoding="utf-8",
            )
            verified = VerifiedRuntimeEvidence(
                repository="owner/game",
                source_commit="a" * 40,
                base_pilot_commit="b" * 40,
                saved_scene_path="res://.godot-live-editor-pilot/scratch.tscn",
                saved_scene_sha256=_sha256(scene),
                runtime_result_sha256=_sha256(runtime_result),
                ledger_states=("COMPLETED", "COMPLETED"),
            )

            exported = runner.export_runtime_evidence_bundle(
                workspace,
                runtime_result,
                output,
                verified,
            )

            self.assertEqual(output / "runtime-result.json", exported.runtime_result)
            self.assertEqual(output / "scratch.tscn", exported.saved_scene)
            self.assertEqual(verified.runtime_result_sha256, _sha256(exported.runtime_result))
            self.assertEqual(verified.saved_scene_sha256, _sha256(exported.saved_scene))

    def test_export_rejects_hash_mismatch(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            workspace = root / "workspace"
            output = root / "output"
            scene = workspace / ".godot-live-editor-pilot/scratch.tscn"
            runtime_result = workspace / "artifacts/godot-project-pilot/runtime-result.json"
            scene.parent.mkdir(parents=True)
            runtime_result.parent.mkdir(parents=True)
            scene.write_text("[gd_scene format=3]\n", encoding="utf-8")
            runtime_result.write_text("{}\n", encoding="utf-8")
            verified = VerifiedRuntimeEvidence(
                repository="owner/game",
                source_commit="a" * 40,
                base_pilot_commit="b" * 40,
                saved_scene_path="res://.godot-live-editor-pilot/scratch.tscn",
                saved_scene_sha256="0" * 64,
                runtime_result_sha256=_sha256(runtime_result),
                ledger_states=("COMPLETED", "COMPLETED"),
            )

            with self.assertRaisesRegex(ValueError, "ARTIFACT_BYTE_HASH_MISMATCH"):
                runner.export_runtime_evidence_bundle(
                    workspace,
                    runtime_result,
                    output,
                    verified,
                )


if __name__ == "__main__":
    unittest.main()
