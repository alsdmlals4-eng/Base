from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "tools/reuse_modules/balance_scenario_batch_simulator.py"


def load_module():
    spec = importlib.util.spec_from_file_location(
        "balance_scenario_batch_simulator_read_only", MODULE_PATH
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("balance_scenario_batch_simulator module could not be loaded")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class BalanceScenarioBatchReadOnlyTests(unittest.TestCase):
    def test_report_metadata_is_detached_from_input_manifest(self) -> None:
        module = load_module()
        manifest = {
            "schema_version": 1,
            "project_id": "TEST",
            "snapshot": {"source_commit": "abc", "nested": {"value": 1}},
            "evidence_ceiling": ["PLANNING_ONLY"],
            "runs": [
                {"seed": 1, "variant": "baseline", "metrics": {"score": 1}}
            ],
        }

        report = module.analyze_manifest(manifest)
        report["snapshot"]["nested"]["value"] = 99
        report["evidence_ceiling"].append("MUTATED_REPORT")

        self.assertEqual(1, manifest["snapshot"]["nested"]["value"])
        self.assertEqual(["PLANNING_ONLY"], manifest["evidence_ceiling"])
        self.assertFalse(report["mutates_project_data"])


if __name__ == "__main__":
    unittest.main()
