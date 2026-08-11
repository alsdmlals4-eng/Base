from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SEEDS = ROOT / "docs" / "knowledge" / "game-development" / "PERIODIC_EXTERNAL_SOURCE_DISCOVERY_SEEDS.md"
WATCHLIST = ROOT / "docs" / "knowledge" / "game-development" / "PERIODIC_EXTERNAL_SOURCE_WATCHLIST.md"
ART_GUIDE = ROOT / "docs" / "knowledge" / "game-development" / "ART_DIRECTION_AND_ASSET_PLANNING_GUIDE.md"
SIZE_GUIDE = ROOT / "docs" / "knowledge" / "game-development" / "GAME_BUILD_SIZE_AND_ASSET_OPTIMIZATION_GUIDE.md"


class PeriodicExternalSourceDiscoverySeedTests(unittest.TestCase):
    def test_github_and_solo_gamedev_seeds_preserve_authority_and_format_boundaries(self) -> None:
        self.assertTrue(SEEDS.is_file())
        content = SEEDS.read_text(encoding="utf-8")
        watchlist = WATCHLIST.read_text(encoding="utf-8")

        for required in (
            "ACTIVE_DISCOVERY_SEED",
            "GitHub",
            "repositories",
            "releases",
            "issues",
            "pull requests",
            "discussions",
            "stars",
            "trending",
            "@zang_gamedev",
            "https://www.youtube.com/@zang_gamedev",
            "Shorts",
            "long-form",
            "BLOCKED_UNVERIFIED",
            "PROFESSIONAL_PRACTICE",
            "DISCOVERY_FEED",
            "ORIGINAL_SOURCE_BACKTRACE",
            "repeat_value_confirmed",
            "PERIODIC_SOURCE_OPERATIONS_LEDGER.json",
        ):
            self.assertIn(required, content)

        self.assertIn("GitHub Actions / Code Security Docs", watchlist)
        self.assertIn("GitHub Copilot Docs", watchlist)
        self.assertIn("새 사이트 추가 Gate", watchlist)
        self.assertIn("조회수", content)
        self.assertIn("구독자", content)
        self.assertIn("권위", content)
        self.assertIn("같은 format", content)
        self.assertNotIn("stars = authority", content.lower())
        self.assertNotIn("views = authority", content.lower())

    def test_pixel_art_sources_route_to_existing_art_and_size_owners(self) -> None:
        seeds = SEEDS.read_text(encoding="utf-8")
        art_guide = ART_GUIDE.read_text(encoding="utf-8")
        size_guide = SIZE_GUIDE.read_text(encoding="utf-8")

        for required in (
            "Aseprite",
            "https://www.aseprite.org/docs/",
            "https://github.com/aseprite/aseprite",
            "Saint11",
            "https://saint11.org/blog/pixel-art-tutorials/",
            "Lospec",
            "https://lospec.com/",
            "PixelJoint",
            "https://pixeljoint.com/",
            "AUTHORITY_TARGET",
            "PROFESSIONAL_PRACTICE",
            "DISCOVERY_FEED",
            "integer scaling",
            "nearest",
            "pixel clusters",
            "banding",
            "palette",
            "sprite sheet",
            "BLOCKED_UNVERIFIED",
        ):
            self.assertIn(required, seeds)

        self.assertIn("PERIODIC_EXTERNAL_SOURCE_DISCOVERY_SEEDS.md", art_guide)
        self.assertIn("pixel art", art_guide.lower())
        self.assertIn("Base-wide default", art_guide)
        self.assertIn("pixel art does not automatically prove a smaller shipped build", size_guide.lower())
        self.assertIn("actual build", size_guide.lower())


if __name__ == "__main__":
    unittest.main()
