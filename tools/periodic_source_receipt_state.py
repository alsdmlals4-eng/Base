"""Validate Source review receipts and reconcile reviewed Ledger observations."""

from __future__ import annotations

import copy
import json
import re
from collections.abc import Mapping, Sequence
from datetime import date

from tools.periodic_source_analysis_contract import AnalysisBlocked

from tools.periodic_source_operations_state import (
    MATERIAL_COUNT_FIELD,
    MATERIAL_DATE_FIELD,
    SCAN_DATE_FIELD,
)

_ALLOWED_DISPOSITIONS = {"NO_CHANGE", "MATERIAL_CHANGE", "BLOCKED_UNVERIFIED"}
_LEDGER_WRITE = "DEFER_TO_WEEKLY_SCAN_STATE_BATCH"
_SHA_RE = re.compile(r"[0-9a-fA-F]{40}")
_BASE_DATE_FIELD = "last_base_contribution_at"
_BASE_REF_FIELD = "last_base_contribution_ref"
_BASE_COUNT_FIELD = "base_contribution_count_since_tracking_start"


def _blocked(detail: str) -> AnalysisBlocked:
    return AnalysisBlocked("BLOCKED_CONTEXT_SCHEMA", detail)


def _parse_iso_date(value: object, field: str) -> date:
    if not isinstance(value, str) or not value:
        raise _blocked(f"{field} must be an ISO date")
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise _blocked(f"{field} must be an ISO date") from exc


def _require_sha(value: object, field: str) -> str:
    if not isinstance(value, str) or _SHA_RE.fullmatch(value) is None:
        raise _blocked(f"{field} must be a 40-character commit SHA")
    return value.lower()


def _string_list(value: object, field: str) -> list[str]:
    if not isinstance(value, list) or any(not isinstance(item, str) or not item for item in value):
        raise _blocked(f"{field} must be a list of non-empty strings")
    if len(value) != len(set(value)):
        raise _blocked(f"{field} must not contain duplicates")
    return list(value)


def _normalize_pr_number(value: object) -> int | None:
    if value is None:
        return None
    if isinstance(value, bool):
        raise _blocked("pr_created must be a positive pull request number or null")
    if isinstance(value, int):
        number = value
    elif isinstance(value, str):
        text = value.strip()
        if text.startswith("#"):
            text = text[1:]
        if not text.isdecimal():
            raise _blocked("pr_created must be a positive pull request number or null")
        number = int(text)
    else:
        raise _blocked("pr_created must be a positive pull request number or null")
    if number <= 0:
        raise _blocked("pr_created must be a positive pull request number or null")
    return number


def _normalize_contribution_refs(
    value: object,
    retained_source_ids: Sequence[str],
    receipt_pr: int | None,
    receipt_merge_sha: str | None,
) -> list[dict[str, object]]:
    if not isinstance(value, list):
        raise _blocked("merged_base_contribution_refs must be a list")
    if not value:
        return []

    if all(isinstance(item, str) for item in value):
        refs = _string_list(value, "merged_base_contribution_refs")
        if len(retained_source_ids) != 1:
            raise _blocked("legacy contribution refs require one retained Source")
        if receipt_pr is None or receipt_merge_sha is None:
            raise _blocked("legacy contribution refs require receipt PR and merge SHA")
        return [{
            "source_id": retained_source_ids[0],
            "pr": receipt_pr,
            "merge_sha": receipt_merge_sha,
            "refs": refs,
        }]

    if not all(isinstance(item, Mapping) for item in value):
        raise _blocked("merged Base contribution refs must use one consistent format")

    normalized: list[dict[str, object]] = []
    seen: set[tuple[str, str]] = set()
    for item in value:
        assert isinstance(item, Mapping)
        source_id = item.get("source_id", item.get("source"))
        if not isinstance(source_id, str) or not source_id:
            raise _blocked("contribution Source must be a non-empty string")
        if source_id not in retained_source_ids:
            raise _blocked("contribution Source must be retained")

        item_pr = _normalize_pr_number(item.get("pr", receipt_pr))
        if item_pr is None:
            raise _blocked("contribution ref requires a pull request number")
        if receipt_pr is not None and item_pr != receipt_pr:
            raise _blocked("contribution PR does not match receipt PR")

        item_merge_sha = _require_sha(
            item.get("merge_sha", receipt_merge_sha), "contribution merge_sha"
        )
        if receipt_merge_sha is not None and item_merge_sha != receipt_merge_sha:
            raise _blocked("contribution merge SHA does not match receipt merge SHA")

        key = (source_id, item_merge_sha)
        if key in seen:
            raise _blocked("duplicate merged Base contribution")
        seen.add(key)
        row: dict[str, object] = {
            "source_id": source_id,
            "pr": item_pr,
            "merge_sha": item_merge_sha,
        }
        owner = item.get("owner")
        if owner is not None:
            if not isinstance(owner, str) or not owner:
                raise _blocked("contribution owner must be a non-empty string")
            row["owner"] = owner
        refs = item.get("refs")
        if refs is not None:
            row["refs"] = _string_list(refs, "contribution refs")
        normalized.append(row)
    return normalized


