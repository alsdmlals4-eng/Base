from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXTERNAL_AI_SKILL = ROOT / "skills" / "orchestrating-deepseek-worktrees" / "SKILL.md"
EXTERNAL_AI_LOG = ROOT / "skills" / "orchestrating-deepseek-worktrees" / "LEARNING_LOG.md"
MODEL_COST_SKILL = ROOT / "skills" / "optimizing-ai-model-and-prompt-costs" / "SKILL.md"
MODEL_COST_LOG = ROOT / "skills" / "optimizing-ai-model-and-prompt-costs" / "LEARNING_LOG.md"
ROUTING_GUIDE = ROOT / "docs" / "knowledge" / "ai" / "SKILL_ROUTING_PRECISION_GUIDE.md"
P08_PARTITION_LOG = ROOT / "docs" / "operations" / "base-partitions" / "learning" / "P08_LEARNING_LOG.md"
FRESHNESS = ROOT / ".github" / "reference-freshness.json"
BASE_V9_WORKFLOW = ROOT / ".github" / "workflows" / "validate-base-v9-rc.yml"


class P08AiOperationsContractTests(unittest.TestCase):
    def test_external_executor_rehydrates_canon_and_keeps_codex_optional(self) -> None:
        text = EXTERNAL_AI_SKILL.read_text(encoding="utf-8")
        for required in (
            "EXECUTOR_REHYDRATION_GATE",
            "GPT_PRIMARY_REVIEWER",
            "OPTIONAL_CODEX_EXECUTOR",
            "exact branch/commit",
            "AGENTS.md",
            "REVIEW_PENDING",
        ):
            with self.subTest(required=required):
                self.assertIn(required, text)
        self.assertNotIn("Codex가 `skills/reviewing-and-validating-project-changes", text)

    def test_cost_routing_separates_included_subscription_from_metered_spend(self) -> None:
        text = MODEL_COST_SKILL.read_text(encoding="utf-8")
        for required in (
            "COST_SURFACE_GATE",
            "SUBSCRIPTION_INCLUDED",
            "SEPARATELY_METERED",
            "COST_GATE_BLOCKED",
            "GPT_PRO",
            "credits",
            "API",
        ):
            with self.subTest(required=required):
                self.assertIn(required, text)
        self.assertIn("사용자 승인", text)

    def test_sparse_routing_applies_to_tools_as_well_as_skills(self) -> None:
        text = ROUTING_GUIDE.read_text(encoding="utf-8")
        for required in (
            "TOOL_SHORTLIST_JUST_IN_TIME",
            "목적이 겹치는 Tool",
            "현재 단계",
            "실측 model-run eval",
        ):
            with self.subTest(required=required):
                self.assertIn(required, text)

    def test_p08_test_is_exact_freshness_companion_and_permanent_ci_consumer(self) -> None:
        data = json.loads(FRESHNESS.read_text(encoding="utf-8"))
        rule = next(row for row in data["coupled_change_rules"] if row["name"] == "local-skill-contract-learning-test-sync")
        self.assertEqual(["skills/**/SKILL.md"], rule["when_changed"])
        self.assertIn("tests/test_p08_ai_operations_contract.py", rule["require_any_changed"])
        workflow = BASE_V9_WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("tests.test_p08_ai_operations_contract", workflow)

    def test_local_learning_logs_reference_only_real_current_evidence(self) -> None:
        stale = "docs/operations/ai-executors/P08_OPTIMIZATION_REPORT_2026-08-19.md"
        for path in (EXTERNAL_AI_LOG, MODEL_COST_LOG):
            text = path.read_text(encoding="utf-8")
            self.assertNotIn(stale, text, path)
            self.assertNotIn("PENDING_FINAL_EXACT_HEAD_CI", text, path)
            self.assertIn("REVALIDATED_FOCUSED_AND_BASE_V9_ON_727ecb15", text, path)
            self.assertIn("tests/test_p08_ai_operations_contract.py", text, path)
            self.assertIn("docs/operations/base-partitions/learning/P08_LEARNING_LOG.md", text, path)
        self.assertTrue(P08_PARTITION_LOG.is_file())

    def test_old_p08_nonblocking_ownership_questions_survive_takeover_without_old_report_authority(self) -> None:
        text = P08_PARTITION_LOG.read_text(encoding="utf-8")
        for required in (
            "CARRY_FORWARD_TO_FINAL_INTEGRATION",
            "P08-OWNERSHIP-01",
            "templates/ai/DEEPSEEK_WORK_PACKAGE.md",
            "P08-OWNERSHIP-02",
            ".codex-plugin/plugin.json",
            "former P08 freshness ownership deadlock is resolved",
        ):
            with self.subTest(required=required):
                self.assertIn(required, text)
        self.assertIn("PR #535 Git history", text)


if __name__ == "__main__":
    unittest.main()
