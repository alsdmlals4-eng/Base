#!/usr/bin/env python3
"""Apply the approved Base v9.4 AI operations migration deterministically."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "skills/SKILL_REGISTRY.json"
PROPOSAL_REGISTRY = ROOT / "[수정제안서]/PROPOSAL_REGISTRY.json"
SUMMARY_PATH = ROOT / "docs/generated/BASE_ACTIVE_SKILLS.md"
LOCK_PATH = ROOT / "base-v9.4.lock.json"

SKILL_ID = "optimizing-ai-model-and-prompt-costs"
IMPLEMENTATION_PR = 118
BASELINE_COMMIT = "b5de93ff1c5544b962b4e23c21acbeb103bcbb07"


def canonical_minified(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":")) + "\n"


def canonical_pretty(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2) + "\n"


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_if_changed(path: Path, text: str) -> bool:
    current = path.read_text(encoding="utf-8") if path.is_file() else None
    if current == text:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")
    return True


def append_once(path: Path, marker: str, section: str) -> bool:
    text = path.read_text(encoding="utf-8")
    if marker in text:
        return False
    suffix = "" if text.endswith("\n") else "\n"
    return write_if_changed(path, text + suffix + "\n" + section.rstrip() + "\n")


def add_unique(values: list[str], additions: list[str]) -> None:
    for value in additions:
        if value not in values:
            values.append(value)


def find_skill(registry: dict[str, Any], skill_id: str) -> dict[str, Any]:
    for skill in registry["skills"]:
        if skill["skill_id"] == skill_id:
            return skill
    raise KeyError(skill_id)


def update_registry() -> bool:
    registry = load_json(REGISTRY_PATH)
    existing = {item["skill_id"] for item in registry["skills"]}
    if SKILL_ID not in existing:
        registry["skills"].append(
            {
                "skill_id": SKILL_ID,
                "layer": "specialist",
                "discipline": "ai-model-cost-operations",
                "path": "skills/optimizing-ai-model-and-prompt-costs/SKILL.md",
                "status": "ACTIVE",
                "load_by_default": False,
                "trigger_tags": [
                    "model-recommendation",
                    "model-effort-routing",
                    "luna-terra-sol",
                    "reasoning-effort",
                    "prompt-caching",
                    "cacheable-prefix",
                    "ai-cost-estimation",
                    "usage-measurement",
                    "provider-profile",
                    "cost-recalibration",
                ],
                "use_when": [
                    "AI 작업의 품질 위험·재시도·재작업을 포함해 모델과 추론 단계를 추천하거나, 반복 Prompt의 cacheable prefix를 설계하고 실제 usage와 순비용으로 재보정한다."
                ],
                "do_not_use_when": [
                    "모델 선택권이 없거나 한 번뿐인 짧은 요청이거나, 검증 책임이 비용보다 우선하는 고위험 작업에서 하향 모델을 강제하려는 경우다."
                ],
                "learning_log": "skills/SKILL_LEARNING_LOG.md",
                "review_triggers": [
                    "가장 싼 모델 우선",
                    "숨은 고위험 판단 하향 분류",
                    "provider option 가용성 환각",
                    "stale 가격·TTL·할인율 상수화",
                    "민감 정보 cache prefix 포함",
                    "재시도·상위 모델 재작업 비용 누락",
                    "검증 없는 절감률 보장",
                    "실제 모델 자동 변경 주장",
                ],
                "last_reviewed_at": "2026-08-01",
                "last_reviewed_commit": BASELINE_COMMIT,
                "knowledge_state": "HYPOTHESIS",
            }
        )

    intake = find_skill(registry, "managing-project-intake-and-work-contract")
    add_unique(
        intake["trigger_tags"],
        [
            "instruction-authority",
            "interface-first-prompt",
            "context-curation",
            "artifact-first-delivery",
        ],
    )
    add_unique(
        intake["review_triggers"],
        [
            "hard constraint weakened",
            "user decision hidden as default",
            "context counterevidence removed",
            "artifact claim overreach",
        ],
    )

    simplifying = find_skill(registry, "simplifying-skill-bodies")
    add_unique(
        simplifying["trigger_tags"],
        ["instruction-budget", "example-as-fixture", "golden-set-preservation"],
    )
    add_unique(
        simplifying["review_triggers"],
        ["example fixture deleted", "judgment space overconstrained", "safety rule hidden"],
    )

    ui = find_skill(registry, "auditing-and-refining-ui-art")
    add_unique(
        ui["trigger_tags"],
        [
            "ui-motion-design",
            "animation-interruption",
            "instant-complete",
            "reduced-motion",
            "motion-feedback-budget",
        ],
    )
    add_unique(
        ui["review_triggers"],
        [
            "animation owns domain result",
            "motion interruption duplicates result",
            "reduced motion loses information",
            "repetition fatigue untested",
        ],
    )

    return write_if_changed(REGISTRY_PATH, canonical_minified(registry))


def update_proposals() -> bool:
    registry = load_json(PROPOSAL_REGISTRY)
    approvals = {
        "BCP-2026-003-ai-model-prompt-cost-optimization": "https://github.com/alsdmlals4-eng/Base/issues/113",
        "BCP-2026-004-ai-instruction-context-ui-motion": "https://github.com/alsdmlals4-eng/Base/issues/115",
    }
    for proposal in registry["proposals"]:
        proposal_id = proposal["proposal_id"]
        if proposal_id in approvals:
            proposal["status"] = "APPROVED_FOR_IMPLEMENTATION"
            proposal["approval_ref"] = approvals[proposal_id]
            proposal["implementation_pr"] = IMPLEMENTATION_PR
    changed = write_if_changed(PROPOSAL_REGISTRY, canonical_pretty(registry))

    for proposal_id, approval_ref in approvals.items():
        path = ROOT / "[수정제안서]" / proposal_id / "PROPOSAL.md"
        text = path.read_text(encoding="utf-8")
        text = text.replace("- 상태: `SUBMITTED`", "- 상태: `APPROVED_FOR_IMPLEMENTATION`")
        marker = "## Base v9.4 구현 연결"
        if marker not in text:
            text += (
                "\n## Base v9.4 구현 연결\n\n"
                f"- approval_ref: `{approval_ref}`\n"
                f"- implementation_pr: `https://github.com/alsdmlals4-eng/Base/pull/{IMPLEMENTATION_PR}`\n"
                "- 상태 전환 위치: 제안 PR이 아니라 승인된 별도 Base v9.4 구현 PR\n"
                "- BCP-2026-003과 BCP-2026-004는 같은 후보 PR을 사용하지만 Skill·Method·Reference·Test 책임을 분리한다.\n"
            )
        changed = write_if_changed(path, text) or changed
    return changed


def update_skill_and_method_consumers() -> bool:
    changed = False
    sections: dict[str, tuple[str, str]] = {
        "skills/managing-project-intake-and-work-contract/SKILL.md": (
            "## Base v9.4 지시 권위·Context 큐레이션",
            """## Base v9.4 지시 권위·Context 큐레이션

