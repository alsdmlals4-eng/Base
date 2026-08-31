from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AI_KNOWLEDGE = ROOT / "docs" / "knowledge" / "ai"
REVIEW = (
    AI_KNOWLEDGE
    / "agent-tools"
    / "EXTERNAL_AGENT_TOOL_ADOPTION_REVIEW_2026-08-31.md"
)
ADAPTER = AI_KNOWLEDGE / "agent-tools" / "EXTERNAL_AGENT_ADAPTER_CONTRACT.md"
BRIEFING = AI_KNOWLEDGE / "READER_ADAPTIVE_ACTION_BRIEFING.md"
SOURCE_CATALOG = (
    ROOT
    / "skills"
    / "evaluating-godot-assets-and-plugins-before-creation"
    / "references"
    / "source-catalog.md"
)
FIRST_PROMPT = (
    ROOT
    / "skills"
    / "managing-project-intake-and-work-contract"
    / "references"
    / "first-prompt-direction-anchoring.md"
)
OLD_PACKAGED_REFERENCES = (
    ROOT
    / "skills"
    / "evaluating-godot-assets-and-plugins-before-creation"
    / "references"
    / "agent-tool-adoption-review-2026-08-31.md",
    ROOT
    / "skills"
    / "evaluating-godot-assets-and-plugins-before-creation"
    / "references"
    / "external-agent-adapter-contract.md",
    ROOT
    / "skills"
    / "managing-project-intake-and-work-contract"
    / "references"
    / "reader-adaptive-action-briefing.md",
)