def _existing_material_state(row: Mapping[str, object]) -> tuple[int, date | None]:
    count = row.get(MATERIAL_COUNT_FIELD, 0)
    date_value = row.get(MATERIAL_DATE_FIELD)
    if isinstance(count, bool) or not isinstance(count, int) or count < 0:
        raise _blocked("invalid existing material candidate count")
    event_date = (
        None
        if date_value is None
        else _parse_iso_date(date_value, MATERIAL_DATE_FIELD)
    )
    if (count == 0) != (event_date is None):
        raise _blocked("existing material candidate state is inconsistent")
    return count, event_date


def _existing_base_contribution_state(
    row: Mapping[str, object],
) -> tuple[int, date | None, str | None]:
    count = row.get(_BASE_COUNT_FIELD, 0)
    date_value = row.get(_BASE_DATE_FIELD)
    reference = row.get(_BASE_REF_FIELD)
    if isinstance(count, bool) or not isinstance(count, int) or count < 0:
        raise _blocked("invalid existing Base contribution count")
    event_date = (
        None
        if date_value is None
        else _parse_iso_date(date_value, _BASE_DATE_FIELD)
    )
    if reference is not None and (
        not isinstance(reference, str) or _SHA_RE.fullmatch(reference) is None
    ):
        raise _blocked("invalid existing Base contribution ref")
    empty = count == 0 and event_date is None and reference is None
    populated = count > 0 and event_date is not None and reference is not None
    if not (empty or populated):
        raise _blocked("existing Base contribution state is inconsistent")
    return count, event_date, reference


def _known_ledger_source_ids(ledger: Mapping[str, object]) -> tuple[dict[str, object], set[str]]:
    result = copy.deepcopy(dict(ledger))
    rows = result.get("sources")
    if result.get("schema_version") != 1 or not isinstance(rows, list):
        raise _blocked("invalid operations Ledger")
    known_ids: set[str] = set()
    for row in rows:
        if not isinstance(row, dict):
            raise _blocked("invalid operations Ledger Source row")
        source_id = row.get("source_id")
        if not isinstance(source_id, str) or not source_id or source_id in known_ids:
            raise _blocked("invalid or duplicate operations Ledger Source ID")
        _existing_material_state(row)
        _existing_base_contribution_state(row)
        known_ids.add(source_id)
    return result, known_ids


