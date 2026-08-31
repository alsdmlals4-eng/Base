"""Final independent-review regressions; structural only, never runtime proof."""
from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "tools/validate_player_surface_plan.py"
FIXTURE_FILE = ROOT / "tests/test_player_surface_plan.py"
GUIDE = ROOT / "docs/knowledge/game-development/BENCHMARK_FIRST_MODULAR_UI_PRODUCTION.md"


def _load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class PlayerSurfacePlanReviewRound3Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.checker = _load(CHECKER, "surface_plan_checker_round3")
        cls.fixtures = _load(FIXTURE_FILE, "surface_plan_fixtures_round3")

    def rejected(self, packet, code: str, gate: str = "plan"):
        errors = self.checker.validate_packet(packet, gate)
        self.assertTrue(any(code in error for error in errors), (code, errors))

    def test_dot_only_repository_segments_are_not_canonical_identity(self):
        packet = self.fixtures.packet()
        packet["repository"] = "./."
        self.rejected(packet, "SOURCE_IDENTITY")

    def test_composed_raster_module_requires_family_ownership_on_that_surface(self):
        packet = self.fixtures.frame_packet()
        frame_family = packet["visual_families"][0]
        frame_family["surfaces"] = ["title"]
        frame_family["approval_ref"] = "fixture-only-family-approval"
        packet["visual_families"].append({
            "id": "settings-native",
            "surfaces": ["settings"],
            "owner": "docs/ui.md#settings-native",
            "kind": "PANEL",
            "required_states": ["normal"],
            "state_methods": {"normal": "render live settings controls"},
            "production": "NATIVE_UI",
            "asset_status": "NOT_REQUIRED",
            "asset_manifest_ref": "NO_NEW_IMAGE_FILE_REQUIRED",
        })
        packet["surfaces"][1]["state_bindings"] = {
            "normal": {"family_id": "settings-native", "state": "normal"}
        }
        self.rejected(packet, "RASTER_MODULE_TARGET_UNOWNED", "handoff")

    def test_guide_documents_final_packet_boundaries(self):
        text = GUIDE.read_text(encoding="utf-8")
        for token in [
            "canonical `owner/repo`",
            "RASTER_MODULE_TARGET_UNOWNED",
            "`module_ids`를 생략하거나 `null`",
            "parser-level argument error",
            "`--help`",
        ]:
            with self.subTest(token=token):
                self.assertIn(token, text)


if __name__ == "__main__":
    unittest.main()
