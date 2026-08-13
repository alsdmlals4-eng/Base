from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SEEDS = ROOT / "docs" / "knowledge" / "game-development" / "PERIODIC_EXTERNAL_SOURCE_DISCOVERY_SEEDS.md"
WATCHLIST = ROOT / "docs" / "knowledge" / "game-development" / "PERIODIC_EXTERNAL_SOURCE_WATCHLIST.md"
ART_GUIDE = ROOT / "docs" / "knowledge" / "game-development" / "ART_DIRECTION_AND_ASSET_PLANNING_GUIDE.md"
SIZE_GUIDE = ROOT / "docs" / "knowledge" / "game-development" / "GAME_BUILD_SIZE_AND_ASSET_OPTIMIZATION_GUIDE.md"
BENCHMARK = ROOT / "skills" / "analyzing-and-refining-game-concepts" / "references" / "benchmark-player-evidence-and-playtests.md"


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

    def test_figma_market_success_and_kick_sources_preserve_metric_boundaries(self) -> None:
        seeds = SEEDS.read_text(encoding="utf-8")
        benchmark = BENCHMARK.read_text(encoding="utf-8")
        combined = seeds + "\n" + benchmark

        for required in (
            "Figma practical design workflow",
            "help.figma.com",
            "Auto Layout",
            "Variants",
            "Variables",
            "FigJam",
            "Dev Mode",
            "SteamDB",
            "GameDiscoverCo",
            "Sensor Tower",
            "VERIFIED_100K_DOWNLOAD_INSTALL",
            "VERIFIED_100K_SALES",
            "ESTIMATED_100K_PLUS",
            "Shattered Pixel Dungeon",
            "Mindustry",
            "Slice & Dice",
            "Sledding Game",
            "God Of Weapons",
            "Astrea: Six-Sided Oracles",
            "PLAYER_NOTICEABLE",
            "LOOP_RELEVANT",
            "MARKET_LEGIBLE",
            "PRODUCTION_FIT",
            "NON_DERIVATIVE",
        ):
            self.assertIn(required, combined)

        self.assertIn("downloads", combined.lower())
        self.assertIn("sales", combined.lower())
        self.assertIn("estimate", combined.lower())
        self.assertIn("causal", combined.lower())

    def test_prompt_planning_writing_work_structure_executable_and_asset_sources_route_to_existing_owners(self) -> None:
        seeds = SEEDS.read_text(encoding="utf-8")

        for required in (
            "Prompt engineering / evaluation / security",
            "DSPy official docs + repository",
            "https://dspy.ai/",
            "promptfoo official docs + repository",
            "https://www.promptfoo.dev/docs/",
            "OWASP GenAI Security Project",
            "https://genai.owasp.org/",
            "DAIR.AI Prompt Engineering Guide",
            "https://github.com/dair-ai/Prompt-Engineering-Guide",
            "OpenAI official prompting / evals / instruction hierarchy",
            "Anthropic prompt engineering / evals",
            "Gemini prompt design strategies",
            "Game design / planning research and system modeling",
            "DiGRA Digital Library",
            "https://dl.digra.org/",
            "Game Studies",
            "https://gamestudies.org/",
            "MDA: A Formal Approach to Game Design and Game Research",
            "Game Design Patterns",
            "Game Design Workshop",
            "Machinations docs + original modeling research",
            "https://machinations.io/docs",
            "Writing craft / Korean prose / story industry",
            "국립국어원",
            "https://www.korean.go.kr/",
            "한국콘텐츠진흥원 / Storyum",
            "https://www.storyum.kr/",
            "Writing Excuses",
            "https://writingexcuses.com/",
            "Brandon Sanderson BYU writing class",
            "Jane Friedman",
            "Writer's Digest",
            "Writer Beware",
            "Work structure / documentation / decision methods",
            "Diátaxis",
            "Architecture Decision Records",
            "C4 model",
            "DORA",
            "Skill / addon / executable source discovery and quarantine",
            "Agent Skills specification",
            "anthropics/skills",
            "obra/superpowers",
            "skills.sh",
            "OpenSSF Scorecard",
            "OSV / OSV-Scanner",
            "deps.dev",
            "SLSA",
            "Godot Asset Store / reusable production assets",
            "Godot Asset Store",
            "Godot Asset Library",
            "godotengine/awesome-godot",
            "GDQuest",
            "Kenney",
            "Poly Haven",
            "Freesound",
            "OpenGameArt",
            "Godot Shaders",
            "AI_WORKFLOW_AND_PROMPT_SOURCE_NOTES.md",
            "AI_SKILL_ADOPTION_GUIDE.md",
            "analyzing-and-refining-game-concepts",
            "GAME_FEATURE_DESIGN_SPEC.md",
            "managing-design-documents",
            "developing-and-revising-serial-fiction",
            "NARRATIVE_AND_RELATIONSHIP_METHOD.md",
            "ART_DIRECTION_AND_ASSET_PLANNING_GUIDE.md",
            "GAME_BUILD_SIZE_AND_ASSET_OPTIMIZATION_GUIDE.md",
            "prompt popularity != authority",
            "optimizer score != project correctness",
            "red-team tool pass != security/compliance PASS",
            "framework != universal design law",
            "simulation != playtest",
            "어문 규범 준수 != 문학적 완성도",
            "creator advice != universal craft law",
            "author popularity != permission to copy voice or style",
            "listing != vetted dependency",
            "discovery-only",
            "이번 등록은 durable Watchlist/Ledger 승격이 아니다",
        ):
            self.assertIn(required, seeds)


if __name__ == "__main__":
    unittest.main()