L1 이상 Prompt 계약에서 강한 지시를 추가하기 전에 `HARD_CONSTRAINT / RECOMMENDED_DEFAULT / JUDGMENT_SPACE`로 권위를 분류한다. 보안·권한·데이터 무결성·비가역 변경·저장 호환성·법적 경계는 완화하지 않는다.

입력·출력·불변조건·실패조건·검증을 예시보다 먼저 정의하는 Interface-first 계약을 사용한다. 예시는 정상·실패·경계·회귀 Fixture 또는 Golden Set으로 보존한다.

Context 큐레이션은 현재 `decision_question`을 고정한 뒤 권위·freshness·representation·deduplication·known conflicts·반대 근거·`progressive_load_trigger`·`refresh_trigger`를 기록한다. 상세 Method: `docs/knowledge/game-development/AI_INSTRUCTION_AND_CONTEXT_DESIGN_METHOD.md`.
""",
        ),
        "skills/simplifying-skill-bodies/SKILL.md": (
            "## Base v9.4 지시 분류와 Fixture 보존",
            """## Base v9.4 지시 분류와 Fixture 보존

Skill 본문을 정리할 때 문단을 `Always hard constraint / Conditional default / Judgment space / Fixture or example / Historical / Duplicate`로 분류한다. 강한 안전 규칙을 단순화 명목으로 숨기지 않고, 판단 가능한 표현·배치·비파괴 초안은 불필요한 강제 규칙으로 고정하지 않는다.

