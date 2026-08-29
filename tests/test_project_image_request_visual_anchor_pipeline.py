from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "docs/GPT_IMAGE_GENERATION_AND_REVIEW_POLICY.md"
PIPELINE = (
    ROOT
    / "docs/knowledge/game-development/PROJECT_IMAGE_REQUEST_VISUAL_ANCHOR_PIPELINE.md"
)
GATE = ROOT / "docs/knowledge/game-development/IMAGE_CONVERSATION_APPROVAL_GATE.md"


class ProjectImageRequestVisualAnchorPipelineTests(unittest.TestCase):
    @staticmethod
    def _read(path: Path) -> str:
        if not path.exists():
            raise AssertionError(f"required visual owner missing: {path}")
        return path.read_text(encoding="utf-8")

    def test_explicit_project_image_request_auto_loads_the_pipeline(self) -> None:
        pipeline = self._read(PIPELINE)
        for token in (
            "EXPLICIT_PROJECT_IMAGE_REQUEST_AUTO_PIPELINE",
            "NO_SEPARATE_LONG_IMAGE_INSTRUCTION_REQUIRED",
            "APPROVED_VISUAL_DIRECTION_RESOLUTION_REQUIRED",
            "EXACT_PROJECT_AND_ACTUAL_CONSUMER_REQUIRED",
        ):
            self.assertIn(token, pipeline)

    def test_main_policy_routes_explicit_and_candidate_first_generation(self) -> None:
        policy = self._read(POLICY)
        for token in (
            "PROJECT_IMAGE_REQUEST_VISUAL_ANCHOR_PIPELINE.md",
            "CURRENT_TURN_EXPLICIT_IMAGE_REQUEST",
            "EXPLICIT_REQUEST_IS_ONE_OUTPUT_AUTHORITY",
            "NEEDED_VISUAL_CANDIDATE_MAY_BE_GENERATED_BEFORE_USER_LOCK",
            "GENERATED_CANDIDATE_REQUIRES_POST_GENERATION_USER_DECISION",
            "USER_LOCK_REQUIRED_FOR_CANON_OR_RUNTIME_PROMOTION",
            "NO_AUTOMATIC_IMAGE_CHAIN",
        ):
            self.assertIn(token, policy)

    def test_gate_allows_needed_candidate_before_user_lock(self) -> None:
        gate = self._read(GATE)
        for token in (
            "PROJECT_CANON_AND_EXISTING_VISUAL_READBACK_REQUIRED",
            "ACTUAL_OR_PLANNED_CONSUMER_REQUIRED",
            "VISUAL_NEED_CONFIRMED_DURING_APPROVED_WORK",
            "NEEDED_VISUAL_CANDIDATE_MAY_BE_GENERATED_BEFORE_USER_LOCK",
            "GENERATED_CANDIDATE_REQUIRES_POST_GENERATION_USER_DECISION",
            "USER_LOCK_REQUIRED_FOR_CANON_OR_RUNTIME_PROMOTION",
            "GENERATED_CANDIDATE != USER_APPROVED != CANON_REGISTERED != IMPLEMENTED != RUNTIME_VERIFIED",
            "HOST_PLATFORM_PRECEDENCE",
            "STOP_REQUIRED_AFTER_GENERATION",
        ):
            self.assertIn(token, gate)

    def test_legacy_two_turn_markers_are_explicitly_inactive(self) -> None:
        gate = self._read(GATE)
        policy = self._read(POLICY)
        for text in (gate, policy):
            self.assertIn("LEGACY_SUPERSEDED_ONLY", text)
            self.assertIn("ASSISTANT_INITIATED_VISUAL_NEED_RETAINS_TWO_TURN_GATE", text)
            self.assertIn("TEXT_BRIEF_STOP_REQUIRED", text)
            self.assertIn("NEXT_USER_EXPLICIT_APPROVAL", text)
            self.assertLess(
                text.index("NEEDED_VISUAL_CANDIDATE_MAY_BE_GENERATED_BEFORE_USER_LOCK"),
                text.rindex("LEGACY_SUPERSEDED_ONLY"),
            )

    def test_candidate_promotion_states_remain_separate(self) -> None:
        for text in (self._read(POLICY), self._read(GATE)):
            for token in (
                "GENERATED_CANDIDATE",
                "USER_APPROVED",
                "CANON_REGISTERED",
                "IMPLEMENTED",
                "RUNTIME_VERIFIED",
            ):
                self.assertIn(token, text)
        self.assertIn(
            "GENERATED_CANDIDATE != USER_APPROVED != CANON_REGISTERED != IMPLEMENTED != RUNTIME_VERIFIED",
            self._read(GATE),
        )

    def test_one_consumer_can_request_a_bounded_state_family(self) -> None:
        gate = self._read(GATE)
        self.assertIn("BOUNDED_STATE_FAMILY_ALLOWED_WHEN_CONSUMER_REQUIRES", gate)
        self.assertIn("NO_AUTOMATIC_IMAGE_CHAIN", gate)
        self.assertIn("GENERATE_EXACTLY_ONE", gate)

    def test_existing_approved_anchor_is_shown_and_reused(self) -> None:
        pipeline = self._read(PIPELINE)
        for token in (
            "APPROVED_VISUAL_ANCHOR_FOUND",
            "SURFACE_APPROVED_ANCHOR_TO_USER",
            "ANCHOR_PREVIEW_OR_BINARY_READBACK_REQUIRED",
            "USE_CURRENT_APPROVED_ANCHOR",
            "APPROVED_VISUAL_REFERENCE",
        ):
            self.assertIn(token, pipeline)

    def test_missing_anchor_routes_to_one_comparison_deliverable_before_production(self) -> None:
        pipeline = self._read(PIPELINE)
        for token in (
            "NO_USABLE_APPROVED_VISUAL_ANCHOR",
            "GENERATE_CONCEPT_OPTION_COMPARISON",
            "CONCEPT_COMPARISON_IS_GENERATED_EXPLORATION",
            "COMPARISON_BOARD_ONE_DELIVERABLE",
            "THREE_MATERIALLY_DISTINCT_VISUAL_OPTIONS",
            "USER_SELECTS_ONE_DIRECTION_BEFORE_PRODUCTION",
        ):
            self.assertIn(token, pipeline)

    def test_selected_direction_becomes_a_bounded_continuity_packet(self) -> None:
        pipeline = self._read(PIPELINE)
        for token in (
            "VISUAL_DIRECTION_LOCK_PACKET",
            "global_style_anchor:",
            "surface_layer_anchor:",
            "flow_screen_context:",
            "keep:",
            "avoid:",
            "do_not_drift:",
            "superseded_reference_ids:",
        ):
            self.assertIn(token, pipeline)

    def test_conflict_and_inaccessible_anchor_fail_closed(self) -> None:
        pipeline = self._read(PIPELINE)
        for token in (
            "MULTIPLE_CURRENT_VISUAL_ANCHORS_CONFLICT",
            "APPROVED_ANCHOR_BINARY_UNREADABLE",
            "VISUAL_CANONICAL_CONFLICT",
            "BLOCKED_UNVERIFIED",
        ):
            self.assertIn(token, pipeline)

    def test_production_results_are_reviewed_for_style_and_flow_consistency(self) -> None:
        pipeline = self._read(PIPELINE)
        for token in (
            "STYLE_CONTINUITY_REVIEW_REQUIRED",
            "FLOW_AND_SCREEN_SEMANTIC_CONSISTENCY_REQUIRED",
            "NO_UNAPPROVED_STYLE_DRIFT",
            "OBJECTIVE_DEFECT_CORRECTION_WITHIN_APPROVED_DELIVERABLE",
            "GENERATED_EXPLORATION != PROJECT_ASSET_APPROVED != RUNTIME_PROMOTED",
        ):
            self.assertIn(token, pipeline)

    def test_comparison_sheet_is_not_a_runtime_asset(self) -> None:
        pipeline = self._read(PIPELINE)
        self.assertIn("COMPARISON_SHEET_NOT_PRODUCTION_ASSET", pipeline)
        self.assertIn("SELECTED_DIRECTION_REQUIRES_STANDALONE_ANCHOR", pipeline)
        self.assertIn("PROJECT_ASSET_APPROVED", pipeline)

    def test_existing_specialist_owners_are_composed_not_replaced(self) -> None:
        pipeline = self._read(PIPELINE)
        for owner in (
            "GPT_IMAGE_GENERATION_AND_REVIEW_POLICY.md",
            "ART_DIRECTION_AND_ASSET_PLANNING_GUIDE.md",
            "notion-project-visual-continuity-gate.md",
            "candidate-review-and-reusable-harvest.md",
            "NOTION_VISUAL_ASSET_AND_FLOW_WORKFLOW.md",
        ):
            self.assertIn(owner, pipeline)
        self.assertIn("THIN_PIPELINE_NOT_SECOND_VISUAL_CANON", pipeline)


if __name__ == "__main__":
    unittest.main()
