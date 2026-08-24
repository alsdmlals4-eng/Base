from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NOTE = (
    ROOT
    / "docs"
    / "knowledge"
    / "game-development"
    / "reuse"
    / "COCOS_PATTERN_ABSORPTION_2026-08-24.md"
)
BUILD = (
    ROOT
    / "docs"
    / "knowledge"
    / "game-development"
    / "GAME_BUILD_SIZE_AND_ASSET_OPTIMIZATION_GUIDE.md"
)
TECH = (
    ROOT
    / "docs"
    / "knowledge"
    / "game-development"
    / "TECHNICAL_PRODUCTION_AND_RELEASE_GUIDE.md"
)
PLATFORM = (
    ROOT
    / "docs"
    / "knowledge"
    / "game-development"
    / "PC_ANDROID_CROSS_PLATFORM_DELIVERY_GUIDE.md"
)
WATCH = (
    ROOT
    / "docs"
    / "knowledge"
    / "game-development"
    / "PERIODIC_EXTERNAL_SOURCE_WATCHLIST.md"
)
REGISTRY = (
    ROOT
    / "docs"
    / "knowledge"
    / "game-development"
    / "reuse"
    / "REUSABLE_MODULE_REGISTRY.md"
)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class CocosPatternAbsorptionIntoGodotTests(unittest.TestCase):
    maxDiff = None

    def assert_pattern_note_exists(self) -> None:
        self.assertTrue(NOTE.exists(), f"missing Cocos pattern note: {NOTE}")

    def test_pattern_note_keeps_godot_as_only_runtime(self) -> None:
        self.assert_pattern_note_exists()
        note = read(NOTE)
        for term in (
            "GODOT_ONLY_RUNTIME",
            "ABSORB_COCOS_PATTERNS_ONLY",
            "NO_COCOS_RUNTIME",
            "NO_TYPESCRIPT_REQUIREMENT",
            "NO_SECOND_ENGINE_SELECTION_GATE",
            "Cocos evidence != Godot runtime evidence",
        ):
            self.assertIn(term, note)

    def test_patterns_reuse_existing_owner_contracts(self) -> None:
        self.assert_pattern_note_exists()
        note = read(NOTE)
        for term in (
            "FIRST_LOAD_BUDGET_AND_DEFERRED_CONTENT",
            "REPRODUCIBLE_BUILD_PROFILE",
            "PLATFORM_ADAPTER_STAYS_OUTSIDE_GAME_RULES",
            "PACKAGE_BUDGET_DRIVES_CONTENT_BOUNDARIES",
            "PARTIAL_REBUILD_CANDIDATE",
            "GAME_BUILD_SIZE_AND_ASSET_OPTIMIZATION_GUIDE.md",
            "TECHNICAL_PRODUCTION_AND_RELEASE_GUIDE.md",
            "PC_ANDROID_CROSS_PLATFORM_DELIVERY_GUIDE.md",
        ):
            self.assertIn(term, note)

        build = read(BUILD)
        self.assertIn("first_launch_additional_download_bytes", build)
        self.assertIn("delivery_separation_candidate", build)

        platform = read(PLATFORM)
        self.assertIn("shared_gameplay_rules", platform)
        self.assertIn("platform_service_adapter", platform)

        self.assertTrue(TECH.exists())

    def test_unverified_godot_capabilities_remain_test_only(self) -> None:
        self.assert_pattern_note_exists()
        note = read(NOTE)
        for term in (
            "PCK_DEFERRED_CONTENT: TEST",
            "PARTIAL_REBUILD: TEST",
            "GODOT_WEB_RELEASE_READY: NOT_RUN",
            "API_EXISTS_IS_NOT_PROJECT_READY",
        ):
            self.assertIn(term, note)

    def test_cocos_uses_existing_periodic_source_pipeline(self) -> None:
        self.assert_pattern_note_exists()
        note = read(NOTE)
        for term in (
            "PERIODIC_EXTERNAL_SOURCE_WATCHLIST.md",
            "Cocos Creator official docs/releases",
            "Cocos behavior",
            "Godot runtime authority",
        ):
            self.assertIn(term, note)
        self.assertNotIn("COCOS_SPECIFIC_SCHEDULER", read(WATCH))

    def test_no_cocos_runtime_dependency_new_broad_skill_or_premature_module(self) -> None:
        skill_registry = read(ROOT / "skills" / "SKILL_REGISTRY.json")
        for forbidden in (
            '"skill_id":"cocos-game-development"',
            '"skill_id":"dual-engine-game-development"',
            '"skill_id":"cocos-godot-bridge"',
        ):
            self.assertNotIn(forbidden, skill_registry)

        module_registry = read(REGISTRY)
        self.assertNotIn("COCOS_PATTERN_ABSORPTION", module_registry)
        self.assertNotIn("COCOS_RUNTIME", module_registry)


if __name__ == "__main__":
    unittest.main()
