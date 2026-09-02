from __future__ import annotations

from pathlib import Path


PATH = Path("tools/periodic_source_receipt_state.py")


def replace_once(text: str, old: str, new: str, label: str) -> str:
    if text.count(old) != 1:
        raise SystemExit(f"{label} anchor missing or ambiguous")
    return text.replace(old, new)


def main() -> int:
    text = PATH.read_text(encoding="utf-8")

    text = replace_once(
        text,
        '''def _validate_source_classification(
    *,
    scanned_source_ids: Sequence[str],
    scanned_discovery_seed_ids: Sequence[str],
    ledger_sources: Mapping[str, Mapping[str, object]],
    known_discovery_seed_ids: set[str],
    historical_discovery_seed_ids: set[str],
    source_state_at_scan: Mapping[str, str],
) -> None:
''',
        '''def _validate_source_classification(
    *,
    scanned_source_ids: Sequence[str],
    scanned_discovery_seed_ids: Sequence[str],
    ledger_sources: Mapping[str, Mapping[str, object]],
    known_discovery_seed_ids: set[str],
    historical_discovery_seed_ids: set[str],
    source_state_at_scan: Mapping[str, str],
    validate_current_source_state: bool,
) -> None:
''',
        "classification signature",
    )

    text = replace_once(
        text,
        '''        if stated is not None and stated != "DURABLE_ACTIVE":
            raise _blocked(
                "receipt-time classification contradicts durable lane"
            )
        row = ledger_sources.get(source_id)
''',
        '''        if stated is not None and stated != "DURABLE_ACTIVE":
            raise _blocked(
                "receipt-time classification contradicts durable lane"
            )
        if not validate_current_source_state:
            continue
        row = ledger_sources.get(source_id)
''',
        "durable classification",
    )

    text = replace_once(
        text,
        '''        if stated is not None and stated != "DISCOVERY_ACTIVE":
            raise _blocked(
                "receipt-time classification contradicts discovery lane"
            )
        if seed_id in known_discovery_seed_ids and seed_id not in ledger_sources:
''',
        '''        if stated is not None and stated != "DISCOVERY_ACTIVE":
            raise _blocked(
                "receipt-time classification contradicts discovery lane"
            )
        if not validate_current_source_state:
            continue
        if seed_id in known_discovery_seed_ids and seed_id not in ledger_sources:
''',
        "discovery classification",
    )

    text = replace_once(
        text,
        '''    if validate_current_source_state:
        _validate_source_classification(
            scanned_source_ids=scanned_sources,
            scanned_discovery_seed_ids=scanned_discovery,
            ledger_sources=ledger_sources,
            known_discovery_seed_ids=current_discovery,
            historical_discovery_seed_ids=historical_discovery,
            source_state_at_scan=classification,
        )
''',
        '''    _validate_source_classification(
        scanned_source_ids=scanned_sources,
        scanned_discovery_seed_ids=scanned_discovery,
        ledger_sources=ledger_sources,
        known_discovery_seed_ids=current_discovery,
        historical_discovery_seed_ids=historical_discovery,
        source_state_at_scan=classification,
        validate_current_source_state=validate_current_source_state,
    )
''',
        "classification call",
    )

    text = replace_once(
        text,
        '''        identity_payload = {
            "actual_source_review_receipt": identity_receipt,
            "source_state_at_scan": envelope["source_state_at_scan"],
            "contribution_merge_dates": envelope["contribution_merge_dates"],
        }
        payload_sha = _payload_hash(identity_payload)
''',
        '''        # Envelope fields validate provenance and historical lane context.
        # Their effective values are already folded into identity_receipt, so
        # redundant explicit maps must not create a second material event.
        payload_sha = _payload_hash(identity_receipt)
''',
        "semantic receipt identity",
    )

    PATH.write_text(text, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