Example은 삭제 대상이 아니라 정상·실패·경계·회귀를 검출하는 Fixture다. 예시를 이동·축약할 때 그 행동을 Golden Set·Test·Reference가 계속 검증하는지 비교한다. 상세 Method: `docs/knowledge/game-development/AI_INSTRUCTION_AND_CONTEXT_DESIGN_METHOD.md`.
""",
        ),
        "skills/simplifying-skill-bodies/references/progressive-disclosure-rules.md": (
            "## Base v9.4 authority and fixture classification",
            """## Base v9.4 authority and fixture classification

- Always hard constraint: 보안·권한·무결성·비가역·저장 호환성·법적 경계.
- Conditional default: 특정 mode에서 적용하고 조정 조건과 검증을 가진 기본값.
- Judgment space: 정본·불변조건 안에서 AI가 선택할 수 있는 표현·배치·대안.
- Fixture/example: 인터페이스 뒤에 위치하며 정상·실패·경계·회귀를 검증한다.

예시를 제거해 검증 행동이 사라지거나, 안전 규칙을 reference 깊숙이 숨기거나, 판단 공간을 반복 금지문으로 과도하게 막으면 실패다.
""",
        ),
        "skills/auditing-and-refining-ui-art/SKILL.md": (
            "## Base v9.4 UI 모션·상호작용",
            """## Base v9.4 UI 모션·상호작용

모션·상호작용 작업에서는 `references/ui-motion-and-interaction-principles.md`를 읽는다. 정보 구조와 상태 소유권이 준비된 뒤 모션 목적·staging·입력 접수/처리 중/결과·중단·즉시 완료·빠른 반복·재진입·Reduced Motion·mute·haptic-off·성능을 설계한다.

`AnimationPlayer`와 `Tween`은 표현을 담당하며 구매·보상·저장·진행의 도메인 상태 권위를 소유하지 않는다. 모션이 중단되거나 즉시 완료돼도 결과는 한 번만 발생해야 한다.
""",
        ),
        "skills/auditing-and-refining-ui-art/references/ux-ui-design-system-method.md": (
            "## 3.12 UI 모션·상호작용",
            """## 3.12 UI 모션·상호작용

모션이 상태 변화·입력 접수·공간 관계·결과 위치를 설명해야 하는 경우 `ui-motion-and-interaction-principles.md`를 사용한다. 모션 목적, 중단, 즉시 완료, 빠른 반복, 재진입, Reduced Motion, mute, haptic-off, 성능과 도메인 상태 권위를 검증한다. 프로젝트별 timing·easing 값은 실제 입력 빈도와 목표 플랫폼 증거로 정하며 Base 상수로 고정하지 않는다.
""",
        ),
        "docs/knowledge/game-development/AI_ASSISTED_GAME_DEVELOPMENT_GUIDE.md": (
            "## Base v9.4 지시·Context·모델 비용 라우팅",
            """## Base v9.4 지시·Context·모델 비용 라우팅

Prompt·Context의 지시 권위, Interface-first, Example as Fixture, 결정 질문 중심 큐레이션과 Artifact 주장 상한은 `AI_INSTRUCTION_AND_CONTEXT_DESIGN_METHOD.md`를 사용한다.

