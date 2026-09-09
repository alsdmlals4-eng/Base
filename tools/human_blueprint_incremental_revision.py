"""Validate lossless human Blueprint revision receipts."""

from __future__ import annotations

import re
from typing import Any


SHA = re.compile(r"^[0-9a-f]{40}$")
INVENTORY_LIST_FIELDS = (
    "stable_ids",
    "section_ids",
    "diagram_ids",
    "approved_asset_ids",
    "consumer_refs",
    "evidence_refs",
)
REVISION_MODES = {
    "INCREMENTAL_WHEN_VALID_PREDECESSOR_EXISTS",
    "INITIAL_CREATION_NO_VALID_PREDECESSOR",
    "PREDECESSOR_UNAVAILABLE_BLOCKED_UNVERIFIED",
}
JUSTIFICATION_TYPES = {
    "REMOVED",
    "REPLACED",
    "RENAMED",
    "STATUS_DOWNGRADE",
}
MATURITY_RANK = {
    "DOCUMENTED": 0,
    "CONFIRMED": 1,
    "IMPLEMENTED": 2,
    "AUTOMATED_TEST_PASS": 3,
    "RUNTIME_VERIFIED": 4,
    "UX_VERIFIED": 5,
    "RELEASE_READY": 6,
}


def _text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _string_list(value: Any, *, nonempty: bool = False) -> bool:
    if not isinstance(value, list):
        return False
    if nonempty and not value:
        return False
    return all(_text(item) for item in value)


def _collect_list_values(value: Any, key: str) -> set[str]:
    collected: set[str] = set()
    if isinstance(value, dict):
        for child_key, child_value in value.items():
            if child_key == key and isinstance(child_value, list):
                collected.update(
                    item for item in child_value if isinstance(item, str) and item
                )
            else:
                collected.update(_collect_list_values(child_value, key))
    elif isinstance(value, list):
        for child in value:
            collected.update(_collect_list_values(child, key))
    return collected


def projection_status_facts(projection: dict[str, Any]) -> dict[str, str]:
    """Return status facts that the successor inventory must cover."""
    facts: dict[str, str] = {}
    for record_type, id_key in (
        ("goals", "goal_id"),
        ("systems", "system_id"),
    ):
        for record in projection.get(record_type, []):
            if not isinstance(record, dict) or not _text(record.get(id_key)):
                continue
            identity = record[id_key]
            if _text(record.get("maturity_status")):
                facts[f"{identity}:maturity_status"] = record["maturity_status"]
            for check in record.get("checklist", []):
                if not isinstance(check, dict) or not _text(check.get("id")):
                    continue
                if _text(check.get("status")):
                    facts[f"{identity}:checklist:{check['id']}"] = check["status"]

    for case in projection.get("cases", []):
        if not isinstance(case, dict) or not _text(case.get("case_id")):
            continue
        identity = case["case_id"]
        for field in ("applicability", "maturity_status"):
            if _text(case.get(field)):
                facts[f"{identity}:{field}"] = case[field]
        for verification in case.get("verification", []):
            if not isinstance(verification, dict):
                continue
            if _text(verification.get("level")) and _text(
                verification.get("status")
            ):
                key = f"{identity}:verification:{verification['level']}"
                facts[key] = verification["status"]

    board = projection.get("project_work_kanban", {})
    if isinstance(board, dict):
        for work in board.get("work_items", []):
            if not isinstance(work, dict) or not _text(work.get("work_item_id")):
                continue
            identity = work["work_item_id"]
            if _text(work.get("status")):
                facts[f"{identity}:status"] = work["status"]
            for check in work.get("checklist", []):
                if not isinstance(check, dict) or not _text(check.get("id")):
                    continue
                if _text(check.get("status")):
                    facts[f"{identity}:checklist:{check['id']}"] = check["status"]
            for verification in work.get("verification", []):
                if not isinstance(verification, dict):
                    continue
                if _text(verification.get("level")) and _text(
                    verification.get("status")
                ):
                    key = f"{identity}:verification:{verification['level']}"
                    facts[key] = verification["status"]
    return facts


def projection_stable_ids(projection: dict[str, Any]) -> set[str]:
    identities: set[str] = set()
    for record_type, id_key in (
        ("goals", "goal_id"),
        ("systems", "system_id"),
        ("cases", "case_id"),
    ):
        for record in projection.get(record_type, []):
            if isinstance(record, dict) and _text(record.get(id_key)):
                identities.add(record[id_key])
    board = projection.get("project_work_kanban", {})
    if isinstance(board, dict):
        for work in board.get("work_items", []):
            if isinstance(work, dict) and _text(work.get("work_item_id")):
                identities.add(work["work_item_id"])
    return identities


