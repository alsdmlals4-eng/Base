from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "tools/reuse_modules/balance_scenario_batch_simulator.py"


def load_module():
    spec = importlib.util.spec_from_file_location(
        "balance_scenario_batch_simulator_source_patterns", MODULE_PATH
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("balance_scenario_batch_simulator module could not be loaded")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def make_runs() -> list[dict[str, object]]:
    runs: list[dict[str, object]] = []
    values_by_variant = {
        "hp_30": [10, 10],
        "hp_50": [30, 30],
        "hp_75": [20, 20],
    }
    for variant, values in values_by_variant.items():
        for seed, value in enumerate(values, start=1):
            runs.append(
                {
                    "seed": seed,
                    "variant": variant,
                    "metrics": {"score": value},
                }
            )
    return runs


class BalanceScenarioBatchSourcePatternTests(unittest.TestCase):
    def test_parameter_sweep_reports_every_crossing_without_best_value_claim(self) -> None:
        module = load_module()
        manifest = {
            "schema_version": 1,
            "project_id": "TEST",
            "runs": make_runs(),
            "parameter_sweeps": [
                {
                    "parameter": "enemy_hp",
                    "metric": "score",
                    "summary_stat": "median",
                    "target": 25,
                    "locked_parameters": ["player_damage", "armor"],
                    "points": [
                        {"value": 30, "variant": "hp_30"},
                        {"value": 50, "variant": "hp_50"},
                        {"value": 75, "variant": "hp_75"},
                    ],
                }
            ],
        }

        report = module.analyze_manifest(manifest)
        sweep = report["parameter_sweeps"][0]

        self.assertTrue(sweep["single_tunable_only"])
        self.assertFalse(sweep["automatic_best_value"])
        self.assertTrue(sweep["non_authoritative"])
        self.assertTrue(sweep["seed_set_equal_across_points"])
        self.assertEqual(2, sweep["seed_count_per_point"])
        self.assertTrue(sweep["metric_seed_set_equal_across_points"])
        self.assertEqual(2, sweep["metric_seed_count_per_point"])
        self.assertEqual("DECLARED_NOT_RUNTIME_VERIFIED", sweep["locked_parameter_verification"])
        self.assertEqual(["player_damage", "armor"], sweep["locked_parameters"])
        self.assertEqual(2, sweep["threshold_crossing_count"])
        self.assertAlmostEqual(45.0, sweep["threshold_crossings"][0]["estimated_parameter_value"])
        self.assertAlmostEqual(62.5, sweep["threshold_crossings"][1]["estimated_parameter_value"])
        self.assertEqual(
            "LINEAR_INTERPOLATION_ESTIMATE_NOT_PROJECT_TRUTH",
            sweep["threshold_crossings"][0]["evidence_ceiling"],
        )

    def test_parameter_sweep_requires_same_seed_set_and_known_variants(self) -> None:
        module = load_module()
        runs = make_runs()
        runs = [
            run
            for run in runs
            if not (run["variant"] == "hp_75" and run["seed"] == 2)
        ]
        manifest = {
            "schema_version": 1,
            "project_id": "TEST",
            "runs": runs,
            "parameter_sweeps": [
                {
                    "parameter": "enemy_hp",
                    "metric": "score",
                    "points": [
                        {"value": 30, "variant": "hp_30"},
                        {"value": 75, "variant": "hp_75"},
                    ],
                }
            ],
        }

        with self.assertRaisesRegex(ValueError, "same seed set"):
            module.analyze_manifest(manifest)

        manifest["runs"] = make_runs()
        manifest["parameter_sweeps"][0]["points"][1]["variant"] = "missing"
        with self.assertRaisesRegex(ValueError, "sweep variant .* not found"):
            module.analyze_manifest(manifest)

    def test_strategy_baselines_never_become_player_skill_or_difficulty_truth(self) -> None:
        module = load_module()
        manifest = {
            "schema_version": 1,
            "project_id": "TEST",
            "runs": make_runs(),
            "strategy_baselines": [
                {"variant": "hp_30", "strategy_id": "random"},
                {"variant": "hp_50", "strategy_id": "greedy_damage"},
            ],
        }

        baselines = module.analyze_manifest(manifest)["strategy_baselines"]

        self.assertEqual("BEHAVIORAL_BASELINE", baselines[0]["role"])
        self.assertFalse(baselines[0]["player_skill_truth"])
        self.assertFalse(baselines[0]["player_fun_truth"])
        self.assertFalse(baselines[0]["difficulty_truth"])
        self.assertEqual(
            "BEHAVIORAL_BASELINE_NOT_PLAYER_EVIDENCE",
            baselines[0]["claim_ceiling"],
        )

    def test_mathematical_model_requires_explicit_equivalence_artifact(self) -> None:
        module = load_module()
        manifest = {
            "schema_version": 1,
            "project_id": "TEST",
            "runs": make_runs(),
            "analysis_context": {
                "adapter_evidence_mode": "MATHEMATICAL_MODEL",
                "adapter_equivalence": {"status": "NOT_VERIFIED"},
            },
        }

        evidence = module.analyze_manifest(manifest)["adapter_evidence"]
        self.assertTrue(evidence["runtime_equivalence_required"])
        self.assertFalse(evidence["runtime_equivalence_verified"])
        self.assertEqual(
            "MATHEMATICAL_MODEL_ONLY_RUNTIME_EQUIVALENCE_NOT_VERIFIED",
            evidence["claim_ceiling"],
        )

        manifest["analysis_context"]["adapter_equivalence"] = {"status": "VERIFIED"}
        with self.assertRaisesRegex(ValueError, "validation_artifact"):
            module.analyze_manifest(manifest)

        manifest["analysis_context"]["adapter_equivalence"] = {
            "status": "VERIFIED",
            "validation_artifact": "project-test://adapter-equivalence",
        }
        evidence = module.analyze_manifest(manifest)["adapter_evidence"]
        self.assertTrue(evidence["runtime_equivalence_verified"])
        self.assertEqual(
            "MATHEMATICAL_MODEL_EQUIVALENCE_RECORDED_NOT_RUNTIME_OR_PLAYER_PASS",
            evidence["claim_ceiling"],
        )

    def test_sweep_rejects_multi_value_aliasing_and_invalid_locked_parameter_contract(self) -> None:
        module = load_module()
        manifest = {
            "schema_version": 1,
            "project_id": "TEST",
            "runs": make_runs(),
            "parameter_sweeps": [
                {
                    "parameter": "enemy_hp",
                    "metric": "score",
                    "locked_parameters": ["enemy_hp"],
                    "points": [
                        {"value": 30, "variant": "hp_30"},
                        {"value": 30, "variant": "hp_50"},
                    ],
                }
            ],
        }

        with self.assertRaisesRegex(ValueError, "swept parameter cannot also be locked"):
            module.analyze_manifest(manifest)

        manifest["parameter_sweeps"][0]["locked_parameters"] = ["armor"]
        with self.assertRaisesRegex(ValueError, "sweep point values must be unique"):
            module.analyze_manifest(manifest)

    def test_parameter_sweep_rejects_metric_samples_from_different_seed_sets(self) -> None:
        module = load_module()
        runs = make_runs()
        for run in runs:
            if run["variant"] == "hp_30" and run["seed"] == 2:
                run["metrics"] = {}
            if run["variant"] == "hp_50" and run["seed"] == 1:
                run["metrics"] = {}
        manifest = {
            "schema_version": 1,
            "project_id": "TEST",
            "runs": runs,
            "parameter_sweeps": [
                {
                    "parameter": "enemy_hp",
                    "metric": "score",
                    "target": 20,
                    "points": [
                        {"value": 30, "variant": "hp_30"},
                        {"value": 50, "variant": "hp_50"},
                    ],
                }
            ],
        }

        with self.assertRaisesRegex(ValueError, "metric .* every seed"):
            module.analyze_manifest(manifest)


if __name__ == "__main__":
    unittest.main()
