from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WATCHLIST = ROOT / "docs" / "knowledge" / "game-development" / "PERIODIC_EXTERNAL_SOURCE_WATCHLIST.md"
RECENT_REVIEW = ROOT / "docs" / "knowledge" / "game-development" / "RECENT_EXTERNAL_EVIDENCE_REVIEW_2026-08-10.md"
HUB = ROOT / "docs" / "knowledge" / "game-development" / "README.md"
METHOD = ROOT / "docs" / "knowledge" / "game-development" / "EVIDENCE_BASED_GAME_DEVELOPMENT_METHOD.md"
PLANNING_POLICY = ROOT / "docs" / "PLANNING_SEQUENCE_AND_EVIDENCE_POLICY.md"
AI_SKILL_GUIDE = ROOT / "docs" / "AI_SKILL_ADOPTION_GUIDE.md"
NARRATIVE_METHOD = ROOT / "docs" / "knowledge" / "methods" / "NARRATIVE_AND_RELATIONSHIP_METHOD.md"
NARRATIVE_TEMPLATE = ROOT / "templates" / "planning" / "NARRATIVE_CONTENT_PLAN.md"
YOUTUBE_SKILL = ROOT / "skills" / "producing-game-development-youtube-videos" / "SKILL.md"
WORKFLOW = ROOT / ".github" / "workflows" / "validate-evidence-knowledge.yml"


