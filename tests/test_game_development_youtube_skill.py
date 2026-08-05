from __future__ import annotations

import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_ID = "producing-game-development-youtube-videos"
SKILL_PATH = ROOT / f"skills/{SKILL_ID}/SKILL.md"
PACKET_PATH = ROOT / "templates/game-development-youtube/EPISODE_PACKET.md"
REGISTRY_PATH = ROOT / "skills/SKILL_REGISTRY.json"
COVERAGE_PATH = ROOT / "skills/SKILL_BEHAVIOR_COVERAGE_EVALS.json"
EVIDENCE_PATH = ROOT / "skills/SKILL_IMPLEMENTATION_EVIDENCE.json"
SHARED_ROUTES_PATH = ROOT / "skills/BASE_SHARED_SKILL_ROUTES.json"


class GameDevelopmentYouTubeSkillTests(unittest.TestCase):
    maxDiff = None

    def read_required(self, path: Path) -> str:
        self.assertTrue(path.is_file(), f"Required artifact is missing: {path.relative_to(ROOT)}")
        return path.read_text(encoding="utf-8")

    def test_skill_contract_and_modes_are_present(self) -> None:
        text = self.read_required(SKILL_PATH)
        self.assertRegex(text, rf"(?m)^name:\s*{re.escape(SKILL_ID)}\s*$")
        self.assertRegex(text, r"(?m)^description:\s*Use when\b")
        for mode in (
            "channel-portfolio",
            "episode-concept",
            "script-and-shot-plan",
            "title-thumbnail-package",
            "production-and-publish",
            "analytics-review",
        ):
            self.assertIn(f"`{mode}`", text)

    def test_skill_enforces_truthful_publication_and_sample_limits(self) -> None:
        text = self.read_required(SKILL_PATH)
        for token in (
            "PROJECT_CANON_AND_ACTUAL_BUILD_FIRST",
            "ONE_VIEWER_JOB",
            "ONE_EPISODE_PROMISE",
            "ACTUAL_BUILD_EVIDENCE",
            "TITLE_THUMBNAIL_PROMISE_MATCH",
            "RIGHTS_RATING_SPOILER_SECURITY_REVIEW",
            "ONE_PRIMARY_CTA",
            "ANALYTICS_WITH_SAMPLE_LIMITS",
            "BLOCKED_UNVERIFIED",
            "PUBLICATION_BOUNDARY_UNVERIFIED",
            "RIGHTS_OR_RATING_UNVERIFIED",
            "CONVERSION_UNVERIFIED",
            "HUMAN_NOT_RUN",
            "INSUFFICIENT_SAMPLE",
            "KEEP",
            "CHANGE",
            "STOP",
        ):
            self.assertIn(token, text)

    def test_skill_preserves_owner_boundaries(self) -> None:
        text = self.read_required(SKILL_PATH)
        for owner in (
            "analyzing-and-refining-game-concepts",
            "designing-vertical-slices",
            "designing-art-prompts-and-technique-cards",
            "reviewing-and-validating-project-changes",
        ):
            self.assertIn(owner, text)
        for boundary in (
            "게임 자체 기획",
            "썸네일 이미지 생성",
            "플랫폼 심사",
            "에셋 권리 원장",
            "영상 편집 도구",
            "프로젝트별 KPI 절대값",
        ):
            self.assertIn(boundary, text)

    def test_episode_packet_contains_complete_evidence_loop(self) -> None:
        text = self.read_required(PACKET_PATH)
        for heading in (
            "Project canon and actual build evidence",
            "Target viewer and episode job",
            "One-sentence promise",
            "Conflict, change, and visible result",
            "Marketing stage and primary CTA",
            "Spoiler, confidentiality, security, rights, and rating limits",
            "Hook alternatives",
            "Script",
            "Shot list and capture evidence",
            "Edit beat sheet",
            "Title and thumbnail packages",
            "Description, chapters, pinned comment, playlist, and end screen",
            "Shorts derivatives",
            "Pre-publish adversarial review",
            "Publish record",
            "Analytics precommit",
            "Analytics result and sample limits",
            "KEEP / CHANGE / STOP / INSUFFICIENT_SAMPLE",
            "Learning and next experiment",
        ):
            self.assertIn(f"## {heading}", text)

    def test_registry_behavior_and_evidence_surfaces_are_synchronized(self) -> None:
        registry = json.loads(self.read_required(REGISTRY_PATH))
        entries = {entry["skill_id"]: entry for entry in registry["skills"]}
        self.assertIn(SKILL_ID, entries)
        entry = entries[SKILL_ID]
        self.assertEqual("ACTIVE", entry["status"])
        self.assertEqual("specialist", entry["layer"])
        self.assertEqual("game-marketing-content-production", entry["discipline"])
        self.assertFalse(entry["load_by_default"])

        coverage = json.loads(self.read_required(COVERAGE_PATH))
        cases = coverage["cases"]
        self.assertTrue(any(case["expected_primary_skill"] == SKILL_ID for case in cases))
        self.assertTrue(any(SKILL_ID in case["forbidden_skills"] for case in cases))

        evidence = json.loads(self.read_required(EVIDENCE_PATH))
        indexed = {entry["skill_id"]: entry for entry in evidence["entries"]}
        self.assertIn(SKILL_ID, indexed)
        self.assertTrue(
            any(
                item["kind"] == "TEST"
                and item["path"] == "tests/test_game_development_youtube_skill.py"
                for item in indexed[SKILL_ID]["evidence"]
            )
        )

    def test_unadapted_base_skill_does_not_invent_shared_project_route(self) -> None:
        routes = json.loads(self.read_required(SHARED_ROUTES_PATH))
        serialized = json.dumps(routes, ensure_ascii=False)
        self.assertNotIn(SKILL_ID, serialized)


if __name__ == "__main__":
    unittest.main()
