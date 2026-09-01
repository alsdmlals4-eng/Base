from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AGENTS = ROOT / "AGENTS.md"
LONG_HORIZON = ROOT / "docs" / "LONG_HORIZON_WORK_EXECUTION_POLICY.md"
ROUTING_GUIDE = ROOT / "docs" / "knowledge" / "ai" / "SKILL_ROUTING_PRECISION_GUIDE.md"
PLANNING_POLICY = ROOT / "docs" / "PLANNING_SEQUENCE_AND_EVIDENCE_POLICY.md"
AI_GUIDE = (
    ROOT
    / "docs"
    / "knowledge"
    / "game-development"
    / "AI_ASSISTED_GAME_DEVELOPMENT_GUIDE.md"
)
OPERATING_MODEL = ROOT / "docs" / "operations" / "BASE_PARTITION_OPERATING_MODEL.md"
MANIFEST = ROOT / "docs" / "operations" / "BASE_PARTITION_MANIFEST.json"
OPTIMIZATION_PROMPT = ROOT / "templates" / "prompts" / "BASE_PARTITION_OPTIMIZATION_PROMPT.md"
INTEGRATION_PROMPT = ROOT / "templates" / "prompts" / "BASE_PARTITION_INTEGRATION_PROMPT.md"
SYNC_SKILL = ROOT / "skills" / "synchronizing-local-and-github-state" / "SKILL.md"
SYNC_PROTOCOL = (
    ROOT
    / "skills"
    / "synchronizing-local-and-github-state"
    / "references"
    / "safe-sync-protocol.md"
)
BEHAVIOR_EVALS = ROOT / "skills" / "SKILL_BEHAVIOR_EVALS.json"
BEHAVIOR_COVERAGE_EVALS = ROOT / "skills" / "SKILL_BEHAVIOR_COVERAGE_EVALS.json"
DASHBOARD_SKILL = ROOT / "skills" / "building-project-visual-dashboards" / "SKILL.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class DeliberateWorkRoutingRecoveryTests(unittest.TestCase):
    def test_l1_deep_work_cannot_finish_before_required_evidence(self) -> None:
        required = (
            "DEEP_WORK_PREANSWER_GATE",
            "REQUIRED_EVIDENCE_BEFORE_FINAL",
            "NOT_RUN_MANDATORY_GATE_BLOCKS_COMPLETION",
            "INTERMEDIATE_REPORT_SUPPRESSION_IS_NOT_WORK_REDUCTION",
        )
        for text in (read(AGENTS), read(LONG_HORIZON)):
            for token in required:
                self.assertIn(token, text)

    def test_sparse_skill_and_tool_routing_cannot_defer_required_research_or_review(self) -> None:
        guide = read(ROUTING_GUIDE)
        for token in (
            "SPARSE_ROUTING_MUST_NOT_SKIP_MANDATORY_GATES",
            "TOOL_SHORTLIST_MUST_NOT_DEFER_REQUIRED_RESEARCH",
            "MANDATORY_GUARD_IS_NOT_BUDGET_FILLING",
            "REQUIRED_RESEARCH_IS_CURRENT_STAGE_WORK",
        ):
            self.assertIn(token, guide)

        self.assertNotIn(
            "검증 Skill을 PLAN 시작부터 미리 붙여 budget을 채우지 않는다.",
            guide,
        )

    def test_full_part_coordinator_is_explicit_maintenance_mode_not_general_default(self) -> None:
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        coordinator = manifest["coordinator_execution"]
        self.assertEqual(
            "EXPLICIT_BASE_FULL_P01_P09_OPTIMIZATION",
            coordinator["applies_only_when"],
        )
        self.assertFalse(coordinator["is_default_for_general_project_work"])
        self.assertEqual(
            "GOAL_SCOPED_PLAN_RESEARCH_REVIEW_THEN_BUILD_VERIFY",
            coordinator["general_project_workflow"],
        )

        for text in (
            read(OPERATING_MODEL),
            read(OPTIMIZATION_PROMPT),
            read(INTEGRATION_PROMPT),
        ):
            self.assertIn("BASE_FULL_PART_COORDINATOR_EXPLICIT_ONLY", text)
            self.assertIn("GENERAL_PROJECT_WORK_USES_GOAL_SCOPED_PHASES", text)

    def test_open_prs_are_read_only_and_followups_target_merged_main(self) -> None:
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        self.assertEqual("OPEN_PR_READ_ONLY_BY_DEFAULT", manifest["open_pr_policy"])
        detection = manifest["active_workstream_detection"]
        self.assertTrue(detection["open_pr_state_is_sufficient_for_read_only"])
        self.assertTrue(detection["mutation_requires_explicit_named_authorization"])
        self.assertEqual("MERGED_MAIN_ONLY", detection["default_follow_up_target"])

        for text in (
            read(AGENTS),
            read(LONG_HORIZON),
            read(OPERATING_MODEL),
            read(SYNC_SKILL),
            read(SYNC_PROTOCOL),
        ):
            self.assertIn("OPEN_PR_READ_ONLY_BY_DEFAULT", text)
            self.assertIn("OPEN_PR_MUTATION_REQUIRES_EXPLICIT_NAMED_AUTHORIZATION", text)
            self.assertIn("FOLLOW_UP_TARGET_IS_MERGED_MAIN", text)

    def test_gpt_primary_and_high_reasoning_cannot_replace_required_execution(self) -> None:
        required = (
            "GPT_PRIMARY_IS_DECISION_OWNERSHIP_NOT_TEXT_ONLY",
            "REASONING_EFFORT_IS_NOT_WORK_EVIDENCE",
            "REQUIRED_TOOL_EXECUTION_IS_NOT_OPTIONAL_EXECUTOR_HANDOFF",
        )
        for text in (
            read(AGENTS),
            read(LONG_HORIZON),
            read(PLANNING_POLICY),
            read(AI_GUIDE),
        ):
            for token in required:
                self.assertIn(token, text)

    def test_behavior_evals_use_current_modes_and_pressure_deliberate_work(self) -> None:
        documents = (
            json.loads(BEHAVIOR_EVALS.read_text(encoding="utf-8")),
            json.loads(BEHAVIOR_COVERAGE_EVALS.read_text(encoding="utf-8")),
        )
        cases = {
            case["case_id"]: case
            for document in documents
            for case in document["cases"]
        }

        self.assertEqual(
            ["preflight", "reconcile", "verify"],
            cases["SBE-028"]["expected_skill_modes"],
        )
        self.assertNotIn("HTML", cases["SBE-031"]["prompt"])
        self.assertIn("repository human projection", cases["SBE-031"]["prompt"])
        self.assertEqual(
            [
                "frame-project-home",
                "map-canonical-sources",
                "build-project-home",
                "bind-evidence-status",
                "verify-destination-readback",
            ],
            cases["SBE-031"]["expected_skill_modes"],
        )
        self.assertEqual(
            ["recover", "publish", "verify"],
            cases["SBE-039"]["expected_skill_modes"],
        )
        self.assertIn(
            "GITHUB_CAPABILITY_FALLBACK",
            "\n".join(cases["SBE-039"]["required_evidence"]),
        )

        deliberate = cases["SBE-040"]
        self.assertEqual(
            "managing-project-intake-and-work-contract",
            deliberate["expected_primary_skill"],
        )
        self.assertEqual(
            {
                "running-adversarial-review-and-refinement",
                "reviewing-and-validating-project-changes",
            },
            set(deliberate["expected_supporting_skills"]),
        )
        required_evidence = "\n".join(deliberate["required_evidence"])
        for token in (
            "2일 전",
            "인터넷 원출처",
            "최소 3개",
            "Tool 실행",
            "5회",
            "NOT_RUN",
            "중간보고",
        ):
            self.assertIn(token, required_evidence)

        dashboard = read(DASHBOARD_SKILL)
        for mode in cases["SBE-031"]["expected_skill_modes"]:
            self.assertIn(f"`{mode}`", dashboard)

if __name__ == "__main__":
    unittest.main()
