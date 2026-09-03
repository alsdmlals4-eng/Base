"""Validate and render a human Blueprint progress projection.

The projection is a derived exact-SHA snapshot assembled from repository owners,
the AI production spec, the existing project_work_kanban receipt, and evidence.
It never executes URLs, commands, or embedded markup and it never becomes a
second project-status authority.
"""
from __future__ import annotations

import argparse
import html
import json
import re
import unicodedata
from pathlib import Path
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
BLOCKED_WORK_STATES = frozenset(
    {"BLOCKED_UNVERIFIED", "USER_DECISION_REQUIRED", "DEFERRED"}
)
EVIDENCE_LEVELS = frozenset(
    {
        "E0_CONTRACT",
        "E1_STATIC",
        "E2_TEST",
        "E3_RUNTIME",
        "E4_VISUAL",
        "E5_PLAY",
        "E6_HUMAN_PLAYTEST",
    }
)
EVIDENCE_STATES = frozenset(
    {"PASS", "FAIL", "PARTIAL", "NOT_RUN", "BLOCKED_UNVERIFIED", "NOT_APPLICABLE"}
)
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
SHA = re.compile(r"[0-9a-f]{40}\Z")


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
        or len(values) != len(set(values or []))
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
    return current in MATURITY_RANK and target in MATURITY_RANK and MATURITY_RANK[current] >= MATURITY_RANK[target]


def _case_complete(case: dict[str, Any]) -> bool:
    if case.get("applicability") != "APPLICABLE" or not _maturity_complete(case):
        return False
    verification = {
        entry.get("level"): entry
        for entry in case.get("verification", [])
        if isinstance(entry, dict)
    }
    return all(
        verification.get(level, {}).get("status") == "PASS"
        for level in case.get("required_evidence", [])
    )


def _work_complete(work: dict[str, Any]) -> bool:
    return work.get("status") == "DONE"


