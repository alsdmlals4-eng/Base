from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RADAR = ROOT / "docs" / "knowledge" / "game-development" / "AI_GAME_AND_AI_ASSISTED_INDIE_RADAR.md"
PACK = (
    ROOT
    / "docs"
    / "knowledge"
    / "game-development"
    / "reuse"
    / "AI_ASSISTED_INDIE_PATTERN_PACK_2026-08-24.md"
)


class AiIndieGameReverseEngineeringRadarTests(unittest.TestCase):
    def test_specialty_radar_preserves_existing_authority_and_weekly_capture(self) -> None:
        self.assertTrue(RADAR.is_file())
        text = RADAR.read_text(encoding="utf-8")
        for required in (
            "PERIODIC_EXTERNAL_SOURCE_WATCHLIST.md",
            "REVERSE_ENGINEERING_REUSE_PIPELINE.md",
            "scheduler_authority: EXTERNAL_TO_BASE",
            "recommended_cadence: weekly",
            "PRODUCTION_ASSISTED",
            "RUNTIME_GENERATIVE",
            "popularity_is_not_authority: true",
            "compare_with_previous_scan: true",
            "ADOPT | ADAPT | TEST | REJECT | REFERENCE_ONLY",
        ):
            with self.subTest(required=required):
                self.assertIn(required, text)

    def test_pattern_pack_captures_success_failure_and_reuse_boundaries(self) -> None:
        self.assertTrue(PACK.is_file())
        text = PACK.read_text(encoding="utf-8")
        for required in (
            "Slotbound",
            "Ashen Crown",
            "Express 404",
            "Infinite Arcana",
            "Vapor World: Over the Mind",
            "HUMAN_DIRECTED_AI_BUILD_LOOP",
            "SILENT_OMISSION_GATE",
            "CONTEXT_SCOPE_AND_ARCHITECTURE_BUDGET",
            "BREADTH_AFTER_CORE_IDENTITY_LOCK",
            "PLAYER_FEEDBACK_REBUILD_LOOP",
            "AI_VISIBLE_OUTPUT_QUALITY_GATE",
            "RNG_AGENCY_AND_RECOVERY",
            "Implementation Reality Gate",
            "Adversarial review 5/5",
            "PROJECT_ADOPTION_NOT_RUN",
        ):
            with self.subTest(required=required):
                self.assertIn(required, text)


if __name__ == "__main__":
    unittest.main()
