from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8")


class V9GovernanceDocumentTests(unittest.TestCase):
    def test_ui_reference_card_covers_open_source_adoption_and_godot_contract(self) -> None:
        card = read("templates/research/UX_UI_REFERENCE_CARD.md")
        for field in (
            "license",
            "commercial_use",
            "attribution",
            "modification_and_redistribution",
            "godot_compatibility",
            "maintenance",
            "dependency_removal",
            "copying_prohibited",
            "transformation_and_validation",
        ):
            self.assertIn(field, card)
        godot = read("skills/auditing-and-refining-ui-art/references/godot-ui-implementation-contract.md")
        for term in ("Control", "Container", "Theme", "Signal", "focus", "Korean", "resolution"):
            self.assertIn(term, godot)

    def test_common_project_adoption_order_is_explicitly_held(self) -> None:
        order = read("templates/prompts/BASE_V9_COMMON_PROJECT_ADOPTION_WORK_ORDER.md")
        for project in ("Ten Paces: Hidden Moves", "Blacksmith", "OMENWARD", "urban-legend", "GRIMOIRE"):
            self.assertIn(project, order)
        for prerequisite in ("Base v9.0.0 lock", "repository audit", "Sheet access", "user approval", "verification environment"):
            self.assertIn(prerequisite, order)
        self.assertIn("[보류]", order)
        self.assertIn("No Sheet write", order)

    def test_release_design_plan_and_integrity_audit_keep_dispositions_and_evidence_visible(self) -> None:
        design = read("docs/operations/BASE_V9_RELEASE_DESIGN.md")
        implementation = read("docs/operations/BASE_V9_IMPLEMENTATION_PLAN.md")
        audit = read("docs/operations/BASE_V9_INTEGRITY_AUDIT.md")
        for term in ("Registry", "frontmatter", "generated", "Base Adapter", "project-specific"):
            self.assertIn(term, design)
        self.assertIn("POST_RELEASE_PROJECT_ADOPTION_WAVE", implementation)
        for disposition in ("KEEP", "CONSOLIDATE", "ARCHIVE", "RETIRE", "BLOCKED"):
            self.assertIn(disposition, audit)
        for check in ("link", "orphan", "cycle", "provenance", "template consumer"):
            self.assertIn(check, audit)

    def test_v9_workflow_exposes_ci_and_adversarial_gates_for_all_change_paths(self) -> None:
        workflow = read(".github/workflows/validate-base-v9-rc.yml")
        for term in ("docs/**", "tools/**", ".github/workflows/**", "ci-gate:", "adversarial-gate:"):
            self.assertIn(term, workflow)
        self.assertIn("check_base_v9_integrity.py", workflow)

    def test_cross_project_handoff_is_archived_without_active_authority(self) -> None:
        archive_path = "docs/archive/handoffs/2026-07-29-ux-ui-common-system-expansion.md"
        stub = read("docs/ACTIVE_HANDOFF.md")
        archive_file = ROOT / archive_path

        self.assertTrue(archive_file.is_file(), archive_path)
        archive = archive_file.read_text(encoding="utf-8")
        documentation_map = read("docs/DOCUMENTATION_MAP.md")
        changelog = read("docs/CHANGELOG.md")

        for term in ("COMPATIBILITY_ONLY", archive_path, "프로젝트 저장소"):
            self.assertIn(term, stub)
        self.assertNotIn("| `Blacksmith` |", stub)

        for term in (
            "status: SUPERSEDED",
            "original_path: docs/ACTIVE_HANDOFF.md",
            "active_authority: false",
            "implementation_authority: NONE",
            "rollback_ref: dc98a666563b1f0f87b665eac97dbd8a8be37576",
            "# UX/UI 공용 체계 확산 Active Handoff",
        ):
            self.assertIn(term, archive)

        self.assertIn(archive_path, documentation_map)
        self.assertIn("COMPATIBILITY_ONLY", documentation_map)
        self.assertIn(archive_path, changelog)


if __name__ == "__main__":
    unittest.main()
