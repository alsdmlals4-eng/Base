"""Regression guards for Notion research inputs and safe legacy export.

These test repository documentation contracts, not Notion UI/API behavior.
Each assertion is scoped to its responsible section so historical mentions
elsewhere cannot accidentally satisfy an active instruction.
"""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
SEEDS = ROOT / "docs/knowledge/game-development/PERIODIC_EXTERNAL_SOURCE_DISCOVERY_SEEDS.md"
MIGRATION = ROOT / "templates/project-operations/NOTION_TO_REPOSITORY_MIGRATION_CHECKLIST.md"


def section(text: str, heading: str) -> str:
    """Return a Markdown heading and its content through the next peer/parent."""
    match = re.search(r"^" + re.escape(heading) + r"\s*$", text, re.MULTILINE)
    if match is None:
        raise AssertionError(f"Missing active section: {heading}")
    level = len(heading) - len(heading.lstrip("#"))
    following = re.search(r"^#{1," + str(level) + r"} ", text[match.end():], re.MULTILINE)
    end = match.end() + following.start() if following else len(text)
    return text[match.start():end]


class NotionResearchAndExportBoundaries(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.seeds = section(SEEDS.read_text(encoding="utf-8"),
                            "## 12. Notion skills, work structure, and utilization workflow")
        cls.migration = MIGRATION.read_text(encoding="utf-8")

    def test_existing_official_seed_and_weekly_cadence_are_preserved(self) -> None:
        for token in ("seed_group: notion-skills-work-structure", "status: ACTIVE_DISCOVERY_SEED",
                      "source_role: AUTHORITY_TARGET_FOR_NOTION_BEHAVIOR", "recommended_cadence: weekly"):
            with self.subTest(token=token):
                self.assertIn(token, self.seeds)

    def test_practitioner_sources_are_actionable_and_not_official_authority(self) -> None:
        practice = section(self.seeds, "### 12.3 비공식 실무·게임 개발 조사 lane")
        for url in ("https://www.notion.vip/insights/streamline-project-management-with-notion",
                    "https://thomasjfrank.com/docs/ultimate-tasks/databases/"):
            with self.subTest(url=url):
                rows = [line for line in practice.splitlines() if line.startswith("|") and url in line]
                self.assertEqual(len(rows), 1)
                self.assertIn("`PROFESSIONAL_PRACTICE`", rows[0])
                self.assertNotIn("AUTHORITY_TARGET", rows[0])
                self.assertIn("상업 이해관계", rows[0])
        self.assertIn("비공식 자료로 공식 제품 사실을 확정하지 않는다", practice)

    def test_game_and_community_lanes_preserve_source_ceiling(self) -> None:
        practice = section(self.seeds, "### 12.3 비공식 실무·게임 개발 조사 lane")
        for token in ("인디/솔로", "스튜디오", "GDD", "postmortem",
                      "https://arxiv.org/abs/2202.06183", "표본",
                      "https://www.notion.com/templates/game-design-document",
                      "OBSERVATIONAL_DATA_OR_VENDOR_GUIDE", "DISCOVERY_FEED", "Reddit"):
            with self.subTest(token=token):
                self.assertIn(token, practice)

    def test_research_routes_to_existing_owner_not_a_second_canon(self) -> None:
        for token in ("DESKTOP_GPT_REPOSITORY_FIRST_WORKSPACE_POLICY.md",
                      "REPOSITORY_PRIMARY_CANON", "NO_NEW_NOTION_WRITE_BY_DEFAULT",
                      "FIGMA_USAGE: DISABLED_BY_USER", "ZERO_INCREMENTAL_COST_REQUIRED",
                      "ADOPT / ADAPT / TEST / AVOID / REFERENCE_ONLY", "기존 owner"):
            with self.subTest(token=token):
                self.assertIn(token, self.seeds)
        self.assertNotRegex(self.seeds, r"https?://[^\s|]*(?:figma\.com|huddling\.ai)")

    def test_scan_instructions_do_not_claim_scheduler_or_fabricated_success(self) -> None:
        practice = section(self.seeds, "### 12.3 비공식 실무·게임 개발 조사 lane")
        for token in ("last_successful_scan_at", "실제로 읽은", "scheduler", "실행 증거"):
            with self.subTest(token=token):
                self.assertIn(token, practice)

    def test_skill_auto_selection_is_not_scheduled_autonomy_or_sync(self) -> None:
        skills = section(self.seeds, "### 12.4 Skill 호출·이식성의 현재 검증 경계")
        for token in ("https://www.notion.com/help/create-and-manage-skills",
                      "description", "수동 호출", "자동 선택", "일정", "SKILL.md",
                      "자동 동기화가 아니다", "다시 다운로드", "동일 결과를 보장하지 않는다"):
            with self.subTest(token=token):
                self.assertIn(token, skills)

    def test_export_revalidates_format_and_page_vs_workspace_pdf(self) -> None:
        export = section(self.migration, "### 2.1 Export 범위·권한 대조")
        for token in ("https://www.notion.com/help/export-your-content", "2026-08-31",
                      "workspace 전체 PDF", "개별 페이지 PDF", "HTML", "Markdown", "CSV",
                      "checked_at", "export_format", "exporter_access_scope",
                      "EXPORT_IS_NOT_RESTORE_PROOF"):
            with self.subTest(token=token):
                self.assertIn(token, export)

    def test_export_inventory_covers_hidden_access_views_and_originals(self) -> None:
        export = section(self.migration, "### 2.1 Export 범위·권한 대조")
        for token in ("private", "teamspace", "current/default view", "Form view",
                      "page/record/attachment", "원본 binary", "권한을 자동 확대하지 않는다",
                      "readback", "relation/rollup/formula"):
            with self.subTest(token=token):
                self.assertIn(token, export)

    def test_unknown_inventory_cannot_be_zero_retirement_evidence(self) -> None:
        counters = section(self.migration, "## 10. 이관 잔여 카운터")
        for token in ("UNKNOWN_IS_NOT_ZERO", "inventory_scope_status", "INCOMPLETE", "UNKNOWN",
                      "COMPLETE", "LEGACY_READ_ONLY", "null", "NOTION_UNIQUE_CANON_COUNT"):
            with self.subTest(token=token):
                self.assertIn(token, counters)
        receipt = section(self.migration, "## 12. 완료 receipt")
        self.assertIn("inventory_scope_status:", receipt)
        self.assertIn("export_receipt:", receipt)

    def test_retirement_decision_itself_requires_complete_readback(self) -> None:
        counters = section(self.migration, "## 10. 이관 잔여 카운터")
        decision = counters.split("판정:", 1)[1]
        self.assertIn("inventory_scope_status != COMPLETE", decision)
        self.assertIn("미확정(null)", decision)
        self.assertIn("모두 0 + inventory_scope_status=COMPLETE + source/export/repository readback 완료", decision)

    def test_five_loops_are_not_five_separate_review_lenses(self) -> None:
        review = section(self.migration, "## 11. 적대적 검토 5회")
        self.assertIn("매 회차", review)
        self.assertIn("다섯 관점을 모두", review)
        self.assertIn("최소 5회", review)
        self.assertIn("running-adversarial-review-and-refinement/SKILL.md", review)
        self.assertNotRegex(review, r"(?m)^### Loop [1-5]",
                            msg="Review lenses must not be counted as full loops")

    def test_existing_binary_and_no_delete_safeguards_remain(self) -> None:
        binary = section(self.migration, "## 5. 이미지·파일·binary 이관")
        for token in ("원본 binary", "SHA-256", "actual consumer", "readback"):
            with self.subTest(token=token):
                self.assertIn(token, binary)
        self.assertIn("NO_DELETE_REQUIRED_FOR_RETIREMENT", self.migration)
        self.assertIn("test PASS ≠ runtime PASS ≠ UX PASS ≠ player PASS", self.migration)


if __name__ == "__main__":
    unittest.main()
