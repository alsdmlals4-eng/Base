from __future__ import annotations

import json
import tempfile
import unittest
from datetime import date
from pathlib import Path

from tools.periodic_source_scan_queue import (
    ISSUE_MARKER,
    ISSUE_TITLE,
    load_ledger,
    parse_iso_date,
    render_issue_body,
    select_due_sources,
    source_is_due,
)


ROOT = Path(__file__).resolve().parents[1]
QUEUE_WORKFLOW = ROOT / ".github" / "workflows" / "periodic-source-scan-queue.yml"
EVIDENCE_WORKFLOW = ROOT / ".github" / "workflows" / "validate-evidence-knowledge.yml"
WATCHLIST = ROOT / "docs" / "knowledge" / "game-development" / "PERIODIC_EXTERNAL_SOURCE_WATCHLIST.md"
QUEUE_GUIDE = ROOT / "docs" / "knowledge" / "game-development" / "PERIODIC_SOURCE_SCAN_QUEUE.md"
RADAR = ROOT / "docs" / "knowledge" / "game-development" / "NARRATIVE_WORLD_CHARACTER_SOURCE_RADAR.md"
TUTORIAL = ROOT / "docs" / "knowledge" / "game-development" / "TUTORIAL_AND_ONBOARDING_DESIGN_GUIDE.md"
CHECKPOINT = ROOT / "docs" / "knowledge" / "game-development" / "SOURCE_SCAN_CHECKPOINT_2026-08-14.md"
LEDGER = ROOT / "docs" / "knowledge" / "game-development" / "PERIODIC_SOURCE_OPERATIONS_LEDGER.json"


def source(
    source_id: str,
    cadence: str,
    last_scan: str | None,
    *,
    status: str = "ACTIVE",
) -> dict[str, object]:
    return {
        "source_id": source_id,
        "name": source_id.replace("-", " ").title(),
        "domains": ["FICTION_AND_INTERACTIVE_NARRATIVE"],
        "roles": ["PROFESSIONAL_PRACTICE"],
        "recommended_cadence": cadence,
        "scan_surfaces": ["recent articles", "linked originals"],
        "last_successful_scan_at": last_scan,
        "last_material_candidate_at": None,
        "last_base_contribution_at": None,
        "last_base_contribution_ref": None,
        "material_candidate_count_since_tracking_start": 0,
        "base_contribution_count_since_tracking_start": 0,
        "status": status,
    }


def payload(sources: list[dict[str, object]]) -> dict[str, object]:
    return {
        "schema_version": 1,
        "ledger_role": "periodic-source-operational-state",
        "tracking_started_at": "2026-08-11",
        "watchlist_owner": "docs/knowledge/game-development/PERIODIC_EXTERNAL_SOURCE_WATCHLIST.md",
        "state_semantics": "test fixture",
        "sources": sources,
    }