모델·추론 단계·Prompt caching·비용 추정과 실제 usage 재보정은 `optimizing-ai-model-and-prompt-costs`를 사용한다. `[모델 추천]` 호출 시 모델·추론 단계·이유·다음 checkpoint를 먼저 제안하며 실제 설정을 자동 변경했다고 주장하지 않는다.
""",
        ),
        "docs/PLANNING_SEQUENCE_AND_EVIDENCE_POLICY.md": (
            "## Base v9.4 Context 큐레이션 Gate",
            """## Base v9.4 Context 큐레이션 Gate

Context 선별이 기획 근거를 바꾸는 작업에서는 `decision_question / include_criteria / exclude_criteria / authority_level / freshness / representation / deduplication / known_conflicts / progressive_load_trigger / refresh_trigger`를 기록한다.

반대 근거·실패 사례·보호 규칙을 관련 없다는 이유로 제거하지 않는다. 제외에는 이유와 재조회 조건을 남기며, 화면·Schema·Fixture 같은 Artifact가 런타임·사람 이해·접근성·성능을 증명한다고 과장하지 않는다.
""",
        ),
        "docs/DOCUMENTATION_MAP.md": (
            "## Base v9.4 AI 운영 계약",
            """## Base v9.4 AI 운영 계약

| 질문 | 책임 원본 |
|---|---|
| 모델·추론 단계·Prompt caching·비용 | `skills/optimizing-ai-model-and-prompt-costs/SKILL.md` |
| 지시 권위·Interface-first·Context 큐레이션·Artifact 주장 상한 | `docs/knowledge/game-development/AI_INSTRUCTION_AND_CONTEXT_DESIGN_METHOD.md` |
| 게임 UI 모션·중단·반복·Reduced Motion | `skills/auditing-and-refining-ui-art/references/ui-motion-and-interaction-principles.md` |
| Base v9.4 후보·evidence·pin 순서 | `docs/operations/BASE_V9_4_RELEASE_CONTRACT.md` |
""",
        ),
        "templates/project-operations/AI_WORKFLOW.md": (
            "## Base v9.4 AI 작업 패키지",
            """## Base v9.4 AI 작업 패키지

- `[모델 추천]`: 현재 작업을 `SIMPLE_BULK / ROUTINE_BALANCED / HIGH_RISK_REASONING`으로 분류하고 모델·추론 단계·이유·변경 checkpoint를 제시한다.
- 지시 권위: `HARD_CONSTRAINT / RECOMMENDED_DEFAULT / JUDGMENT_SPACE`를 구분한다.
- Context 큐레이션: 현재 결정 질문, 포함·제외 기준, 권위, freshness, known conflicts, 반대 근거, progressive load와 refresh trigger를 기록한다.
- 예시는 인터페이스 뒤의 Fixture·Golden Set이며 정본을 덮어쓰지 않는다.
- Artifact는 주장 상한과 실행하지 않은 검증을 `NOT_RUN`으로 남긴다.
""",
        ),
        "templates/planning/GAME_UX_UI_SYSTEM.md": (
            "## UI 모션·상호작용 계약",
            """## UI 모션·상호작용 계약

```yaml
모션 목적:
상태 변화:
staging과 첫 시선:
입력 접수:
처리 중:
결과 위치:
중단:
즉시 완료:
빠른 반복·재진입:
Reduced Motion:
mute:
haptic-off:
도메인 상태 권위:
성능·전후 증거:
```

프로젝트별 timing·easing 값은 실제 반복 빈도와 목표 플랫폼에서 검증한다.
""",
        ),
        "templates/quality/GAME_UX_UI_REVIEW_CHECKLIST.md": (
            "## UI 모션·상호작용 검수",
            """## UI 모션·상호작용 검수

