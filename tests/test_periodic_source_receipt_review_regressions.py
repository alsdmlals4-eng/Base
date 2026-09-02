from __future__ import annotations

import copy
import unittest
from datetime import date

from tools import periodic_source_receipt_state as state
from tools.periodic_source_analysis_contract import AnalysisBlocked


BATCH_DATE = date(2026, 9, 2)
DISCOVERY_SEEDS = {"github-repositories-discovery"}


def source(source_id: str) -> dict[str, object]:
    return {
        "source_id": source_id,
        "name": source_id,
        "domains": ["GAME_DEVELOPMENT"],
        "roles": ["AUTHORITY_TARGET"],
        "recommended_cadence": "daily-or-weekly",
        "scan_surfaces": ["official surface"],
        "last_successful_scan_at": None,
        "last_material_candidate_at": None,
        "last_base_contribution_at": None,
        "last_base_contribution_ref": None,
        "material_candidate_count_since_tracking_start": 0,
        "base_contribution_count_since_tracking_start": 0,
        "status": "ACTIVE",
    }


def ledger() -> dict[str, object]:
    return {
        "schema_version": 1,
        "ledger_role": "periodic-source-operational-state",
        "tracking_started_at": "2026-08-11",
        "watchlist_owner": "docs/knowledge/game-development/PERIODIC_EXTERNAL_SOURCE_WATCHLIST.md",
        "state_semantics": "fixture",
        "sources": [source("anthropic"), source("godot"), source("github-copilot")],
    }


def receipt(**overrides: object) -> dict[str, object]:
    value: dict[str, object] = {
        "scan_date": "2026-09-01",
        "start_main": "1" * 40,
        "final_main": "1" * 40,
        "disposition": "NO_CHANGE",
        "high_nutrient_sources": [
            {
                "source": "https://www.anthropic.com/news/example",
                "nutrient_score": 11,
                "source_archetype": "FAILURE_POSTMORTEM",
                "reusable_units": ["UNIT_B", "UNIT_A"],
            }
        ],
        "scanned_source_ids": ["anthropic", "godot", "github-copilot"],
        "scanned_discovery_seed_ids": ["github-repositories-discovery"],
        "retained_candidate_source_ids": ["anthropic"],
        "material_candidate_count_by_source": {"anthropic": 1},
        "merged_base_contribution_refs": [],
        "repository_change": "NONE",
        "pr_created": None,
        "merge_sha": None,
        "ledger_write": "DEFER_TO_WEEKLY_SCAN_STATE_BATCH",
        "unverified_scope": ["scope-b", "scope-a"],
    }
    value.update(overrides)
    return value


def reconcile(
    current: dict[str, object], entries: list[dict[str, object]]
) -> dict[str, object]:
    return state.reconcile_operations_ledger_from_receipts(
        current,
        entries,
        known_discovery_seed_ids=DISCOVERY_SEEDS,
        batch_date=BATCH_DATE,
    )


