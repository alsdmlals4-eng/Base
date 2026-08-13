"""Source operations state helper."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from datetime import date


def update_operations_ledger(
    ledger: Mapping[str, object],
    scanned_source_ids: set[str],
    retained_candidates: Sequence[Mapping[str, object]],
    run_date: date,
) -> dict[str, object]:
    del scanned_source_ids, retained_candidates, run_date
    return dict(ledger)
