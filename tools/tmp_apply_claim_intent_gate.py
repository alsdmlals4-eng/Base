#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OWNER = "reviewing-and-validating-project-changes"
BRANCH = "feat/claim-intent-verification-gate-final"


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def write(path: str, text: str) -> None:
    (ROOT / path).parent.mkdir(parents=True, exist_ok=True)
    (ROOT / path).write_text(text, encoding="utf-8")


def replace_once(text: str, old: str, new: str, *, label: str) -> str:
    if new in text:
        return text
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: expected one anchor, found {count}")
    return text.replace(old, new, 1)


def append_section_once(path: str, marker: str, section: str) -> None:
    text = read(path)
    if marker in text:
        return
    write(path, text.rstrip() + "\n\n" + section.strip() + "\n")


def update_plan_and_design() -> None:
    for path in (
        "docs/superpowers/plans/2026-08-13-claim-and-intent-verification.md",
        "docs/superpowers/specs/2026-08-13-claim-and-intent-verification-design.md",
    ):
        text = read(path)
        text = text.replace("#317", "#319")
        text = text.replace(
            "feat/claim-intent-verification-gate-20260813",
            BRANCH,
        )
        text = "\n".join(line.rstrip() for line in text.splitlines()) + "\n"
        write(path, text)


def update_skill() -> None:
    path = f"skills/{OWNER}/SKILL.md"
    text = read(path)

    mode_anchor = (
        "- `external-source-review`: 외부 AI·병렬 작업자의 초안과 주장을 독립 검수한다.\n"
    )
    mode_block = mode_anchor + (
        "- `claim-and-intent-verification`: AI·Agent·작업자의 material claim과 승인 Intent를 "
        "actual diff·exact HEAD·실행 Evidence·post-merge main readback에 연결하고 "
        "`MATERIAL_CLAIM_LEDGER`, `INTENT_IMPLEMENTATION_FIDELITY_MATRIX`, "
        "`COMPLETION_CLAIM_GATE`로 판정한다. 증거가 없으면 `CLAIM_UNVERIFIED` 또는 "
        "`IMPLEMENTATION_UNVERIFIED`를 유지한다.\n"
    )
    text = replace_once(text, mode_anchor, mode_block, label="skill mode")

    input_anchor = "acceptance_criteria:\nvalidation_commands_and_tools:\n"
    input_block = (
        "acceptance_criteria:\n"
        "material_claims:\n"
        "approved_intent_and_acceptance:\n"
        "claim_authority_freshness_and_counterevidence:\n"
        "validation_commands_and_tools:\n"
    )
    text = replace_once(text, input_anchor, input_block, label="skill inputs")

    process_anchor = "### 3. Reference freshness\n"
    process_block = """### 2C. Claim and intent verification

완료·검증·병합 주장 또는 승인 의도와 실제 구현의 일치 판정이 포함되면
`references/claim-and-intent-verification.md`를 적용한다.

1. 결과 판정을 바꾸는 주장만 `MATERIAL_CLAIM_LEDGER`에 원자화한다.
2. 각 주장의 authority source, freshness, exact-ref file readback과 counterevidence를 확인한다.
3. 승인된 Intent·Acceptance를 실제 diff·implementation path·관찰 결과에 연결해
   `INTENT_IMPLEMENTATION_FIDELITY_MATRIX`를 작성한다.
4. 구현·검증·의도·통합 주장을 `COMPLETION_CLAIM_GATE`의 서로 다른 Evidence 층으로 판정한다.
5. 검색 결과, Builder 보고, 모델 자신감, 테스트 정의, 다른 SHA의 PASS는 직접 Evidence로 승격하지 않는다.
6. 필요한 Evidence가 없으면 `CLAIM_UNVERIFIED`, `IMPLEMENTATION_UNVERIFIED` 또는
   `BLOCKED_UNVERIFIED`를 유지한다.
7. 병합 완료는 merged 상태, merge SHA, post-merge main readback과 post-merge 검사를 모두 요구한다.

### 3. Reference freshness
"""
    text = replace_once(text, process_anchor, process_block, label="skill process")

    dod_anchor = "## Failure conditions\n"
    dod_block = """- 완료·검증·병합을 주장할 때 material claim, 승인 Intent, 실제 diff, exact HEAD 실행 결과와 필요한 post-merge Evidence를 연결했다.
- 한 Acceptance라도 unmapped이거나 필요한 Evidence 층이 없으면 완료 상태를 `IMPLEMENTATION_UNVERIFIED` 또는 `BLOCKED_UNVERIFIED`로 유지했다.

## Failure conditions
"""
    text = replace_once(text, dod_anchor, dod_block, label="skill definition of done")

    failure_anchor = "- 실제 파일을 읽지 않고 완료를 주장한다.\n"
    failure_block = failure_anchor + (
        "- 검색 결과·snippet·작업자 설명을 exact-ref file readback 없이 저장소 사실로 승격한다.\n"
        "- 테스트 정의나 파일 존재를 해당 exact HEAD의 실행 결과로 승격한다.\n"
        "- merge SHA와 post-merge main readback 없이 병합 완료를 주장한다.\n"
    )
    text = replace_once(text, failure_anchor, failure_block, label="skill failure conditions")

    reference_anchor = "- `references/accessibility-and-performance-validation.md`\n"
    reference_block = reference_anchor + "- `references/claim-and-intent-verification.md`\n"
    text = replace_once(text, reference_anchor, reference_block, label="skill reference")

    write(path, text)


