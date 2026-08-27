from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTRACT = (
    ROOT
    / "docs/knowledge/game-development/VISUAL_CONCEPT_EXPLORATION_AND_CONTINUITY_LOCK.md"
)
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

    def test_visual_continuity_gate_routes_the_new_composed_contract(self) -> None:
        text = self._read(CONTINUITY_GATE)
        self.assertIn("VISUAL_CONCEPT_EXPLORATION_AND_CONTINUITY_LOCK.md", text)
        self.assertIn("VISUAL_DIRECTION_EXPLORATION_BEFORE_SCALE", text)
        self.assertIn("APPROVED_VISUAL_DIRECTION_PACKET", text)

    def test_contract_composes_current_owners_instead_of_replacing_them(self) -> None:
        text = self._read(CONTRACT)
        for owner in (
            "docs/GPT_IMAGE_GENERATION_AND_REVIEW_POLICY.md",
            "ART_DIRECTION_AND_ASSET_PLANNING_GUIDE.md",
            "IMAGE_CONVERSATION_APPROVAL_GATE.md",
            "candidate-review-and-reusable-harvest.md",
            "notion-project-visual-continuity-gate.md",
            "WORK_PROJECT_LOCAL_VISUAL_ASSET_DELIVERY_PROFILE.md",
        ):
            self.assertIn(owner, text)
        self.assertIn("THIN_CONTRACT_NOT_SECOND_ART_BIBLE", text)

    def test_contract_requires_explore_select_lock_then_scale(self) -> None:
        text = self._read(CONTRACT)
        stages = (
            "CONCEPT_OPTIONS_BEFORE_PRODUCTION_LOCK",
            "USER_SELECTED_VISUAL_DIRECTION_REQUIRED",
            "APPROVED_VISUAL_DIRECTION_PACKET",
            "CONSISTENCY_REVIEW_AGAINST_VISUAL_DIRECTION_LOCK",
        )
        for token in (
            "VISUAL_DIRECTION_EXPLORATION_BEFORE_SCALE",
            "MINIMUM_VIABLE_CONCEPT_DIRECTIONS: 3",
            "NO_FAKE_CONCEPT_OPTION",
            "SAME_CONSUMER_CONTROLLED_COMPARISON",
            "FLOW_AND_SCREEN_ANCHORS_LOCKED_BEFORE_SCALE",
            "ALLOWED_VARIATION_WITHOUT_UNAUTHORIZED_STYLE_DRIFT",
            *stages,
        ):
            self.assertIn(token, text)
        self.assertEqual([text.index(s) for s in stages], sorted(text.index(s) for s in stages))

    def test_comparison_board_is_one_explicit_exploration_result_not_runtime_asset_compression(self) -> None:
        text = self._read(CONTRACT)
        gate = self._read(APPROVAL_GATE)
        combined = text + "\n" + gate
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

    def test_selection_and_visual_direction_packets_record_decision_and_continuity(self) -> None:
        text = self._read(CONTRACT)
        for token in (
            "CONCEPT_DIRECTION_SELECTION",
            "selected_candidate_id:",
            "adopted_elements:",
            "rejected_elements:",
            "selection_reason:",
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
        ):
            self.assertIn(token, text)

    def test_existing_candidate_and_continuity_owners_remain_inputs(self) -> None:
        candidate = self._read(CANDIDATE_REVIEW)
        continuity = self._read(CONTINUITY_GATE)
        for token in (
            "canon / approved-reference fit",
            "actual-use readability",
            "APPROVED_CANDIDATE",
        ):
            self.assertIn(token, candidate)
        for token in (
            "APPROVED_VISUAL_REFERENCE",
            "Keep",
            "Avoid",
            "Do Not Drift",
        ):
            self.assertIn(token, continuity)

    def test_contract_maps_lock_identity_into_existing_local_visual_packet(self) -> None:
        contract = self._read(CONTRACT)
        profile = self._read(LOCAL_VISUAL_PROFILE)
        for field in (
            "approved_reference_or_style_anchor:",
            "notion_reference_surface:",
            "objective_acceptance:",
            "runtime_validation:",
        ):
            self.assertIn(field, profile)
            self.assertIn(field, contract)
        for token in (
            "visual_direction_lock_id",
            "approved_flow_or_screen_anchor_ids",
            "runtime_consistency_validation",
        ):
            self.assertIn(token, contract)

    def test_exploration_approval_and_runtime_promotion_remain_separate(self) -> None:
        text = self._read(CONTRACT)
        image_policy = self._read(IMAGE_POLICY)
        combined = text + "\n" + image_policy
        for token in (
            "GENERATED_EXPLORATION",
            "APPROVED_CANDIDATE",
            "PROJECT_ASSET_APPROVED",
            "APPLIED_AND_RUNTIME_VERIFIED",
        ):
            self.assertIn(token, combined)
        self.assertIn("comparison board", text)
        self.assertIn("not runtime evidence", text)

    def test_material_direction_or_flow_change_reopens_only_affected_visual_scope(self) -> None:
        text = self._read(CONTRACT)
        for token in (
            "VISUAL_DIRECTION_OR_FLOW_DRIFT_REVALIDATION_REQUIRED",
            "EARLIEST_AFFECTED_VISUAL_SCOPE_REOPENS",
            "NO_FULL_PROJECT_VISUAL_RESTART_FOR_LOCAL_DRIFT",
        ):
            self.assertIn(token, text)


if __name__ == "__main__":
    unittest.main()
