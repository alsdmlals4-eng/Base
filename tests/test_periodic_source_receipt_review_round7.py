from __future__ import annotations

import unittest

from tools.periodic_source_analysis_contract import AnalysisBlocked
from tests.test_periodic_source_receipt_state import (
    BATCH_DATE,
    entry,
    ledger,
    material_receipt,
    reconcile,
)


class PeriodicSourceReceiptReviewRound7Tests(unittest.TestCase):
    def test_persisted_contribution_source_must_be_scanned_by_linking_receipt(self) -> None:
        value = material_receipt(
            scanned_source_ids=["anthropic"],
            scanned_discovery_seed_ids=[],
        )
        current = reconcile(ledger(), [entry(value, ref="linked")])
        identity = current["receipt_reconciliation_state"]
        old_key = identity["processed_receipts"][0]["contribution_keys"][0]
        merge_sha = old_key.split(":", 1)[1]
        new_key = f"godot:{merge_sha}"
        identity["processed_receipts"][0]["contribution_keys"] = [new_key]
        identity["processed_contributions"][0]["source_id"] = "godot"
        for row in current["sources"]:
            row["last_base_contribution_at"] = None
            row["last_base_contribution_ref"] = None
            row["base_contribution_count_since_tracking_start"] = 0

        with self.assertRaisesRegex(
            AnalysisBlocked,
            "contribution Source.*linking receipt.*scanned_source_ids",
        ):
            reconcile(current, [])

    def test_persisted_receipt_scan_date_cannot_predate_tracking_start(self) -> None:
        current = reconcile(ledger(), [])
        current["receipt_reconciliation_state"]["processed_receipts"].append(
            {
                "receipt_ref": "issue-334-comment-999",
                "payload_sha256": "f" * 64,
                "scan_date": "2026-08-10",
                "scanned_source_ids": ["anthropic"],
                "material_candidate_count_by_source": {},
                "contribution_keys": [],
            }
        )

        with self.assertRaisesRegex(
            AnalysisBlocked,
            "processed receipt scan_date predates operations Ledger tracking start",
        ):
            reconcile(current, [])

    def test_initial_tracking_start_cannot_follow_batch_date(self) -> None:
        current = ledger()
        current["tracking_started_at"] = "2026-09-03"

        with self.assertRaisesRegex(
            AnalysisBlocked,
            "tracking_started_at cannot be after batch_date",
        ):
            reconcile(current, [])

    def test_persisted_contribution_metadata_is_revalidated(self) -> None:
        current = reconcile(
            ledger(),
            [entry(material_receipt(), ref="invalid-persisted-metadata")],
        )
        current["receipt_reconciliation_state"]["processed_contributions"][0][
            "pr"
        ] = -99

        with self.assertRaisesRegex(
            AnalysisBlocked,
            "processed contribution pr must be a positive pull request number",
        ):
            reconcile(current, [])


if __name__ == "__main__":
    unittest.main()
