"""Verified Source scan state helper."""

from __future__ import annotations

import copy
from collections.abc import Mapping, Sequence
from datetime import date

from tools.periodic_source_analysis_contract import AnalysisBlocked

SCAN_DATE_FIELD = "last_successful_scan_at"
MATERIAL_DATE_FIELD = "last_material_candidate_at"
MATERIAL_COUNT_FIELD = "material_candidate_count_since_tracking_start"


def update_operations_ledger(
    ledger: Mapping[str, object],
    scanned_source_ids: set[str],
    retained_candidates: Sequence[Mapping[str, object]],
    run_date: date,
) -> dict[str, object]:
    if "receipt_reconciliation_state" in ledger:
        raise AnalysisBlocked(
            "BLOCKED_RECEIPT_RECONCILIATION_REQUIRED",
            "identity-enabled Operations Ledger must mutate through the receipt reconciler",
        )
    result = copy.deepcopy(dict(ledger))
    rows = result.get("sources")
    if result.get("schema_version") != 1 or not isinstance(rows, list):
        raise AnalysisBlocked("BLOCKED_CONTEXT_SCHEMA", "invalid operations Ledger")
    by_id = {
        str(row.get("source_id")): row
        for row in rows
        if isinstance(row, dict)
    }
    if not scanned_source_ids.issubset(by_id):
        raise AnalysisBlocked("BLOCKED_CONTEXT_SCHEMA", "unknown scanned Source ID")
    material_counts: dict[str, int] = {}
    for candidate in retained_candidates:
        source_id = str(candidate.get("source_id"))
        if source_id not in scanned_source_ids:
            raise AnalysisBlocked("BLOCKED_CONTEXT_SCHEMA", "material Source was not scanned")
        material_counts[source_id] = material_counts.get(source_id, 0) + 1
    for source_id in scanned_source_ids:
        row = by_id[source_id]
        row[SCAN_DATE_FIELD] = run_date.isoformat()
        if material_counts.get(source_id):
            row[MATERIAL_DATE_FIELD] = run_date.isoformat()
            row[MATERIAL_COUNT_FIELD] = int(row.get(MATERIAL_COUNT_FIELD, 0)) + material_counts[source_id]
    return result
