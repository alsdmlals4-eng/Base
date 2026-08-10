# BCP-2026-014 — Handoff Machine-Consumer Compatibility-Safe Closeout

## 출처와 상태

- Proposal ID: `BCP-2026-014-handoff-machine-consumer-compatibility-closeout`
- 출처 프로젝트: `alsdmlals4-eng/urban-legend`
- 출처 프로젝트 기준 Handoff head: `2b424906c4ecaa4a027719383d3400486b03c72e`
- 관련 프로젝트 PR: `urban-legend #187`
- 관련 Base Proposal: `BCP-2026-013-post-merge-continuation-state-reconciliation`
- 제출일: `2026-08-10`
- 상태: `SUBMITTED`
- 지식 상태: `관찰`
- Existing Solution Verdict: `ABSORB`
- Same-goal assessment: `MATERIAL_SCOPE_EXTENSION_NOT_DUPLICATE`

이번 proposal은 Base 활성 Skill·Template·Test·Workflow를 수정하지 않는다. `[수정제안서]/**` 안에서 제안·증거·Registry만 등록한다.

BCP-2026-013은 **merge 이후 live continuation state가 즉시 stale해지는 lifecycle**을 다룬다. 본 BCP는 그보다 앞선 Handoff refresh/closeout 단계에서 **사람이 읽는 현재 상태와 machine consumer가 요구하는 호환 계약을 함께 보존하는 문제**를 다룬다. 같은 owner의 인접 lifecycle이지만 실패 원인과 검증 시나리오가 다르므로 중복 제안으로 보지 않는다.

## 관찰과 증거

### Problem

`urban-legend`의 `docs/CURRENT_HANDOFF.md`를 오래된 상태 문구를 제거하고 최신 GitHub·Google Sheet·runtime 사실 중심으로 압축 교체했을 때, 문서의 사람이 읽는 의미는 더 정확해졌지만 기존 테스트가 Handoff를 **machine-readable compatibility surface**로 사용하고 있어 exact-head CI가 실패했다.

초기 Handoff commit `b131bb520172e9252dc5c4e07107ccb3e82fc83e`에서 다음 workflow가 실패했다.

- `Validate documentation contracts` run `31351675821`: FAIL
- `Validate core and documentation baseline` run `31351675802`: FAIL
- `Validate ANNUAL-MVP-001` run `31351675833`: FAIL

실패한 활성 계약은 Handoff에서 다음 historical/compatibility token을 찾고 있었다.

- `APPROVED_DESIGN_BASELINE`
- `CORE-VALIDATION-001`
- `UX-PD-001 2A`
- `Ver 4.2`
- `mvp-039`

이 문자열을 제거한 이유는 현재 상태와 맞지 않거나 현재 버전처럼 오인될 수 있었기 때문이다. 하지만 소비자 migration 없이 삭제하면 machine contract가 깨졌다.

첫 보정 commit `71fe4007de1dd9ab14bde0b0b19fdf8fa0535b1c`에서 위 token을 `Historical Compatibility Anchors` 영역에 분리했지만 `POC_PASSED: NOT_DECLARED`라는 추가 consumer requirement가 드러나 다시 실패했다.

최종 Handoff head `2b424906c4ecaa4a027719383d3400486b03c72e`에서는 current-state section과 compatibility-only section을 분리하고 필요한 machine-consumed anchor를 보존했다. 그 exact head에서 다음 workflow가 모두 성공했다.

- `Validate documentation contracts` run `31351847793`: PASS
- `Validate Urban Legend BCA Adoption` run `31351847833`: PASS
- `Validate Project Base Adapter` run `31351847790`: PASS
- `Validate core and documentation baseline` run `31351847798`: PASS
- `Validate ANNUAL-MVP-001` run `31351847784`: PASS

상세 lineage와 benchmark는 `evidence/URBAN_LEGEND_HANDOFF_COMPATIBILITY_EVIDENCE.md`가 책임진다.

### Root Cause

현재 Base는 이미 두 책임을 소유한다.

1. `maintaining-project-context-and-handoff`
   - Handoff를 현재 상태·읽기 순서·미완료 작업·위험·다음 책임자를 연결하는 압축 router로 유지한다.
   - 오래된 상태를 current truth로 취급하지 않는다.
