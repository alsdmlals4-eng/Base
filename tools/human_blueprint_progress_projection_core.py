"""Calculate Blueprint goal, system, case, and work completion."""
from __future__ import annotations

from typing import Any

from human_blueprint_progress_projection_schema import (
    BLOCKED_WORK_STATES,
    _case_complete,
    _checklist_complete,
    _maturity_complete,
)


def _projection_maps(
    projection: dict[str, Any],
) -> tuple[
    dict[str, dict[str, Any]],
    dict[str, dict[str, Any]],
    dict[str, dict[str, Any]],
    dict[str, dict[str, Any]],
    dict[str, dict[str, Any]],
]:
    goals = {item["goal_id"]: item for item in projection.get("goals", [])}
    systems = {item["system_id"]: item for item in projection.get("systems", [])}
    cases = {item["case_id"]: item for item in projection.get("cases", [])}
    work_items = {
        item["work_item_id"]: item
        for item in projection.get("project_work_kanban", {}).get("work_items", [])
    }
    work_links = {
        item["work_item_id"]: item
        for item in projection.get("work_item_links", [])
    }
    return goals, systems, cases, work_items, work_links


def _completion_maps(
    projection: dict[str, Any],
) -> tuple[dict[str, bool], dict[str, bool], dict[str, bool], dict[str, bool]]:
    goals, systems, cases, work_items, _ = _projection_maps(projection)
    case_completion = {
        case_id: _case_complete(case) for case_id, case in cases.items()
    }
    work_completion = {
        work_id: work.get("status") == "DONE"
        for work_id, work in work_items.items()
    }

    system_completion: dict[str, bool] = {}
    for system_id, system in systems.items():
        applicable_case_refs = [
            case_id
            for case_id in system.get("case_refs", [])
            if cases.get(case_id, {}).get("applicability") == "APPLICABLE"
        ]
        system_completion[system_id] = (
            _maturity_complete(system)
            and _checklist_complete(system)
            and all(case_completion.get(case_id, False) for case_id in applicable_case_refs)
            and all(
                work_completion.get(work_id, False)
                for work_id in system.get("work_item_refs", [])
            )
        )

    goal_completion: dict[str, bool] = {}
    for goal_id, goal in goals.items():
        applicable_case_refs = [
            case_id
            for case_id in goal.get("case_refs", [])
            if cases.get(case_id, {}).get("applicability") == "APPLICABLE"
        ]
        goal_completion[goal_id] = (
            _maturity_complete(goal)
            and _checklist_complete(goal)
            and all(
                system_completion.get(system_id, False)
                for system_id in goal.get("system_refs", [])
            )
            and all(case_completion.get(case_id, False) for case_id in applicable_case_refs)
            and all(
                work_completion.get(work_id, False)
                for work_id in goal.get("work_item_refs", [])
            )
        )
    return goal_completion, system_completion, case_completion, work_completion


def summarize_projection(projection: dict[str, Any]) -> dict[str, Any]:
    """Calculate independent counts; never average child percentages."""

    goals, systems, cases, work_items, _ = _projection_maps(projection)
    goal_completion, system_completion, case_completion, work_completion = (
        _completion_maps(projection)
    )
    applicable_cases = {
        case_id: case
        for case_id, case in cases.items()
        if case.get("applicability") == "APPLICABLE"
    }

    blocked = sum(
        work.get("status") in BLOCKED_WORK_STATES for work in work_items.values()
    )
    blocked += sum(
        any(
            check.get("status") in {"BLOCKED_UNVERIFIED", "DEFERRED"}
            for check in item.get("checklist", [])
            if isinstance(check, dict)
        )
        for item in [*goals.values(), *systems.values()]
    )
    blocked += sum(
        any(
            entry.get("status") == "BLOCKED_UNVERIFIED"
            for entry in case.get("verification", [])
            if isinstance(entry, dict)
        )
        for case in applicable_cases.values()
    )

    user_decisions = sum(
        work.get("status") == "USER_DECISION_REQUIRED"
        for work in work_items.values()
    )
    user_decisions += sum(
        any(
            check.get("status") == "USER_DECISION_REQUIRED"
            for check in item.get("checklist", [])
            if isinstance(check, dict)
        )
        for item in [*goals.values(), *systems.values()]
    )

    return {
        "goals": {
            "completed": sum(goal_completion.values()),
            "applicable": len(goals),
        },
        "systems": {
            "completed": sum(system_completion.values()),
            "applicable": len(systems),
        },
        "cases": {
            "completed": sum(
                case_completion.get(case_id, False) for case_id in applicable_cases
            ),
            "applicable": len(applicable_cases),
        },
        "work_items": {
            "completed": sum(work_completion.values()),
            "applicable": len(work_items),
        },
        "blocked": blocked,
        "user_decisions": user_decisions,
    }
