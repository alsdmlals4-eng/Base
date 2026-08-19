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

    def test_benchmark_reverse_engineering_requires_pattern_and_genre_reuse_boundaries(self) -> None:
        guide = read("docs/BENCHMARKING_REFERENCE_GUIDE.md")
        method = read("docs/knowledge/research/DESIGN_RESEARCH_AND_EVIDENCE_METHOD.md")
        benchmark = read("templates/planning/GAME_BENCHMARK_PLAYER_EVIDENCE.md")

        for surface in (guide, method, benchmark):
            for term in (
                "BENCHMARK_REVERSE_ENGINEERING_PATTERN_REUSE",
                "REUSABLE_UNIT_DISCOVERY",
                "MECHANIC_PATTERN_LIBRARY",
                "GENRE_FOUNDATION_REFERENCE",
                "MULTI_SOURCE_EXTRACTION",
                "NOVELTY_DELTA",
                "CLEAN_ROOM_REIMPLEMENTATION",
            ):
                self.assertIn(term, surface)

        for reusable_unit in (
            "SYSTEM_PATTERN",
            "TOOL_PATTERN",
            "ASSET_MATERIAL_PATTERN",
            "UI_UX_PATTERN",
            "CONTENT_PATTERN",
            "WORKFLOW_PATTERN",
            "SKILL_PATTERN",
        ):
            self.assertIn(reusable_unit, benchmark)

        self.assertIn("테트리스류", benchmark)
        self.assertIn("텍스트 선택형", benchmark)
        self.assertIn("덱빌딩 로그라이크", benchmark)
        self.assertIn("서바이버라이크", benchmark)
        self.assertIn("표현·자산·코드", benchmark)

    def test_reverse_engineered_skill_and_workflow_candidates_use_existing_adoption_owner(self) -> None:
        guide = read("docs/BENCHMARKING_REFERENCE_GUIDE.md")
        skill_guide = read("docs/AI_SKILL_ADOPTION_GUIDE.md")

        for term in (
            "REVERSE_ENGINEERED_SKILL_WORKFLOW_CANDIDATE",
            "PATTERN_NOT_PACKAGE_COPY",
            "EVAL_BEFORE_PROMOTION",
        ):
            self.assertIn(term, skill_guide)

        for owner in (
            "AI_SKILL_ADOPTION_GUIDE.md",
            "PROJECT_LOCAL_ASSET_VAULT_POLICY.md",
            "CAPABILITY_COMPOSITION_MAP.md",
        ):
            self.assertIn(owner, guide)

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
