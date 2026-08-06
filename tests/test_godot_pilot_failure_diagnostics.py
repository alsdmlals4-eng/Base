from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from tools.godot_project_pilot_evidence import (
    EvidenceVerificationError,
    verify_runtime_evidence,
)


class GodotPilotFailureDiagnosticTests(unittest.TestCase):
    def test_failed_runtime_reports_only_bounded_verification_fields(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            result_path = root / "runtime-result.json"
            result_path.write_text(
                json.dumps(
                    {
                        "status": "FAIL",
                        "code": "ADAPTER_NOT_CONFIGURED",
                        "main_scene_inspect": "NOT_RUN",
                        "scratch_scene_rename": "NOT_RUN",
                        "editor_undo": "NOT_RUN",
                        "scratch_scene_save": "NOT_RUN",
                        "ledger_states": [],
                        "base_network_listener": False,
                        "untrusted_free_text": "must-not-be-copied",
                    }
                ),
                encoding="utf-8",
            )

            with self.assertRaises(EvidenceVerificationError) as raised:
                verify_runtime_evidence(root, result_path)

            message = str(raised.exception)
            for marker in (
                "RUNTIME_EVIDENCE_FAILED",
                '"status":"FAIL"',
                '"code":"ADAPTER_NOT_CONFIGURED"',
                '"main_scene_inspect":"NOT_RUN"',
                '"scratch_scene_rename":"NOT_RUN"',
                '"editor_undo":"NOT_RUN"',
                '"scratch_scene_save":"NOT_RUN"',
                '"ledger_states":[]',
                '"base_network_listener":false',
            ):
                self.assertIn(marker, message)
            self.assertNotIn("untrusted_free_text", message)
            self.assertNotIn("must-not-be-copied", message)


if __name__ == "__main__":
    unittest.main()
