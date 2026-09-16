from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ACTIVE_CONSUMERS = (
    "docs/BASE_SHARED_SKILL_ADAPTER_CONTRACT.md",
    "templates/planning/EXECUTION_SEQUENCE_PLAN.md",
    "templates/project-operations/AI_WORKFLOW.md",
    "templates/project-operations/PROJECT_START_HERE.md",
    "templates/project-operations/.agents/skills/base-project-router/SKILL.md",
    "templates/project-operations/PROJECT_WORK_ITEM_CHECKLIST.md",
    "templates/project-operations/WORK_PROJECT_EXECUTION_CURRENT_ROUTER.md",
    "templates/project-operations/WORK_PROJECT_START_CANON_CHECKLIST.md",
    "templates/project-operations/WORK_CODEX_MINIMUM_TRANSITION_STARTER_PROMPT.md",
)


class PromptApprovalActiveConsumerTests(unittest.TestCase):
    def test_every_active_start_consumer_exposes_prepare_confirm_execute(self) -> None:
        for relative in ACTIVE_CONSUMERS:
            text = (ROOT / relative).read_text(encoding="utf-8")
            with self.subTest(path=relative):
                self.assertIn("PROMPT_APPROVAL_EXECUTION_GATE_REQUIRED", text)
                self.assertIn("PROMPT_APPROVAL_GATE_RECEIPT.json", text)
                self.assertIn("--phase prepare", text)
                self.assertIn("--expected-source-sha", text)
                self.assertIn("--render-markdown", text)
                self.assertIn("EXECUTION AUTHORIZED: NO", text)
                self.assertIn("CONFIRMED", text)
                self.assertIn("REUSED_APPROVAL", text)
                self.assertIn("--phase start", text)
                self.assertIn("--phase resume", text)
                self.assertIn("prompt-approval-execution-gate.md", text)

    def test_active_consumers_link_instead_of_copying_the_full_schema(self) -> None:
        for relative in ACTIVE_CONSUMERS:
            text = (ROOT / relative).read_text(encoding="utf-8")
            section = text.rsplit("## Prompt approval execution gate", 1)[-1]
            with self.subTest(path=relative):
                self.assertEqual(1, text.count("PROMPT_APPROVAL_EXECUTION_GATE_REQUIRED"))
                self.assertNotIn('"schema_version"', section)
                self.assertNotIn('"context_and_sources"', section)
                self.assertNotIn('"approved_contract_sha256"', section)


if __name__ == "__main__":
    unittest.main()