class PeriodicSourceScanQueueTests(unittest.TestCase):
    def test_date_parser_accepts_null_and_strict_iso_date(self) -> None:
        self.assertIsNone(parse_iso_date(None))
        self.assertEqual(parse_iso_date("2026-08-14"), date(2026, 8, 14))

        for invalid in ("", "2026/08/14", "14-08-2026", 20260814, True):
            with self.subTest(invalid=invalid):
                with self.assertRaises(ValueError):
                    parse_iso_date(invalid)

    def test_due_policy_matches_watchlist_cadences(self) -> None:
        today = date(2026, 8, 14)
        cases = (
            ("daily-or-weekly", "2026-08-07", True),
            ("daily-or-weekly", "2026-08-08", False),
            ("weekly", "2026-08-07", True),
            ("weekly", "2026-08-08", False),
            ("monthly-or-on-demand", "2026-07-15", True),
            ("monthly-or-on-demand", "2026-07-16", False),
            ("quarterly-or-when-relevant", "2026-05-16", True),
            ("quarterly-or-when-relevant", "2026-05-17", False),
        )
        for cadence, last_scan, expected in cases:
            with self.subTest(cadence=cadence, last_scan=last_scan):
                self.assertEqual(
                    source_is_due(source("candidate", cadence, last_scan), today),
                    expected,
                )

    def test_null_scan_is_due_and_inactive_sources_are_excluded(self) -> None:
        today = date(2026, 8, 14)
        ledger = payload(
            [
                source("never-scanned", "weekly", None),
                source("inactive", "weekly", None, status="RETIRED"),
            ]
        )
        selected = select_due_sources(ledger, today)
        self.assertEqual([item["source_id"] for item in selected], ["never-scanned"])

    def test_invalid_cadence_date_and_future_scan_fail_closed(self) -> None:
        today = date(2026, 8, 14)
        for item in (
            source("unknown", "hourly", None),
            source("bad-date", "weekly", "not-a-date"),
            source("future", "weekly", "2026-08-15"),
        ):
            with self.subTest(source_id=item["source_id"]):
                with self.assertRaises(ValueError):
                    source_is_due(item, today)

    def test_load_ledger_requires_schema_unique_ids_and_known_cadence(self) -> None:
        fixtures = (
            ({"schema_version": 2, "sources": []}, "schema_version"),
            (payload([source("duplicate", "weekly", None), source("duplicate", "weekly", None)]), "duplicate"),
            (payload([source("unknown", "hourly", None)]), "cadence"),
        )
        for data, expected_message in fixtures:
            with self.subTest(expected_message=expected_message):
                with tempfile.TemporaryDirectory() as directory:
                    path = Path(directory) / "ledger.json"
                    path.write_text(json.dumps(data), encoding="utf-8")
                    with self.assertRaisesRegex(ValueError, expected_message):
                        load_ledger(path)

    def test_issue_body_is_deterministic_and_preserves_evidence_boundaries(self) -> None:
        today = date(2026, 8, 14)
        ledger = payload(
            [
                source("weekly-source", "weekly", "2026-08-07"),
                source("monthly-source", "monthly-or-on-demand", "2026-07-01"),
                source("fresh-source", "weekly", "2026-08-13"),
            ]
        )
        first = render_issue_body(ledger, today)
        self.assertEqual(first, render_issue_body(ledger, today))
        self.assertTrue(first.startswith(ISSUE_MARKER))
        self.assertEqual(ISSUE_TITLE, "[Periodic Source Scan Queue]")

        for required in (
            "UNVERIFIED_DISCOVERY",
            "2026-08-14",
            "weekly-source",
            "monthly-source",
            "기존 Source의 새 글·수정 글 확인",
            "신규 Source 사이트 탐색",
            "original source backtrace",
            "published_or_updated_at",
            "current_base_owner",
            "current_project_consumer",
            "claim ceiling",
            "validation artifact",
            "rollback_or_discard_condition",
            "ADOPT | ADAPT | TEST | PROJECT_ONLY | REFERENCE_ONLY | AVOID",
            "Queue 완료 != Ledger scan 완료",
        ):
            self.assertIn(required, first)
        self.assertNotIn("fresh-source", first)

    def test_scheduled_workflow_is_minimum_permission_issue_queue(self) -> None:
        self.assertTrue(QUEUE_WORKFLOW.is_file())
        workflow = QUEUE_WORKFLOW.read_text(encoding="utf-8")
        for required in (
            'cron: "17 10 * * 1"',
            'timezone: "Asia/Seoul"',
            "workflow_dispatch:",
            "contents: read",
            "issues: write",
            "tools/periodic_source_scan_queue.py",
            "PERIODIC_SOURCE_OPERATIONS_LEDGER.json",
            "periodic-source-scan-queue.md",
            "actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1",
            "actions/setup-python@5fda3b95a4ea91299a34e894583c3862153e4b97",
            "actions/upload-artifact@043fb46d1a93c77aae656e7c1c64a875d1fc6a0a",
        ):
            self.assertIn(required, workflow)
        self.assertNotIn("contents: write", workflow)
        self.assertNotIn("pull_request_target", workflow)

    def test_first_scan_sources_and_minimal_absorptions_are_connected(self) -> None:
        self.assertTrue(CHECKPOINT.is_file())
        radar = RADAR.read_text(encoding="utf-8")
        tutorial = TUTORIAL.read_text(encoding="utf-8")
        checkpoint = CHECKPOINT.read_text(encoding="utf-8")
        queue_guide = QUEUE_GUIDE.read_text(encoding="utf-8")

        for source_name in (
            "DiGRA Digital Library",
            "Game Studies",
            "MCLC Resource Center",
            "Library of Congress Web Cultures Web Archive",
            "Data & Society",
        ):
            self.assertIn(source_name, radar)
            self.assertIn(source_name, checkpoint)

        for required in (
            "story_holon_local_coherence",
            "shared_storyworld_contribution",
            "fragment_inference_burden",
            "optional_fragment_redundancy_and_recovery",
            "wuxia_xianxia_cultivation_boundary",
            "cosmology_and_technical_practice",
            "translation_and_cross_cultural_boundary",
            "platform_commercialization_and_governance_stage",
            "native_symbol_system_and_recontextualization",
        ):
            self.assertIn(required, radar)

        for required in (
            "prior_game_expertise",
            "expertise_measure",
            "novice_expert_segment",
            "expertise_by_onboarding_interaction",
        ):
            self.assertIn(required, tutorial)

        for required in (
            "UNVERIFIED_DISCOVERY",
            "Queue 완료 != scan 완료",
            "새 글·수정 글",
            "신규 Source 사이트",
            "Issue 갱신 != Ledger timestamp 갱신",
            "기존 owner",
            "자동 Canon",
            "자동 PR",
        ):
            self.assertIn(required, queue_guide)

    def test_evidence_workflow_executes_and_archives_queue_contract(self) -> None:
        workflow = EVIDENCE_WORKFLOW.read_text(encoding="utf-8")
        for required in (
            '"tools/periodic_source_scan_queue.py"',
            '"tests/test_periodic_source_scan_queue.py"',
            '".github/workflows/periodic-source-scan-queue.yml"',
            "tools/periodic_source_scan_queue.py",
            "tests/test_periodic_source_scan_queue.py",
            "docs/knowledge/game-development/SOURCE_SCAN_CHECKPOINT_2026-08-14.md",
            "docs/knowledge/game-development/PERIODIC_SOURCE_SCAN_QUEUE.md",
        ):
            self.assertIn(required, workflow)

    def test_repository_ledger_remains_the_only_operational_state(self) -> None:
        self.assertTrue(LEDGER.is_file())
        watchlist = WATCHLIST.read_text(encoding="utf-8")
        queue_workflow = QUEUE_WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("고유 Source family 하나로 추적", watchlist)
        self.assertIn("PERIODIC_SOURCE_OPERATIONS_LEDGER.json", watchlist)
        self.assertIn("PERIODIC_SOURCE_OPERATIONS_LEDGER.json", queue_workflow)
        self.assertNotIn("last_successful_scan_at", queue_workflow)


if __name__ == "__main__":
    unittest.main()
