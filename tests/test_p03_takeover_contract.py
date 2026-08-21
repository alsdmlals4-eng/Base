from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


class P03TakeoverContractTests(unittest.TestCase):
    def test_adversarial_skill_keeps_true_full_loop_and_fix_guided_verification(self) -> None:
        text = read("skills/running-adversarial-review-and-refinement/SKILL.md")
        for token in (
            "FULL_LOOP_IS_NOT_A_REVIEW_LENS",
            "FIX_GUIDED_VERIFICATION_WHEN_EXECUTABLE",
            "FULL_LOOP_COUNT_MINIMUM: 5",
            "CLEAN_REVIEW_EXIT",
        ):
            self.assertIn(token, text)
        self.assertIn("Loop 1=scope", text)
        self.assertIn("full loop로 계수", text)

    def test_review_protocols_use_configured_workspace_conditionally(self) -> None:
        paths = (
            "skills/running-adversarial-review-and-refinement/references/finding-and-regression-protocol.md",
            "skills/running-adversarial-review-and-refinement/references/repository-wide-audit-protocol.md",
            "templates/quality/POST_MERGE_ADVERSARIAL_REVIEW.md",
        )
        for path in paths:
            text = read(path)
            self.assertIn("CONFIGURED_PROJECT_WORKSPACE", text, path)
        protocol = read(paths[0])
        for token in (
            "baseline_contract_result",
            "candidate_fix_result",
            "counterfactual_improvement",
            "new_regressions",
        ):
            self.assertIn(token, protocol)

    def test_git_sync_declares_connector_only_execution_surface_without_reverting_open_pr_policy(self) -> None:
        for path in (
            "skills/synchronizing-local-and-github-state/SKILL.md",
            "skills/synchronizing-local-and-github-state/references/safe-sync-protocol.md",
        ):
            text = read(path)
            for token in (
                "execution_surface",
                "GITHUB_CONNECTOR_ONLY",
                "NOT_APPLICABLE_CONNECTOR_ONLY",
            ):
                self.assertIn(token, text, path)
        manifest = read("docs/operations/BASE_PARTITION_MANIFEST.json")
        self.assertIn("OPEN_PR_READ_ONLY_BY_DEFAULT", manifest)


if __name__ == "__main__":
    unittest.main()
