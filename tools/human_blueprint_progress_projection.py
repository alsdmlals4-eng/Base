"""Render and expose the validated human Blueprint progress projection API."""
from __future__ import annotations

import argparse
import html
import json
import sys
from pathlib import Path
from typing import Any

TOOLS_DIR = str(Path(__file__).resolve().parent)
if TOOLS_DIR not in sys.path:
    sys.path.insert(0, TOOLS_DIR)

from human_blueprint_progress_projection_core import (  # noqa: E402
    _case_complete,
    _completion_maps,
    _projection_maps,
    summarize_projection,
)
from human_blueprint_progress_projection_validation import (  # noqa: E402
    validate_projection,
)


def _plain(value: Any) -> str:
    normalized = " ".join(str(value).split())
    normalized = html.escape(normalized, quote=False)
    for character in "\\`*{}[]<>()|!#":
        normalized = normalized.replace(character, "\\" + character)
    return normalized


def _refs(values: Any) -> str:
    if not isinstance(values, list) or not values:
        return "—"
    return ", ".join(f"`{_plain(value)}`" for value in values)


def _count(summary: dict[str, Any], key: str) -> str:
    entry = summary[key]
    if entry["applicable"] == 0:
        return "NO_APPLICABLE_CHECKLIST"
    return f"{entry['completed']} / {entry['applicable']}"


def _check_detail(check: dict[str, Any]) -> str:
    if check.get("status") == "NOT_APPLICABLE":
        return "reason: " + _plain(check.get("reason", ""))
    evidence = check.get("evidence", [])
    return _refs(evidence)


def _verification_summary(case: dict[str, Any]) -> str:
    if case.get("applicability") == "NOT_APPLICABLE":
        return "NOT_APPLICABLE — " + _plain(case.get("reason", ""))
    verification = {
        entry.get("level"): entry
        for entry in case.get("verification", [])
        if isinstance(entry, dict)
    }
    return "; ".join(
        f"{_plain(level)}: {_plain(verification.get(level, {}).get('status', 'MISSING'))}"
        for level in case.get("required_evidence", [])
    )


def _linked_work_state(
    work_refs: list[str], work_items: dict[str, dict[str, Any]]
) -> str:
    return "; ".join(
        f"{_plain(work_id)}: {_plain(work_items.get(work_id, {}).get('status', 'MISSING'))}"
        for work_id in work_refs
    ) or "—"


