"""Pending Source-site candidate state helper."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from datetime import date


def update_candidate_ledger(
    ledger: Mapping[str, object],
    new_sources: Sequence[Mapping[str, object]],
    run_date: date,
) -> dict[str, object]:
    del new_sources, run_date
    return dict(ledger)
