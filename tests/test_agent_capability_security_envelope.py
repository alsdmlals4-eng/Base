from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SECURITY = (
    ROOT
    / "docs"
    / "knowledge"
    / "ai"
    / "agent-tools"
    / "AGENT_CAPABILITY_SECURITY_ENVELOPE.md"
)
ADAPTER = (
    ROOT
    / "docs"
    / "knowledge"
    / "ai"
    / "agent-tools"
    / "EXTERNAL_AGENT_ADAPTER_CONTRACT.md"
)
SOURCE_CATALOG = (
    ROOT
    / "skills"
    / "evaluating-godot-assets-and-plugins-before-creation"
    / "references"
    / "source-catalog.md"
)


class AgentCapabilitySecurityEnvelopeTests(unittest.TestCase):
    """Contract checks only; these are not runtime security tests."""

    def test_existing_owner_routes_security_contract_without_a_new_skill(self) -> None:
        self.assertTrue(SECURITY.is_file(), f"missing security contract: {SECURITY}")
        security = SECURITY.read_text(encoding="utf-8")
        catalog = SOURCE_CATALOG.read_text(encoding="utf-8")

        self.assertIn(
            "docs/knowledge/ai/agent-tools/AGENT_CAPABILITY_SECURITY_ENVELOPE.md",
            catalog,
        )
        for marker in (
            "AUTHORITATIVE_OWNER: skills/evaluating-godot-assets-and-plugins-before-creation/SKILL.md",
            "NO_NEW_SKILL_REGISTRATION",
            "EXTERNAL_AGENT_ADAPTER_CONTRACT.md",
        ):
            self.assertIn(marker, security)

    def test_contract_covers_the_full_context_to_harness_stack(self) -> None:
        security = SECURITY.read_text(encoding="utf-8")
        for marker in (
            "MODEL_AND_MULTIMODAL_INPUT_BOUNDARY",
            "KNOWLEDGE_AND_RAG_BOUNDARY",
            "MCP_AND_TOOL_BOUNDARY",
            "AGENT_DELEGATION_BOUNDARY",
            "WORKFLOW_EFFECT_BOUNDARY",
            "HARNESS_POLICY_BOUNDARY",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, security)

    def test_retrieval_authorization_and_provenance_precede_relevance(self) -> None:
        security = SECURITY.read_text(encoding="utf-8")
        for marker in (
            "EXTERNAL_CONTENT_IS_UNTRUSTED_DATA",
            "RETRIEVAL_AUTHORIZATION_BEFORE_RELEVANCE",
            "PROVENANCE_AND_CONFIDENTIALITY_PROPAGATE",
            "SUMMARY_DOES_NOT_LAUNDER_TRUST",
            "VECTOR_ID_IS_NOT_AUTHORIZATION",
            "RETRIEVED_INSTRUCTIONS_DO_NOT_GAIN_AUTHORITY",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, security)

    def test_delegation_cannot_amplify_permissions_or_hide_approval(self) -> None:
        security = SECURITY.read_text(encoding="utf-8")
        for marker in (
            "DELEGATED_CAPABILITY_SUBSET_ONLY",
            "PARENT_CANNOT_GRANT_UNHELD_CAPABILITY",
            "ROOT_APPROVAL_SURFACE_PRESERVED",
            "STICKY_APPROVAL_DOES_NOT_CROSS_IDENTITY",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, security)

    def test_mcp_authorization_is_effect_scoped_and_token_safe(self) -> None:
        security = SECURITY.read_text(encoding="utf-8")
        for marker in (
            "EFFECT_BASED_DENY_ASK_ALLOW",
            "APPROVAL_BOUND_TO_CALL_IDENTITY",
            "TOKEN_AUDIENCE_BOUND_NO_PASSTHROUGH",
            "SENSITIVE_AUTH_OUT_OF_BAND",
            "TOOL_DESCRIPTION_AND_OUTPUT_UNTRUSTED_BY_DEFAULT",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, security)

    def test_harness_enforces_policy_beyond_prompt_wording(self) -> None:
        security = SECURITY.read_text(encoding="utf-8")
        for marker in (
            "HARNESS_ENFORCEMENT_NOT_PROMPT_ONLY",
            "FAIL_CLOSED_ON_UNKNOWN_POLICY",
            "PRE_TOOL_AND_POST_TOOL_GUARD_REQUIRED",
            "KILL_SWITCH_AND_REVOCATION",
            "POLICY_RECEIPT_REQUIRED",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, security)

    def test_contract_does_not_claim_runtime_enforcement_or_paid_adoption(self) -> None:
        security = SECURITY.read_text(encoding="utf-8")
        adapter = ADAPTER.read_text(encoding="utf-8")

        for marker in (
            "CONTRACT_ONLY_NO_RUNTIME_ENFORCEMENT",
            "CONTRACT_TESTS_ARE_NOT_SECURITY_BEHAVIOR_TESTS",
            "ZERO_INCREMENTAL_COST_DEFAULT",
            "PROJECT_ADOPTION_REQUIRES_RUNTIME_EVIDENCE",
        ):
            self.assertIn(marker, security)

        for forbidden in (
            "PROMPT_ONLY_DEFENSE_IS_SUFFICIENT",
            "CHILD_AGENT_INHERITS_ALL_TOOLS",
            "TOKEN_PASSTHROUGH_ALLOWED",
            "AUTO_APPROVE_BY_TOOL_NAME_ONLY",
            "PAID_AI_FIREWALL_REQUIRED",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, security)
                self.assertNotIn(forbidden, adapter)


if __name__ == "__main__":
    unittest.main()
