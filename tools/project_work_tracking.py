"""Validate and render the existing PM card receipt; never execute its references.

Authority: docs/GITHUB_WORK_ITEM_LIFECYCLE_POLICY.md section 14.
This checks recorded consistency, not the truth of external evidence or approvals.
"""
from __future__ import annotations

import html
import re
import unicodedata
from typing import Any

TASK_STATES = frozenset({"BACKLOG", "READY", "IN_PROGRESS", "VERIFY_REVIEW", "BLOCKED_UNVERIFIED", "USER_DECISION_REQUIRED", "DEFERRED", "DONE"})
CHECK_STATES = TASK_STATES - {"DONE"} | {"PASS", "FAIL", "NOT_RUN", "PARTIAL", "NOT_APPLICABLE"}
EVIDENCE_STATES = frozenset({"PASS", "FAIL", "PARTIAL", "NOT_RUN", "BLOCKED_UNVERIFIED", "NOT_APPLICABLE"})
LEVELS = frozenset({"E0_CONTRACT", "E1_STATIC", "E2_TEST", "E3_RUNTIME", "E4_VISUAL", "E5_PLAY", "E6_HUMAN_PLAYTEST"})
BLOCKED = frozenset({"BLOCKED_UNVERIFIED", "USER_DECISION_REQUIRED", "DEFERRED"})
SHA = re.compile(r"[0-9a-f]{40}\Z")
_STALE_HEAD_STATUS = "VERIFY_REVIEW_STALE_HEAD"


def text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip()) and not any(unicodedata.category(c) in {"Cc", "Cf", "Cs"} and c not in "\n\r\t" for c in value) and not (value.strip().startswith("<") and value.strip().endswith(">")) and value.strip().upper() not in {"TODO", "TBD", "N/A"}


def strings(value: Any, *, nonempty: bool = True) -> bool:
    return isinstance(value, list) and (bool(value) or not nonempty) and all(text(x) for x in value)


def choice(value: Any, allowed: Any) -> bool:
    return isinstance(value, str) and value in allowed


def _canonical_identifier(value: Any) -> bool:
    return text(value) and not any(character.isspace() for character in value)


def _records(value: Any, key: str, prefix: str, errors: list[str]) -> dict[str, dict]:
    records: dict[str, dict] = {}
    if not isinstance(value, list) or not value:
        errors.append(f"{prefix} must be a nonempty list")
        return records
    for index, item in enumerate(value):
        if not isinstance(item, dict) or not text(item.get(key)):
            errors.append(f"{prefix}[{index}].{key} is required")
            continue
        identity = item[key]
        if not _canonical_identifier(identity):
            errors.append(f"{prefix}[{index}].{key} must be a canonical identifier without whitespace")
            continue
        if identity in records:
            errors.append(f"{prefix}: duplicate {key} {identity}")
        records[identity] = item
    return records


def _trusted_head(value: Any) -> str | None:
    return value if isinstance(value, str) and SHA.fullmatch(value) is not None else None


def _render_status(task: dict, expected_head_sha: str | None) -> str:
    trusted_head = _trusted_head(expected_head_sha)
    if (
        trusted_head is not None
        and task.get("status") == "DONE"
        and task.get("verified_head_sha") != trusted_head
    ):
        return _STALE_HEAD_STATUS
    status = task.get("status")
    return status if isinstance(status, str) else "INVALID"


def progress(board: dict, *, expected_head_sha: str | None = None) -> tuple[int, int]:
    """Count required DONE work items, excluding stale-head claims in derived views."""
    items = board["work_items"]
    return sum(_render_status(item, expected_head_sha) == "DONE" for item in items), len(items)


