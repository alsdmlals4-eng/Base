from __future__ import annotations

import unittest
from datetime import date, timedelta
from pathlib import Path

from tools.periodic_source_scan_queue import select_due_sources


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "periodic-source-scan-queue.yml"


def source(source_id: str) -> dict[str, object]:
    return {
        "source_id": source_id,
        "name": source_id,
        "domains": ["GAME_DEVELOPMENT"],
        "roles": ["AUTHORITY_TARGET"],
        "recommended_cadence": "daily-or-weekly",
        "scan_surfaces": ["recent articles"],
        "last_successful_scan_at": None,
        "last_material_candidate_at": None,
        "last_base_contribution_at": None,
        "last_base_contribution_ref": None,
        "material_candidate_count_since_tracking_start": 0,
        "base_contribution_count_since_tracking_start": 0,
        "status": "ACTIVE",
    }


def operations_payload(ids: list[str]) -> dict[str, object]:
    return {
        "schema_version": 1,
        "ledger_role": "periodic-source-operational-state",
        "tracking_started_at": "2026-08-11",
        "watchlist_owner": "docs/knowledge/game-development/PERIODIC_EXTERNAL_SOURCE_WATCHLIST.md",
        "state_semantics": "fixture",
        "sources": [source(source_id) for source_id in ids],
    }


class PeriodicSourceAnalysisRunnerTests(unittest.TestCase):
    def test_daily_due_order_rotates_across_equal_priority_sources(self) -> None:
        payload = operations_payload([f"source-{index}" for index in range(6)])
        first = [row["source_id"] for row in select_due_sources(payload, date(2026, 8, 14))[:2]]
        second = [
            row["source_id"]
            for row in select_due_sources(payload, date(2026, 8, 14) + timedelta(days=1))[:2]
        ]
        self.assertNotEqual(first, second)
        self.assertEqual(2, len(first))
        self.assertEqual(2, len(second))

    def test_workflow_suppresses_successful_no_material_repository_churn(self) -> None:
        workflow = WORKFLOW.read_text(encoding="utf-8")
        for required in (
            "Suppress successful no-material repository churn",
            'status.get("state") != "READY_FOR_PR"',
            'record.get("retained_candidate_ids", [])',
            'analysis.get("new_source_candidates", [])',
            'status["state"] = "NO_CHANGE"',
            'status["generated_paths"] = []',
            "No material candidate survived the Evidence gate.",
        ):
            self.assertIn(required, workflow)
        self.assertLess(
            workflow.index("Suppress successful no-material repository churn"),
            workflow.index("Create, validate, and auto-merge the bounded evidence PR"),
        )


if __name__ == "__main__":
    unittest.main()