2. `auditing-canonical-reference-freshness`
   - 정본 변경 뒤 활성 소비자·테스트·workflow·legacy reference를 찾고 `LEGACY_REFERENCE_ALLOWED`와 stale reference를 구분한다.

하지만 Handoff/Active Context를 **큰 폭으로 압축 교체하거나 closeout**할 때 다음 연결이 명시적 종료 조건으로 묶여 있지 않다.

```text
HANDOFF_REFRESH
→ MACHINE_CONSUMER_INVENTORY
→ CURRENT_AUTHORITY / HISTORICAL_COMPATIBILITY_ONLY / STALE_REMOVE 분류
→ current-state compression
→ exact-head document/contract validation
→ failure attribution
→ compatibility-only restoration 또는 consumer migration
→ exact-head GREEN
→ closeout
```

즉 새 광역 Skill이 필요한 것이 아니라 기존 Handoff owner와 canonical-reference-freshness owner 사이의 closeout 계약이 부족하다.

## 일반화 후보

### Proposed General Rule

프로젝트 Active Context/Handoff를 큰 폭으로 갱신하거나 세션 종료 checkpoint를 만들 때, 사람이 읽는 현재 상태만 정리하지 말고 **machine consumer inventory와 compatibility classification을 먼저 수행**한다.

```text
LATEST_RUNTIME_AND_REPOSITORY_TRUTH
→ HANDOFF_DIFF_FREEZE
→ MACHINE_CONSUMER_INVENTORY
→ token/reference classification
   CURRENT_AUTHORITY
   HISTORICAL_COMPATIBILITY_ONLY
   STALE_REMOVE
→ compressed current-state update
→ exact-head contract validation
→ failure attribution
→ compatibility-only restoration or consumer migration
→ exact-head GREEN
→ checkpoint closeout
```

### Classification

#### `CURRENT_AUTHORITY`

최신 main, active PR, 현재 blocker, 현재 Decision, 현재 Sheet state처럼 현재 사실을 표현하는 값이다.

#### `HISTORICAL_COMPATIBILITY_ONLY`

테스트·parser·validator·migration·과거 계약이 아직 소비하지만 현재 상태를 의미하지 않는 값이다.

요건:

- 별도 compatibility/history 영역에 둔다.
- 현재 버전·현재 상태·현재 Decision처럼 읽히지 않도록 명시한다.
- 실제 consumer 근거가 있어야 한다.
- consumer migration이 완료되면 freshness audit에서 제거 후보가 된다.

#### `STALE_REMOVE`

활성 소비자가 없고 current state를 오도하는 과거 토큰·경로·상태다. freshness audit 근거가 있을 때 제거한다.

### Handoff Closeout Invariant

```text
current_state_truth_is_fresh
AND machine_consumers_are_accounted_for
AND allowed_legacy_is_explicitly_labeled
AND exact_head_validation_is_green
```

이 네 조건이 동시에 충족되기 전에는 `HANDOFF_CHECKPOINT_GREEN` 또는 동등한 완료 상태를 주장하지 않는다.

### Relationship to BCP-2026-013

두 제안은 `maintaining-project-context-and-handoff`에 흡수될 가능성이 높지만 lifecycle edge가 다르다.

```text
BCP-2026-014
pre-merge / refresh / closeout
→ machine-consumer compatibility-safe handoff

BCP-2026-013
post-merge / integration
→ live continuation-state reconciliation
```

향후 두 제안이 모두 구현 승인된다면 하나의 기존 owner 변경 세트에서 조정할 수 있으나, 이번 proposal-only 단계에서는 어느 활성 Base 파일도 수정하지 않는다.

### 프로젝트 전용으로 남길 내용

Base에 복사하지 않을 값:

- `urban-legend`의 PR 번호, commit SHA, Decision ID
- `Ver 4.2` / `Ver 4.3` 자체
- `CORE-VALIDATION-001`, `UX-PD-001 2A`, `mvp-039`, `POC_PASSED: NOT_DECLARED` 자체
- 프로젝트 Google Sheet 구조와 셀 주소
- Godot runtime blocker 내용
- 특정 Handoff 문서의 실제 compatibility token 집합

Base는 **consumer inventory·분류·검증·closeout 순서**만 소유한다.

