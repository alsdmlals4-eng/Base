# Claim and Intent Verification

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

### Completion-candidate correction requirement

`COMPLETION_CLAIM_GATE`가 각 Evidence 층을 PASS로 판정해도 계획 목록 소진이나 `required_work_remaining: 0`만으로 **전체 완료**를 선언하지 않는다. Base `docs/OPERATING_MODEL.md`의 `REMAINING_WORK_COMPLETION_GATE`를 소비한다.

```text
REMAINING_WORK_RECALCULATION_REQUIRED
→ actionable remaining work == 0
→ COMPLETION_CANDIDATE
→ IMPLEMENTATION_CORRECTION_RESCAN
   ├─ valid finding → NEW_FINDING_REOPENS_REMAINING_WORK → fix / verify / recalculate
   └─ no required finding → POST_COMPLETION_ADVERSARIAL_REVIEW_REQUIRED
→ same final POST_CHANGE_MONITOR_LOOP
→ minimum-five full-scope loops, then until CLEAN_REVIEW_EXIT
→ FULL_COMPLETION_REQUIRES_ZERO_REMAINING_WORK
→ full-completion claim allowed
```

`POST_COMPLETION_ADVERSARIAL_REVIEW_REQUIRED`는 두 번째 독립 review cycle이 아니라 최종 completion candidate를 입력으로 하는 기존 `POST_CHANGE_MONITOR_LOOP`다. 승인 범위 안에 `BLOCKED_UNVERIFIED`, `USER_DECISION_REQUIRED`, 미해결 required `DEFER` 또는 새 구현/교정 finding이 남아 있으면 full-completion claim은 `BLOCKED_UNVERIFIED` 또는 현재 부분 상태로 유지한다.

## Connector / MCP executable-surface Reality Gate

외부 connector·MCP·agent runtime의 self-discovery나 capability 목록은 **탐색 증거**다.
`available`, `enabled`, `connected`, `supported`라는 표시만으로 실제 실행 가능·효과 발생·사용자 표시를 PASS 처리하지 않는다.

```text
DISCOVERED_AVAILABLE != EXECUTABLE_AVAILABLE
EXECUTABLE_AVAILABLE != EFFECT_VERIFIED
SERVER_READBACK_PASS != HUMAN_VISIBLE_DEVICE_PASS
```

Capability를 완료 근거로 사용할 때는 필요한 층까지 아래 순서를 실제로 통과한다.

```text
capability discovery
→ callable function + usable schema exposure
→ minimum real invocation
→ durable effect / destination readback when applicable
→ consumer / human / device-visible observation when the claim depends on that surface
```

허용 상태:

- `DISCOVERED_ONLY`: capability/self 상태만 확인됨.
- `CALLABLE_SCHEMA_PRESENT`: 현재 실행 surface에 필요한 입력 Schema가 실제 노출됨.
- `INVOCATION_PASS`: 실제 최소 호출이 성공함.
- `READBACK_PASS`: 쓰기/효과가 대상 시스템에서 다시 읽혀 지속됨.
- `HUMAN_VISIBLE_PASS`: 사람·기기 표시가 claim에 필요하고 실제 관찰됨.
- `BLOCKED_TOOL_SURFACE`: 공급자는 기능을 표시하지만 현재 client/tool surface가 호출에 필요한 함수나 usable schema를 노출하지 않음.
- `FAIL`: 필요한 실제 호출·효과·표시가 실행됐고 실패함.

### 판정 규칙

- self/workspace discovery의 `available`만 있으면 최대 `DISCOVERED_ONLY`다.
- 설명 문서에 함수가 있어도 현재 callable schema가 없거나 필수 입력을 전달할 수 없으면 `BLOCKED_TOOL_SURFACE`다.
- 실제 호출 성공만으로 write/effect를 완료 처리하지 않는다. durable 변경이면 destination readback을 요구한다.
- 서버 readback은 Android/iOS/브라우저 등 실제 client rendering의 대체 증거가 아니다.
- runtime·render·device·human claim은 그 consumer를 실제 관찰하지 않았다면 기존 Evidence Ceiling에 따라 `NOT_RUN`/`BLOCKED_UNVERIFIED`를 유지한다.
- connector 구현 세부를 새로운 광역 Skill로 복제하지 않고 이 기존 verification owner가 공용 claim ceiling을 소유한다.

