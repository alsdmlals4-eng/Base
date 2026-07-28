from __future__ import annotations

import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def replace_once(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{path}: expected one occurrence, found {count}: {old!r}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


def update_registry() -> None:
    path = ROOT / "skills/SKILL_REGISTRY.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    target = next(
        skill
        for skill in data["skills"]
        if skill["skill_id"] == "running-adversarial-review-and-refinement"
    )
    for tag in (
        "repository-wide-audit",
        "full-file-audit",
        "stale-file-audit",
        "untouched-consumer-audit",
        "prompt-drift",
    ):
        if tag not in target["trigger_tags"]:
            target["trigger_tags"].append(tag)
    target["use_when"] = [
        "설계·계획·문서·코드·데이터·UX·병합 결과 또는 저장소 전체를 실패 관점으로 공격하고 비판을 재검증한 뒤, 검증된 Finding만 최소 수정·회귀 재검사한다. repository-wide-audit에서는 현행 권한·중복·stale·고아 파일·untouched 소비자·Prompt·파생본 drift를 전문 Skill과 연결해 감사한다."
    ]
    for trigger in (
        "repository-wide stale authority",
        "untouched consumer missing",
        "prompt contract drift",
        "history treated as current",
        "search results claimed as full inventory",
    ):
        if trigger not in target["review_triggers"]:
            target["review_triggers"].append(trigger)
    target["last_reviewed_at"] = "2026-07-28"
    target["last_reviewed_commit"] = os.environ.get("GITHUB_SHA", "PR-51")
    path.write_text(
        json.dumps(data, ensure_ascii=False, separators=(",", ":")),
        encoding="utf-8",
    )


def update_orchestration() -> None:
    path = ROOT / "docs/knowledge/vertical-slice/SKILL_ORCHESTRATION_AND_EVIDENCE.md"
    replacements = [
        (
            "→ CORE_POC\n→ Slice 계약·품질·파이프라인",
            "→ 데모 핵심 위험 등록·필요 시 내부 TECHNICAL_SPIKE\n→ Demo-First Slice 계약·품질·파이프라인",
        ),
        (
            "- `CORE_POC`·버티컬 슬라이스 계약",
            "- Demo-First Vertical Slice·데모 핵심 위험·내부 Spike 계약",
        ),
        (
            "### `VERTICAL_SLICE_FULL_PROFILE`",
            "### `DEMO_FIRST_FULL_PROFILE`\n\n과거 `VERTICAL_SLICE_FULL_PROFILE`은 호환 이름이며 새 작업에서는 `DEMO_FIRST_FULL_PROFILE`로 해석한다.",
        ),
        (
            "→ 외부 Slice Validation\n→ Gate 판정",
            "→ 통합 QA·내부 플레이테스트\n→ 외부 플레이테스트·반응 조사\n→ DEMO_VALIDATION\n→ Gate 판정",
        ),
        (
            "- `CORE_POC` 계약",
            "- 데모 핵심 위험 등록부·필요 시 내부 `TECHNICAL_SPIKE` 계약",
        ),
        (
            "누락은 `MUST_FIX / SHOULD_FIX / DEFER / REJECT / BLOCKED_UNVERIFIED`로 분류한다.",
            "누락은 `MUST_FIX / SHOULD_FIX / USER_DECISION_REQUIRED / DEFER / REJECTED_CRITIQUE / BLOCKED_UNVERIFIED / ALLOWED_LEGACY`로 분류한다.",
        ),
    ]
    for old, new in replacements:
        replace_once(path, old, new)


def update_reference_config() -> None:
    path = ROOT / ".github/reference-freshness.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    canonical_name = "integrated-vertical-slice-prompt-entrypoints"
    if not any(rule.get("name") == canonical_name for rule in data["canonical_reference_rules"]):
        data["canonical_reference_rules"].append(
            {
                "name": canonical_name,
                "canonical_path": "templates/prompts/VERTICAL_SLICE_INTEGRATED_EXECUTION_PROMPT_v7.md",
                "reference_tokens": [
                    "templates/prompts/VERTICAL_SLICE_INTEGRATED_EXECUTION_PROMPT_v7.md",
                    "VERTICAL_SLICE_INTEGRATED_EXECUTION_PROMPT_v7.md",
                ],
                "required_consumers": [
                    "START_HERE.md",
                    "docs/DOCUMENTATION_MAP.md",
                    "templates/project-operations/README.md",
                ],
            }
        )
    coupled_name = "integrated-prompt-contract-test-sync"
    if not any(rule.get("name") == coupled_name for rule in data["coupled_change_rules"]):
        data["coupled_change_rules"].append(
            {
                "name": coupled_name,
                "when_changed": [
                    "templates/prompts/VERTICAL_SLICE_INTEGRATED_EXECUTION_PROMPT_v7.md"
                ],
                "exclude_when_changed": [],
                "require_all_changed": [],
                "require_any_changed": [
                    "tests/test_integrated_vertical_slice_prompt_v7.py"
                ],
            }
        )
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    update_registry()
    update_orchestration()
    update_reference_config()


if __name__ == "__main__":
    main()
