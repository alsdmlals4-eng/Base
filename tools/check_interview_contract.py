#!/usr/bin/env python3
"""Validate interview registry state, records, and the confirmation gate."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from jsonschema import Draft202012Validator


REQUIRED_HEADINGS = (
    "## 원 요청",
    "## 검증된 저장소 사실",
    "## 사용자 의도와 플레이어·사용자 경험",
    "## 결정과 근거",
    "## 범위·제외 범위",
    "## 제약·보호 대상",
    "## 산출물",
    "## 모호성 장부",
    "## 참고자료 출처와 대조",
    "## 보류·미검증",
    "## 완료 기준과 검증",
    "## 최종 한 문장 재진술",
    "## 사용자 확인 근거",
    "## 실행 프롬프트 연결",
)
MANDATORY_CHANGE_TYPES = frozenset({
    "feature",
    "game-experience",
    "art-direction",
    "architecture",
    "workflow",
    "base-change-proposal",
})


def requires_deep_interview(
    change_types: set[str] | frozenset[str],
    *,
    typo_only: bool = False,
    explicit_single_file_mechanical: bool = False,
    unchanged_validation_rerun: bool = False,
) -> bool:
    """Return the mandatory gate decision without guessing from prose."""
    if MANDATORY_CHANGE_TYPES.intersection(change_types):
        return True
    if typo_only or explicit_single_file_mechanical or unchanged_validation_rerun:
        return False
    return False


def validate_registry(root: Path, registry_path: Path, schema_path: Path) -> list[str]:
    errors: list[str] = []
    payload = json.loads(registry_path.read_text(encoding="utf-8"))
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    for error in sorted(Draft202012Validator(schema).iter_errors(payload), key=lambda item: list(item.path)):
        errors.append(f"schema:{'/'.join(map(str, error.path))}: {error.message}")

    seen: set[str] = set()
    for item in payload.get("interviews", []):
        interview_id = item.get("interview_id", "<missing>")
        if interview_id in seen:
            errors.append(f"{interview_id}: duplicate interview_id")
        seen.add(interview_id)
        record = root / item.get("record_path", "")
        if not record.is_file():
            errors.append(f"{interview_id}: missing record {record}")
            continue
        text = record.read_text(encoding="utf-8")
        for heading in REQUIRED_HEADINGS:
            if heading not in text:
                errors.append(f"{interview_id}: missing heading {heading}")

        status = item.get("status")
        confirmation = item.get("user_confirmation_ref")
        prompt_path = item.get("executable_prompt_path")
        if status == "CONFIRMED":
            if not confirmation:
                errors.append(f"{interview_id}: CONFIRMED requires user_confirmation_ref")
            if not prompt_path:
                errors.append(f"{interview_id}: CONFIRMED requires executable_prompt_path")
            elif not (root / prompt_path).is_file():
                errors.append(f"{interview_id}: missing executable prompt {prompt_path}")
        else:
            if prompt_path:
                errors.append(f"{interview_id}: executable prompt is forbidden before CONFIRMED")
            if confirmation and status not in {"SUPERSEDED"}:
                errors.append(f"{interview_id}: confirmation is inconsistent with {status}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--registry", type=Path, required=True)
    parser.add_argument("--schema", type=Path, default=Path(__file__).resolve().parents[1] / "schemas/interview-registry-v1.schema.json")
    args = parser.parse_args()
    root = args.root.resolve()
    registry = args.registry if args.registry.is_absolute() else root / args.registry
    errors = validate_registry(root, registry, args.schema.resolve())
    if errors:
        print("Interview contract validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"Interview contract is valid: {registry}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
