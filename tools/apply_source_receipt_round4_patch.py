from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "tools" / "periodic_source_receipt_state.py"
OPERATIONS = ROOT / "tools" / "periodic_source_operations_state.py"


def replace_once(text: str, old: str, new: str, label: str) -> str:
    if text.count(old) != 1:
        raise SystemExit(f"{label} anchor missing or ambiguous")
    return text.replace(old, new)


def patch_state() -> None:
    source = STATE.read_text(encoding="utf-8")

    parser_pattern = re.compile(
        r"def parse_active_discovery_seed_ids\(text: str\) -> set\[str\]:\n.*?\n\ndef _existing_material_state",
        re.DOTALL,
    )
    parser_replacement = '''def parse_active_discovery_seed_ids(text: str) -> set[str]:
    if not isinstance(text, str):
        raise _blocked("discovery seed registry must be text")

    active: set[str] = set()
    seen: set[str] = set()
    fenced_ranges: list[tuple[int, int]] = []
    seed_pattern = re.compile(
        r"(?m)^seed_id:\\s*([A-Za-z0-9][A-Za-z0-9._-]*)\\s*$"
    )
    status_pattern = re.compile(r"(?m)^status:\\s*([^\\s#]+)\\s*$")

    for block in re.finditer(r"(?ms)^```yaml\\s*\\n(.*?)^```\\s*$", text):
        fenced_ranges.append(block.span())
        body = block.group(1)
        seed_matches = list(seed_pattern.finditer(body))
        for index, match in enumerate(seed_matches):
            seed_id = match.group(1)
            if seed_id in seen:
                raise _blocked("duplicate discovery seed ID")
            seen.add(seed_id)
            segment_end = (
                seed_matches[index + 1].start()
                if index + 1 < len(seed_matches)
                else len(body)
            )
            record = body[match.start() : segment_end]
            status_matches = status_pattern.findall(record)
            if len(status_matches) > 1:
                raise _blocked("discovery seed record contains multiple status values")
            if not status_matches or status_matches[0] == "ACTIVE_DISCOVERY_SEED":
                active.add(seed_id)

    loose_text = text
    for start, end in reversed(fenced_ranges):
        loose_text = (
            loose_text[:start]
            + ("\\n" * text[start:end].count("\\n"))
            + loose_text[end:]
        )
    for match in seed_pattern.finditer(loose_text):
        seed_id = match.group(1)
        if seed_id in seen:
            raise _blocked("duplicate discovery seed ID")
        seen.add(seed_id)
        active.add(seed_id)

    if not active:
        raise _blocked("discovery seed registry contains no active seed_id entries")
    return active


def _existing_material_state'''
    source, count = parser_pattern.subn(parser_replacement, source)
    if count != 1:
        raise SystemExit("discovery seed parser anchor missing or ambiguous")

    source = replace_once(
        source,
        '''    if not scanned_sources and not scanned_discovery:
        raise _blocked("receipt must identify an actually reviewed Source")
    unused_classifications = set(classification) - (
''',
        '''    if not scanned_sources and not scanned_discovery:
        raise _blocked("receipt must identify an actually reviewed Source")
    if set(scanned_sources) & set(scanned_discovery):
        raise _blocked("one Source ID cannot appear in both scanned Source lanes")
    unused_classifications = set(classification) - (
''',
        "disjoint source lanes",
    )

    source = replace_once(
        source,
        '''def _receipt_entry_envelope(entry: Mapping[str, object]) -> dict[str, object]:
    return {
        "source_state_at_scan": _normalize_source_state_at_scan(
            entry.get("source_state_at_scan")
        ),
        "contribution_merge_dates": _normalize_merge_date_map(
            entry.get("contribution_merge_dates")
        ),
    }
''',
        '''def _receipt_entry_envelope(entry: Mapping[str, object]) -> dict[str, object]:
    allowed = {
        "receipt_ref",
        "actual_source_review_receipt",
        "source_state_at_scan",
        "contribution_merge_dates",
    }
    unsupported = set(entry) - allowed
    if unsupported:
        raise _blocked(
            "unsupported receipt entry fields: " + ", ".join(sorted(unsupported))
        )
    return {
        "source_state_at_scan": _normalize_source_state_at_scan(
            entry.get("source_state_at_scan")
        ),
        "contribution_merge_dates": _normalize_merge_date_map(
            entry.get("contribution_merge_dates")
        ),
    }
''',
        "receipt envelope",
    )

    source = replace_once(
        source,
        '''    result, ledger_sources = _known_ledger_sources(ledger)
    tracking_started = _parse_iso_date(
        result.get("tracking_started_at"), "tracking_started_at"
    )
    current_seed_ids = set(known_discovery_seed_ids or set())
''',
        '''    result, ledger_sources = _known_ledger_sources(ledger)
    tracking_started = _parse_iso_date(
        result.get("tracking_started_at"), "tracking_started_at"
    )
    raw_reconciliation_state = result.get(_RECONCILIATION_FIELD)
    if raw_reconciliation_state is not None:
        if not isinstance(raw_reconciliation_state, Mapping):
            raise _blocked("invalid receipt reconciliation state")
        persisted_tracking_start = _parse_iso_date(
            raw_reconciliation_state.get("tracking_started_at"),
            "reconciliation tracking_started_at",
        )
        if persisted_tracking_start != tracking_started:
            raise _blocked("tracking_started_at changed after reconciliation began")
    current_seed_ids = set(known_discovery_seed_ids or set())
''',
        "tracking start",
    )

    source = replace_once(
        source,
        '''    for source_id, row in ledger_sources.items():
        if source_id not in source_baselines:
            source_baselines[source_id] = _capture_source_baseline(source_id, row)
        else:
            _validate_current_row_against_baseline(
                source_id, row, source_baselines[source_id]
            )
''',
        '''    missing_baselined_sources = set(source_baselines) - set(ledger_sources)
    if missing_baselined_sources:
        raise _blocked(
            "baselined Source ID disappeared without identity migration: "
            + ", ".join(sorted(missing_baselined_sources))
        )
    for source_id, row in ledger_sources.items():
        if source_id not in source_baselines:
            source_baselines[source_id] = _capture_source_baseline(source_id, row)
        else:
            _validate_current_row_against_baseline(
                source_id, row, source_baselines[source_id]
            )
''',
        "baseline source membership",
    )

    source = replace_once(
        source,
        '''    result[_RECONCILIATION_FIELD] = {
        "schema_version": _RECONCILIATION_SCHEMA_VERSION,
        "identity_floor_date": identity_floor.isoformat(),
''',
        '''    result[_RECONCILIATION_FIELD] = {
        "schema_version": _RECONCILIATION_SCHEMA_VERSION,
        "tracking_started_at": tracking_started.isoformat(),
        "identity_floor_date": identity_floor.isoformat(),
''',
        "reconciliation output tracking start",
    )

    STATE.write_text(source, encoding="utf-8")


def patch_operations() -> None:
    source = OPERATIONS.read_text(encoding="utf-8")
    source = replace_once(
        source,
        '''    result = copy.deepcopy(dict(ledger))
    rows = result.get("sources")
''',
        '''    if "receipt_reconciliation_state" in ledger:
        raise AnalysisBlocked(
            "BLOCKED_RECEIPT_RECONCILIATION_REQUIRED",
            "identity-enabled Operations Ledger must mutate through the receipt reconciler",
        )
    result = copy.deepcopy(dict(ledger))
    rows = result.get("sources")
''',
        "shared operations updater guard",
    )
    OPERATIONS.write_text(source, encoding="utf-8")


def main() -> int:
    patch_state()
    patch_operations()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
