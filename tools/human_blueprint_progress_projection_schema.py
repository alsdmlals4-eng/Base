"""Validate and render a human Blueprint project-progress projection.

The projection is a derived exact-SHA snapshot. Goal, system, and case data
come from repository owners; work status comes directly from the existing
``project_work_kanban`` receipt. The module never executes references or
becomes a second status authority.
"""
from __future__ import annotations

import importlib.util
import re
import unicodedata
from datetime import datetime
from pathlib import Path
from types import ModuleType
from typing import Any

MATURITY_STATES = (
    "DOCUMENTED",
    "CONFIRMED",
    "IMPLEMENTED",
    "AUTOMATED_TEST_PASS",
    "RUNTIME_VERIFIED",
    "UX_VERIFIED",
    "RELEASE_READY",
)
MATURITY_RANK = {state: index for index, state in enumerate(MATURITY_STATES)}
EVIDENCE_LEVEL_SEQUENCE = (
    "E0_CONTRACT",
    "E1_STATIC",
    "E2_TEST",
    "E3_RUNTIME",
    "E4_VISUAL",
    "E5_PLAY",
    "E6_HUMAN_PLAYTEST",
)
EVIDENCE_LEVELS = frozenset(EVIDENCE_LEVEL_SEQUENCE)
EVIDENCE_RANK = {
    level: index for index, level in enumerate(EVIDENCE_LEVEL_SEQUENCE)
}
EVIDENCE_STATES = frozenset(
    {
        "PASS",
        "FAIL",
        "PARTIAL",
        "NOT_RUN",
        "BLOCKED_UNVERIFIED",
        "NOT_APPLICABLE",
    }
)
CHECK_STATES = frozenset(
    {
        "BACKLOG",
        "READY",
        "IN_PROGRESS",
        "VERIFY_REVIEW",
        "BLOCKED_UNVERIFIED",
        "USER_DECISION_REQUIRED",
        "DEFERRED",
        "PASS",
        "FAIL",
        "NOT_RUN",
        "PARTIAL",
        "NOT_APPLICABLE",
    }
)
WORK_STATES = frozenset(
    {
        "BACKLOG",
        "READY",
        "IN_PROGRESS",
        "VERIFY_REVIEW",
        "BLOCKED_UNVERIFIED",
        "USER_DECISION_REQUIRED",
        "DEFERRED",
        "DONE",
    }
)
BLOCKED_WORK_STATES = frozenset({"BLOCKED_UNVERIFIED", "DEFERRED"})
CASE_TYPES = frozenset(
    {
        "NORMAL",
        "BOUNDARY",
        "FAILURE",
        "CONFLICT",
        "INTERRUPTION",
        "RECOVERY",
        "SAVE_LOAD",
        "UI_STATE",
        "ACCESSIBILITY",
        "PERFORMANCE",
    }
)
APPLICABILITY = frozenset({"APPLICABLE", "NOT_APPLICABLE"})
SNAPSHOT_STALENESS = frozenset(
    {"CURRENT_AT_SOURCE_SHA", "STALE_SNAPSHOT", "UNVERIFIED"}
)
PROGRESS_BASIS = "INDEPENDENT_GOAL_SYSTEM_CASE_WORK_COUNTS"
SHA = re.compile(r"[0-9a-f]{40}\Z")
_WORK_TRACKING_MODULE: ModuleType | None = None


def _text(value: Any) -> bool:
    return (
        isinstance(value, str)
        and bool(value.strip())
        and not any(
            unicodedata.category(character) in {"Cc", "Cf", "Cs"}
            and character not in "\n\r\t"
            for character in value
        )
        and not (value.strip().startswith("<") and value.strip().endswith(">"))
        and value.strip().upper() not in {"TODO", "TBD", "N/A"}
    )


def _strings(value: Any, *, nonempty: bool = True) -> bool:
    return (
        isinstance(value, list)
        and (bool(value) or not nonempty)
        and all(_text(item) for item in value)
    )


def _identifier(value: Any) -> bool:
    return _text(value) and not any(character.isspace() for character in value)


def _timestamp(value: Any) -> datetime | None:
    if not _text(value):
        return None
    normalized = value[:-1] + "+00:00" if value.endswith("Z") else value
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError:
        return None
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        return None
    return parsed


