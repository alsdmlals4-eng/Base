from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


class V47ProjectExecutionContractTests(unittest.TestCase):
    def test_long_horizon_policy_covers_v47_project_execution_contract(self) -> None:
        policy = read("docs/LONG_HORIZON_WORK_EXECUTION_POLICY.md")
        for term in (
            "CREATIVE_SYNTHESIS_AND_NOVELTY_GATE",
            "BENCHMARK_PORTFOLIO_NOT_SINGLE_REFERENCE",
            "FUN_HYPOTHESIS_AND_DISTINCTIVENESS",
            "PROJECT_UNDERSTANDING_BEFORE_VISUALIZATION",
            "VISUALIZATION_NEEDS_INVENTORY_TO_NOTION",
            "USER_DECLARED_OTHER_CHAT_WORKSTREAM_PROTECTED",
            "NEW_SYSTEM_OR_SKILL_ALLOWED_AFTER_EXISTING_SOLUTION_FIRST",
            "CORE_LOOP_BALANCE_BUDGET_BUILD_TEST",
            "WORLD_STORYLINE_CORE_ARC_REQUIRED",
            "APPROVAL_CHECKPOINT_SYNC_MERGE_PR_RECHECK",
            "USER_LEARNING_COMPLETION_REPORT",
            "NO_TOOL_HUB_DEFAULT_ROUTE",
            "NO_QA_EVIDENCE_STUDIO_DEFAULT_ROUTE",
        ):
            self.assertIn(term, policy)

    def test_entrypoints_do_not_recommend_retired_tool_hub_or_qa_studio(self) -> None:
        start = read("START_HERE.md")
        powershell = read("docs/operations/POWERSHELL_FRESH_SHELL_EXECUTION_CONTRACT.md")
        self.assertIn("NO_TOOL_HUB_DEFAULT_ROUTE", start)
        self.assertIn("NO_QA_EVIDENCE_STUDIO_DEFAULT_ROUTE", start)
        self.assertIn("Loop Engineering", powershell)
        self.assertNotIn("Tool Hub 실제 runtime을 우선", powershell)

    def test_visualization_is_project_understanding_first_and_notion_bound(self) -> None:
        visual = read("docs/VISUAL_COLLABORATION_TOOL_POLICY.md")
        for term in (
            "PROJECT_UNDERSTANDING_BEFORE_VISUALIZATION",
            "VISUALIZATION_NEEDS_INVENTORY_TO_NOTION",
            "visualization_need_id",
            "Notion",
            "PROJECT_RELATION_REQUIRED",
        ):
            self.assertIn(term, visual)
        self.assertNotIn("FIGMA_DEFAULT_VISUAL_WORKSPACE", visual)

    def test_user_declared_other_chat_work_is_protected_even_when_pr_state_changes(self) -> None:
        agents = read("AGENTS.md")
        policy = read("docs/LONG_HORIZON_WORK_EXECUTION_POLICY.md")
        for text in (agents, policy):
            self.assertIn("USER_DECLARED_OTHER_CHAT_WORKSTREAM_PROTECTED", text)
            self.assertIn("ACTIVE_OTHER_WORKER", text)

    def test_learning_report_teaches_purpose_inputs_outputs_and_effects(self) -> None:
        policy = read("docs/LONG_HORIZON_WORK_EXECUTION_POLICY.md")
        for term in (
            "USER_LEARNING_COMPLETION_REPORT",
            "왜 존재하는가",
            "핵심 규칙",
            "핵심 Skill",
            "핵심 Module",
            "BEFORE → AFTER",
            "장기 효과",
            "재검토 조건",
        ):
            self.assertIn(term, policy)


if __name__ == "__main__":
    unittest.main()
