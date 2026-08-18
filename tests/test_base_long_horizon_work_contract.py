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
            "FIVE_DISTINCT_ADVERSARIAL_ROUNDS",
            "REQUIRED_WORK_REMAINING",
            "FIGMA_DEFAULT_VISUAL_WORKSPACE",
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
            "FIVE_DISTINCT_ADVERSARIAL_ROUNDS",
            "POSTMERGE_PROMOTION_AND_SUPERSESSION",
            "REQUIRED_WORK_REMAINING: 0",
        ):
            self.assertIn(term, policy)

    def test_claims_require_executed_current_comparison_benchmark_and_review_evidence(self) -> None:
        policy = read("docs/LONG_HORIZON_WORK_EXECUTION_POLICY.md")
        for term in (
            "EXECUTION_EVIDENCE_BEFORE_CLAIM",
            "CURRENT_STATE_COMPARISON_REQUIRED",
            "benchmark_sources",
            "commands_or_queries",
            "observed_results",
            "NOT_RUN",
            "BLOCKED_UNVERIFIED",
        ):
            self.assertIn(term, policy)

        review = read("skills/running-adversarial-review-and-refinement/SKILL.md")
        for term in (
            "EXECUTION_EVIDENCE_BEFORE_CLAIM",
            "current_state_baseline",
            "evidence_locator",
            "benchmark_sources",
            "observed_results",
        ):
            self.assertIn(term, review)

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

    def test_visual_and_structured_data_authority_is_split_safely(self) -> None:
        policy = read("docs/LONG_HORIZON_WORK_EXECUTION_POLICY.md")
        for term in (
            "FIGMA_DEFAULT_VISUAL_WORKSPACE",
            "REPO_NATIVE_STRUCTURED_DATA",
            "GOOGLE_SHEETS_LEGACY_MIGRATION_SOURCE",
            "EXTERNAL_HTML_TOOL_CATALOG: DERIVED_DISCOVERY_SURFACE",
            "TOOL_HUB: REQUIRED_WHEN_RELEVANT",
            "LOOP_ENGINEERING: REQUIRED_WHEN_RELEVANT",
        ):
            self.assertIn(term, policy)

    def test_figma_professional_workflow_does_not_depend_on_unavailable_branching(self) -> None:
        policy = read("docs/VISUAL_COLLABORATION_TOOL_POLICY.md")
        profile = read("templates/project-operations/FIGMA_VISUAL_BIBLE_PROFILE.md")
        for text in (policy, profile):
            self.assertIn("FIGMA_PRO_BRANCHING_NOT_ASSUMED", text)
            self.assertIn("Professional", text)
            self.assertIn("version history", text)
            self.assertIn("Pages/Sections", text)

    def test_adversarial_review_owner_requires_exactly_five_distinct_rounds_when_invoked(self) -> None:
        skill = read("skills/running-adversarial-review-and-refinement/SKILL.md")
        for term in (
            "FIVE_DISTINCT_ADVERSARIAL_ROUNDS: REQUIRED_WHEN_REVIEW_RUNS",
            "ROUND_1_INTENT_ASSUMPTIONS_SCOPE",
            "ROUND_2_CANON_STRUCTURE_DEPENDENCIES",
            "ROUND_3_FAILURE_SECURITY_CONCURRENCY",
            "ROUND_4_VALUE_BENCHMARK_COST_MAINTAINABILITY",
            "ROUND_5_REGRESSION_EVIDENCE_COMPLETION_FRESHNESS",
        ):
            self.assertIn(term, skill)

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


if __name__ == "__main__":
    unittest.main()
