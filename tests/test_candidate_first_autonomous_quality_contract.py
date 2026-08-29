from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GATE = ROOT / "docs/knowledge/game-development/IMAGE_CONVERSATION_APPROVAL_GATE.md"
POLICY = ROOT / "docs/GPT_IMAGE_GENERATION_AND_REVIEW_POLICY.md"
PIPELINE = (
    ROOT
    / "docs/knowledge/game-development/PROJECT_IMAGE_REQUEST_VISUAL_ANCHOR_PIPELINE.md"
)
CUSTOM = ROOT / "templates/custom-instructions.gpt.md"
V49 = ROOT / "templates/project-operations/CHATGPT_WORK_PROJECT_EXECUTION_INSTRUCTION_v4.9.md"
BLUEPRINT = ROOT / "docs/PROJECT_MASTER_GDD_TWO_ARTIFACT_POLICY.md"


class CandidateFirstAutonomousQualityContractTests(unittest.TestCase):
    @staticmethod
    def _read(path: Path) -> str:
        if not path.exists():
            raise AssertionError(f"required contract owner missing: {path}")
        return path.read_text(encoding="utf-8")

    def test_candidate_first_visual_route_is_active_across_current_owners(self) -> None:
        gate = self._read(GATE)
        policy = self._read(POLICY)
        pipeline = self._read(PIPELINE)
        bundle = "\n".join((gate, policy, pipeline))

        for token in (
            "CANDIDATE_FIRST_VISUAL_PRODUCTION",
            "VISUAL_NEED_CONFIRMED",
            "CURRENT_PROJECT_AND_VISUAL_CANON_READBACK",
            "ACTUAL_OR_EXPLICITLY_PLANNED_CONSUMER_REQUIRED",
            "EXISTING_APPROVED_ASSET_AND_CANDIDATE_REUSE_CHECK",
            "CANDIDATE_GENERATION_PREAUTHORIZED_AFTER_PROJECT_REVIEW",
            "IMAGE_MODEL_GENERATES_ONE_CANDIDATE",
            "PRESENT_FOR_USER_FINAL_LOCK",
            "NO_AUTOMATIC_SCOPE_EXPANSION",
        ):
            self.assertIn(token, bundle)

        self.assertIn("CANDIDATE_FIRST_VISUAL_PRODUCTION", gate)
        self.assertIn("CANDIDATE_FIRST_VISUAL_PRODUCTION", policy)
        self.assertIn("CANDIDATE_FIRST_VISUAL_PRODUCTION", pipeline)

    def test_generation_final_lock_canon_implementation_and_runtime_are_separate(self) -> None:
        bundle = "\n".join(
            (self._read(GATE), self._read(POLICY), self._read(PIPELINE), self._read(CUSTOM))
        )
        for token in (
            "NEEDED",
            "BRIEF_READY",
            "GENERATED_CANDIDATE",
            "USER_FINAL_LOCKED",
            "CANON_REGISTERED",
            "IMPLEMENTED",
            "RUNTIME_VERIFIED",
            "GENERATED_CANDIDATE != USER_FINAL_LOCKED",
            "USER_FINAL_LOCKED != PROJECT_ASSET_APPROVED",
            "CANDIDATE_PRODUCTION_IS_NOT_IMPLEMENTATION_AUTHORITY",
        ):
            self.assertIn(token, bundle)

    def test_old_assistant_two_turn_preapproval_gate_is_retired_not_active(self) -> None:
        gate = self._read(GATE)
        policy = self._read(POLICY)
        v49 = self._read(V49)
        bundle = "\n".join((gate, policy, v49))

        for token in (
            "RETIRED_COMPATIBILITY_ALIAS",
            "ASSISTANT_INITIATED_VISUAL_NEED_RETAINS_TWO_TURN_GATE",
            "TEXT_BRIEF_STOP_REQUIRED",
        ):
            self.assertIn(token, bundle)

        self.assertNotIn(
            "TEXT_BRIEF → STOP_REQUIRED → NEXT_USER_EXPLICIT_APPROVAL → GENERATE_EXACTLY_ONE",
            gate + "\n" + policy,
        )
        self.assertNotIn(
            "assistant가 먼저 이미지 필요성을 제안한 경우에는 그 제안만으로 생성하지 않는다",
            gate + "\n" + policy,
        )

    def test_custom_instructions_are_repository_first_and_remove_stale_notion_authority(self) -> None:
        custom = self._read(CUSTOM)
        for token in (
            "REPOSITORY_PRIMARY_CANON",
            "NOTION_LEGACY_MIGRATION_ONLY",
            "GOOGLE_SHEETS_MIGRATION_ONLY",
            "CANDIDATE_FIRST_VISUAL_PRODUCTION",
            "MINIMIZE_USER_INTERVENTION_WITH_SAFE_FINAL_CONTROL",
        ):
            self.assertIn(token, custom)

        for stale in (
            "GitHub·Notion·AI 협업으로 관리",
            "Notion은 사람이 읽고 비교·수정하는",
            "해당 프로젝트 저장소와 연결된 Notion에서 필요한 최신 정본",
            "필요한 GitHub/Notion 정본에 동기화",
            "이미지 생성·편집은 내가 명시적으로 요청했을 때만 진행",
        ):
            self.assertNotIn(stale, custom)

    def test_material_decisions_require_current_research_and_actual_feasibility(self) -> None:
        custom = self._read(CUSTOM)
        v49 = self._read(V49)
        bundle = custom + "\n" + v49
        for token in (
            "IMPLEMENTATION_FEASIBILITY_BEFORE_COMMITMENT",
            "CURRENT_OFFICIAL_PRIMARY_RESEARCH_REQUIRED",
            "DIRECTLY_RELEVANT_FIELD_EVIDENCE_REQUIRED",
            "ACTUAL_PROJECT_STRUCTURE_FEASIBILITY_REQUIRED",
            "FEASIBLE | PARTIAL | BLOCKED_UNVERIFIED",
            "MECHANICAL_NO_EXTERNAL_DEPENDENCY",
        ):
            self.assertIn(token, bundle)

    def test_long_term_quality_rejects_both_local_shortcuts_and_overengineering(self) -> None:
        custom = self._read(CUSTOM)
        v49 = self._read(V49)
        bundle = custom + "\n" + v49
        for token in (
            "LONG_TERM_QUALITY_OVER_LOCAL_SPEED",
            "ROOT_CAUSE_AND_REUSE_BEFORE_REPEATED_MANUAL_PATCH",
            "MINIMUM_SUFFICIENT_COMPLEXITY",
            "SPECULATIVE_OVERENGINEERING_REJECTED",
            "PLAYABLE_OR_OPERATIONAL_VALUE_OVER_DOCUMENT_VOLUME",
        ):
            self.assertIn(token, bundle)

    def test_post_change_adversarial_review_requires_actual_evidence_and_correction(self) -> None:
        custom = self._read(CUSTOM)
        v49 = self._read(V49)
        bundle = custom + "\n" + v49
        for token in (
            "ACTUAL_POST_COMPLETION_ADVERSARIAL_REVIEW_REQUIRED",
            "FULL_LOOP_COUNT_MINIMUM: 5",
            "EXECUTION_EVIDENCE_REQUIRED",
            "CORRECT_VALIDATED_FINDINGS",
            "CLEAN_REVIEW_EXIT",
            "NO_REVIEW_COMPLETION_CLAIM_WITHOUT_EVIDENCE",
        ):
            self.assertIn(token, bundle)

    def test_automation_learning_loop_preserves_safe_user_control(self) -> None:
        custom = self._read(CUSTOM)
        v49 = self._read(V49)
        bundle = custom + "\n" + v49
        for token in (
            "MINIMIZE_USER_INTERVENTION_WITH_SAFE_FINAL_CONTROL",
            "INCIDENT_SOLUTION_LESSON_AUTOMATION_LOOP",
            "problem → reproducible evidence → root cause",
            "regression prevention",
            "Base BCP",
            "USER_FINAL_LOCKED",
        ):
            self.assertIn(token, bundle)

    def test_candidate_generation_does_not_bypass_blueprint_implementation_approval(self) -> None:
        blueprint = self._read(BLUEPRINT)
        gate = self._read(GATE)
        policy = self._read(POLICY)
        bundle = blueprint + "\n" + gate + "\n" + policy
        for token in (
            "NO_IMPLEMENTATION_BEFORE_USER_FINAL_APPROVAL",
            "CANDIDATE_PRODUCTION_MAY_PRECEDE_BLUEPRINT_FINAL_REVIEW",
            "CANDIDATE_PRODUCTION_IS_NOT_IMPLEMENTATION_AUTHORITY",
            "USER_FINAL_REVIEW_APPROVAL_REQUIRED",
        ):
            self.assertIn(token, bundle)


if __name__ == "__main__":
    unittest.main()