def create_reference() -> None:
    path = f"skills/{OWNER}/references/claim-and-intent-verification.md"
    content = """# Claim and Intent Verification

`claim-and-intent-verification`은 새 ACTIVE Skill이 아니라
`reviewing-and-validating-project-changes`의 fail-closed Skill Mode다.
AI·Agent·작업자의 설명을 신뢰 점수로 승인하지 않고 material claim과 승인 Intent를
exact repository·execution Evidence에 연결한다.

## 적용 조건

- 구현·테스트·검증·병합이 완료됐다는 주장
- 외부 AI·Agent·병렬 작업자의 저장소 사실 또는 현재 상태 주장
- 승인된 WHAT/WHY·Acceptance Criteria와 실제 diff의 일치 판정
- 외부 사실·인용·버전·정책을 현재 사실로 승격하는 작업
- L2 이상 복합 변경의 요구사항 추적성·통합 상태 판정

L0 오탈자나 동일 입력의 단순 재실행에는 전체 원장을 강제하지 않는다.
순수 창작 문장과 중요하지 않은 중간 메모를 원장에 복제하지 않는다.

## 기본 원칙

1. **deterministic-first**: exact-ref 파일, 실제 diff, Schema·정적 검사, 실행 로그,
   런타임·렌더, merged PR와 main readback을 먼저 사용한다.
2. **생산자 설명은 lead**: Builder·Agent·모델의 보고는 확인 대상을 알려 줄 뿐
   독립 Evidence가 아니다.
3. **Evidence ceiling**: 낮은 층의 PASS를 높은 층의 PASS로 승격하지 않는다.
   테스트 PASS는 UX·재미·시장성 PASS가 아니다.
4. **미확인은 실패와 구분**: 반증이 없다는 이유로 통과시키지 않고
   `CLAIM_UNVERIFIED` 또는 `IMPLEMENTATION_UNVERIFIED`를 유지한다.
5. **현재성 고정**: branch·commit·날짜·버전이 없는 자료는 현재 상태 증거가 아니다.
6. **병합 후 재검증**: exact HEAD 검증과 post-merge main readback은 서로 대체하지 않는다.

## 권한 순서

```text
최신 사용자 지시·승인된 작업 계약
→ exact SHA의 실제 저장소·등록 정본
→ 해당 SHA에서 실행된 정적·테스트·런타임 결과
→ 날짜·버전이 확인된 공식 외부 1차 출처
→ 명시적 추론
→ 작업자·Builder·모델 설명
```

같은 층의 증거가 충돌하면 더 최신이고 대상에 직접 연결된 증거를 우선한다.
충돌을 해소하지 못하면 PASS가 아니라 미검증이다.

## MATERIAL_CLAIM_LEDGER

결정·구현·검증·병합 상태를 바꾸는 주장만 원자화한다.

```yaml
MATERIAL_CLAIM_LEDGER:
  - claim_id:
    claim_type: REPOSITORY_FACT | EXTERNAL_FACT | INFERENCE | IMPLEMENTATION | VERIFICATION | INTEGRATION
    claim_text:
    authority_source:
    evidence_locator:
    freshness:
      observed_at:
      branch_or_version:
      commit_sha:
    counterevidence:
    status: CLAIM_VERIFIED | CLAIM_CONTRADICTED | CLAIM_UNVERIFIED | NOT_APPLICABLE
```

### 판정

- `CLAIM_VERIFIED`: authority와 freshness가 맞고 직접 증거가 주장을 지지하며
  material counterevidence가 없다.
- `CLAIM_CONTRADICTED`: 더 높은 권한 또는 더 최신 직접 증거가 주장을 반박한다.
- `CLAIM_UNVERIFIED`: 필요한 파일·SHA·실행·현재성·권한 증거가 없거나 충돌이 해소되지 않았다.
- `NOT_APPLICABLE`: 결과 판정에 영향을 주지 않는 주장이다.

### 저장소 사실 반례

```text
검색 결과·검색 snippet·작업자 설명
+ exact-ref file readback 없음
→ CLAIM_UNVERIFIED
→ 정본·감사 finding·완료 보고로 승격 금지
```

`검색 결과`는 탐색용 lead다. 저장소 사실은 대상 branch 또는 commit의
`exact-ref file readback`, 실제 tree/diff, 필요 시 소비자 재조회로 확인한다.

## INTENT_IMPLEMENTATION_FIDELITY_MATRIX

승인 의도와 구현의 연결을 Acceptance 단위로 기록한다.

```yaml
INTENT_IMPLEMENTATION_FIDELITY_MATRIX:
  - intent_id:
    approved_intent_or_acceptance:
    protected_and_excluded_scope:
    implementation_paths:
    observed_behavior:
    verification_evidence:
    evidence_ceiling:
    drift_status: INTENT_CONFORMANT | MINOR_TECHNICAL_DRIFT | PLANNING_CONFLICT | IMPLEMENTATION_UNVERIFIED
```

- `INTENT_CONFORMANT`: 승인된 결과·보호 동작과 실제 구현·관찰 결과가 일치한다.
- `MINOR_TECHNICAL_DRIFT`: HOW만 달라졌고 WHAT/WHY·제품 의미·보호 동작은 동일하다.
- `PLANNING_CONFLICT`: 플레이어 경험, 주요 UX, 콘텐츠 의미, 범위 또는 우선순위가
  승인 내용과 충돌한다. 구현을 멈추고 재승인한다.
- `IMPLEMENTATION_UNVERIFIED`: 필요한 diff, runtime, render, test 또는 사람 Evidence가 없다.

Acceptance 하나라도 unmapped이면 전체 의도 적합성을 PASS로 선언하지 않는다.

## COMPLETION_CLAIM_GATE

```yaml
COMPLETION_CLAIM_GATE:
  implementation:
    required: actual_diff + requirement_to_implementation_paths + out_of_scope_absence
    status: PASS | FAIL | BLOCKED_UNVERIFIED
  verification:
    required: command + environment + exact_HEAD + result + failure_count
    status: PASS | FAIL | NOT_RUN | BLOCKED_UNVERIFIED
  intent:
    required: acceptance_by_acceptance_observation + required_evidence_level
    status: PASS | PLANNING_CONFLICT | IMPLEMENTATION_UNVERIFIED
  integration:
    required: merged_PR_state + merge_SHA + post-merge_main_readback + post-merge_checks
    status: PASS | FAIL | BLOCKED_UNVERIFIED
```

| 완료 주장 | 최소 Evidence |
|---|---|
| 구현 완료 | 실제 diff, 요구사항별 `implementation_paths`, 보호·범위 밖 변경 부재 |
| 테스트·검증 완료 | 실행 명령, 환경, exact HEAD, 결과, 실패·skip 수 |
| 의도대로 동작 | Acceptance별 관찰 결과와 필요한 Evidence level |
| 병합 완료 | PR merged 상태, merge SHA, 새 main readback, post-merge 필수 검사 |

파일 존재는 실행 증거가 아니다. 다른 SHA의 PASS는 현재 HEAD의 PASS가 아니다.
CI가 queued·cancelled·skipped이면 성공으로 바꾸지 않는다.

## 실행 순서

```text
승인 Intent·Acceptance·Protected Scope 고정
→ material claim 원자화
→ authority·freshness·counterevidence 검사
→ 실제 diff·consumer·implementation path 연결
→ deterministic static/test/runtime evidence 실행
→ Evidence ceiling 적용
→ 독립 VERIFIER/CRITIC 검토
→ exact HEAD 판정
→ merge 뒤 main readback
→ claim / intent / verification / integration 최종 보고
```

## 최소 출력

```md
## Claim and Intent Verification
- 기준 branch·exact HEAD:
- 승인 Intent·Acceptance:
- Material Claim Ledger:
- Intent–Implementation Fidelity Matrix:
- Completion Claim Gate:
- counterevidence·충돌:
- 실행한 검증·결과·실패·skip:
- 미실행·미검증:
- merge SHA·post-merge main readback:
- 최종 판정: PASS / REVISE / PLANNING_CONFLICT / BLOCKED_UNVERIFIED
```

## 실패 조건

- exact-ref 파일을 읽지 않고 저장소 사실을 확정한다.
- 검색 결과나 과거 대화를 현재 정본보다 우선한다.
- 테스트 파일 존재를 실행 결과로 보고한다.
- Builder·모델 자기평가만으로 완료를 선언한다.
- 하나의 Acceptance 또는 보호 경로가 unmapped인데 전체 구현을 완료 처리한다.
- 정적 PASS를 runtime·render·사용성·재미 PASS로 승격한다.
- stale branch의 검증을 current main 후보에 재사용한다.
- merged 상태·merge SHA·main readback 없이 병합 완료를 주장한다.
- 필요한 증거가 없는데 `CLAIM_UNVERIFIED`, `IMPLEMENTATION_UNVERIFIED`,
  `BLOCKED_UNVERIFIED`를 해제한다.

## 도구 사용 경계

외부 Eval SaaS나 LLM judge는 선택적 보조 수단이다. deterministic evidence와 정본 대조를
대체하지 않으며, judge 결과에도 dataset·rubric·version·실행 환경·반례가 필요하다.
공급자 도구가 없더라도 이 Gate의 저장소·diff·실행·readback 계약은 동작해야 한다.
"""
    write(path, content)


