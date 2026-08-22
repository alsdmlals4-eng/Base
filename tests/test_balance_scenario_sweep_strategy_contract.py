from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULES = ROOT / "docs" / "knowledge" / "game-development" / "reuse" / "PRODUCTION_TOOL_WORKFLOW_MODULES.md"
EXTENSION = ROOT / "docs" / "knowledge" / "game-development" / "reuse" / "BALANCE_SCENARIO_SWEEP_STRATEGY_EXTENSION.md"


class BalanceScenarioSweepStrategyContractTests(unittest.TestCase):
    def extension_text(self) -> str:
        self.assertTrue(EXTENSION.is_file(), "RM-TOOL-003 sweep/strategy extension is missing")
        return EXTENSION.read_text(encoding="utf-8")

    def test_extension_is_owned_by_existing_balance_module(self) -> None:
        modules = MODULES.read_text(encoding="utf-8")
        extension = self.extension_text()
        self.assertIn("RM-TOOL-003 · BALANCE_SCENARIO_BATCH_SIMULATOR", modules)
        self.assertIn("owner: RM-TOOL-003 BALANCE_SCENARIO_BATCH_SIMULATOR", extension)
        self.assertIn("NO_NEW_PUBLIC_MODULE_ID", extension)

    def test_strategy_baselines_separate_random_heuristic_and_project_policies(self) -> None:
        text = self.extension_text()
        for marker in (
            "STRATEGY_BASELINE_MATRIX",
            "RANDOM_BASELINE",
            "HEURISTIC_BASELINE",
            "PROJECT_STRATEGY",
            "SIMULATION_STRATEGY_IS_NOT_PLAYER_BEHAVIOR_PROOF",
        ):
            self.assertIn(marker, text)

    def test_parameter_sweep_is_single_axis_paired_and_non_authoritative(self) -> None:
        text = self.extension_text()
        for marker in (
            "PARAMETER_SWEEP_SINGLE_AXIS_FIRST",
            "PAIR_SWEEP_STEPS_BY_SEED_SET",
            "THRESHOLD_ESTIMATE_NOT_RECOMMENDED_VALUE",
            "SWEEP_THRESHOLD_REQUIRES_UNCERTAINTY_CHECK",
        ):
            self.assertIn(marker, text)

    def test_model_adapter_fidelity_is_explicit(self) -> None:
        text = self.extension_text()
        for marker in (
            "AUTHORITATIVE_RULE_ADAPTER",
            "ABSTRACT_MATH_MODEL",
            "MODEL_PARITY_CHECK_REQUIRED_FOR_PRODUCTION_CLAIM",
            "MODEL_SIMULATION_PASS_IS_NOT_PRODUCTION_RUNTIME_PASS",
        ):
            self.assertIn(marker, text)

    def test_godot_autosim_is_pattern_source_not_default_dependency(self) -> None:
        text = self.extension_text()
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
