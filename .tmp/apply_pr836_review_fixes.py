from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "tools" / "periodic_source_receipt_state.py"
RECORDER = ROOT / "tools" / "record_periodic_source_scan.py"


def replace_once(text: str, old: str, new: str, label: str) -> str:
    if text.count(old) != 1:
        raise SystemExit(f"{label} anchor missing or ambiguous: {text.count(old)}")
    return text.replace(old, new)


def patch_state() -> None:
    text = STATE.read_text(encoding="utf-8")

    text = replace_once(
        text,
        '''        if state not in _SOURCE_CLASSIFICATIONS:
            raise _blocked("invalid source_state_at_scan classification")
        result[source_id] = state
''',
        '''        if state not in _SOURCE_CLASSIFICATIONS:
            raise _blocked("invalid source_state_at_scan classification")
        if source_id in result:
            raise _blocked(
                "duplicate normalized source_state_at_scan Source ID"
            )
        result[source_id] = state
''',
        "normalized source-state collision",
    )

    text = replace_once(
        text,
        '''    for match in seed_pattern.finditer(loose_text):
        seed_id = match.group(1)
        if seed_id in seen:
            raise _blocked("duplicate discovery seed ID")
        seen.add(seed_id)
        active.add(seed_id)
''',
        '''    loose_seed_matches = list(seed_pattern.finditer(loose_text))
    for index, match in enumerate(loose_seed_matches):
        seed_id = match.group(1)
        if seed_id in seen:
            raise _blocked("duplicate discovery seed ID")
        seen.add(seed_id)
        segment_end = (
            loose_seed_matches[index + 1].start()
            if index + 1 < len(loose_seed_matches)
            else len(loose_text)
        )
        record = loose_text[match.start() : segment_end]
        status_matches = status_pattern.findall(record)
        if len(status_matches) > 1:
            raise _blocked("discovery seed record contains multiple status values")
        if not status_matches or status_matches[0] == "ACTIVE_DISCOVERY_SEED":
            active.add(seed_id)
''',
        "loose discovery seed status",
    )

    text = replace_once(
        text,
        '''    result: list[dict[str, object]] = []
    for raw in value:
''',
        '''    result: list[dict[str, object]] = []
    seen_rows: set[str] = set()
    for raw in value:
''',
        "high nutrient seen set",
    )

    text = replace_once(
        text,
        '''        row.update(
            source=source_name,
            nutrient_score=score,
            source_archetype=archetype,
            reusable_units=reusable_units,
        )
        result.append(row)
''',
        '''        row.update(
            source=source_name,
            nutrient_score=score,
            source_archetype=archetype,
            reusable_units=reusable_units,
        )
        canonical_row = _canonical_json(row)
        if canonical_row in seen_rows:
            raise _blocked("duplicate high-nutrient source row")
        seen_rows.add(canonical_row)
        result.append(row)
''',
        "high nutrient duplicate guard",
    )

    text = replace_once(
        text,
        '''    _, ledger_sources = _known_ledger_sources(ledger)
    current_discovery = set(known_discovery_seed_ids or set())
''',
        '''    _, ledger_sources = _known_ledger_sources(ledger)
    tracking_started = _parse_iso_date(
        ledger.get("tracking_started_at"), "tracking_started_at"
    )
    current_discovery = set(known_discovery_seed_ids or set())
''',
        "receipt tracking start",
    )

    text = replace_once(
        text,
        '''            if merge_date > batch_date:
                raise _blocked("contribution merge_date cannot be after batch_date")
''',
        '''            if merge_date > batch_date:
                raise _blocked("contribution merge_date cannot be after batch_date")
            if merge_date < tracking_started:
                raise _blocked(
                    "contribution merge_date predates operations Ledger tracking start"
                )
''',
        "incoming pretracking contribution",
    )

    text = replace_once(
        text,
        '''    if previous_batch is not None and batch_date < previous_batch:
        raise _blocked("batch_date cannot move backwards")

    missing_baselined_sources = set(source_baselines) - set(ledger_sources)
''',
        '''    if previous_batch is not None and batch_date < previous_batch:
        raise _blocked("batch_date cannot move backwards")
    if previous_batch is not None:
        for persisted_receipt in processed_by_ref.values():
            persisted_scan_date = _parse_iso_date(
                persisted_receipt["scan_date"],
                "processed receipt scan_date",
            )
            if persisted_scan_date > previous_batch:
                raise _blocked(
                    "processed receipt scan_date cannot follow last_batch_date"
                )
        for persisted_contribution in processed_contributions.values():
            persisted_merge_date = _parse_iso_date(
                persisted_contribution["merge_date"],
                "processed contribution merge_date",
            )
            if persisted_merge_date > previous_batch:
                raise _blocked(
                    "processed contribution merge_date cannot follow last_batch_date"
                )
            if persisted_merge_date < tracking_started:
                raise _blocked(
                    "processed contribution merge_date predates operations Ledger tracking start"
                )

    missing_baselined_sources = set(source_baselines) - set(ledger_sources)
''',
        "persisted event date bounds",
    )

    text = replace_once(
        text,
        '''        payload_to_effects[payload_sha] = effects

    # Rebuild every derived row from its immutable baseline plus each unique payload.
''',
        '''        payload_to_effects[payload_sha] = effects

    receipt_contribution_keys = {
        contribution_key
        for processed_receipt in processed_by_ref.values()
        for contribution_key in processed_receipt["contribution_keys"]
    }
    orphan_contributions = set(processed_contributions) - receipt_contribution_keys
    if orphan_contributions:
        raise _blocked(
            "processed contribution is not linked by a processed receipt: "
            + ", ".join(sorted(orphan_contributions))
        )
    missing_contribution_metadata = (
        receipt_contribution_keys - set(processed_contributions)
    )
    if missing_contribution_metadata:
        raise _blocked(
            "processed receipt contribution metadata is missing: "
            + ", ".join(sorted(missing_contribution_metadata))
        )

    contributions_by_source_date: dict[tuple[str, str], set[str]] = {}
    for metadata in processed_contributions.values():
        grouping_key = (
            str(metadata["source_id"]),
            str(metadata["merge_date"]),
        )
        contributions_by_source_date.setdefault(grouping_key, set()).add(
            str(metadata["merge_sha"])
        )
    ambiguous_same_day = [
        f"{source_id}@{merge_date}"
        for (source_id, merge_date), merge_shas in contributions_by_source_date.items()
        if len(merge_shas) > 1
    ]
    if ambiguous_same_day:
        raise _blocked(
            "same-day contributions require chronological evidence: "
            + ", ".join(sorted(ambiguous_same_day))
        )

    # Rebuild every derived row from its immutable baseline plus each unique payload.
''',
        "contribution linkage and chronology",
    )

    text = replace_once(
        text,
        '''        source_contributions = [
            metadata
            for key, metadata in processed_contributions.items()
            if key.startswith(f"{source_id}:")
        ]
''',
        '''        source_contributions = [
            metadata
            for metadata in processed_contributions.values()
            if str(metadata["source_id"]) == source_id
        ]
''',
        "exact contribution source matching",
    )

    STATE.write_text(text, encoding="utf-8")


def patch_recorder() -> None:
    text = RECORDER.read_text(encoding="utf-8")
    text = replace_once(
        text,
        '''import json
import sys
import tempfile
''',
        '''import json
import stat
import sys
import tempfile
''',
        "stat import",
    )
    text = replace_once(
        text,
        '''def _atomic_write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
''',
        '''def _atomic_write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    existing_mode = (
        stat.S_IMODE(path.stat().st_mode) if path.exists() else None
    )
    with tempfile.NamedTemporaryFile(
''',
        "existing mode capture",
    )
    text = replace_once(
        text,
        '''        handle.write("\\n")
        temporary = Path(handle.name)
    temporary.replace(path)
''',
        '''        handle.write("\\n")
        temporary = Path(handle.name)
    if existing_mode is not None:
        temporary.chmod(existing_mode)
    temporary.replace(path)
''',
        "existing mode restore",
    )
    RECORDER.write_text(text, encoding="utf-8")


def main() -> int:
    patch_state()
    patch_recorder()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
