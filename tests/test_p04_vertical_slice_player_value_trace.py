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
        concept = read("skills/analyzing-and-refining-game-concepts/SKILL.md")
        plan = read("templates/planning/VERTICAL_SLICE_PLAN.md")

        self.assertIn("WORLD_STORYLINE_FIT_REQUIRED", concept)
        for term in ("세계관", "핵심 스토리", "플레이어 판타지"):
            self.assertIn(term, concept)

        self.assertIn("WORLD_STORYLINE_FIT_REQUIRED", plan)
        self.assertIn("NOT_APPLICABLE", plan)

    def test_legacy_sheet_planning_template_is_migration_only(self) -> None:
        legacy = read("templates/planning/PROJECT_PLANNING_SEQUENCE_AND_SHEET_TABS.md")

        for term in (
            "MIGRATION_ONLY_UNTIL_REMOVAL",
            "NOTION_DEFAULT_PROJECT_WORKSPACE",
            "NEW_PROJECT_USE: FORBIDDEN",
        ):
            self.assertIn(term, legacy)

        self.assertNotIn("새 Sheet에 설치하는 권장 핵심 tab", legacy)
        self.assertNotIn("실제 Figma·Whimsical·기타 시각 Artifact가 있을 때만 설치한다", legacy)


if __name__ == "__main__":
    unittest.main()
