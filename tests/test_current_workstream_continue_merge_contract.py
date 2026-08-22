from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


class CurrentWorkstreamContinueMergeContractTests(unittest.TestCase):
    def test_current_workstream_continue_authorizes_normal_lifecycle_through_merge(self) -> None:
        owners = (
            read("AGENTS.md"),
            read("docs/LONG_HORIZON_WORK_EXECUTION_POLICY.md"),
            read("skills/synchronizing-local-and-github-state/SKILL.md"),
            read("skills/synchronizing-local-and-github-state/references/safe-sync-protocol.md"),
        )

        for text in owners:
            self.assertIn("CURRENT_WORKSTREAM_CONTINUE_INCLUDES_MERGE", text)
            self.assertIn("EXACT_HEAD_REQUIRED_CHECKS_PASS", text)
            self.assertIn("POSTMERGE_READBACK_REQUIRED", text)

        agents = owners[0]
        for phrase in (
            "진행해",
            "계속 진행해",
            "남은 작업 전부 진행해",
        ):
            self.assertIn(phrase, agents)

    def test_continuation_exception_does_not_authorize_foreign_or_unsafe_pr_mutation(self) -> None:
        agents = read("AGENTS.md")
        policy = read("docs/LONG_HORIZON_WORK_EXECUTION_POLICY.md")
        skill = read("skills/synchronizing-local-and-github-state/SKILL.md")
        protocol = read("skills/synchronizing-local-and-github-state/references/safe-sync-protocol.md")
        combined = "\n".join((agents, policy, skill, protocol))

        for token in (
            "OPEN_PR_READ_ONLY_BY_DEFAULT",
            "OPEN_PR_MUTATION_REQUIRES_EXPLICIT_NAMED_AUTHORIZATION",
            "CURRENT_WORKSTREAM_IDENTITY_REQUIRED",
            "FOREIGN_OR_UNKNOWN_WORKSTREAM_REQUIRES_NAMED_AUTHORIZATION",
            "EXPLICIT_STOP_BEFORE_MERGE_OVERRIDES_CONTINUATION",
            "BLOCK_ON_FAILED_OR_PENDING_REQUIRED_CHECKS",
            "NO_FORCE_PUSH_OR_GOVERNANCE_BYPASS",
            "SEMANTIC_CONFLICT_REQUIRES_USER_DECISION",
        ):
            self.assertIn(token, combined)

    def test_continuation_contract_covers_conflict_reconciliation_without_scope_expansion(self) -> None:
        protocol = read("skills/synchronizing-local-and-github-state/references/safe-sync-protocol.md")
        for token in (
            "CURRENT_WORKSTREAM_CONTINUE_INCLUDES_MERGE",
            "bounded current-PR conflict reconciliation",
            "preserve latest completed `main`",
            "preserve approved current-workstream semantics",
            "re-run exact-head checks",
            "post-merge main readback",
        ):
            self.assertIn(token, protocol)


if __name__ == "__main__":
    unittest.main()
