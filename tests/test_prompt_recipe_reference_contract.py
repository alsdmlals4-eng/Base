from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_AUDIT = ROOT / "docs" / "knowledge" / "research" / "PROMPT_RECIPE_SOURCE_AUDIT.md"
RECIPE_CARD = ROOT / "templates" / "research" / "AI_IMAGE_PROMPT_RECIPE_CARD.md"
TECHNIQUE_CARD = ROOT / "templates" / "planning" / "ART_TECHNIQUE_CARD.md"
SKILL = ROOT / "skills" / "designing-art-prompts-and-technique-cards" / "SKILL.md"
DESIGN = (
    ROOT
    / "docs"
    / "superpowers"
    / "specs"
    / "2026-07-29-prompt-recipe-reference-integration-design.md"
)


class PromptRecipeReferenceContractTests(unittest.TestCase):
    def test_required_files_exist(self) -> None:
        missing = [
            path.relative_to(ROOT).as_posix()
            for path in (SOURCE_AUDIT, RECIPE_CARD, TECHNIQUE_CARD, SKILL, DESIGN)
            if not path.is_file()
        ]
        self.assertEqual([], missing)

    def test_source_audit_preserves_reference_and_rights_boundaries(self) -> None:
        text = SOURCE_AUDIT.read_text(encoding="utf-8")
        for required in (
            "https://promptrecipe.pages.dev/",
            "REFERENCE_ONLY",
            "UNVERIFIED",
            "원문 전문을 복제하지 않는다",
            "유사 이미지",
            "유사 프롬프트",
            "특정 작가",
            "재검증 조건",
        ):
            with self.subTest(required=required):
                self.assertIn(required, text)

    def test_recipe_card_requires_forecast_reasoning_and_result_comparison(self) -> None:
        text = RECIPE_CARD.read_text(encoding="utf-8")
        for required in (
            "similar_image_references",
            "similar_prompt_references",
            "pre_generation_forecast",
            "prediction_confidence",
            "confidence_basis",
            "unverified_assumptions",
            "desired_observation_to_prompt",
            "reasoning_basis",
            "expected_model_response",
            "risk_and_correction",
            "actual_result_review",
            "PREDICTION_NOT_TESTED",
            "MODEL_OR_CONTEXT_CHANGED_RETEST_REQUIRED",
        ):
            with self.subTest(required=required):
                self.assertIn(required, text)

    def test_existing_technique_card_routes_reference_assisted_forecast(self) -> None:
        technique = TECHNIQUE_CARD.read_text(encoding="utf-8")
        skill = SKILL.read_text(encoding="utf-8")
        self.assertIn("`technique-card`", skill)
        self.assertIn("templates/planning/ART_TECHNIQUE_CARD.md", skill)
        for required in (
            "PROMPT_RECIPE_SOURCE_AUDIT.md",
            "AI_IMAGE_PROMPT_RECIPE_CARD.md",
            "생성 전 예측",
            "프롬프트 추론 근거",
            "유사 이미지",
            "유사 프롬프트",
            "예측과 실제 결과",
        ):
            with self.subTest(required=required):
                self.assertIn(required, technique)

    def test_unrun_generation_cannot_be_verified(self) -> None:
        source = SOURCE_AUDIT.read_text(encoding="utf-8")
        card = RECIPE_CARD.read_text(encoding="utf-8")
        technique = TECHNIQUE_CARD.read_text(encoding="utf-8")
        combined = source + "\n" + card + "\n" + technique
        self.assertIn("실제 생성 없이", combined)
        self.assertIn("VERIFIED", combined)
        self.assertIn("가설", combined)


if __name__ == "__main__":
    unittest.main()
