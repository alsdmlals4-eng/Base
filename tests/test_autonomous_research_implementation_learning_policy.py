from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "docs/AUTONOMOUS_RESEARCH_IMPLEMENTATION_AND_LEARNING_POLICY.md"
CUSTOM = ROOT / "templates/custom-instructions.gpt.md"
IMAGE_POLICY = ROOT / "docs/GPT_IMAGE_GENERATION_AND_REVIEW_POLICY.md"
IMAGE_GATE = ROOT / "docs/knowledge/game-development/IMAGE_CONVERSATION_APPROVAL_GATE.md"


class AutonomousResearchImplementationLearningPolicyTests(unittest.TestCase):
    @staticmethod
    def _read(path: Path) -> str:
        if not path.exists():
            raise AssertionError(f"required policy missing: {path}")
        return path.read_text(encoding="utf-8")

    def test_policy_defines_research_to_feasibility_and_implementation(self) -> None:
        text = self._read(POLICY)
        for token in (
            "TARGETED_CURRENT_RESEARCH_REQUIRED",
            "OFFICIAL_PRIMARY_SOURCE_FIRST",
            "INDUSTRY_SUCCESS_FAILURE_COMPARISON",
            "ADOPT_ADAPT_REJECT_REQUIRED",
            "CURRENT_IMPLEMENTATION_READBACK_REQUIRED",
            "IMPLEMENTATION_FEASIBILITY_PACKET_REQUIRED",
            "FEASIBLE | PARTIAL | BLOCKED_UNVERIFIED",
            "SPEC_ONLY_IS_NOT_IMPLEMENTATION_PROOF",
            "AUTHORIZED_SCOPE_CONTINUES_TO_IMPLEMENTATION",
        ):
            self.assertIn(token, text)
        self.assertLess(
            text.index("current project authority / actual implementation / open PR readback"),
            text.index("targeted current official / primary-source Internet research"),
        )
        self.assertLess(
            text.index("targeted current official / primary-source Internet research"),
            text.index("actual project feasibility packet"),
        )

    def test_policy_prioritizes_long_term_quality_without_overengineering(self) -> None:
        text = self._read(POLICY)
        for token in (
            "LONG_TERM_TOTAL_COST_OVER_LOCAL_SPEED",
            "MINIMUM_COMPLEXITY_WITH_DURABLE_QUALITY",
            "NO_SPECULATIVE_OVERENGINEERING",
            "현재 필요를 충족하는 최소 복잡도 + 검증 가능한 장기 확장점",
        ):
            self.assertIn(token, text)

    def test_policy_minimizes_user_intervention_but_preserves_real_gates(self) -> None:
        text = self._read(POLICY)
        for token in (
            "MINIMIZE_USER_INTERVENTION",
            "AUTONOMOUS_SAFE_CONTINUATION",
            "USER_DECISION_ONLY_FOR_MEANING_LOCK_OR_HIGH_RISK",
            "최종 Visual Direction 또는 제품 자산 lock",
            "되돌리기 어려운 삭제·migration",
        ):
            self.assertIn(token, text)

    def test_learning_is_durable_repository_system_not_claimed_model_training(self) -> None:
        text = self._read(POLICY)
        for token in (
            "DURABLE_LEARNING_LOOP_REQUIRED",
            "AUTOMATION_IS_PERSISTENT_SYSTEM_NOT_MODEL_SELF_TRAINING",
            "PROBLEM_TO_ROOT_CAUSE_TO_FIX_TO_REGRESSION_GUARD",
            "PROJECT_LESSON_BEFORE_BASE_PROMOTION",
            "NO_NEW_LEARNING_CHURN_WITHOUT_REUSABLE_EVIDENCE",
            "모델이 대화만으로 영구 학습한다는 뜻이 아니다",
        ):
            self.assertIn(token, text)

    def test_candidate_first_image_contract_is_shared_across_owners(self) -> None:
        texts = (
            self._read(POLICY),
            self._read(CUSTOM),
            self._read(IMAGE_POLICY),
            self._read(IMAGE_GATE),
        )
        for text in texts:
            self.assertIn(
                "NEEDED_VISUAL_CANDIDATE_MAY_BE_GENERATED_BEFORE_USER_LOCK",
                text,
            )
            self.assertIn(
                "USER_LOCK_REQUIRED_FOR_CANON_OR_RUNTIME_PROMOTION",
                text,
            )

    def test_custom_instructions_are_repository_first_and_feasibility_driven(self) -> None:
        text = self._read(CUSTOM)
        for token in (
            "repository-first",
            "targeted fresh-read",
            "최신 공식/1차 자료",
            "FEASIBLE / PARTIAL / BLOCKED_UNVERIFIED",
            "장기 총비용",
            "자동화·최적화·학습 시스템",
            "생성됨 ≠ 사용자 승인 ≠ 정본 등록 ≠ 구현 ≠ runtime 검증",
        ):
            self.assertIn(token, text)
        self.assertNotIn(
            "이미지 생성·편집은 내가 명시적으로 요청했을 때만 진행한다",
            text,
        )

    def test_blueprint_candidate_preparation_does_not_authorize_runtime_implementation(self) -> None:
        for text in (self._read(POLICY), self._read(CUSTOM), self._read(IMAGE_POLICY), self._read(IMAGE_GATE)):
            self.assertIn("Blueprint", text)
        self.assertIn(
            "Blueprint 최종 승인을 요구하는 implementation package는 승인 전 runtime 구현으로 넘어가지 않는다",
            self._read(IMAGE_GATE),
        )


if __name__ == "__main__":
    unittest.main()
