from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "auditing-and-refining-ui-art" / "SKILL.md"
REFERENCE_ROOT = ROOT / "skills" / "auditing-and-refining-ui-art" / "references"


class GameUxUiSystemContractTests(unittest.TestCase):
    def test_shared_reference_and_template_files_exist(self) -> None:
        required = [
            REFERENCE_ROOT / "ux-ui-design-system-method.md",
            REFERENCE_ROOT / "game-ux-pattern-library.md",
            REFERENCE_ROOT / "ux-ui-reference-library.md",
            REFERENCE_ROOT / "godot-ui-implementation-contract.md",
            REFERENCE_ROOT / "project-adapter-contract.md",
            ROOT / "templates" / "planning" / "GAME_UX_UI_SYSTEM.md",
            ROOT / "templates" / "research" / "UX_UI_REFERENCE_CARD.md",
            ROOT / "templates" / "quality" / "GAME_UX_UI_REVIEW_CHECKLIST.md",
        ]
        missing = [path.relative_to(ROOT).as_posix() for path in required if not path.is_file()]
        self.assertEqual([], missing)

    def test_skill_exposes_design_and_audit_modes(self) -> None:
        text = SKILL.read_text(encoding="utf-8")
        required_modes = {
            "experience-contract",
            "flow-and-information-architecture",
            "pattern-selection",
            "design-system-contract",
            "godot-ui-contract",
            "accessibility-gate",
            "playtest-contract",
            "runtime-ui-audit",
            "refine-approved-findings",
            "reaudit",
        }
        for mode in required_modes:
            with self.subTest(mode=mode):
                self.assertIn(f"`{mode}`", text)

    def test_skill_preserves_existing_ui_audit_contract(self) -> None:
        text = SKILL.read_text(encoding="utf-8")
        for required in (
            "scan_ui_art_signals.py",
            "A~E",
            "CANDIDATE",
            "사용자 승인 전",
            "전후 렌더",
        ):
            with self.subTest(required=required):
                self.assertIn(required, text)

    def test_skill_keeps_ui_out_of_domain_state_ownership(self) -> None:
        text = SKILL.read_text(encoding="utf-8")
        self.assertIn("도메인 규칙", text)
        self.assertIn("사용자 의도", text)
        self.assertIn("Signal", text)
        self.assertIn("재계산", text)

    def test_reference_library_uses_adoption_decisions_and_official_sources(self) -> None:
        text = (REFERENCE_ROOT / "ux-ui-reference-library.md").read_text(encoding="utf-8")
        for decision in ("ADOPT", "ADAPT", "AVOID", "TEST", "IGNORE"):
            self.assertIn(decision, text)
        for source in (
            "Xbox Accessibility Guidelines",
            "WCAG 2.2",
            "Godot",
            "Apple Human Interface Guidelines",
            "Material Design 3",
            "Nielsen Norman Group",
        ):
            with self.subTest(source=source):
                self.assertIn(source, text)

    def test_pattern_library_covers_core_player_risks(self) -> None:
        text = (REFERENCE_ROOT / "game-ux-pattern-library.md").read_text(encoding="utf-8")
        required_pattern_ids = {
            "UXP-STATUS-VISIBILITY",
            "UXP-ACTION-FEEDBACK",
            "UXP-PREDICT-BEFORE-COMMIT",
            "UXP-PROGRESSIVE-DISCLOSURE",
            "UXP-COMPARABLE-CHOICES",
            "UXP-SAFE-REVERSAL",
            "UXP-ERROR-RECOVERY",
            "UXP-FOCUS-NAVIGATION",
            "UXP-MULTI-CHANNEL-CUES",
            "UXP-RETURNING-PLAYER-MEMORY",
            "UXP-CAUSAL-RECAP",
            "UXP-EMPTY-LOCKED-FALLBACK",
        }
        for pattern_id in required_pattern_ids:
            with self.subTest(pattern_id=pattern_id):
                self.assertIn(pattern_id, text)

    def test_human_validation_is_not_replaced_by_automation(self) -> None:
        checklist = (ROOT / "templates" / "quality" / "GAME_UX_UI_REVIEW_CHECKLIST.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("HUMAN_NOT_RUN", checklist)
        self.assertIn("자동 검사", checklist)
        self.assertIn("사람 이해", checklist)


if __name__ == "__main__":
    unittest.main()
