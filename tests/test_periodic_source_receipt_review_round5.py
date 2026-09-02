from __future__ import annotations

import copy
import os
import stat
import tempfile
import unittest
from pathlib import Path

from tools import periodic_source_receipt_state as state
from tools.periodic_source_analysis_contract import AnalysisBlocked
from tools.record_periodic_source_scan import record
from tests.test_periodic_source_receipt_state import (
    BATCH_DATE,
    DISCOVERY_SEEDS,
    entry,
    ledger,
    material_receipt,
    receipt,
    reconcile,
)


class PeriodicSourceReceiptReviewRound5Tests(unittest.TestCase):
    def test_processed_contribution_links_are_bidirectional(self) -> None:
        orphan = reconcile(ledger(), [])
        orphan["receipt_reconciliation_state"]["processed_contributions"].append(
            {
                "source_id": "anthropic",
                "pr": 649,
                "merge_sha": "2" * 40,
                "merge_date": "2026-09-01",
            }
        )

        with self.assertRaisesRegex(
            AnalysisBlocked, "processed contribution.*processed receipt"
        ):
            reconcile(orphan, [])

        missing = reconcile(
            ledger(), [entry(material_receipt(), ref="linked")]
        )
        missing["receipt_reconciliation_state"]["processed_contributions"] = []
        with self.assertRaisesRegex(
            AnalysisBlocked, "processed receipt.*contribution metadata"
        ):
            reconcile(missing, [])

    def test_persisted_event_dates_cannot_exceed_previous_batch(self) -> None:
        receipt_state = reconcile(ledger(), [])
        receipt_state["receipt_reconciliation_state"]["processed_receipts"].append(
            {
                "receipt_ref": "future-receipt",
                "payload_sha256": "1" * 64,
                "scan_date": "2026-09-03",
                "scanned_source_ids": ["anthropic"],
                "material_candidate_count_by_source": {},
                "contribution_keys": [],
            }
        )
        with self.assertRaisesRegex(
            AnalysisBlocked, "processed receipt scan_date.*last_batch_date"
        ):
            reconcile(receipt_state, [])

        contribution_state = reconcile(ledger(), [])
        contribution_key = f"anthropic:{'3' * 40}"
        contribution_state["receipt_reconciliation_state"]["processed_receipts"].append(
            {
                "receipt_ref": "future-contribution-receipt",
                "payload_sha256": "2" * 64,
                "scan_date": "2026-09-02",
                "scanned_source_ids": ["anthropic"],
                "material_candidate_count_by_source": {},
                "contribution_keys": [contribution_key],
            }
        )
        contribution_state["receipt_reconciliation_state"][
            "processed_contributions"
        ].append(
            {
                "source_id": "anthropic",
                "pr": 650,
                "merge_sha": "3" * 40,
                "merge_date": "2026-09-03",
            }
        )
        with self.assertRaisesRegex(
            AnalysisBlocked,
            "processed contribution merge_date.*last_batch_date",
        ):
            reconcile(contribution_state, [])

    def test_normalized_classification_key_collision_is_rejected(self) -> None:
        with self.assertRaisesRegex(
            AnalysisBlocked, "duplicate normalized source_state_at_scan.*ID"
        ):
            state.validate_actual_source_review_receipt(
                receipt(),
                ledger(),
                known_discovery_seed_ids=DISCOVERY_SEEDS,
                source_state_at_scan={
                    " anthropic ": "DISCOVERY_ACTIVE",
                    "anthropic": "DURABLE_ACTIVE",
                },
                batch_date=BATCH_DATE,
            )

    def test_loose_discovery_seed_records_respect_status(self) -> None:
        text = """
seed_id: retired-seed
status: RETIRED
seed_id: active-seed
status: ACTIVE_DISCOVERY_SEED
"""
        self.assertEqual(
            {"active-seed"}, state.parse_active_discovery_seed_ids(text)
        )

    def test_same_day_contributions_require_trusted_chronological_order(self) -> None:
        first = material_receipt(sha="2" * 40)
        second = material_receipt(sha="3" * 40)
        second["start_main"] = "2" * 40
        second["pr_created"] = 650
        second["merged_base_contribution_refs"][0]["pr"] = 650

        with self.assertRaisesRegex(
            AnalysisBlocked, "same-day contribution.*chronological evidence"
        ):
            reconcile(
                ledger(),
                [entry(first, ref="first"), entry(second, ref="second")],
            )

    @unittest.skipIf(os.name == "nt", "POSIX mode preservation")
    def test_atomic_ledger_replacement_preserves_existing_mode(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "ledger.json"
            path.write_text(
                __import__("json").dumps(ledger()), encoding="utf-8"
            )
            path.chmod(0o644)

            record(path, "2026-08-22", ["anthropic"], [])

            self.assertEqual(0o644, stat.S_IMODE(path.stat().st_mode))

    def test_duplicate_normalized_high_nutrient_rows_are_rejected(self) -> None:
        row = {
            "source": "https://example.com/source",
            "nutrient_score": 10,
            "source_archetype": "TOOL_WITH_SOURCE",
            "reusable_units": ["B", "A"],
        }
        duplicate = copy.deepcopy(row)
        duplicate["reusable_units"] = ["A", "B"]
        value = receipt(high_nutrient_sources=[row, duplicate])

        with self.assertRaisesRegex(
            AnalysisBlocked, "duplicate high-nutrient source row"
        ):
            state.validate_actual_source_review_receipt(
                value,
                ledger(),
                known_discovery_seed_ids=DISCOVERY_SEEDS,
                batch_date=BATCH_DATE,
            )

    def test_contribution_source_ids_are_matched_exactly(self) -> None:
        current = ledger()
        foo = copy.deepcopy(current["sources"][0])
        foo["source_id"] = "foo"
        foo_bar = copy.deepcopy(current["sources"][0])
        foo_bar["source_id"] = "foo:bar"
        current["sources"] = [foo, foo_bar]

        value = material_receipt(sha="4" * 40)
        value["scanned_source_ids"] = ["foo:bar"]
        value["retained_candidate_source_ids"] = ["foo:bar"]
        value["material_candidate_count_by_source"] = {"foo:bar": 1}
        value["merged_base_contribution_refs"][0]["source_id"] = "foo:bar"

        result = state.reconcile_operations_ledger_from_receipts(
            current,
            [entry(value, ref="nested-source")],
            known_discovery_seed_ids=DISCOVERY_SEEDS,
            batch_date=BATCH_DATE,
        )
        rows = {row["source_id"]: row for row in result["sources"]}
        self.assertEqual(0, rows["foo"]["base_contribution_count_since_tracking_start"])
        self.assertEqual(
            1, rows["foo:bar"]["base_contribution_count_since_tracking_start"]
        )

    def test_pretracking_contribution_is_rejected(self) -> None:
        value = material_receipt(sha="5" * 40)
        value["merged_base_contribution_refs"][0]["merge_date"] = "2026-08-10"

        with self.assertRaisesRegex(
            AnalysisBlocked, "contribution.*predates operations Ledger tracking start"
        ):
            reconcile(ledger(), [entry(value, ref="pretracking")])


if __name__ == "__main__":
    unittest.main()
