from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
IMAGE_POLICY = ROOT / "docs/GPT_IMAGE_GENERATION_AND_REVIEW_POLICY.md"
APPROVAL_GATE = ROOT / "docs/knowledge/game-development/IMAGE_CONVERSATION_APPROVAL_GATE.md"
ART_GUIDE = ROOT / "docs/knowledge/game-development/ART_DIRECTION_AND_ASSET_PLANNING_GUIDE.md"
CONTINUITY_GATE = (
    ROOT
    / "skills/designing-art-prompts-and-technique-cards/references/notion-project-visual-continuity-gate.md"
)
CANDIDATE_REVIEW = (
    ROOT
    / "skills/designing-art-prompts-and-technique-cards/references/candidate-review-and-reusable-harvest.md"
)
LOCAL_VISUAL_PROFILE = (
    ROOT / "templates/project-operations/WORK_PROJECT_LOCAL_VISUAL_ASSET_DELIVERY_PROFILE.md"
)


class VisualConceptExplorationAndContinuityLockTests(unittest.TestCase):
    @staticmethod
    def _read(path: Path) -> str:
        if not path.exists():
            raise AssertionError(f"required visual owner missing: {path}")
        return path.read_text(encoding="utf-8")

    def test_existing_art_direction_guide_remains_the_exploration_owner(self) -> None:
        text = self._read(ART_GUIDE)
        for token in (
            "## 7. Concept Exploration",
            "서로 다른 방향 3개 안팎",
            "동일 구도·조건 비교",
            "## 8. Concept → Art Bible → Asset Specification",
        ):
            self.assertIn(token, text)

    def test_image_policy_requires_explore_select_lock_then_scale(self) -> None:
        text = self._read(IMAGE_POLICY)
        for token in (
            "VISUAL_DIRECTION_EXPLORATION_BEFORE_SCALE",
            "CONCEPT_OPTIONS_BEFORE_PRODUCTION_LOCK",
            "MINIMUM_VIABLE_CONCEPT_DIRECTIONS: 3",
            "NO_FAKE_CONCEPT_OPTION",
            "SAME_CONSUMER_CONTROLLED_COMPARISON",
            "USER_SELECTED_VISUAL_DIRECTION_REQUIRED",
            "APPROVED_VISUAL_DIRECTION_PACKET",
            "FLOW_AND_SCREEN_ANCHORS_LOCKED_BEFORE_SCALE",
            "CONSISTENCY_REVIEW_AGAINST_VISUAL_DIRECTION_LOCK",
            "ALLOWED_VARIATION_WITHOUT_UNAUTHORIZED_STYLE_DRIFT",
        ):
            self.assertIn(token, text)
        self.assertLess(
            text.index("CONCEPT_OPTIONS_BEFORE_PRODUCTION_LOCK"),
            text.index("USER_SELECTED_VISUAL_DIRECTION_REQUIRED"),
        )
        self.assertLess(
            text.index("USER_SELECTED_VISUAL_DIRECTION_REQUIRED"),
            text.index("CONSISTENCY_REVIEW_AGAINST_VISUAL_DIRECTION_LOCK"),
        )

    def test_comparison_board_is_one_explicit_exploration_result_not_runtime_asset_compression(self) -> None:
        policy = self._read(IMAGE_POLICY)
        gate = self._read(APPROVAL_GATE)
        combined = policy + "\n" + gate
        for token in (
            "EXPLICIT_CONCEPT_COMPARISON_BOARD",
            "ONE_EXPLORATION_BOARD_NOT_N_RUNTIME_DELIVERABLES",
            "CONCEPT_COMPARISON_BOARD_IS_EXPLORATION_NOT_RUNTIME_ASSET",
            "CONTROLLED_VARIABLE_COMPARISON_REQUIRED",
            "GENERATE_EXACTLY_ONE",
            "TEXT_BRIEF_STOP_REQUIRED",
            "NEXT_USER_EXPLICIT_APPROVAL",
        ):
            self.assertIn(token, combined)
        self.assertIn("explicit comparison artifact", combined)
        self.assertIn("independent runtime asset", combined)

    def test_candidate_selection_records_adopted_rejected_and_lock_output(self) -> None:
        text = self._read(CANDIDATE_REVIEW)
        for token in (
            "CONCEPT_DIRECTION_SELECTION",
            "selected_candidate_id:",
            "adopted_elements:",
            "rejected_elements:",
            "selection_reason:",
            "allowed_variation:",
            "visual_direction_lock_output:",
        ):
            self.assertIn(token, text)

    def test_visual_continuity_gate_carries_direction_and_flow_anchors(self) -> None:
        text = self._read(CONTINUITY_GATE)
        for token in (
            "APPROVED_VISUAL_DIRECTION_PACKET",
            "visual_direction_lock_id:",
            "source_candidate_ids:",
            "approved_flow_or_screen_anchor_ids:",
            "mood_and_emotion:",
            "style_and_rendering_language:",
            "palette_value_material_lighting:",
            "camera_framing_density:",
            "keep:",
            "avoid:",
            "do_not_drift:",
            "allowed_variation:",
            "VISUAL_DIRECTION_OR_FLOW_DRIFT_REVALIDATION_REQUIRED",
        ):
            self.assertIn(token, text)

    def test_local_visual_packet_delivers_lock_identity_to_codex_and_runtime_review(self) -> None:
        text = self._read(LOCAL_VISUAL_PROFILE)
        packet = text.split("### 4.1 Visual production packet override", 1)[1].split(
            "### 4.2 Manifest 최소 필드", 1
        )[0]
        for field in (
            "visual_direction_lock_id:",
            "approved_flow_or_screen_anchor_ids:",
            "approved_reference_or_style_anchor:",
            "continuity_acceptance:",
            "runtime_consistency_validation:",
        ):
            self.assertIn(field, packet)

    def test_exploration_approval_and_runtime_promotion_remain_separate(self) -> None:
        combined = "\n".join(
            (
                self._read(IMAGE_POLICY),
                self._read(CONTINUITY_GATE),
                self._read(LOCAL_VISUAL_PROFILE),
            )
        )
        for token in (
            "GENERATED_EXPLORATION",
            "APPROVED_CANDIDATE",
            "PROJECT_ASSET_APPROVED",
            "APPLIED_AND_RUNTIME_VERIFIED",
        ):
            self.assertIn(token, combined)
        self.assertIn("comparison board", combined)
        self.assertIn("not runtime evidence", combined)


if __name__ == "__main__":
    unittest.main()
