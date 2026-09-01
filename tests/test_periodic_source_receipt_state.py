from __future__ import annotations

import copy
import unittest

from tools import periodic_source_operations_state as state
from tools.periodic_source_analysis_contract import AnalysisBlocked


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
                "source_archetype": "FAILURE_POSTMORTEM + WORKFLOW_WITH_RECEIPTS",
                "reusable_units": ["CONFIRM_TASK_SOLVABLE_BEFORE_AGENT_RUN"],
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
        "unverified_scope": ["Independent review is incomplete."],
    }
    value.update(overrides)
    return value


class PeriodicSourceReceiptStateTests(unittest.TestCase):
    def test_validates_source_ids_and_normalizes_pr_number(self) -> None:
        checked = state.validate_actual_source_review_receipt(
            receipt(
                pr_created="#649",
                disposition="MATERIAL_CHANGE",
                repository_change="2_FILES",
                merge_sha="2" * 40,
                merged_base_contribution_refs=["PR-649"],
            ),
            ledger(),
        )
        self.assertEqual(649, checked["pr_created"])
        self.assertEqual(["anthropic"], checked["retained_candidate_source_ids"])

    def test_rejects_candidate_id_misfiled_as_retained_source_id(self) -> None:
        bad = receipt(
            retained_candidate_source_ids=["anthropic-eval-containment-solvability-20260901"],
            material_candidate_count_by_source={"anthropic": 1},
        )
        with self.assertRaisesRegex(AnalysisBlocked, "unknown retained Candidate Source ID"):
            state.validate_actual_source_review_receipt(bad, ledger())

    def test_rejects_material_count_keys_that_do_not_match_retained_sources(self) -> None:
        with self.assertRaisesRegex(AnalysisBlocked, "material candidate Source IDs do not match"):
            state.validate_actual_source_review_receipt(
                receipt(retained_candidate_source_ids=["anthropic", "godot"]),
                ledger(),
            )

    def test_rejects_low_score_inside_high_nutrient_sources(self) -> None:
        bad_high = copy.deepcopy(receipt()["high_nutrient_sources"])
        assert isinstance(bad_high, list)
        bad_high[0]["nutrient_score"] = 8
        with self.assertRaisesRegex(AnalysisBlocked, "high-nutrient score must be 9..12"):
            state.validate_actual_source_review_receipt(
                receipt(high_nutrient_sources=bad_high), ledger()
            )

    def test_no_change_cannot_claim_repository_or_merge_change(self) -> None:
        with self.assertRaisesRegex(AnalysisBlocked, "NO_CHANGE cannot claim repository change"):
            state.validate_actual_source_review_receipt(
                receipt(repository_change="2_FILES", merge_sha="2" * 40), ledger()
            )

    def test_reconciles_full_receipt_corpus_idempotently_and_deduplicates_refs(self) -> None:
        first_entry = {
            "receipt_ref": "issue-334-comment-1",
            "actual_source_review_receipt": receipt(),
        }
        no_material = receipt(
            scan_date="2026-08-24",
            retained_candidate_source_ids=[],
            material_candidate_count_by_source={},
            high_nutrient_sources=[],
            scanned_source_ids=["godot"],
            scanned_discovery_seed_ids=[],
        )
        second_entry = {
            "receipt_ref": "issue-334-comment-2",
            "actual_source_review_receipt": no_material,
        }
        corpus = [first_entry, second_entry, copy.deepcopy(first_entry)]
        once = state.reconcile_operations_ledger_from_receipts(ledger(), corpus)
        twice = state.reconcile_operations_ledger_from_receipts(once, corpus)
        self.assertEqual(once, twice)
        rows = {row["source_id"]: row for row in once["sources"]}
        self.assertEqual("2026-09-01", rows["anthropic"]["last_successful_scan_at"])
        self.assertEqual("2026-09-01", rows["anthropic"]["last_material_candidate_at"])
        self.assertEqual(1, rows["anthropic"]["material_candidate_count_since_tracking_start"])
        self.assertEqual("2026-09-01", rows["godot"]["last_successful_scan_at"])

    def test_reconciliation_adds_only_material_receipts_after_existing_watermark(self) -> None:
        current = ledger()
        anth = current["sources"][0]
        anth["last_material_candidate_at"] = "2026-08-20"
        anth["material_candidate_count_since_tracking_start"] = 5
        entry = {"receipt_ref": "new-week", "actual_source_review_receipt": receipt()}
        once = state.reconcile_operations_ledger_from_receipts(current, [entry])
        twice = state.reconcile_operations_ledger_from_receipts(once, [entry])
        rows = {row["source_id"]: row for row in once["sources"]}
        self.assertEqual(6, rows["anthropic"]["material_candidate_count_since_tracking_start"])
        self.assertEqual("2026-09-01", rows["anthropic"]["last_material_candidate_at"])
        self.assertEqual(once, twice)

    def test_semantically_equivalent_receipts_dedupe_after_normalization(self) -> None:
        material_string_pr = receipt(
            disposition="MATERIAL_CHANGE",
            repository_change="2_FILES",
            pr_created="#649",
            merge_sha="2" * 40,
            merged_base_contribution_refs=["PR-649"],
        )
        material_integer_pr = copy.deepcopy(material_string_pr)
        material_integer_pr["pr_created"] = 649
        reconciled = state.reconcile_operations_ledger_from_receipts(
            ledger(),
            [
                {"receipt_ref": "comment-a", "actual_source_review_receipt": material_string_pr},
                {"receipt_ref": "comment-b", "actual_source_review_receipt": material_integer_pr},
            ],
        )
        rows = {row["source_id"]: row for row in reconciled["sources"]}
        self.assertEqual(1, rows["anthropic"]["material_candidate_count_since_tracking_start"])

    def test_same_receipt_ref_with_conflicting_payload_fails_closed(self) -> None:
        first = {"receipt_ref": "same-ref", "actual_source_review_receipt": receipt()}
        second = {
            "receipt_ref": "same-ref",
            "actual_source_review_receipt": receipt(scan_date="2026-08-31"),
        }
        with self.assertRaisesRegex(AnalysisBlocked, "conflicting duplicate receipt ref"):
            state.reconcile_operations_ledger_from_receipts(ledger(), [first, second])


if __name__ == "__main__":
    unittest.main()