def validate_tracking(
    board: object,
    *,
    phase: str = "start",
    expected_source_sha: str | None = None,
    expected_head_sha: str | None = None,
) -> list[str]:
    errors: list[str] = []
    if not choice(phase, {"start", "resume", "closeout", "inspect"}):
        return ["phase must be start, resume, closeout or inspect"]
    if not isinstance(board, dict):
        return ["project_work_kanban is required for L1+ execution"]
    for key in ("goal_or_slice_issue_ref", "next_action"):
        if not text(board.get(key)):
            errors.append(f"project_work_kanban.{key} is required")
    source = board.get("source_main_sha")
    if not isinstance(source, str) or SHA.fullmatch(source) is None:
        errors.append("project_work_kanban.source_main_sha must be an exact 40-character SHA")
    if expected_source_sha is not None:
        if not isinstance(expected_source_sha, str) or SHA.fullmatch(expected_source_sha) is None or source != expected_source_sha:
            errors.append("project_work_kanban.source_main_sha does not match trusted expected source")

    trusted_head_valid = _trusted_head(expected_head_sha) is not None
    if phase == "closeout" and not trusted_head_valid:
        errors.append("expected_head_sha from the trusted final-head caller is required for closeout")

    tasks = _records(board.get("work_items"), "work_item_id", "project_work_kanban.work_items", errors)
    refs = board.get("work_item_refs")
    if not strings(refs) or any(not _canonical_identifier(ref) for ref in refs) or len(refs) != len(set(refs)) or set(refs) != set(tasks):
        errors.append("project_work_kanban.work_item_refs must match unique canonical required work_items exactly")
    active = board.get("active_work_item_ref")
    in_progress = [key for key, task in tasks.items() if task.get("status") == "IN_PROGRESS"]
    reviewing = [key for key, task in tasks.items() if task.get("status") == "VERIFY_REVIEW"]
    active_candidates = in_progress + reviewing
    if len(in_progress) > 1 or len(reviewing) > 1:
        errors.append("project_work_kanban WIP limit exceeded (IN_PROGRESS=1, VERIFY_REVIEW=1)")
    if active is not None and (
        not _canonical_identifier(active)
        or active not in tasks
        or not choice(tasks[active].get("status"), {"IN_PROGRESS", "VERIFY_REVIEW"})
    ):
        errors.append("active_work_item_ref must identify a canonical IN_PROGRESS or VERIFY_REVIEW task")
    if active_candidates and active not in active_candidates:
        errors.append("active_work_item_ref must match the current active task")
    if phase in {"start", "resume"} and not active_candidates:
        errors.append(f"{phase} requires one IN_PROGRESS or VERIFY_REVIEW task; record blockers without authorizing execution")
    if phase == "closeout" and (active is not None or not tasks or any(t.get("status") != "DONE" for t in tasks.values())):
        errors.append("closeout requires all required work_items DONE and no active task")
    if phase == "closeout" and board.get("next_action") != "STOP_APPROVED_SCOPE_COMPLETE":
        errors.append("closeout.next_action must be STOP_APPROVED_SCOPE_COMPLETE; new scope needs its own approval")

    dependencies: dict[str, list[str]] = {}
    for identity, task in tasks.items():
        prefix = f"work_items[{identity}]"
        status = task.get("status")
        if not choice(status, TASK_STATES):
            errors.append(f"{prefix}.status is invalid")
        for key in ("title", "canon_owner", "next_action"):
            if not text(task.get(key)):
                errors.append(f"{prefix}.{key} is required")
        if not strings(task.get("actual_consumers")):
            errors.append(f"{prefix}.actual_consumers is required")
        deps = task.get("depends_on")
        if not strings(deps, nonempty=False) or any(not _canonical_identifier(dep) for dep in deps) or len(deps) != len(set(deps)):
            errors.append(f"{prefix}.depends_on must be unique canonical dependency IDs")
            deps = []
        dependencies[identity] = deps
        for dep in deps:
            if dep not in tasks or dep == identity:
                errors.append(f"{prefix}: unknown or self dependency {dep}")
            elif choice(status, {"READY", "IN_PROGRESS", "VERIFY_REVIEW", "DONE"}) and tasks[dep].get("status") != "DONE":
                errors.append(f"{prefix}: dependency {dep} is not DONE")
        if choice(status, BLOCKED):
            for key in ("blocker", "resume_condition"):
                if not text(task.get(key)):
                    errors.append(f"{prefix}.{key} is required for {status}")
        checks = _records(task.get("checklist"), "id", prefix + ".checklist", errors)
        ac = task.get("acceptance_criteria")
        if not strings(ac) or any(not _canonical_identifier(item) for item in ac) or len(ac) != len(set(ac)):
            errors.append(f"{prefix}.acceptance_criteria must contain unique canonical required checklist IDs")
            ac = []
        for acceptance in ac:
            if acceptance not in checks:
                errors.append(f"{prefix}: missing acceptance criterion {acceptance}")
            elif checks[acceptance].get("status") == "NOT_APPLICABLE":
                errors.append(f"{prefix}: required acceptance {acceptance} cannot be NOT_APPLICABLE")
        applicable = 0
        passed = 0
        for check_id, check in checks.items():
            check_status = check.get("status")
            if not choice(check_status, CHECK_STATES) or not text(check.get("text")):
                errors.append(f"{prefix}.checklist[{check_id}] requires valid status and text")
            if "evidence" in check and not strings(check["evidence"], nonempty=False):
                errors.append(f"{prefix}.checklist[{check_id}].evidence must be a list of text")
            if check_status == "NOT_APPLICABLE":
                if not text(check.get("reason")):
                    errors.append(f"{prefix}.checklist[{check_id}].reason is required")
            else:
                applicable += 1
            if check_status == "PASS":
                passed += 1
                if not strings(check.get("evidence")):
                    errors.append(f"{prefix}.checklist[{check_id}].evidence is required for PASS")
        verification = _records(task.get("verification"), "level", prefix + ".verification", errors)
        required = task.get("required_evidence")
        if not strings(required) or any(not _canonical_identifier(level) for level in required) or len(required) != len(set(required)) or any(level not in LEVELS for level in required):
            errors.append(f"{prefix}.required_evidence must be unique known evidence levels")
            required = []
        for level, entry in verification.items():
            if level not in LEVELS or not choice(entry.get("status"), EVIDENCE_STATES):
                errors.append(f"{prefix}.verification[{level}] is invalid")
            if "evidence" in entry and not strings(entry["evidence"], nonempty=False):
                errors.append(f"{prefix}.verification[{level}].evidence must be a list of text")
            if entry.get("status") == "PASS" and not strings(entry.get("evidence")):
                errors.append(f"{prefix}.verification[{level}].evidence is required for PASS")
            if entry.get("status") == "NOT_APPLICABLE" and not text(entry.get("reason")):
                errors.append(f"{prefix}.verification[{level}].reason is required")
        for level in required:
            if level not in verification:
                errors.append(f"{prefix}: missing required evidence level {level}")
            elif verification[level].get("status") == "NOT_APPLICABLE":
                errors.append(f"{prefix}: required evidence {level} cannot be waived")
        if status == "DONE":
            if any(entry.get("status") in ("FAIL", "BLOCKED_UNVERIFIED") for entry in verification.values()):
                errors.append(f"{prefix}: DONE contradicts recorded failed or blocked verification")
            head = task.get("verified_head_sha")
            if not isinstance(head, str) or SHA.fullmatch(head) is None:
                errors.append(f"{prefix}: DONE requires verified_head_sha for the recorded evidence")
            elif phase == "closeout" and trusted_head_valid and head != expected_head_sha:
                errors.append(f"{prefix}.verified_head_sha does not match trusted expected head")
            if applicable == 0 or passed != applicable:
                errors.append(f"{prefix}: DONE requires every applicable checklist item PASS")
            for level in required:
                if verification.get(level, {}).get("status") != "PASS":
                    errors.append(f"{prefix}: DONE requires {level} PASS")
            for counter in ("must_fix_remaining", "blocked_unverified_remaining", "user_decision_required_remaining"):
                if type(task.get(counter)) is not int or task[counter] != 0:
                    errors.append(f"{prefix}: DONE requires {counter}=0")
            if task.get("repository_readback") != "PASS" or not strings(task.get("readback_evidence")) or not text(task.get("rollback")):
                errors.append(f"{prefix}: DONE requires repository_readback PASS, readback_evidence and rollback")

    pending = dict(dependencies)
    resolved: set[str] = set()
    while pending:
        ready = [key for key, deps in pending.items() if all(dep in resolved for dep in deps)]
        if not ready:
            errors.append("work_items dependency cycle or unresolved dependency")
            break
        for key in ready:
            resolved.add(key)
            del pending[key]
    if "progress_summary" in board:
        summary = board["progress_summary"]
        completed = sum(task.get("status") == "DONE" for task in tasks.values())
        if not isinstance(summary, dict) or any(type(summary.get(k)) is not int for k in ("completed_items", "applicable_items")) or summary.get("completed_items") != completed or summary.get("applicable_items") != len(tasks):
            errors.append("project_work_kanban.progress_summary differs from required child DONE count")
        if isinstance(summary, dict) and "display" in summary and summary["display"] != f"{completed} / {len(tasks)}":
            errors.append("project_work_kanban.progress_summary.display differs from required child DONE count")
    return errors