def _records(
    value: Any,
    key: str,
    prefix: str,
    errors: list[str],
    *,
    nonempty: bool = True,
) -> dict[str, dict[str, Any]]:
    records: dict[str, dict[str, Any]] = {}
    if not isinstance(value, list) or (nonempty and not value):
        qualifier = "nonempty " if nonempty else ""
        errors.append(f"{prefix} must be a {qualifier}list")
        return records
    for index, item in enumerate(value):
        if not isinstance(item, dict):
            errors.append(f"{prefix}[{index}] must be an object")
            continue
        identity = item.get(key)
        if not _identifier(identity):
            errors.append(f"{prefix}[{index}].{key} must be a canonical identifier")
            continue
        if identity in records:
            errors.append(f"{prefix}: duplicate {key} {identity}")
            continue
        records[identity] = item
    return records


def _validate_ref_list(
    record: dict[str, Any],
    key: str,
    prefix: str,
    target: dict[str, dict[str, Any]],
    errors: list[str],
    *,
    nonempty: bool,
) -> list[str]:
    values = record.get(key)
    if (
        not _strings(values, nonempty=nonempty)
        or len(values or []) != len(set(values or []))
        or any(not _identifier(value) for value in values or [])
    ):
        qualifier = "nonempty " if nonempty else ""
        errors.append(f"{prefix}.{key} must be a unique {qualifier}canonical ID list")
        return []
    for value in values:
        if value not in target:
            errors.append(f"{prefix}.{key} has unresolved reference {value}")
    return values


def _validate_maturity(record: dict[str, Any], prefix: str, errors: list[str]) -> None:
    for key in ("maturity_status", "target_status"):
        if record.get(key) not in MATURITY_RANK:
            errors.append(f"{prefix}.{key} must be a known maturity state")


def _maturity_complete(record: dict[str, Any]) -> bool:
    current = record.get("maturity_status")
    target = record.get("target_status")
    return (
        current in MATURITY_RANK
        and target in MATURITY_RANK
        and MATURITY_RANK[current] >= MATURITY_RANK[target]
    )


def _validate_checklist(
    record: dict[str, Any], prefix: str, errors: list[str]
) -> dict[str, dict[str, Any]]:
    checks = _records(
        record.get("checklist"), "id", prefix + ".checklist", errors
    )
    for check_id, check in checks.items():
        check_prefix = f"{prefix}.checklist[{check_id}]"
        if not _text(check.get("text")):
            errors.append(f"{check_prefix}.text is required")
        status = check.get("status")
        if status not in CHECK_STATES:
            errors.append(f"{check_prefix}.status is invalid")
        evidence = check.get("evidence", [])
        if not _strings(evidence, nonempty=False):
            errors.append(f"{check_prefix}.evidence must be a text list")
        if status == "PASS" and not _strings(evidence):
            errors.append(f"{check_prefix}.evidence is required for PASS")
        if status == "NOT_APPLICABLE" and not _text(check.get("reason")):
            errors.append(f"{check_prefix}.reason is required for NOT_APPLICABLE")
    return checks


def _checklist_complete(record: dict[str, Any]) -> bool:
    checks = [
        check
        for check in record.get("checklist", [])
        if isinstance(check, dict) and check.get("status") != "NOT_APPLICABLE"
    ]
    return bool(checks) and all(check.get("status") == "PASS" for check in checks)


def _case_complete(case: dict[str, Any]) -> bool:
    if case.get("applicability") != "APPLICABLE" or not _maturity_complete(case):
        return False
    required = case.get("required_evidence", [])
    if not required:
        return False
    verification = {
        entry.get("level"): entry
        for entry in case.get("verification", [])
        if isinstance(entry, dict)
    }
    return all(
        verification.get(level, {}).get("status") == "PASS" for level in required
    )


def _load_work_tracking() -> ModuleType:
    global _WORK_TRACKING_MODULE
    if _WORK_TRACKING_MODULE is not None:
        return _WORK_TRACKING_MODULE
    path = Path(__file__).with_name("project_work_tracking.py")
    if not path.exists():
        raise RuntimeError(f"existing PM validator is missing: {path}")
    spec = importlib.util.spec_from_file_location("project_work_tracking", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"existing PM validator could not be loaded: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    _WORK_TRACKING_MODULE = module
    return module


def _board_tasks(
    board: Any, errors: list[str], *, expected_source_sha: str | None
) -> dict[str, dict[str, Any]]:
    if not isinstance(board, dict):
        errors.append("projection.project_work_kanban is required")
        return {}
    try:
        tracking = _load_work_tracking()
    except RuntimeError as error:
        errors.append(str(error))
        return {}
    for error in tracking.validate_tracking(
        board, phase="inspect", expected_source_sha=expected_source_sha
    ):
        errors.append(f"project_work_kanban: {error}")
    return _records(
        board.get("work_items"),
        "work_item_id",
        "projection.project_work_kanban.work_items",
        errors,
    )

