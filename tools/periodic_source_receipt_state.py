"""Validate reviewed Source receipts and reconcile Operations Ledger state.

The reconciler is deliberately pure. Callers supply an operator-reviewed receipt
corpus and persist the returned Ledger only after validation succeeds.
"""

from __future__ import annotations

import copy
import hashlib
import json
import re
from collections.abc import Mapping, Sequence
from datetime import date
from typing import Any

from tools.periodic_source_analysis_contract import AnalysisBlocked
from tools.periodic_source_operations_state import (
    MATERIAL_COUNT_FIELD,
    MATERIAL_DATE_FIELD,
    SCAN_DATE_FIELD,
)

_ALLOWED_DISPOSITIONS = {"NO_CHANGE", "MATERIAL_CHANGE", "BLOCKED_UNVERIFIED"}
_LEDGER_WRITE = "DEFER_TO_WEEKLY_SCAN_STATE_BATCH"
_SHA_RE = re.compile(r"[0-9a-fA-F]{40}\Z")
_DIGEST_RE = re.compile(r"[0-9a-fA-F]{64}\Z")
_BASE_DATE_FIELD = "last_base_contribution_at"
_BASE_REF_FIELD = "last_base_contribution_ref"
_BASE_COUNT_FIELD = "base_contribution_count_since_tracking_start"
_RECONCILIATION_FIELD = "receipt_reconciliation_state"
_RECONCILIATION_SCHEMA_VERSION = 1
_SOURCE_CLASSIFICATIONS = {"DURABLE_ACTIVE", "DISCOVERY_ACTIVE"}


class _AlreadyProcessed(Exception):
    """Internal control flow for an unchanged, previously processed receipt."""


def _blocked(detail: str) -> AnalysisBlocked:
    return AnalysisBlocked("BLOCKED_CONTEXT_SCHEMA", detail)


def _parse_iso_date(value: object, field: str) -> date:
    if not isinstance(value, str) or not value:
        raise _blocked(f"{field} must be an ISO date")
    try:
        parsed = date.fromisoformat(value)
    except ValueError as exc:
        raise _blocked(f"{field} must be an ISO date") from exc
    if parsed.isoformat() != value:
        raise _blocked(f"{field} must be a canonical ISO date")
    return parsed


def _require_sha(value: object, field: str) -> str:
    if not isinstance(value, str) or _SHA_RE.fullmatch(value) is None:
        raise _blocked(f"{field} must be a 40-character commit SHA")
    return value.lower()


def _require_digest(value: object, field: str) -> str:
    if not isinstance(value, str) or _DIGEST_RE.fullmatch(value) is None:
        raise _blocked(f"{field} must be a 64-character SHA-256 digest")
    return value.lower()


