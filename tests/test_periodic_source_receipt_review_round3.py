from __future__ import annotations

import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from tools import periodic_source_receipt_state as state
from tools.periodic_source_analysis_contract import AnalysisBlocked
from tests.test_periodic_source_receipt_state import (
    BATCH_DATE,
    DISCOVERY_SEEDS,
    entry,
    ledger,
    material_receipt,
    receipt,
    reconcile,
)

ROOT = Path(__file__).resolve().parents[1]
RECORDER = ROOT / "tools" / "record_periodic_source_scan.py"

class PeriodicSourceReceiptReviewRound3Tests(unittest.TestCase):
    def test_durable_lane_rejects_discovery_classification_even_when_source_is_active(self):
        with self.assertRaisesRegex(AnalysisBlocked, "classification.*durable lane"):
            state.validate_actual_source_review_receipt(receipt(), ledger(), known_discovery_seed_ids=DISCOVERY_SEEDS, source_state_at_scan={"anthropic": "DISCOVERY_ACTIVE"}, batch_date=BATCH_DATE)

    def test_current_contribution_ref_requires_matching_existing_watermark_date(self):
        current=ledger(); row=current["sources"][0]
        row["last_base_contribution_at"]="2026-09-01"; row["last_base_contribution_ref"]="a"*40; row["base_contribution_count_since_tracking_start"]=1
        value=material_receipt(sha="a"*40); value["merged_base_contribution_refs"][0]["merge_date"]="2026-08-31"
        with self.assertRaisesRegex(AnalysisBlocked, "current contribution ref.*watermark"):
            reconcile(current,[entry(value,ref="mismatch")])

    def test_conflicting_merge_date_aliases_fail_closed(self):
        value=material_receipt(); value["merged_base_contribution_refs"][0]["merged_at"]="2026-08-31"
        with self.assertRaisesRegex(AnalysisBlocked, "conflicting contribution merge-date aliases"):
            state.validate_actual_source_review_receipt(value, ledger(), known_discovery_seed_ids=DISCOVERY_SEEDS, batch_date=BATCH_DATE)

    def test_high_nutrient_rows_have_total_canonical_order(self):
        rows=[{"source":"https://example.com/same","nutrient_score":10,"source_archetype":"TOOL_WITH_SOURCE","reusable_units":["A"]},{"source":"https://example.com/same","nutrient_score":10,"source_archetype":"TOOL_WITH_SOURCE","reusable_units":["B"]}]
        first=receipt(high_nutrient_sources=rows); reordered=copy.deepcopy(first); reordered["high_nutrient_sources"]=list(reversed(reordered["high_nutrient_sources"]))
        result=reconcile(ledger(),[entry(first,ref="ordered"),entry(reordered,ref="reordered")])
        self.assertEqual(1,result["sources"][0]["material_candidate_count_since_tracking_start"])

    def test_processed_receipt_rebuilds_rolled_back_derived_state(self):
        value=material_receipt(); once=reconcile(ledger(),[entry(value,ref="authoritative")]); expected=copy.deepcopy(once["sources"][0]); row=once["sources"][0]
        row["last_successful_scan_at"]=None; row["last_material_candidate_at"]=None; row["material_candidate_count_since_tracking_start"]=0; row["last_base_contribution_at"]=None; row["last_base_contribution_ref"]=None; row["base_contribution_count_since_tracking_start"]=0
        repaired=reconcile(once,[entry(value,ref="authoritative")]); self.assertEqual(expected,repaired["sources"][0])

    def test_baseline_rejects_base_contribution_regression(self):
        current=ledger(); row=current["sources"][0]; row["last_base_contribution_at"]="2026-08-20"; row["last_base_contribution_ref"]="b"*40; row["base_contribution_count_since_tracking_start"]=5
        bootstrapped=reconcile(current,[]); regressed=bootstrapped["sources"][0]; regressed["last_base_contribution_at"]="2026-08-15"; regressed["last_base_contribution_ref"]="c"*40; regressed["base_contribution_count_since_tracking_start"]=1
        with self.assertRaisesRegex(AnalysisBlocked,"regressed below reconciliation baseline"): reconcile(bootstrapped,[])

    def test_receipt_mode_rejects_legacy_material_argument(self):
        with tempfile.TemporaryDirectory() as temporary:
            root=Path(temporary); lp=root/'ledger.json'; cp=root/'corpus.json'; sp=root/'seeds.md'; lp.write_text(json.dumps(ledger())); cp.write_text(json.dumps([])); sp.write_text('seed_id: github-repositories-discovery\n')
            result=subprocess.run([sys.executable,str(RECORDER),'--ledger',str(lp),'--receipt-corpus',str(cp),'--discovery-seeds',str(sp),'--batch-date','2026-09-02','--material','anthropic'],cwd=ROOT,text=True,capture_output=True)
        self.assertNotEqual(0,result.returncode); self.assertIn('mutually exclusive',result.stderr)

    def test_duplicate_json_object_keys_are_rejected_before_ledger_write(self):
        with tempfile.TemporaryDirectory() as temporary:
            root=Path(temporary); lp=root/'ledger.json'; cp=root/'corpus.json'; sp=root/'seeds.md'; original=json.dumps(ledger()); lp.write_text(original); cp.write_text('{"schema_version":1,"receipts":[],"receipts":[]}'); sp.write_text('seed_id: github-repositories-discovery\n')
            result=subprocess.run([sys.executable,str(RECORDER),'--ledger',str(lp),'--receipt-corpus',str(cp),'--discovery-seeds',str(sp),'--batch-date','2026-09-02'],cwd=ROOT,text=True,capture_output=True)
            self.assertNotEqual(0,result.returncode); self.assertIn('duplicate JSON object key',result.stderr); self.assertEqual(original,lp.read_text())

    def test_legacy_cli_rejects_identity_enabled_ledger(self):
        current=reconcile(ledger(),[])
        with tempfile.TemporaryDirectory() as temporary:
            lp=Path(temporary)/'ledger.json'; lp.write_text(json.dumps(current)); result=subprocess.run([sys.executable,str(RECORDER),'--ledger',str(lp),'--date','2026-09-03','--sources','anthropic','--material','anthropic'],cwd=ROOT,text=True,capture_output=True)
        self.assertNotEqual(0,result.returncode); self.assertIn('legacy recorder cannot mutate',result.stderr)

if __name__ == '__main__': unittest.main()
