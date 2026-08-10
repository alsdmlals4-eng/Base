from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MATRIX = (
    ROOT
    / "docs"
    / "knowledge"
    / "game-development"
    / "UX_LAWS_COMPLETENESS_MATRIX.md"
)
REFERENCE_LIBRARY = (
    ROOT
    / "skills"
    / "auditing-and-refining-ui-art"
    / "references"
    / "ux-ui-reference-library.md"
)


class UxLawsCompletenessMatrixTests(unittest.TestCase):
    def test_matrix_is_routed_from_reference_library(self) -> None:
        self.assertTrue(MATRIX.is_file())
        library = REFERENCE_LIBRARY.read_text(encoding="utf-8")
        self.assertIn("UX_LAWS_COMPLETENESS_MATRIX.md", library)

    def test_all_user_supplied_laws_are_explicitly_mapped(self) -> None:
        text = MATRIX.read_text(encoding="utf-8")
        required = (
            "Aesthetic-Usability Effect",
            "Cognitive Bias",
            "Cognitive Load",
            "Selective Attention",
            "Working Memory",
            "Choice Overload",
            "Hick's Law",
            "Mental Model",
            "Doherty Threshold",
            "Fitts's Law",
            "Flow",
            "Goal-Gradient Effect",
            "Zeigarnik Effect",
            "Chunking",
            "Miller's Law",
            "Serial Position Effect",
            "Law of Common Region",
            "Law of Proximity",
            "Law of Prägnanz",
            "Law of Similarity",
            "Law of Uniform Connectedness",
            "Jakob's Law",
            "Paradox of the Active User",
            "Peak-End Rule",
            "Von Restorff Effect",
            "Primacy-Recency",
            "Tesler's Law",
            "Postel's Law",
            "Occam's Razor",
            "Pareto Principle",
            "Parkinson's Law",
        )
        for law in required:
            with self.subTest(law=law):
                self.assertIn(law, text)

    def test_matrix_declares_31_of_31_and_duplicate_normalization(self) -> None:
        text = MATRIX.read_text(encoding="utf-8")
        self.assertIn("31/31 MAPPED", text)
        self.assertIn("#26 → #16 Serial Position Effect", text)
        self.assertIn("#2 Cognitive Bias", text)
        self.assertIn("#23 Paradox of the Active User", text)

    def test_matrix_does_not_promote_psychology_to_global_constants(self) -> None:
        text = MATRIX.read_text(encoding="utf-8")
        for required in (
            "전역 강제 수치로 승격: `0`",
            "다크 패턴 정당화에 사용 가능: `0`",
            "실제 사용자 연구·플레이테스트를 대체하지 않는다",
        ):
            self.assertIn(required, text)


if __name__ == "__main__":
    unittest.main()
