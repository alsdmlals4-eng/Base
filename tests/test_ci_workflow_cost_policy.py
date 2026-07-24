from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github/workflows/validate-game-project-operating-system.yml"


class CiWorkflowCostPolicyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.text = WORKFLOW.read_text(encoding="utf-8")

    def test_workflow_has_pr_main_nightly_and_manual_events(self) -> None:
        for term in (
            "pull_request:",
            "push:",
            "branches:",
            "- main",
            "schedule:",
            "cron:",
            "workflow_dispatch:",
            "validation_level:",
        ):
            self.assertIn(term, self.text)

    def test_workflow_cancels_stale_pr_runs(self) -> None:
        self.assertIn("concurrency:", self.text)
        self.assertIn("github.event.pull_request.number || github.ref", self.text)
        self.assertIn("cancel-in-progress:", self.text)

    def test_workflow_classifies_change_risk(self) -> None:
        for term in (
            "classify-changes:",
            "docs_only",
            "canonical_contract",
            "code_or_engine",
            "ci_toolchain_high_risk",
            "full_matrix",
            "platform_smoke",
        ):
            self.assertIn(term, self.text)

    def test_heavy_publication_and_windows_jobs_are_conditional(self) -> None:
        publication_match = re.search(
            r"publication-validation:\n(?P<body>.*?)(?=\n  [a-zA-Z0-9_-]+:|\Z)",
            self.text,
            flags=re.DOTALL,
        )
        self.assertIsNotNone(publication_match)
        self.assertIn("if: needs.classify-changes.outputs.run_publication == 'true'", publication_match.group("body"))

        windows_match = re.search(
            r"platform-smoke-windows:\n(?P<body>.*?)(?=\n  [a-zA-Z0-9_-]+:|\Z)",
            self.text,
            flags=re.DOTALL,
        )
        self.assertIsNotNone(windows_match)
        self.assertIn("if: needs.classify-changes.outputs.run_windows == 'true'", windows_match.group("body"))

    def test_docs_job_does_not_install_heavy_dependencies(self) -> None:
        docs_match = re.search(
            r"docs-validation:\n(?P<body>.*?)(?=\n  [a-zA-Z0-9_-]+:|\Z)",
            self.text,
            flags=re.DOTALL,
        )
        self.assertIsNotNone(docs_match)
        body = docs_match.group("body")
        for forbidden in ("libreoffice", "poppler", "pnpm install", "windows-latest"):
            self.assertNotIn(forbidden, body.lower())

    def test_workflow_has_stable_ci_gate(self) -> None:
        self.assertIn("ci-gate:", self.text)
        self.assertIn("if: always()", self.text)
        self.assertIn("required job failed or was not executed", self.text)
        self.assertIn("CI gate passed", self.text)

    def test_new_contract_tests_are_part_of_ci(self) -> None:
        self.assertIn("tests/test_gpt_codex_workflow_contract.py", self.text)
        self.assertIn("tests/test_ci_workflow_cost_policy.py", self.text)
        self.assertIn("tests/test_deep_interview_contract.py", self.text)


if __name__ == "__main__":
    unittest.main()