- [ ] 모션 목적과 상태 변화가 명확하다.
- [ ] 입력 접수·처리 중·실제 결과가 구분된다.
- [ ] AnimationPlayer·Tween이 도메인 상태 권위를 소유하지 않는다.
- [ ] 중단·즉시 완료·빠른 반복·재진입에서 결과 중복과 transform drift가 없다.
- [ ] Reduced Motion·mute·haptic-off에서 핵심 정보와 결과가 유지된다.
- [ ] 목표 해상도·긴 한국어·성능·전후 증거를 실제로 검사했다.
""",
        ),
        "docs/BASE_RULES_VERSION.md": (
            "## Base v9.4 compatible candidate",
            """## Base v9.4 compatible candidate

Base v9.4 is the compatible AI-operations candidate over released v9.3. It adds model/effort/cost routing and judgment-centered instruction, context, artifact, and game UI motion contracts. Its identity is recorded in `../base-v9.4.lock.json`; candidate release and evidence pins remain null until separate trusted-main evidence and pin-finalization PRs are merged. The immutable v9.0 table and released v9.3 identity are not rewritten.
""",
        ),
        "docs/CHANGELOG.md": (
            "### Base v9.4 AI operations candidate",
            """### Base v9.4 AI operations candidate

- Added provider-neutral model/effort routing, Prompt caching boundaries, cost measurement and recalibration.
- Added instruction authority budgeting, Interface-first Prompt, Context curation, Example-as-Fixture and Artifact claim limits.
- Added Godot game UI motion contracts for interruption, instant completion, repetition, Reduced Motion, mute, haptic-off and domain authority.
- Preserved released Base v9.3 history and separated candidate, trusted evidence and pin-finalization stages.
""",
        ),
        "skills/SKILL_LEARNING_LOG.md": (
            "## 2026-08-01 — Base v9.4 AI operations",
            """## 2026-08-01 — Base v9.4 AI operations

- BCP-2026-003: 모델 하향의 재시도·상위 모델 재작업 비용까지 포함해야 비용 최적화가 성립한다.
- BCP-2026-004: 강한 안전 규칙은 보존하되 예시는 Fixture로, 표현·배치는 검증 가능한 판단 공간으로 분리한다.
- 신규 제안은 사용자 승인 근거가 있어도 제안 PR에서 `SUBMITTED`로 시작하고 승인 상태는 별도 구현 PR에서 전환해야 한다.
- UI 모션은 표현이며 도메인 결과의 권위가 아니다. 중단·즉시 완료·빠른 반복과 접근성 폴백을 함께 검증한다.
""",
        ),
    }
    for rel_path, (marker, section) in sections.items():
        changed = append_once(ROOT / rel_path, marker, section) or changed
    return changed


def generate_summary_and_lock() -> bool:
    sys.path.insert(0, str(ROOT / "tools"))
    from build_base_v9_artifacts import generated_summary, load_active_skills  # type: ignore

    _, skills = load_active_skills()
    registry_hash = hashlib.sha256(REGISTRY_PATH.read_bytes()).hexdigest()
    changed = write_if_changed(SUMMARY_PATH, generated_summary(skills, registry_hash))
    lock = {
        "schema_version": 1,
        "artifact_role": "BASE_V9_4_RELEASE_CANDIDATE_LOCK",
        "release_line": "v9.4.0",
        "release_state": "RELEASE_CANDIDATE",
        "repository": "alsdmlals4-eng/Base",
        "github_issue": 113,
        "linked_issue": 115,
        "candidate_release_commit": None,
        "candidate_release_evidence_commit": None,
        "candidate_registry": {
            "path": "skills/SKILL_REGISTRY.json",
            "sha256": registry_hash,
            "hash_definition": "RAW_FILE_BYTES_SHA256",
        },
    }
    changed = write_if_changed(LOCK_PATH, canonical_pretty(lock)) or changed
    return changed


def main() -> int:
    changed = False
    changed = update_registry() or changed
    changed = update_proposals() or changed
    changed = update_skill_and_method_consumers() or changed
    changed = generate_summary_and_lock() or changed
    print("Base v9.4 AI operations migration applied" if changed else "Base v9.4 AI operations already current")
    print(hashlib.sha256(REGISTRY_PATH.read_bytes()).hexdigest())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
