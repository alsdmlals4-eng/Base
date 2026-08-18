from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STYLE_SYSTEM = ROOT / "docs" / "knowledge" / "game-development" / "PIXEL_ART_STYLE_SYSTEM.md"
VISUAL_GALLERY = ROOT / "docs" / "knowledge" / "game-development" / "PIXEL_ART_VISUAL_REFERENCE_GALLERY.md"
HUB = ROOT / "docs" / "knowledge" / "game-development" / "README.md"
ART_BRIEF = ROOT / "templates" / "planning" / "ART_DIRECTION_BRIEF.md"
WORKFLOW = ROOT / ".github" / "workflows" / "validate-evidence-knowledge.yml"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class PixelArtStyleSystemTests(unittest.TestCase):
    def test_multiaxis_style_system_is_routed_and_project_owned(self) -> None:
        self.assertTrue(STYLE_SYSTEM.is_file())
        self.assertTrue(VISUAL_GALLERY.is_file())
        style = read(STYLE_SYSTEM)
        hub = read(HUB)
        brief = read(ART_BRIEF)

        self.assertIn("PIXEL_ART_STYLE_SYSTEM.md", hub)
        self.assertIn("PIXEL_ART_VISUAL_REFERENCE_GALLERY.md", hub)
        self.assertIn("PIXEL_ART_STYLE_SYSTEM.md", brief)
        self.assertIn("PIXEL_ART_VISUAL_REFERENCE_GALLERY.md", style)

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
            "4-Tone Handheld Pixel",
            "8-Bit Limited Palette",
            "16-Bit Rich Pixel",
            "Clean Cluster Pixel",
            "Dithered Texture Pixel",
            "Soft No-Outline Pixel",
            "Hard-Outline Comic Pixel",
            "Chibi Pixel",
            "Anime / JRPG Pixel",
            "HD Pixel",
            "Painterly Pixel",
            "Pixel Noir",
            "Gothic Pixel",
            "Cozy Pastel Pixel",
            "Neon Pixel",
            "Isometric Pixel",
            "Tactical Top-down Pixel",
            "3D-to-Pixel Hybrid",
            "HD-2D Hybrid",
        ):
            self.assertIn(preset, style)
            self.assertIn(preset, read(VISUAL_GALLERY))

        for contract in (
            "MINIMUM_SUBSTANTIVE_ALTERNATIVES: 3",
            "BETTER_ALTERNATIVE_SEARCH_UNTIL_DECISION",
            "LONG_TERM_PLAN_FIT",
            "PRE_DECISION_REREVIEW",
            "PROJECT_ART_CANON_REMAINS_PROJECT_OWNED",
            "NO_AUTOMATIC_PROJECT_STYLE_PROMOTION",
        ):
            self.assertIn(contract, style)

    def test_visual_gallery_has_reference_only_images_and_provenance(self) -> None:
        gallery = read(VISUAL_GALLERY)
        self.assertGreaterEqual(gallery.count("!["), 20)
        self.assertGreaterEqual(gallery.count("reference_status: REFERENCE_ONLY"), 20)
        self.assertGreaterEqual(gallery.count("license:"), 20)
        self.assertGreaterEqual(gallery.count("source:"), 20)
        self.assertGreaterEqual(gallery.count("observe:"), 20)
        self.assertIn("외부 예시는 스타일 정의가 아니라 관찰 자료", gallery)
        self.assertIn("PROJECT_ASSET_APPROVED를 부여하지 않는다", gallery)

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

    def test_visual_gallery_is_preserved_in_validation_evidence(self) -> None:
        workflow = read(WORKFLOW)
        self.assertIn(
            "docs/knowledge/game-development/PIXEL_ART_VISUAL_REFERENCE_GALLERY.md",
            workflow,
        )


if __name__ == "__main__":
    unittest.main()
