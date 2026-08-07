from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GUIDE = (
    ROOT
    / "docs"
    / "knowledge"
    / "game-development"
    / "GAME_BUILD_SIZE_AND_ASSET_OPTIMIZATION_GUIDE.md"
)
PROFILE = ROOT / "templates" / "planning" / "PC_ANDROID_DELIVERY_PROFILE.md"
ART_GUIDE = (
    ROOT
    / "docs"
    / "knowledge"
    / "game-development"
    / "ART_DIRECTION_AND_ASSET_PLANNING_GUIDE.md"
)
SOURCE_CATALOG = (
    ROOT
    / "docs"
    / "knowledge"
    / "game-development"
    / "REFERENCE_SOURCE_CATALOG.md"
)
GUIDE_PATH = (
    "docs/knowledge/game-development/"
    "GAME_BUILD_SIZE_AND_ASSET_OPTIMIZATION_GUIDE.md"
)


def read(path: Path | str) -> str:
    target = path if isinstance(path, Path) else ROOT / path
    return target.read_text(encoding="utf-8")


class GameBuildSizeAssetOptimizationTests(unittest.TestCase):
    maxDiff = None

    def test_guide_exists_and_separates_size_dimensions(self) -> None:
        self.assertTrue(GUIDE.is_file())
        guide = read(GUIDE)
        for term in (
            "DOWNLOAD",
            "INSTALLED",
            "RUNTIME",
            "PATCH",
            "windows_size_budget:",
            "android_size_budget:",
            "asset_size_breakdown:",
            "optimization_change:",
        ):
            self.assertIn(term, guide)

    def test_asset_profiles_preserve_quality_and_platform_boundaries(self) -> None:
        guide = read(GUIDE)
        for term in (
            "quality_class:",
            "HERO:",
            "GAMEPLAY_CRITICAL:",
            "font_profile:",
            "fallback_families:",
            "required_glyph_sets:",
            "texture_profile:",
            "windows_import_profile:",
            "android_import_profile:",
            "mipmap_policy:",
            "audio_profile:",
            "A/B listening",
        ):
            self.assertIn(term, guide)

        for forbidden in (
            "폰트는 무조건 하나",
            "모든 텍스처는 동일 해상도",
            "모바일과 PC는 동일 texture compression",
            "mipmap은 전부 제거",
            "압축률은 무조건 최대로",
        ):
            self.assertIn(forbidden, guide)

        self.assertIn("다음을 Base 공용 규칙으로 만들지 않는다", guide)

    def test_profile_extends_legacy_summary_without_breaking_it(self) -> None:
        profile = read(PROFILE)
        self.assertIn("package_and_download_size:", profile)
        self.assertIn("build_size_and_asset_optimization:", profile)
        for term in (
            "windows_size_budget:",
            "android_size_budget:",
            "asset_size_breakdown:",
            "top_contributors:",
            "accepted_optimizations:",
            "rejected_optimizations:",
            "visual_quality_evidence:",
            "audio_quality_evidence:",
            "runtime_evidence:",
            "patch_evidence:",
        ):
            self.assertIn(term, profile)

    def test_art_asset_specification_connects_to_size_quality_gates(self) -> None:
        art = read(ART_GUIDE)
        for term in (
            "size_quality_class:",
            "platform_import_profile:",
            "quality_validation:",
            GUIDE_PATH,
            "동일 texture import profile",
        ):
            self.assertIn(term, art)

    def test_official_sources_cover_engine_android_and_steam(self) -> None:
        sources = read(SOURCE_CATALOG)
        for term in (
            "GODOT-ASSET-IMAGE-001",
            "importing_images.html",
            "GODOT-ASSET-AUDIO-001",
            "importing_audio_samples.html",
            "GODOT-FONT-001",
            "gui_using_fonts.html",
            "ANDROID-SIZE-001",
            "developer.android.com/games/optimize/game-size",
            "ANDROID-TCF-001",
            "asset-delivery/texture-compression",
            "ANDROID-PAD-001",
            "developer.android.com/guide/playcore/asset-delivery",
            "STEAM-PIPE-001",
            "partner.steamgames.com/doc/sdk/uploading",
            "checked_at: 2026-08-07",
        ):
            self.assertIn(term, sources)

    def test_cold_start_and_documentation_map_discover_guide(self) -> None:
        for path in (
            "START_HERE.md",
            "docs/DOCUMENTATION_MAP.md",
            "docs/knowledge/game-development/README.md",
            "docs/knowledge/game-development/PC_ANDROID_CROSS_PLATFORM_DELIVERY_GUIDE.md",
        ):
            self.assertIn(GUIDE_PATH, read(path), path)

    def test_existing_skill_routes_are_reused_without_new_broad_skill(self) -> None:
        registry = read("skills/SKILL_REGISTRY.json")
        for existing_trigger in (
            '"performance-budget"',
            '"performance-profile"',
            '"target-platform"',
        ):
            self.assertIn(existing_trigger, registry)

        for forbidden in (
            '"skill_id":"game-build-size-optimization"',
            '"skill_id":"asset-size-optimization"',
            '"skill_id":"package-size-optimization"',
        ):
            self.assertNotIn(forbidden, registry)

    def test_project_specific_fixed_defaults_are_not_common_policy(self) -> None:
        guide = read(GUIDE)
        for forbidden in (
            "무조건 500MB",
            "모든 텍스처는 1024",
            "모든 오디오는 동일 bitrate",
        ):
            self.assertNotIn(forbidden, guide)

    def test_unverified_runtime_store_and_human_evidence_remain_explicit(self) -> None:
        guide = read(GUIDE)
        cross_platform = read(
            "docs/knowledge/game-development/PC_ANDROID_CROSS_PLATFORM_DELIVERY_GUIDE.md"
        )
        for term in (
            "DEVICE_NOT_RUN",
            "STORE_NOT_RUN",
            "HUMAN_NOT_RUN",
            "BLOCKED_UNVERIFIED",
        ):
            self.assertIn(term, guide)
        self.assertIn("build_size_project_measurement: NOT_RUN", cross_platform)


if __name__ == "__main__":
    unittest.main()
