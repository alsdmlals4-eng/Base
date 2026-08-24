from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AGENTS = ROOT / "AGENTS.md"


class AgentsAlwaysOnContextContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.agents = AGENTS.read_text(encoding="utf-8")

    def test_agents_declares_progressive_loading_for_detailed_contracts(self) -> None:
        self.assertIn("ALWAYS_ON_CONTEXT_ONLY", self.agents)
        self.assertIn("PROGRESSIVE_LOAD_DETAILED_CONTRACTS", self.agents)
        for owner in (
            "docs/OPERATING_MODEL.md",
            "docs/WORK_MODE_AND_SKILL_ROUTING.md",
            "docs/LONG_HORIZON_WORK_EXECUTION_POLICY.md",
            "skills/managing-project-intake-and-work-contract/references/continuous-work-execution.md",
            "docs/knowledge/game-development/PLATFORM_REVIEW_ASSET_RIGHTS_AND_REFERENCE_PRODUCTION_GUIDE.md",
        ):
            with self.subTest(owner=owner):
                self.assertIn(owner, self.agents)

    def test_detailed_playbooks_are_not_duplicated_in_always_on_context(self) -> None:
        for detail in (
            "## 4.1 플랫폼 심사·자산 권리 불변 규칙",
            "content_rating_target",
            "target_audience",
            "CONTINUATION_INTENT_ALIASES",
            "전체 범위 공격 → finding 검증",
        ):
            with self.subTest(detail=detail):
                self.assertNotIn(detail, self.agents)

    def test_slimming_preserves_always_on_safety_and_authority(self) -> None:
        for invariant in (
            "사용자의 최신 지시",
            "BLOCKED_UNVERIFIED",
            "OPEN_PR_READ_ONLY_BY_DEFAULT",
            "CURRENT_TASK_CONTINUATION_AUTHORIZES_READY_MERGE",
            "ADVERSARIAL_REVIEW_UNTIL_CLEAN",
            "FULL_LOOP_COUNT_MINIMUM: 5",
            "MINIMUM_FULL_LOOPS_BEFORE_CLEAN_EXIT: 5",
            "CURRENT_STATE_BENCHMARK_ALTERNATIVE_TRADE_STUDY",
            "MINIMUM_VIABLE_ALTERNATIVES: 3",
            "CURRENT_PAID_PLANS: GPT_PRO",
            "PAID_PLAN_COUNT: 1",
            "NOTION_DEFAULT_PROJECT_WORKSPACE",
            "PROJECT_RELATION_REQUIRED",
            "RELEASE_BLOCKED_UNVERIFIED",
            "secure_original_location",
        ):
            with self.subTest(invariant=invariant):
                self.assertIn(invariant, self.agents)


if __name__ == "__main__":
    unittest.main()
