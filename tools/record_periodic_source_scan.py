#!/usr/bin/env python3
"""Record verified periodic source scans without rewriting unrelated ledger state."""
from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path

from tools.periodic_source_operations_state import reconcile_operations_ledger_from_receipts


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


def _load_json_object(path: Path, label: str) -> dict[str, object]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError(f"invalid {label} JSON: {path}") from error
    if not isinstance(payload, dict):
        raise ValueError(f"{label} JSON root must be an object")
    return payload


def record_receipt_corpus(ledger_path: Path, receipt_corpus_path: Path) -> None:
    """Validate a trusted receipt corpus and reconcile the reviewed weekly Ledger."""

    ledger = _load_json_object(ledger_path, "operations Ledger")
    corpus = _load_json_object(receipt_corpus_path, "receipt corpus")
    receipts = corpus.get("receipts")
    if not isinstance(receipts, list):
        raise ValueError("receipt corpus receipts must be a list")
    reconciled = reconcile_operations_ledger_from_receipts(ledger, receipts)
    ledger_path.write_text(
        json.dumps(reconciled, ensure_ascii=False, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ledger", type=Path, required=True)
    parser.add_argument("--receipt-corpus", type=Path)
    parser.add_argument("--date")
    parser.add_argument("--sources")
    parser.add_argument("--material", default="")
    args = parser.parse_args(argv)
    if args.receipt_corpus is not None:
        if args.date is not None or args.sources is not None or args.material:
            parser.error("--receipt-corpus cannot be combined with --date/--sources/--material")
        record_receipt_corpus(args.ledger, args.receipt_corpus)
        return 0
    if args.date is None or args.sources is None:
        parser.error("--date and --sources are required without --receipt-corpus")
    record(args.ledger, args.date, _parse_ids(args.sources), _parse_ids(args.material))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