def _linked_blockers(
    work_refs: list[str], work_items: dict[str, dict[str, Any]]
) -> str:
    entries: list[str] = []
    for work_id in work_refs:
        work = work_items.get(work_id, {})
        status = work.get("status")
        if status in {"BLOCKED_UNVERIFIED", "USER_DECISION_REQUIRED", "DEFERRED"}:
            entries.append(
                f"{_plain(work_id)} — {_plain(work.get('blocker', status))}; resume: {_plain(work.get('resume_condition', 'UNRECORDED'))}"
            )
    return "; ".join(entries) or "없음"


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
        raise ValueError(
            "invalid human Blueprint progress projection: " + "; ".join(errors)
        )

    summary = summarize_projection(projection)
    goals, systems, cases, work_items, work_links = _projection_maps(projection)
    goal_completion, system_completion, _, _ = _completion_maps(projection)
    board = projection["project_work_kanban"]
    active = work_items.get(board.get("active_work_item_ref"))

    lines = [
        "## 프로젝트 작업 현황",
        "",
        "`PDF_SOURCE_SNAPSHOT_NOT_LIVE_CANON` — 이 장은 repository 정본과 기존 PM/evidence를 같은 source SHA에서 읽어 만든 파생 snapshot입니다.",
        "",
        "| 항목 | 값 |",
        "|---|---|",
        f"| 프로젝트 | {_plain(projection['project'])} |",
        f"| 현재 Goal/Playable Slice | {_plain(board['goal_or_slice_issue_ref'])} |",
        f"| 포함 범위 | {_plain(projection['included_scope'])} |",
        f"| source_commit | `{_plain(projection['source_commit'])}` |",
        f"| generated_at | {_plain(projection['generated_at'])} |",
        f"| approval_status | {_plain(projection['approval_status'])} |",
        f"| evidence_ceiling | {_plain(projection['evidence_ceiling'])} |",
        f"| work_status_snapshot_source | {_plain(projection['work_status_snapshot_source'])} |",
        f"| work_status_snapshot_generated_at | {_plain(projection['work_status_snapshot_generated_at'])} |",
        f"| work_status_snapshot_staleness | {_plain(projection['work_status_snapshot_staleness'])} |",
        f"| progress_calculation_basis | {_plain(projection['progress_calculation_basis'])} |",
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
    lines.append(f"- 프로젝트 다음 안전 작업: {_plain(board['next_action'])}")

    blocked_or_decision = [
        work
        for work in work_items.values()
        if work.get("status")
        in {"BLOCKED_UNVERIFIED", "USER_DECISION_REQUIRED", "DEFERRED"}
    ]
    if blocked_or_decision:
        lines.extend(["", "#### 차단·결정 대기", ""])
        for work in blocked_or_decision:
            lines.append(
                f"- `{_plain(work['work_item_id'])}` · {_plain(work['status'])} — {_plain(work['blocker'])}; 재개: {_plain(work['resume_condition'])}"
            )

    lines.extend(
        [
            "",
            "## 프로젝트 목표 지도",
            "",
            "| GOAL_ID | 목표 | 연결 시스템 | 연결 케이스 | 연결 작업 |",
            "|---|---|---|---|---|",
        ]
    )
    for goal in goals.values():
        lines.append(
            "| "
            + " | ".join(
                (
                    f"`{_plain(goal['goal_id'])}`",
                    _plain(goal["title"]),
                    _refs(goal["system_refs"]),
                    _refs(goal["case_refs"]),
                    _refs(goal["work_item_refs"]),
                )
            )
            + " |"
        )

    lines.extend(["", "## 목표별 체크리스트", ""])
    for goal_id, goal in goals.items():
        mark = "x" if goal_completion[goal_id] else " "
        lines.extend(
            [
                f"### `{_plain(goal_id)}` {_plain(goal['title'])}",
                "",
                f"- [{mark}] 목표 완료 조건 충족",
                f"- 플레이어 가치: {_plain(goal['player_value'])}",
                f"- 성숙도: `{_plain(goal['maturity_status'])}` → 목표 `{_plain(goal['target_status'])}`",
                f"- 연결 시스템: {_refs(goal['system_refs'])}",
                f"- 연결 케이스: {_refs(goal['case_refs'])}",
                f"- 연결 작업 상태: {_linked_work_state(goal['work_item_refs'], work_items)}",
                f"- 연결 차단: {_linked_blockers(goal['work_item_refs'], work_items)}",
                f"- 다음 행동: {_plain(goal['next_action'])}",
                "",
                "| 체크 ID | 항목 | 상태 | 증거 / 사유 |",
                "|---|---|---|---|",
            ]
        )
        for check in goal["checklist"]:
            lines.append(
                f"| `{_plain(check['id'])}` | {_plain(check['text'])} | {_plain(check['status'])} | {_check_detail(check)} |"
            )
        lines.append("")

    lines.extend(["## 시스템 기획별 체크리스트", ""])
    for system_id, system in systems.items():
        mark = "x" if system_completion[system_id] else " "
        applicable_case_refs = [
            case_id
            for case_id in system["case_refs"]
            if cases[case_id]["applicability"] == "APPLICABLE"
        ]
        completed_cases = sum(_case_complete(cases[case_id]) for case_id in applicable_case_refs)
        case_count = (
            "NO_APPLICABLE_CHECKLIST"
            if not applicable_case_refs
            else f"{completed_cases} / {len(applicable_case_refs)}"
        )
        lines.extend(
            [
                f"### `{_plain(system_id)}` {_plain(system['title'])}",
                "",
                f"- [{mark}] 시스템 완료 조건 충족",
                f"- 플레이어 가치: {_plain(system['player_value'])}",
                f"- 성숙도: `{_plain(system['maturity_status'])}` → 목표 `{_plain(system['target_status'])}`",
                f"- 케이스 검증: {case_count}",
                f"- 정본 owner: {_plain(system['canon_owner'])}",
                f"- 실제 consumer: {_refs(system['actual_consumers'])}",
                f"- 연결 목표: {_refs(system['goal_refs'])}",
                f"- 연결 작업 상태: {_linked_work_state(system['work_item_refs'], work_items)}",
                f"- 연결 차단: {_linked_blockers(system['work_item_refs'], work_items)}",
                f"- 다음 행동: {_plain(system['next_action'])}",
                "",
                "| 체크 ID | 항목 | 상태 | 증거 / 사유 |",
                "|---|---|---|---|",
            ]
        )
        for check in system["checklist"]:
            lines.append(
                f"| `{_plain(check['id'])}` | {_plain(check['text'])} | {_plain(check['status'])} | {_check_detail(check)} |"
            )
        lines.append("")

    lines.extend(
        [
            "## 케이스별 검증 현황",
            "",
            "| CASE_ID | 유형 | 시스템 | 관련 목표 | 적용 | 성숙도 | 필수 증거 | 검증 결과 | 작업 상태 | 다음 행동 |",
            "|---|---|---|---|---|---|---|---|---|---|",
        ]
    )
    for case in cases.values():
        lines.append(
            "| "
            + " | ".join(
                (
                    f"`{_plain(case['case_id'])}`",
                    _plain(case["case_type"]),
                    f"`{_plain(case['system_ref'])}`",
                    _refs(case["goal_refs"]),
                    _plain(case["applicability"]),
                    f"{_plain(case['maturity_status'])} → {_plain(case['target_status'])}",
                    _refs(case["required_evidence"]),
                    _verification_summary(case),
                    _linked_work_state(case["work_item_refs"], work_items),
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
            "| WORK_ITEM_ID | 작업 | 상태 | 목표 | 시스템 | 케이스 | owner / consumer | blocker · resume · next |",
            "|---|---|---|---|---|---|---|---|",
        ]
    )
    for work_id, work in work_items.items():
        link = work_links[work_id]
        if work.get("status") in {
            "BLOCKED_UNVERIFIED",
            "USER_DECISION_REQUIRED",
            "DEFERRED",
        }:
            action = (
                f"{_plain(work['blocker'])}; resume: {_plain(work['resume_condition'])}; next: {_plain(work['next_action'])}"
            )
        else:
            action = _plain(work["next_action"])
        owner_and_consumers = (
            _plain(work["canon_owner"]) + "; " + _refs(work["actual_consumers"])
        )
        lines.append(
            "| "
            + " | ".join(
                (
                    f"`{_plain(work_id)}`",
                    _plain(work["title"]),
                    _plain(work["status"]),
                    _refs(link["goal_refs"]),
                    _refs(link["system_refs"]),
                    _refs(link["case_refs"]),
                    owner_and_consumers,
                    action,
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