def _nonempty_string(value: object, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise _blocked(f"{field} must be a non-empty string")
    return value.strip()


def _string_list(value: object, field: str, *, unordered: bool = False) -> list[str]:
    if not isinstance(value, list) or any(
        not isinstance(item, str) or not item.strip() for item in value
    ):
        raise _blocked(f"{field} must be a list of non-empty strings")
    normalized = [item.strip() for item in value]
    if len(normalized) != len(set(normalized)):
        raise _blocked(f"{field} must not contain duplicates")
    return sorted(normalized) if unordered else normalized


def _normalize_pr_number(value: object, *, field: str = "pr_created") -> int | None:
    if value is None:
        return None
    if isinstance(value, bool):
        raise _blocked(f"{field} must be a positive pull request number or null")
    if isinstance(value, int):
        number = value
    elif isinstance(value, str):
        text = value.strip()
        if text.startswith("#"):
            text = text[1:]
        if not text.isdecimal():
            raise _blocked(f"{field} must be a positive pull request number or null")
        number = int(text)
    else:
        raise _blocked(f"{field} must be a positive pull request number or null")
    if number <= 0:
        raise _blocked(f"{field} must be a positive pull request number or null")
    return number


def normalize_receipt_ref(value: object) -> str:
    ref = _nonempty_string(value, "receipt_ref")
    lowered = ref.lower()
    for prefix in ("issue-334-comment-", "issue#334-comment-", "comment-"):
        if lowered.startswith(prefix):
            suffix = lowered[len(prefix) :]
            if suffix.isdecimal():
                return f"issue-334-comment-{int(suffix)}"
    if lowered.startswith("#") and lowered[1:].isdecimal():
        return f"issue-334-comment-{int(lowered[1:])}"
    if lowered.isdecimal():
        return f"issue-334-comment-{int(lowered)}"
    return ref


def parse_active_discovery_seed_ids(text: str) -> set[str]:
    if not isinstance(text, str):
        raise _blocked("discovery seed registry must be text")
    identifiers = {
        match.group(1)
        for match in re.finditer(
            r"(?m)^seed_id:\s*([A-Za-z0-9][A-Za-z0-9._-]*)\s*$", text
        )
    }
    if not identifiers:
        raise _blocked("discovery seed registry contains no seed_id entries")
    return identifiers


def _existing_material_state(row: Mapping[str, object]) -> tuple[int, date | None]:
    if MATERIAL_COUNT_FIELD not in row or MATERIAL_DATE_FIELD not in row:
        raise _blocked("missing material candidate state fields")
    count = row[MATERIAL_COUNT_FIELD]
    date_value = row[MATERIAL_DATE_FIELD]
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
    required = {_BASE_COUNT_FIELD, _BASE_DATE_FIELD, _BASE_REF_FIELD}
    if not required.issubset(row):
        raise _blocked("missing Base contribution state fields")
    count = row[_BASE_COUNT_FIELD]
    date_value = row[_BASE_DATE_FIELD]
    reference = row[_BASE_REF_FIELD]
    if isinstance(count, bool) or not isinstance(count, int) or count < 0:
        raise _blocked("invalid existing Base contribution count")
    event_date = (
        None
        if date_value is None
        else _parse_iso_date(date_value, _BASE_DATE_FIELD)
    )
    normalized_ref = None if reference is None else _require_sha(reference, _BASE_REF_FIELD)
    empty = count == 0 and event_date is None and normalized_ref is None
    populated = count > 0 and event_date is not None and normalized_ref is not None
    if not (empty or populated):
        raise _blocked("existing Base contribution state is inconsistent")
    return count, event_date, normalized_ref


def _known_ledger_sources(
    ledger: Mapping[str, object],
) -> tuple[dict[str, object], dict[str, dict[str, object]]]:
    result = copy.deepcopy(dict(ledger))
    rows = result.get("sources")
    if result.get("schema_version") != 1 or not isinstance(rows, list):
        raise _blocked("invalid operations Ledger")
    by_id: dict[str, dict[str, object]] = {}
    for raw in rows:
        if not isinstance(raw, dict):
            raise _blocked("invalid operations Ledger Source row")
        source_id = _nonempty_string(raw.get("source_id"), "source_id")
        if source_id in by_id:
            raise _blocked("invalid or duplicate operations Ledger Source ID")
        _existing_material_state(raw)
        _, _, normalized_ref = _existing_base_contribution_state(raw)
        if normalized_ref is not None:
            raw[_BASE_REF_FIELD] = normalized_ref
        by_id[source_id] = raw
    return result, by_id


def _normalize_source_state_at_scan(value: object) -> dict[str, str]:
    if value is None:
        return {}
    if not isinstance(value, Mapping):
        raise _blocked("source_state_at_scan must be an object")
    result: dict[str, str] = {}
    for raw_id, raw_state in value.items():
        source_id = _nonempty_string(raw_id, "source_state_at_scan key")
        state = _nonempty_string(raw_state, "source_state_at_scan value")
        if state not in _SOURCE_CLASSIFICATIONS:
            raise _blocked("invalid source_state_at_scan classification")
        result[source_id] = state
    return dict(sorted(result.items()))


def _normalize_merge_date_map(value: object) -> dict[str, str]:
    if value is None:
        return {}
    if not isinstance(value, Mapping):
        raise _blocked("contribution_merge_dates must be an object")
    result: dict[str, str] = {}
    for raw_sha, raw_date in value.items():
        sha = _require_sha(raw_sha, "contribution merge-date SHA")
        merged = _parse_iso_date(raw_date, "contribution merge_date").isoformat()
        previous = result.get(sha)
        if previous is not None and previous != merged:
            raise _blocked("conflicting contribution merge dates")
        result[sha] = merged
    return dict(sorted(result.items()))


def _resolve_contribution_source(item: Mapping[str, object]) -> str:
    source_id = item.get("source_id")
    legacy_source = item.get("source")
    if source_id is not None and legacy_source is not None and source_id != legacy_source:
        raise _blocked("conflicting contribution Source aliases")
    return _nonempty_string(
        source_id if source_id is not None else legacy_source,
        "contribution Source",
    )


def _resolve_merge_date(
    item: Mapping[str, object],
    merge_sha: str,
    contribution_merge_dates: Mapping[str, str],
) -> str:
    direct = item.get("merge_date", item.get("merged_at"))
    mapped = contribution_merge_dates.get(merge_sha)
    if direct is not None:
        parsed = _parse_iso_date(direct, "contribution merge_date").isoformat()
        if mapped is not None and mapped != parsed:
            raise _blocked("conflicting contribution merge dates")
        return parsed
    if mapped is not None:
        return mapped
    raise _blocked("contribution merge_date requires trusted merge evidence")


def _normalize_contribution_refs(
    value: object,
    retained_source_ids: Sequence[str],
    receipt_pr: int | None,
    receipt_merge_sha: str | None,
    contribution_merge_dates: Mapping[str, str],
) -> list[dict[str, object]]:
    if not isinstance(value, list):
        raise _blocked("merged_base_contribution_refs must be a list")
    if not value:
        return []

    if all(isinstance(item, str) for item in value):
        refs = _string_list(value, "merged_base_contribution_refs", unordered=True)
        if len(retained_source_ids) != 1:
            raise _blocked("legacy contribution refs require one retained Source")
        if receipt_pr is None or receipt_merge_sha is None:
            raise _blocked("legacy contribution refs require receipt PR and merge SHA")
        merge_date = contribution_merge_dates.get(receipt_merge_sha)
        if merge_date is None:
            raise _blocked("legacy contribution refs require trusted merge_date")
        return [
            {
                "source_id": retained_source_ids[0],
                "pr": receipt_pr,
                "merge_sha": receipt_merge_sha,
                "merge_date": merge_date,
                "refs": refs,
            }
        ]

    if not all(isinstance(item, Mapping) for item in value):
        raise _blocked("merged Base contribution refs must use one consistent format")

    normalized: list[dict[str, object]] = []
    seen: set[tuple[str, str]] = set()
    for raw_item in value:
        assert isinstance(raw_item, Mapping)
        source_id = _resolve_contribution_source(raw_item)
        if source_id not in retained_source_ids:
            raise _blocked("contribution Source must be retained")

        item_pr = _normalize_pr_number(
            raw_item.get("pr", receipt_pr), field="contribution pr"
        )
        if item_pr is None:
            raise _blocked("contribution ref requires a pull request number")
        if receipt_pr is not None and item_pr != receipt_pr:
            raise _blocked("contribution PR does not match receipt PR")

        merge_sha = _require_sha(
            raw_item.get("merge_sha", receipt_merge_sha), "contribution merge_sha"
        )
        if receipt_merge_sha is not None and merge_sha != receipt_merge_sha:
            raise _blocked("contribution merge SHA does not match receipt merge SHA")
        merge_date = _resolve_merge_date(raw_item, merge_sha, contribution_merge_dates)

        key = (source_id, merge_sha)
        if key in seen:
            raise _blocked("duplicate merged Base contribution")
        seen.add(key)
        row: dict[str, object] = {
            "source_id": source_id,
            "pr": item_pr,
            "merge_sha": merge_sha,
            "merge_date": merge_date,
        }
        owner = raw_item.get("owner")
        if owner is not None:
            row["owner"] = _nonempty_string(owner, "contribution owner")
        refs = raw_item.get("refs")
        if refs is not None:
            row["refs"] = _string_list(
                refs, "contribution refs", unordered=True
            )
        normalized.append(row)
    return sorted(
        normalized,
        key=lambda item: (
            str(item["source_id"]),
            str(item["merge_sha"]),
            int(item["pr"]),
        ),
    )


def _validate_source_classification(
    *,
    scanned_source_ids: Sequence[str],
    scanned_discovery_seed_ids: Sequence[str],
    ledger_sources: Mapping[str, Mapping[str, object]],
    known_discovery_seed_ids: set[str],
    historical_discovery_seed_ids: set[str],
    source_state_at_scan: Mapping[str, str],
) -> None:
    allowed_historical_discovery = known_discovery_seed_ids | historical_discovery_seed_ids
    for source_id in scanned_source_ids:
        row = ledger_sources.get(source_id)
        if row is None:
            raise _blocked("unknown scanned Source ID")
        if row.get("status") == "ACTIVE":
            continue
        if source_state_at_scan.get(source_id) != "DURABLE_ACTIVE":
            raise _blocked("historical inactive Source requires receipt-time classification")

    for seed_id in scanned_discovery_seed_ids:
        if seed_id in known_discovery_seed_ids and seed_id not in ledger_sources:
            continue
        if (
            seed_id in allowed_historical_discovery
            and source_state_at_scan.get(seed_id) == "DISCOVERY_ACTIVE"
        ):
            continue
        if seed_id in ledger_sources:
            raise _blocked("durable Source ID must use scanned_source_ids")
        raise _blocked("unknown discovery seed ID")


def _normalize_high_nutrient_sources(value: object) -> list[dict[str, object]]:
    if value is None:
        value = []
    if not isinstance(value, list):
        raise _blocked("high_nutrient_sources must be a list")
    result: list[dict[str, object]] = []
    for raw in value:
        if not isinstance(raw, Mapping):
            raise _blocked("high_nutrient_sources rows must be objects")
        source_name = _nonempty_string(raw.get("source"), "high-nutrient source")
        score = raw.get("nutrient_score")
        if isinstance(score, bool) or not isinstance(score, int) or not 9 <= score <= 12:
            raise _blocked("high-nutrient score must be 9..12")
        archetype = _nonempty_string(
            raw.get("source_archetype"), "high-nutrient source archetype"
        )
        reusable_units = _string_list(
            raw.get("reusable_units"),
            "high-nutrient reusable_units",
            unordered=True,
        )
        row = dict(raw)
        row.update(
            source=source_name,
            nutrient_score=score,
            source_archetype=archetype,
            reusable_units=reusable_units,
        )
        result.append(row)
    return sorted(
        result,
        key=lambda item: (
            str(item["source"]),
            int(item["nutrient_score"]),
            str(item["source_archetype"]),
        ),
    )


def validate_actual_source_review_receipt(
    receipt: Mapping[str, object],
    ledger: Mapping[str, object],
    *,
    known_discovery_seed_ids: set[str] | None = None,
    historical_discovery_seed_ids: set[str] | None = None,
    source_state_at_scan: Mapping[str, str] | None = None,
    contribution_merge_dates: Mapping[str, str] | None = None,
    batch_date: date | None = None,
    validate_current_source_state: bool = True,
) -> dict[str, object]:
    """Validate and normalize one actual Source review receipt.

    Current receipt classifications are checked against current Ledger/seed state.
    Historical classification overrides are accepted only from the operator-reviewed
    corpus envelope and must use explicit `DURABLE_ACTIVE`/`DISCOVERY_ACTIVE` values.
    """

    if not isinstance(receipt, Mapping):
        raise _blocked("actual Source review receipt must be an object")
    checked = copy.deepcopy(dict(receipt))
    _, ledger_sources = _known_ledger_sources(ledger)
    current_discovery = set(known_discovery_seed_ids or set())
    historical_discovery = set(historical_discovery_seed_ids or set())
    classification = _normalize_source_state_at_scan(source_state_at_scan)
    merge_dates = _normalize_merge_date_map(contribution_merge_dates)

    scan_date = _parse_iso_date(checked.get("scan_date"), "scan_date")
    if batch_date is not None and scan_date > batch_date:
        raise _blocked("scan_date cannot be after batch_date")
    checked["scan_date"] = scan_date.isoformat()
    checked["start_main"] = _require_sha(checked.get("start_main"), "start_main")
    checked["final_main"] = _require_sha(checked.get("final_main"), "final_main")

    disposition = checked.get("disposition")
    if disposition not in _ALLOWED_DISPOSITIONS:
        raise _blocked("invalid actual Source review disposition")

    scanned_sources = _string_list(
        checked.get("scanned_source_ids"), "scanned_source_ids", unordered=True
    )
    scanned_discovery = _string_list(
        checked.get("scanned_discovery_seed_ids"),
        "scanned_discovery_seed_ids",
        unordered=True,
    )
    if not scanned_sources and not scanned_discovery:
        raise _blocked("receipt must identify an actually reviewed Source")
    if validate_current_source_state:
        _validate_source_classification(
            scanned_source_ids=scanned_sources,
            scanned_discovery_seed_ids=scanned_discovery,
            ledger_sources=ledger_sources,
            known_discovery_seed_ids=current_discovery,
            historical_discovery_seed_ids=historical_discovery,
            source_state_at_scan=classification,
        )
    checked["scanned_source_ids"] = scanned_sources
    checked["scanned_discovery_seed_ids"] = scanned_discovery

    retained_sources = _string_list(
        checked.get("retained_candidate_source_ids"),
        "retained_candidate_source_ids",
        unordered=True,
    )
    allowed_retained = set(scanned_sources) | set(scanned_discovery)
    if set(retained_sources) - allowed_retained:
        raise _blocked("unknown retained Candidate Source ID")
    checked["retained_candidate_source_ids"] = retained_sources

    counts = checked.get("material_candidate_count_by_source")
    if not isinstance(counts, Mapping):
        raise _blocked("material_candidate_count_by_source must be an object")
    if set(counts) != set(retained_sources):
        raise _blocked("material candidate Source IDs do not match retained Sources")
    normalized_counts: dict[str, int] = {}
    for source_id, raw_count in counts.items():
        if isinstance(raw_count, bool) or not isinstance(raw_count, int) or raw_count <= 0:
            raise _blocked("material candidate counts must be positive integers")
        normalized_counts[str(source_id)] = raw_count
    checked["material_candidate_count_by_source"] = dict(
        sorted(normalized_counts.items())
    )

    checked["high_nutrient_sources"] = _normalize_high_nutrient_sources(
        checked.get("high_nutrient_sources", [])
    )
    checked["unverified_scope"] = _string_list(
        checked.get("unverified_scope"), "unverified_scope", unordered=True
    )

    repository_change = _nonempty_string(
        checked.get("repository_change"), "repository_change"
    )
    checked["repository_change"] = repository_change
    checked["pr_created"] = _normalize_pr_number(checked.get("pr_created"))
    raw_merge_sha = checked.get("merge_sha")
    checked["merge_sha"] = (
        None if raw_merge_sha is None else _require_sha(raw_merge_sha, "merge_sha")
    )
    checked["merged_base_contribution_refs"] = _normalize_contribution_refs(
        checked.get("merged_base_contribution_refs", []),
        retained_sources,
        checked["pr_created"],
        checked["merge_sha"],
        merge_dates,
    )
    if checked.get("ledger_write") != _LEDGER_WRITE:
        raise _blocked("ledger_write must defer to the weekly scan-state batch")

    if disposition == "NO_CHANGE":
        if (
            repository_change != "NONE"
            or checked["pr_created"] is not None
            or checked["merge_sha"] is not None
            or checked["merged_base_contribution_refs"]
        ):
            raise _blocked("NO_CHANGE cannot claim repository change")
    elif disposition == "MATERIAL_CHANGE":
        if (
            repository_change == "NONE"
            or checked["pr_created"] is None
            or checked["merge_sha"] is None
            or not checked["merged_base_contribution_refs"]
        ):
            raise _blocked("MATERIAL_CHANGE requires merged repository evidence")
    elif checked["merge_sha"] is not None or checked["merged_base_contribution_refs"]:
        raise _blocked("BLOCKED_UNVERIFIED cannot claim merged contribution evidence")

    return checked


def _canonical_json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _payload_hash(normalized_receipt: Mapping[str, object]) -> str:
    return hashlib.sha256(_canonical_json(normalized_receipt).encode("utf-8")).hexdigest()


def _normalize_existing_reconciliation_state(
    value: object,
) -> tuple[
    dict[str, str],
    dict[str, dict[str, object]],
    date | None,
    dict[str, dict[str, object]],
]:
    if value is None:
        return {}, {}, None, {}
    if not isinstance(value, Mapping) or value.get("schema_version") != 1:
        raise _blocked("invalid receipt reconciliation state")
    processed = value.get("processed_receipts")
    contributions = value.get("processed_contributions")
    last_batch = value.get("last_batch_date")
    if not isinstance(processed, list) or not isinstance(contributions, list):
        raise _blocked("invalid receipt reconciliation identity state")

    ref_hashes: dict[str, str] = {}
    processed_rows: dict[str, dict[str, object]] = {}
    for row in processed:
        if not isinstance(row, Mapping):
            raise _blocked("invalid processed receipt identity")
        ref = normalize_receipt_ref(row.get("receipt_ref"))
        payload_sha = _require_digest(row.get("payload_sha256"), "processed receipt hash")
        normalized_row: dict[str, object] = {
            "receipt_ref": ref,
            "payload_sha256": payload_sha,
        }
        if row.get("scan_date") is not None:
            normalized_row["scan_date"] = _parse_iso_date(
                row.get("scan_date"), "processed receipt scan_date"
            ).isoformat()
        previous = ref_hashes.get(ref)
        if previous is not None and previous != payload_sha:
            raise _blocked("conflicting processed receipt identity")
        ref_hashes[ref] = payload_sha
        processed_rows[ref] = normalized_row

    contribution_by_key: dict[str, dict[str, object]] = {}
    for row in contributions:
        if not isinstance(row, Mapping):
            raise _blocked("invalid processed contribution identity")
        source_id = _nonempty_string(row.get("source_id"), "processed contribution Source")
        merge_sha = _require_sha(
            row.get("merge_sha"), "processed contribution merge_sha"
        )
        metadata = dict(row)
        metadata["source_id"] = source_id
        metadata["merge_sha"] = merge_sha
        if "refs" in metadata:
            metadata["refs"] = _string_list(
                metadata["refs"], "processed contribution refs", unordered=True
            )
        if "merge_date" in metadata:
            metadata["merge_date"] = _parse_iso_date(
                metadata["merge_date"], "processed contribution merge_date"
            ).isoformat()
        key = f"{source_id}:{merge_sha}"
        previous = contribution_by_key.get(key)
        if previous is not None and _canonical_json(previous) != _canonical_json(metadata):
            raise _blocked("conflicting processed contribution metadata")
        contribution_by_key[key] = metadata

    normalized_last_batch = (
        None if last_batch is None else _parse_iso_date(last_batch, "last_batch_date")
    )
    return ref_hashes, contribution_by_key, normalized_last_batch, processed_rows


def _receipt_entry_envelope(entry: Mapping[str, object]) -> dict[str, object]:
    return {
        "source_state_at_scan": _normalize_source_state_at_scan(
            entry.get("source_state_at_scan")
        ),
        "contribution_merge_dates": _normalize_merge_date_map(
            entry.get("contribution_merge_dates")
        ),
    }


def reconcile_operations_ledger_from_receipts(
    ledger: Mapping[str, object],
    receipt_entries: Sequence[Mapping[str, object]],
    *,
    known_discovery_seed_ids: set[str] | None = None,
    historical_discovery_seed_ids: set[str] | None = None,
    batch_date: date,
) -> dict[str, object]:
    """Reconcile operator-reviewed receipts with persisted identity state.

    Existing processed receipts are matched by normalized reference and canonical
    payload hash before current source lifecycle validation. This allows safe replay
    after a Source becomes inactive or a discovery seed is promoted. New historical
    receipts whose classification no longer matches current state require explicit
    receipt-time classification in the reviewed corpus envelope.
    """

    result, ledger_sources = _known_ledger_sources(ledger)
    tracking_started = _parse_iso_date(
        result.get("tracking_started_at"), "tracking_started_at"
    )
    current_seed_ids = set(known_discovery_seed_ids or set())
    historical_seed_ids = set(historical_discovery_seed_ids or set())
    ref_hashes, processed_contributions, previous_batch, existing_processed_rows = (
        _normalize_existing_reconciliation_state(result.get(_RECONCILIATION_FIELD))
    )
    if previous_batch is not None and batch_date < previous_batch:
        raise _blocked("batch_date cannot move backwards")

    payload_hashes = set(ref_hashes.values())
    new_processed_rows: dict[str, dict[str, object]] = dict(existing_processed_rows)
    latest_scans: dict[str, date] = {}
    material_events: dict[str, list[tuple[date, int, str]]] = {}
    contribution_events: dict[str, dict[str, dict[str, object]]] = {}

    for raw_entry in receipt_entries:
        if not isinstance(raw_entry, Mapping):
            raise _blocked("receipt corpus entries must be objects")
        receipt_ref = normalize_receipt_ref(raw_entry.get("receipt_ref"))
        raw_receipt = raw_entry.get("actual_source_review_receipt")
        if not isinstance(raw_receipt, Mapping):
            raise _blocked("receipt corpus entry is missing actual_source_review_receipt")
        envelope = _receipt_entry_envelope(raw_entry)

        # First normalize structure only. Previously trusted receipt identities can be
        # replayed after a Source lifecycle transition without reinterpreting history
        # through current ACTIVE/discovery state.
        identity_receipt = validate_actual_source_review_receipt(
            raw_receipt,
            result,
            known_discovery_seed_ids=current_seed_ids,
            historical_discovery_seed_ids=historical_seed_ids,
            source_state_at_scan=envelope["source_state_at_scan"],
            contribution_merge_dates=envelope["contribution_merge_dates"],
            batch_date=batch_date,
            validate_current_source_state=False,
        )
        payload_sha = _payload_hash(identity_receipt)
        previous_hash = ref_hashes.get(receipt_ref)
        if previous_hash is not None:
            if previous_hash != payload_sha:
                raise _blocked("conflicting duplicate receipt ref")
            continue
        new_processed_rows[receipt_ref] = {
            "receipt_ref": receipt_ref,
            "payload_sha256": payload_sha,
            "scan_date": identity_receipt["scan_date"],
        }
        ref_hashes[receipt_ref] = payload_sha
        if payload_sha in payload_hashes:
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
        payload_hashes.add(payload_sha)

        event_date = _parse_iso_date(normalized["scan_date"], "scan_date")
        if event_date < tracking_started:
            raise _blocked("receipt predates operations Ledger tracking start")
        for source_id in normalized["scanned_source_ids"]:
            previous = latest_scans.get(source_id)
            if previous is None or event_date > previous:
                latest_scans[source_id] = event_date
        discovery_sources_at_scan = set(normalized["scanned_discovery_seed_ids"])
        for source_id, count in normalized["material_candidate_count_by_source"].items():
            if source_id in ledger_sources and source_id not in discovery_sources_at_scan:
                material_events.setdefault(source_id, []).append(
                    (event_date, int(count), payload_sha)
                )
        for contribution in normalized["merged_base_contribution_refs"]:
            source_id = str(contribution["source_id"])
            if source_id not in ledger_sources or source_id in discovery_sources_at_scan:
                continue
            merge_sha = str(contribution["merge_sha"])
            key = f"{source_id}:{merge_sha}"
            existing = processed_contributions.get(key)
            if existing is not None:
                if _canonical_json(existing) != _canonical_json(contribution):
                    raise _blocked("conflicting contribution metadata")
                continue
            per_source = contribution_events.setdefault(source_id, {})
            previous = per_source.get(merge_sha)
            if previous is not None and _canonical_json(previous) != _canonical_json(contribution):
                raise _blocked("conflicting contribution metadata")
            per_source[merge_sha] = dict(contribution)

    for source_id, scan_date in latest_scans.items():
        row = ledger_sources[source_id]
        current = row.get(SCAN_DATE_FIELD)
        if current is None or _parse_iso_date(current, SCAN_DATE_FIELD) < scan_date:
            row[SCAN_DATE_FIELD] = scan_date.isoformat()

    had_identity_state = result.get(_RECONCILIATION_FIELD) is not None
    for source_id, events in material_events.items():
        row = ledger_sources[source_id]
        current_count, current_date = _existing_material_state(row)
        ordered = sorted(events, key=lambda item: (item[0], item[2]))
        for event_date, increment, _ in ordered:
            if not had_identity_state and current_date is not None:
                if event_date == current_date:
                    raise _blocked("ambiguous same-day material event without identity state")
                if event_date < current_date:
                    continue
            current_count += increment
            if current_date is None or event_date > current_date:
                current_date = event_date
        row[MATERIAL_COUNT_FIELD] = current_count
        row[MATERIAL_DATE_FIELD] = None if current_date is None else current_date.isoformat()

    for source_id, by_sha in contribution_events.items():
        row = ledger_sources[source_id]
        current_count, current_date, current_ref = _existing_base_contribution_state(row)
        for merge_sha, metadata in sorted(
            by_sha.items(),
            key=lambda item: (
                _parse_iso_date(item[1]["merge_date"], "contribution merge_date"),
                item[0],
            ),
        ):
            merge_date = _parse_iso_date(
                metadata["merge_date"], "contribution merge_date"
            )
            key = f"{source_id}:{merge_sha}"
            if merge_sha == current_ref:
                processed_contributions.setdefault(key, metadata)
                continue
            if not had_identity_state and current_date is not None and merge_date <= current_date:
                raise _blocked("ambiguous historical contribution without identity state")
            current_count += 1
            if current_date is None or merge_date >= current_date:
                current_date = merge_date
                current_ref = merge_sha
            processed_contributions[key] = metadata
        row[_BASE_COUNT_FIELD] = current_count
        row[_BASE_DATE_FIELD] = None if current_date is None else current_date.isoformat()
        row[_BASE_REF_FIELD] = current_ref

    result[_RECONCILIATION_FIELD] = {
        "schema_version": _RECONCILIATION_SCHEMA_VERSION,
        "identity_floor_date": (
            result.get(_RECONCILIATION_FIELD, {}).get("identity_floor_date")
            if isinstance(result.get(_RECONCILIATION_FIELD), Mapping)
            else batch_date.isoformat()
        ),
        "last_batch_date": batch_date.isoformat(),
        "processed_receipts": [
            new_processed_rows[key] for key in sorted(new_processed_rows)
        ],
        "processed_contributions": [
            processed_contributions[key] for key in sorted(processed_contributions)
        ],
    }
    return result
