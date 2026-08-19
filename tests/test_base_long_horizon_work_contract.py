from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


class BaseLongHorizonWorkContractTests(unittest.TestCase):
    def test_entrypoint_routes_long_horizon_policy(self) -> None:
        agents = read("AGENTS.md")
        self.assertIn("docs/LONG_HORIZON_WORK_EXECUTION_POLICY.md", agents)
        for term in (
            "ADVERSARIAL_REVIEW_UNTIL_CLEAN",
            "FULL_LOOP_COUNT_MINIMUM: 5",
            "MINIMUM_FULL_LOOPS_BEFORE_CLEAN_EXIT: 5",
            "REQUIRED_WORK_REMAINING",
            "NOTION_DEFAULT_PROJECT_WORKSPACE",
            "PROJECT_RELATION_REQUIRED",
        ):
            self.assertIn(term, agents)

    def test_policy_covers_direction_completion_recovery_and_cost(self) -> None:
        policy = read("docs/LONG_HORIZON_WORK_EXECUTION_POLICY.md")
        for term in (
            "DIRECTION_FIRST",
            "BENCHMARK_SYNTHESIS",
            "EXPECTED_EFFECTS_RISKS_MITIGATIONS_BEFORE_BUILD",
            "SINGLE_INITIAL_APPROVAL_THEN_CONTINUE",
            "RECOVER_TRY_ALTERNATIVES_RESUME",
            "ZERO_INCREMENTAL_COST_REQUIRED",
            "ADVERSARIAL_REVIEW_UNTIL_CLEAN",
            "FULL_LOOP_COUNT_MINIMUM: 5",
            "MINIMUM_FULL_LOOPS_BEFORE_CLEAN_EXIT: 5",
            "POSTMERGE_PROMOTION_AND_SUPERSESSION",
            "REQUIRED_WORK_REMAINING: 0",
        ):
            self.assertIn(term, policy)

    def test_material_decisions_require_current_state_alternatives_and_benchmark_synthesis(self) -> None:
        agents = read("AGENTS.md")
        policy = read("docs/LONG_HORIZON_WORK_EXECUTION_POLICY.md")
        for term in (
            "최신 main",
            "실제 구현",
            "최소 3개",
            "되돌리기 난이도",
            "더 나은 방안",
            "장기계획",
        ):
            self.assertIn(term, agents)
        for term in (
            "벤치마킹은 한 성공사례를 모방하는 절차가 아니다",
            "실무사례·실패사례를 여러 개 비교",
            "ADOPT / ADAPT / REJECT",
            "장기적으로 더 강한 방안",
        ):
            self.assertIn(term, policy)

    def test_base_explicitly_requires_three_or_more_options_and_long_term_selection(self) -> None:
        agents = read("AGENTS.md")
        policy = read("docs/LONG_HORIZON_WORK_EXECUTION_POLICY.md")
        for text in (agents, policy):
            for term in (
                "CURRENT_STATE_BENCHMARK_ALTERNATIVE_TRADE_STUDY",
                "MINIMUM_VIABLE_ALTERNATIVES: 3",
                "BETTER_ALTERNATIVE_SEARCH",
                "LONG_TERM_PLAN_FIT_REQUIRED",
                "현행 조사",
                "최소 3개",
            ):
                self.assertIn(term, text)
        self.assertIn("장기적으로 최선", policy)

    def test_default_paid_plan_and_notion_free_cost_boundary(self) -> None:
        agents = read("AGENTS.md")
        policy = read("docs/LONG_HORIZON_WORK_EXECUTION_POLICY.md")
        for text in (agents, policy):
            for term in (
                "CURRENT_PAID_PLANS: GPT_PRO",
                "PAID_PLAN_COUNT: 1",
                "GPT Pro",
                "Notion",
                "새 사용자 승인",
            ):
                self.assertIn(term, text)
            self.assertNotIn("CURRENT_PAID_PLANS: GPT_PRO, FIGMA_PRO", text)

    def test_execution_and_external_claims_are_fail_closed_by_existing_verification_owner(self) -> None:
        verification = read(
            "skills/reviewing-and-validating-project-changes/references/claim-and-intent-verification.md"
        )
        for term in (
            "MATERIAL_CLAIM_LEDGER",
            "EXTERNAL_FACT",
            "evidence_locator",
            "Evidence ceiling",
            "LATEST_EXACT_HEAD_ONLY",
            "TEST_CONSUMPTION_PROOF",
            "BLOCKED_UNVERIFIED",
        ):
            self.assertIn(term, verification)

    def test_independent_workstreams_are_isolated_unless_user_explicitly_authorizes_absorption(self) -> None:
        policy = read("docs/LONG_HORIZON_WORK_EXECUTION_POLICY.md")
        for term in (
            "INDEPENDENT_WORKSTREAM_ISOLATION",
            "OTHER_CHAT_BRANCH_PATH_PR: DO_NOT_TOUCH_BY_DEFAULT",
            "EXPLICIT_USER_ABSORPTION_AUTHORIZATION: REQUIRED_FOR_EXCEPTION",
        ):
            self.assertIn(term, policy)

    def test_game_contract_is_budgeted_buildable_and_reusable(self) -> None:
        policy = read("docs/LONG_HORIZON_WORK_EXECUTION_POLICY.md")
        for term in (
            "CORE_LOOP_DUMMY_BALANCE_BUILD_TEST",
            "BALANCE_BUDGET",
            "WORLD_STORYLINE_FIT_REQUIRED",
            "REUSABLE_SYSTEM_EXTRACTION",
            "ADOPT / ADAPT / REJECT",
        ):
            self.assertIn(term, policy)

    def test_notion_visual_and_structured_data_authority_is_split_safely(self) -> None:
        policy = read("docs/LONG_HORIZON_WORK_EXECUTION_POLICY.md")
        for term in (
            "NOTION_DEFAULT_PROJECT_WORKSPACE",
            "PROJECT_RELATION_REQUIRED",
            "WORK_MASTER",
            "ASSET_KNOWLEDGE_MASTER",
            "VISUAL_MAP_DERIVED",
            "REPO_NATIVE_STRUCTURED_DATA",
            "GOOGLE_SHEETS_MIGRATION_ONLY_UNTIL_REMOVAL",
            "EXTERNAL_HTML_WORKSPACE_RETIRED",
            "LOOP_ENGINEERING: REQUIRED_WHEN_RELEVANT",
        ):
            self.assertIn(term, policy)

    def test_deprecated_figma_and_tool_hub_are_not_active_long_horizon_authorities(self) -> None:
        policy = read("docs/LONG_HORIZON_WORK_EXECUTION_POLICY.md")
        visual_policy = read("docs/VISUAL_COLLABORATION_TOOL_POLICY.md")
        self.assertNotIn("FIGMA_DEFAULT_VISUAL_WORKSPACE", policy)
        self.assertNotIn("TOOL_HUB: REQUIRED_WHEN_RELEVANT", policy)
        self.assertNotIn("FIGMA_DEFAULT_VISUAL_WORKSPACE", visual_policy)
        self.assertIn("NOTION_DEFAULT_PROJECT_WORKSPACE", visual_policy)

    def test_adversarial_review_requires_minimum_five_then_until_clean(self) -> None:
        skill = read("skills/running-adversarial-review-and-refinement/SKILL.md")
        for term in (
            "ADVERSARIAL_REVIEW_UNTIL_CLEAN: REQUIRED_WHEN_REVIEW_RUNS",
            "FULL_LOOP_COUNT_MINIMUM: 5",
            "MINIMUM_FULL_LOOPS_BEFORE_CLEAN_EXIT: 5",
            "FULL_SCOPE_REVIEW",
            "FIND → VALIDATE → REFINE → VERIFY → RE-ATTACK",
            "BETTER_ALTERNATIVE_SEARCH",
            "LONG_TERM_PLAN_FIT_RECHECK",
            "CLEAN_REVIEW_EXIT",
            "최소 5회의 완전한 전체 개선 루프",
            "5회 이후에도",
            "새로운 유효 오류·충돌·누락·blocking finding이 0",
        ):
            self.assertIn(term, skill)
        self.assertNotIn("FIVE_DISTINCT_ADVERSARIAL_ROUNDS", skill)
        self.assertNotIn("ROUND_1_INTENT_ASSUMPTIONS_SCOPE", skill)

    def test_loop_foundation_doc_points_to_current_operational_checkpoint(self) -> None:
        loop_doc = read("docs/LOOP_ENGINEERING_A2_RUNTIME.md")
        self.assertIn("SUPERSEDED_STATUS_SNAPSHOT", loop_doc)
        self.assertIn("docs/operations/UNIVERSAL_LOOP_CROSS_PROJECT_ACCEPTANCE.json", loop_doc)
        self.assertNotIn(
            "The real Codex Builder and GPT Critic are not implemented by the current runtime.",
            loop_doc,
        )

    def test_loop_preserves_package_and_product_selection_as_distinct_human_gates(self) -> None:
        loop_doc = read("docs/LOOP_ENGINEERING_A2_RUNTIME.md")
        self.assertIn("AUTOMATIC_PACKAGE_SELECTION: FORBIDDEN", loop_doc)
        self.assertIn("AUTOMATIC_PRODUCT_SCOPE_SELECTION: FORBIDDEN", loop_doc)
        self.assertIn("둘은 서로 다른 권한 경계", loop_doc)

    def test_sparse_skill_routing_is_wired_without_expanding_registry(self) -> None:
        guide = ROOT / "docs/knowledge/ai/SKILL_ROUTING_PRECISION_GUIDE.md"
        self.assertTrue(guide.exists())
        text = guide.read_text(encoding="utf-8")
        for term in (
            "DEFAULT_SUPPORTING_SKILL_BUDGET: 1",
            "SECOND_SUPPORTING_SKILL: EXCEPTION_ONLY",
            "FULL_SKILL_BODY_TIE_BREAK: REQUIRED",
            "FUNCTIONAL_OVERLAP: REUSE_ABSORB_MERGE_FIRST",
        ):
            self.assertIn(term, text)

    def test_gpt_first_visualized_poc_legacy_removal_and_clean_review_contract(self) -> None:
        agents = read("AGENTS.md")
        policy = read("docs/LONG_HORIZON_WORK_EXECUTION_POLICY.md")
        codex = read("docs/GPT_CODEX_WORKFLOW_POLICY.md")
        visual = read("docs/VISUAL_COLLABORATION_TOOL_POLICY.md")
        sheets = read("docs/PROJECT_GDD_GOOGLE_SHEETS_POLICY.md")
        adversarial = read("skills/running-adversarial-review-and-refinement/SKILL.md")
        for token in (
            "ADVERSARIAL_REVIEW_UNTIL_CLEAN",
            "CLEAN_REVIEW_EXIT",
            "GPT_FIRST_PLANNING_AND_REVIEW",
            "OPTIONAL_CODEX_EXECUTOR",
            "VISUALIZED_POC_BEFORE_DEMO_TEST",
            "LEGACY_ABSORB_VERIFY_REMOVE",
            "PAID_PLAN_GATE",
        ):
            self.assertIn(token, policy if token not in ("CLEAN_REVIEW_EXIT",) else policy + adversarial + agents)
        self.assertIn("사용자 학습형 완료보고", agents)
        self.assertIn("GPT_FIRST_PLANNING_AND_REVIEW", codex)
        self.assertIn("OPTIONAL_CODEX_EXECUTOR", codex)
        self.assertIn("VISUALIZED_POC_BEFORE_DEMO_TEST", visual)
        self.assertIn("MIGRATION_ONLY_UNTIL_REMOVAL", sheets)
        self.assertIn("FULL_LOOP_COUNT_MINIMUM: 5", adversarial)
        self.assertIn("MINIMUM_FULL_LOOPS_BEFORE_CLEAN_EXIT: 5", adversarial)
        self.assertNotIn("FIVE_DISTINCT_ADVERSARIAL_ROUNDS", adversarial)


if __name__ == "__main__":
    unittest.main()