def _validate_inventory(
    value: Any,
    label: str,
    errors: list[str],
) -> dict[str, Any] | None:
    if not isinstance(value, dict):
        errors.append(f"{label} must be an object")
        return None
    for field in INVENTORY_LIST_FIELDS:
        items = value.get(field)
        if not _string_list(items):
            errors.append(f"{label}.{field} must be a list of nonempty strings")
            continue
        if len(items) != len(set(items)):
            errors.append(f"{label}.{field} must not contain duplicates")
    status_facts = value.get("status_facts")
    if not isinstance(status_facts, dict):
        errors.append(f"{label}.status_facts must be an object")
    else:
        for key, status in status_facts.items():
            if not _text(key) or not _text(status):
                errors.append(
                    f"{label}.status_facts must map nonempty keys to statuses"
                )
                break
    return value


def _inventory_is_empty(inventory: dict[str, Any]) -> bool:
    return not any(inventory.get(field) for field in INVENTORY_LIST_FIELDS) and not (
        inventory.get("status_facts")
    )


def _status_is_downgrade(key: str, before: str, after: str) -> bool:
    if before == after:
        return False
    if key.endswith(":maturity_status"):
        before_rank = MATURITY_RANK.get(before)
        after_rank = MATURITY_RANK.get(after)
        return (
            before_rank is not None
            and after_rank is not None
            and after_rank < before_rank
        )
    if key.endswith(":applicability"):
        return before == "APPLICABLE" and after != "APPLICABLE"
    if before == "PASS":
        return after != "PASS"
    if before == "DONE":
        return after != "DONE"
    return False


def _detected_loss_keys(
    predecessor: dict[str, Any],
    successor: dict[str, Any],
) -> set[str]:
    losses: set[str] = set()
    for field in INVENTORY_LIST_FIELDS:
        before = set(predecessor.get(field, []))
        after = set(successor.get(field, []))
        losses.update(f"{field}:{item}" for item in before - after)

    before_status = predecessor.get("status_facts", {})
    after_status = successor.get("status_facts", {})
    if isinstance(before_status, dict) and isinstance(after_status, dict):
        for key, before in before_status.items():
            after = after_status.get(key)
            if after is None or _status_is_downgrade(key, before, after):
                losses.add(f"status_facts:{key}")
    return losses


def _validate_justifications(
    value: Any,
    detected_losses: set[str],
    errors: list[str],
) -> None:
    if not isinstance(value, list):
        errors.append("removal_or_downgrade_justifications must be a list")
        return
    seen: set[str] = set()
    for index, record in enumerate(value):
        prefix = f"removal_or_downgrade_justifications[{index}]"
        if not isinstance(record, dict):
            errors.append(f"{prefix} must be an object")
            continue
        change_key = record.get("change_key")
        change_type = record.get("change_type")
        if not _text(change_key):
            errors.append(f"{prefix}.change_key is required")
            continue
        if change_key in seen:
            errors.append(f"{prefix}.change_key must be unique: {change_key}")
        seen.add(change_key)
        if change_key not in detected_losses:
            errors.append(
                f"{prefix}.change_key does not match a detected loss: {change_key}"
            )
        if change_type not in JUSTIFICATION_TYPES:
            errors.append(f"{prefix}.change_type is invalid")
        for field in ("reason", "verification_impact"):
            if not _text(record.get(field)):
                errors.append(f"{prefix}.{field} is required")
        for field in ("replacement_refs", "affected_consumers", "evidence"):
            if not _string_list(record.get(field)):
                errors.append(f"{prefix}.{field} must be a list of nonempty strings")
        if change_type in {"REPLACED", "RENAMED"} and not record.get(
            "replacement_refs"
        ):
            errors.append(f"{prefix}.replacement_refs is required for {change_type}")
        if not record.get("evidence"):
            errors.append(f"{prefix}.evidence must not be empty")

    for loss in sorted(detected_losses - seen):
        errors.append(
            "UNEXPLAINED_REMOVAL_OR_STATUS_DOWNGRADE_FORBIDDEN: " + loss
        )


