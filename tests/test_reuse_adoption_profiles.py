from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROFILE_ROOT = ROOT / "docs/knowledge/game-development/reuse/adoption/profiles"
PROJECT_KEYS = (
    "COC_FICTION",
    "GRIMOIRE",
    "SWITCHY",
    "TETRIS",
    "URBAN_LEGEND",
    "NINJA_SURVIVAL",
    "MY_LITTLE_BOAT",
    "BLACKSMITH",
    "TEN_PACES",
    "OMENWARD",
)


def load_adoption_module():
    module_path = ROOT / "tools/reuse_modules/reuse_adoption.py"
    spec = importlib.util.spec_from_file_location("reuse_adoption_profiles", module_path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ReuseAdoptionProfileTests(unittest.TestCase):
    def test_all_active_projects_have_machine_valid_profiles_matching_matrix(self) -> None:
        module = load_adoption_module()
        matrix = json.loads(
            (ROOT / "docs/knowledge/game-development/reuse/adoption/ACTIVE_PROJECT_ADOPTION_MATRIX.json").read_text(
                encoding="utf-8"
            )
        )
        for project_key in PROJECT_KEYS:
            profile_path = PROFILE_ROOT / f"{project_key}.json"
            self.assertTrue(profile_path.is_file(), project_key)
            profile = module.load_manifest(profile_path)
            self.assertEqual(matrix["base_reference_commit"], profile["base_source_commit"])
            self.assertEqual(matrix["projects"][project_key]["modules"], {
                module_id: config["state"]
                for module_id, config in profile["modules"].items()
            })

    def test_enabled_profiles_use_project_specific_destinations(self) -> None:
        expected_destinations = {
            ("SWITCHY", "RM-SYS-001"): "game/reuse/grid_placement_rule_engine.gd",
            ("SWITCHY", "RM-VIS-001"): "game/reuse/semantic_ui_skin_kit.gd",
            ("SWITCHY", "RM-VIS-002"): "game/reuse/gameplay_symbol_atlas.gd",
            ("OMENWARD", "RM-SYS-003"): "scripts/reuse/candidate_draft_weight_engine.gd",
            ("MY_LITTLE_BOAT", "RM-VIS-001"): "scripts/base_reuse/semantic_ui_skin_kit.gd",
            ("MY_LITTLE_BOAT", "RM-VIS-002"): "scripts/base_reuse/gameplay_symbol_atlas.gd",
        }
        for (project_key, module_id), destination in expected_destinations.items():
            profile = json.loads((PROFILE_ROOT / f"{project_key}.json").read_text(encoding="utf-8"))
            self.assertEqual("enabled", profile["modules"][module_id]["state"])
            self.assertEqual(destination, profile["modules"][module_id]["destination"])

    def test_adapted_project_implementation_is_not_mislabeled_as_vendored_source(self) -> None:
        profile = json.loads((PROFILE_ROOT / "URBAN_LEGEND.json").read_text(encoding="utf-8"))
        matrix = json.loads(
            (ROOT / "docs/knowledge/game-development/reuse/adoption/ACTIVE_PROJECT_ADOPTION_MATRIX.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual("ADOPTED_AND_VERIFIED", matrix["projects"]["URBAN_LEGEND"]["status"])
        self.assertEqual("deferred", profile["modules"]["RM-TOOL-001"]["state"])
        self.assertEqual("deferred", matrix["projects"]["URBAN_LEGEND"]["modules"]["RM-TOOL-001"])


if __name__ == "__main__":
    unittest.main()
