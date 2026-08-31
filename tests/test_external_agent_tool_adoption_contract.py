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
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, review)

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


if __name__ == "__main__":
    unittest.main()
