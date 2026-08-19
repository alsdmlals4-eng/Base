from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXTERNAL_AI_SKILL = ROOT / "skills" / "orchestrating-deepseek-worktrees" / "SKILL.md"
MODEL_COST_SKILL = ROOT / "skills" / "optimizing-ai-model-and-prompt-costs" / "SKILL.md"
ROUTING_GUIDE = ROOT / "docs" / "knowledge" / "ai" / "SKILL_ROUTING_PRECISION_GUIDE.md"


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


if __name__ == "__main__":
    unittest.main()