def validate_projection(
    projection: object,
    *,
    expected_source_sha: str | None = None,
) -> list[str]:
    """Return consistency errors without claiming external evidence is true."""

    errors: list[str] = []
    if not isinstance(projection, dict):
        return ["human Blueprint progress projection must be an object"]

    for key in (
        "project",
        "generated_at",
        "included_scope",
        "approval_status",
        "evidence_ceiling",
        "next_action",
    ):
        if not _text(projection.get(key)):
            errors.append(f"projection.{key} is required")

    source_commit = projection.get("source_commit")
    if not isinstance(source_commit, str) or SHA.fullmatch(source_commit) is None:
        errors.append("projection.source_commit must be an exact 40-character SHA")
    if expected_source_sha is not None:
        if SHA.fullmatch(expected_source_sha) is None or source_commit != expected_source_sha:
            errors.append("projection.source_commit does not match trusted expected source SHA")

    goals = _records(projection.get("goals"), "goal_id", "projection.goals", errors)
    systems = _records(projection.get("systems"), "system_id", "projection.systems", errors)
    cases = _records(projection.get("cases"), "case_id", "projection.cases", errors)
    work_items = _records(
        projection.get("work_items"), "work_item_id", "projection.work_items", errors
    )

    goal_links: dict[str, tuple[list[str], list[str], list[str]]] = {}
    for goal_id, goal in goals.items():
        prefix = f"goals[{goal_id}]"
        for key in ("title", "player_value", "next_action"):
            if not _text(goal.get(key)):
                errors.append(f"{prefix}.{key} is required")
        _validate_maturity(goal, prefix, errors)
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
        if not _strings(system.get("actual_consumers")):
            errors.append(f"{prefix}.actual_consumers must be a nonempty text list")
        _validate_maturity(system, prefix, errors)
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
            errors.append(f"{prefix}.required_evidence must be a unique known level list")
            required = []
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
            status = entry.get("status")
            if status not in EVIDENCE_STATES:
                errors.append(f"{prefix}.verification[{level}].status is invalid")
            evidence = entry.get("evidence", [])
            if not _strings(evidence, nonempty=False):
                errors.append(f"{prefix}.verification[{level}].evidence must be a text list")
            if status == "PASS" and not _strings(evidence):
                errors.append(f"{prefix}.verification[{level}].evidence is required for PASS")
            if status == "NOT_APPLICABLE" and not _text(entry.get("reason")):
                errors.append(f"{prefix}.verification[{level}].reason is required")
        for level in required:
            if level not in verification:
                errors.append(f"{prefix}: missing required evidence level {level}")
            elif verification[level].get("status") == "NOT_APPLICABLE":
                errors.append(f"{prefix}: required evidence {level} cannot be NOT_APPLICABLE")

    work_links: dict[str, tuple[list[str], list[str], list[str]]] = {}
    for work_id, work in work_items.items():
        prefix = f"work_items[{work_id}]"
        for key in ("title", "source_ref", "next_action"):
            if not _text(work.get(key)):
                errors.append(f"{prefix}.{key} is required")
        status = work.get("status")
        if status not in WORK_STATES:
            errors.append(f"{prefix}.status is invalid")
        goal_refs = _validate_ref_list(
            work, "goal_refs", prefix, goals, errors, nonempty=True
        )
        system_refs = _validate_ref_list(
            work, "system_refs", prefix, systems, errors, nonempty=False
        )
        case_refs = _validate_ref_list(
            work, "case_refs", prefix, cases, errors, nonempty=False
        )
        work_links[work_id] = (goal_refs, system_refs, case_refs)
        if status in BLOCKED_WORK_STATES:
            if not _text(work.get("blocker")):
                errors.append(f"{prefix}.blocker is required for {status}")
            if not _text(work.get("resume_condition")):
                errors.append(f"{prefix}.resume_condition is required for {status}")

    active = projection.get("active_work_item_ref")
    active_items = [
        work_id
        for work_id, work in work_items.items()
        if work.get("status") in {"IN_PROGRESS", "VERIFY_REVIEW"}
    ]
    if active is not None and (
        not _identifier(active)
        or active not in work_items
        or work_items[active].get("status") not in {"IN_PROGRESS", "VERIFY_REVIEW"}
    ):
        errors.append(
            "projection.active_work_item_ref must identify an IN_PROGRESS or VERIFY_REVIEW work item"
        )
    if active_items and active not in active_items:
        errors.append("projection.active_work_item_ref must match the current active work item")
    if sum(
        work.get("status") == "IN_PROGRESS" for work in work_items.values()
    ) > 1 or sum(
        work.get("status") == "VERIFY_REVIEW" for work in work_items.values()
    ) > 1:
        errors.append("projection work-item WIP limit exceeded")

    # Bidirectional traceability prevents a visually plausible but one-sided map.
    for goal_id, (system_refs, case_refs, work_refs) in goal_links.items():
        for system_ref in system_refs:
            if system_ref in system_links and goal_id not in system_links[system_ref][0]:
                errors.append(f"{goal_id} ↔ {system_ref} traceability is not bidirectional")
        for case_ref in case_refs:
            if case_ref in case_links and goal_id not in case_links[case_ref][1]:
                errors.append(f"{goal_id} ↔ {case_ref} traceability is not bidirectional")
        for work_ref in work_refs:
            if work_ref in work_links and goal_id not in work_links[work_ref][0]:
                errors.append(f"{goal_id} ↔ {work_ref} traceability is not bidirectional")

    for system_id, (goal_refs, case_refs, work_refs) in system_links.items():
        for case_ref in case_refs:
            if case_ref in case_links and case_links[case_ref][0] != system_id:
                errors.append(f"{system_id} ↔ {case_ref} traceability is inconsistent")
        for work_ref in work_refs:
            if work_ref in work_links and system_id not in work_links[work_ref][1]:
                errors.append(f"{system_id} ↔ {work_ref} traceability is not bidirectional")
        for goal_ref in goal_refs:
            if goal_ref in goal_links and system_id not in goal_links[goal_ref][0]:
                errors.append(f"{system_id} ↔ {goal_ref} traceability is not bidirectional")

    for case_id, (system_ref, goal_refs, work_refs) in case_links.items():
        for work_ref in work_refs:
            if work_ref in work_links and case_id not in work_links[work_ref][2]:
                errors.append(f"{case_id} ↔ {work_ref} traceability is not bidirectional")
        if system_ref in system_links and case_id not in system_links[system_ref][1]:
            errors.append(f"{case_id} ↔ {system_ref} traceability is not bidirectional")
        for goal_ref in goal_refs:
            if goal_ref in goal_links and case_id not in goal_links[goal_ref][1]:
                errors.append(f"{case_id} ↔ {goal_ref} traceability is not bidirectional")

    for work_id, (goal_refs, system_refs, case_refs) in work_links.items():
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