def validate_actual_source_review_receipt(
    receipt: Mapping[str, object],
    ledger: Mapping[str, object],
) -> dict[str, object]:
    """Validate and normalize one machine-readable actual Source review receipt.

    The receipt records Source identities, not Candidate Packet identities. Newly
    discovered Sources may remain represented by the discovery seed that actually
    produced the retained Candidate Packet until they receive a durable Ledger ID.
    """

    if not isinstance(receipt, Mapping):
        raise _blocked("actual Source review receipt must be an object")
    checked = copy.deepcopy(dict(receipt))
    checked_ledger, known_source_ids = _known_ledger_source_ids(ledger)

    checked["scan_date"] = _parse_iso_date(
        checked.get("scan_date"), "scan_date"
    ).isoformat()
    checked["start_main"] = _require_sha(checked.get("start_main"), "start_main")
    checked["final_main"] = _require_sha(checked.get("final_main"), "final_main")

    disposition = checked.get("disposition")
    if disposition not in _ALLOWED_DISPOSITIONS:
        raise _blocked("invalid actual Source review disposition")

    scanned_source_ids = _string_list(checked.get("scanned_source_ids"), "scanned_source_ids")
    checked["scanned_source_ids"] = scanned_source_ids
    unknown_scanned = set(scanned_source_ids) - known_source_ids
    if unknown_scanned:
        raise _blocked("unknown scanned Source ID")
    rows = checked_ledger["sources"]
    assert isinstance(rows, list)
    inactive_scanned = {
        str(row["source_id"])
        for row in rows
        if isinstance(row, dict)
        and row["source_id"] in scanned_source_ids
        and row.get("status") != "ACTIVE"
    }
    if inactive_scanned:
        raise _blocked("cannot record inactive Source")
    discovery_seed_ids = _string_list(
        checked.get("scanned_discovery_seed_ids"), "scanned_discovery_seed_ids"
    )
    if set(discovery_seed_ids) & known_source_ids:
        raise _blocked("durable Source ID must use scanned_source_ids")
    if not scanned_source_ids and not discovery_seed_ids:
        raise _blocked("receipt must identify an actually reviewed Source")
    retained_source_ids = _string_list(
        checked.get("retained_candidate_source_ids"), "retained_candidate_source_ids"
    )
    checked["scanned_discovery_seed_ids"] = discovery_seed_ids
    checked["retained_candidate_source_ids"] = retained_source_ids
    allowed_retained_ids = set(scanned_source_ids) | set(discovery_seed_ids)
    unknown_retained = set(retained_source_ids) - allowed_retained_ids
    if unknown_retained:
        raise _blocked("unknown retained Candidate Source ID")

    counts = checked.get("material_candidate_count_by_source")
    if not isinstance(counts, dict):
        raise _blocked("material_candidate_count_by_source must be an object")
    if set(counts) != set(retained_source_ids):
        raise _blocked("material candidate Source IDs do not match retained Sources")
    normalized_counts: dict[str, int] = {}
    for source_id, count in counts.items():
        if isinstance(count, bool) or not isinstance(count, int) or count <= 0:
            raise _blocked("material candidate counts must be positive integers")
        normalized_counts[str(source_id)] = count
    checked["material_candidate_count_by_source"] = normalized_counts

    high_nutrient_sources = checked.get("high_nutrient_sources", [])
    if not isinstance(high_nutrient_sources, list):
        raise _blocked("high_nutrient_sources must be a list")
    checked["high_nutrient_sources"] = high_nutrient_sources
    for row in high_nutrient_sources:
        if not isinstance(row, dict):
            raise _blocked("high_nutrient_sources rows must be objects")
        source_name = row.get("source")
        archetype = row.get("source_archetype")
        score = row.get("nutrient_score")
        reusable_units = row.get("reusable_units")
        if not isinstance(source_name, str) or not source_name:
            raise _blocked("high-nutrient source must be non-empty")
        if isinstance(score, bool) or not isinstance(score, int) or not 9 <= score <= 12:
            raise _blocked("high-nutrient score must be 9..12")
        if not isinstance(archetype, str) or not archetype:
            raise _blocked("high-nutrient source archetype must be non-empty")
        _string_list(reusable_units, "high-nutrient reusable_units")

    checked["unverified_scope"] = _string_list(
        checked.get("unverified_scope"), "unverified_scope"
    )
    repository_change = checked.get("repository_change")
    if not isinstance(repository_change, str) or not repository_change:
        raise _blocked("repository_change must be a non-empty string")
    checked["pr_created"] = _normalize_pr_number(checked.get("pr_created"))
    merge_sha = checked.get("merge_sha")
    if merge_sha is not None:
        checked["merge_sha"] = _require_sha(merge_sha, "merge_sha")
    else:
        checked["merge_sha"] = None
    checked["merged_base_contribution_refs"] = _normalize_contribution_refs(
        checked.get("merged_base_contribution_refs", []),
        retained_source_ids,
        checked["pr_created"],
        checked["merge_sha"],
    )
    if checked.get("ledger_write") != _LEDGER_WRITE:
        raise _blocked("ledger_write must defer to the weekly scan-state batch")

    if disposition == "NO_CHANGE":
        if (
            repository_change != "NONE"
            or checked["pr_created"] is not None
            or checked.get("merge_sha") is not None
            or checked["merged_base_contribution_refs"]
        ):
            raise _blocked("NO_CHANGE cannot claim repository change")
    elif disposition == "MATERIAL_CHANGE":
        if (
            repository_change == "NONE"
            or checked["pr_created"] is None
            or checked.get("merge_sha") is None
            or not checked["merged_base_contribution_refs"]
        ):
            raise _blocked("MATERIAL_CHANGE requires merged repository evidence")
    elif checked.get("merge_sha") is not None or checked["merged_base_contribution_refs"]:
        raise _blocked("BLOCKED_UNVERIFIED cannot claim merged contribution evidence")

    return checked


def _latest_date_text(left: object, right: date) -> str:
    if isinstance(left, str):
        try:
            previous = date.fromisoformat(left)
        except ValueError as exc:
            raise _blocked("invalid existing operations Ledger date") from exc
        if previous > right:
            return left
    return right.isoformat()