class ExternalAgentToolAdoptionContractTests(unittest.TestCase):
    """Check documentation contracts; these are not external-tool runtime tests."""

    def test_shared_references_exist_without_creating_parallel_skills(self) -> None:
        for path in (REVIEW, ADAPTER, BRIEFING):
            with self.subTest(path=path):
                self.assertTrue(path.is_file(), f"missing contract reference: {path}")

        for path in OLD_PACKAGED_REFERENCES:
            with self.subTest(path=path):
                self.assertFalse(
                    path.exists(),
                    f"shared AI knowledge must not remain as an orphan skill reference: {path}",
                )

    def test_existing_owner_loaders_route_shared_references(self) -> None:
        source_catalog = SOURCE_CATALOG.read_text(encoding="utf-8")
        first_prompt = FIRST_PROMPT.read_text(encoding="utf-8")

        for relative_path in (
            "docs/knowledge/ai/agent-tools/EXTERNAL_AGENT_TOOL_ADOPTION_REVIEW_2026-08-31.md",
            "docs/knowledge/ai/agent-tools/EXTERNAL_AGENT_ADAPTER_CONTRACT.md",
        ):
            with self.subTest(relative_path=relative_path):
                self.assertIn(relative_path, source_catalog)

        self.assertIn(
            "docs/knowledge/ai/READER_ADAPTIVE_ACTION_BRIEFING.md",
            first_prompt,
        )

    def test_review_covers_every_candidate_and_records_bounded_dispositions(self) -> None:
        review = REVIEW.read_text(encoding="utf-8")
        for tool_id in (
            "i-have-adhd",
            "ballast",
            "ponytail",
            "open-code-review",
            "rtk",
            "eli5",
            "paperthin",
            "click",
            "antigravity-cli",
            "macro",
        ):
            with self.subTest(tool_id=tool_id):
                self.assertIn(f"`{tool_id}`", review)

        for marker in (
            "EVIDENCE_AS_OF: 2026-08-31",
            "AUTHORITATIVE_OWNER:",
            "NO_NEW_SKILL_REGISTRATION",
            "ADOPT",
            "ADAPT",
            "TRIAL_OPTIONAL",
            "REFERENCE_ONLY",
            "REJECT_AS_REQUIRED_DEPENDENCY",
            "REVALIDATION_TRIGGER",
            "ROLLBACK_BOUNDARY",
            "docs/knowledge/ai/agent-tools/EXTERNAL_AGENT_ADAPTER_CONTRACT.md",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, review)

        self.assertNotIn("`external-agent-adapter-contract.md`", review)

    def test_external_adapter_contract_preserves_authority_cost_and_raw_evidence(self) -> None:
        adapter = ADAPTER.read_text(encoding="utf-8")
        for marker in (
            "REPOSITORY_PRIMARY_CANON",
            "EXTERNAL_OUTPUT_ADVISORY_ONLY",
            "INSPECT_MUTATE_VERIFY_SEPARATION",
            "ARGV_ARRAY_EXECUTION",
            "SHELL_FALSE",
            "RAW_OUTPUT_FALLBACK_REQUIRED",
            "SOURCE_MODEL_VERSION_RECEIPT",
            "A_B_EVIDENCE_REQUIRED",
            "NO_HIDDEN_BILLING",
            "NO_PLAINTEXT_SECRET_OR_PROMPT_LOGGING",
            "BOUNDED_RETRY",
            "KILL_SWITCH_REQUIRED",
            "PROVIDER_NEUTRAL_CORE",
            "MACRO_OPTIONAL_ADAPTER",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, adapter)

        for forbidden in (
            "MACRO_PRIMARY_CANON",
            "AUTO_PAID_CREDITS",
            "TRUST_EXTERNAL_OUTPUT",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, adapter)

    def test_reader_briefing_reduces_load_without_diagnosis_or_time_promises(self) -> None:
        briefing = BRIEFING.read_text(encoding="utf-8")
        for marker in (
            "ACTION_FIRST_WHEN_ACTIONABLE",
            "CONCLUSION_FIRST_WHEN_DECISION_READY",
            "VISIBLE_STATE_AND_NEXT_ACTION",
            "KOREAN_BEGINNER_DEVELOPER_DEFAULT",
            "JARGON_DEFINE_ONCE_KEEP_IDENTIFIER",
            "PATH_COMMAND_REASON_VERIFICATION",
            "MATTER_OF_FACT_ERROR_REPORTING",
            "SAFETY_AND_UNCERTAINTY_OVERRIDE",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, briefing)

        for forbidden in (
            "ADHD_DIAGNOSIS_REQUIRED",
            "PROMISE_TIME_ESTIMATE",
            "UNIVERSAL_LIST_CAP",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, briefing)

    def test_review_lenses_cannot_claim_executed_or_independent_loops(self) -> None:
        review = REVIEW.read_text(encoding="utf-8")
        self.assertNotIn("## 6. Five adversarial review loops", review)
        for marker in (
            "REVIEW_LENSES_ARE_NOT_FULL_LOOPS",
            "FULL_LOOP_RECEIPT_REQUIRED",
            "SAME_AUTHOR_REVIEW_IS_NOT_INDEPENDENT_REVIEW",
            "EXTERNAL_TOOL_RUNTIME_NOT_RUN",
        ):
            self.assertIn(marker, review)

    def test_raw_fallback_preserves_command_outcome_without_side_effect_replay(self) -> None:
        adapter = ADAPTER.read_text(encoding="utf-8")
        for marker in (
            "RAW_CAPTURE_BEFORE_TRANSFORM",
            "PRESERVE_UPSTREAM_EXIT_STATUS",
            "NO_AUTOMATIC_COMMAND_REPLAY",
            "FILTER_FAILURE_IS_NOT_COMMAND_FAILURE",
        ):
            self.assertIn(marker, adapter)

    def test_receipts_distinguish_inapplicable_models_and_stale_evidence(self) -> None:
        adapter = ADAPTER.read_text(encoding="utf-8")
        self.assertIn("MODEL_NOT_APPLICABLE_FOR_DETERMINISTIC_TOOL", adapter)
        self.assertIn("FRESHNESS_BOUND_TO_REVISION_AND_INPUT", adapter)

    def test_trial_readiness_precedes_measurement_and_activation(self) -> None:
        adapter = ADAPTER.read_text(encoding="utf-8")
        for marker in (
            "DISPOSITION_NOT_INSTALLATION_AUTHORITY",
            "READINESS_PRECEDES_TRIAL",
            "TRIAL_EVIDENCE_PRECEDES_ACTIVATION",
            "TRIAL_APPROVED",
            "ADOPTED_ACTIVE",
        ):
            self.assertIn(marker, adapter)

    def test_briefing_does_not_invent_a_project_runner_or_inflate_zero_exit(self) -> None:
        briefing = BRIEFING.read_text(encoding="utf-8")
        self.assertNotIn("res://tests/run_all.gd", briefing)
        self.assertIn("DISCOVER_PROJECT_VALIDATOR_BEFORE_COMMAND", briefing)
        self.assertIn("ZERO_EXIT_IS_NOT_TEST_COVERAGE", briefing)

    def test_learning_and_absorption_are_owned_and_evidence_bounded(self) -> None:
        review = REVIEW.read_text(encoding="utf-8")
        for marker in (
            "## 8. Corrections and reusable learning",
            "CONTRACT_TESTS_ARE_NOT_BEHAVIOR_EVALUATIONS",
            "EXISTING_OWNER_REUSE_NOT_NEW_HOOK_IMPLEMENTATION",
            "UPSTREAM_BENCHMARK_NOT_LOCAL_A_B_RESULT",
        ):
            self.assertIn(marker, review)

    def test_future_running_mate_reference_does_not_authorize_implementation(self) -> None:
        adapter = ADAPTER.read_text(encoding="utf-8")
        self.assertIn("FUTURE_ARCHITECTURE_REFERENCE_ONLY", adapter)
        self.assertIn("NO_NEW_RUNNING_MATE_IMPLEMENTATION", adapter)
        self.assertNotIn("Build the running mate as", adapter)

    def test_ab_comparison_uses_isolated_equivalent_starting_state(self) -> None:
        adapter = ADAPTER.read_text(encoding="utf-8")
        for marker in (
            "A_B_ISOLATED_EQUIVALENT_STATE", "starting_state_hash",
            "separate disposable workspaces", "one intentional treatment difference",
            "order and cache conditions", "predeclared acceptance criteria",
        ):
            self.assertIn(marker, adapter)

    def test_token_estimates_do_not_claim_provider_usage_or_quota_savings(self) -> None:
        adapter = ADAPTER.read_text(encoding="utf-8")
        for marker in (
            "TOKEN_MEASUREMENT_KIND", "OBSERVED_PROVIDER", "BYTE_HEURISTIC",
            "UNAVAILABLE", "ESTIMATE_IS_NOT_PROVIDER_USAGE", "ChatGPT/Codex quota",
        ):
            self.assertIn(marker, adapter)
        self.assertNotIn(
            "public counter-evidence includes low-output overhead",
            REVIEW.read_text(encoding="utf-8"),
        )

    def test_explicit_decisions_are_not_delayed_until_recurrence(self) -> None:
        review = REVIEW.read_text(encoding="utf-8")
        self.assertIn("EXPLICIT_USER_DECISION_IS_NOT_LEARNED_HEURISTIC", review)
        self.assertIn("Record an explicit user-approved decision immediately", review)
        self.assertNotIn("Promote only repeated evidence-backed corrections", review)

    def test_absorption_and_learning_remain_under_existing_owners(self) -> None:
        review = REVIEW.read_text(encoding="utf-8")
        for marker in (
            "NEW_REFERENCE_ROUTING", "REUSED_EXISTING_CONTRACT",
            "CONTRACT_ONLY_NO_HOOK_ENFORCEMENT", "OPTIONAL_TOOL_NOT_ACTIVATED",
            "skills/evolving-project-discipline-skills/SKILL.md",
            "skills/reviewing-and-validating-project-changes/SKILL.md",
            "skills/evaluating-godot-assets-and-plugins-before-creation/LEARNING_LOG.md",
            "GDScript-specific review quality remains unverified",
        ):
            self.assertIn(marker, review)

    def test_project_pin_and_valid_scoped_approval_are_preserved(self) -> None:
        adapter = ADAPTER.read_text(encoding="utf-8")
        for marker in (
            "PROJECT_ADOPTED_VERSION_REMAINS_AUTHORITY", "REUSE_VALID_SCOPED_APPROVAL",
            "NO_SILENT_PROJECT_ROLLOUT", "current project AGENTS.md",
            "before any remote write or merge",
        ):
            self.assertIn(marker, adapter)
        self.assertNotIn("human approval obtained for any cost, auth, external write", adapter)


if __name__ == "__main__":
    unittest.main()