def summarize_projection(projection: dict[str, Any]) -> dict[str, Any]:
    """Calculate independent counts; never average child percentages."""

    goals = {
        item["goal_id"]: item
        for item in projection.get("goals", [])
        if isinstance(item, dict) and _identifier(item.get("goal_id"))
    }
    systems = {
        item["system_id"]: item
        for item in projection.get("systems", [])
        if isinstance(item, dict) and _identifier(item.get("system_id"))
    }
    cases = {
        item["case_id"]: item
        for item in projection.get("cases", [])
        if isinstance(item, dict) and _identifier(item.get("case_id"))
    }
    work_items = {
        item["work_item_id"]: item
        for item in projection.get("work_items", [])
        if isinstance(item, dict) and _identifier(item.get("work_item_id"))
    }

    case_completion = {case_id: _case_complete(case) for case_id, case in cases.items()}
    work_completion = {
        work_id: _work_complete(work) for work_id, work in work_items.items()
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

    applicable_cases = [
        case for case in cases.values() if case.get("applicability") == "APPLICABLE"
    ]
    blocked = sum(
        work.get("status") in BLOCKED_WORK_STATES for work in work_items.values()
    )
    blocked += sum(
        any(
            entry.get("status") == "BLOCKED_UNVERIFIED"
            for entry in case.get("verification", [])
            if isinstance(entry, dict)
        )
        for case in applicable_cases
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
            "completed": sum(_case_complete(case) for case in applicable_cases),
            "applicable": len(applicable_cases),
        },
        "work_items": {
            "completed": sum(work_completion.values()),
            "applicable": len(work_items),
        },
        "blocked": blocked,
        "user_decisions": sum(
            work.get("status") == "USER_DECISION_REQUIRED"
            for work in work_items.values()
        ),
    }


def _plain(value: Any) -> str:
    normalized = " ".join(str(value).split())
    normalized = html.escape(normalized, quote=False)
    for character in "\\`*_{}[]<>()|!#":
        normalized = normalized.replace(character, "\\" + character)
    return normalized


def _refs(values: Any) -> str:
    if not isinstance(values, list) or not values:
        return "—"
    return ", ".join(_plain(value) for value in values)


def _count(summary: dict[str, Any], key: str) -> str:
    entry = summary[key]
    return f"{entry['completed']} / {entry['applicable']}"


