from __future__ import annotations
import json
from pathlib import Path
import tempfile
import unittest
from tools.record_periodic_source_scan import record


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


if __name__ == "__main__":
    unittest.main()
