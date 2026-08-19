from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


class P04VerticalSlicePlayerValueTraceTests(unittest.TestCase):
    def test_vertical_slice_plan_consumes_required_player_value_trace(self) -> None:
        plan = read("templates/planning/VERTICAL_SLICE_PLAN.md")

        self.assertIn("P04_PLAYER_VALUE_TO_EVIDENCE_TRACE", plan)
        for term in (
            "player_promise",
            "meaningful_choice",
            "expected_experience",
            "research_question",
            "observable_signal",
            "evidence_ceiling",
            "slice_acceptance",
        ):
            self.assertIn(term, plan)

    def test_world_storyline_fit_is_consumed_by_p04_execution_surfaces(self) -> None:
        concept_skill = read("skills/analyzing-and-refining-game-concepts/SKILL.md")
        concept_plan = read("templates/planning/GAME_CONCEPT_DIRECTION_REVIEW.md")
        slice_plan = read("templates/planning/VERTICAL_SLICE_PLAN.md")

        self.assertIn("WORLD_STORYLINE_FIT_REQUIRED", concept_skill)
        self.assertIn("WORLD_STORYLINE_FIT_REQUIRED", concept_plan)
        for term in ("세계관", "핵심 스토리", "플레이어 판타지"):
            self.assertIn(term, concept_skill)
            self.assertIn(term, concept_plan)

        self.assertIn("WORLD_STORYLINE_FIT_REQUIRED", slice_plan)
        self.assertIn("NOT_APPLICABLE", slice_plan)

    def test_benchmark_template_requires_real_alternatives_and_long_term_fit(self) -> None:
        benchmark = read("templates/planning/GAME_BENCHMARK_PLAYER_EVIDENCE.md")

        for term in (
            "CURRENT_STATE_BENCHMARK_ALTERNATIVE_TRADE_STUDY",
            "MINIMUM_VIABLE_ALTERNATIVES: 3",
            "BETTER_ALTERNATIVE_SEARCH",
            "LONG_TERM_PLAN_FIT_REQUIRED",
            "revisit_condition",
        ):
            self.assertIn(term, benchmark)

    def test_current_active_projects_have_reusable_module_catalog(self) -> None:
        registry = read(
            "docs/knowledge/game-development/reuse/REUSABLE_MODULE_REGISTRY.md"
        )

        for project_key in (
            "COC_FICTION",
            "GRIMOIRE",
            "SWITCHY",
            "TETRIS",
            "URBAN_LEGEND",
            "NINJA_SURVIVAL",
            "MY_LITTLE_BOAT",
            "BLACKSMITH",
            "TEN_PACES",
            "OMENWARD",
        ):
            self.assertIn(project_key, registry)

        for module_id in (
            "RM-SYS-001",
            "RM-SYS-003",
            "RM-SYS-005",
            "RM-SYS-011",
            "RM-SYS-012",
            "RM-SYS-013",
            "RM-SYS-015",
            "RM-SYS-016",
            "RM-SYS-017",
            "RM-SYS-018",
            "RM-SYS-019",
            "RM-SYS-020",
            "RM-NAR-001",
            "RM-NAR-002",
            "RM-TOOL-001",
            "RM-TOOL-003",
            "RM-VIS-001",
            "RM-VIS-003",
            "RM-WORK-001",
            "RM-WORK-002",
        ):
            self.assertIn(module_id, registry)

        for term in (
            "MODULE_CONTRACT_DEFINED",
            "IMPLEMENTATION_NOT_BUILT",
            "RIGHTS_REVIEW_REQUIRED",
            "NOTION_HUMAN_VIEW",
        ):
            self.assertIn(term, registry)

    def test_reusable_module_catalog_keeps_family_contracts_separate(self) -> None:
        gameplay = read(
            "docs/knowledge/game-development/reuse/GAMEPLAY_AND_CONTENT_MODULES.md"
        )
        production = read(
            "docs/knowledge/game-development/reuse/PRODUCTION_TOOL_WORKFLOW_MODULES.md"
        )
        visual = read(
            "docs/knowledge/game-development/reuse/VISUAL_ASSET_MATERIAL_MODULES.md"
        )

        for term in (
            "GRID_PLACEMENT_RULE_ENGINE",
            "NARRATIVE_NODE_CHOICE_STATE_ENGINE",
            "CARD_ACTION_EFFECT_ENGINE",
            "SURVIVOR_AUTO_COMBAT_PROGRESSION_CORE",
            "FALLING_BLOCK_LINE_CLEAR_CORE",
        ):
            self.assertIn(term, gameplay)

        for term in (
            "DATA_SCHEMA_CROSSREF_VALIDATOR",
            "DETERMINISTIC_SEED_REPLAY_CAPTURE",
            "BALANCE_SCENARIO_BATCH_SIMULATOR",
            "PROJECT_REUSE_OPPORTUNITY_SCAN",
            "SKILL_WORKFLOW_PATTERN_EVAL",
        ):
            self.assertIn(term, production)

        for term in (
            "SEMANTIC_UI_SKIN_KIT",
            "GAMEPLAY_SYMBOL_ATLAS",
            "MODULAR_BACKGROUND_LAYER_KIT",
            "COMBAT_TELEGRAPH_VFX_KIT",
            "PORTRAIT_STATE_VARIANT_KIT",
        ):
            self.assertIn(term, visual)

        self.assertIn("TETRIS_TRADE_DRESS_BOUNDARY", gameplay)
        self.assertIn("DIRECT_LICENSED_REUSE", visual)
        self.assertIn("PROJECT_ASSET_APPROVED", visual)

    def test_tutorial_template_uses_current_project_workspace(self) -> None:
        tutorial = read("templates/planning/TUTORIAL_AND_ONBOARDING_DESIGN_CONTRACT.md")

        self.assertIn("NOTION_DEFAULT_PROJECT_WORKSPACE", tutorial)
        self.assertNotIn("connected_google_sheet:", tutorial)
        self.assertNotIn("configured_google_sheets_state:", tutorial)
        self.assertNotIn("Google Sheets가 구성된 경우", tutorial)

    def test_feature_spec_does_not_restore_retired_sheet_or_figma_authority(self) -> None:
        feature = read("templates/planning/GAME_FEATURE_DESIGN_SPEC.md")

        self.assertIn("Notion", feature)
        self.assertNotIn("Google Sheets에는 Feature ID", feature)
        self.assertNotIn("Mermaid·Figma·FigJam", feature)

    def test_benchmark_finalization_uses_current_workspace_not_project_sheet(self) -> None:
        benchmark = read("templates/planning/GAME_BENCHMARK_PLAYER_EVIDENCE.md")

        self.assertIn("Notion", benchmark)
        self.assertNotIn("Project Sheet 갱신", benchmark)

    def test_game_ux_ui_template_does_not_restore_figma_authority(self) -> None:
        ux = read("templates/planning/GAME_UX_UI_SYSTEM.md")

        self.assertIn("Notion", ux)
        self.assertIn("repository", ux)
        self.assertNotIn("Figma Frame", ux)


if __name__ == "__main__":
    unittest.main()
