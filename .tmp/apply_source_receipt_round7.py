from __future__ import annotations

from pathlib import Path


PATH = Path("tools/periodic_source_receipt_state.py")


def replace_once(text: str, old: str, new: str, label: str) -> str:
    if text.count(old) != 1:
        raise SystemExit(f"{label} anchor missing or ambiguous")
    return text.replace(old, new)


def main() -> int:
    source = PATH.read_text(encoding="utf-8")

    old_contribution_loop = '''    contribution_by_key: dict[str, dict[str, object]] = {}
    for raw in contributions:
        if not isinstance(raw, Mapping):
            raise _blocked("invalid processed contribution identity")
        source_id = _nonempty_string(
            raw.get("source_id"), "processed contribution Source"
        )
        merge_sha = _require_sha(
            raw.get("merge_sha"), "processed contribution merge_sha"
        )
        merge_date = _parse_iso_date(
            raw.get("merge_date"), "processed contribution merge_date"
        ).isoformat()
        metadata = dict(raw)
        metadata["source_id"] = source_id
        metadata["merge_sha"] = merge_sha
        metadata["merge_date"] = merge_date
        if "refs" in metadata:
            metadata["refs"] = _string_list(
                metadata["refs"], "processed contribution refs", unordered=True
            )
        key = f"{source_id}:{merge_sha}"
        previous = contribution_by_key.get(key)
        if previous is not None and _canonical_json(previous) != _canonical_json(metadata):
            raise _blocked("conflicting processed contribution metadata")
        contribution_by_key[key] = metadata
'''
    new_contribution_loop = '''    contribution_by_key: dict[str, dict[str, object]] = {}
    canonical_contribution_fields = {
        "source_id",
        "pr",
        "merge_sha",
        "merge_date",
        "owner",
        "refs",
    }
    for raw in contributions:
        if not isinstance(raw, Mapping):
            raise _blocked("invalid processed contribution identity")
        unsupported = set(raw) - canonical_contribution_fields
        if unsupported:
            raise _blocked(
                "unsupported processed contribution fields: "
                + ", ".join(sorted(unsupported))
            )
        source_id = _nonempty_string(
            raw.get("source_id"), "processed contribution Source"
        )
        item_pr = _normalize_pr_number(
            raw.get("pr"), field="processed contribution pr"
        )
        if item_pr is None:
            raise _blocked(
                "processed contribution pr must be a positive pull request number"
            )
        merge_sha = _require_sha(
            raw.get("merge_sha"), "processed contribution merge_sha"
        )
        merge_date = _parse_iso_date(
            raw.get("merge_date"), "processed contribution merge_date"
        ).isoformat()
        metadata: dict[str, object] = {
            "source_id": source_id,
            "pr": item_pr,
            "merge_sha": merge_sha,
            "merge_date": merge_date,
        }
        if "owner" in raw:
            metadata["owner"] = _nonempty_string(
                raw.get("owner"), "processed contribution owner"
            )
        if "refs" in raw:
            metadata["refs"] = _string_list(
                raw.get("refs"), "processed contribution refs", unordered=True
            )
        key = f"{source_id}:{merge_sha}"
        previous = contribution_by_key.get(key)
        if previous is not None and _canonical_json(previous) != _canonical_json(metadata):
            raise _blocked("conflicting processed contribution metadata")
        contribution_by_key[key] = metadata
'''
    source = replace_once(
        source,
        old_contribution_loop,
        new_contribution_loop,
        "persisted contribution normalization",
    )

    old_tracking = '''    tracking_started = _parse_iso_date(
        result.get("tracking_started_at"), "tracking_started_at"
    )
    reconciliation_state_present = _RECONCILIATION_FIELD in result
'''
    new_tracking = '''    tracking_started = _parse_iso_date(
        result.get("tracking_started_at"), "tracking_started_at"
    )
    if tracking_started > batch_date:
        raise _blocked("tracking_started_at cannot be after batch_date")
    reconciliation_state_present = _RECONCILIATION_FIELD in result
'''
    source = replace_once(
        source, old_tracking, new_tracking, "bootstrap tracking bound"
    )

    old_receipt_bounds = '''            if persisted_scan_date > previous_batch:
                raise _blocked(
                    "processed receipt scan_date cannot follow last_batch_date"
                )
'''
    new_receipt_bounds = '''            if persisted_scan_date < tracking_started:
                raise _blocked(
                    "processed receipt scan_date predates operations Ledger tracking start"
                )
            if persisted_scan_date > previous_batch:
                raise _blocked(
                    "processed receipt scan_date cannot follow last_batch_date"
                )
'''
    source = replace_once(
        source,
        old_receipt_bounds,
        new_receipt_bounds,
        "persisted receipt lower bound",
    )

    old_link_check = '''    missing_contribution_metadata = (
        receipt_contribution_keys - set(processed_contributions)
    )
    if missing_contribution_metadata:
        raise _blocked(
            "processed receipt contribution metadata is missing: "
            + ", ".join(sorted(missing_contribution_metadata))
        )

    contributions_by_source_date: dict[tuple[str, str], set[str]] = {}
'''
    new_link_check = '''    missing_contribution_metadata = (
        receipt_contribution_keys - set(processed_contributions)
    )
    if missing_contribution_metadata:
        raise _blocked(
            "processed receipt contribution metadata is missing: "
            + ", ".join(sorted(missing_contribution_metadata))
        )

    receipt_scans_by_contribution: dict[str, list[set[str]]] = {}
    for processed_receipt in processed_by_ref.values():
        scanned_sources = set(processed_receipt["scanned_source_ids"])
        for contribution_key in processed_receipt["contribution_keys"]:
            receipt_scans_by_contribution.setdefault(
                str(contribution_key), []
            ).append(scanned_sources)
    for contribution_key, metadata in processed_contributions.items():
        source_id = str(metadata["source_id"])
        linking_receipt_scans = receipt_scans_by_contribution.get(
            contribution_key, []
        )
        if not any(source_id in scanned for scanned in linking_receipt_scans):
            raise _blocked(
                "processed contribution Source must appear in a linking receipt "
                "scanned_source_ids"
            )

    contributions_by_source_date: dict[tuple[str, str], set[str]] = {}
'''
    source = replace_once(
        source,
        old_link_check,
        new_link_check,
        "contribution receipt Source linkage",
    )

    PATH.write_text(source, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
