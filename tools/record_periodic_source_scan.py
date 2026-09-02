#!/usr/bin/env python3
"""Record verified periodic Source observations into the Operations Ledger."""

from __future__ import annotations

import argparse
import json
import sys
import tempfile
from datetime import date
from pathlib import Path
from typing import Any

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.periodic_source_receipt_state import (  # noqa: E402
    parse_active_discovery_seed_ids,
    reconcile_operations_ledger_from_receipts,
)


def _parse_ids(value: str) -> list[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


def _atomic_write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        newline="\n",
        dir=path.parent,
        delete=False,
        prefix=f".{path.stem}.",
        suffix=".tmp",
    ) as handle:
        json.dump(payload, handle, ensure_ascii=False, separators=(",", ":"))
        handle.write("\n")
        temporary = Path(handle.name)
    temporary.replace(path)


def _load_json(path: Path, *, label: str) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"invalid {label}: {path}") from exc


def record(
    path: Path,
    scan_date: str,
    source_ids: list[str],
    material_ids: list[str],
) -> None:
    """Preserve the legacy direct recorder interface."""

    parsed_date = date.fromisoformat(scan_date)
    if parsed_date.isoformat() != scan_date:
        raise ValueError("scan date must be canonical ISO date")
    payload = _load_json(path, label="operations Ledger JSON")
    if not isinstance(payload, dict):
        raise ValueError("ledger root must be an object")
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
    _atomic_write_json(path, payload)


def _load_receipt_corpus(
    path: Path,
) -> tuple[list[dict[str, object]], set[str]]:
    raw = _load_json(path, label="receipt corpus JSON")
    if isinstance(raw, list):
        entries = raw
        historical: list[object] = []
    elif isinstance(raw, dict):
        entries = raw.get("receipts")
        historical = raw.get("historical_discovery_seed_ids", [])
    else:
        raise ValueError("receipt corpus root must be a list or object")
    if not isinstance(entries, list) or any(not isinstance(row, dict) for row in entries):
        raise ValueError("receipt corpus receipts must be a list of objects")
    if not isinstance(historical, list) or any(
        not isinstance(item, str) or not item.strip() for item in historical
    ):
        raise ValueError("historical_discovery_seed_ids must be a string list")
    normalized_historical = {item.strip() for item in historical}
    if len(normalized_historical) != len(historical):
        raise ValueError("historical_discovery_seed_ids must not contain duplicates")
    return [dict(row) for row in entries], normalized_historical


def record_receipt_corpus(
    ledger_path: Path,
    receipt_corpus_path: Path,
    discovery_seed_path: Path,
    batch_date: str,
) -> None:
    parsed_batch_date = date.fromisoformat(batch_date)
    if parsed_batch_date.isoformat() != batch_date:
        raise ValueError("batch date must be canonical ISO date")
    ledger = _load_json(ledger_path, label="operations Ledger JSON")
    if not isinstance(ledger, dict):
        raise ValueError("ledger root must be an object")
    entries, historical_seed_ids = _load_receipt_corpus(receipt_corpus_path)
    try:
        discovery_text = discovery_seed_path.read_text(encoding="utf-8")
    except OSError as exc:
        raise ValueError(f"invalid discovery seed registry: {discovery_seed_path}") from exc
    current_seed_ids = parse_active_discovery_seed_ids(discovery_text)
    updated = reconcile_operations_ledger_from_receipts(
        ledger,
        entries,
        known_discovery_seed_ids=current_seed_ids,
        historical_discovery_seed_ids=historical_seed_ids,
        batch_date=parsed_batch_date,
    )
    _atomic_write_json(ledger_path, updated)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ledger", type=Path, required=True)
    parser.add_argument("--date")
    parser.add_argument("--sources")
    parser.add_argument("--material", default="")
    parser.add_argument("--receipt-corpus", type=Path)
    parser.add_argument("--discovery-seeds", type=Path)
    parser.add_argument("--batch-date")
    args = parser.parse_args(argv)

    receipt_mode = args.receipt_corpus is not None
    legacy_mode = args.date is not None or args.sources is not None
    if receipt_mode and legacy_mode:
        parser.error("receipt-corpus mode and legacy date/source mode are mutually exclusive")
    if receipt_mode:
        if args.discovery_seeds is None or args.batch_date is None:
            parser.error("receipt-corpus mode requires --discovery-seeds and --batch-date")
        record_receipt_corpus(
            args.ledger,
            args.receipt_corpus,
            args.discovery_seeds,
            args.batch_date,
        )
        return 0
    if args.date is None or args.sources is None:
        parser.error("legacy mode requires --date and --sources")
    if args.discovery_seeds is not None or args.batch_date is not None:
        parser.error("--discovery-seeds and --batch-date require --receipt-corpus")
    record(
        args.ledger,
        args.date,
        _parse_ids(args.sources),
        _parse_ids(args.material),
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
