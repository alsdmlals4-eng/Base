from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ORCHESTRATION = ROOT / "docs" / "knowledge" / "vertical-slice" / "SKILL_ORCHESTRATION_AND_EVIDENCE.md"


class ExecutionCoverageDrivabilityContractTests(unittest.TestCase):
    def test_coverage_must_be_executable_or_explicitly_environment_gated(self) -> None:
        text = ORCHESTRATION.read_text(encoding="utf-8")
        for marker in (
            "EXECUTABLE_COVERAGE_OR_EXPLICIT_ENV_GATE",
            "UNRUNNABLE_COVERAGE_IS_A_COVERAGE_BUG",
            "ENV_GATED_SKIP_IS_NOT_COVERAGE_PASS",
            "ENV_GATED_EXPECTED_SKIP",
            "UNRUNNABLE_COVERAGE_GAP",
        ):
            self.assertIn(marker, text)

    def test_structural_unrunnability_is_not_laundered_into_skip_or_coverage(self) -> None:
        text = ORCHESTRATION.read_text(encoding="utf-8")
        for marker in (
            "실행 가능한 legitimate environment",
            "coverage count에서 제외",
            "필요한 environment·version·device·tool을 명시",
            "현재 환경에서 PASS로 승격하지 않는다",
            "반복되는 영구 SKIP",
        ):
            self.assertIn(marker, text)


if __name__ == "__main__":
    unittest.main()