def reconcile_operations_ledger_from_receipts(
    ledger: Mapping[str, object],
    receipt_entries: Sequence[Mapping[str, object]],
) -> dict[str, object]:
    """Reconcile a full receipt corpus without double-counting repeated receipts.

    The function is deliberately pure. It does not scrape GitHub comments or write the
    Ledger. Callers must supply trusted receipt references and persist the returned
    Ledger through the normal reviewed weekly batch. Because the current Ledger keeps a
    date watermark rather than processed receipt refs, one reviewed batch must include
    every same-day receipt for a Source.
    """

    result, known_source_ids = _known_ledger_source_ids(ledger)
    tracking_started_at = _parse_iso_date(result.get("tracking_started_at"), "tracking_started_at")
    rows = result["sources"]
    assert isinstance(rows, list)
    by_id = {str(row["source_id"]): row for row in rows if isinstance(row, dict)}

    seen_refs: dict[str, str] = {}
    seen_payloads: set[str] = set()
    latest_scans: dict[str, date] = {}
    material_events: dict[str, list[tuple[date, int]]] = {}
    contribution_events: dict[str, dict[str, date]] = {}

    for entry in receipt_entries:
        if not isinstance(entry, Mapping):
            raise _blocked("receipt corpus entries must be objects")
        receipt_ref = entry.get("receipt_ref")
        payload = entry.get("actual_source_review_receipt")
        if not isinstance(receipt_ref, str) or not receipt_ref:
            raise _blocked("receipt_ref must be a non-empty string")
        if not isinstance(payload, Mapping):
            raise _blocked("receipt corpus entry is missing actual_source_review_receipt")
        checked = validate_actual_source_review_receipt(payload, result)
        canonical_checked = json.dumps(
            checked, ensure_ascii=False, sort_keys=True, separators=(",", ":")
        )
        previous = seen_refs.get(receipt_ref)
        if previous is not None:
            if previous != canonical_checked:
                raise _blocked("conflicting duplicate receipt ref")
            continue
        seen_refs[receipt_ref] = canonical_checked
        if canonical_checked in seen_payloads:
            continue
        seen_payloads.add(canonical_checked)

        scan_date = _parse_iso_date(checked["scan_date"], "scan_date")
        if scan_date < tracking_started_at:
            continue
        for source_id in checked["scanned_source_ids"]:
            if source_id not in known_source_ids:
                raise _blocked("unknown scanned Source ID")
            if source_id not in latest_scans or scan_date > latest_scans[source_id]:
                latest_scans[source_id] = scan_date
        counts = checked["material_candidate_count_by_source"]
        assert isinstance(counts, dict)
        for source_id, count in counts.items():
            if source_id not in known_source_ids:
                # Discovery-only candidates stay out of the durable Ledger until promotion.
                continue
            material_events.setdefault(source_id, []).append((scan_date, int(count)))
        contributions = checked["merged_base_contribution_refs"]
        assert isinstance(contributions, list)
        for contribution in contributions:
            assert isinstance(contribution, dict)
            source_id = str(contribution["source_id"])
            if source_id not in known_source_ids:
                # Discovery-only contributions remain in the receipt until Source promotion.
                continue
            merge_sha = str(contribution["merge_sha"])
            source_events = contribution_events.setdefault(source_id, {})
            previous_date = source_events.get(merge_sha)
            if previous_date is None or scan_date < previous_date:
                source_events[merge_sha] = scan_date

    for source_id, scan_date in latest_scans.items():
        row = by_id[source_id]
        row[SCAN_DATE_FIELD] = _latest_date_text(row.get(SCAN_DATE_FIELD), scan_date)
    for source_id, events in material_events.items():
        row = by_id[source_id]
        existing_count, existing_date = _existing_material_state(row)
        existing_date_value = row.get(MATERIAL_DATE_FIELD)
        increment = sum(
            count for event_date, count in events
            if existing_date is None or event_date > existing_date
        )
        latest_event_date = max(event_date for event_date, _ in events)
        row[MATERIAL_DATE_FIELD] = _latest_date_text(existing_date_value, latest_event_date)
        row[MATERIAL_COUNT_FIELD] = existing_count + increment

    for source_id, events_by_sha in contribution_events.items():
        row = by_id[source_id]
        existing_count, existing_date, existing_ref = (
            _existing_base_contribution_state(row)
        )
        existing_date_value = row.get(_BASE_DATE_FIELD)

        new_events = [
            (event_date, merge_sha)
            for merge_sha, event_date in events_by_sha.items()
            if merge_sha != existing_ref
            and (existing_date is None or event_date > existing_date)
        ]
        if new_events:
            latest_event_date, latest_merge_sha = max(new_events, key=lambda item: (item[0], item[1]))
            row[_BASE_DATE_FIELD] = _latest_date_text(existing_date_value, latest_event_date)
            row[_BASE_REF_FIELD] = latest_merge_sha
            row[_BASE_COUNT_FIELD] = existing_count + len(new_events)

    return result

