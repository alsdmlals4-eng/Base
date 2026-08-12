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
            "ART_DIRECTION_AND_ASSET_PLANNING_GUIDE.md",
            "GAME_BUILD_SIZE_AND_ASSET_OPTIMIZATION_GUIDE.md",
            "designing-art-prompts-and-technique-cards",
            "BLOCKED_UNVERIFIED",
        ):
            self.assertIn(required, seeds)

        self.assertIn("Visual Requirement Gate", art_guide)
        self.assertIn("2D·pixel art 보호", size_guide)
        for measurement_type in ("DOWNLOAD", "INSTALLED", "RUNTIME", "PATCH"):
            self.assertIn(measurement_type, size_guide)
        self.assertIn("pixel art", seeds.lower())
        self.assertIn("base-wide default", seeds.lower())
        self.assertIn("smaller shipped build", seeds.lower())
        self.assertIn("actual build", seeds.lower())

    def test_backend_ai_deploy_and_media_sources_route_to_existing_owners(self) -> None:
        seeds = SEEDS.read_text(encoding="utf-8")

        for required in (
            "Backend / API engineering",
            "OpenAPI Specification",
            "FastAPI official",
            "PostgreSQL official",
            "OWASP API Security",
            "AI coding / coding agents",
            "OpenAI Developers / Codex",
            "Claude Code",
            "Gemini CLI",
            "aider",
            "SWE-bench",
            "Deployment / WAS / cloud runtime",
            "Cloudflare Workers",
            "Fly.io Machines",
            "Railway",
            "Render",
            "PC capture and AI-assisted media editing",
            "OBS Studio",
            "FFmpeg",
            "Xbox Game Bar",
            "NVIDIA App / ShadowPlay",
            "DaVinci Resolve",
            "Adobe Premiere / Photoshop / Firefly",
            "Runway",
            "GAME_BACKEND_CLOUD_RUN_AND_ONLINE_SERVICES_GUIDE.md",
            "AI_ASSISTED_GAME_DEVELOPMENT_GUIDE.md",
            "producing-game-development-youtube-videos",
            "designing-art-prompts-and-technique-cards",
            "Cloud Run is not universally better",
            "benchmark score does not prove project correctness",
            "actual PC capture measurement",
            "rights + provenance + similarity",
        ):
            self.assertIn(required, seeds)


if __name__ == "__main__":
    unittest.main()
