from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

from tools.periodic_source_analysis_contract import AnalysisBlocked
from tools.record_periodic_source_scan import main, record, record_receipt_corpus


class RecordPeriodicSourceScanTests(unittest.TestCase):
    def test_updates_only_requested_sources_and_material_counter(self) -> None:
        payload = {"schema_version": 1, "sources": [
            {"source_id": "a", "status": "ACTIVE", "last_successful_scan_at": None, "last_material_candidate_at": None, "material_candidate_count_since_tracking_start": 0},
            {"source_id": "b", "status": "ACTIVE", "last_successful_scan_at": "2026-08-01", "last_material_candidate_at": None, "material_candidate_count_since_tracking_start": 0},
        ]}
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "ledger.json"
            path.write_text(json.dumps(payload), encoding="utf-8")
            record(path, "2026-08-22", ["a"], ["a"])
            result = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(result["sources"][0]["last_successful_scan_at"], "2026-08-22")
        self.assertEqual(result["sources"][0]["last_material_candidate_at"], "2026-08-22")
        self.assertEqual(result["sources"][0]["material_candidate_count_since_tracking_start"], 1)
        self.assertEqual(result["sources"][1]["last_successful_scan_at"], "2026-08-01")

    def test_cli_receipt_corpus_mode_uses_the_validated_consumer(self) -> None:
        payload = {
            "schema_version": 1,
            "tracking_started_at": "2026-08-11",
            "sources": [{
                "source_id": "a",
                "status": "ACTIVE",
                "last_successful_scan_at": None,
                "last_material_candidate_at": None,
                "material_candidate_count_since_tracking_start": 0,
            }],
        }
        receipt = {
            "scan_date": "2026-09-01",
            "start_main": "1" * 40,
            "final_main": "1" * 40,
            "disposition": "NO_CHANGE",
            "high_nutrient_sources": [],
            "scanned_source_ids": ["a"],
            "scanned_discovery_seed_ids": [],
            "retained_candidate_source_ids": [],
            "material_candidate_count_by_source": {},
            "merged_base_contribution_refs": [],
            "repository_change": "NONE",
            "pr_created": None,
            "merge_sha": None,
            "ledger_write": "DEFER_TO_WEEKLY_SCAN_STATE_BATCH",
            "unverified_scope": [],
        }
        corpus = {"receipts": [{
            "receipt_ref": "issue-334-comment-cli",
            "actual_source_review_receipt": receipt,
        }]}
        with tempfile.TemporaryDirectory() as tmp:
            ledger_path = Path(tmp) / "ledger.json"
            corpus_path = Path(tmp) / "receipts.json"
            ledger_path.write_text(json.dumps(payload), encoding="utf-8")
            corpus_path.write_text(json.dumps(corpus), encoding="utf-8")
            exit_code = main([
                "--ledger", str(ledger_path),
                "--receipt-corpus", str(corpus_path),
            ])
            result = json.loads(ledger_path.read_text(encoding="utf-8"))
        self.assertEqual(0, exit_code)
        self.assertEqual("2026-09-01", result["sources"][0]["last_successful_scan_at"])

    def test_receipt_corpus_mode_validates_and_updates_the_ledger(self) -> None:
        payload = {
            "schema_version": 1,
            "tracking_started_at": "2026-08-11",
            "sources": [{
                "source_id": "a",
                "status": "ACTIVE",
                "last_successful_scan_at": None,
                "last_material_candidate_at": None,
                "material_candidate_count_since_tracking_start": 0,
            }],
        }
        receipt = {
            "scan_date": "2026-09-01",
            "start_main": "1" * 40,
            "final_main": "1" * 40,
            "disposition": "NO_CHANGE",
            "high_nutrient_sources": [],
            "scanned_source_ids": ["a"],
            "scanned_discovery_seed_ids": [],
            "retained_candidate_source_ids": ["a"],
            "material_candidate_count_by_source": {"a": 1},
            "merged_base_contribution_refs": [],
            "repository_change": "NONE",
            "pr_created": None,
            "merge_sha": None,
            "ledger_write": "DEFER_TO_WEEKLY_SCAN_STATE_BATCH",
            "unverified_scope": [],
        }
        corpus = {"receipts": [{
            "receipt_ref": "issue-334-comment-1",
            "actual_source_review_receipt": receipt,
        }]}
        with tempfile.TemporaryDirectory() as tmp:
            ledger_path = Path(tmp) / "ledger.json"
            corpus_path = Path(tmp) / "receipts.json"
            ledger_path.write_text(json.dumps(payload), encoding="utf-8")
            corpus_path.write_text(json.dumps(corpus), encoding="utf-8")
            record_receipt_corpus(ledger_path, corpus_path)
            result = json.loads(ledger_path.read_text(encoding="utf-8"))
        self.assertEqual("2026-09-01", result["sources"][0]["last_successful_scan_at"])
        self.assertEqual(1, result["sources"][0]["material_candidate_count_since_tracking_start"])

    def test_invalid_receipt_corpus_leaves_the_ledger_unchanged(self) -> None:
        payload = {
            "schema_version": 1,
            "tracking_started_at": "2026-08-11",
            "sources": [{
                "source_id": "a",
                "status": "ACTIVE",
                "last_successful_scan_at": None,
                "last_material_candidate_at": None,
                "material_candidate_count_since_tracking_start": 0,
            }],
        }
        invalid = {"receipts": [{
            "receipt_ref": "issue-334-comment-1",
            "actual_source_review_receipt": {
                "scan_date": "2026-09-01",
                "start_main": "1" * 40,
                "final_main": "1" * 40,
                "disposition": "NO_CHANGE",
                "scanned_source_ids": ["a"],
                "scanned_discovery_seed_ids": [],
                "retained_candidate_source_ids": ["candidate-id-not-source-id"],
                "material_candidate_count_by_source": {"a": 1},
                "merged_base_contribution_refs": [],
                "repository_change": "NONE",
                "pr_created": None,
                "merge_sha": None,
                "ledger_write": "DEFER_TO_WEEKLY_SCAN_STATE_BATCH",
                "unverified_scope": [],
            },
        }]}
        with tempfile.TemporaryDirectory() as tmp:
            ledger_path = Path(tmp) / "ledger.json"
            corpus_path = Path(tmp) / "receipts.json"
            original = json.dumps(payload)
            ledger_path.write_text(original, encoding="utf-8")
            corpus_path.write_text(json.dumps(invalid), encoding="utf-8")
            with self.assertRaisesRegex(AnalysisBlocked, "unknown retained Candidate Source ID"):
                record_receipt_corpus(ledger_path, corpus_path)
            self.assertEqual(original, ledger_path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
