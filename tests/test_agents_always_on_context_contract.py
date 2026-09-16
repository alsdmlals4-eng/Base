from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AGENTS = ROOT / "AGENTS.md"


class AgentsAlwaysOnContextContractTests(unittest.TestCase):
    def test_source_blocker_is_dependency_scoped_not_blanket_stop(self) -> None:
        self.assertIn("SOURCE_DEPENDENCY_SCOPED_BLOCKER", self.agents)
        self.assertNotIn("다른 독립 작업으로 임의 전환하지 않는다", self.agents)
        self.assertIn("사용자가 전체 중단", self.agents)

    def test_proportionate_research_and_tool_routing_are_explicit(self) -> None:
        owner = (ROOT / "docs/LONG_HORIZON_WORK_EXECUTION_POLICY.md").read_text(encoding="utf-8")
        self.assertIn("IMPORTANT_DECISION_ALTERNATIVES_ONLY", owner)
        self.assertIn("이미 승인된", owner)
        routing = (ROOT / "skills/managing-project-intake-and-work-contract/references/external-source-and-tool-routing.md").read_text(encoding="utf-8")
        self.assertIn("GODOT_CONSUMER_SCOPED_TOOL_ROUTE", routing)
        self.assertIn("비-Godot", routing)

    def test_start_and_godot_evaluator_keep_consumer_scoped_entrypoints(self) -> None:
        start = (ROOT / "START_HERE.md").read_text(encoding="utf-8")
        evaluation = (ROOT / "skills/evaluating-godot-assets-and-plugins-before-creation/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("GODOT_CONSUMER_SCOPED_TOOL_ROUTE", start)
        for body in (start, evaluation):
            self.assertIn("Godot consumer가 없는", body)
            self.assertIn("실제 Godot 엔진·저작·씬·리소스 consumer가 있는", body)
        route = next(line for line in start.splitlines() if line.startswith('|') and 'inventory-current-environment / disposition' in line)
        self.assertIn("Godot consumer가 있는", route.split('|')[1])
        self.assertNotIn("요청은 설계보다 먼저", start)

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
            "FULL_LOOP_COUNT_MINIMUM: 2",
            "MINIMUM_FULL_LOOPS_BEFORE_CLEAN_EXIT: 2",
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
