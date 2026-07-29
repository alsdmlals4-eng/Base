from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "auditing-and-refining-ui-art" / "SKILL.md"
REFERENCE_ROOT = ROOT / "skills" / "auditing-and-refining-ui-art" / "references"
REGISTRY = ROOT / "skills" / "SKILL_REGISTRY.json"
REFERENCE_FRESHNESS = ROOT / ".github" / "reference-freshness.json"
UX_UI_WORKFLOW = ROOT / ".github" / "workflows" / "validate-game-ux-ui-system.yml"
PLANNING_TEMPLATE = ROOT / "templates" / "planning" / "GAME_UX_UI_SYSTEM.md"
REFERENCE_CARD = ROOT / "templates" / "research" / "UX_UI_REFERENCE_CARD.md"
REVIEW_CHECKLIST = ROOT / "templates" / "quality" / "GAME_UX_UI_REVIEW_CHECKLIST.md"


class GameUxUiSystemContractTests(unittest.TestCase):
    def test_shared_reference_and_template_files_exist(self) -> None:
        required = [
            REFERENCE_ROOT / "ux-ui-design-system-method.md",
            REFERENCE_ROOT / "game-ux-pattern-library.md",
            REFERENCE_ROOT / "ux-ui-reference-library.md",
            REFERENCE_ROOT / "godot-ui-implementation-contract.md",
            REFERENCE_ROOT / "project-adapter-contract.md",
            REFERENCE_ROOT / "ui-polishing-method.md",
            PLANNING_TEMPLATE,
            REFERENCE_CARD,
            REVIEW_CHECKLIST,
        ]
        missing = [path.relative_to(ROOT).as_posix() for path in required if not path.is_file()]
        self.assertEqual([], missing)

    def test_skill_exposes_design_polishing_and_audit_modes(self) -> None:
        text = SKILL.read_text(encoding="utf-8")
        required_modes = {
            "experience-contract",
            "flow-and-information-architecture",
            "pattern-selection",
            "design-system-contract",
            "godot-ui-contract",
            "accessibility-gate",
            "playtest-contract",
            "polishing-pass",
            "runtime-ui-audit",
            "refine-approved-findings",
            "reaudit",
        }
        for mode in required_modes:
            with self.subTest(mode=mode):
                self.assertIn(f"`{mode}`", text)

    def test_skill_defines_polishing_priority_and_repetition_contract(self) -> None:
        text = SKILL.read_text(encoding="utf-8")
        for required in (
            "P0 BLOCKER",
            "P1 CLARITY",
            "P2 CONSISTENCY",
            "P3 DELIGHT",
            "반복 사용",
            "중단·재진입",
            "ui-polishing-method.md",
        ):
            with self.subTest(required=required):
                self.assertIn(required, text)

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

    def test_reference_card_carries_polishing_evidence(self) -> None:
        text = REFERENCE_CARD.read_text(encoding="utf-8")
        for required in (
            "polishing_evidence",
            "affected_priority",
            "feedback_tier",
            "expected_repetition_frequency",
            "reduced_motion_mute_haptic_off_path",
            "before_after_validation",
        ):
            with self.subTest(required=required):
                self.assertIn(required, text)

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

    def test_project_template_carries_polishing_contract(self) -> None:
        text = PLANNING_TEMPLATE.read_text(encoding="utf-8")
        for required in (
            "폴리싱 준비도",
            "피드백 예산",
            "반복 사용·중단·재진입",
            "전후 Artifact",
        ):
            with self.subTest(required=required):
                self.assertIn(required, text)

    def test_review_checklist_carries_polishing_gates(self) -> None:
        text = REVIEW_CHECKLIST.read_text(encoding="utf-8")
        for required in (
            "P0",
            "P1",
            "P2",
            "P3",
            "reduced motion",
            "중복 입력",
            "애니메이션 중단",
            "반복 사용",
        ):
            with self.subTest(required=required):
                self.assertIn(required, text)

    def test_registry_routes_design_polishing_and_runtime_audit(self) -> None:
        registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
        skill = next(
            item
            for item in registry["skills"]
            if item["skill_id"] == "auditing-and-refining-ui-art"
        )
        required_tags = {
            "game-ux",
            "ui-design",
            "ui-polishing",
            "interaction-feedback",
            "godot-ui",
            "runtime-ui-audit",
        }
        self.assertTrue(required_tags.issubset(set(skill["trigger_tags"])))
        use_when = " ".join(skill["use_when"])
        for required in ("설계", "폴리싱", "감사"):
            with self.subTest(required=required):
                self.assertIn(required, use_when)

    def test_ui_skill_coupled_change_requires_all_consumers(self) -> None:
        config = json.loads(REFERENCE_FRESHNESS.read_text(encoding="utf-8"))
        rule = next(
            item
            for item in config["coupled_change_rules"]
            if item["name"] == "game-ux-ui-skill-sync"
        )
        required = {
            "skills/SKILL_REGISTRY.json",
            "skills/SKILL_LEARNING_LOG.md",
            "skills/README.md",
            "templates/planning/GAME_UX_UI_SYSTEM.md",
            "templates/research/UX_UI_REFERENCE_CARD.md",
            "templates/quality/GAME_UX_UI_REVIEW_CHECKLIST.md",
            "tests/test_game_ux_ui_system.py",
            ".github/workflows/validate-game-ux-ui-system.yml",
        }
        self.assertTrue(required.issubset(set(rule["require_all_changed"])))

    def test_registry_structure_rule_accepts_ui_system_contract_test(self) -> None:
        config = json.loads(REFERENCE_FRESHNESS.read_text(encoding="utf-8"))
        rule = next(
            item
            for item in config["coupled_change_rules"]
            if item["name"] == "registry-structure-test-sync"
        )
        self.assertIn("tests/test_game_ux_ui_system.py", rule["require_any_changed"])

    def test_ui_workflow_watches_all_contract_consumers(self) -> None:
        text = UX_UI_WORKFLOW.read_text(encoding="utf-8")
        for required in (
            "skills/SKILL_REGISTRY.json",
            "skills/SKILL_LEARNING_LOG.md",
            "AGENTS.md",
            "START_HERE.md",
            "docs/OPERATING_MODEL.md",
            "docs/DOCUMENTATION_MAP.md",
            "docs/superpowers/specs/2026-07-29-ui-polishing-system-design.md",
            "docs/superpowers/plans/2026-07-29-ui-polishing-system.md",
        ):
            with self.subTest(required=required):
                self.assertIn(f'      - "{required}"', text)

    def test_human_entrypoints_route_design_polishing_and_audit(self) -> None:
        paths = [
            ROOT / "skills" / "README.md",
            ROOT / "AGENTS.md",
            ROOT / "START_HERE.md",
            ROOT / "docs" / "OPERATING_MODEL.md",
            ROOT / "docs" / "DOCUMENTATION_MAP.md",
        ]
        for path in paths:
            text = path.read_text(encoding="utf-8")
            with self.subTest(path=path.relative_to(ROOT).as_posix()):
                self.assertIn("auditing-and-refining-ui-art", text)
                self.assertIn("폴리싱", text)

    def test_human_validation_is_not_replaced_by_automation(self) -> None:
        checklist = REVIEW_CHECKLIST.read_text(encoding="utf-8")
        self.assertIn("HUMAN_NOT_RUN", checklist)
        self.assertIn("자동 검사", checklist)
        self.assertIn("사람 이해", checklist)


if __name__ == "__main__":
    unittest.main()
