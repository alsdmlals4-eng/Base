"""Regression contracts for Notion research and loss-aware legacy migration.

These tests inspect repository guidance, not a live Notion workspace. Passing
cannot establish scheduler execution, export completeness, or runtime parity.
"""

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
SEEDS = ROOT / "docs/knowledge/game-development/PERIODIC_EXTERNAL_SOURCE_DISCOVERY_SEEDS.md"
MIGRATION = ROOT / "templates/project-operations/NOTION_TO_REPOSITORY_MIGRATION_CHECKLIST.md"


def section(text: str, heading: str, following: str) -> str:
    """Return an existing bounded section, failing clearly on a broken route."""
    _, found, tail = text.partition(heading)
    if not found:
        raise AssertionError(f"Missing section: {heading}")
    body, found, _ = tail.partition(following)
    if not found:
        raise AssertionError(f"Missing following section: {following}")
    return body


class NotionResearchMigrationBoundaryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.seeds = SEEDS.read_text(encoding="utf-8")
        cls.notion = section(cls.seeds, "## 12. Notion", "## 13. Game market")
        cls.migration = MIGRATION.read_text(encoding="utf-8")

    def assert_terms(self, text: str, *terms: str) -> None:
        for term in terms:
            with self.subTest(term=term):
                self.assertIn(term, text)

    def test_research_keeps_repository_canon_and_retired_figma_boundary(self) -> None:
        self.assert_terms(
            self.notion,
            "DESKTOP_GPT_REPOSITORY_FIRST_WORKSPACE_POLICY.md",
            "NO_NEW_NOTION_WRITE_BY_DEFAULT",
            "FIGMA_USAGE: DISABLED_BY_USER",
            "ZERO_INCREMENTAL_COST_REQUIRED",
        )

    def test_professional_and_discovery_lanes_are_not_product_authority(self) -> None:
        practice = section(self.notion, "### 12.3", "### 12.4")
        self.assert_terms(
            practice,
            "notion.vip/insights/streamline-project-management-with-notion",
            "thomasjfrank.com/docs/ultimate-tasks/databases/",
            "PROFESSIONAL_PRACTICE",
            "DISCOVERY_FEED",
            "AUTHORITY_TARGET",
            "arxiv.org/abs/2202.06183",
            "인디/솔로",
        )

    def test_practice_review_records_context_and_preserves_no_change(self) -> None:
        self.assert_terms(
            self.notion,
            "published_or_updated_at",
            "commercial_interest",
            "counterevidence",
            "actual_consumer",
            "ADOPT / ADAPT / TEST / AVOID / REFERENCE_ONLY",
            "NO_CHANGE",
            "문서 길이만으로",
        )

    def test_automatic_skill_use_has_eligibility_and_current_source(self) -> None:
        self.assert_terms(
            self.notion,
            "SKILL_AUTO_USE_REQUIRES_DATABASE_DESCRIPTION",
            "skills database",
            "description",
            "Use automatically",
            "create-and-manage-skills",
        )

    def test_skill_export_does_not_authorize_execution_or_claim_parity(self) -> None:
        self.assert_terms(
            self.notion,
            "NOTION_SKILL_EXPORT_IS_TRANSPORT_NOT_EQUIVALENCE",
            "SKILL.md",
            "scripts",
            "대표 입력",
            "실행하지 않는다",
        )

    def test_seed_registration_is_not_scheduler_or_scan_evidence(self) -> None:
        self.assert_terms(self.seeds, "scheduler_authority: EXTERNAL_TO_BASE")
        self.assert_terms(
            self.notion,
            "실제로 읽은",
            "last_successful_scan_at",
            "예약 실행",
            "NOT_RUN",
        )

    def test_export_surface_and_account_rollout_are_distinct(self) -> None:
        backup = section(self.migration, "## 2.", "## 3.")
        self.assert_terms(
            backup,
            "2026-08-31",
            "HTML",
            "Markdown",
            "CSV",
            "개별 페이지 PDF",
            "back-up-your-data",
            "계정별",
            "완전 복원",
        )

    def test_unknown_inventory_cannot_be_retired_as_zero(self) -> None:
        counters = section(self.migration, "## 10.", "## 11.")
        self.assert_terms(
            counters,
            "INCOMPLETE_INVENTORY_IS_NOT_ZERO",
            "UNKNOWN",
            "inventory_complete == true",
            "LEGACY_READ_ONLY",
        )

    def test_receipt_exposes_export_coverage_not_only_blank_counters(self) -> None:
        receipt = self.migration.split("## 12. 완료 receipt", 1)[1]
        self.assert_terms(
            receipt,
            "inventory_complete:",
            "export_coverage_status:",
            "unreadable_scope:",
            "archive_sha256:",
            "missing_attachment_count:",
        )


if __name__ == "__main__":
    unittest.main()
