from __future__ import annotations

import copy
import importlib.util
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "tools/reuse_modules/balance_scenario_batch_simulator.py"
TEMPLATE_PATH = ROOT / "templates/reuse-modules/BALANCE_SCENARIO_BATCH_MANIFEST.json"


def load_module():
    spec = importlib.util.spec_from_file_location(
        "balance_scenario_batch_simulator", MODULE_PATH
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("balance_scenario_batch_simulator module could not be loaded")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class BalanceScenarioBatchSimulatorTests(unittest.TestCase):
    def manifest(self) -> dict[str, object]:
        return {
            "schema_version": 1,
            "project_id": "TEST",
            "snapshot": {"source_commit": "abc123"},
            "evidence_ceiling": ["PLANNING_ONLY"],
            "baseline_variant": "baseline",
            "runs": [
                {
                    "seed": 1,
                    "variant": "baseline",
                    "metrics": {"score": 10},
                    "choices": ["A"],
                },
                {
                    "seed": 2,
                    "variant": "baseline",
                    "metrics": {"score": 20},
                    "choices": ["A"],
                    "failures": ["SHORT"],
                },
                {
                    "seed": 3,
                    "variant": "baseline",
                    "metrics": {"score": 30},
                    "choices": ["B"],
                },
                {
                    "seed": 4,
                    "variant": "baseline",
                    "metrics": {"score": 40},
                    "choices": ["A"],
                },
                {
                    "seed": 1,
                    "variant": "candidate_good",
                    "metrics": {"score": 12},
                    "choices": ["A"],
                },
                {
                    "seed": 2,
                    "variant": "candidate_good",
                    "metrics": {"score": 24},
                    "choices": ["B"],
                },
                {
                    "seed": 3,
                    "variant": "candidate_good",
                    "metrics": {"score": 36},
                    "choices": ["B"],
                },
                {
                    "seed": 4,
                    "variant": "candidate_good",
                    "metrics": {"score": 48},
                    "choices": ["B"],
                },
                {"seed": 1, "variant": "candidate_bad", "metrics": {"score": 1}},
                {"seed": 2, "variant": "candidate_bad", "metrics": {"score": 2}},
                {"seed": 3, "variant": "candidate_bad", "metrics": {"score": 3}},
                {"seed": 4, "variant": "candidate_bad", "metrics": {"score": 4}},
            ],
            "goal_seek": [
                {
                    "metric": "score",
                    "target": [30, 50],
                    "variants": ["candidate_good", "candidate_bad"],
                }
            ],
        }

    def test_distribution_pairing_failures_choices_and_goal_seek(self) -> None:
        self.assertTrue(MODULE_PATH.is_file(), MODULE_PATH)
        module = load_module()
        source = self.manifest()
        source_before = copy.deepcopy(source)

        report = module.analyze_manifest(source)

        self.assertEqual(source_before, source)
        self.assertEqual("TEST", report["project_id"])
        self.assertEqual(
            "LINEAR_INDEX_Q_TIMES_N_MINUS_1", report["percentile_method"]
        )
        self.assertEqual(["PLANNING_ONLY"], report["evidence_ceiling"])
        self.assertFalse(report["mutates_project_data"])

        baseline = report["variants"]["baseline"]
        self.assertEqual(4, baseline["run_count"])
        self.assertEqual(
            {
                "count": 4,
                "mean": 25.0,
                "median": 25.0,
                "min": 10.0,
                "max": 40.0,
                "percentile_05": 11.5,
                "percentile_25": 17.5,
                "percentile_75": 32.5,
                "percentile_95": 38.5,
            },
            baseline["metrics"]["score"],
        )
        self.assertEqual("RUNS_CONTAINING_TAG", baseline["failure_rate_denominator"])
        self.assertEqual({"SHORT": 0.25}, baseline["failure_rates"])
        self.assertEqual("TOTAL_CHOICE_EVENTS", baseline["choice_share_denominator"])
        self.assertEqual(4, baseline["choice_event_count"])
        self.assertEqual(
            {"choice": "A", "count": 3, "share": 0.75},
            baseline["dominant_choice"],
        )
        self.assertEqual(
            [
                {"seed": 4, "value": 40.0},
                {"seed": 3, "value": 30.0},
                {"seed": 2, "value": 20.0},
            ],
            baseline["tail_runs"]["score"]["highest"],
        )

        delta = report["paired_seed_deltas"]["candidate_good"]["score"]
        self.assertEqual(4, delta["paired_count"])
        self.assertEqual(5.0, delta["mean_delta"])
        self.assertEqual(5.0, delta["median_delta"])
        self.assertEqual(2.3, delta["percentile_05_delta"])
        self.assertEqual(7.7, delta["percentile_95_delta"])

        ranking = report["goal_seek"][0]["ranking"]
        self.assertEqual("candidate_good", ranking[0]["variant"])
        self.assertEqual(0.0, ranking[0]["distance_to_target"])
        self.assertTrue(ranking[0]["inside_target"])
        self.assertEqual(0.5, ranking[0]["inside_target_share"])
        self.assertEqual("candidate_bad", ranking[1]["variant"])
        self.assertTrue(report["goal_seek"][0]["non_authoritative"])

    def test_failure_rate_deduplicates_same_tag_within_one_run(self) -> None:
        module = load_module()
        manifest = {
            "schema_version": 1,
            "project_id": "TEST",
            "runs": [
                {
                    "seed": 1,
                    "variant": "baseline",
                    "metrics": {"score": 1},
                    "failures": ["X", "X"],
                }
            ],
        }

        report = module.analyze_manifest(manifest)

        baseline = report["variants"]["baseline"]
        self.assertEqual({"X": 1.0}, baseline["failure_rates"])
        self.assertLessEqual(max(baseline["failure_rates"].values()), 1.0)

    def test_goal_seek_prefers_more_runs_inside_target_when_medians_tie(self) -> None:
        module = load_module()
        runs = []
        volatile = [0, 40, 40, 100]
        stable = [35, 40, 40, 45]
        for seed, value in enumerate(volatile, start=1):
            runs.append(
                {
                    "seed": seed,
                    "variant": "candidate_a_volatile",
                    "metrics": {"score": value},
                }
            )
        for seed, value in enumerate(stable, start=1):
            runs.append(
                {
                    "seed": seed,
                    "variant": "candidate_z_stable",
                    "metrics": {"score": value},
                }
            )
        manifest = {
            "schema_version": 1,
            "project_id": "TEST",
            "runs": runs,
            "goal_seek": [
                {
                    "metric": "score",
                    "target": [30, 50],
                    "variants": ["candidate_a_volatile", "candidate_z_stable"],
                }
            ],
        }

        ranking = module.analyze_manifest(manifest)["goal_seek"][0]["ranking"]

        self.assertEqual("candidate_z_stable", ranking[0]["variant"])
        self.assertEqual(1.0, ranking[0]["inside_target_share"])
        self.assertEqual(0.5, ranking[1]["inside_target_share"])
        self.assertEqual(0.0, ranking[0]["distance_to_target"])
        self.assertEqual(0.0, ranking[1]["distance_to_target"])

    def test_rejects_duplicate_variant_seed_and_invalid_metrics(self) -> None:
        self.assertTrue(MODULE_PATH.is_file(), MODULE_PATH)
        module = load_module()

        duplicate = self.manifest()
        duplicate["runs"] = [
            {"seed": 1, "variant": "same", "metrics": {"score": 1}},
            {"seed": 1, "variant": "same", "metrics": {"score": 2}},
        ]
        duplicate.pop("baseline_variant", None)
        duplicate.pop("goal_seek", None)
        with self.assertRaisesRegex(ValueError, "duplicate variant/seed pair"):
            module.analyze_manifest(duplicate)

        invalid_metric = {
            "schema_version": 1,
            "project_id": "TEST",
            "runs": [
                {
                    "seed": 1,
                    "variant": "baseline",
                    "metrics": {"score": "not-a-number"},
                }
            ],
        }
        with self.assertRaisesRegex(ValueError, "must be numeric"):
            module.analyze_manifest(invalid_metric)

        non_finite_metric = {
            "schema_version": 1,
            "project_id": "TEST",
            "runs": [
                {
                    "seed": 1,
                    "variant": "baseline",
                    "metrics": {"score": float("nan")},
                }
            ],
        }
        with self.assertRaisesRegex(ValueError, "must be finite"):
            module.analyze_manifest(non_finite_metric)

        non_finite_target = self.manifest()
        non_finite_target["goal_seek"] = [
            {"metric": "score", "target": [0, float("inf")]}
        ]
        with self.assertRaisesRegex(ValueError, "target values must be finite"):
            module.analyze_manifest(non_finite_target)

    def test_manifest_template_is_runnable_and_read_only(self) -> None:
        self.assertTrue(TEMPLATE_PATH.is_file(), TEMPLATE_PATH)
        module = load_module()
        manifest = json.loads(TEMPLATE_PATH.read_text(encoding="utf-8"))

        report = module.analyze_manifest(manifest)

        self.assertEqual("EXAMPLE_PROJECT", report["project_id"])
        self.assertEqual(2, report["run_count"])
        self.assertFalse(report["mutates_project_data"])
        self.assertEqual("candidate", report["goal_seek"][0]["ranking"][0]["variant"])

    def test_cli_fail_closed_for_invalid_manifest(self) -> None:
        self.assertTrue(MODULE_PATH.is_file(), MODULE_PATH)
        module = load_module()
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "manifest.json"
            path.write_text(json.dumps({"schema_version": 99}), encoding="utf-8")
            output = StringIO()
            with redirect_stdout(output):
                status = module.main([str(path)])
        self.assertEqual(2, status)
        payload = json.loads(output.getvalue())
        self.assertFalse(payload["ok"])
        self.assertIn("schema_version", payload["error"])


if __name__ == "__main__":
    unittest.main()
