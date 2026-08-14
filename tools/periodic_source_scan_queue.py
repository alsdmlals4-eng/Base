#!/usr/bin/env python3
"""Render the deterministic Source Scan Queue from the canonical operations ledger."""

from __future__ import annotations

import argparse
import json
import re
from datetime import date, timedelta
from itertools import groupby
from pathlib import Path
from typing import Any, Sequence

CADENCE_DAYS = {
    "daily-or-weekly": 1,
    "weekly": 7,
    "monthly-or-on-demand": 30,
    "quarterly-or-when-relevant": 90,
}
CADENCE_ORDER = {name: index for index, name in enumerate(CADENCE_DAYS)}
ISSUE_TITLE = "[Periodic Source Scan Queue]"
ISSUE_MARKER = "<!-- periodic-source-scan-queue -->"
_DATE = re.compile(r"\d{4}-\d{2}-\d{2}\Z")


def parse_iso_date(value: object) -> date | None:
    if value is None:
        return None
    if not isinstance(value, str) or not _DATE.fullmatch(value):
        raise ValueError(f"invalid ISO date: {value!r}")
    try:
        parsed = date.fromisoformat(value)
    except ValueError as error:
        raise ValueError(f"invalid ISO date: {value!r}") from error
    if parsed.isoformat() != value:
        raise ValueError(f"invalid ISO date: {value!r}")
    return parsed


def _text(value: object, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} must be a non-empty string")
    return value.strip()


def _validate_source(raw: object) -> dict[str, object]:
    if not isinstance(raw, dict):
        raise ValueError("each source must be an object")
    source = dict(raw)
    source_id = _text(source.get("source_id"), "source_id")
    cadence = _text(source.get("recommended_cadence"), "recommended_cadence")
    if cadence not in CADENCE_DAYS:
        raise ValueError(f"unknown cadence for {source_id}: {cadence}")
    status = _text(source.get("status"), "status")
    last_scan = parse_iso_date(source.get("last_successful_scan_at"))
    surfaces = source.get("scan_surfaces")
    if not isinstance(surfaces, list) or any(
        not isinstance(item, str) or not item.strip() for item in surfaces
    ):
        raise ValueError(f"scan_surfaces must be a string list for {source_id}")
    source.update(
        source_id=source_id,
        recommended_cadence=cadence,
        status=status,
        last_successful_scan_at=last_scan.isoformat() if last_scan else None,
    )
    return source


def _validate_payload(raw: object) -> dict[str, object]:
    if not isinstance(raw, dict):
        raise ValueError("ledger root must be an object")
    if raw.get("schema_version") != 1:
        raise ValueError("schema_version must equal 1")
    rows = raw.get("sources")
    if not isinstance(rows, list):
        raise ValueError("sources must be a list")
    sources: list[dict[str, object]] = []
    seen: set[str] = set()
    for row in rows:
        source = _validate_source(row)
        source_id = str(source["source_id"])
        if source_id in seen:
            raise ValueError(f"duplicate source_id: {source_id}")
        seen.add(source_id)
        sources.append(source)
    payload = dict(raw)
    payload["sources"] = sources
    return payload


def load_ledger(path: Path) -> dict[str, object]:
    try:
        payload: Any = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise ValueError(f"invalid JSON ledger: {path}") from error
    return _validate_payload(payload)


def source_is_due(source: dict[str, object], today: date) -> bool:
    row = _validate_source(source)
    source_id = str(row["source_id"])
    last_scan = parse_iso_date(row.get("last_successful_scan_at"))
    if last_scan and last_scan > today:
        raise ValueError(
            f"last_successful_scan_at is in the future for {source_id}: "
            f"{last_scan.isoformat()} > {today.isoformat()}"
        )
    if row["status"] != "ACTIVE":
        return False
    return last_scan is None or (today - last_scan).days >= CADENCE_DAYS[str(row["recommended_cadence"])]


