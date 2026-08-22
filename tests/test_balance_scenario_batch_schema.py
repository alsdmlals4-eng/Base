from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "tools/reuse_modules/balance_scenario_batch_simulator.py"


def load_module():
    spec = importlib.util.spec_from_file_location(
        "balance_scenario_batch_simulator_schema", MODULE_PATH
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("balance_scenario_batch_simulator module could not be loaded")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class BalanceScenarioBatchSchemaTests(unittest.TestCase):
    def base_run(self) -> dict[str, object]:
        return {"seed": 1, "variant": "baseline", "metrics": {"score": 1}}

    def analyze_one(self, run: dict[str, object]):
        module = load_module()
        return module.analyze_manifest(
            {"schema_version": 1, "project_id": "TEST", "runs": [run]}
        )

    def test_seed_must_be_json_integer_without_bool_or_float_coercion(self) -> None:
        for invalid_seed in (True, 1.9, "1"):
            run = self.base_run()
            run["seed"] = invalid_seed
            with self.subTest(seed=invalid_seed):
                with self.assertRaisesRegex(ValueError, "seed must be an integer"):
                    self.analyze_one(run)

    def test_variant_must_be_non_empty_string(self) -> None:
        for invalid_variant in ("", "   ", 7):
            run = self.base_run()
            run["variant"] = invalid_variant
            with self.subTest(variant=invalid_variant):
                with self.assertRaisesRegex(ValueError, "variant must be a non-empty string"):
                    self.analyze_one(run)

    def test_metrics_choices_and_failures_require_expected_container_types(self) -> None:
        run = self.base_run()
        run["metrics"] = []
        with self.assertRaisesRegex(ValueError, "metrics must be an object"):
            self.analyze_one(run)

        run = self.base_run()
        run["choices"] = "AB"
        with self.assertRaisesRegex(ValueError, "choices must be a list"):
            self.analyze_one(run)

        run = self.base_run()
        run["failures"] = "FAIL"
        with self.assertRaisesRegex(ValueError, "failures must be a list"):
            self.analyze_one(run)

    def test_goal_seek_requires_structured_requests_and_known_variants(self) -> None:
        module = load_module()
        base = {
            "schema_version": 1,
            "project_id": "TEST",
            "runs": [self.base_run()],
        }

        malformed = dict(base)
        malformed["goal_seek"] = "score"
        with self.assertRaisesRegex(ValueError, "goal_seek must be a list"):
            module.analyze_manifest(malformed)

        unknown_variant = dict(base)
        unknown_variant["goal_seek"] = [
            {"metric": "score", "target": [0, 1], "variants": ["missing"]}
        ]
        with self.assertRaisesRegex(ValueError, "goal_seek variant .* not found"):
            module.analyze_manifest(unknown_variant)


if __name__ == "__main__":
    unittest.main()
