from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools/reuse_modules/balance_scenario_batch_simulator.py"
TEMPLATE = ROOT / "templates/reuse-modules/BALANCE_SCENARIO_BATCH_MANIFEST.json"
PILOT = ROOT / "docs/knowledge/game-development/reuse/RM_TOOL_003_IMPLEMENTATION_PILOT.md"
P0 = ROOT / "docs/knowledge/game-development/reuse/P0_IMPLEMENTATION_PILOT.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class RMTool003ImplementationPilotTests(unittest.TestCase):
    def test_reference_surfaces_and_status_owner_exist(self) -> None:
        for path in (TOOL, TEMPLATE, PILOT, P0):
            self.assertTrue(path.is_file(), path)

        p0 = read(P0)
        pilot = read(PILOT)
        self.assertIn("RM-TOOL-003 BALANCE_SCENARIO_BATCH_SIMULATOR", p0)
        self.assertIn("RM_TOOL_003_IMPLEMENTATION_PILOT.md", p0)
        self.assertIn("BASE_REFERENCE_IMPLEMENTED", pilot)
        self.assertIn("project-supplied deterministic run record", pilot)
        self.assertIn("Tool Hub", pilot)
        self.assertIn("DEFER", pilot)
        self.assertIn("OMENWARD · PR #202", pilot)
        self.assertIn("BLACKSMITH · PR #181", pilot)
        self.assertIn("NINJA_SURVIVAL · PR #24", pilot)

    def test_stale_omenward_p0_pr197_is_not_current_pilot(self) -> None:
        p0 = read(P0)
        self.assertIn("Omenward PR #198", p0)
        self.assertIn("67487c932cc883db95da7bc852f4eb33883f0052", p0)
        self.assertNotIn("| Omenward PR #197 |", p0)

    def test_manifest_template_runs_through_reference_analyzer(self) -> None:
        spec = importlib.util.spec_from_file_location("rm_tool_003", TOOL)
        self.assertIsNotNone(spec)
        module = importlib.util.module_from_spec(spec)
        assert spec is not None and spec.loader is not None
        spec.loader.exec_module(module)

        manifest = json.loads(read(TEMPLATE))
        report = module.analyze_manifest(manifest)

        self.assertEqual("EXAMPLE_PROJECT", report["project_id"])
        self.assertFalse(report["mutates_project_data"])
        self.assertIn("baseline", report["variants"])
        self.assertIn("candidate", report["variants"])

    def test_p0_preserves_project_authority_and_evidence_ceiling(self) -> None:
        p0 = read(P0)
        for term in (
            "project-owned deterministic record producer",
            "PRODUCT_BALANCE_PASS: NOT_CLAIMED",
            "HUMAN_PLAYER_EXPERIENCE: NOT_RUN",
            "RM_TOOL_003_TOOL_HUB_GUI: DEFER",
            "Omenward #202 / Blacksmith #181 / Ninja #24",
        ):
            self.assertIn(term, p0)


if __name__ == "__main__":
    unittest.main()