def _due_key(source: dict[str, object]) -> tuple[bool, date, int, str]:
    cadence = str(source["recommended_cadence"])
    last_scan = parse_iso_date(source.get("last_successful_scan_at"))
    next_due = date.min if last_scan is None else last_scan + timedelta(days=CADENCE_DAYS[cadence])
    return last_scan is not None, next_due, CADENCE_ORDER[cadence], str(source["source_id"])


def select_due_sources(payload: dict[str, object], today: date) -> list[dict[str, object]]:
    rows = _validate_payload(payload)["sources"]
    assert isinstance(rows, list)
    due = [row for row in rows if isinstance(row, dict) and source_is_due(row, today)]
    return sorted(due, key=_due_key)


def select_due_source_batch(
    payload: dict[str, object],
    today: date,
    batch_size: int,
) -> list[dict[str, object]]:
    """Select a bounded due batch while rotating tied priority groups by date."""

    if isinstance(batch_size, bool) or not isinstance(batch_size, int) or not 1 <= batch_size <= 20:
        raise ValueError("batch size must be between 1 and 20")
    ordered = select_due_sources(payload, today)
    rotated: list[dict[str, object]] = []
    for _, group in groupby(ordered, key=lambda row: _due_key(row)[:2]):
        tied = list(group)
        if len(tied) > 1:
            start = (today.toordinal() * batch_size) % len(tied)
            tied = tied[start:] + tied[:start]
        rotated.extend(tied)
    return rotated[:batch_size]


def _cell(value: object) -> str:
    return ("" if value is None else str(value)).replace("|", "\\|").replace("\n", " ").strip()


