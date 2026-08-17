from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CLAIM_REFERENCE = (
    ROOT
    / "skills"
    / "reviewing-and-validating-project-changes"
    / "references"
    / "claim-and-intent-verification.md"
)
FRESHNESS_SKILL = ROOT / "skills" / "auditing-canonical-reference-freshness" / "SKILL.md"
LEARNING_LOG = ROOT / "skills" / "SKILL_LEARNING_LOG.md"
LOCAL_EXECUTOR_DOC = ROOT / "docs" / "LOOP_A2_LOCAL_EXECUTOR.md"


class UniversalLoopV1ClosureLearningReuseTests(unittest.TestCase):
    def test_claim_verification_reuses_exact_closure_evidence_rules(self) -> None:
        reference = CLAIM_REFERENCE.read_text(encoding="utf-8")
        for marker in (
            "MACHINE_EVIDENCE_CORRECTION",
            "TEST_CONSUMPTION_PROOF",
            "LATEST_EXACT_HEAD_ONLY",
            "BOUNDED_ZERO_ESCAPE",
            "workflow trigger",
            "receipt digest",
            "stale-head",
        ):
            self.assertIn(marker, reference)
        self.assertIn("summary", reference.lower())
        self.assertIn("실행 증거가 아니다", reference)

    def test_reference_freshness_rechecks_mutable_successor_consumers(self) -> None:
        skill = FRESHNESS_SKILL.read_text(encoding="utf-8")
        for marker in (
            "VERIFIED_SUCCESSOR_STATE",
            "PREDECESSOR_CEILING_FREEZE",
            "CURRENT_MUTABLE",
            "HISTORICAL_DISCOVERY",
        ):
            self.assertIn(marker, skill)
        self.assertIn("NOT_RUN", skill)
        self.assertIn("0", skill)
        self.assertIn("historical", skill.lower())

    def test_learning_log_records_the_real_v1_closure_pattern(self) -> None:
        learning = LEARNING_LOG.read_text(encoding="utf-8")
        self.assertIn("2026-08-17 — Universal Loop v1 closure evidence hardening", learning)
        for marker in (
            "MACHINE_EVIDENCE_CORRECTION",
            "TEST_CONSUMPTION_PROOF",
            "VERIFIED_SUCCESSOR_STATE",
            "LATEST_EXACT_HEAD_ONLY",
            "BOUNDED_ZERO_ESCAPE",
        ):
            self.assertIn(marker, learning)
        self.assertIn("#489", learning)
        self.assertIn("#490", learning)
        self.assertIn("#491", learning)
        self.assertIn("#492", learning)
        self.assertIn("#494", learning)

    def test_active_local_executor_doc_matches_completed_machine_checkpoint(self) -> None:
        doc = LOCAL_EXECUTOR_DOC.read_text(encoding="utf-8")
        for marker in (
            "live_v4_user_pc_preflight: PASS",
            "real_local_chatgpt_codex_call: PASS",
            "blacksmith_real_burnin_runs: 3",
            "f4deebfc06de828cc956e47220e829cd98b1eb09",
            "6b241f28969410de78156c90cc10f33a067426a2",
            "BS_A2_DIAG_20260817_005",
            "BS_A2_BURNIN_001_R1",
            "BS_A2_BURNIN_001_R2",
            "BS_A2_BURNIN_001_R3",
            "2b8856054573f1a06297ac8e65f5ca009fa2daef",
        ):
            self.assertIn(marker, doc)
        current_section = doc.split("## Queue job", 1)[0]
        self.assertNotIn("live_v4_user_pc_preflight: NOT_RUN", current_section)
        self.assertNotIn("real_local_chatgpt_codex_call: NOT_COMPLETED", current_section)
        self.assertNotIn("blacksmith_real_burnin_runs: 0", current_section)

    def test_preserved_boundaries_remain_explicit(self) -> None:
        claim = CLAIM_REFERENCE.read_text(encoding="utf-8")
        local = LOCAL_EXECUTOR_DOC.read_text(encoding="utf-8")
        self.assertIn("A3", local)
        self.assertIn("Scheduler", local)
        self.assertIn("paid OpenAI API", local)
        self.assertIn("Evidence ceiling", claim)


if __name__ == "__main__":
    unittest.main()