### Benchmark

외부 사례는 본 제안의 직접 규칙이 아니라 compatibility contract를 다루는 **비교 근거**로만 사용했다.

1. GitHub Required Status Checks
   - required workflow/check가 path filtering 등으로 생성되지 않으면 해당 check가 Pending 상태로 남아 merge를 차단할 수 있다.
   - 사람에게는 “이 변경에 CI가 필요 없어 보인다”는 판단과 별개로 machine-consumed check 계약은 유지된다.
   - 적용 원리: machine consumer가 존재하는 surface는 소비자를 migration하거나 compatibility contract를 보존해야 한다.
2. Semantic Versioning 2.0.0
   - public API는 코드뿐 아니라 문서로 선언될 수도 있고, backward-incompatible change는 호환성 비용을 명시적으로 다룬다.
   - 적용 원리: 문서 안의 token이라도 외부 machine consumer가 의존하면 사실상 contract surface로 취급한다.
3. Kubernetes Deprecation Policy
   - 안정 API 요소는 기존 version에서 임의 제거하지 않고 deprecation/version lifecycle을 둔다.
   - 적용 원리: 오래된 token을 영구 보존하자는 뜻이 아니라, consumer migration 없이 즉시 제거하지 않는 staged compatibility 원리를 참고한다.

Sources:

- https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/troubleshooting-required-status-checks
- https://semver.org/
- https://kubernetes.io/docs/reference/using-api/deprecation-policy/

## 적용 조건과 비사용 조건

### Use When

- Handoff/Active Context를 부분 수정이 아니라 큰 폭으로 압축·교체한다.
- 해당 문서를 테스트·workflow·validator·parser가 소비한다.
- 과거 상태 문자열을 지우면 자동 계약이 실패하거나, 반대로 보존하면 현재 상태처럼 오독될 수 있다.
- 세션 종료·담당자 교체·AI handoff 직전에 checkpoint를 closeout하려 한다.

### Do Not Use When

- 외부 consumer가 없는 단순 메모/오탈자 변경이다.
- 과거 token이 실제 current authority라 compatibility 분리가 필요 없다.
- 테스트가 잘못된 요구를 고정한 것이 명백하고 같은 승인 범위에서 consumer migration을 안전하게 완료할 수 있다. 이 경우 compatibility anchor를 늘리지 말고 consumer를 고친다.
- project-only 상태·게임 규칙·버전 값을 Base 표준으로 승격하려 한다.
- reusable gap 없이 단순히 Handoff를 작성했다는 이유만으로 BCP를 만들려 한다.

## 반례와 위험

### Counterexample 1 — consumer migration이 더 맞는 경우

Handoff의 과거 token 하나를 단일 테스트가 문자열 포함 여부로만 확인하고 그 요구 자체가 이미 폐기되었다면, `HISTORICAL_COMPATIBILITY_ONLY`를 추가하는 대신 테스트를 새 contract로 migration하는 편이 맞다.

### Counterexample 2 — historical snapshot

날짜가 붙은 review/handoff가 과거 시점의 상태를 정확하게 기록한 경우에는 current-state 문구로 바꾸지 않는다. history는 history로 보존한다.

### Counterexample 3 — machine consumer가 없음

개인 메모나 외부 소비자가 없는 단순 context note는 이 절차 전체를 강제할 필요가 없다.

### Risks

- compatibility section이 영구 쓰레기통이 될 수 있다.
- 오래된 상태를 compatibility라는 이름으로 무제한 보존할 수 있다.
- 잘못된 테스트까지 token 추가로 연명할 수 있다.
- closeout 절차가 과도하게 길어질 수 있다.
- exact-head GREEN만 보고 Handoff 내용 자체의 의미 정확성을 놓칠 수 있다.

### Mitigation

- compatibility token마다 실제 consumer/test 근거를 요구한다.
- current-state와 compatibility/history section을 분리한다.
- consumer가 제거되면 compatibility token도 freshness audit 대상이 된다.
- 작은 handoff에는 전체 절차를 강제하지 않는다.
- exact-head validation은 의미 검토를 대체하지 않고 마지막 closeout gate로만 사용한다.

## 영향 범위와 검증

### Existing Solution First

