from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RULEBOOK = (
    ROOT
    / "skills"
    / "auditing-and-refining-ui-art"
    / "references"
    / "ui-ux-visual-design-rulebook.md"
)
REFERENCE_LIBRARY = (
    ROOT
    / "skills"
    / "auditing-and-refining-ui-art"
    / "references"
    / "ux-ui-reference-library.md"
)
PLANNING_TEMPLATE = ROOT / "templates" / "planning" / "GAME_UX_UI_SYSTEM.md"
REVIEW_CHECKLIST = ROOT / "templates" / "quality" / "GAME_UX_UI_REVIEW_CHECKLIST.md"


class UiUxVisualDesignRuleContractTests(unittest.TestCase):
    def test_rulebook_exists_and_is_routed_from_existing_owner_reference(self) -> None:
        self.assertTrue(RULEBOOK.is_file())
        library = REFERENCE_LIBRARY.read_text(encoding="utf-8")
        self.assertIn("ui-ux-visual-design-rulebook.md", library)
        self.assertIn("2026-08-10", library)

    def test_rulebook_separates_rule_strength_and_evidence_types(self) -> None:
        text = RULEBOOK.read_text(encoding="utf-8")
        for required in (
            "MUST",
            "SHOULD",
            "STYLE_DEFAULT",
            "TEST_REQUIRED",
            "규범 표준",
            "플랫폼 권고",
            "인지·사용성 휴리스틱",
            "시각 스타일 휴리스틱",
        ):
            with self.subTest(required=required):
                self.assertIn(required, text)

    def test_rulebook_preserves_platform_specific_target_units(self) -> None:
        text = RULEBOOK.read_text(encoding="utf-8")
        for required in (
            "24×24 CSS px",
            "44×44 pt",
            "48×48 dp",
            "4.5:1",
            "3:1",
            "200%",
        ):
            with self.subTest(required=required):
                self.assertIn(required, text)
        self.assertIn("하나의 전역 상수", text)

    def test_rulebook_covers_gui_semantic_alphabet_and_recovery(self) -> None:
        text = RULEBOOK.read_text(encoding="utf-8")
        for required in (
            "버튼",
            "링크",
            "폼",
            "메뉴",
            "대화상자",
            "알림",
            "아이콘",
            "체크박스",
            "라디오",
            "토글",
            "탭",
            "검색",
            "실행 취소",
            "결과 중심",
        ):
            with self.subTest(required=required):
                self.assertIn(required, text)

    def test_rulebook_covers_psychology_without_turning_it_into_dark_patterns(self) -> None:
        text = RULEBOOK.read_text(encoding="utf-8")
        for required in (
            "Hick",
            "Fitts",
            "Jakob",
            "인지 부하",
            "작업 기억",
            "Choice Overload",
            "Gestalt",
            "Flow",
            "Goal-Gradient",
            "Zeigarnik",
            "Peak-End",
            "Tesler",
            "Postel",
            "Occam",
            "Pareto",
            "Parkinson",
            "다크 패턴",
            "허위 진행",
            "의도적 지연",
            "7±2",
        ):
            with self.subTest(required=required):
                self.assertIn(required, text)

    def test_rulebook_covers_visual_defaults_without_making_them_global_laws(self) -> None:
        text = RULEBOOK.read_text(encoding="utf-8")
        for required in (
            "near-black",
            "near-white",
            "12-column",
            "16px",
            "70자",
            "8 기반",
            "optical alignment",
            "shadow",
            "container brightness",
            "최대 2개 서체",
            "STYLE_DEFAULT",
        ):
            with self.subTest(required=required):
                self.assertIn(required, text)

    def test_rulebook_covers_game_specific_accessibility_and_input(self) -> None:
        text = RULEBOOK.read_text(encoding="utf-8")
        for required in (
            "controller focus",
            "remapping",
            "subtitles/captions",
            "TV 거리",
            "FOV",
            "camera movement",
            "Reduced Motion",
            "색상만",
        ):
            with self.subTest(required=required):
                self.assertIn(required, text)

    def test_planning_template_records_rule_profile_and_exceptions(self) -> None:
        text = PLANNING_TEMPLATE.read_text(encoding="utf-8")
        for required in (
            "UI/UX·비주얼 규칙 프로필",
            "rule_id",
            "MUST/SHOULD/STYLE_DEFAULT/TEST_REQUIRED",
            "예외 사유",
            "검증 증거",
        ):
            with self.subTest(required=required):
                self.assertIn(required, text)

    def test_review_checklist_enforces_semantics_accessibility_and_heuristic_boundaries(self) -> None:
        text = REVIEW_CHECKLIST.read_text(encoding="utf-8")
        for required in (
            "버튼과 링크",
            "체크박스·라디오·토글",
            "24×24 CSS px",
            "44×44 pt",
            "48×48 dp",
            "Miller의 7±2",
            "허위 진행",
            "의도적 지연",
            "12-column",
            "16px",
            "70자",
            "STYLE_DEFAULT",
        ):
            with self.subTest(required=required):
                self.assertIn(required, text)


if __name__ == "__main__":
    unittest.main()
