from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


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
