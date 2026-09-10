from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


class P03AdversarialQualityContractTests(unittest.TestCase):
    def test_active_review_surfaces_use_configured_workspace_not_google_sheets(self) -> None:
        surfaces = (
            "skills/running-adversarial-review-and-refinement/references/finding-and-regression-protocol.md",
            "skills/running-adversarial-review-and-refinement/references/repository-wide-audit-protocol.md",
            "templates/quality/POST_MERGE_ADVERSARIAL_REVIEW.md",
        )

        for relative in surfaces:
            text = read(relative)
            self.assertIn("CONFIGURED_PROJECT_WORKSPACE", text, relative)
            self.assertNotIn("Google Sheets", text, relative)

    def test_executable_findings_use_fix_guided_counterfactual_verification(self) -> None:
        skill = read("skills/running-adversarial-review-and-refinement/SKILL.md")
        protocol = read(
            "skills/running-adversarial-review-and-refinement/references/"
            "finding-and-regression-protocol.md"
        )

        self.assertIn("FIX_GUIDED_VERIFICATION_WHEN_EXECUTABLE", skill)
        for token in (
            "baseline_contract_result",
            "candidate_fix_result",
            "counterfactual_improvement",
            "new_regressions",
        ):
            self.assertIn(token, protocol)

    def test_post_merge_template_records_five_whole_state_loops_before_clean_exit(self) -> None:
        template = read("templates/quality/POST_MERGE_ADVERSARIAL_REVIEW.md")
        for token in (
            "Whole-state adversarial loop receipts",
            "loop_index",
            "exact_head",
            "whole_state_readback",
            "alternatives",
            "finding",
            "validation",
            "refinement",
            "regression",
            "whole_state_re_attack",
            "result",
            "REVIEW_INCOMPLETE",
            "CLEAN_REVIEW_EXIT",
            "at least five completed rows",
        ):
            self.assertIn(token, template)

    def test_connector_only_git_preflight_has_explicit_execution_surface(self) -> None:
        skill = read("skills/synchronizing-local-and-github-state/SKILL.md")
        protocol = read(
            "skills/synchronizing-local-and-github-state/references/safe-sync-protocol.md"
        )

        for text in (skill, protocol):
            for token in (
                "execution_surface",
                "GITHUB_CONNECTOR_ONLY",
                "NOT_APPLICABLE_CONNECTOR_ONLY",
            ):
                self.assertIn(token, text)


if __name__ == "__main__":
    unittest.main()
