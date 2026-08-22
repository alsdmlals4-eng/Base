from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULES = ROOT / "docs" / "knowledge" / "game-development" / "reuse" / "PRODUCTION_TOOL_WORKFLOW_MODULES.md"
SOURCES = ROOT / "docs" / "knowledge" / "game-development" / "reuse" / "BENCHMARK_SOURCE_NOTES.md"


class BalanceScenarioSweepStrategyContractTests(unittest.TestCase):
    def test_strategy_baselines_separate_random_heuristic_and_project_policies(self) -> None:
        text = MODULES.read_text(encoding="utf-8")
        for marker in (
            "STRATEGY_BASELINE_MATRIX",
            "RANDOM_BASELINE",
            "HEURISTIC_BASELINE",
            "PROJECT_STRATEGY",
            "SIMULATION_STRATEGY_IS_NOT_PLAYER_BEHAVIOR_PROOF",
        ):
            self.assertIn(marker, text)

    def test_parameter_sweep_is_single_axis_paired_and_non_authoritative(self) -> None:
        text = MODULES.read_text(encoding="utf-8")
        for marker in (
            "PARAMETER_SWEEP_SINGLE_AXIS_FIRST",
            "PAIR_SWEEP_STEPS_BY_SEED_SET",
            "THRESHOLD_ESTIMATE_NOT_RECOMMENDED_VALUE",
            "SWEEP_THRESHOLD_REQUIRES_UNCERTAINTY_CHECK",
        ):
            self.assertIn(marker, text)

    def test_model_adapter_fidelity_is_explicit(self) -> None:
        text = MODULES.read_text(encoding="utf-8")
        for marker in (
            "AUTHORITATIVE_RULE_ADAPTER",
            "ABSTRACT_MATH_MODEL",
            "MODEL_PARITY_CHECK_REQUIRED_FOR_PRODUCTION_CLAIM",
            "MODEL_SIMULATION_PASS_IS_NOT_PRODUCTION_RUNTIME_PASS",
        ):
            self.assertIn(marker, text)

    def test_godot_autosim_is_recorded_as_pattern_source_not_default_dependency(self) -> None:
        text = SOURCES.read_text(encoding="utf-8")
        for marker in (
            "applesnort/godot-autosim",
            "MIT license",
            "parameter sweep",
            "strategy baseline",
            "PATTERN_EXTRACT",
            "PROJECT_ADOPTION_REQUIRES_EXISTING_SOLUTION_FIRST",
        ):
            self.assertIn(marker, text)


if __name__ == "__main__":
    unittest.main()
