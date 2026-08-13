"""Verified Source scan state helper."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from datetime import date

from tools.periodic_source_analysis_contract import AnalysisBlocked


def update_operations_ledger(
    ledger: Mapping[str, object],
    scanned_source_ids: set[str],
    retained_candidates: Sequence[Mapping[str, object]],
    run_date: date,
) -> dict[str, object]:
    rows = ledger.get("sources")
    if ledger.get("schema_version") != 1 or not isinstance(rows, list):
        raise AnalysisBlocked("BLOCKED_CONTEXT_SCHEMA", "invalid operations Ledger")
    known_ids = {
        str(row.get("source_id"))
        for row in rows
        if isinstance(row, dict)
    }
    if not scanned_source_ids.issubset(known_ids):
        raise AnalysisBlocked("BLOCKED_CONTEXT_SCHEMA", "unknown scanned Source ID")
    del retained_candidates, run_date
    return dict(ledger)
