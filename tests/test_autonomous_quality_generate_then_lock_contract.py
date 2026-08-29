from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CUSTOM = ROOT / "templates/custom-instructions.gpt.md"
AUTONOMY = ROOT / "docs/AUTONOMOUS_QUALITY_OPTIMIZATION_AND_LEARNING_POLICY.md"
IMAGE_POLICY = ROOT / "docs/GPT_IMAGE_GENERATION_AND_REVIEW_POLICY.md"
IMAGE_GATE = ROOT / "docs/knowledge/game-development/IMAGE_CONVERSATION_APPROVAL_GATE.md"
RECEIPT = ROOT / "templates/project-operations/ADVERSARIAL_REVIEW_EVIDENCE_RECEIPT.yml"


class AutonomousQualityGenerateThenLockContractTests(unittest.TestCase):
    @staticmethod
    def _read(path: Path) -> str:
        if not path.exists():
            raise AssertionError(f"required owner missing: {path}")
        return path.read_text(encoding="utf-8")

    def test_custom_instructions_are_repository_first_and_stable(self) -> None:
        text = self._read(CUSTOM)
        for token in (
            "REPOSITORY_FIRST_CURRENT_CANON",
            "PAST_CHAT_AND_MEMORY_DISCOVERY_ONLY",
            "PROJECT_INSTRUCTIONS_OVERRIDE_GLOBAL_CUSTOM_INSTRUCTIONS",
            "NO_MUTABLE_SHA_PR_OR_CURRENT_TASK_IN_GLOBAL_CUSTOM_INSTRUCTIONS",
            "AUTONOMOUS_QUALITY_OPTIMIZATION_AND_LEARNING_POLICY.md",
        ):
            self.assertIn(token, text)
        self.assertNotIn("Notion은 사람용 정본", text)
        self.assertNotIn("Google Sheets를 우선", text)

    def test_concrete_visual_need_generates_candidate_before_final_lock(self) -> None:
        for text in (self._read(IMAGE_POLICY), self._read(IMAGE_GATE)):
            for token in (
                "NEED_DRIVEN_GENERATE_THEN_LOCK",
                "CONCRETE_CONSUMER_OR_PLANNING_BOARD_REQUIRED",
                "CURRENT_APPROVED_VISUAL_ANCHOR_READBACK_REQUIRED",
                "GENERATE_ONE_CANDIDATE_BEFORE_LOCK",
                "USER_LOCK_REVISE_REJECT_AFTER_GENERATION",
                "GENERATED_CANDIDATE != USER_LOCKED != PROJECT_ASSET_APPROVED != IMPLEMENTED != RUNTIME_VERIFIED",
                "NO_AUTOMATIC_IMAGE_CHAIN",
            ):
                self.assertIn(token, text)
        self.assertIn(
            "ASSISTANT_INITIATED_VISUAL_NEED_RETAINS_TWO_TURN_GATE__SUPERSEDED",
            self._read(IMAGE_GATE),
        )

    def test_candidate_generation_preserves_visual_and_asset_boundaries(self) -> None:
        policy = self._read(IMAGE_POLICY)
        for token in (
            "ACTUAL_CONSUMER_REQUIRED",
            "APPROVED_VISUAL_DIRECTION_RESOLUTION_REQUIRED",
            "EXISTING_APPROVED_ASSET_REUSE_FIRST",
            "STYLE_CONTINUITY_REVIEW_REQUIRED",
            "IMAGE_MODEL_ONLY_VISUAL_CREATION_POLICY.md",
            "PROJECT_ASSET_APPROVED",
            "SHA-256",
            "provenance",
            "RIGHTS_AND_REFERENCE_REVIEW_REQUIRED",
            "STOP_REQUIRED_AFTER_GENERATION",
        ):
            self.assertIn(token, policy)

    def test_implementation_structure_requires_current_research_and_actual_feasibility(self) -> None:
        for text in (self._read(AUTONOMY), self._read(CUSTOM)):
            for token in (
                "CURRENT_RESEARCH_AND_IMPLEMENTATION_FEASIBILITY_REQUIRED",
                "MINIMUM_MATERIALLY_DISTINCT_ALTERNATIVES: 3",
                "ADOPT / ADAPT / TEST / REJECT",
                "FEASIBLE | PARTIAL | BLOCKED_UNVERIFIED",
                "ACTUAL_PROJECT_BOUNDARY_MAPPING_REQUIRED",
                "RESEARCH_SUMMARY_IS_NOT_IMPLEMENTATION_PROOF",
            ):
                self.assertIn(token, text)

    def test_long_term_quality_is_balanced_against_overengineering(self) -> None:
        for text in (self._read(AUTONOMY), self._read(CUSTOM)):
            for token in (
                "LONG_TERM_EFFICIENCY_AND_COMPLETENESS_FIRST",
                "QUALITY_OVER_RESPONSE_SPEED",
                "TOTAL_LIFECYCLE_COST",
                "NO_UNSUPPORTED_OVERENGINEERING",
                "MINIMUM_NECESSARY_COMPLEXITY",
            ):
                self.assertIn(token, text)

    def test_automation_minimizes_user_intervention_without_bypassing_risk_gates(self) -> None:
        for text in (self._read(AUTONOMY), self._read(CUSTOM)):
            for token in (
                "LOW_INTERVENTION_AUTOMATION_AND_LEARNING_LOOP",
                "SAFE_REVERSIBLE_WORK_CONTINUES_WITHOUT_ROUTINE_REAPPROVAL",
                "USER_DECISION_ONLY_FOR_PRODUCT_MEANING_FINAL_VISUAL_LOCK_OR_HIGH_RISK",
                "FAIL_CLOSED_TO_HUMAN_ON_UNSAFE_OR_CANON_CONFLICT",
                "INCIDENT_SOLUTION_LESSON_TO_AUTOMATION_OR_BASE_PROMOTION",
            ):
                self.assertIn(token, text)

    def test_adversarial_review_requires_actual_evidence_per_full_loop(self) -> None:
        policy = self._read(AUTONOMY)
        receipt = self._read(RECEIPT)
        for token in (
            "CLAIM_ONLY_ADVERSARIAL_REVIEW_INVALID",
            "EVIDENCE_RECEIPT_REQUIRED_PER_FULL_LOOP",
            "EXACT_HEAD_OR_STATE_REQUIRED",
            "ACTUAL_READS_AND_CHECK_RESULTS_REQUIRED",
            "VALIDATED_FINDING_REQUIRES_CORRECTION_OR_EXPLICIT_BLOCKER",
            "MINIMUM_FULL_LOOPS_BEFORE_CLEAN_EXIT: 5",
        ):
            self.assertIn(token, policy)
        for field in (
            "loop_index:",
            "input_exact_head_or_state:",
            "actual_reads:",
            "actual_commands_or_checks:",
            "validated_findings:",
            "corrections_applied:",
            "verification_results:",
            "output_exact_head_or_state:",
            "clean_exit_candidate:",
        ):
            self.assertIn(field, receipt)

    def test_blueprint_final_approval_still_blocks_new_implementation(self) -> None:
        autonomy = self._read(AUTONOMY)
        for token in (
            "BLUEPRINT_PRE_IMPLEMENTATION_REVIEW_GATE",
            "REQUIRED_IMAGE_AND_MATERIAL_PREPARATION",
            "USER_FINAL_REVIEW_APPROVAL",
            "IMPLEMENTATION_AUTHORIZED",
            "GENERATED_CANDIDATE_IS_NOT_IMPLEMENTATION_AUTHORITY",
        ):
            self.assertIn(token, autonomy)


if __name__ == "__main__":
    unittest.main()
