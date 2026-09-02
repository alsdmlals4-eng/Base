from __future__ import annotations

import copy
import unittest
from datetime import date

from tools import periodic_source_receipt_state as state
from tools.periodic_source_analysis_contract import AnalysisBlocked


BATCH_DATE = date(2026, 9, 2)
DISCOVERY_SEEDS = {"github-repositories-discovery", "youtube-solo-gamedev-zang"}


def source(source_id: str, *, status: str = "ACTIVE") -> dict[str, object]:
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
        "status": status,
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


def entry(
    value: dict[str, object] | None = None,
    *,
    ref: str = "issue-334-comment-1",
    source_state_at_scan: dict[str, str] | None = None,
    contribution_merge_dates: dict[str, str] | None = None,
) -> dict[str, object]:
    result: dict[str, object] = {
        "receipt_ref": ref,
        "actual_source_review_receipt": value or receipt(),
    }
    if source_state_at_scan is not None:
        result["source_state_at_scan"] = source_state_at_scan
    if contribution_merge_dates is not None:
        result["contribution_merge_dates"] = contribution_merge_dates
    return result


def reconcile(
    current: dict[str, object], rows: list[dict[str, object]]
) -> dict[str, object]:
    return state.reconcile_operations_ledger_from_receipts(
        current,
        rows,
        known_discovery_seed_ids=DISCOVERY_SEEDS,
        batch_date=BATCH_DATE,
    )


def material_receipt(*, sha: str = "2" * 40, **overrides: object) -> dict[str, object]:
    value = receipt(
        disposition="MATERIAL_CHANGE",
        repository_change="2_FILES",
        pr_created="#649",
        merge_sha=sha,
        merged_base_contribution_refs=[
            {
                "source_id": "anthropic",
                "pr": 649,
                "merge_sha": sha,
                "merge_date": "2026-09-01",
                "owner": "docs/AI_SKILL_ADOPTION_GUIDE.md",
                "refs": ["owner", "PR#649"],
            }
        ],
    )
    value.update(overrides)
    return value


