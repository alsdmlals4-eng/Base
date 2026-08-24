from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RADAR_PATH = ROOT / "docs" / "knowledge" / "game-development" / "TRPG_RULE_DESIGN_REFERENCE_RADAR.md"
README_PATH = ROOT / "docs" / "knowledge" / "game-development" / "README.md"
CATALOG_PATH = ROOT / "docs" / "knowledge" / "game-development" / "REFERENCE_SOURCE_CATALOG.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class TrpgRuleDesignReferenceRadarTests(unittest.TestCase):
    def test_radar_is_routed_without_new_project_authority(self) -> None:
        self.assertTrue(RADAR_PATH.is_file())
        radar = read(RADAR_PATH)
        hub = read(README_PATH)
        catalog = read(CATALOG_PATH)

        self.assertIn("TRPG_RULE_DESIGN_REFERENCE_RADAR.md", hub)
        self.assertIn("TRPG_RULE_DESIGN_REFERENCE_RADAR.md", catalog)
        self.assertIn("execution_authority: none", radar)
        self.assertIn("project_canon_authority: none", radar)

    def test_radar_keeps_analysis_pedagogy_and_rights_fields(self) -> None:
        radar = read(RADAR_PATH)

        for term in (
            "problem_solved:",
            "mechanic_solution:",
            "chapter_or_teaching_order:",
            "progressive_disclosure:",
            "example_and_reference_strategy:",
            "support_artifacts:",
            "gm_player_information_boundary:",
            "REFERENCE_SCHEMA_IS_NOT_TEACHING_ORDER",
            "SUPPORT_ARTIFACT_IS_PLAY_INTERFACE",
            "FREE_PUBLICATION != OPEN_REUSE",
            "ADOPT / ADAPT / TEST / AVOID / REFERENCE_ONLY",
        ):
            self.assertIn(term, radar)

    def test_user_fixed_sources_are_preserved_with_fail_closed_access(self) -> None:
        radar = read(RADAR_PATH)

        for source in (
            "https://cympub.kr/",
            "https://sites.google.com/view/dwtemporary/",
            "https://www.trpgclub.com/",
            "https://www.dropbox.com/scl/fo/ujjpyxy96tem420xotrpy/AKPLR0cPK7cifVgK5mTdYh8",
            "https://blog.naver.com/adventurekeeper",
            "https://hangyul219-prog.github.io/TRPG-/",
        ):
            self.assertIn(source, radar)

        self.assertIn("UNVERIFIED_DIRECT_ACCESS", radar)

    def test_project_specific_eclipse_values_do_not_leak_into_base_reference(self) -> None:
        radar = read(RADAR_PATH)

        for forbidden in (
            "에르강티아",
            "균열의 마석",
            "디멘션 가디언",
            "아젠티온",
        ):
            self.assertNotIn(forbidden, radar)


if __name__ == "__main__":
    unittest.main()
