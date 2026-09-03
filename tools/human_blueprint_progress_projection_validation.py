"""Validate one human Blueprint progress projection."""
from __future__ import annotations

from typing import Any

from human_blueprint_progress_projection_schema import (
    APPLICABILITY,
    CASE_TYPES,
    EVIDENCE_LEVELS,
    EVIDENCE_RANK,
    EVIDENCE_STATES,
    PROGRESS_BASIS,
    SHA,
    SNAPSHOT_STALENESS,
    _board_tasks,
    _identifier,
    _records,
    _strings,
    _text,
    _timestamp,
    _validate_checklist,
    _validate_maturity,
    _validate_ref_list,
)


def validate_projection(
    projection: object,
    *,
    expected_source_sha: str | None = None,
) -> list[str]:
    """Return consistency errors without claiming that external evidence is true."""

    errors: list[str] = []
    if not isinstance(projection, dict):
        return ["human Blueprint progress projection must be an object"]

    for forbidden in ("work_items", "active_work_item_ref", "next_action"):
        if forbidden in projection:
            errors.append(
                f"projection.{forbidden} is forbidden; project_work_kanban is the direct work-status source"
            )

    for key in (
        "project",
        "included_scope",
        "approval_status",
        "work_status_snapshot_source",
    ):
        if not _text(projection.get(key)):
            errors.append(f"projection.{key} is required")

    generated_at = _timestamp(projection.get("generated_at"))
    if generated_at is None:
        errors.append("projection.generated_at must be an ISO-8601 timestamp with timezone")
    snapshot_generated_at = _timestamp(
        projection.get("work_status_snapshot_generated_at")
    )
    if snapshot_generated_at is None:
        errors.append(
            "projection.work_status_snapshot_generated_at must be an ISO-8601 timestamp with timezone"
        )
    if (
        generated_at is not None
        and snapshot_generated_at is not None
        and snapshot_generated_at > generated_at
    ):
        errors.append(
            "projection.work_status_snapshot_generated_at cannot be later than generated_at"
        )

    source_commit = projection.get("source_commit")
    source_valid = isinstance(source_commit, str) and SHA.fullmatch(source_commit)
    if not source_valid:
        errors.append("projection.source_commit must be an exact 40-character SHA")
    if expected_source_sha is not None:
        if (
            not isinstance(expected_source_sha, str)
            or SHA.fullmatch(expected_source_sha) is None
            or source_commit != expected_source_sha
        ):
            errors.append(
                "projection.source_commit does not match trusted expected source SHA"
            )

    ceiling = projection.get("evidence_ceiling")
    ceiling_rank = EVIDENCE_RANK.get(ceiling)
    if ceiling_rank is None:
        errors.append("projection.evidence_ceiling must be a known evidence level")

    staleness = projection.get("work_status_snapshot_staleness")
    if staleness not in SNAPSHOT_STALENESS:
        errors.append("projection.work_status_snapshot_staleness is invalid")
    if expected_source_sha is not None and staleness != "CURRENT_AT_SOURCE_SHA":
        errors.append(
            "projection.work_status_snapshot_staleness must be CURRENT_AT_SOURCE_SHA for a current publication"
        )
    if projection.get("progress_calculation_basis") != PROGRESS_BASIS:
        errors.append(
            f"projection.progress_calculation_basis must be {PROGRESS_BASIS}"
        )

    board = projection.get("project_work_kanban")
    work_items = _board_tasks(
        board, errors, expected_source_sha=source_commit if source_valid else None
    )
    if source_valid and isinstance(board, dict) and board.get("source_main_sha") != source_commit:
        errors.append(
            "project_work_kanban.source_main_sha does not match projection.source_commit"
        )

    goals = _records(projection.get("goals"), "goal_id", "projection.goals", errors)
    systems = _records(
        projection.get("systems"), "system_id", "projection.systems", errors
    )
    cases = _records(projection.get("cases"), "case_id", "projection.cases", errors)
    work_links = _records(
        projection.get("work_item_links"),
        "work_item_id",
        "projection.work_item_links",
        errors,
        nonempty=bool(work_items),
    )
    if set(work_links) != set(work_items):
        errors.append(
            "projection.work_item_links IDs must match project_work_kanban.work_items exactly"
        )

    goal_links: dict[str, tuple[list[str], list[str], list[str]]] = {}
    for goal_id, goal in goals.items():
        prefix = f"goals[{goal_id}]"
        for key in ("title", "player_value", "next_action"):
            if not _text(goal.get(key)):
                errors.append(f"{prefix}.{key} is required")
        _validate_maturity(goal, prefix, errors)
        _validate_checklist(goal, prefix, errors)
        system_refs = _validate_ref_list(
            goal, "system_refs", prefix, systems, errors, nonempty=True
        )
        case_refs = _validate_ref_list(
            goal, "case_refs", prefix, cases, errors, nonempty=True
        )
        work_refs = _validate_ref_list(
            goal, "work_item_refs", prefix, work_items, errors, nonempty=True
        )
        goal_links[goal_id] = (system_refs, case_refs, work_refs)

    system_links: dict[str, tuple[list[str], list[str], list[str]]] = {}
    for system_id, system in systems.items():
        prefix = f"systems[{system_id}]"
        for key in ("title", "player_value", "canon_owner", "next_action"):
            if not _text(system.get(key)):
                errors.append(f"{prefix}.{key} is required")
        consumers = system.get("actual_consumers")
        if (
            not _strings(consumers)
            or len(consumers or []) != len(set(consumers or []))
        ):
            errors.append(
                f"{prefix}.actual_consumers must be a unique nonempty text list"
            )
        _validate_maturity(system, prefix, errors)
        _validate_checklist(system, prefix, errors)
        goal_refs = _validate_ref_list(
            system, "goal_refs", prefix, goals, errors, nonempty=True
        )
        case_refs = _validate_ref_list(
            system, "case_refs", prefix, cases, errors, nonempty=True
        )
        work_refs = _validate_ref_list(
            system, "work_item_refs", prefix, work_items, errors, nonempty=True
        )
        system_links[system_id] = (goal_refs, case_refs, work_refs)

    case_links: dict[str, tuple[str | None, list[str], list[str]]] = {}
    for case_id, case in cases.items():
        prefix = f"cases[{case_id}]"
        for key in ("title", "next_action"):
            if not _text(case.get(key)):
                errors.append(f"{prefix}.{key} is required")
        if case.get("case_type") not in CASE_TYPES:
            errors.append(f"{prefix}.case_type is invalid")
        system_ref = case.get("system_ref")
        if not _identifier(system_ref) or system_ref not in systems:
            errors.append(f"{prefix}.system_ref has unresolved reference {system_ref}")
            system_ref = None
        goal_refs = _validate_ref_list(
            case, "goal_refs", prefix, goals, errors, nonempty=True
        )
        work_refs = _validate_ref_list(
            case, "work_item_refs", prefix, work_items, errors, nonempty=False
        )
        case_links[case_id] = (system_ref, goal_refs, work_refs)
        _validate_maturity(case, prefix, errors)

        applicability = case.get("applicability")
        if applicability not in APPLICABILITY:
            errors.append(f"{prefix}.applicability is invalid")
        if applicability == "NOT_APPLICABLE" and not _text(case.get("reason")):
            errors.append(f"{prefix}.reason is required for NOT_APPLICABLE")

        required = case.get("required_evidence")
        if (
            not _strings(required, nonempty=False)
            or len(required or []) != len(set(required or []))
            or any(level not in EVIDENCE_LEVELS for level in required or [])
        ):
            errors.append(
                f"{prefix}.required_evidence must be a unique known level list"
            )
            required = []
        if applicability == "APPLICABLE" and not required:
            errors.append(f"{prefix}: applicable case requires nonempty required_evidence")
        if ceiling_rank is not None:
            for level in required:
                if EVIDENCE_RANK[level] > ceiling_rank:
                    errors.append(
                        f"{prefix}.required_evidence {level} exceeds evidence ceiling {ceiling}"
                    )

        verification = _records(
            case.get("verification"),
            "level",
            prefix + ".verification",
            errors,
            nonempty=False,
        )
        for level, entry in verification.items():
            if level not in EVIDENCE_LEVELS:
                errors.append(f"{prefix}.verification[{level}] uses an unknown level")
                continue
            status = entry.get("status")
            if status not in EVIDENCE_STATES:
                errors.append(f"{prefix}.verification[{level}].status is invalid")
            evidence = entry.get("evidence", [])
            if not _strings(evidence, nonempty=False):
                errors.append(
                    f"{prefix}.verification[{level}].evidence must be a text list"
                )
            if status == "PASS" and not _strings(evidence):
                errors.append(
                    f"{prefix}.verification[{level}].evidence is required for PASS"
                )
            if status == "NOT_APPLICABLE" and not _text(entry.get("reason")):
                errors.append(f"{prefix}.verification[{level}].reason is required")
            if (
                status == "PASS"
                and ceiling_rank is not None
                and EVIDENCE_RANK[level] > ceiling_rank
            ):
                errors.append(
                    f"{prefix}.verification[{level}] PASS exceeds evidence ceiling {ceiling}"
                )
        for level in required:
            if level not in verification:
                errors.append(f"{prefix}: missing required evidence level {level}")
            elif verification[level].get("status") == "NOT_APPLICABLE":
                errors.append(
                    f"{prefix}: required evidence {level} cannot be NOT_APPLICABLE"
                )

    link_map: dict[str, tuple[list[str], list[str], list[str]]] = {}
    for work_id, link in work_links.items():
        prefix = f"work_item_links[{work_id}]"
        goal_refs = _validate_ref_list(
            link, "goal_refs", prefix, goals, errors, nonempty=True
        )
        system_refs = _validate_ref_list(
            link, "system_refs", prefix, systems, errors, nonempty=False
        )
        case_refs = _validate_ref_list(
            link, "case_refs", prefix, cases, errors, nonempty=False
        )
        link_map[work_id] = (goal_refs, system_refs, case_refs)

    # Every relationship must be recoverable from both directions.
    for goal_id, (system_refs, case_refs, work_refs) in goal_links.items():
        for system_ref in system_refs:
            if system_ref in system_links and goal_id not in system_links[system_ref][0]:
                errors.append(f"{goal_id} ↔ {system_ref} traceability is not bidirectional")
        for case_ref in case_refs:
            if case_ref in case_links and goal_id not in case_links[case_ref][1]:
                errors.append(f"{goal_id} ↔ {case_ref} traceability is not bidirectional")
        for work_ref in work_refs:
            if work_ref in link_map and goal_id not in link_map[work_ref][0]:
                errors.append(f"{goal_id} ↔ {work_ref} traceability is not bidirectional")

    for system_id, (goal_refs, case_refs, work_refs) in system_links.items():
        for goal_ref in goal_refs:
            if goal_ref in goal_links and system_id not in goal_links[goal_ref][0]:
                errors.append(f"{system_id} ↔ {goal_ref} traceability is not bidirectional")
        for case_ref in case_refs:
            if case_ref in case_links and case_links[case_ref][0] != system_id:
                errors.append(f"{system_id} ↔ {case_ref} traceability is inconsistent")
        for work_ref in work_refs:
            if work_ref in link_map and system_id not in link_map[work_ref][1]:
                errors.append(f"{system_id} ↔ {work_ref} traceability is not bidirectional")

    for case_id, (system_ref, goal_refs, work_refs) in case_links.items():
        if system_ref in system_links and case_id not in system_links[system_ref][1]:
            errors.append(f"{case_id} ↔ {system_ref} traceability is not bidirectional")
        for goal_ref in goal_refs:
            if goal_ref in goal_links and case_id not in goal_links[goal_ref][1]:
                errors.append(f"{case_id} ↔ {goal_ref} traceability is not bidirectional")
        for work_ref in work_refs:
            if work_ref in link_map and case_id not in link_map[work_ref][2]:
                errors.append(f"{case_id} ↔ {work_ref} traceability is not bidirectional")

    for work_id, (goal_refs, system_refs, case_refs) in link_map.items():
        for goal_ref in goal_refs:
            if goal_ref in goal_links and work_id not in goal_links[goal_ref][2]:
                errors.append(f"{work_id} ↔ {goal_ref} traceability is not bidirectional")
        for system_ref in system_refs:
            if system_ref in system_links and work_id not in system_links[system_ref][2]:
                errors.append(f"{work_id} ↔ {system_ref} traceability is not bidirectional")
        for case_ref in case_refs:
            if case_ref in case_links and work_id not in case_links[case_ref][2]:
                errors.append(f"{work_id} ↔ {case_ref} traceability is not bidirectional")

    return errors

