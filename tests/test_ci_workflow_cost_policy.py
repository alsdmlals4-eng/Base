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
CI_POLICY = ROOT / "docs/CI_EXECUTION_COST_POLICY.md"
GITHUB_POLICY = ROOT / "docs/GITHUB_PRO_OPERATING_POLICY.md"
USAGE_BUDGET = ROOT / "templates/project-operations/github/GITHUB_USAGE_BUDGET.md"
VALIDATION_SKILL = ROOT / "skills/reviewing-and-validating-project-changes/SKILL.md"
LOCAL_VALIDATION_TEST = ROOT / "tests/test_local_validation.py"


class CiWorkflowCostPolicyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.text = WORKFLOW.read_text(encoding="utf-8")
        cls.prompt_text = PROMPT_WORKFLOW.read_text(encoding="utf-8")
        cls.ci_policy = CI_POLICY.read_text(encoding="utf-8")
        cls.github_policy = GITHUB_POLICY.read_text(encoding="utf-8")
        cls.usage_budget = USAGE_BUDGET.read_text(encoding="utf-8")
        cls.validation_skill = VALIDATION_SKILL.read_text(encoding="utf-8")
        cls.local_validation_test = LOCAL_VALIDATION_TEST.read_text(encoding="utf-8")
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

    def test_workflow_cancels_stale_pr_and_main_push_runs(self) -> None:
        self.assertIn("concurrency:", self.text)
        self.assertIn(
            "group: ci-${{ github.workflow }}-${{ github.event_name }}-${{ github.event.pull_request.number || github.ref }}",
            self.text,
        )
        self.assertIn(
            "cancel-in-progress: ${{ github.event_name == 'pull_request' || github.event_name == 'push' }}",
            self.text,
        )

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

    def test_publication_validation_is_bounded_and_install_steps_are_diagnostic(self) -> None:
        publication_match = re.search(
            r"publication-validation:\n(?P<body>.*?)(?=\n  [a-zA-Z0-9_-]+:|\Z)",
            self.text,
            flags=re.DOTALL,
        )
        self.assertIsNotNone(publication_match)
        body = publication_match.group("body")
        self.assertIn("timeout-minutes: 15", body)
        for step_name in (
            "Install system publication dependencies",
            "Install Python publication dependencies",
            "Install Node publication dependencies",
        ):
            self.assertIn(step_name, body)
        self.assertNotIn("- name: Install publication dependencies", body)

    def test_windows_publication_smoke_is_bounded_and_install_steps_are_diagnostic(self) -> None:
        windows_match = re.search(
            r"platform-smoke-windows:\n(?P<body>.*?)(?=\n  [a-zA-Z0-9_-]+:|\Z)",
            self.text,
            flags=re.DOTALL,
        )
        self.assertIsNotNone(windows_match)
        body = windows_match.group("body")
        self.assertIn("timeout-minutes: 15", body)
        for step_name in (
            "Install Windows system publication dependencies",
            "Install Windows Python publication dependencies",
            "Install Windows Node publication dependencies",
        ):
            self.assertIn(step_name, body)
        self.assertNotIn("- name: Install Windows publication dependencies", body)
        self.assertNotIn("choco install libreoffice-fresh", body)
        for term in (
            '$libreOfficeVersion = "26.2.3"',
            '$libreOfficeSha256 = "468d1fb3880af3bcddac002e9054155912c70b45d105bfa1c82036f33456133d"',
            "https://download.documentfoundation.org/libreoffice/stable/$libreOfficeVersion/win/x86_64/LibreOffice_${libreOfficeVersion}_Win_x86-64.msi",
            "Get-FileHash -Algorithm SHA256",
            "Start-Process msiexec.exe",
            "@(0, 3010) -notcontains $libreOfficeInstall.ExitCode",
        ):
            self.assertIn(term, body)
        self.assertRegex(
            body,
            r"pnpm install --frozen-lockfile\s+"
            r"if \(\$LASTEXITCODE -ne 0\) \{ exit \$LASTEXITCODE \}",
        )

    def test_retired_qa_evidence_studio_is_not_required_windows_smoke(self) -> None:
        classification = re.search(
            r"case \"\$path\" in(?P<body>.*?)(?=\n\s+esac)",
            self.text,
            flags=re.DOTALL,
        )
        self.assertIsNotNone(classification)
        body = classification.group("body")
        self.assertIn("tools/qa-evidence-studio/*", body)
        self.assertRegex(
            body,
            r"tools/qa-evidence-studio/\*\)\s+"
            r"has_code=true\s+"
            r"platform_smoke=false",
        )
        for retired in ("tools/tool-hub/*", "tools/expression-studio/*", "tools/sprite-animation-studio/*"):
            self.assertNotIn(retired, body)

        windows_match = re.search(
            r"platform-smoke-windows:\n(?P<body>.*?)(?=\n  ci-gate:)",
            self.text,
            flags=re.DOTALL,
        )
        self.assertIsNotNone(windows_match)
        windows_body = windows_match.group("body")
        for disabled_step in (
            "- name: Install Windows QA Evidence Studio dependencies\n        if: ${{ false }}",
            "- name: Run Windows QA Evidence Studio smoke\n        if: ${{ false }}",
        ):
            self.assertIn(disabled_step, windows_body)
        self.assertNotIn("tools/tool-hub", windows_body)

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
        self.assertRegex(
            windows_job.group("body"),
            r"python tools/check_publication_environment\.py --require-mermaid\s+"
            r"if \(\$LASTEXITCODE -ne 0\) \{ exit \$LASTEXITCODE \}",
        )

    def test_local_ci_fallback_is_aggregated_into_existing_ci_contract(self) -> None:
        self.assertIn("tests/test_local_validation.py", self.text)
        self.assertIn("from tests.test_local_ci_fallback import", self.local_validation_test)
        self.assertIn("LocalCiFallbackTests as _LocalCiFallbackTests", self.local_validation_test)

    def test_dual_mode_policy_is_fail_closed(self) -> None:
        for text in (self.ci_policy, self.validation_skill):
            self.assertIn("REMOTE_CI", text)
            self.assertIn("LOCAL_FALLBACK", text)
            self.assertIn("`ci-gate` Check Run", text)
            self.assertIn("tools/run_local_ci_fallback.py", text)
        self.assertIn("테스트 실패", self.ci_policy)
        self.assertIn("fallback으로 전환하지 않는다", self.ci_policy)
        self.assertIn("BLOCKED_BY_GITHUB_ACTIONS", self.ci_policy)
        self.assertIn("UNVERIFIED", self.ci_policy)

    def test_fallback_contract_requires_remote_run_absence_and_local_reproducibility(self) -> None:
        for text in (self.ci_policy, self.validation_skill):
            self.assertIn("REMOTE_CI workflow run", text)
            self.assertIn("locally reproducible", text)
        self.assertIn("CODE_OR_ENGINE", self.ci_policy)
        self.assertIn("CI_TOOLCHAIN_HIGH_RISK", self.ci_policy)

    def test_public_repository_budget_does_not_select_fallback(self) -> None:
        for text in (self.github_policy, self.usage_budget):
            self.assertIn("public", text.lower())
            self.assertIn("standard GitHub-hosted", text)
            self.assertIn("LOCAL_FALLBACK", text)
        self.assertNotIn("| omenward | private |", self.usage_budget)

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
