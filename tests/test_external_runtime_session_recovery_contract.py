from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8")


class ExternalRuntimeSessionRecoveryContractTests(unittest.TestCase):
    def test_canonical_recovery_contract_requires_same_snapshot_evidence_and_fail_closed_classification(
        self,
    ) -> None:
        source = read("docs/knowledge/godot/GODOT_LIVE_EDITOR_SECURITY_AND_RECOVERY.md")

        for token in (
            "TARGET_PROCESS_IDENTITY",
            "TARGET_TRANSPORT_OWNERSHIP",
            "SERVER_HANDSHAKE_AND_SESSION_LOGS",
            "IMMEDIATE_SESSION_REGISTRY_READ",
            "EXACT_SESSION_RECOVERED",
            "SAME_SERVER_HANDSHAKE_REGISTRATION_BLOCKER",
            "PROCESS_OR_TRANSPORT_BLOCKER",
            "BLOCKED_UNVERIFIED",
        ):
            self.assertIn(token, source)

    def test_shared_server_and_stale_identity_rules_prevent_unsafe_resume(self) -> None:
        source = read("docs/knowledge/godot/GODOT_LIVE_EDITOR_SECURITY_AND_RECOVERY.md")

        for token in (
            "ONE_TARGET_SESSION_MISSING",
            "SHARED_SERVER_SAFE_TO_RESTART",
            "PAST_PID != CURRENT_TARGET",
            "PAST_WS_CONNECTION != CURRENT_TRANSPORT_PROOF",
            "PAST_SESSION_ID != CURRENT_REGISTRY_PROOF",
            "SESSION_RECOVERY_GREEN",
            "project tests/runtime validation remain separate",
        ):
            self.assertIn(token, source)

    def test_adapter_and_handoff_keep_distinct_recovery_responsibilities(self) -> None:
        adapter = read(
            "templates/project-operations/godot-live-editor/addons/"
            "base_live_editor_adapter/README.md"
        )
        handoff = read("skills/maintaining-project-context-and-handoff/SKILL.md")

        self.assertIn("same-snapshot", adapter)
        self.assertIn("external transport", adapter)
        self.assertIn("stale PID/session", handoff)


if __name__ == "__main__":
    unittest.main()
