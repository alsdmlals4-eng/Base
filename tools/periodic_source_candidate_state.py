"""Pending unverified Source-site candidate state."""

from __future__ import annotations

import copy
import hashlib
from collections.abc import Mapping, Sequence
from datetime import date

from tools.periodic_source_analysis_contract import (
    AnalysisBlocked,
    SOURCE_ROLES,
    enum_value,
    non_empty,
    normalize_url,
)

CANDIDATE_STATUSES = {"UNVERIFIED_DISCOVERY", "PROMOTION_CANDIDATE", "REJECTED"}


def update_candidate_ledger(
    ledger: Mapping[str, object],
    new_sources: Sequence[Mapping[str, object]],
    run_date: date,
) -> dict[str, object]:
    result = copy.deepcopy(dict(ledger))
    if (
        result.get("schema_version") != 1
        or result.get("ledger_role") != "periodic-unverified-source-candidates"
        or result.get("authority") != "UNVERIFIED_DISCOVERY_ONLY"
    ):
        raise AnalysisBlocked("BLOCKED_CONTEXT_SCHEMA", "invalid candidate Ledger authority")
    rows = result.get("candidates")
    if not isinstance(rows, list):
        raise AnalysisBlocked("BLOCKED_CONTEXT_SCHEMA", "candidate Ledger rows missing")
    by_key: dict[str, dict[str, object]] = {}
    for row in rows:
        if not isinstance(row, dict):
            raise AnalysisBlocked("BLOCKED_CONTEXT_SCHEMA", "candidate Ledger row must be an object")
        fingerprint = non_empty(row.get("fingerprint"), "fingerprint", "BLOCKED_CONTEXT_SCHEMA")
        if fingerprint in by_key:
            raise AnalysisBlocked("BLOCKED_CONTEXT_SCHEMA", "duplicate candidate fingerprint")
        if row.get("status") not in CANDIDATE_STATUSES:
            raise AnalysisBlocked("BLOCKED_CONTEXT_SCHEMA", "invalid candidate status")
        normalize_url(row.get("url"))
        by_key[fingerprint] = row
    for source in new_sources:
        name = non_empty(source.get("name"), "name", "BLOCKED_CONTEXT_SCHEMA")
        url = normalize_url(source.get("url"))
        fingerprint = hashlib.sha256(f"{name.casefold()}\n{url}".encode("utf-8")).hexdigest()
        existing = by_key.get(fingerprint)
        if existing is None:
            existing = {
                "candidate_id": f"source-{fingerprint[:16]}",
                "fingerprint": fingerprint,
                "name": name,
                "domain": non_empty(source.get("domain"), "domain", "BLOCKED_CONTEXT_SCHEMA"),
                "url": url,
                "source_role": enum_value(
                    source.get("source_role"), SOURCE_ROLES, "source_role", "BLOCKED_CONTEXT_SCHEMA"
                ),
                "reason": non_empty(source.get("reason"), "reason", "BLOCKED_CONTEXT_SCHEMA"),
                "first_seen_at": run_date.isoformat(),
                "last_seen_at": run_date.isoformat(),
                "seen_count": 1,
                "status": "UNVERIFIED_DISCOVERY",
            }
            rows.append(existing)
            by_key[fingerprint] = existing
        else:
            existing["last_seen_at"] = run_date.isoformat()
            existing["seen_count"] = int(existing.get("seen_count", 0)) + 1
    rows.sort(key=lambda row: (str(row.get("status")), str(row.get("name")), str(row.get("url"))))
    return result
