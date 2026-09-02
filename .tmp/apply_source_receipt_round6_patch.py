from __future__ import annotations

from pathlib import Path


STATE = Path("tools/periodic_source_receipt_state.py")
ANALYSIS = Path("tools/periodic_source_analysis.py")


def replace_once(text: str, old: str, new: str, label: str) -> str:
    if text.count(old) != 1:
        raise SystemExit(f"{label} anchor missing or ambiguous: {text.count(old)}")
    return text.replace(old, new)


def patch_receipt_state() -> None:
    text = STATE.read_text(encoding="utf-8")

    text = replace_once(
        text,
        '''        if normalized_id not in scanned_sources:
            raise _blocked(
                "processed receipt material Source must be in durable scanned Sources"
            )
        counts[normalized_id] = raw_count
''',
        '''        if normalized_id not in scanned_sources:
            raise _blocked(
                "processed receipt material Source must be in durable scanned Sources"
            )
        if normalized_id in counts:
            raise _blocked(
                "duplicate normalized processed material Source"
            )
        counts[normalized_id] = raw_count
''',
        "processed material collision",
    )

    capture_anchor = '''def _capture_source_baseline(
    source_id: str, row: Mapping[str, object]
) -> dict[str, object]:
'''
    helper = '''def _validate_source_baseline_window(
    baseline: Mapping[str, object],
    *,
    tracking_started: date,
    upper_bound: date,
) -> None:
    for field, label in (
        ("scan_date", "baseline scan date"),
        ("material_date", "baseline material date"),
        ("base_contribution_date", "baseline Base contribution date"),
    ):
        raw_value = baseline.get(field)
        if raw_value is None:
            continue
        value = _parse_iso_date(raw_value, label)
        if value < tracking_started or value > upper_bound:
            raise _blocked(
                f"{label} must stay within operations Ledger tracking and batch dates"
            )


'''
    text = replace_once(
        text,
        capture_anchor,
        helper + capture_anchor,
        "baseline window helper",
    )

    text = replace_once(
        text,
        '''    raw_reconciliation_state = result.get(_RECONCILIATION_FIELD)
    if raw_reconciliation_state is not None:
        if not isinstance(raw_reconciliation_state, Mapping):
            raise _blocked("invalid receipt reconciliation state")
''',
        '''    reconciliation_state_present = _RECONCILIATION_FIELD in result
    raw_reconciliation_state = result.get(_RECONCILIATION_FIELD)
    if reconciliation_state_present:
        if raw_reconciliation_state is None:
            raise _blocked("receipt reconciliation state cannot be null")
        if not isinstance(raw_reconciliation_state, Mapping):
            raise _blocked("invalid receipt reconciliation state")
''',
        "null reconciliation state",
    )

    text = replace_once(
        text,
        '''    missing_baselined_sources = set(source_baselines) - set(ledger_sources)
    if missing_baselined_sources:
''',
        '''    if previous_batch is not None:
        for baseline in source_baselines.values():
            _validate_source_baseline_window(
                baseline,
                tracking_started=tracking_started,
                upper_bound=previous_batch,
            )

    missing_baselined_sources = set(source_baselines) - set(ledger_sources)
    if missing_baselined_sources:
''',
        "persisted baseline bounds",
    )

    text = replace_once(
        text,
        '''    for source_id, row in ledger_sources.items():
        if source_id not in source_baselines:
            source_baselines[source_id] = _capture_source_baseline(source_id, row)
        else:
''',
        '''    for source_id, row in ledger_sources.items():
        if source_id not in source_baselines:
            captured_baseline = _capture_source_baseline(source_id, row)
            _validate_source_baseline_window(
                captured_baseline,
                tracking_started=tracking_started,
                upper_bound=batch_date,
            )
            source_baselines[source_id] = captured_baseline
        else:
''',
        "captured baseline bounds",
    )

    old_duplicate = '''        if payload_sha in payload_to_effects:
            if _canonical_json(payload_to_effects[payload_sha]) != _canonical_json(
                identity_effects
            ):
                raise _blocked("conflicting duplicate receipt payload")
            processed_by_ref[receipt_ref] = _processed_row_for_receipt(
                receipt_ref, payload_sha, identity_effects
            )
            continue

        normalized = validate_actual_source_review_receipt(
            raw_receipt,
            result,
            known_discovery_seed_ids=current_seed_ids,
            historical_discovery_seed_ids=historical_seed_ids,
            source_state_at_scan=envelope["source_state_at_scan"],
            contribution_merge_dates=envelope["contribution_merge_dates"],
            batch_date=batch_date,
        )
'''
    new_duplicate = '''        normalized = validate_actual_source_review_receipt(
            raw_receipt,
            result,
            known_discovery_seed_ids=current_seed_ids,
            historical_discovery_seed_ids=historical_seed_ids,
            source_state_at_scan=envelope["source_state_at_scan"],
            contribution_merge_dates=envelope["contribution_merge_dates"],
            batch_date=batch_date,
        )
        if payload_sha in payload_to_effects:
            if _canonical_json(payload_to_effects[payload_sha]) != _canonical_json(
                identity_effects
            ):
                raise _blocked("conflicting duplicate receipt payload")
            processed_by_ref[receipt_ref] = _processed_row_for_receipt(
                receipt_ref, payload_sha, identity_effects
            )
            continue

'''
    text = replace_once(
        text,
        old_duplicate,
        new_duplicate,
        "order-independent duplicate payload validation",
    )

    STATE.write_text(text, encoding="utf-8")


def patch_analysis() -> None:
    text = ANALYSIS.read_text(encoding="utf-8")
    text = replace_once(
        text,
        '''    operations = load_ledger(operations_ledger_path)
    selected = select_due_source_batch(operations, run_date, batch_size)
''',
        '''    operations = load_ledger(operations_ledger_path)
    if "receipt_reconciliation_state" in operations:
        raise AnalysisBlocked(
            "BLOCKED_RECEIPT_RECONCILIATION_REQUIRED",
            "identity-enabled Operations Ledger must use reviewed receipt reconciliation before any model transport",
        )
    selected = select_due_source_batch(operations, run_date, batch_size)
''',
        "pre-transport identity guard",
    )
    ANALYSIS.write_text(text, encoding="utf-8")


def main() -> int:
    patch_receipt_state()
    patch_analysis()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
