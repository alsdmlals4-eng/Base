from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from tools.record_periodic_source_scan import record, record_receipt_corpus


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools" / "record_periodic_source_scan.py"


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
        "watchlist_owner": "watchlist",
        "state_semantics": "fixture",
        "sources": [source("anthropic"), source("godot")],
    }


def receipt() -> dict[str, object]:
    return {
        "scan_date": "2026-09-01",
        "start_main": "1" * 40,
        "final_main": "1" * 40,
        "disposition": "NO_CHANGE",
        "high_nutrient_sources": [],
        "scanned_source_ids": ["anthropic"],
        "scanned_discovery_seed_ids": ["github-repositories-discovery"],
        "retained_candidate_source_ids": [],
        "material_candidate_count_by_source": {},
        "merged_base_contribution_refs": [],
        "repository_change": "NONE",
        "pr_created": None,
        "merge_sha": None,
        "ledger_write": "DEFER_TO_WEEKLY_SCAN_STATE_BATCH",
        "unverified_scope": [],
    }


def write_json(path: Path, payload: object) -> None:
    path.write_text(json.dumps(payload), encoding="utf-8")


class RecordPeriodicSourceScanTests(unittest.TestCase):
    def test_legacy_record_function_updates_only_requested_source(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "ledger.json"
            write_json(path, ledger())
            record(path, "2026-08-22", ["anthropic"], ["anthropic"])
            result = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual("2026-08-22", result["sources"][0]["last_successful_scan_at"])
        self.assertEqual(1, result["sources"][0]["material_candidate_count_since_tracking_start"])
        self.assertIsNone(result["sources"][1]["last_successful_scan_at"])

    def test_direct_legacy_cli_execution_remains_available(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "ledger.json"
            write_json(path, ledger())
            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--ledger",
                    str(path),
                    "--date",
                    "2026-08-22",
                    "--sources",
                    "anthropic",
                    "--material",
                    "anthropic",
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(0, result.returncode, result.stderr)
            updated = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual("2026-08-22", updated["sources"][0]["last_successful_scan_at"])

    def test_receipt_corpus_cli_executes_and_is_idempotent(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            ledger_path = root / "ledger.json"
            corpus_path = root / "corpus.json"
            seeds_path = root / "seeds.md"
            write_json(ledger_path, ledger())
            write_json(
                corpus_path,
                {
                    "schema_version": 1,
                    "historical_discovery_seed_ids": [],
                    "receipts": [
                        {
                            "receipt_ref": "1",
                            "actual_source_review_receipt": receipt(),
                        }
                    ],
                },
            )
            seeds_path.write_text(
                "seed_id: github-repositories-discovery\nstatus: ACTIVE_DISCOVERY_SEED\n",
                encoding="utf-8",
            )
            command = [
                sys.executable,
                str(SCRIPT),
                "--ledger",
                str(ledger_path),
                "--receipt-corpus",
                str(corpus_path),
                "--discovery-seeds",
                str(seeds_path),
                "--batch-date",
                "2026-09-02",
            ]
            first = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, check=False)
            self.assertEqual(0, first.returncode, first.stderr)
            first_bytes = ledger_path.read_bytes()
            second = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, check=False)
            self.assertEqual(0, second.returncode, second.stderr)
            self.assertEqual(first_bytes, ledger_path.read_bytes())
            result = json.loads(first_bytes)
            self.assertEqual("2026-09-01", result["sources"][0]["last_successful_scan_at"])
            self.assertEqual(1, len(result["receipt_reconciliation_state"]["processed_receipts"]))

    def test_invalid_corpus_leaves_ledger_bytes_unchanged(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            ledger_path = root / "ledger.json"
            corpus_path = root / "corpus.json"
            seeds_path = root / "seeds.md"
            write_json(ledger_path, ledger())
            original_hash = hashlib.sha256(ledger_path.read_bytes()).hexdigest()
            bad = receipt()
            bad["scanned_discovery_seed_ids"] = ["typo-seed"]
            write_json(
                corpus_path,
                [{"receipt_ref": "bad", "actual_source_review_receipt": bad}],
            )
            seeds_path.write_text(
                "seed_id: github-repositories-discovery\n",
                encoding="utf-8",
            )
            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--ledger",
                    str(ledger_path),
                    "--receipt-corpus",
                    str(corpus_path),
                    "--discovery-seeds",
                    str(seeds_path),
                    "--batch-date",
                    "2026-09-02",
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertNotEqual(0, result.returncode)
            self.assertEqual(original_hash, hashlib.sha256(ledger_path.read_bytes()).hexdigest())

    def test_record_receipt_corpus_function_reads_seed_registry(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            ledger_path = root / "ledger.json"
            corpus_path = root / "corpus.json"
            seeds_path = root / "seeds.md"
            write_json(ledger_path, ledger())
            write_json(
                corpus_path,
                [{"receipt_ref": "1", "actual_source_review_receipt": receipt()}],
            )
            seeds_path.write_text(
                "seed_id: github-repositories-discovery\n",
                encoding="utf-8",
            )
            record_receipt_corpus(
                ledger_path,
                corpus_path,
                seeds_path,
                "2026-09-02",
            )
            result = json.loads(ledger_path.read_text(encoding="utf-8"))
            self.assertEqual("2026-09-01", result["sources"][0]["last_successful_scan_at"])


if __name__ == "__main__":
    unittest.main()