def update_registry() -> None:
    path = "skills/SKILL_REGISTRY.json"
    data = json.loads(read(path))
    owners = [entry for entry in data["skills"] if entry["skill_id"] == OWNER]
    if len(owners) != 1:
        raise RuntimeError(f"expected one registry owner, found {len(owners)}")
    owner = owners[0]
    for trigger in (
        "completion-claim",
        "claim-evidence",
        "intent-conformance",
        "hallucination-audit",
    ):
        if trigger not in owner["trigger_tags"]:
            owner["trigger_tags"].append(trigger)
    use_when = (
        "AI·Agent·작업자의 완료 주장과 승인 의도가 실제 diff·exact HEAD·실행 Evidence·"
        "post-merge main readback에 연결됐는지 검증하고, 근거가 없으면 미검증 상태를 유지한다."
    )
    if use_when not in owner["use_when"]:
        owner["use_when"].append(use_when)
    for review_trigger in (
        "unsupported completion claim",
        "approved intent drift",
        "search snippet promoted to repository fact",
        "merge claimed without main readback",
    ):
        if review_trigger not in owner["review_triggers"]:
            owner["review_triggers"].append(review_trigger)
    write(path, json.dumps(data, ensure_ascii=False, separators=(",", ":")) + "\n")


def update_template() -> None:
    path = "templates/quality/PROJECT_CHANGE_VALIDATION.md"
    text = read(path)
    anchor = "## 4. 정적 검사\n"
    block = """## 3.1 Material Claim Ledger

결정·구현·검증·병합 상태를 바꾸는 material claim만 기록한다.
검색 결과·작업자 설명은 lead이며 exact-ref 파일·diff·실행 결과를 대신하지 않는다.

| claim_id | claim_type | claim_text | authority_source | evidence_locator | freshness | counterevidence | status |
|---|---|---|---|---|---|---|---|
| | `REPOSITORY_FACT / EXTERNAL_FACT / INFERENCE / IMPLEMENTATION / VERIFICATION / INTEGRATION` | | | | branch·version·exact SHA·관찰일 | | `CLAIM_VERIFIED / CLAIM_CONTRADICTED / CLAIM_UNVERIFIED / NOT_APPLICABLE` |

## 3.2 Intent–Implementation Fidelity Matrix

| intent_id | approved_intent_or_acceptance | protected_and_excluded_scope | implementation_paths | observed_behavior | verification_evidence | evidence_ceiling | drift_status |
|---|---|---|---|---|---|---|---|
| | | | | | | | `INTENT_CONFORMANT / MINOR_TECHNICAL_DRIFT / PLANNING_CONFLICT / IMPLEMENTATION_UNVERIFIED` |

Acceptance 하나라도 unmapped이거나 필요한 runtime·render·사람 Evidence가 없으면
전체 의도 적합성을 PASS로 선언하지 않는다.

## 3.3 Completion Claim Gate

| Gate | 최소 Evidence | 현재 상태 | 판정 |
|---|---|---|---|
| 구현 완료 | 실제 diff + 요구사항별 implementation path + 범위 밖 변경 부재 | | `PASS / FAIL / BLOCKED_UNVERIFIED` |
| 테스트·검증 완료 | 실행 명령·환경 + exact HEAD + 결과 + 실패·skip 수 | | `PASS / FAIL / NOT_RUN / BLOCKED_UNVERIFIED` |
| 의도대로 동작 | Acceptance별 관찰 결과 + 필요한 Evidence level | | `PASS / PLANNING_CONFLICT / IMPLEMENTATION_UNVERIFIED` |
| 병합 완료 | merged PR 상태 + merge SHA + post-merge main readback + post-merge 검사 | | `PASS / FAIL / BLOCKED_UNVERIFIED` |

파일 존재, 다른 SHA의 PASS, Builder·모델의 자기보고만으로 Gate를 통과시키지 않는다.
상세 절차: `skills/reviewing-and-validating-project-changes/references/claim-and-intent-verification.md`.

## 4. 정적 검사
"""
    text = replace_once(text, anchor, block, label="validation template")
    write(path, text)