def render_projection(
    projection: dict[str, Any],
    *,
    expected_source_sha: str | None = None,
) -> str:
    """Render text-native Markdown for inclusion in the existing human PDF."""

    errors = validate_projection(
        projection, expected_source_sha=expected_source_sha
    )
    if errors:
        raise ValueError("invalid human Blueprint progress projection: " + "; ".join(errors))

    summary = summarize_projection(projection)
    work_by_id = {item["work_item_id"]: item for item in projection["work_items"]}
    case_by_id = {item["case_id"]: item for item in projection["cases"]}
    active = work_by_id.get(projection.get("active_work_item_ref"))

    lines = [
        "## 프로젝트 작업 현황",
        "",
        "`PDF_SOURCE_SNAPSHOT_NOT_LIVE_CANON` — 이 장은 repository 정본과 PM/evidence를 같은 source SHA에서 읽어 만든 파생 snapshot입니다.",
        "",
        "| 항목 | 값 |",
        "|---|---|",
        f"| 프로젝트 | {_plain(projection['project'])} |",
        f"| 포함 범위 | {_plain(projection['included_scope'])} |",
        f"| source_commit | `{_plain(projection['source_commit'])}` |",
        f"| generated_at | {_plain(projection['generated_at'])} |",
        f"| approval_status | {_plain(projection['approval_status'])} |",
        f"| evidence_ceiling | {_plain(projection['evidence_ceiling'])} |",
        "",
        "| 현황 축 | 완료 / 적용 |",
        "|---|---:|",
        f"| 프로젝트 목표 | {_count(summary, 'goals')} |",
        f"| 시스템 | {_count(summary, 'systems')} |",
        f"| 플레이 케이스 | {_count(summary, 'cases')} |",
        f"| 필수 작업 | {_count(summary, 'work_items')} |",
        f"| 차단 | {summary['blocked']} |",
        f"| 사용자 결정 필요 | {summary['user_decisions']} |",
        "",
        "### 현재 작업과 다음 행동",
        "",
    ]
    if active is None:
        lines.append("- 현재 활성 작업: 없음")
    else:
        lines.append(
            f"- 현재 활성 작업: `{_plain(active['work_item_id'])}` · {_plain(active['status'])} · {_plain(active['title'])}"
        )
        lines.append(f"- 작업 다음 행동: {_plain(active['next_action'])}")
    lines.append(f"- 프로젝트 다음 안전 작업: {_plain(projection['next_action'])}")

    lines.extend(["", "## 목표별 체크리스트", ""])
    for goal in projection["goals"]:
        completed = summarize_projection(
            {
                **projection,
                "goals": [goal],
            }
        )["goals"]["completed"] == 1
        mark = "x" if completed else " "
        lines.extend(
            [
                f"### `{_plain(goal['goal_id'])}` {_plain(goal['title'])}",
                "",
                f"- [{mark}] 목표 완료 조건 충족",
                f"- 플레이어 가치: {_plain(goal['player_value'])}",
                f"- 성숙도: `{_plain(goal['maturity_status'])}` → 목표 `{_plain(goal['target_status'])}`",
                f"- 연결 시스템: {_refs(goal['system_refs'])}",
                f"- 연결 케이스: {_refs(goal['case_refs'])}",
                f"- 연결 작업: {_refs(goal['work_item_refs'])}",
                f"- 다음 행동: {_plain(goal['next_action'])}",
                "",
            ]
        )

    lines.extend(["## 시스템 기획별 체크리스트", ""])
    for system in projection["systems"]:
        system_cases = [
            case_by_id[case_id]
            for case_id in system["case_refs"]
            if case_id in case_by_id and case_by_id[case_id]["applicability"] == "APPLICABLE"
        ]
        required_case_count = len(system_cases)
        completed_case_count = sum(_case_complete(case) for case in system_cases)
        lines.extend(
            [
                f"### `{_plain(system['system_id'])}` {_plain(system['title'])}",
                "",
                f"- 플레이어 가치: {_plain(system['player_value'])}",
                f"- 성숙도: `{_plain(system['maturity_status'])}` → 목표 `{_plain(system['target_status'])}`",
                f"- 케이스 검증: {completed_case_count} / {required_case_count}",
                f"- 정본 owner: {_plain(system['canon_owner'])}",
                f"- 실제 consumer: {_refs(system['actual_consumers'])}",
                f"- 연결 목표: {_refs(system['goal_refs'])}",
                f"- 연결 작업: {_refs(system['work_item_refs'])}",
                f"- 다음 행동: {_plain(system['next_action'])}",
                "",
            ]
        )

    lines.extend(
        [
            "## 케이스별 검증 현황",
            "",
            "| CASE_ID | 유형 | 시스템 | 적용 | 성숙도 | 필수 증거 | 결과 | 다음 행동 |",
            "|---|---|---|---|---|---|---|---|",
        ]
    )
    for case in projection["cases"]:
        if case["applicability"] == "NOT_APPLICABLE":
            result = "NOT_APPLICABLE — " + _plain(case["reason"])
        else:
            result = "PASS" if _case_complete(case) else "INCOMPLETE"
        evidence = _refs(case["required_evidence"])
        lines.append(
            "| "
            + " | ".join(
                (
                    f"`{_plain(case['case_id'])}`",
                    _plain(case["case_type"]),
                    f"`{_plain(case['system_ref'])}`",
                    _plain(case["applicability"]),
                    f"{_plain(case['maturity_status'])} → {_plain(case['target_status'])}",
                    evidence,
                    result,
                    _plain(case["next_action"]),
                )
            )
            + " |"
        )

    lines.extend(
        [
            "",
            "## 목표 ↔ 시스템 ↔ 케이스 ↔ 작업 추적",
            "",
            "| WORK_ITEM_ID | 상태 | 목표 | 시스템 | 케이스 | source |",
            "|---|---|---|---|---|---|",
        ]
    )
    for work in projection["work_items"]:
        lines.append(
            "| "
            + " | ".join(
                (
                    f"`{_plain(work['work_item_id'])}`",
                    _plain(work["status"]),
                    _refs(work["goal_refs"]),
                    _refs(work["system_refs"]),
                    _refs(work["case_refs"]),
                    _plain(work["source_ref"]),
                )
            )
            + " |"
        )

    lines.extend(
        [
            "",
            "> 성숙도, 작업 상태, evidence 결과는 서로 다른 축입니다. 문서 생성이나 자동 테스트 PASS를 runtime·UX·사용자 승인으로 해석하지 않습니다.",
        ]
    )
    return "\n".join(lines)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate and render a derived human Blueprint progress projection."
    )
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--expected-source-sha")
    parser.add_argument("--render-markdown", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    try:
        projection = json.loads(args.input.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        print(f"INVALID PROJECTION INPUT: {error}")
        return 2

    errors = validate_projection(
        projection, expected_source_sha=args.expected_source_sha
    )
    if errors:
        print("HUMAN BLUEPRINT PROGRESS PROJECTION: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("HUMAN BLUEPRINT PROGRESS PROJECTION: PASS")
    if args.render_markdown:
        print(render_projection(projection, expected_source_sha=args.expected_source_sha))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
