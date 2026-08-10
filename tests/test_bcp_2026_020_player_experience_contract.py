from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


class PlayerExperienceValidationGateTests(unittest.TestCase):
    def test_bcp020_has_explicit_implementation_approval_without_a_new_active_skill(self) -> None:
        registry = json.loads(read("[수정제안서]/PROPOSAL_REGISTRY.json"))
        entry = next(
            item
            for item in registry["proposals"]
            if item["proposal_id"] == "BCP-2026-020-player-experience-validation-gates"
        )
        self.assertEqual("APPROVED_FOR_IMPLEMENTATION", entry["status"])
        self.assertTrue(entry["approval_ref"])
        self.assertIsNone(entry["implementation_pr"])
        self.assertNotIn("player-experience-management", read("skills/SKILL_REGISTRY.json"))

    def test_evidence_layers_do_not_promote_technical_or_ui_checks_to_human_experience(self) -> None:
        guide = read("docs/knowledge/game-development/GAME_DESIGN_AND_PLAYER_EXPERIENCE_GUIDE.md")
        validation = read("templates/quality/PROJECT_CHANGE_VALIDATION.md")
        feature_spec = read("templates/planning/GAME_FEATURE_DESIGN_SPEC.md")
        for text in (guide, validation):
            for token in (
                "TECH_EVIDENCE",
                "UI_EVIDENCE",
                "HUMAN_USABILITY_EVIDENCE",
                "PLAYER_EXPERIENCE_EVIDENCE",
                "NOT_RUN",
            ):
                self.assertIn(token, text)
        self.assertIn("executed verification", feature_spec)
        self.assertIn("실제 실행 결과", feature_spec)

    def test_first_session_decision_screen_and_minigame_gates_keep_genre_exceptions(self) -> None:
        guide = read("docs/knowledge/game-development/GAME_DESIGN_AND_PLAYER_EXPERIENCE_GUIDE.md")
        tutorial = read("templates/planning/TUTORIAL_AND_ONBOARDING_DESIGN_CONTRACT.md")
        ui_checklist = read("templates/quality/GAME_UX_UI_REVIEW_CHECKLIST.md")
        for token in (
            "FIRST_10_MINUTES_CONTRACT",
            "대표 문제",
            "대표 행동",
            "첫 선택",
            "첫 결과",
            "다음 질문",
            "MINIGAME_NARRATIVE_FUNCTION_GATE",
            "CORE_INTERACTION_EVIDENCE",
        ):
            self.assertIn(token, guide)
        self.assertIn("FIRST_10_MINUTES_CONTRACT", tutorial)
        for token in ("현재 상황", "선택할 수 있는가", "선택에 필요한 정보", "비용·위험·결과"):
            self.assertIn(token, ui_checklist)


if __name__ == "__main__":
    unittest.main()
