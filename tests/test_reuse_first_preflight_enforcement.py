from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


class ReuseFirstPreflightEnforcementTests(unittest.TestCase):
    def test_root_and_intake_enforce_reuse_first_before_new_creation(self) -> None:
        agents = read("AGENTS.md")
        intake = read("skills/managing-project-intake-and-work-contract/SKILL.md")
        start = read("START_HERE.md")

        self.assertIn("REUSE_FIRST_PREFLIGHT_REQUIRED", agents)
        self.assertIn("REUSE_LEARNING_HANDOFF_REQUIRED", agents)
        self.assertIn("PROJECT_WORK_REUSE_HANDOFF.json", intake)
        self.assertIn("Asset/Reference/Benchmark", intake)
        self.assertIn("Base accumulated knowledge/case/reference", intake)
        self.assertIn("targeted", intake.lower())
        self.assertIn("NOT_RUN", intake)
        self.assertIn("REUSED_EVIDENCE", intake)
        self.assertIn("NOT_APPLICABLE", intake)
        self.assertIn("REUSE_FIRST_PREFLIGHT_REQUIRED", start)

        project_pos = intake.find("target project GitHub current main")
        asset_pos = intake.find("Asset/Reference/Benchmark")
        reuse_pos = intake.find("PROJECT_WORK_REUSE_HANDOFF.json")
        accumulated_pos = intake.find("Base accumulated knowledge/case/reference")
        targeted_pos = intake.lower().find("targeted cross-project")
        benchmark_pos = intake.find("benchmark + professional practice")
        self.assertGreaterEqual(project_pos, 0)
        self.assertGreater(asset_pos, project_pos)
        self.assertGreater(reuse_pos, asset_pos)
        self.assertGreater(accumulated_pos, reuse_pos)
        self.assertGreater(targeted_pos, accumulated_pos)
        self.assertGreater(benchmark_pos, targeted_pos)

    def test_structured_handoff_is_fail_closed_and_targeted(self) -> None:
        handoff = json.loads(
            read(
                "docs/knowledge/game-development/reuse/adoption/PROJECT_WORK_REUSE_HANDOFF.json"
            )
        )

        preflight = handoff["preflight_gate"]
        self.assertEqual(preflight["id"], "REUSE_FIRST_PREFLIGHT_REQUIRED")
        self.assertTrue(preflight["not_run_blocks_build_new"])
        self.assertTrue(preflight["targeted_cross_project_only"])
        self.assertTrue(preflight["no_bulk_project_scan"])
        self.assertIn("REUSED_EVIDENCE", preflight["allowed_evidence_states"])
        self.assertIn("NOT_APPLICABLE", preflight["allowed_evidence_states"])
        self.assertIn("PROJECT_APPROVED_ASSET_REFERENCE_BENCHMARK_SURFACES", preflight["required_source_order"])
        self.assertIn("BASE_REUSE_HANDOFF_PROFILE_MATRIX_REGISTRY", preflight["required_source_order"])
        self.assertIn("BASE_ACCUMULATED_KNOWLEDGE_CASE_REFERENCE", preflight["required_source_order"])
        self.assertIn("TARGETED_CROSS_PROJECT_VERIFIED_EVIDENCE", preflight["required_source_order"])
        self.assertIn("DECISION_RELEVANT_EXTERNAL_BENCHMARK", preflight["required_source_order"])

        exit_gate = handoff["exit_learning_gate"]
        self.assertEqual(exit_gate["id"], "REUSE_LEARNING_HANDOFF_REQUIRED")
        self.assertEqual(exit_gate["no_change_result"], "NO_NEW_REUSE_LEARNING")
        self.assertTrue(exit_gate["promotion_is_not_automatic"])
        self.assertEqual(exit_gate["required_fields"], handoff["exit_handoff_fields"])

    def test_project_handoff_resolves_mutable_state_from_current_authority(self) -> None:
        handoff = json.loads(
            read(
                "docs/knowledge/game-development/reuse/adoption/PROJECT_WORK_REUSE_HANDOFF.json"
            )
        )
        entry_rules = handoff["entry_rules"]
        self.assertTrue(entry_rules["project_canon_overrides_base_reference"])
        self.assertTrue(
            entry_rules[
                "project_specific_next_action_uses_current_project_authority"
            ]
        )
        self.assertTrue(
            entry_rules["legacy_workspace_requires_current_project_authority"]
        )

        # Base must route mutable state; it must not freeze historical project snapshots.
        actions = {
            project_id: handoff["projects"][project_id]["next_project_work_action"]
            for project_id in (
                "SWITCHY",
                "TETRIS",
                "NINJA_SURVIVAL",
                "TEN_PACES",
                "OMENWARD",
            )
        }
        for project_id, action in actions.items():
            with self.subTest(project_id=project_id):
                self.assertIn("current project authority", action.lower())

        self.assertNotIn("SX-DEC-", actions["SWITCHY"])
        self.assertNotIn("TETRIS-CORE-024", actions["TETRIS"])
        self.assertNotIn("TETRIS-TIME-025", actions["TETRIS"])
        self.assertNotIn("Phase-C", actions["NINJA_SURVIVAL"])
        self.assertNotIn("exact Notion state", actions["TEN_PACES"])
        self.assertIn("migration/history", actions["TEN_PACES"])
        self.assertNotIn("Issue #", actions["OMENWARD"])
        self.assertNotIn("PR #", actions["OMENWARD"])

    def test_gate_does_not_force_unbounded_research_or_project_adoption(self) -> None:
        intake = read("skills/managing-project-intake-and-work-contract/SKILL.md")
        agents = read("AGENTS.md")
        combined = "\n".join((intake, agents))

        self.assertIn("모든 프로젝트를 전수", combined)
        self.assertIn("기계적", combined)
        self.assertIn("프로젝트 정본", combined)
        self.assertIn("신규 제작", combined)
        self.assertIn("재사용", combined)


if __name__ == "__main__":
    unittest.main()
