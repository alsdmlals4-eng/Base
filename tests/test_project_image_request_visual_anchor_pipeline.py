from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "docs/GPT_IMAGE_GENERATION_AND_REVIEW_POLICY.md"
GATE = ROOT / "docs/knowledge/game-development/IMAGE_CONVERSATION_APPROVAL_GATE.md"
CONTINUITY = (
    ROOT
    / "skills/designing-art-prompts-and-technique-cards/references/notion-project-visual-continuity-gate.md"
)
CANDIDATE = (
    ROOT
    / "skills/designing-art-prompts-and-technique-cards/references/candidate-review-and-reusable-harvest.md"
)


class ProjectImageRequestVisualAnchorPipelineTests(unittest.TestCase):
    @staticmethod
    def _read(path: Path) -> str:
        if not path.exists():
            raise AssertionError(f"required visual owner missing: {path}")
        return path.read_text(encoding="utf-8")

    def test_explicit_project_image_request_auto_loads_the_pipeline(self) -> None:
        policy = self._read(POLICY)
        for token in (
            "EXPLICIT_PROJECT_IMAGE_REQUEST_AUTO_PIPELINE",
            "NO_SEPARATE_LONG_IMAGE_INSTRUCTION_REQUIRED",
            "APPROVED_VISUAL_DIRECTION_RESOLUTION_REQUIRED",
            "EXACT_PROJECT_AND_ACTUAL_CONSUMER_REQUIRED",
        ):
            self.assertIn(token, policy)

    def test_current_turn_explicit_request_has_a_direct_one_output_route(self) -> None:
        gate = self._read(GATE)
        for token in (
            "CURRENT_TURN_EXPLICIT_IMAGE_REQUEST",
            "EXPLICIT_REQUEST_IS_ONE_OUTPUT_AUTHORITY",
            "ASSISTANT_INITIATED_VISUAL_NEED_RETAINS_TWO_TURN_GATE",
            "HOST_PLATFORM_PRECEDENCE",
            "STOP_REQUIRED_AFTER_GENERATION",
        ):
            self.assertIn(token, gate)

    def test_existing_approved_anchor_is_shown_and_reused(self) -> None:
        combined = self._read(POLICY) + "\n" + self._read(CONTINUITY)
        for token in (
            "APPROVED_VISUAL_ANCHOR_FOUND",
            "SURFACE_APPROVED_ANCHOR_TO_USER",
            "ANCHOR_PREVIEW_OR_BINARY_READBACK_REQUIRED",
            "USE_CURRENT_APPROVED_ANCHOR",
            "APPROVED_VISUAL_REFERENCE",
        ):
            self.assertIn(token, combined)

    def test_missing_anchor_routes_to_one_comparison_deliverable_before_production(self) -> None:
        combined = self._read(POLICY) + "\n" + self._read(CANDIDATE)
        for token in (
            "NO_USABLE_APPROVED_VISUAL_ANCHOR",
            "GENERATE_CONCEPT_OPTION_COMPARISON",
            "CONCEPT_COMPARISON_IS_GENERATED_EXPLORATION",
            "COMPARISON_BOARD_ONE_DELIVERABLE",
            "THREE_MATERIALLY_DISTINCT_VISUAL_OPTIONS",
            "USER_SELECTS_ONE_DIRECTION_BEFORE_PRODUCTION",
        ):
            self.assertIn(token, combined)

    def test_selected_direction_becomes_a_bounded_continuity_packet(self) -> None:
        continuity = self._read(CONTINUITY)
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
            self.assertIn(token, continuity)

    def test_conflict_and_inaccessible_anchor_fail_closed(self) -> None:
        continuity = self._read(CONTINUITY)
        for token in (
            "MULTIPLE_CURRENT_VISUAL_ANCHORS_CONFLICT",
            "APPROVED_ANCHOR_BINARY_UNREADABLE",
            "VISUAL_CANONICAL_CONFLICT",
            "BLOCKED_UNVERIFIED",
        ):
            self.assertIn(token, continuity)

    def test_production_results_are_reviewed_for_style_and_flow_consistency(self) -> None:
        combined = self._read(POLICY) + "\n" + self._read(CONTINUITY)
        for token in (
            "STYLE_CONTINUITY_REVIEW_REQUIRED",
            "FLOW_AND_SCREEN_SEMANTIC_CONSISTENCY_REQUIRED",
            "NO_UNAPPROVED_STYLE_DRIFT",
            "OBJECTIVE_DEFECT_CORRECTION_WITHIN_APPROVED_DELIVERABLE",
            "GENERATED_EXPLORATION != PROJECT_ASSET_APPROVED != RUNTIME_PROMOTED",
        ):
            self.assertIn(token, combined)

    def test_no_anchor_pipeline_does_not_turn_a_comparison_sheet_into_runtime_asset(self) -> None:
        candidate = self._read(CANDIDATE)
        self.assertIn("COMPARISON_SHEET_NOT_PRODUCTION_ASSET", candidate)
        self.assertIn("SELECTED_DIRECTION_REQUIRES_STANDALONE_ANCHOR", candidate)
        self.assertIn("PROJECT_ASSET_APPROVED", candidate)


if __name__ == "__main__":
    unittest.main()
