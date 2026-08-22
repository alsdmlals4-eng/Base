#!/usr/bin/env python3
"""Record verified periodic source scans without rewriting unrelated ledger state."""
from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path


def _parse_ids(value: str) -> list[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


def record(path: Path, scan_date: str, source_ids: list[str], material_ids: list[str]) -> None:
    parsed_date = date.fromisoformat(scan_date)
    if parsed_date.isoformat() != scan_date:
        raise ValueError("scan date must be canonical ISO date")
    payload = json.loads(path.read_text(encoding="utf-8"))
    rows = payload.get("sources")
    if not isinstance(rows, list):
        raise ValueError("ledger sources must be a list")
    by_id = {row.get("source_id"): row for row in rows if isinstance(row, dict)}
    missing = sorted(set(source_ids + material_ids) - set(by_id))
    if missing:
        raise ValueError(f"unknown source ids: {', '.join(missing)}")
    for source_id in source_ids:
        row = by_id[source_id]
        if row.get("status") != "ACTIVE":
            raise ValueError(f"cannot record inactive source: {source_id}")
        row["last_successful_scan_at"] = scan_date
    for source_id in material_ids:
        row = by_id[source_id]
        if row.get("last_material_candidate_at") != scan_date:
            row["last_material_candidate_at"] = scan_date
            row["material_candidate_count_since_tracking_start"] = int(
                row.get("material_candidate_count_since_tracking_start") or 0
            ) + 1
    if "last_updated_at" in payload:
        payload["last_updated_at"] = scan_date
    path.write_text(json.dumps(payload, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ledger", type=Path, required=True)
    parser.add_argument("--date", required=True)
    parser.add_argument("--sources", required=True)
    parser.add_argument("--material", default="")
    args = parser.parse_args()
    record(args.ledger, args.date, _parse_ids(args.sources), _parse_ids(args.material))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
