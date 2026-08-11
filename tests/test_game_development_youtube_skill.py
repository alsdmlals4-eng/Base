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
            "STORY_EVIDENCE_EDIT_FIRST",
            "VERSIONED_REVIEW",
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

    def test_skill_defines_story_first_edit_and_versioned_review(self) -> None:
        text = self.read_required(SKILL_PATH)
        for token in (
            "STORY_AND_EVIDENCE_ROUGH_CUT",
            "CLARITY_AND_PACING_TRIM",
            "DIALOGUE_AND_AUDIO_CLEANUP",
            "GRAPHICS_CAPTIONS_AND_CONTEXT",
            "COLOR_VFX_AND_POLISH",
            "EXPORT_AND_PLAYBACK_QC",
            "KEEP | CHANGE | REJECT | QUESTION",
            "YOUTUBE_AND_VIDEO_EDITING",
        ):
            self.assertIn(token, text)

    def test_skill_treats_retention_as_observation_not_causality(self) -> None:
        text = self.read_required(SKILL_PATH)
        for token in (
            "impressions·CTR·views·unique viewers",
            "watch time·average view duration·key moments for audience retention",
            "new·casual·regular/returning viewer",
            "drop·spike·rewatch",
            "원인이라고 자동 단정하지 않고",
            "OBSERVATIONAL_DATA_OR_VENDOR_GUIDE",
        ):
            self.assertIn(token, text)

    def test_title_thumbnail_package_can_record_platform_ab_experiment(self) -> None:
        skill = self.read_required(SKILL_PATH)
        packet = self.read_required(PACKET_PATH)
        for text in (skill, packet):
            for token in (
                "youtube_package_experiment:",
                "feature_support_checked_at:",
                "eligibility_status: AVAILABLE | UNAVAILABLE | BLOCKED_UNVERIFIED",
                "tested_packages:",
                "test_started_at:",
                "test_ended_at:",
                "platform_result:",
                "watch_time_result:",
                "ctr_context:",
                "confounders:",
                "KEEP | CHANGE | INSUFFICIENT_SAMPLE | NOT_RUN",
            ):
                self.assertIn(token, text)

        self.assertIn("watch time", skill.lower())
        self.assertIn("CTR 단독", skill)
        self.assertIn("게임 수요", skill)
        self.assertIn("지원·자격", skill)
        self.assertIn("선택 사항", skill)

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
            "Story-and-evidence edit passes",
            "Versioned edit review rounds",
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

        for token in (
            "traffic_sources",
            "impressions_ctr",
            "unique_viewers",
            "average_view_duration",
            "key_moments_for_audience_retention",
            "benchmark_sample_and_context",
            "Retention drops, spikes, and rewatches are observations",
        ):
            self.assertIn(token, text)

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

    def test_repository_checks_do_not_claim_human_marketing_results(self) -> None:
        text = self.read_required(SKILL_PATH)
        self.assertIn("정적 테스트 통과를 `HUMAN_NOT_RUN` 해소로 보고한다", text)
        self.assertIn("human_audience_validation: HUMAN_NOT_RUN", text)
        self.assertIn("conversion_validation: CONVERSION_UNVERIFIED", text)
        self.assertIn("production_marketing_effectiveness: NOT_PROVEN", text)

    def test_unadapted_base_skill_does_not_invent_shared_project_route(self) -> None:
        routes = json.loads(self.read_required(SHARED_ROUTES_PATH))
        serialized = json.dumps(routes, ensure_ascii=False)
        self.assertNotIn(SKILL_ID, serialized)


if __name__ == "__main__":
    unittest.main()
