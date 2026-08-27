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

    def test_information_artifacts_remain_required_without_forcing_image_generation(self):
        owner_paths = (
            ROOT / "docs/knowledge/game-development/GAME_VISUAL_ASSET_COVERAGE_CHECKLIST.md",
            ROOT / "docs/knowledge/game-development/ART_DIRECTION_AND_ASSET_PLANNING_GUIDE.md",
            ROOT / "docs/GPT_IMAGE_GENERATION_AND_REVIEW_POLICY.md",
        )
        for path in owner_paths:
            text = path.read_text(encoding="utf-8")
            self.assertIn("PRODUCTION_INFORMATION", text, path.as_posix())
            self.assertIn("TEXT_TABLE_FLOW_DB_FIRST", text, path.as_posix())
        coverage = owner_paths[0].read_text(encoding="utf-8")
        policy = owner_paths[2].read_text(encoding="utf-8")
        self.assertIn("INFORMATION_ARTIFACT_NOT_IMAGE_ASSET", coverage)
        self.assertIn("INFORMATION_ARTIFACT_NOT_IMAGE_ASSET", policy)
        for information_kind in ("시스템 설명", "세계관", "관계도", "제작 체크리스트"):
            self.assertIn(information_kind, policy)

    def test_image_generation_requires_an_actual_game_or_product_consumer(self):
        owner_paths = (
            ROOT / "docs/knowledge/game-development/GAME_VISUAL_ASSET_COVERAGE_CHECKLIST.md",
            ROOT / "docs/knowledge/game-development/ART_DIRECTION_AND_ASSET_PLANNING_GUIDE.md",
            ROOT / "docs/GPT_IMAGE_GENERATION_AND_REVIEW_POLICY.md",
            ROOT / "skills/designing-art-prompts-and-technique-cards/SKILL.md",
            ROOT / "templates/planning/GPT_IMAGE_GENERATION_AND_REVIEW_PLAN.md",
        )
        for path in owner_paths:
            text = path.read_text(encoding="utf-8")
            self.assertIn("ACTUAL_CONSUMER_REQUIRED", text, path.as_posix())
            self.assertIn("PLAYER_FACING_EXPLANATORY", text, path.as_posix())
        art_guide = owner_paths[1].read_text(encoding="utf-8")
        self.assertIn("인게임 튜토리얼 그림, 도감·세력 관계 UI", art_guide)
        self.assertIn("시스템 다이어그램, 세계관 구조, 관계도", art_guide)
        policy = owner_paths[2].read_text(encoding="utf-8")
        self.assertIn("DO_NOT_GENERATE", policy)

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

    def test_screen_surface_inventory_precedes_asset_category_decomposition(self):
        path = (
            ROOT
            / "docs/knowledge/game-development/GAME_SCREEN_SURFACE_INVENTORY_AND_VISUAL_ASSET_MATRIX.md"
        )
        self.assertTrue(path.exists(), "screen-first visual coverage owner must exist")
        text = path.read_text(encoding="utf-8")
        for required in (
            "SCREEN_SURFACE_INVENTORY_FIRST",
            "SCREEN_LEVEL_COMPOSITION_REQUIRED",
            "SCREEN_DESIGN_REFERENCE",
            "RUNTIME_COMPONENT_ASSET",
            "NO_NEW_IMAGE_FILE_REQUIRED",
            "SCREEN_TO_ASSET_COVERAGE_MATRIX",
            "PLAYER_VISIBLE_SCREEN_FAMILIES",
            "MAIN_TITLE_MENU",
            "RESULT_REWARD",
            "PAUSE_SETTINGS",
            "LOADING_TRANSITION_ERROR",
            "GAME_VISUAL_ASSET_COVERAGE_CHECKLIST.md",
            "NO_AUTOMATIC_IMAGE_GENERATION_FROM_GAPS",
        ):
            self.assertIn(required, text)
        self.assertLess(
            text.index("SCREEN_SURFACE_INVENTORY_FIRST"),
            text.index("SCREEN_TO_ASSET_COVERAGE_MATRIX"),
        )

    def test_work_template_is_paste_ready_and_executes_correction(self):
        path = (
            ROOT
            / "templates/project-operations/GPT_WORK_SCREEN_FIRST_VISUAL_ASSET_COVERAGE_AND_CORRECTION_INSTRUCTION.md"
        )
        self.assertTrue(path.exists(), "paste-ready Work instruction must exist")
        text = path.read_text(encoding="utf-8")
        for required in (
            "현재 이 채팅이 연결된 프로젝트",
            "SCREEN_SURFACE_INVENTORY_FIRST",
            "메인/타이틀 화면",
            "화면별 구성요소",
            "Godot",
            "Notion",
            "GitHub",
            "NO_AUTOMATIC_IMAGE_GENERATION_FROM_GAPS",
            "교정 로그",
            "남은 blocking gap",
            "GAME_SCREEN_SURFACE_INVENTORY_AND_VISUAL_ASSET_MATRIX.md",
            "GAME_VISUAL_ASSET_COVERAGE_CHECKLIST.md",
        ):
            self.assertIn(required, text)
        self.assertNotIn("[프로젝트명]", text)
        self.assertNotIn("TBD", text)


if __name__ == "__main__":
    unittest.main()
