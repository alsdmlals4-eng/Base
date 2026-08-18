from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STYLE_SYSTEM = ROOT / "docs" / "knowledge" / "game-development" / "PIXEL_ART_STYLE_SYSTEM.md"
HUB = ROOT / "docs" / "knowledge" / "game-development" / "README.md"
ART_BRIEF = ROOT / "templates" / "planning" / "ART_DIRECTION_BRIEF.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class PixelArtStyleSystemTests(unittest.TestCase):
    def test_multiaxis_style_system_is_routed_and_project_owned(self) -> None:
        self.assertTrue(STYLE_SYSTEM.is_file())
        style = read(STYLE_SYSTEM)
        hub = read(HUB)
        brief = read(ART_BRIEF)

        self.assertIn("PIXEL_ART_STYLE_SYSTEM.md", hub)
        self.assertIn("PIXEL_ART_STYLE_SYSTEM.md", brief)

        for axis in (
            "PIXEL_GRAMMAR",
            "CHARACTER_SHAPE",
            "VIEW",
            "MOOD_PALETTE",
            "DETAIL_MOTION",
        ):
            self.assertIn(axis, style)

        for preset in (
            "1-Bit Graphic Pixel",
            "Clean Cluster Pixel",
            "Anime / JRPG Pixel",
            "Isometric Pixel",
            "HD Pixel",
            "3D-to-Pixel Hybrid",
            "HD-2D Hybrid",
        ):
            self.assertIn(preset, style)

        for contract in (
            "MINIMUM_SUBSTANTIVE_ALTERNATIVES: 3",
            "BETTER_ALTERNATIVE_SEARCH_UNTIL_DECISION",
            "LONG_TERM_PLAN_FIT",
            "PRE_DECISION_REREVIEW",
            "PROJECT_ART_CANON_REMAINS_PROJECT_OWNED",
            "NO_AUTOMATIC_PROJECT_STYLE_PROMOTION",
        ):
            self.assertIn(contract, style)

    def test_pixel_candidate_template_captures_axes_cost_and_validation(self) -> None:
        brief = read(ART_BRIEF)
        for term in (
            "pixel_art_candidate: YES | NO",
            "pixel_grammar:",
            "character_shape:",
            "view:",
            "mood_palette:",
            "detail_motion:",
            "production_cost: LOW | MEDIUM | HIGH",
            "runtime_validation:",
            "minimum_substantive_alternatives: 3",
        ):
            self.assertIn(term, brief)


if __name__ == "__main__":
    unittest.main()
