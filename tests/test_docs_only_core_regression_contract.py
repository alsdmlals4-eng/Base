from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github/workflows/validate-game-project-operating-system.yml"
GATE = ROOT / "tools/evaluate_ci_required_gate.py"


class DocsOnlyCoreRegressionContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.workflow = WORKFLOW.read_text(encoding="utf-8")
        cls.gate = GATE.read_text(encoding="utf-8")

    def test_change_classifier_exposes_core_regression_requirement(self) -> None:
        self.assertIn(
            "run_core: ${{ steps.classify.outputs.run_core }}",
            self.workflow,
        )
        docs_case = re.search(
            r"docs\)\n(?P<body>.*?)(?=\n\s+;;)",
            self.workflow,
            flags=re.DOTALL,
        )
        self.assertIsNotNone(docs_case)
        self.assertIn("run_core=false", docs_case.group("body"))
        for level in ("contract", "code", "ci", "full"):
            match = re.search(
                rf"{level}\)\n(?P<body>.*?)(?=\n\s+;;)",
                self.workflow,
                flags=re.DOTALL,
            )
            self.assertIsNotNone(match, level)
            self.assertIn("run_core=true", match.group("body"), level)

    def test_core_regression_job_is_conditional_on_classifier(self) -> None:
        match = re.search(
            r"core-regression:\n(?P<body>.*?)(?=\n  ubuntu-contract:)",
            self.workflow,
            flags=re.DOTALL,
        )
        self.assertIsNotNone(match)
        body = match.group("body")
        self.assertIn("needs: classify-changes", body)
        self.assertIn(
            "if: needs.classify-changes.outputs.run_core == 'true'",
            body,
        )

    def test_ci_gate_treats_core_regression_as_conditional(self) -> None:
        self.assertIn("CORE_REQUIRED", self.workflow)
        self.assertIn("CORE_REQUIRED", self.gate)
        always_required = re.search(
            r"ALWAYS_REQUIRED = \((?P<body>.*?)\)\nCONDITIONAL",
            self.gate,
            flags=re.DOTALL,
        )
        self.assertIsNotNone(always_required)
        self.assertNotIn("core-regression", always_required.group("body"))
        self.assertIn(
            '("core-regression", "CORE_REQUIRED", "CORE_REGRESSION_RESULT")',
            self.gate,
        )


if __name__ == "__main__":
    unittest.main()
