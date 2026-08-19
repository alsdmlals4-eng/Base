from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


class ConcurrentGitSyncPreflightContractTests(unittest.TestCase):
    def test_sync_skill_fails_closed_on_concurrent_change_evidence(self) -> None:
        skill = read("skills/synchronizing-local-and-github-state/SKILL.md")

        for token in (
            "CONCURRENT_CHANGE_PREFLIGHT",
            "current_task_or_pr_identity",
            "source_main_sha",
            "current_main_sha",
            "write_parent_sha",
            "expected_head_sha",
            "PENDING_FIRST_WRITE",
            "intended_paths",
            "semantic_resource_locks",
            "same_goal_open_and_recent_prs",
            "open_pr_changed_paths",
            "CLEAR",
            "STALE_BASE_SHA",
            "WAITING_RESOURCE",
            "DUPLICATE_WORK",
            "BLOCKED_UNVERIFIED",
        ):
            self.assertIn(token, skill)

    def test_safe_sync_protocol_rechecks_before_write_pr_merge_and_after_merge(self) -> None:
        protocol = read(
            "skills/synchronizing-local-and-github-state/references/safe-sync-protocol.md"
        )

        for token in (
            "first persistent write",
            "PR creation",
            "merge",
            "post-merge main readback",
            "current_task_or_pr_identity",
            "write_parent_sha",
            "PENDING_FIRST_WRITE",
            "exclude the current task or PR itself",
            "PATH_OVERLAP",
            "SEMANTIC_OVERLAP",
            "SAME_GOAL",
            "UNKNOWN",
            "cooperative",
        ):
            self.assertIn(token, protocol)

    def test_copy_integration_standing_authorization_reconciles_before_merge(self) -> None:
        agents = read("AGENTS.md")
        skill = read("skills/synchronizing-local-and-github-state/SKILL.md")
        protocol = read(
            "skills/synchronizing-local-and-github-state/references/safe-sync-protocol.md"
        )

        for text in (agents, skill, protocol):
            self.assertIn("PROVISIONAL_INTEGRATION", text)
            self.assertIn("BASE_COPY_INTEGRATION_STANDING_AUTHORIZATION_2026_08_16", text)

        for token in (
            "owner PR branches",
            "semantic reconciliation",
            "exact-head",
            "selective copy",
            "absorbed_owner_deltas",
            "residual_owner_deltas",
        ):
            self.assertIn(token, protocol)

        self.assertIn("owner_pr_head_shas", skill)
        self.assertIn("provisional_overlap_paths", skill)
        self.assertIn("provisional_semantic_resources", skill)
        self.assertIn("absorbed_owner_deltas", skill)
        self.assertIn("residual_owner_deltas", skill)
        self.assertIn("standing authorization", skill)
        self.assertIn("owner PR", agents)
        self.assertIn("latest completed `main`", agents)
        self.assertIn("superseded", agents)

    def test_open_pr_requires_current_owner_evidence_before_protection(self) -> None:
        agents = read("AGENTS.md")
        skill = read("skills/synchronizing-local-and-github-state/SKILL.md")
        protocol = read(
            "skills/synchronizing-local-and-github-state/references/safe-sync-protocol.md"
        )
        policy = read("docs/LONG_HORIZON_WORK_EXECUTION_POLICY.md")

        for text in (agents, skill, protocol, policy):
            self.assertIn("OPEN_PR_IS_NOT_ACTIVE_WORKSTREAM", text)
            self.assertIn("ACTIVE_OTHER_WORKER", text)

        for text in (skill, protocol, policy):
            self.assertIn("CURRENT_OWNER_EVIDENCE_REQUIRED", text)
            self.assertNotIn("OTHER_CHAT_BRANCH_PATH_PR: DO_NOT_TOUCH_BY_DEFAULT", text)
            self.assertNotIn("EXPLICIT_USER_ABSORPTION_AUTHORIZATION: REQUIRED_FOR_EXCEPTION", text)

        for token in (
            "current_workstream_identity",
            "owner_workstream_identity",
            "owner_activity_classification",
            "current_owner_evidence",
            "cross_workstream_absorption_authorized",
            "NO_ACTIVE_OWNER_EVIDENCE",
            "COORDINATOR_TAKEOVER",
        ):
            self.assertIn(token, skill)
            self.assertIn(token, protocol)

        required_takeover_token = (
            "EXPLICIT_USER_ABSORPTION_AUTHORIZATION: "
            "REQUIRED_FOR_ACTIVE_OTHER_WORKER_EXCEPTION"
        )
        self.assertIn(required_takeover_token, skill)
        self.assertIn(required_takeover_token, protocol)
        self.assertIn("same workstream", skill)
        self.assertIn("different workstream", skill)
        self.assertIn("CURRENT_COORDINATOR_CHAT", agents)

        self.assertNotIn(
            "approved same-goal/path/semantic overlap에 한해서 이 standing authorization이 필요한 `explicit user authorization`을 제공",
            skill,
        )

    def test_audit_invalidates_search_only_readme_drift_hypothesis(self) -> None:
        readme = read("README.md")
        audit = read(
            "docs/audits/2026-08-13-base-work-structure-adversarial-audit.md"
        )
        design = read(
            "docs/superpowers/specs/2026-08-13-concurrent-sync-preflight-design.md"
        )
        plan = read(
            "docs/superpowers/plans/2026-08-13-concurrent-sync-preflight.md"
        )
        learning = read("skills/synchronizing-local-and-github-state/LEARNING_LOG.md")

        self.assertIn(
            "This entrypoint does not maintain a second Skill list.",
            readme,
        )
        for text in (audit, design, plan, learning):
            self.assertIn("INVALIDATED_FINDING", text)
            self.assertIn("exact-SHA readback", text)

        for false_claim in (
            "README는 `27`",
            "README의 `27`",
            "README hardcoded 27",
            "README `27` vs",
        ):
            for text in (audit, design, plan, learning):
                self.assertNotIn(false_claim, text)


if __name__ == "__main__":
    unittest.main()
