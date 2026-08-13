from __future__ import annotations

import json
import tempfile
import unittest
from datetime import date, timedelta
from pathlib import Path

from tools.periodic_source_analysis import run_analysis, select_analysis_batch


ARTICLE_URL = "https://example.com/current-source-note"


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


def response_text(text: str) -> dict[str, object]:
    return {
        "output": [{
            "type": "message",
            "content": [{"type": "output_text", "text": text}],
        }]
    }


class PeriodicSourceAnalysisRunnerTests(unittest.TestCase):
    def test_daily_batch_rotates_across_an_unchanged_due_set(self) -> None:
        rows = [source(f"source-{index}") for index in range(6)]
        first = [row["source_id"] for row in select_analysis_batch(rows, date(2026, 8, 14), 2)]
        second = [
            row["source_id"]
            for row in select_analysis_batch(rows, date(2026, 8, 14) + timedelta(days=1), 2)
        ]
        self.assertNotEqual(first, second)
        self.assertEqual(2, len(first))
        self.assertEqual(2, len(second))
        self.assertTrue(set(first + second).issubset({row["source_id"] for row in rows}))

    def test_successful_no_change_run_writes_status_only_not_daily_repository_churn(self) -> None:
        run_date = date(2026, 8, 14)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            operations = root / "operations.json"
            candidates = root / "candidates.json"
            output = root / "source-scans"
            operations.write_text(
                json.dumps(operations_payload(["godot"]), ensure_ascii=False),
                encoding="utf-8",
            )
            candidates.write_text(
                json.dumps({
                    "schema_version": 1,
                    "ledger_role": "periodic-unverified-source-candidates",
                    "authority": "UNVERIFIED_DISCOVERY_ONLY",
                    "candidates": [],
                }),
                encoding="utf-8",
            )
            original_operations = operations.read_bytes()
            original_candidates = candidates.read_bytes()
            calls = 0

            def transport(payload: dict[str, object], api_key: str) -> dict[str, object]:
                nonlocal calls
                self.assertEqual("test-key", api_key)
                calls += 1
                if calls == 1:
                    return {
                        "output": [
                            {"type": "web_search_call", "action": {
                                "sources": [{"url": ARTICLE_URL}]
                            }},
                            {"type": "message", "content": [{
                                "type": "output_text",
                                "text": "The approved Source was checked and produced no material decision delta.",
                                "annotations": [{"type": "url_citation", "url": ARTICLE_URL}],
                            }]},
                        ]
                    }
                if calls == 2:
                    return response_text(json.dumps({
                        "run_date": run_date.isoformat(),
                        "scanned_sources": ["godot"],
                        "candidates": [],
                        "new_source_candidates": [],
                        "no_change_reason": "No material candidate survived the Evidence relevance filter.",
                    }))
                return response_text(json.dumps({
                    "run_date": run_date.isoformat(),
                    "findings": [],
                    "approved_candidate_ids": [],
                    "blocked_candidate_ids": [],
                    "url_verification_passed": True,
                    "claim_ceiling_passed": True,
                    "protected_semantic_change": False,
                    "result": "AUTO_MERGE_ELIGIBLE",
                }))

            result = run_analysis(
                operations_ledger_path=operations,
                candidate_ledger_path=candidates,
                output_root=output,
                run_date=run_date,
                run_id="runner-test",
                model="gpt-5.6-terra",
                batch_size=1,
                api_key="test-key",
                transport=transport,
            )

            self.assertEqual("NO_CHANGE", result["state"])
            self.assertEqual(["godot"], result["selected_source_ids"])
            self.assertEqual(["godot"], result["scanned_source_ids"])
            self.assertEqual(original_operations, operations.read_bytes())
            self.assertEqual(original_candidates, candidates.read_bytes())
            self.assertFalse(output.exists())
            self.assertEqual(3, calls)


if __name__ == "__main__":
    unittest.main()
