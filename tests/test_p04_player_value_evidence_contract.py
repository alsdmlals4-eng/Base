from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


class P04PlayerValueEvidenceContractTests(unittest.TestCase):
    def test_game_design_guide_owns_the_cross_module_trace(self) -> None:
        guide = read("docs/knowledge/game-development/GAME_DESIGN_AND_PLAYER_EXPERIENCE_GUIDE.md")
        self.assertIn("P04_PLAYER_VALUE_TO_EVIDENCE_TRACE", guide)
        for field in (
            "player_promise",
            "meaningful_choice",
            "expected_experience",
            "research_question",
            "observable_signal",
            "evidence_ceiling",
            "slice_acceptance",
        ):
            self.assertIn(field, guide)

    def test_concept_refinement_uses_current_canon_and_clear_research_boundary(self) -> None:
        skill = read("skills/analyzing-and-refining-game-concepts/SKILL.md")
        self.assertNotIn("프로젝트 정본·Google Sheets·실제 코드", skill)
        self.assertIn("DECISION_SPECIFIC_RESEARCH", skill)
        self.assertIn("Notion/GitHub", skill)

    def test_user_research_coverage_is_question_first_not_checklist_completion(self) -> None:
        skill = read("skills/governing-game-user-research-coverage/SKILL.md")
        self.assertIn("RESEARCH_QUESTION_FIRST", skill)
        self.assertIn("DECISION_RELEVANT_COVERAGE", skill)
        self.assertIn("NOT_APPLICABLE", skill)
        self.assertIn("11/11", skill)

    def test_vertical_slice_traces_player_value_and_respects_evidence_ceiling(self) -> None:
        skill = read("skills/designing-vertical-slices/SKILL.md")
        self.assertIn("PLAYER_VALUE_TRACE_REQUIRED", skill)
        self.assertIn("player_promise", skill)
        self.assertIn("meaningful_choice", skill)
        self.assertIn("observable_signal", skill)
        self.assertIn("evidence_ceiling", skill)
        self.assertIn("slice_acceptance", skill)


if __name__ == "__main__":
    unittest.main()