def update_operating_docs() -> None:
    section = """## CLAIM_AND_INTENT_VERIFICATION_GATE

완료·검증·병합 주장 또는 승인 의도와 실제 구현의 일치 판정은 `REVIEW`에서
`reviewing-and-validating-project-changes: claim-and-intent-verification`으로 라우팅한다.

```text
material claim 원자화
→ authority·freshness·counterevidence
→ 승인 Intent·Acceptance와 실제 diff 연결
→ exact HEAD 실행 Evidence
→ Completion Claim Gate
→ merge 뒤 post-merge main readback
```

검색 결과·생산자 설명·모델 자신감·테스트 정의·다른 SHA의 PASS는 직접 Evidence가 아니다.
필수 Evidence가 없으면 `CLAIM_UNVERIFIED`, `IMPLEMENTATION_UNVERIFIED` 또는
`BLOCKED_UNVERIFIED`를 유지한다.

Reference: `skills/reviewing-and-validating-project-changes/references/claim-and-intent-verification.md`
"""
    for path in ("docs/WORK_MODE_AND_SKILL_ROUTING.md", "docs/OPERATING_MODEL.md"):
        append_section_once(path, "## CLAIM_AND_INTENT_VERIFICATION_GATE", section)


def update_behavior_eval() -> None:
    path = "skills/SKILL_BEHAVIOR_EVALS.json"
    data = json.loads(read(path))
    coverage = json.loads(read("skills/SKILL_BEHAVIOR_COVERAGE_EVALS.json"))
    all_ids = {case["case_id"] for case in data["cases"]}
    all_ids.update(case["case_id"] for case in coverage["cases"])
    if "SBE-038" in all_ids:
        raise RuntimeError("SBE-038 is already allocated")
    data["cases"].append(
        {
            "case_id": "SBE-038",
            "case_type": "cross-skill",
            "prompt": (
                "외부 AI가 작업을 완료하고 병합했다고 보고했지만 검색 결과와 작업자 설명만 있고 "
                "저장소 exact-ref readback, 실제 diff, 현재 HEAD 실행 결과, merge SHA와 새 main readback이 없습니다. "
                "승인한 의도와 구현이 일치하는지도 검증해줘."
            ),
            "expected_work_mode": "REVIEW",
            "expected_primary_skill": OWNER,
            "expected_supporting_skills": [
                "running-adversarial-review-and-refinement"
            ],
            "expected_skill_modes": [
                "claim-and-intent-verification",
                "external-source-review",
                "contract-check",
                "evidence-report"
            ],
            "forbidden_skills": [
                "creating-user-learning-notes",
                "building-project-visual-dashboards"
            ],
            "required_evidence": [
                "검색 결과와 생산자 설명을 저장소 사실의 단독 증거로 사용하지 않는다.",
                "대상 branch 또는 commit의 exact-ref file readback을 요구한다.",
                "승인 Acceptance와 실제 diff·implementation path를 항목별로 연결한다.",
                "현재 exact HEAD에서 실행된 명령·환경·결과·실패·skip 수를 요구한다.",
                "필요한 증거가 없으면 CLAIM_UNVERIFIED 또는 IMPLEMENTATION_UNVERIFIED로 미검증 상태를 유지한다.",
                "병합 완료는 merged PR, merge SHA, post-merge main readback과 post-merge 검사를 요구한다."
            ],
            "expected_user_decision_state": "NOT_REQUIRED",
            "rationale": (
                "완료·의도·병합 주장의 독립 검증이 주 책임이며 생산자 설명이나 검색 snippet을 "
                "Evidence로 승격하지 않는다."
            )
        }
    )
    write(path, json.dumps(data, ensure_ascii=False, indent=2) + "\n")


