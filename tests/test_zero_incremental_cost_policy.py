from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AGENTS = ROOT / "AGENTS.md"
WORKFLOW = ROOT / ".github" / "workflows" / "periodic-source-scan-queue.yml"
RUNNER = ROOT / "tools" / "run_periodic_source_scan_queue.sh"
QUEUE_DOC = ROOT / "docs" / "knowledge" / "game-development" / "PERIODIC_SOURCE_SCAN_QUEUE.md"


class ZeroIncrementalCostPolicyTests(unittest.TestCase):
    def test_base_policy_fails_closed_on_incremental_or_uncertain_cost(self) -> None:
        agents = AGENTS.read_text(encoding="utf-8")
        for required in (
            "ZERO_INCREMENTAL_COST_REQUIRED",
            "COST_GATE_BLOCKED",
            "pay-as-you-go",
            "separately metered",
        ):
            self.assertIn(required, agents)

    def test_active_source_scheduler_has_no_metered_model_path(self) -> None:
        contract = "\n".join(
            path.read_text(encoding="utf-8")
            for path in (WORKFLOW, RUNNER, QUEUE_DOC)
        )
        for required in (
            "ZERO_INCREMENTAL_COST_QUEUE_PREP",
            "AWAITING_CHATGPT_REVIEW",
            "USER_DIRECTED_CHATGPT_REVIEW",
            "ai_api_call",
            "NONE",
        ):
            self.assertIn(required, contract)
        for forbidden in (
            "OPENAI_API_KEY",
            "SOURCE_ANALYSIS_MODEL",
            "python -m tools.periodic_source_analysis",
            "gh pr create",
            "gh workflow run validate-evidence-knowledge.yml",
            "gh workflow run validate-base-v9-rc.yml",
            "gh workflow run validate-game-project-operating-system.yml",
            "gh pr merge",
        ):
            self.assertNotIn(forbidden, contract)

    def test_queue_preparation_does_not_have_repository_or_pr_write_authority(self) -> None:
        workflow = WORKFLOW.read_text(encoding="utf-8")
        job_block = workflow.split("jobs:", 1)[1]
        self.assertIn("issues: write", job_block)
        for forbidden in (
            "actions: write",
            "contents: write",
            "pull-requests: write",
        ):
            self.assertNotIn(forbidden, job_block)


if __name__ == "__main__":
    unittest.main()
