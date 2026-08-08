from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROMPT = ROOT / "templates/prompts/PROJECT_ADAPTIVE_INGAME_ART_CHECKPOINT_PROMPT.md"


class ProjectAdaptiveInGameArtPromptTests(unittest.TestCase):
    def test_prompt_requires_project_first_scene_approval_and_review(self) -> None:
        text = PROMPT.read_text(encoding="utf-8")
        for token in (
            "PROJECT_ADAPTIVE_INGAME_ART_CHECKPOINT",
            "PROJECT_FIRST",
            "PR_CHECK_REQUIRED",
            "SCENE_SET_APPROVAL_REQUIRED",
            "GRILL_ME_REQUIRED",
            "IMAGE_GENERATION_PROHIBITED_BEFORE_APPROVAL",
            "FINAL_USER_OUTPUT_IMAGE_ONLY",
        ):
            self.assertIn(token, text)
        self.assertIn("모든 프로젝트에 고정 화면 세트를 강제하지 않는다", text)
        self.assertIn("열린 PR", text)
        self.assertIn("최근 병합 PR", text)

    def test_prompt_preserves_evidence_and_adversarial_gates(self) -> None:
        text = PROMPT.read_text(encoding="utf-8")
        for token in (
            "CURRENT",
            "INFERRED",
            "PROPOSED",
            "PLACEHOLDER",
            "MISSING_CANON",
            "CANON_CONFLICT",
            "VISUAL_CANONICAL_CONFLICT",
            "DRAFT_VISUAL",
            "attack",
            "validate-critique",
            "decision-report",
            "regression-recheck",
        ):
            self.assertIn(token, text)

    def test_prompt_supports_individual_scenes_and_readable_boards(self) -> None:
        text = PROMPT.read_text(encoding="utf-8")
        self.assertIn("개별 장면", text)
        self.assertIn("TWO_BOARD_DEFAULT_WHEN_DENSITY_RISK", text)
        self.assertIn("합", text)
        self.assertIn("절초", text)
        self.assertIn("사용자가 검토 기록을 요청", text)


if __name__ == "__main__":
    unittest.main()