def render_issue_body(payload: dict[str, object], today: date) -> str:
    normalized = _validate_payload(payload)
    due = select_due_sources(normalized, today)
    lines = [
        ISSUE_MARKER,
        f"# {ISSUE_TITLE} — {today.isoformat()}",
        "",
        "> **UNVERIFIED_DISCOVERY** — 이 Issue는 검토 Queue다. 링크·제목·snippet·AI 요약은 원출처와 실제 consumer를 검증하기 전 Evidence·Canon·구현 사실이 아니다.",
        "",
        "```yaml",
        f"queue_date: {today.isoformat()}",
        f"tracking_started_at: {_cell(normalized.get('tracking_started_at')) or 'UNKNOWN'}",
        "state_owner: docs/knowledge/game-development/PERIODIC_SOURCE_OPERATIONS_LEDGER.json",
        "source_policy_owner: docs/knowledge/game-development/PERIODIC_EXTERNAL_SOURCE_WATCHLIST.md",
        "evidence_owner: docs/knowledge/game-development/EVIDENCE_BASED_GAME_DEVELOPMENT_METHOD.md",
        "queue_writes_ledger_state: false",
        "queue_writes_project_canon: false",
        "```",
        "",
        "## 1. Due Source",
        "",
    ]
    if due:
        lines += [
            "| cadence | source_id | Source | last successful scan | due reason | scan surfaces |",
            "|---|---|---|---|---|---|",
        ]
        for row in due:
            cadence = str(row["recommended_cadence"])
            last_scan = row.get("last_successful_scan_at")
            reason = "never scanned since tracking start" if last_scan is None else f">= {CADENCE_DAYS[cadence]} days since {last_scan}"
            surfaces = "; ".join(str(item).strip() for item in row["scan_surfaces"])
            lines.append(
                f"| {_cell(cadence)} | `{_cell(row['source_id'])}` | {_cell(row.get('name') or row['source_id'])} | "
                f"{_cell(last_scan or 'NEVER')} | {_cell(reason)} | {_cell(surfaces)} |"
            )
    else:
        lines.append("현재 cadence 기준 due Source 없음. 아래 확장·새 글 검토는 계속 수행한다.")
    lines += [
        "",
        "## 2. 기존 Source의 새 글·수정 글 확인",
        "",
        "- [ ] 각 due Source의 공식 recent/latest/archive/release surface를 확인했다.",
        "- [ ] 마지막 성공 scan 또는 tracking start 이후의 새 글·수정 글을 구분했다.",
        "- [ ] 제목·snippet에서 멈추지 않고 original source backtrace를 완료했다.",
        "- [ ] `published_or_updated_at`과 `checked_at`을 분리했다.",
        "- [ ] Version·region·language·medium·sample·commercial interest를 기록했다.",
        "- [ ] 실패·혼합 결과와 반례를 함께 찾았다.",
        "",
        "## 3. 신규 Source 사이트 탐색",
        "",
        "- [ ] 현재 프로젝트·Base의 반복 실패나 빈 Coverage에서 검색 질문을 만들었다.",
        "- [ ] 공식 기관·원자료·학술/현업·당사자/전문가 Source 후보를 추가 조사했다.",
        "- [ ] 기존 Watchlist·Radar·Reference와 중복·더 권위 있는 원출처 여부를 확인했다.",
        "- [ ] 새 사이트 수를 목표로 채우지 않았고 material candidate만 남겼다.",
        "- [ ] 지속적 기여가 불명확하면 `REFERENCE_ONLY` 또는 `BLOCKED_UNVERIFIED`로 닫았다.",
        "",
        "## 4. Candidate Packet",
        "",
        "```yaml",
        "candidate_id:", "source_name:", "source_role:", "original_url:",
        "published_or_updated_at:", "checked_at:", "current_question_or_failure:",
        "exact_era_region_language_medium_version:", "sample_or_method:",
        "commercial_or_creator_interest:", "claim_or_practice:",
        "original source backtrace:", "current_base_owner:", "current_project_consumer:",
        "project_canon_conflict:", "claim ceiling:", "failure_or_counterevidence:",
        "rights_or_representation_risk:", "validation artifact:",
        "rollback_or_discard_condition:",
        "disposition: ADOPT | ADAPT | TEST | PROJECT_ONLY | REFERENCE_ONLY | AVOID | IGNORE | BLOCKED_UNVERIFIED | PROMOTION_CANDIDATE",
        "```",
        "",
        "## 5. 흡수·검증·Rollback Gate",
        "",
        "- [ ] Existing Solution First: 새 Skill·Guide보다 기존 owner 흡수를 먼저 판정했다.",
        "- [ ] 실제로 바뀔 결정·파일·프로젝트 consumer가 있다.",
        "- [ ] 가장 작은 문서·테스트·데이터·프로토타입 validation artifact를 지정했다.",
        "- [ ] 적용 전 실패 조건과 rollback_or_discard_condition을 선언했다.",
        "- [ ] AI 추론, Source 주장, 프로젝트 사실, 사람 관찰을 분리했다.",
        "- [ ] 검증된 최소 변경만 PR로 제안하고 관련 회귀를 재실행했다.",
        "",
        "## 6. 완료 경계",
        "",
        "- [ ] Queue의 각 후보가 disposition으로 닫혔다.",
        "- [ ] 실제 scan을 수행한 Source만 Ledger 갱신 후보로 기록했다.",
        "- [ ] Source 기여가 실제 owner 변경과 검증으로 이어졌을 때만 contribution을 기록했다.",
        "",
        "**Queue 완료 != Ledger scan 완료. Issue check 표시 != Evidence 검증·Base 흡수·프로젝트 Canon 갱신.**",
        "",
    ]
    return "\n".join(lines)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Render a periodic source review queue from the Base ledger.")
    parser.add_argument("--ledger", type=Path, required=True)
    parser.add_argument("--date", dest="queue_date", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    queue_date = parse_iso_date(args.queue_date)
    if queue_date is None:
        parser.error("--date cannot be null")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(render_issue_body(load_ledger(args.ledger), queue_date), encoding="utf-8", newline="\n")
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
