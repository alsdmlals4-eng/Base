from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from tools.periodic_source_analysis import run_analysis
from tools.periodic_source_analysis_contract import AnalysisBlocked
from tests.test_periodic_source_receipt_state import (
    BATCH_DATE,
    entry,
    ledger,
    receipt,
    reconcile,
)


class PeriodicSourceReceiptReviewRound6Tests(unittest.TestCase):
    def test_new_and_persisted_baselines_are_bounded_by_tracking_and_batch_dates(self) -> None:
        future = ledger()
        future["sources"][0]["last_successful_scan_at"] = "2099-01-01"
        with self.assertRaisesRegex(
            AnalysisBlocked, "baseline scan date.*tracking.*batch"
        ):
            reconcile(future, [])

        pretracking = ledger()
        pretracking["sources"][0]["last_material_candidate_at"] = "2026-08-10"
        pretracking["sources"][0][
            "material_candidate_count_since_tracking_start"
        ] = 1
        with self.assertRaisesRegex(
            AnalysisBlocked, "baseline material date.*tracking.*batch"
        ):
            reconcile(pretracking, [])

        persisted = reconcile(ledger(), [])
        persisted["receipt_reconciliation_state"]["source_baselines"][0][
            "base_contribution_count"
        ] = 1
        persisted["receipt_reconciliation_state"]["source_baselines"][0][
            "base_contribution_date"
        ] = "2099-01-01"
        persisted["receipt_reconciliation_state"]["source_baselines"][0][
            "base_contribution_ref"
        ] = "a" * 40
        with self.assertRaisesRegex(
            AnalysisBlocked, "baseline Base contribution date.*tracking.*batch"
        ):
            reconcile(persisted, [])

    def test_processed_material_count_key_collisions_fail_closed(self) -> None:
        current = reconcile(ledger(), [entry(receipt(), ref="source")])
        current["receipt_reconciliation_state"]["processed_receipts"][0][
            "material_candidate_count_by_source"
        ] = {"anthropic": 1, " anthropic ": 2}

        with self.assertRaisesRegex(
            AnalysisBlocked, "duplicate normalized processed material Source"
        ):
            reconcile(current, [])

    def test_present_null_reconciliation_state_cannot_reinitialize_identity(self) -> None:
        current = ledger()
        current["receipt_reconciliation_state"] = None

        with self.assertRaisesRegex(
            AnalysisBlocked, "receipt reconciliation state cannot be null"
        ):
            reconcile(current, [])

    def test_duplicate_payload_historical_classification_is_order_independent(self) -> None:
        current = ledger()
        current["sources"][0]["status"] = "INACTIVE"
        value = receipt()
        explicit = entry(
            value,
            ref="explicit",
            source_state_at_scan={"anthropic": "DURABLE_ACTIVE"},
        )
        implicit = entry(value, ref="implicit")

        for rows in ([explicit, implicit], [implicit, explicit]):
            with self.subTest(order=[row["receipt_ref"] for row in rows]):
                with self.assertRaisesRegex(
                    AnalysisBlocked,
                    "historical durable Source requires explicit receipt-time classification",
                ):
                    reconcile(current, rows)

    def test_identity_enabled_analysis_blocks_before_any_transport_call(self) -> None:
        calls: list[dict[str, object]] = []

        def transport(payload: dict[str, object], api_key: str) -> dict[str, object]:
            calls.append(payload)
            raise AssertionError("metered transport must not be called")

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            operations_path = root / "operations.json"
            candidate_path = root / "candidates.json"
            output_root = root / "out"
            operations_path.write_text(
                json.dumps(reconcile(ledger(), [])), encoding="utf-8"
            )
            candidate_path.write_text(
                json.dumps(
                    {
                        "schema_version": 1,
                        "ledger_role": "periodic-unverified-source-candidates",
                        "authority": "UNVERIFIED_DISCOVERY_ONLY",
                        "candidates": [],
                    }
                ),
                encoding="utf-8",
            )

            with self.assertRaisesRegex(
                AnalysisBlocked, "identity-enabled Operations Ledger"
            ):
                run_analysis(
                    operations_ledger_path=operations_path,
                    candidate_ledger_path=candidate_path,
                    output_root=output_root,
                    run_date=BATCH_DATE,
                    run_id="round6",
                    model="test-model",
                    batch_size=1,
                    api_key="",
                    transport=transport,
                )

        self.assertEqual([], calls)


if __name__ == "__main__":
    unittest.main()