class PeriodicSourceReceiptReviewRegressionTests(unittest.TestCase):
    def test_new_same_day_receipt_is_counted_once_after_identity_state_exists(self) -> None:
        first = {
            "receipt_ref": "issue-334-comment-1",
            "actual_source_review_receipt": receipt(),
        }
        once = reconcile(ledger(), [first])
        second = {
            "receipt_ref": "issue-334-comment-2",
            "actual_source_review_receipt": receipt(start_main="2" * 40),
        }
        twice = reconcile(once, [second])
        repeated = reconcile(twice, [second])
        row = twice["sources"][0]
        self.assertEqual(2, row["material_candidate_count_since_tracking_start"])
        self.assertEqual(twice, repeated)
        reconciliation = twice["receipt_reconciliation_state"]
        self.assertEqual(2, len(reconciliation["processed_receipts"]))

    def test_initial_same_day_material_event_without_identity_state_fails_closed(self) -> None:
        current = ledger()
        row = current["sources"][0]
        row["last_material_candidate_at"] = "2026-09-01"
        row["material_candidate_count_since_tracking_start"] = 5
        with self.assertRaisesRegex(AnalysisBlocked, "ambiguous same-day material"):
            reconcile(
                current,
                [{"receipt_ref": "late", "actual_source_review_receipt": receipt()}],
            )

    def test_unregistered_discovery_seed_is_rejected(self) -> None:
        bad = receipt(
            scanned_discovery_seed_ids=["github-repositories-discoveri"],
        )
        with self.assertRaisesRegex(AnalysisBlocked, "unknown discovery seed ID"):
            state.validate_actual_source_review_receipt(
                bad,
                ledger(),
                known_discovery_seed_ids=DISCOVERY_SEEDS,
                batch_date=BATCH_DATE,
            )

    def test_conflicting_contribution_source_aliases_are_rejected(self) -> None:
        bad = receipt(
            disposition="MATERIAL_CHANGE",
            repository_change="2_FILES",
            pr_created=649,
            merge_sha="2" * 40,
            merged_base_contribution_refs=[
                {
                    "source_id": "anthropic",
                    "source": "godot",
                    "pr": 649,
                    "merge_sha": "2" * 40,
                }
            ],
        )
        with self.assertRaisesRegex(AnalysisBlocked, "conflicting contribution Source aliases"):
            state.validate_actual_source_review_receipt(
                bad,
                ledger(),
                known_discovery_seed_ids=DISCOVERY_SEEDS,
                batch_date=BATCH_DATE,
            )

    def test_uppercase_existing_contribution_sha_dedupes_against_lowercase_receipt(self) -> None:
        current = ledger()
        row = current["sources"][0]
        row["last_base_contribution_at"] = "2026-08-20"
        row["last_base_contribution_ref"] = "A" * 40
        row["base_contribution_count_since_tracking_start"] = 1
        material = receipt(
            disposition="MATERIAL_CHANGE",
            repository_change="2_FILES",
            pr_created=649,
            merge_sha="a" * 40,
            merged_base_contribution_refs=[
                {
                    "source_id": "anthropic",
                    "pr": 649,
                    "merge_sha": "a" * 40,
                }
            ],
        )
        result = reconcile(
            current,
            [{"receipt_ref": "same-sha", "actual_source_review_receipt": material}],
        )
        updated = result["sources"][0]
        self.assertEqual(1, updated["base_contribution_count_since_tracking_start"])
        self.assertEqual("a" * 40, updated["last_base_contribution_ref"])

    def test_set_like_receipt_order_dedupes_across_different_refs(self) -> None:
        first = receipt()
        reordered = copy.deepcopy(first)
        reordered["scanned_source_ids"] = list(reversed(first["scanned_source_ids"]))
        reordered["unverified_scope"] = list(reversed(first["unverified_scope"]))
        reordered["high_nutrient_sources"][0]["reusable_units"] = ["UNIT_A", "UNIT_B"]
        result = reconcile(
            ledger(),
            [
                {"receipt_ref": "first", "actual_source_review_receipt": first},
                {"receipt_ref": "copy", "actual_source_review_receipt": reordered},
            ],
        )
        self.assertEqual(1, result["sources"][0]["material_candidate_count_since_tracking_start"])

    def test_future_receipt_date_is_rejected_against_batch_date(self) -> None:
        with self.assertRaisesRegex(AnalysisBlocked, "scan_date cannot be after batch_date"):
            reconcile(
                ledger(),
                [
                    {
                        "receipt_ref": "future",
                        "actual_source_review_receipt": receipt(scan_date="2026-09-03"),
                    }
                ],
            )

    def test_repeated_contribution_sha_with_conflicting_metadata_fails_closed(self) -> None:
        base = receipt(
            disposition="MATERIAL_CHANGE",
            repository_change="2_FILES",
            pr_created=649,
            merge_sha="2" * 40,
            merged_base_contribution_refs=[
                {
                    "source_id": "anthropic",
                    "pr": 649,
                    "merge_sha": "2" * 40,
                    "owner": "docs/AI_SKILL_ADOPTION_GUIDE.md",
                }
            ],
        )
        conflict = copy.deepcopy(base)
        conflict["merged_base_contribution_refs"][0]["owner"] = "docs/OTHER_OWNER.md"
        conflict["start_main"] = "2" * 40
        with self.assertRaisesRegex(AnalysisBlocked, "conflicting contribution metadata"):
            reconcile(
                ledger(),
                [
                    {"receipt_ref": "a", "actual_source_review_receipt": base},
                    {"receipt_ref": "b", "actual_source_review_receipt": conflict},
                ],
            )

    def test_missing_required_material_watermark_fields_fail_closed(self) -> None:
        current = ledger()
        del current["sources"][0]["last_material_candidate_at"]
        del current["sources"][0]["material_candidate_count_since_tracking_start"]
        with self.assertRaisesRegex(AnalysisBlocked, "missing material candidate state fields"):
            reconcile(
                current,
                [{"receipt_ref": "receipt", "actual_source_review_receipt": receipt()}],
            )


if __name__ == "__main__":
    unittest.main()