### 대표 반례

```text
MCP self: create_file_upload = available
+ 현재 ChatGPT에 callable create_file_upload 없음
→ DISCOVERED_ONLY + BLOCKED_TOOL_SURFACE
→ "업로드 기능 사용 가능" 완료 주장 금지
```

```text
write invocation PASS
+ destination readback 없음
→ EFFECT_VERIFIED 아님
```

```text
Notion server image block readback PASS
+ Android 실제 렌더 미관찰 또는 422
→ HUMAN_VISIBLE_PASS 아님
```

## Closure evidence hardening

Universal Loop v1 REAL closure에서 확인한 완료 증거 실패 패턴을 기존 Gate에 흡수한다.
새 Skill·새 Work Mode를 만들지 않고 아래 네 규칙을 모든 완료·통합 주장에 재사용한다.

### `MACHINE_EVIDENCE_CORRECTION`

- handoff·chat·worker·summary 설명이 exact repository readback 또는 terminal machine evidence와 충돌하면 설명을 권위로 유지하지 않는다.
- 충돌한 summary는 `counterevidence`로 기록하고, 파생 기록·PR 설명·checkpoint를 실제 evidence에 맞춰 교정한 뒤 최종 판정을 낸다.
- 최종 완료 근거는 가능한 경우 exact issue/run/SHA와 `receipt digest`처럼 재검증 가능한 identity에 묶는다.
- 생산자 설명이 더 편리하거나 먼저 작성됐다는 이유로 exact machine evidence를 덮어쓰지 않는다.

### `TEST_CONSUMPTION_PROOF`

- `workflow trigger`, path filter, 테스트 파일 존재, workflow 시작은 그 테스트의 **실행 증거가 아니다**.
- 새 회귀는 실제 test command·discovery·명시적 suite 목록에 소비됐다는 로그를 확인한다.
- 가능하면 구현 전에 의도한 누락 때문에 해당 테스트가 실제 RED가 되는 것을 확인한다. 테스트가 실행되지 않은 GREEN은 완료 증거가 아니다.

### `LATEST_EXACT_HEAD_ONLY`

- 같은 PR에 여러 Actions run이 있으면 현재 exact HEAD에 속한 required gate만 현재 검증 증거가 된다.
- `stale-head`, cancelled, superseded, zero-step, queued, pending, still-running 결과를 최신 HEAD의 PASS로 대체하지 않는다.
- post-merge 판정도 merge SHA의 새 `main` readback과 해당 main의 검사를 별도로 확인한다.

### `BOUNDED_ZERO_ESCAPE`

- `omission_escape = 0`, `drift_escape = 0`, `unauthorized_addition_escape = 0` 같은 zero-escape 주장은 실제 측정한 exact package·scope·authority·evidence window에만 적용한다.
- 한 operations-only package의 zero-escape를 게임 전체 품질, UX, 밸런스, 아트, 저장 호환성 또는 다른 제품 경로의 무결성으로 일반화하지 않는다.
- 범위가 불명확하면 zero-escape 완료 주장을 `CLAIM_UNVERIFIED`로 유지한다.

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
- capability discovery의 `available`만으로 실제 호출·효과·기기 표시를 PASS 처리한다.
- 필요한 증거가 없는데 `CLAIM_UNVERIFIED`, `IMPLEMENTATION_UNVERIFIED`,
  `BLOCKED_UNVERIFIED`를 해제한다.

## 도구 사용 경계

외부 Eval SaaS나 LLM judge는 선택적 보조 수단이다. deterministic evidence와 정본 대조를
대체하지 않으며, judge 결과에도 dataset·rubric·version·실행 환경·반례가 필요하다.
공급자 도구가 없더라도 이 Gate의 저장소·diff·실행·readback 계약은 동작해야 한다.
