from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WATCHLIST = ROOT / "docs" / "knowledge" / "game-development" / "PERIODIC_EXTERNAL_SOURCE_WATCHLIST.md"
LEDGER = ROOT / "docs" / "knowledge" / "game-development" / "PERIODIC_SOURCE_OPERATIONS_LEDGER.json"
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
            "INCREMENTAL_IMPROVEMENT",
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
        self.assertIn("스킬 추가나 owner 변경이 없어도", content)
        self.assertIn("억지 변경", content)
        self.assertIn("실제 Base 변경은 별도 PR", content)
        self.assertIn("scheduler", content.lower())
        self.assertIn("Base는 scheduler", content)
        self.assertNotIn("DISCOVERY_FEED = T1_PRIMARY_OFFICIAL", content)
        self.assertNotIn("DISCOVERY_FEED = T2_PROFESSIONAL_PRACTICE", content)

    def test_source_operations_ledger_is_unique_machine_readable_state(self) -> None:
        self.assertTrue(LEDGER.is_file())
        data = json.loads(LEDGER.read_text(encoding="utf-8"))
        self.assertEqual(1, data["schema_version"])
        self.assertEqual("2026-08-11", data["tracking_started_at"])
        sources = data["sources"]
        self.assertGreaterEqual(len(sources), 33)
        self.assertEqual(len(sources), len({row["source_id"] for row in sources}))

        expected_ids = {
            "godot", "steamworks", "android-games", "google-play-policy",
            "xbox-accessibility", "gpuopen", "gdc-vault", "game-developer",
            "games-user-research", "80-level", "level-design-book",
            "game-accessibility-guidelines", "how-to-market-a-game",
            "deconstructor-of-fun", "hada-geeknews", "gamediscoverco",
            "gameanalytics", "steamdb", "openai", "anthropic",
            "github-copilot", "google-ai-adk", "microsoft-learn", "reedsy",
            "inkle-ink", "yarn-spinner", "igda-game-writing", "emily-short",
            "youtube-official", "blackmagic-davinci", "adobe-premiere",
            "frameio", "vidiq",
        }
        self.assertTrue(expected_ids.issubset({row["source_id"] for row in sources}))

        allowed_cadence = {
            "daily-or-weekly", "weekly", "monthly-or-on-demand",
            "quarterly-or-when-relevant",
        }
        required_keys = {
            "source_id", "name", "domains", "roles", "recommended_cadence",
            "scan_surfaces", "last_successful_scan_at",
            "last_material_candidate_at", "last_base_contribution_at",
            "last_base_contribution_ref",
            "material_candidate_count_since_tracking_start",
            "base_contribution_count_since_tracking_start", "status",
        }
        for row in sources:
            with self.subTest(source_id=row["source_id"]):
                self.assertTrue(required_keys.issubset(row))
                self.assertIn(row["recommended_cadence"], allowed_cadence)
                self.assertTrue(row["domains"])
                self.assertTrue(row["roles"])
                self.assertTrue(row["scan_surfaces"])
                for key in (
                    "last_successful_scan_at",
                    "last_material_candidate_at",
                    "last_base_contribution_at",
                    "last_base_contribution_ref",
                ):
                    self.assertTrue(row[key] is None or isinstance(row[key], str))
                self.assertGreaterEqual(row["material_candidate_count_since_tracking_start"], 0)
                self.assertGreaterEqual(row["base_contribution_count_since_tracking_start"], 0)
                self.assertEqual("ACTIVE", row["status"])

    def test_godot_and_code_engineering_sources_preserve_evidence_boundaries(self) -> None:
        content = WATCHLIST.read_text(encoding="utf-8")
        for required in (
            "CODE_ENGINEERING",
            "Godot Improvement Proposals",
            "Godot Demo Projects",
            "Godot Asset Library",
            "Python official docs / What's New / PEPs",
            "GitHub Actions / Code Security Docs",
            "Git official documentation",
            "OWASP Cheat Sheet Series / ASVS",
            "Google Engineering Practices",
            "proposal은 shipped behavior가 아니다",
            "공식 demo는 보편 architecture 정본이 아니다",
            "Asset Library는 vetted dependency 목록이 아니다",
        ):
            self.assertIn(required, content)

        data = json.loads(LEDGER.read_text(encoding="utf-8"))
        by_id = {row["source_id"]: row for row in data["sources"]}
        expected_ids = {
            "godot-proposals",
            "godot-demo-projects",
            "godot-asset-library",
            "python-official",
            "github-platform-engineering",
            "git-scm",
            "owasp",
            "google-engineering-practices",
        }
        self.assertTrue(expected_ids.issubset(by_id))
        self.assertIn("CODE_ENGINEERING", by_id["godot"]["domains"])
        self.assertIn("source repository", by_id["godot"]["scan_surfaces"])
        self.assertIn("AUTHORITY_TARGET", by_id["godot-proposals"]["roles"])
        self.assertIn("AUTHORITY_TARGET", by_id["godot-demo-projects"]["roles"])
        self.assertIn("DISCOVERY_FEED", by_id["godot-asset-library"]["roles"])
        for source_id in expected_ids:
            self.assertIn("CODE_ENGINEERING", by_id[source_id]["domains"], source_id)

    def test_watchlist_connects_context_extraction_to_fail_closed_auto_merge(self) -> None:
        content = WATCHLIST.read_text(encoding="utf-8")
        for required in (
            "SOURCE_OPERATIONS_LEDGER",
            "SOURCE_CONTEXT_PACKET",
            "CONTEXT_EXTRACTION",
            "CONTEXT_TO_CHANGE",
            "SOURCE_SCAN_AUTO_MERGE_GATE",
            "EVIDENCE_ONLY_UPDATE",
            "ABSORB_EXISTING_OWNER",
            "LOW_RISK_BOUNDED_UPDATE",
            "RULE_OR_BCP_CANDIDATE",
            "BCP_OR_USER_DECISION",
            "reviewed_head_sha",
            "current_head_sha",
            "strict up-to-date",
            "strict_up_to_date:",
            "ci-gate",
            "unresolved review thread",
            "ACTIVE Skill ID",
            "behavior schema",
            "security",
            "permission",
            "license",
            "Ruleset",
            "Required Check",
        ):
            self.assertIn(required, content)
        self.assertNotIn("strict up-to_date:", content)
        self.assertIn("제품·게임·소설·채널", content)
        self.assertIn("EVIDENCE_ONLY_UPDATE | ABSORB_EXISTING_OWNER | LOW_RISK_BOUNDED_UPDATE", content)
        self.assertIn("AUTO_MERGE_BLOCKED", content)
        self.assertIn("실제로 확인한 Source만", content)
        self.assertIn("실제 병합된 뒤에만", content)

    def test_scan_state_checkpoint_does_not_force_daily_no_change_prs(self) -> None:
        content = WATCHLIST.read_text(encoding="utf-8")
        self.assertIn("SCAN_STATE_BATCH", content)
        self.assertIn("NO_CHANGE만으로 매일 Ledger-only PR", content)
        self.assertIn("주간 batch checkpoint", content)
        self.assertIn("material change", content)

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
