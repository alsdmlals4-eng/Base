from __future__ import annotations

import copy
import unittest
from datetime import date

from tools import periodic_source_receipt_state as state
from tools.periodic_source_analysis_contract import AnalysisBlocked
from tools.periodic_source_operations_state import update_operations_ledger
from tests.test_periodic_source_receipt_state import (
    BATCH_DATE,
    DISCOVERY_SEEDS,
    entry,
    ledger,
    material_receipt,
    receipt,
    reconcile,
)


class PeriodicSourceReceiptReviewRound4Tests(unittest.TestCase):
    def test_grouped_active_discovery_seed_records_are_all_parsed(self) -> None:
        registry = """
```yaml
seed_id: openai-codex-official
name: OpenAI Codex
status: ACTIVE_DISCOVERY_SEED
url: https://developers.openai.com/

seed_id: anthropic-claude-code-official
name: Claude Code
status: ACTIVE_DISCOVERY_SEED
url: https://docs.anthropic.com/

seed_id: google-gemini-coding-official
name: Gemini
status: ACTIVE_DISCOVERY_SEED
url: https://geminicli.com/docs/
```
"""
        self.assertEqual(
            {
                "openai-codex-official",
                "anthropic-claude-code-official",
                "google-gemini-coding-official",
            },
            state.parse_active_discovery_seed_ids(registry),
        )

    def test_receipt_source_and_discovery_lanes_must_be_disjoint(self) -> None:
        current = ledger()
        current["sources"].append(
            {
                **copy.deepcopy(current["sources"][0]),
                "source_id": "promoted-seed",
                "name": "promoted-seed",
            }
        )
        overlap = receipt(
            scanned_source_ids=["promoted-seed"],
            scanned_discovery_seed_ids=["promoted-seed"],
            retained_candidate_source_ids=[],
            material_candidate_count_by_source={},
            high_nutrient_sources=[],
        )
        with self.assertRaisesRegex(AnalysisBlocked, "both scanned Source lanes"):
            state.validate_actual_source_review_receipt(
                overlap,
                current,
                known_discovery_seed_ids=DISCOVERY_SEEDS | {"promoted-seed"},
                batch_date=BATCH_DATE,
            )

    def test_receipt_entry_envelope_rejects_unknown_keys(self) -> None:
        row = entry(ref="typo")
        row["source_state_at_scna"] = {"anthropic": "DURABLE_ACTIVE"}
        with self.assertRaisesRegex(AnalysisBlocked, "unsupported receipt entry fields"):
            reconcile(ledger(), [row])

    def test_receipt_identity_includes_receipt_time_classification(self) -> None:
        first = entry(receipt(), ref="first")
        first["source_state_at_scan"] = {
            "anthropic": "DURABLE_ACTIVE",
            "godot": "DURABLE_ACTIVE",
            "github-copilot": "DURABLE_ACTIVE",
        }
        once = reconcile(ledger(), [first])

        contradictory = entry(receipt(), ref="contradictory")
        contradictory["source_state_at_scan"] = {
            "anthropic": "DISCOVERY_ACTIVE"
        }
        with self.assertRaisesRegex(AnalysisBlocked, "classification.*durable lane"):
            reconcile(once, [contradictory])

    def test_redundant_explicit_current_classification_does_not_duplicate_event(self) -> None:
        implicit = entry(receipt(), ref="implicit")
        explicit = entry(
            receipt(),
            ref="explicit",
            source_state_at_scan={
                "anthropic": "DURABLE_ACTIVE",
                "godot": "DURABLE_ACTIVE",
                "github-copilot": "DURABLE_ACTIVE",
            },
        )

        result = reconcile(ledger(), [implicit, explicit])
        anthropic = result["sources"][0]
        processed = result["receipt_reconciliation_state"]["processed_receipts"]

        self.assertEqual(1, anthropic["material_candidate_count_since_tracking_start"])
        self.assertEqual(2, len(processed))
        self.assertEqual(1, len({row["payload_sha256"] for row in processed}))

    def test_redundant_merge_date_map_does_not_duplicate_material_event(self) -> None:
        direct = entry(material_receipt(), ref="direct")
        mapped = entry(
            material_receipt(),
            ref="mapped",
            contribution_merge_dates={"2" * 40: "2026-09-01"},
        )

        result = reconcile(ledger(), [direct, mapped])
        anthropic = result["sources"][0]
        processed = result["receipt_reconciliation_state"]["processed_receipts"]

        self.assertEqual(1, anthropic["material_candidate_count_since_tracking_start"])
        self.assertEqual(1, anthropic["base_contribution_count_since_tracking_start"])
        self.assertEqual(2, len(processed))
        self.assertEqual(1, len({row["payload_sha256"] for row in processed}))

    def test_shared_analysis_updater_rejects_identity_enabled_ledger(self) -> None:
        current = reconcile(ledger(), [])
        with self.assertRaisesRegex(AnalysisBlocked, "receipt reconciler"):
            update_operations_ledger(
                current,
                {"anthropic"},
                [{"source_id": "anthropic"}],
                date(2026, 9, 3),
            )

    def test_tracking_start_is_frozen_when_reconciliation_begins(self) -> None:
        current = reconcile(ledger(), [])
        current["tracking_started_at"] = "2026-08-12"
        with self.assertRaisesRegex(AnalysisBlocked, "tracking_started_at changed"):
            reconcile(current, [])

    def test_baselined_source_id_cannot_disappear_without_identity_migration(self) -> None:
        current = reconcile(ledger(), [])
        current["sources"] = [
            row for row in current["sources"] if row["source_id"] != "anthropic"
        ]
        with self.assertRaisesRegex(AnalysisBlocked, "baselined Source ID disappeared"):
            reconcile(current, [])


if __name__ == "__main__":
    unittest.main()
