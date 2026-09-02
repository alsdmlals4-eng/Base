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

    def test_project_handoff_routes_to_current_repository_owners(self) -> None:
        handoff = json.loads(
            read(
                "docs/knowledge/game-development/reuse/adoption/PROJECT_WORK_REUSE_HANDOFF.json"
            )
        )
        matrix = json.loads(
            read(
                "docs/knowledge/game-development/reuse/adoption/ACTIVE_PROJECT_ADOPTION_MATRIX.json"
            )
        )

        switchy_handoff = handoff["projects"]["SWITCHY"]["next_project_work_action"]
        switchy_revisit = matrix["projects"]["SWITCHY"]["revisit"]
        self.assertNotIn("SX-DEC-059", switchy_handoff)
        self.assertNotIn("SX-DEC-059", switchy_revisit)
        self.assertIn("current project", switchy_handoff.lower())
        self.assertIn("current project", switchy_revisit.lower())

        ten_paces_fields = "\n".join(
            [
                handoff["projects"]["TEN_PACES"]["next_project_work_action"],
                matrix["projects"]["TEN_PACES"]["blocker"],
                matrix["projects"]["TEN_PACES"]["revisit"],
            ]
        )
        self.assertNotIn("Notion", ten_paces_fields)
        self.assertIn("current repository", ten_paces_fields.lower())

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
