from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
METHOD = (ROOT / "docs/knowledge/methods/PROJECT_HANDOFF_CONTEXT_METHOD.md").read_text(
    encoding="utf-8"
)
TEMPLATE = (ROOT / "templates/project-operations/HANDOFF.md").read_text(encoding="utf-8")


class HandoffResumabilityContractTests(unittest.TestCase):
    def assert_contract_tokens(self, tokens: tuple[str, ...]) -> None:
        corpus = METHOD + "\n" + TEMPLATE
        for token in tokens:
            with self.subTest(token=token):
                self.assertIn(token, corpus)

    def test_receiver_ack_is_distinct_from_packet_readiness(self) -> None:
        self.assert_contract_tokens(
            ("PACKET_READY", "PENDING_RECEIVER_ACK", "TRANSFER_ACCEPTED", "receiver_ack")
        )

    def test_resume_checkpoint_prevents_duplicate_side_effects(self) -> None:
        self.assert_contract_tokens(
            (
                "last_safe_checkpoint",
                "next_safe_action",
                "side_effects_already_applied",
                "idempotency",
            )
        )

    def test_pending_user_decisions_are_explicit_resume_gates(self) -> None:
        self.assert_contract_tokens(
            ("pending_user_decisions", "approval_required_before_resume")
        )

    def test_resume_rehydrates_instruction_and_canon_surfaces(self) -> None:
        self.assert_contract_tokens(
            ("instruction_surface_readback", "AGENTS.md", "CONTEXT_DRIFT_RECHECK_REQUIRED")
        )

    def test_handoff_context_is_curated_not_transcript_dumped(self) -> None:
        self.assert_contract_tokens(("context_sanitation", "raw tool log", "3~7"))


if __name__ == "__main__":
    unittest.main()
