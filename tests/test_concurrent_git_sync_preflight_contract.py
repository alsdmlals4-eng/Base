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


if __name__ == "__main__":
    unittest.main()