class PeriodicSourceReceiptStateTests(unittest.TestCase):
    def test_valid_receipt_normalizes_set_like_fields_and_pr_number(self) -> None:
        checked = state.validate_actual_source_review_receipt(
            material_receipt(),
            ledger(),
            known_discovery_seed_ids=DISCOVERY_SEEDS,
            batch_date=BATCH_DATE,
        )
        self.assertEqual(649, checked["pr_created"])
        self.assertEqual(
            ["anthropic", "github-copilot", "godot"], checked["scanned_source_ids"]
        )
        self.assertEqual(["UNIT_A", "UNIT_B"], checked["high_nutrient_sources"][0]["reusable_units"])
        self.assertEqual(["scope-a", "scope-b"], checked["unverified_scope"])

    def test_rejects_candidate_packet_id_as_source_identity(self) -> None:
        bad = receipt(
            retained_candidate_source_ids=["anthropic-eval-containment-solvability-20260901"],
            material_candidate_count_by_source={"anthropic": 1},
        )
        with self.assertRaisesRegex(AnalysisBlocked, "unknown retained Candidate Source ID"):
            state.validate_actual_source_review_receipt(
                bad,
                ledger(),
                known_discovery_seed_ids=DISCOVERY_SEEDS,
                batch_date=BATCH_DATE,
            )

    def test_rejects_unknown_discovery_seed_and_durable_id_in_seed_lane(self) -> None:
        for seed_id, message in (
            ("github-repositories-discoveri", "unknown discovery seed ID"),
            ("anthropic", "durable Source ID must use scanned_source_ids"),
        ):
            with self.subTest(seed_id=seed_id):
                bad = receipt(
                    scanned_source_ids=[],
                    scanned_discovery_seed_ids=[seed_id],
                    retained_candidate_source_ids=[],
                    material_candidate_count_by_source={},
                    high_nutrient_sources=[],
                )
                with self.assertRaisesRegex(AnalysisBlocked, message):
                    state.validate_actual_source_review_receipt(
                        bad,
                        ledger(),
                        known_discovery_seed_ids=DISCOVERY_SEEDS,
                        batch_date=BATCH_DATE,
                    )

    def test_rejects_future_receipt_date(self) -> None:
        with self.assertRaisesRegex(AnalysisBlocked, "scan_date cannot be after batch_date"):
            reconcile(ledger(), [entry(receipt(scan_date="2026-09-03"))])

    def test_rejects_future_contribution_merge_date(self) -> None:
        future = material_receipt()
        future["merged_base_contribution_refs"][0]["merge_date"] = "2026-09-03"
        with self.assertRaisesRegex(
            AnalysisBlocked, "contribution merge_date cannot be after batch_date"
        ):
            reconcile(ledger(), [entry(future, ref="future-merge")])

    def test_rejects_missing_material_and_base_watermark_fields(self) -> None:
        for field, message in (
            ("last_material_candidate_at", "missing material candidate state fields"),
            ("material_candidate_count_since_tracking_start", "missing material candidate state fields"),
            ("last_base_contribution_ref", "missing Base contribution state fields"),
        ):
            with self.subTest(field=field):
                current = ledger()
                del current["sources"][0][field]
                with self.assertRaisesRegex(AnalysisBlocked, message):
                    reconcile(current, [entry()])

    def test_rejects_conflicting_contribution_source_aliases(self) -> None:
        bad = material_receipt()
        bad["merged_base_contribution_refs"][0]["source"] = "godot"
        with self.assertRaisesRegex(AnalysisBlocked, "conflicting contribution Source aliases"):
            state.validate_actual_source_review_receipt(
                bad,
                ledger(),
                known_discovery_seed_ids=DISCOVERY_SEEDS,
                batch_date=BATCH_DATE,
            )

    def test_rejects_contribution_without_trusted_merge_date(self) -> None:
        bad = material_receipt()
        del bad["merged_base_contribution_refs"][0]["merge_date"]
        with self.assertRaisesRegex(AnalysisBlocked, "requires trusted merge evidence"):
            state.validate_actual_source_review_receipt(
                bad,
                ledger(),
                known_discovery_seed_ids=DISCOVERY_SEEDS,
                batch_date=BATCH_DATE,
            )

    def test_legacy_flat_contribution_uses_operator_merge_date_map(self) -> None:
        legacy = receipt(
            disposition="MATERIAL_CHANGE",
            repository_change="2_FILES",
            pr_created=608,
            merge_sha="3" * 40,
            merged_base_contribution_refs=["PR#608", "3" * 40],
        )
        checked = state.validate_actual_source_review_receipt(
            legacy,
            ledger(),
            known_discovery_seed_ids=DISCOVERY_SEEDS,
            contribution_merge_dates={"3" * 40: "2026-08-22"},
            batch_date=BATCH_DATE,
        )
        self.assertEqual("2026-08-22", checked["merged_base_contribution_refs"][0]["merge_date"])

    def test_repeated_corpus_is_idempotent_and_receipt_refs_normalize(self) -> None:
        first = entry(ref="#42")
        once = reconcile(ledger(), [first])
        twice = reconcile(once, [entry(ref="42")])
        self.assertEqual(once, twice)
        identity = once["receipt_reconciliation_state"]
        self.assertEqual("issue-334-comment-42", identity["processed_receipts"][0]["receipt_ref"])

    def test_reordered_set_like_receipt_dedupes_across_refs(self) -> None:
        first = receipt()
        reordered = copy.deepcopy(first)
        reordered["scanned_source_ids"] = list(reversed(first["scanned_source_ids"]))
        reordered["unverified_scope"] = list(reversed(first["unverified_scope"]))
        reordered["high_nutrient_sources"][0]["reusable_units"] = ["UNIT_A", "UNIT_B"]
        result = reconcile(
            ledger(),
            [entry(first, ref="1"), entry(reordered, ref="2")],
        )
        self.assertEqual(1, result["sources"][0]["material_candidate_count_since_tracking_start"])
        self.assertEqual(2, len(result["receipt_reconciliation_state"]["processed_receipts"]))

    def test_same_ref_with_different_payload_fails_closed(self) -> None:
        with self.assertRaisesRegex(AnalysisBlocked, "conflicting duplicate receipt ref"):
            reconcile(
                ledger(),
                [entry(ref="same"), entry(receipt(start_main="2" * 40), ref="same")],
            )

    def test_new_same_day_receipt_counts_once_after_identity_state_exists(self) -> None:
        once = reconcile(ledger(), [entry(ref="1")])
        twice = reconcile(
            once,
            [entry(receipt(start_main="2" * 40), ref="2")],
        )
        repeated = reconcile(
            twice,
            [entry(receipt(start_main="2" * 40), ref="2")],
        )
        self.assertEqual(2, twice["sources"][0]["material_candidate_count_since_tracking_start"])
        self.assertEqual(twice, repeated)

    def test_initial_same_day_material_without_identity_state_fails_closed(self) -> None:
        current = ledger()
        current["sources"][0]["last_material_candidate_at"] = "2026-09-01"
        current["sources"][0]["material_candidate_count_since_tracking_start"] = 5
        with self.assertRaisesRegex(AnalysisBlocked, "identity baseline"):
            reconcile(current, [entry(ref="late")])

    def test_empty_bootstrap_does_not_unlock_ambiguous_same_day_material(self) -> None:
        current = ledger()
        current["sources"][0]["last_material_candidate_at"] = "2026-09-01"
        current["sources"][0]["material_candidate_count_since_tracking_start"] = 5
        bootstrapped = reconcile(current, [])
        with self.assertRaisesRegex(AnalysisBlocked, "identity baseline"):
            reconcile(bootstrapped, [entry(ref="late-after-empty-bootstrap")])

    def test_unrelated_bootstrap_does_not_unlock_another_source_baseline(self) -> None:
        current = ledger()
        current["sources"][0]["last_material_candidate_at"] = "2026-09-01"
        current["sources"][0]["material_candidate_count_since_tracking_start"] = 5
        godot_only = receipt(
            scanned_source_ids=["godot"],
            scanned_discovery_seed_ids=[],
            retained_candidate_source_ids=[],
            material_candidate_count_by_source={},
            high_nutrient_sources=[],
        )
        bootstrapped = reconcile(current, [entry(godot_only, ref="godot-only")])
        with self.assertRaisesRegex(AnalysisBlocked, "identity baseline"):
            reconcile(bootstrapped, [entry(ref="late-anthropic")])

    def test_uppercase_existing_contribution_sha_is_not_double_counted(self) -> None:
        current = ledger()
        row = current["sources"][0]
        row["last_base_contribution_at"] = "2026-09-01"
        row["last_base_contribution_ref"] = "A" * 40
        row["base_contribution_count_since_tracking_start"] = 1
        result = reconcile(
            current,
            [entry(material_receipt(sha="a" * 40), ref="same-sha")],
        )
        updated = result["sources"][0]
        self.assertEqual(1, updated["base_contribution_count_since_tracking_start"])
        self.assertEqual("a" * 40, updated["last_base_contribution_ref"])

    def test_repeated_contribution_sha_with_conflicting_metadata_fails_closed(self) -> None:
        first = material_receipt()
        second = copy.deepcopy(first)
        second["start_main"] = "2" * 40
        second["merged_base_contribution_refs"][0]["owner"] = "docs/OTHER.md"
        with self.assertRaisesRegex(AnalysisBlocked, "conflicting contribution metadata"):
            reconcile(
                ledger(),
                [entry(first, ref="a"), entry(second, ref="b")],
            )

    def test_contribution_uses_merge_date_not_scan_date(self) -> None:
        value = material_receipt()
        value["scan_date"] = "2026-08-20"
        value["merged_base_contribution_refs"][0]["merge_date"] = "2026-09-01"
        result = reconcile(ledger(), [entry(value, ref="merge-date")])
        row = result["sources"][0]
        self.assertEqual("2026-09-01", row["last_base_contribution_at"])

    def test_already_processed_receipt_replays_after_source_becomes_inactive(self) -> None:
        once = reconcile(ledger(), [entry(ref="historical")])
        once["sources"][0]["status"] = "INACTIVE"
        replayed = reconcile(once, [entry(ref="historical")])
        self.assertEqual(once, replayed)

    def test_new_historical_receipt_for_inactive_source_requires_explicit_state(self) -> None:
        current = ledger()
        current["sources"][0]["status"] = "INACTIVE"
        with self.assertRaisesRegex(AnalysisBlocked, "receipt-time classification"):
            reconcile(current, [entry(ref="historical-new")])
        accepted = state.reconcile_operations_ledger_from_receipts(
            current,
            [
                entry(
                    ref="historical-new",
                    source_state_at_scan={"anthropic": "DURABLE_ACTIVE"},
                )
            ],
            known_discovery_seed_ids=DISCOVERY_SEEDS,
            batch_date=BATCH_DATE,
        )
        self.assertEqual("2026-09-01", accepted["sources"][0]["last_successful_scan_at"])

    def test_promoted_seed_historical_receipt_requires_explicit_history_registry(self) -> None:
        current = ledger()
        current["sources"].append(source("old-seed"))
        old = receipt(
            scanned_source_ids=[],
            scanned_discovery_seed_ids=["old-seed"],
            retained_candidate_source_ids=["old-seed"],
            material_candidate_count_by_source={"old-seed": 1},
            high_nutrient_sources=[],
        )
        with self.assertRaisesRegex(AnalysisBlocked, "durable Source ID"):
            state.reconcile_operations_ledger_from_receipts(
                current,
                [entry(old, ref="old-seed")],
                known_discovery_seed_ids=DISCOVERY_SEEDS,
                batch_date=BATCH_DATE,
            )
        accepted = state.reconcile_operations_ledger_from_receipts(
            current,
            [
                entry(
                    old,
                    ref="old-seed",
                    source_state_at_scan={"old-seed": "DISCOVERY_ACTIVE"},
                )
            ],
            known_discovery_seed_ids=DISCOVERY_SEEDS,
            historical_discovery_seed_ids={"old-seed"},
            batch_date=BATCH_DATE,
        )
        self.assertEqual(
            0,
            accepted["sources"][-1]["material_candidate_count_since_tracking_start"],
        )

    def test_rejects_unrelated_receipt_time_classification(self) -> None:
        with self.assertRaisesRegex(AnalysisBlocked, "unrelated Source IDs"):
            state.reconcile_operations_ledger_from_receipts(
                ledger(),
                [
                    entry(
                        ref="unrelated-classification",
                        source_state_at_scan={"not-in-receipt": "DURABLE_ACTIVE"},
                    )
                ],
                known_discovery_seed_ids=DISCOVERY_SEEDS,
                batch_date=BATCH_DATE,
            )

    def test_discovery_seed_registry_parser_extracts_seed_ids(self) -> None:
        text = """
```yaml
seed_id: github-repositories-discovery
status: ACTIVE_DISCOVERY_SEED
```
seed_id: youtube-solo-gamedev-zang
"""
        self.assertEqual(DISCOVERY_SEEDS, state.parse_active_discovery_seed_ids(text))


    def test_rejects_unknown_receipt_fields_that_change_payload_identity(self) -> None:
        bad = receipt()
        bad["candidate_packet_ids"] = ["anthropic-candidate-1"]
        with self.assertRaisesRegex(AnalysisBlocked, "unsupported receipt fields"):
            state.validate_actual_source_review_receipt(
                bad,
                ledger(),
                known_discovery_seed_ids=DISCOVERY_SEEDS,
                batch_date=BATCH_DATE,
            )

    def test_rejects_unknown_high_nutrient_fields(self) -> None:
        bad = receipt()
        bad["high_nutrient_sources"][0]["score_breakdown"] = {"primary": 3}
        with self.assertRaisesRegex(AnalysisBlocked, "unsupported high-nutrient source fields"):
            state.validate_actual_source_review_receipt(
                bad,
                ledger(),
                known_discovery_seed_ids=DISCOVERY_SEEDS,
                batch_date=BATCH_DATE,
            )

    def test_discovery_seed_parser_rejects_duplicates_and_excludes_retired_blocks(self) -> None:
        duplicate = """```yaml
seed_id: duplicate
status: ACTIVE_DISCOVERY_SEED
```
```yaml
seed_id: duplicate
status: ACTIVE_DISCOVERY_SEED
```
"""
        with self.assertRaisesRegex(AnalysisBlocked, "duplicate discovery seed ID"):
            state.parse_active_discovery_seed_ids(duplicate)

        mixed = """```yaml
seed_id: active
status: ACTIVE_DISCOVERY_SEED
```
```yaml
seed_id: retired
status: RETIRED
```
"""
        self.assertEqual({"active"}, state.parse_active_discovery_seed_ids(mixed))

    def test_rejects_unrelated_contribution_merge_date_evidence(self) -> None:
        with self.assertRaisesRegex(AnalysisBlocked, "unrelated contribution merge dates"):
            state.validate_actual_source_review_receipt(
                receipt(),
                ledger(),
                known_discovery_seed_ids=DISCOVERY_SEEDS,
                contribution_merge_dates={"2" * 40: "2026-09-01"},
                batch_date=BATCH_DATE,
            )

    def test_rejects_current_ledger_state_that_regresses_below_persisted_baseline(self) -> None:
        current = ledger()
        current["sources"][0]["material_candidate_count_since_tracking_start"] = 5
        current["sources"][0]["last_material_candidate_at"] = "2026-08-20"
        once = reconcile(current, [])
        once["sources"][0]["material_candidate_count_since_tracking_start"] = 4
        with self.assertRaisesRegex(AnalysisBlocked, "regressed below reconciliation baseline"):
            reconcile(once, [])


if __name__ == "__main__":
    unittest.main()
