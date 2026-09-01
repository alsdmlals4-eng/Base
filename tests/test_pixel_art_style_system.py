from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STYLE_SYSTEM = ROOT / "docs" / "knowledge" / "game-development" / "PIXEL_ART_STYLE_SYSTEM.md"
VISUAL_GALLERY = ROOT / "docs" / "knowledge" / "game-development" / "PIXEL_ART_VISUAL_REFERENCE_GALLERY.md"
PREFERRED_LIBRARY = ROOT / "docs" / "knowledge" / "game-development" / "PREFERRED_VISUAL_STYLE_REFERENCE_LIBRARY.md"
PREFERRED_OVERVIEW = ROOT / "docs" / "knowledge" / "game-development" / "reference-images" / "preferred-visual" / "preferred-visual-style-overview.jpg"
SPECIALTY_RADAR = ROOT / "docs" / "knowledge" / "game-development" / "PERIODIC_SPECIALTY_SOURCE_RADAR.md"
VISUAL_STYLE_RADAR = ROOT / "docs" / "knowledge" / "game-development" / "VISUAL_STYLE_SOURCE_RADAR.md"
ART_GUIDE = ROOT / "docs" / "knowledge" / "game-development" / "ART_DIRECTION_AND_ASSET_PLANNING_GUIDE.md"
DOC_MAP = ROOT / "docs" / "DOCUMENTATION_MAP.md"
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
            "MINIMUM_VIABLE_ALTERNATIVES: 3",
            "BETTER_ALTERNATIVE_SEARCH",
            "LONG_TERM_PLAN_FIT_REQUIRED",
            "FIVE_FULL_ADVERSARIAL_IMPROVEMENT_LOOPS",
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

    def test_preferred_visual_library_tracks_user_taste_without_promoting_project_canon(self) -> None:
        self.assertTrue(PREFERRED_LIBRARY.is_file())
        preferred = read(PREFERRED_LIBRARY)
        style = read(STYLE_SYSTEM)

        self.assertIn("PREFERRED_VISUAL_STYLE_REFERENCE_LIBRARY.md", style)
        for style_family in (
            "Pixel Illustration Hybrid",
            "Chibi Epic Dark Fantasy",
            "Ink Wash Wuxia",
            "Dark Gold UI",
            "Noir Archive / Investigation Interface",
        ):
            self.assertIn(style_family, preferred)

        for evaluation_axis in (
            "AI_GENERATED_LOOK_REDUCTION",
            "STYLE_CONSISTENCY_AND_READABILITY",
            "WORLD_CORE_SYSTEM_FIT",
        ):
            self.assertIn(evaluation_axis, preferred)

        for governance_term in (
            "MINIMUM_VIABLE_ALTERNATIVES: 3",
            "BETTER_ALTERNATIVE_SEARCH",
            "LONG_TERM_PLAN_FIT_REQUIRED",
            "REVIEW_TRIGGERS",
            "REFERENCE_ONLY",
            "NO_AUTOMATIC_PROJECT_STYLE_PROMOTION",
        ):
            self.assertIn(governance_term, preferred)

        for benchmark in (
            "Shovel Knight",
            "Dead Cells",
            "OCTOPATH TRAVELER II",
            "Hades",
            "Into the Breach",
        ):
            self.assertIn(benchmark, preferred)

        self.assertGreaterEqual(preferred.count("user_reference_sheet:"), 5)
        self.assertGreaterEqual(preferred.count("benchmark_disposition:"), 5)

    def test_preferred_visual_library_preserves_visible_reference_overview(self) -> None:
        self.assertTrue(PREFERRED_OVERVIEW.is_file())
        preferred = read(PREFERRED_LIBRARY)
        self.assertIn(
            "reference-images/preferred-visual/preferred-visual-style-overview.jpg",
            preferred,
        )
        self.assertIn("DERIVED_CONTACT_SHEET", preferred)
        self.assertIn("REFERENCE_ONLY", preferred)

    def test_continuous_style_discovery_reuses_existing_source_radar(self) -> None:
        self.assertTrue(SPECIALTY_RADAR.is_file())
        self.assertTrue(VISUAL_STYLE_RADAR.is_file())
        preferred = read(PREFERRED_LIBRARY)
        radar = read(VISUAL_STYLE_RADAR)

        for term in (
            "CONTINUOUS_STYLE_DISCOVERY",
            "UNCAPPED_CANDIDATE_INTAKE",
            "ORIGINAL_SOURCE_BACKTRACE",
            "STYLE_FAMILY_MATCH",
            "NEW_FAMILY_CANDIDATE",
            "VISUAL_STYLE_SOURCE_RADAR.md",
        ):
            self.assertIn(term, preferred)

        for term in (
            "ART_DIRECTION_AND_VISUAL_STYLE",
            "PERIODIC_SPECIALTY_SOURCE_RADAR.md",
            "PREFERRED_VISUAL_STYLE_REFERENCE_LIBRARY.md",
            "ORIGINAL_SOURCE_BACKTRACE",
            "AI_GENERATED_LOOK_REDUCTION",
            "STYLE_CONSISTENCY_AND_READABILITY",
            "WORLD_CORE_SYSTEM_FIT",
        ):
            self.assertIn(term, radar)

    def test_notion_reference_sync_requires_project_relation_and_readback(self) -> None:
        preferred = read(PREFERRED_LIBRARY)
        for term in (
            "DESKTOP_GPT_REPOSITORY_FIRST_WORKSPACE",
            "PROJECT_RELATION_REQUIRED",
            "Record Type: REFERENCE",
            "NOTION_READBACK_REQUIRED",
            "REFERENCE_SYNC_READBACK_VERIFIED",
            "source provenance",
        ):
            self.assertIn(term, preferred)
        self.assertNotIn("FIGMA_SYNC_PENDING_TRANSPORT", preferred)
        self.assertNotIn("FIGMA_REFERENCE_SYNCED", preferred)

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
            "minimum_viable_alternatives: 3",
        ):
            self.assertIn(term, brief)

    def test_visual_gallery_is_preserved_in_validation_evidence(self) -> None:
        workflow = read(WORKFLOW)
        self.assertIn(
            "docs/knowledge/game-development/PIXEL_ART_VISUAL_REFERENCE_GALLERY.md",
            workflow,
        )

    def test_canonical_art_owners_route_to_pixel_reference_system(self) -> None:
        art_guide = read(ART_GUIDE)
        doc_map = read(DOC_MAP)
        style = read(STYLE_SYSTEM)
        for required in (
            "PIXEL_ART_STYLE_SYSTEM.md",
            "PIXEL_ART_VISUAL_REFERENCE_GALLERY.md",
        ):
            self.assertIn(required, art_guide)
            self.assertIn(required, doc_map)
        self.assertIn("PREFERRED_VISUAL_STYLE_REFERENCE_LIBRARY.md", style)


if __name__ == "__main__":
    unittest.main()