def _validate_successor_coverage(
    projection: dict[str, Any],
    successor: dict[str, Any],
    errors: list[str],
) -> None:
    expected_ids = projection_stable_ids(projection)
    declared_ids = set(successor.get("stable_ids", []))
    for identity in sorted(expected_ids - declared_ids):
        errors.append(
            f"successor_inventory.stable_ids is missing current projection ID {identity}"
        )

    for field, source_key in (
        ("consumer_refs", "actual_consumers"),
        ("evidence_refs", "evidence"),
    ):
        expected = _collect_list_values(projection, source_key)
        declared = set(successor.get(field, []))
        for item in sorted(expected - declared):
            errors.append(f"successor_inventory.{field} is missing {item}")

    expected_facts = projection_status_facts(projection)
    declared_facts = successor.get("status_facts", {})
    if not isinstance(declared_facts, dict):
        return
    for key, expected in sorted(expected_facts.items()):
        actual = declared_facts.get(key)
        if actual is None:
            errors.append(f"successor_inventory.status_facts is missing {key}")
        elif actual != expected:
            errors.append(
                "successor_inventory.status_facts mismatch for "
                f"{key}: expected {expected}, got {actual}"
            )


def validate_blueprint_revision(projection: dict[str, Any]) -> list[str]:
    """Validate the predecessor-to-successor loss-regression receipt."""
    errors: list[str] = []
    revision = projection.get("blueprint_revision")
    if not isinstance(revision, dict):
        return ["blueprint_revision is required for current PDF publication"]

    mode = revision.get("revision_mode")
    if mode not in REVISION_MODES:
        errors.append("blueprint_revision.revision_mode is invalid")
    publication_status = revision.get("publication_status")
    if publication_status not in {"READY", "BLOCKED_UNVERIFIED"}:
        errors.append("blueprint_revision.publication_status is invalid")

    predecessor = _validate_inventory(
        revision.get("predecessor_inventory"),
        "predecessor_inventory",
        errors,
    )
    successor = _validate_inventory(
        revision.get("successor_inventory"),
        "successor_inventory",
        errors,
    )
    if successor is not None:
        _validate_successor_coverage(projection, successor, errors)

    if not _string_list(revision.get("semantic_delta_summary"), nonempty=True):
        errors.append("semantic_delta_summary must be a nonempty string list")

    if mode == "INCREMENTAL_WHEN_VALID_PREDECESSOR_EXISTS":
        if publication_status != "READY":
            errors.append("incremental publication_status must be READY")
        if not _text(revision.get("predecessor_blueprint_ref")):
            errors.append(
                "predecessor_blueprint_ref is required for incremental revision"
            )
        source = revision.get("predecessor_source_commit")
        if not isinstance(source, str) or not SHA.fullmatch(source):
            errors.append(
                "predecessor_source_commit must be a 40-character lowercase SHA"
            )
        if predecessor is not None and _inventory_is_empty(predecessor):
            errors.append(
                "predecessor_inventory must not be empty for incremental revision"
            )
    elif mode == "INITIAL_CREATION_NO_VALID_PREDECESSOR":
        if publication_status != "READY":
            errors.append("initial publication_status must be READY")
        if revision.get("predecessor_blueprint_ref") not in {None, ""}:
            errors.append(
                "NO_BLANK_REBUILD_WHEN_VALID_PREDECESSOR_EXISTS: "
                "initial creation cannot name a predecessor"
            )
        if revision.get("predecessor_source_commit") not in {None, ""}:
            errors.append(
                "NO_BLANK_REBUILD_WHEN_VALID_PREDECESSOR_EXISTS: "
                "initial creation cannot name a predecessor source commit"
            )
        if predecessor is not None and not _inventory_is_empty(predecessor):
            errors.append(
                "NO_BLANK_REBUILD_WHEN_VALID_PREDECESSOR_EXISTS: "
                "initial creation requires an empty predecessor inventory"
            )
        if not _string_list(
            revision.get("predecessor_search_evidence"),
            nonempty=True,
        ):
            errors.append(
                "predecessor_search_evidence is required for initial creation"
            )
    elif mode == "PREDECESSOR_UNAVAILABLE_BLOCKED_UNVERIFIED":
        if publication_status != "BLOCKED_UNVERIFIED":
            errors.append("unavailable predecessor must remain BLOCKED_UNVERIFIED")
        if not _text(revision.get("predecessor_blueprint_ref")):
            errors.append("known predecessor_blueprint_ref is required when blocked")
        if not _string_list(
            revision.get("predecessor_access_blockers"),
            nonempty=True,
        ):
            errors.append(
                "predecessor_access_blockers must be a nonempty string list"
            )
        errors.append(
            "PREDECESSOR_UNAVAILABLE_BLOCKED_UNVERIFIED: "
            "successor publication is blocked until the predecessor is readable"
        )

    if predecessor is not None and successor is not None:
        detected_losses = _detected_loss_keys(predecessor, successor)
        _validate_justifications(
            revision.get("removal_or_downgrade_justifications"),
            detected_losses,
            errors,
        )
    return errors