| 후보 | 판정 | 이유 |
|---|---|---|
| Handoff current-state router | `REUSE` | `maintaining-project-context-and-handoff`가 이미 소유 |
| stale/legacy reference 분류 | `REUSE` | `auditing-canonical-reference-freshness`가 이미 소유 |
| post-merge live-state reconcile | `REUSE_RELATED_BCP` | BCP-2026-013이 이미 제안함 |
| machine-consumer inventory + compatibility-safe closeout | `ABSORB` | 기존 owner 사이의 호출/종료 연결이 부족 |
| 프로젝트별 legacy token 목록 | `PROJECT_ONLY` | Base 공용값이 아님 |

### 승인될 경우 예상 구현 범위

새 ACTIVE Skill은 만들지 않는다.

최소 후보:

- `skills/maintaining-project-context-and-handoff/SKILL.md`
  - compatibility-safe closeout 절차 추가
  - machine consumer inventory와 exact-head gate 명시
- `skills/auditing-canonical-reference-freshness/SKILL.md`
  - Handoff/Active Context의 machine consumers와 compatibility-only token 분류 연결
- 기존 허용 companion regression test
  - current truth와 historical compatibility가 섞이지 않는 계약
- 필요 시 learning log

이번 proposal은 위 활성 파일을 수정하지 않는다.

### Required Validation if Implemented

- focused RED: Handoff 교체 시 machine consumer inventory/compatibility classification contract 부재가 실패해야 함
- GREEN: 기존 Handoff/freshness owner 연동으로 통과
- Base canonical reference freshness: PASS
- Base proposal validator: PASS
- Base v9 operating contracts: PASS
- Game Project Operating System: PASS
- historical reference가 current authority로 승격되지 않았는지 adversarial review
- BCP-2026-013과 중복/충돌 없이 lifecycle이 이어지는지 검증
- 추가 프로젝트 pilot: `NOT_RUN` 상태를 실제 적용 전까지 유지

### Affected Consumers

- primary Skill: `maintaining-project-context-and-handoff`
- supporting Skill: `auditing-canonical-reference-freshness`
- proposal lifecycle: `managing-base-change-proposals`
- future regression tests: existing allowed companion tests only
- generated views/Registry: active implementation 승인 시 영향 지도 재계산

### Rollback

제안 단계에서는 활성 Base 동작이 바뀌지 않는다. 거절·보류 시 proposal/evidence history를 삭제하지 않고 현행 lifecycle 상태로 전이한다.

## 필요한 도구·파일·권한

- 필요 항목: GitHub repository read/write, Base proposal registry, source-project exact-head CI evidence
- 필요한 이유: proposal 출처와 machine-consumer contract 실패/복구를 재현 가능하게 연결하기 위해 필요
- 설치·적용 방법: 별도 설치 없음
- 설치 후 확인 명령: Base proposal validator와 proposal-only CI
- 최소 권한: proposal branch 작성·PR 생성·제안 전용 병합 권한

## 승인과 구현

- 사용자 제안 저장·병합 지시 근거: `2026-08-10` 현재 단일 파일 실행 계약 — Base `[수정제안서]/**` proposal-only 작성·검증·PR 병합 권한
- proposal storage merge authority: `GRANTED`
- active Base implementation authority: `NOT_GRANTED_IN_THIS_STAGE`
- `approval_ref`: `null`
- 구현 PR: `없음`
- proposal 상태: `SUBMITTED`
- 구현 상태: `NOT_STARTED_IN_THIS_STAGE`
- implementation boundary: `SEPARATE_FOLLOWUP_STAGE`
- 롤백: proposal PR을 병합하지 않거나, 병합 후에는 이력을 삭제하지 않고 Base 현행 lifecycle에 따라 `DEFERRED` 또는 `REJECTED`로 전이한다.

## Evidence ceiling

```yaml
source_project_failure_reproduced: true
source_project_recovery_verified: true
source_project_exact_head_ci_green: true
external_benchmark: PRIMARY_SOURCES_REVIEWED
related_bcp_013: MERGED_SUBMITTED
second_project_pilot_for_this_exact_gap: NOT_RUN
active_base_implementation: NOT_STARTED
human_comprehension_usability: NOT_RUN
knowledge_level: OBSERVATION
```
