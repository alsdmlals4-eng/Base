from __future__ import annotations

import os
import subprocess
import sys
import unittest
from pathlib import Path

from tests.test_universal_loop_local_burnin_readiness_closure import (
    UniversalLoopLocalBurninReadinessClosureTests,
)
from tests.test_universal_loop_network_boundary_closure import (
    UniversalLoopNetworkBoundaryClosureTests,
)
from tests.test_universal_loop_provider_transport_closure import (
    UniversalLoopProviderTransportClosureTests,
)
from tests.test_universal_loop_subscription_cli_closure import (
    UniversalLoopSubscriptionCliClosureTests,
)


ROOT = Path(__file__).resolve().parents[1]
EVALUATOR = ROOT / "tools/evaluate_ci_required_gate.py"
PASSING_ENV = {
    "CLASSIFY_RESULT": "success",
    "DOCS_RESULT": "success",
    "CORE_REGRESSION_RESULT": "success",
    "CONTRACT_REQUIRED": "true",
    "CONTRACT_RESULT": "success",
    "PUBLICATION_REQUIRED": "true",
    "PUBLICATION_RESULT": "success",
    "WINDOWS_REQUIRED": "true",
    "WINDOWS_RESULT": "success",
}


class CiRequiredGateEvaluatorTests(unittest.TestCase):
    def _run(self, overrides: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
        environment = os.environ.copy()
        environment.update(PASSING_ENV)
        if overrides:
            environment.update(overrides)
        return subprocess.run(
            [sys.executable, str(EVALUATOR)],
            capture_output=True,
            text=True,
            encoding="utf-8",
            env=environment,
        )

    def test_all_required_jobs_succeed(self) -> None:
        result = self._run()
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn("CI REQUIRED GATE: PASS", result.stdout)

    def test_always_required_failures_fail_closed(self) -> None:
        for variable, result_value, job_name in (
            ("CLASSIFY_RESULT", "failure", "classify-changes"),
            ("DOCS_RESULT", "skipped", "docs-validation"),
            ("CORE_REGRESSION_RESULT", "failure", "core-regression"),
        ):
            with self.subTest(variable=variable):
                result = self._run({variable: result_value})
                self.assertNotEqual(0, result.returncode)
                self.assertIn(job_name, result.stdout)

    def test_each_required_conditional_job_must_succeed(self) -> None:
        for required, result_name, job_name in (
            ("CONTRACT_REQUIRED", "CONTRACT_RESULT", "ubuntu-contract"),
            ("PUBLICATION_REQUIRED", "PUBLICATION_RESULT", "publication-validation"),
            ("WINDOWS_REQUIRED", "WINDOWS_RESULT", "platform-smoke-windows"),
        ):
            for result_value in ("failure", "skipped"):
                with self.subTest(required=required, result=result_value):
                    result = self._run({required: "true", result_name: result_value})
                    self.assertNotEqual(0, result.returncode)
                    self.assertIn(job_name, result.stdout)

    def test_optional_skipped_jobs_pass(self) -> None:
        result = self._run({
            "CONTRACT_REQUIRED": "false",
            "CONTRACT_RESULT": "skipped",
            "PUBLICATION_REQUIRED": "false",
            "PUBLICATION_RESULT": "skipped",
            "WINDOWS_REQUIRED": "false",
            "WINDOWS_RESULT": "skipped",
        })
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_invalid_required_flags_fail_closed(self) -> None:
        for variable in ("CONTRACT_REQUIRED", "PUBLICATION_REQUIRED", "WINDOWS_REQUIRED"):
            with self.subTest(variable=variable):
                result = self._run({variable: "TRUE"})
                self.assertNotEqual(0, result.returncode)
                self.assertIn(f"invalid required flag: {variable}", result.stdout)

    def test_each_missing_input_fails_closed(self) -> None:
        for missing in PASSING_ENV:
            with self.subTest(missing=missing):
                environment = os.environ.copy()
                environment.update(PASSING_ENV)
                environment.pop(missing)
                result = subprocess.run(
                    [sys.executable, str(EVALUATOR)],
                    capture_output=True,
                    text=True,
                    encoding="utf-8",
                    env=environment,
                )
                self.assertNotEqual(0, result.returncode)
                self.assertIn(f"missing environment variable: {missing}", result.stdout)


if __name__ == "__main__":
    unittest.main()
