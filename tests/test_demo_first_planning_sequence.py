from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


class DemoFirstPlanningSequenceTests(unittest.TestCase):
    def test_policy_declares_notion_repo_scope_and_prework_audit(self) -> None:
        policy = read("docs/PLANNING_SEQUENCE_AND_EVIDENCE_POLICY.md")
        for term in (
            "NOTION_HUMAN_FACING_CANON",
            "REPOSITORY_STRUCTURED_CANON",
            "RETIRED_MIGRATION_ONLY",
            "DUPLICATE_WORK",
            "MISSING_CANON",
            "MISSING_CONSUMER",
            "CANON_CONFLICT",
            "IMPLEMENTATION_CONFLICT",
            "STALE_REFERENCE",
            "PROPAGATION_AUDIT",
        ):
            self.assertIn(term, policy)
        self.assertNotIn("PROJECT_SHEET_CONFIGURED", policy)
        self.assertNotIn("USER_FACING_GDD_WORKSPACE", policy)

    def test_material_planning_uses_three_layer_evidence_and_approval_bundles(self) -> None:
        policy = read("docs/PLANNING_SEQUENCE_AND_EVIDENCE_POLICY.md")
        evidence = read("skills/analyzing-and-refining-game-concepts/references/benchmark-player-evidence-and-playtests.md")
        sequence = read("skills/managing-project-intake-and-work-contract/references/work-decomposition-and-sequencing.md")
        for term in ("BENCHMARK_EVIDENCE", "PLAYER_RESPONSE_EVIDENCE", "PROFESSIONAL_OFFICIAL_EVIDENCE"):
            self.assertIn(term, policy)
            self.assertIn(term, evidence)
        self.assertIn("Approval Bundle", policy)
        self.assertIn("Approval Bundle", sequence)

    def test_compact_size_ceiling_is_removed_without_losing_discoverability(self) -> None:
        skill = read("skills/simplifying-skill-bodies/SKILL.md")
        reference = read("skills/simplifying-skill-bodies/references/progressive-disclosure-rules.md")
        coverage_checker = read("tools/check_skill_system_coverage.py")
        combined = skill + reference
        for term in ("줄 수", "문자 수", "분량 상한", "내용 보존", "한 단계 발견성"):
            self.assertIn(term, combined)
        self.assertNotIn("self.assertLessEqual", read("tests/test_skill_system_coverage.py"))
        self.assertNotIn("exceeds 150 lines", coverage_checker)
        self.assertNotIn("len(text.splitlines()) > 150", coverage_checker)
        self.assertIn("completeness-first contract", coverage_checker)
        self.assertIn("Missing completeness contract token", coverage_checker)

    def test_demo_first_vertical_slice_has_no_standalone_core_poc_section(self) -> None:
        stage = read("docs/knowledge/vertical-slice/INTEGRATED_DEMO_STAGE_GATES.md")
        plan = read("templates/planning/VERTICAL_SLICE_PLAN.md")
        policy = read("docs/PLANNING_SEQUENCE_AND_EVIDENCE_POLICY.md")
        for term in ("DEMO_FIRST_VERTICAL_SLICE", "DEMO_VALIDATION", "완성 품질 데모", "TECHNICAL_SPIKE"):
            self.assertIn(term, policy + stage + plan)
        self.assertNotIn("## 2. CORE_POC 결과", plan)
        self.assertIn("별도 `CORE_POC`", stage)

    def test_project_human_planning_surfaces_follow_approved_order_without_sheet_template(self) -> None:
        policy = read("docs/PLANNING_SEQUENCE_AND_EVIDENCE_POLICY.md")
        ordered = (
            "Project Home",
            "Project Control",
            "Reference / Benchmark",
            "Visual / Story Bible",
            "Core System",
            "Production / Handoff",
        )
        positions = [policy.index(term) for term in ordered]
        self.assertEqual(positions, sorted(positions))
        self.assertNotIn("PROJECT_PLANNING_SEQUENCE_AND_SHEET_TABS.md", policy)


if __name__ == "__main__":
    unittest.main()