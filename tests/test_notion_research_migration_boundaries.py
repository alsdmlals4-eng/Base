"""Notion research guidance and the real periodic-analysis schema boundary.

These are document/schema regressions, not a live Notion scan, paid API call,
project migration, scheduler execution, or cross-agent runtime evaluation.
"""

from datetime import date
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
SEEDS = ROOT / "docs/knowledge/game-development/PERIODIC_EXTERNAL_SOURCE_DISCOVERY_SEEDS.md"


def section(text: str, heading: str, following: str) -> str:
    """Return a bounded section and fail clearly if its route is missing."""
    _, found, tail = text.partition(heading)
    if not found:
        raise AssertionError(f"Missing section: {heading}")
    body, found, _ = tail.partition(following)
    if not found:
        raise AssertionError(f"Missing following section: {following}")
    return body


class NotionResearchBoundaryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.seeds = SEEDS.read_text(encoding="utf-8")
        cls.notion = section(cls.seeds, "## 12. Notion", "## 13. Game market")

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
            "commercial_or_vendor_interest",
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

    def test_primary_research_has_an_explicit_bounded_authority_role(self) -> None:
        row = next(line for line in self.notion.splitlines() if line.startswith("| Video Game Project Management Anti-patterns"))
        role = row.split("|")[2]
        self.assertIn("`AUTHORITY_TARGET`", role)
        self.assertIn("표본", role)
        self.assertIn("방법", role)

    def projection(self) -> dict[str, object]:
        body = section(self.notion, "### 12.3.1", "### 12.4")
        _, marker, tail = body.partition("```json\n")
        self.assertTrue(marker, "The documented schema projection must be JSON")
        encoded, marker, _ = tail.partition("\n```")
        self.assertTrue(marker, "The schema projection code fence must close")
        projection = json.loads(encoded)
        self.assertIsInstance(projection, dict)
        return projection

    def packet_fixture(self) -> tuple[dict[str, object], str, str, date]:
        # Read the actual documented projection, not a separately mirrored schema.
        projection = self.projection()
        from tools.periodic_source_analysis_contract import CANDIDATE_PROPERTIES

        run_date = date(2026, 8, 31)
        source_id = "fixture-notion-practice"
        url = "https://www.notion.vip/insights/streamline-project-management-with-notion"
        candidate: dict[str, object] = {key: "SCHEMA_TEST_ONLY" for key in CANDIDATE_PROPERTIES}
        candidate.update(
            candidate_id="fixture-candidate",
            source_id=source_id,
            original_url=url,
            published_or_updated_at="UNKNOWN",
            checked_at=run_date.isoformat(),
            source_role="PROFESSIONAL_PRACTICE",
            evidence_tier="T6_AI_INFERENCE",
            evidence_status="UNVERIFIED",
            context_conditions=["Fixture; no source scan occurred"],
            counterevidence=["No operational effect was measured"],
            base_overlap="PARTIAL",
            disposition="TEST",
            work_disposition="NO_CHANGE",
        )
        candidate.update(projection)
        packet = {
            "run_date": run_date.isoformat(),
            "scanned_sources": [source_id],
            "candidates": [candidate],
            "new_source_candidates": [],
            "no_change_reason": "Schema fixture only; no source-state write",
        }
        return packet, url, source_id, run_date

    def test_documented_projection_passes_real_analysis_validator(self) -> None:
        packet, url, source_id, run_date = self.packet_fixture()
        from tools.periodic_source_analysis_contract import validate_analysis_packet

        normalized = validate_analysis_packet(packet, {url}, {source_id}, run_date)
        row = normalized["candidates"][0]
        projection = self.projection()
        for key, value in projection.items():
            with self.subTest(field=key):
                self.assertEqual(value, row[key])
        self.assertNotIn("commercial_interest", row)
        self.assertNotIn("actual_consumer", row)
        self.assertTrue(any(value.startswith("actual_consumer:") for value in row["context_conditions"]))

    def test_real_analysis_validator_rejects_undeclared_top_level_aliases(self) -> None:
        # The first read also makes the pre-correction failure about missing routing.
        self.projection()
        from tools.periodic_source_analysis_contract import AnalysisBlocked, validate_analysis_packet

        for alias in ("commercial_interest", "actual_consumer"):
            with self.subTest(alias=alias):
                packet, url, source_id, run_date = self.packet_fixture()
                packet["candidates"][0][alias] = "unapproved schema expansion"
                with self.assertRaises(AnalysisBlocked) as caught:
                    validate_analysis_packet(packet, {url}, {source_id}, run_date)
                self.assertEqual("BLOCKED_CONTEXT_SCHEMA", caught.exception.code)


if __name__ == "__main__":
    unittest.main()