def _plain(value: str) -> str:
    value = html.escape(" ".join(value.split()), quote=False)
    for char in "\\`*_{}[]<>()|!#":
        value = value.replace(char, "\\" + char)
    return value


def render_tracking(board: dict, *, expected_head_sha: str | None = None) -> str:
    """Render shape-validated data without turning receipt text into instructions."""
    completed, total = progress(board, expected_head_sha=expected_head_sha)
    lines = [f"## PM 작업 체크리스트 — {completed} / {total}", "", "이 표는 기록 일관성 검사를 통과한 파생 뷰이며 실제 증거 검수를 대신하지 않습니다.", ""]
    effective_statuses: list[str] = []
    for task in board["work_items"]:
        status = _render_status(task, expected_head_sha)
        effective_statuses.append(status)
        checks = [c for c in task["checklist"] if c["status"] != "NOT_APPLICABLE"]
        passed = sum(c["status"] == "PASS" for c in checks)
        count = f"{passed} / {len(checks)}" if checks else "NO_APPLICABLE_CHECKLIST"
        mark = "x" if status == "DONE" else " "
        lines.append(f"- [{mark}] {_plain(task['work_item_id'])} · {status} · {_plain(task['title'])} ({count})")
        if status == _STALE_HEAD_STATUS:
            lines.append("  다음: trusted expected HEAD에서 evidence와 repository readback을 재검증")
        elif status in BLOCKED:
            lines.append(f"  차단: {_plain(task['blocker'])}; 재개: {_plain(task['resume_condition'])}")
        elif status != "DONE":
            lines.append(f"  다음: {_plain(task['next_action'])}")
    remaining = [status for status in effective_statuses if status != "DONE"]
    if _STALE_HEAD_STATUS in remaining:
        safe_next = "trusted expected HEAD에서 stale evidence와 repository readback 재검증"
    elif remaining and all(status in BLOCKED for status in remaining):
        safe_next = "기록된 차단 해제 조건을 검증한 뒤 receipt 재검사"
    else:
        safe_next = _plain(board["next_action"])
    lines.extend(["", f"다음 안전 작업: {safe_next}"])
    return "\n".join(lines)
