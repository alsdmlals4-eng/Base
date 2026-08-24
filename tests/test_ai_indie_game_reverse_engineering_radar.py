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
RECEIPT = (
    ROOT
    / "docs"
    / "knowledge"
    / "game-development"
    / "reuse"
    / "AI_ASSISTED_INDIE_PROJECT_ADOPTION_RECEIPT_2026-08-24.md"
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

    def test_current_adoption_state_is_routed_to_execution_receipt(self) -> None:
        radar = RADAR.read_text(encoding="utf-8")
        self.assertIn(
            "current_project_adoption_receipt: docs/knowledge/game-development/reuse/AI_ASSISTED_INDIE_PROJECT_ADOPTION_RECEIPT_2026-08-24.md",
            radar,
        )
        self.assertIn("INITIAL_PATTERN_PACK_STATE_IS_HISTORICAL", radar)

        self.assertTrue(RECEIPT.is_file())
        text = RECEIPT.read_text(encoding="utf-8")
        for required in (
            "status: PROJECT_ADOPTION_EXECUTED",
            "notion_sync: COMPLETE_READBACK",
            "runtime_mutation: NONE",
            "alsdmlals4-eng/omenward#203",
            "alsdmlals4-eng/ninja-survival-godot#25",
            "alsdmlals4-eng/Blacksmith#184",
            "alsdmlals4-eng/GRIMOIRE-#156",
            "alsdmlals4-eng/Switchy-Express-Cargo-Puzzle#163",
            "alsdmlals4-eng/Tetris#15",
            "alsdmlals4-eng/urban-legend#223",
            "alsdmlals4-eng/MylittleBoat#3",
            "alsdmlals4-eng/Ten-Paces-Hidden-Moves#190",
            "alsdmlals4-eng/Coc-Fiction#51",
            "RUNTIME_AI_NOT_PROMOTED",
            "PROJECT_SPECIFIC_ADAPTATION_NOT_SHARED_RUNTIME_MODULE",
        ):
            with self.subTest(required=required):
                self.assertIn(required, text)


if __name__ == "__main__":
    unittest.main()