class PeriodicExternalSourceWatchlistTests(unittest.TestCase):
    def test_watchlist_contract_exists_and_preserves_source_authority(self) -> None:
        self.assertTrue(WATCHLIST.is_file())
        content = WATCHLIST.read_text(encoding="utf-8")

        for required in (
            "Hada GeekNews",
            "Godot",
            "Steamworks",
            "GDC Vault",
            "Games User Research",
            "GameDiscoverCo",
            "SteamDB",
            "OpenAI",
            "Anthropic Engineering",
            "GitHub Copilot Docs",
            "Google Developers Blog",
            "Microsoft Learn",
            "PROMPT_AND_AGENT_WORKFLOW",
            "SKILL_AUTHORING_AND_EVOLUTION",
            "Reedsy",
            "inkle / ink",
            "Yarn Spinner",
            "IGDA Game Writing",
            "FICTION_AND_INTERACTIVE_NARRATIVE",
            "YouTube Analytics",
            "Blackmagic Design DaVinci Resolve",
            "Adobe Premiere official release notes",
            "Frame.io Insider",
            "vidIQ",
            "YOUTUBE_AND_VIDEO_EDITING",
            "AUTHORITY_TARGET",
            "PROFESSIONAL_PRACTICE",
            "DISCOVERY_FEED",
            "OBSERVATIONAL_DATA_OR_VENDOR_GUIDE",
            "ORIGINAL_SOURCE_BACKTRACE",
            "ADOPT",
            "ADAPT",
            "TEST",
            "AVOID",
            "IGNORE",
            "REFERENCE_ONLY",
            "ABSORB_EXISTING_OWNER",
            "RULE_OR_BCP_CANDIDATE",
            "2026-02-10",
            "2026-08-10",
            "FULL_INDEX_REVIEW",
            "PARTIAL_INDEX_REVIEW",
            "BCP_OR_USER_DECISION",
        ):
            self.assertIn(required, content)

        self.assertIn("새 규칙이 없다는 이유만으로", content)
        self.assertIn("같은 Goal의 열린·최근 병합 PR", content)
        self.assertIn("적대적 검토", content)
        self.assertIn("scheduler", content.lower())
        self.assertIn("Base는 scheduler", content)
        self.assertNotIn("DISCOVERY_FEED = T1_PRIMARY_OFFICIAL", content)
        self.assertNotIn("DISCOVERY_FEED = T2_PROFESSIONAL_PRACTICE", content)

    def test_recent_six_month_review_records_coverage_and_dispositions(self) -> None:
        self.assertTrue(RECENT_REVIEW.is_file())
        content = RECENT_REVIEW.read_text(encoding="utf-8")

        for required in (
            "2026-02-10",
            "2026-08-10",
            "FULL_INDEX_REVIEW",
            "PARTIAL_INDEX_REVIEW",
            "NO_CHANGE",
            "EVIDENCE_ONLY_UPDATE",
            "LOW_RISK_BOUNDED_UPDATE",
            "REJECTED_OVERGENERALIZATION",
            "원출처",
            "Base overlap",
            "PROMPT_AND_AGENT_WORKFLOW",
            "SKILL_AUTHORING_AND_EVOLUTION",
            "FICTION_AND_INTERACTIVE_NARRATIVE",
            "YOUTUBE_AND_VIDEO_EDITING",
            "OpenAI",
            "Anthropic",
            "GitHub Copilot",
            "Reedsy",
            "Yarn Spinner",
            "YouTube Analytics",
            "DaVinci Resolve",
        ):
            self.assertIn(required, content)

    def test_existing_evidence_authorities_link_to_watchlist_one_hop(self) -> None:
        for path in (HUB, METHOD, PLANNING_POLICY, AI_SKILL_GUIDE, NARRATIVE_METHOD, YOUTUBE_SKILL):
            self.assertTrue(path.is_file())
            content = path.read_text(encoding="utf-8")
            self.assertIn("PERIODIC_EXTERNAL_SOURCE_WATCHLIST.md", content, str(path))

    def test_prompt_instruction_skill_agent_placement_is_explicit(self) -> None:
        content = AI_SKILL_GUIDE.read_text(encoding="utf-8")
        for required in (
            "Prompt / Instruction / Skill / Agent / Tool 배치 결정",
            "repository/global instruction",
            "path/domain-specific instruction",
            "prompt/template",
            "progressive disclosure",
            "deterministic script/tool",
            "goal:",
            "source_of_truth:",
            "protected_constraints:",
            "edge_cases:",
            "stop_or_handoff_conditions:",
            "unverified_or_missing_input_behavior:",
            "Skill 수, agent 수, prompt 파일 수는 능력 지표가 아니다",
            "harness·tool·permission·budget·configuration",
            "consumer surface",
            "지원 여부가 surface마다 다를 수 있다",
            "head branch",
        ):
            self.assertIn(required, content)

    def test_fiction_to_game_narrative_transfer_preserves_medium_boundaries(self) -> None:
        content = NARRATIVE_METHOD.read_text(encoding="utf-8")
        for required in (
            "소설 ↔ 게임 스토리 전이 경계",
            "공통으로 재사용 가능한 것",
            "소설에서 별도로 보호할 것",
            "게임에서 추가할 것",
            "플레이어 agency",
            "branch budget",
            "CANON_AND_CONTINUITY",
            "DEVELOPMENTAL_STRUCTURE",
            "SCENE_AND_CHARACTER",
            "DIALOGUE_AND_INFORMATION",
            "LINE_AND_PROSE",
            "COPY_AND_PROOF",
            "CROSS_RANGE_RECONCILIATION",
            "게임 스토리에는 ADAPT",
            "SELECTION_QUERY_READ_ONLY",
            "STATE_COMMIT_AFTER_SELECTION",
        ):
            self.assertIn(required, content)

    def test_narrative_template_does_not_point_to_missing_legacy_method(self) -> None:
        content = NARRATIVE_TEMPLATE.read_text(encoding="utf-8")
        self.assertIn("docs/knowledge/methods/NARRATIVE_AND_RELATIONSHIP_METHOD.md", content)
        self.assertNotIn("docs/planning/NARRATIVE_CONTENT_METHOD.md", content)

    def test_dedicated_workflow_executes_watchlist_contract(self) -> None:
        self.assertTrue(WORKFLOW.is_file())
        content = WORKFLOW.read_text(encoding="utf-8")
        self.assertGreaterEqual(content.count("tests/test_periodic_external_source_watchlist.py"), 4)
        self.assertIn("tests/test_game_development_youtube_skill.py", content)
        self.assertIn("contents: read", content)
        self.assertNotIn("contents: write", content)


if __name__ == "__main__":
    unittest.main()
