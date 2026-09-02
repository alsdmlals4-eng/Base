from __future__ import annotations

import copy
import unittest

from tools import periodic_source_receipt_state as state
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


    def test_rejects_scans_for_inactive_ledger_sources(self) -> None:
        inactive = ledger()
        inactive["sources"][0]["status"] = "INACTIVE"
        with self.assertRaisesRegex(AnalysisBlocked, "cannot record inactive Source"):
            state.validate_actual_source_review_receipt(receipt(), inactive)

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


    def test_legacy_optional_field_omission_dedupes_with_explicit_defaults(self) -> None:
        explicit = receipt(high_nutrient_sources=[])
        legacy = copy.deepcopy(explicit)
        del legacy["high_nutrient_sources"]
        del legacy["merge_sha"]
        reconciled = state.reconcile_operations_ledger_from_receipts(
            ledger(),
            [
                {"receipt_ref": "explicit", "actual_source_review_receipt": explicit},
                {"receipt_ref": "legacy", "actual_source_review_receipt": legacy},
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


    def test_structured_contribution_updates_durable_ledger_once(self) -> None:
        material = receipt(
            disposition="MATERIAL_CHANGE",
            repository_change="2_FILES",
            pr_created="#649",
            merge_sha="2" * 40,
            merged_base_contribution_refs=[{
                "source": "anthropic",
                "pr": "#649",
                "merge_sha": "2" * 40,
                "owner": "docs/AI_SKILL_ADOPTION_GUIDE.md",
            }],
        )
        entry = {"receipt_ref": "material-649", "actual_source_review_receipt": material}
        once = state.reconcile_operations_ledger_from_receipts(ledger(), [entry])
        twice = state.reconcile_operations_ledger_from_receipts(once, [entry])
        rows = {row["source_id"]: row for row in once["sources"]}
        self.assertEqual("2026-09-01", rows["anthropic"]["last_base_contribution_at"])
        self.assertEqual("2" * 40, rows["anthropic"]["last_base_contribution_ref"])
        self.assertEqual(1, rows["anthropic"]["base_contribution_count_since_tracking_start"])
        self.assertEqual(once, twice)

    def test_legacy_flat_contribution_infers_only_single_retained_source(self) -> None:
        checked = state.validate_actual_source_review_receipt(
            receipt(
                disposition="MATERIAL_CHANGE",
                repository_change="2_FILES",
                pr_created=608,
                merge_sha="3" * 40,
                merged_base_contribution_refs=["PR#608", "3" * 40],
            ),
            ledger(),
        )
        self.assertEqual(
            [{
                "source_id": "anthropic",
                "pr": 608,
                "merge_sha": "3" * 40,
                "refs": ["PR#608", "3" * 40],
            }],
            checked["merged_base_contribution_refs"],
        )

    def test_legacy_flat_contribution_rejects_ambiguous_sources(self) -> None:
        with self.assertRaisesRegex(AnalysisBlocked, "legacy contribution refs require one retained Source"):
            state.validate_actual_source_review_receipt(
                receipt(
                    disposition="MATERIAL_CHANGE",
                    repository_change="2_FILES",
                    pr_created=649,
                    merge_sha="2" * 40,
                    retained_candidate_source_ids=["anthropic", "godot"],
                    material_candidate_count_by_source={"anthropic": 1, "godot": 1},
                    merged_base_contribution_refs=["PR#649", "2" * 40],
                ),
                ledger(),
            )

    def test_structured_contribution_source_must_be_retained(self) -> None:
        with self.assertRaisesRegex(AnalysisBlocked, "contribution Source must be retained"):
            state.validate_actual_source_review_receipt(
                receipt(
                    disposition="MATERIAL_CHANGE",
                    repository_change="2_FILES",
                    pr_created=649,
                    merge_sha="2" * 40,
                    merged_base_contribution_refs=[{
                        "source": "godot",
                        "pr": 649,
                        "merge_sha": "2" * 40,
                    }],
                ),
                ledger(),
            )

    def test_discovery_only_contribution_does_not_create_durable_ledger_row(self) -> None:
        discovery = receipt(
            disposition="MATERIAL_CHANGE",
            repository_change="2_FILES",
            pr_created=649,
            merge_sha="2" * 40,
            scanned_source_ids=[],
            scanned_discovery_seed_ids=["github-repositories-discovery"],
            retained_candidate_source_ids=["github-repositories-discovery"],
            material_candidate_count_by_source={"github-repositories-discovery": 1},
            high_nutrient_sources=[],
            merged_base_contribution_refs=["PR#649", "2" * 40],
        )
        reconciled = state.reconcile_operations_ledger_from_receipts(
            ledger(),
            [{"receipt_ref": "discovery-649", "actual_source_review_receipt": discovery}],
        )
        for row in reconciled["sources"]:
            self.assertEqual(0, row["base_contribution_count_since_tracking_start"])
        self.assertIsNone(row["last_base_contribution_at"])
        self.assertIsNone(row["last_base_contribution_ref"])

    def test_rejects_receipt_without_any_actually_reviewed_source_identity(self) -> None:
        with self.assertRaisesRegex(AnalysisBlocked, "must identify an actually reviewed Source"):
            state.validate_actual_source_review_receipt(
                receipt(
                    scanned_source_ids=[],
                    scanned_discovery_seed_ids=[],
                    retained_candidate_source_ids=[],
                    material_candidate_count_by_source={},
                    high_nutrient_sources=[],
                ),
                ledger(),
            )

    def test_durable_source_id_cannot_be_misfiled_as_discovery_seed(self) -> None:
        with self.assertRaisesRegex(AnalysisBlocked, "durable Source ID must use scanned_source_ids"):
            state.validate_actual_source_review_receipt(
                receipt(
                    scanned_source_ids=[],
                    scanned_discovery_seed_ids=["anthropic"],
                    retained_candidate_source_ids=[],
                    material_candidate_count_by_source={},
                    high_nutrient_sources=[],
                ),
                ledger(),
            )

    def test_reconciliation_adds_new_base_contribution_after_existing_watermark(self) -> None:
        current = ledger()
        anth = current["sources"][0]
        anth["last_base_contribution_at"] = "2026-08-20"
        anth["last_base_contribution_ref"] = "3" * 40
        anth["base_contribution_count_since_tracking_start"] = 5
        material = receipt(
            disposition="MATERIAL_CHANGE",
            repository_change="2_FILES",
            pr_created=649,
            merge_sha="2" * 40,
            merged_base_contribution_refs=[{
                "source": "anthropic",
                "pr": 649,
                "merge_sha": "2" * 40,
            }],
        )
        entry = {"receipt_ref": "new-contribution", "actual_source_review_receipt": material}
        once = state.reconcile_operations_ledger_from_receipts(current, [entry])
        twice = state.reconcile_operations_ledger_from_receipts(once, [entry])
        rows = {row["source_id"]: row for row in once["sources"]}
        self.assertEqual(6, rows["anthropic"]["base_contribution_count_since_tracking_start"])
        self.assertEqual("2026-09-01", rows["anthropic"]["last_base_contribution_at"])
        self.assertEqual("2" * 40, rows["anthropic"]["last_base_contribution_ref"])
        self.assertEqual(once, twice)

    def test_existing_material_count_requires_date_watermark(self) -> None:
        current = ledger()
        anth = current["sources"][0]
        anth["material_candidate_count_since_tracking_start"] = 5
        entry = {"receipt_ref": "new-material", "actual_source_review_receipt": receipt()}
        with self.assertRaisesRegex(AnalysisBlocked, "existing material candidate state is inconsistent"):
            state.reconcile_operations_ledger_from_receipts(current, [entry])

    def test_existing_base_contribution_state_requires_count_date_and_ref_together(self) -> None:
        material = receipt(
            disposition="MATERIAL_CHANGE",
            repository_change="2_FILES",
            pr_created=649,
            merge_sha="2" * 40,
            merged_base_contribution_refs=[{
                "source": "anthropic",
                "pr": 649,
                "merge_sha": "2" * 40,
            }],
        )
        entry = {"receipt_ref": "new-contribution", "actual_source_review_receipt": material}
        broken_states = (
            {"last_base_contribution_at": "2026-08-20", "last_base_contribution_ref": None, "base_contribution_count_since_tracking_start": 1},
            {"last_base_contribution_at": "2026-08-20", "last_base_contribution_ref": "3" * 40, "base_contribution_count_since_tracking_start": 0},
            {"last_base_contribution_at": None, "last_base_contribution_ref": "3" * 40, "base_contribution_count_since_tracking_start": 1},
        )
        for broken in broken_states:
            with self.subTest(broken=broken):
                current = ledger()
                current["sources"][0].update(broken)
                with self.assertRaisesRegex(AnalysisBlocked, "existing Base contribution state is inconsistent"):
                    state.reconcile_operations_ledger_from_receipts(current, [entry])


if __name__ == "__main__":
    unittest.main()