def update_learning_log() -> None:
    path = "skills/SKILL_LEARNING_LOG.md"
    text = read(path)
    if "## 2026-08-13 — BCP-2026-027 Claim and Intent Verification Gate" in text:
        return
    entry = """## 2026-08-13 — BCP-2026-027 Claim and Intent Verification Gate

- **상태:** `PATTERN_CANDIDATE`
- **Trigger:** AI·Agent·작업자의 사실·완료 주장과 승인한 의도가 실제 저장소·실행·병합 결과에 연결됐는지 fail-closed로 확인할 공용 절차가 필요했다.
- **Observed regression:** PR #313 감사에서 `README.md` drift 가설이 검색 결과만으로 저장소 사실에 과승격됐고, PR #316의 exact-SHA readback이 이를 `INVALIDATED_FINDING`으로 교정했다.
- **Decision:** 새 ACTIVE Skill을 만들지 않고 `reviewing-and-validating-project-changes`에 `claim-and-intent-verification` Mode와 전용 reference를 흡수한다. 기존 Registry owner에 좁은 trigger를 추가하고 Material Claim Ledger, Intent–Implementation Fidelity Matrix, Completion Claim Gate를 validation Template·REVIEW 운영 문서·`SBE-038`에 연결한다.
- **Fail-closed boundary:** 검색 결과·snippet·생산자 설명·모델 자신감은 lead일 뿐 Evidence가 아니다. exact-ref file readback, 실제 diff, exact HEAD 실행 결과, merge SHA와 post-merge main readback이 없으면 `CLAIM_UNVERIFIED`, `IMPLEMENTATION_UNVERIFIED` 또는 `BLOCKED_UNVERIFIED`를 유지한다.
- **TDD evidence:** PR #319 exact RED head `bf0890439cbef96777171cc00a0229c65e852af8`의 required workflow에서 기존 계약 뒤 신규 Gate 계약 6개가 예상대로 실패했다. 별도 whitespace 3건도 함께 검출돼 구현 변경에서 제거한다.
- **Evidence ceiling:** 정적·테스트 PASS를 runtime·render·사용성·재미·시장성 PASS로 승격하지 않는다. model behavior run은 실제 실행 전 `NOT_RUN`이다.
- **Next trigger:** 서로 다른 프로젝트에서 완료 오판·의도 drift·검색 사실 과승격이 재발하거나, 새 trigger가 과도하게 route할 때 경계를 재검토한다.

"""
    if not text.startswith("# Base Skill Learning Log\n"):
        raise RuntimeError("unexpected central learning log header")
    text = text.replace("# Base Skill Learning Log\n\n", "# Base Skill Learning Log\n\n" + entry, 1)
    write(path, text)


