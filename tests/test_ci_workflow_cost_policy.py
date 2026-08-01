from __future__ import annotations

import re
import unittest
from pathlib import Path

from tests.test_demo_first_planning_sequence import DemoFirstPlanningSequenceTests
from tests.test_github_work_item_lifecycle_policy import (
    GithubWorkItemLifecyclePolicyTests,
)
from tests.test_integrated_vertical_slice_prompt_v7 import (
    IntegratedVerticalSlicePromptV7Tests,
)
from tests.test_vertical_slice_v6_contract import VerticalSliceV6ContractTests


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github/workflows/validate-game-project-operating-system.yml"
PROMPT_WORKFLOW = ROOT / ".github/workflows/validate-integrated-vertical-slice-prompt.yml"


class CiWorkflowCostPolicyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.text = WORKFLOW.read_text(encoding="utf-8")
        cls.prompt_text = PROMPT_WORKFLOW.read_text(encoding="utf-8")
        cls.gate_evaluator = (
            ROOT / "tools/evaluate_ci_required_gate.py"
        ).read_text(encoding="utf-8")

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

    def test_runtime_readiness_and_local_runner_are_validated_at_their_risk_tiers(self) -> None:
        publication_risk = re.search(
            r"case \"\$path\" in(?P<body>.*?)has_code=true\n\s+platform_smoke=true",
            self.text,
            flags=re.DOTALL,
        )
        self.assertIsNotNone(publication_risk)
        for path in (
            "tools/publication_readiness.py",
            "tests/test_publication_readiness.py",
        ):
            self.assertIn(path, publication_risk.group("body"))

        syntax_step = re.search(
            r"- name: Check Python syntax(?P<body>.*?)(?=\n\s+- name: Validate Base change proposals)",
            self.text,
            flags=re.DOTALL,
        )
        self.assertIsNotNone(syntax_step)
        for path in (
            "tools/publication_readiness.py",
            "tools/run_local_validation.py",
            "tests/test_publication_readiness.py",
            "tests/test_local_validation.py",
        ):
            self.assertIn(path, syntax_step.group("body"))

        publication_job = re.search(
            r"publication-validation:\n(?P<body>.*?)(?=\n  platform-smoke-windows:)",
            self.text,
            flags=re.DOTALL,
        )
        windows_job = re.search(
            r"platform-smoke-windows:\n(?P<body>.*?)(?=\n  ci-gate:)",
            self.text,
            flags=re.DOTALL,
        )
        self.assertIsNotNone(publication_job)
        self.assertIsNotNone(windows_job)
        self.assertIn("tests/test_publication_readiness.py", publication_job.group("body"))
        self.assertIn("tests.test_publication_readiness", windows_job.group("body"))

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
        self.assertIn("run: python tools/evaluate_ci_required_gate.py", self.text)
        self.assertIn("required job failed or was not executed", self.gate_evaluator)
        self.assertIn("CI REQUIRED GATE: PASS", self.gate_evaluator)

    def test_vertical_slice_contract_suites_are_aggregated_into_ci(self) -> None:
        source = Path(__file__).read_text(encoding="utf-8")
        for import_term in (
            "from tests.test_demo_first_planning_sequence import",
            "from tests.test_github_work_item_lifecycle_policy import",
            "from tests.test_integrated_vertical_slice_prompt_v7 import",
            "tests.test_vertical_slice_v9_contract",
            "from tests.test_vertical_slice_v6_contract import",
        ):
            self.assertIn(import_term, source)

        for suite in (
            GithubWorkItemLifecyclePolicyTests,
            DemoFirstPlanningSequenceTests,
            VerticalSliceV6ContractTests,
            IntegratedVerticalSlicePromptV7Tests,
        ):
            self.assertTrue(issubclass(suite, unittest.TestCase))

    def test_prompt_changes_have_focused_lightweight_validation(self) -> None:
        for term in (
            '      - "templates/prompts/**"',
            "tests.test_integrated_vertical_slice_prompt_v7",
            "tests.test_vertical_slice_v9_contract",
            "tests.test_vertical_slice_v6_contract",
            "tests.test_demo_first_planning_sequence",
            "tools/check_canonical_reference_freshness.py",
            "cancel-in-progress: true",
        ):
            self.assertIn(term, self.prompt_text)

        for forbidden in ("libreoffice", "poppler", "pnpm install", "windows-latest"):
            self.assertNotIn(forbidden, self.prompt_text.lower())


if __name__ == "__main__":
    unittest.main()
