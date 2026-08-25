import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class GameVisualAssetCoverageContractTests(unittest.TestCase):
    def test_coverage_guide_exists_and_is_not_a_second_asset_canon(self):
        path = ROOT / "docs/knowledge/game-development/GAME_VISUAL_ASSET_COVERAGE_CHECKLIST.md"
        self.assertTrue(path.exists(), "visual asset coverage guide must exist")
        text = path.read_text(encoding="utf-8")
        for required in (
            "COVERAGE_CHECK_ONLY",
            "NOT_A_SECOND_ASSET_CANON",
            "coverage_status",
            "GAP_BLOCKING",
            "REQUIREMENT_LINKED",
            "STATE_FAMILY_COMPLETENESS",
            "PLATFORM_SPEC_RECHECK_REQUIRED",
            "NO_AUTOMATIC_IMAGE_GENERATION_FROM_GAPS",
        ):
            self.assertIn(required, text)

    def test_image_policy_runs_coverage_before_visual_requirement_gate(self):
        path = ROOT / "docs/GPT_IMAGE_GENERATION_AND_REVIEW_POLICY.md"
        text = path.read_text(encoding="utf-8")
        self.assertIn("Visual Asset Coverage Preflight", text)
        self.assertIn("GAME_VISUAL_ASSET_COVERAGE_CHECKLIST.md", text)
        self.assertIn("NO_AUTOMATIC_IMAGE_GENERATION_FROM_GAPS", text)
        self.assertLess(
            text.index("Visual Asset Coverage Preflight"),
            text.index("## 1. Visual Requirement Gate"),
        )

    def test_art_prompt_skill_consumes_coverage_without_expanding_scope(self):
        path = ROOT / "skills/designing-art-prompts-and-technique-cards/SKILL.md"
        text = path.read_text(encoding="utf-8")
        self.assertIn("coverage_item_id", text)
        self.assertIn("coverage_status", text)
        self.assertIn("GAME_VISUAL_ASSET_COVERAGE_CHECKLIST.md", text)
        self.assertIn("NO_AUTOMATIC_IMAGE_GENERATION_FROM_GAPS", text)

    def test_generation_plan_tracks_coverage_and_state_family(self):
        path = ROOT / "templates/planning/GPT_IMAGE_GENERATION_AND_REVIEW_PLAN.md"
        text = path.read_text(encoding="utf-8")
        for required in (
            "coverage_item_id",
            "coverage_status",
            "state_family_status",
            "## 2A. Visual asset coverage",
            "GAP_BLOCKING",
            "NOT_APPLICABLE",
        ):
            self.assertIn(required, text)


if __name__ == "__main__":
    unittest.main()