def approve_bcp_for_implementation() -> None:
    registry_path = "[수정제안서]/PROPOSAL_REGISTRY.json"
    registry = json.loads(read(registry_path))
    matches = [
        item
        for item in registry["proposals"]
        if item["proposal_id"] == "BCP-2026-027-claim-and-intent-verification-gate"
    ]
    if len(matches) != 1:
        raise RuntimeError(f"expected one BCP-027 entry, found {len(matches)}")
    item = matches[0]
    if item["status"] not in {"SUBMITTED", "APPROVED_FOR_IMPLEMENTATION"}:
        raise RuntimeError(f"unexpected BCP-027 state: {item['status']}")
    item["status"] = "APPROVED_FOR_IMPLEMENTATION"
    item["implementation_pr"] = None
    write(registry_path, json.dumps(registry, ensure_ascii=False, indent=2) + "\n")

    proposal_path = "[수정제안서]/BCP-2026-027-claim-and-intent-verification-gate/PROPOSAL.md"
    proposal = read(proposal_path)
    proposal = proposal.replace(
        "- Registry 상태: `SUBMITTED`",
        "- Registry 상태: `APPROVED_FOR_IMPLEMENTATION`",
        1,
    )
    approval_marker = "- 구현 PR: `https://github.com/alsdmlals4-eng/Base/pull/319`"
    if approval_marker not in proposal:
        proposal = proposal.replace(
            "- 사용자 구현 승인 증거:",
            approval_marker + "\n- 사용자 구현 승인 증거:",
            1,
        )
    proposal = proposal.replace("PR #317", "PR #319")
    write(proposal_path, proposal)


def main() -> int:
    update_plan_and_design()
    update_skill()
    create_reference()
    update_registry()
    update_template()
    update_operating_docs()
    update_behavior_eval()
    update_learning_log()
    approve_bcp_for_implementation()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
