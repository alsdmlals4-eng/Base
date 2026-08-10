# BCP-2026-013 — Handoff Checkpoint 호환성·종료 계약

## 출처와 상태

- Proposal ID: `BCP-2026-013-handoff-checkpoint-compatibility-closeout`
- 출처 프로젝트: `alsdmlals4-eng/urban-legend`
- 출처 프로젝트 기준 Handoff head: `2b424906c4ecaa4a027719383d3400486b03c72e`
- 관련 프로젝트 PR: `urban-legend #187`
- 관련 프로젝트 상태: feature work paused / handoff-only checkpoint
- 제출일: `2026-08-10`
- 상태: `SUBMITTED`
- 지식 상태: `관찰`
- Existing Solution Verdict: `ABSORB`

이번 proposal은 Base 활성 Skill·Template·Test·Workflow를 수정하지 않는다. 승인 전에는 `[수정제안서]/**`의 proposal/evidence/registry만 등록한다.

## 관찰과 증거

### Problem

프로젝트 Handoff를 최신 상태로 압축 교체할 때, 사람이 읽는 의미는 더 정확해졌더라도 해당 문서를 기계적으로 소비하는 기존 테스트·validator·workflow가 과거 호환 토큰을 요구할 수 있다.

`urban-legend`의 `docs/CURRENT_HANDOFF.md`를 현재 GitHub/Google Sheet/runtime 사실에 맞춰 재작성한 첫 Handoff checkpoint는 제품 코드를 전혀 바꾸지 않았지만 active-document contract가 실패했다.

실패 원인은 현재 상태의 정확성이 아니라 다음 문자열을 기존 계약 테스트가 계속 요구한 것이었다.

- `APPROVED_DESIGN_BASELINE`
- `CORE-VALIDATION-001`
- `UX-PD-001 2A`
- `Ver 4.2`
- `mvp-039`
- 이후 재시도에서 `POC_PASSED: NOT_DECLARED`도 추가 필수 소비자로 확인됨

그렇다고 이 문자열을 현재 상태처럼 복원하면 `Ver 4.2` 같은 과거 표현이 현재 제품 상태로 오인될 수 있다. 최종 수정은 이 값들을 `HISTORICAL_COMPATIBILITY_ONLY` 영역으로 격리하고, 현재 Handoff 본문은 최신 August 2026 상태를 유지했다.

최종 exact-head `2b424906c4ecaa4a027719383d3400486b03c72e`에서 Handoff-only 변경은 모든 현재 workflow를 통과했다.

상세 exact-head lineage는 `evidence/URBAN_LEGEND_HANDOFF_COMPATIBILITY_EVIDENCE.md`가 책임진다.

### Root Cause

현재 Base에는 두 책임이 각각 존재한다.

1. `maintaining-project-context-and-handoff`
   - Handoff를 현재 상태·읽기 순서·미완료 작업·위험·다음 책임자를 연결하는 압축 router로 유지한다.
   - 오래된 상태를 현재 사실로 취급하지 않는다.
2. `auditing-canonical-reference-freshness`
   - 정본 변경 뒤 활성 소비자·테스트·workflow·legacy reference를 분류한다.
   - `LEGACY_REFERENCE_ALLOWED`와 stale reference를 구분한다.

하지만 Handoff를 **통째로 압축/교체하는 closeout 시점**에 다음 연결이 명시적으로 강제되지 않는다.

```text
Handoff refresh
→ machine consumer inventory
→ current vs historical-compatibility classification
→ exact-head contract validation
→ merge/closeout
```

즉 새로운 광역 책임이 필요한 것이 아니라 기존 Handoff owner와 freshness owner 사이의 호출·종료 계약이 부족하다.

## 일반화 후보

### Proposed General Rule

프로젝트 Active Context/Handoff를 큰 폭으로 갱신하거나 세션 종료 checkpoint를 만들 때 다음 순서를 사용한다.

```text
LATEST_RUNTIME_AND_REPO_TRUTH
→ HANDOFF_DIFF_FREEZE
→ MACHINE_CONSUMER_INVENTORY
→ token/reference classification
   CURRENT_AUTHORITY
   HISTORICAL_COMPATIBILITY_ONLY
   STALE_REMOVE
→ compressed current-state handoff update
→ exact-head CI / document-contract validation
→ failure attribution
→ compatibility-only restoration when justified
→ exact-head GREEN
→ checkpoint merge/closeout
```

### Classification

#### `CURRENT_AUTHORITY`

현재 프로젝트 상태를 설명하는 값. 최신 main, active PR, current blocker, current Decision, current Sheet state처럼 현재 사실을 표현한다.

#### `HISTORICAL_COMPATIBILITY_ONLY`

테스트·parser·validator·migration·과거 계약이 아직 소비하지만 현재 상태를 의미하지 않는 값.

요건:

- 별도 compatibility/history 영역에 둔다.
- 현재 버전·현재 상태·현재 Decision처럼 읽히지 않도록 명시한다.
- 자동 검사가 요구한다는 이유만으로 본문 current-state section으로 승격하지 않는다.
- 제거 가능 여부는 consumer migration 또는 contract update 뒤 별도 판단한다.

#### `STALE_REMOVE`

활성 소비자가 없고 현재 상태를 오도하는 과거 경로·토큰·상태. freshness audit 근거가 있을 때 제거한다.

### Handoff Closeout Invariant

```text
current_state_truth_is_fresh
AND machine_consumers_are_accounted_for
AND allowed_legacy_is_explicitly_labeled
AND exact_head_validation_is_green
```

이 네 조건이 동시에 충족되기 전에는 `HANDOFF_CHECKPOINT_GREEN` 또는 동등한 완료 상태를 주장하지 않는다.

### Project-learning extraction gate

Handoff closeout 과정에서 실제 CI 실패·복구로 **프로젝트를 넘어 반복될 수 있는 Base contract gap**이 발견되면:

1. Existing Solution First를 수행한다.
2. `REUSE / ABSORB / SPLIT / PROJECT_ONLY`를 판정한다.
3. `ABSORB` 또는 새 Base 후보가 남고 사용자가 Base 제안 작성을 요청했다면 프로젝트 Handoff merge 전에 proposal-only BCP를 제출한다.
4. Base proposal 제출은 활성 Base 구현 승인을 의미하지 않는다.

이 gate는 모든 Handoff에 BCP 작성을 강제하지 않는다. 재사용 가능한 gap이 없으면 `REUSE / NO_PROMOTION`으로 끝낸다.

## 프로젝트 전용으로 남길 내용

Base에 복사하지 않을 값:

- `urban-legend`의 PR 번호, commit SHA, Decision ID
- `Ver 4.2` / `Ver 4.3` 자체
- `CORE-VALIDATION-001`, `UX-PD-001 2A`, `mvp-039` 자체
- 프로젝트 Google Sheet 구조와 셀 주소
- Godot runtime blocker 내용
- 특정 Handoff 문서의 실제 compatibility token 집합

Base는 **분류·consumer inventory·검증·closeout 순서**만 소유한다.

## 적용 조건과 비사용 조건

### Use When

- Handoff/Active Context를 부분 수정이 아니라 큰 폭으로 압축·교체한다.
- 해당 문서를 테스트·workflow·validator·parser가 소비한다.
- 과거 상태 문자열을 지우면 자동 계약이 실패하거나, 반대로 보존하면 현재 상태처럼 오독될 수 있다.
- 세션 종료·담당자 교체·AI handoff 직전에 checkpoint를 merge하려 한다.
- Handoff 과정에서 재사용 가능한 Base 운영 gap이 실제 실패/복구로 드러났다.

### Do Not Use When

- 외부 소비자가 없는 단순 메모/오탈자 변경이다.
- 과거 토큰이 실제로 현재 authority이고 compatibility 분리가 필요 없다.
- 테스트가 명백히 잘못됐고 소비자 migration을 같은 승인 범위에서 안전하게 완료할 수 있다. 이 경우 legacy anchor를 영구 보존하지 말고 consumer를 고친다.
- project-only 상태·게임 규칙·버전 값을 Base 표준으로 승격하려 한다.
- reusable gap 없이 단순히 Handoff를 작성했다는 이유만으로 BCP를 만들려 한다.

## 반례와 위험

### Counterexample 1 — consumer migration이 더 맞는 경우

Handoff의 과거 token 하나를 오직 단일 테스트가 문자열 포함 여부로만 확인하고, 그 테스트가 이미 폐기된 요구를 잘못 고정한 것이 명백하다면 `HISTORICAL_COMPATIBILITY_ONLY`를 추가하는 대신 테스트를 새 contract로 migration하는 것이 맞다.

### Counterexample 2 — 단순 메모

개인 메모 파일처럼 workflow·parser·다른 문서가 소비하지 않는 Handoff를 한 줄 수정하는 경우 machine consumer inventory와 compatibility section을 강제할 필요가 없다.

### Risks

- compatibility section이 영구 쓰레기통이 될 수 있다.
- 오래된 상태를 compatibility라는 이름으로 무제한 보존할 수 있다.
- 테스트가 잘못된 경우에도 token을 계속 추가하는 방향으로 흐를 수 있다.
- Handoff closeout마다 Base proposal을 만들면 proposal noise가 증가할 수 있다.
- exact-head GREEN만 보고 Handoff 내용 자체의 의미 정확성을 놓칠 수 있다.

### Mitigation

- compatibility token마다 실제 consumer 또는 contract 근거가 있어야 한다.
- current-state section과 compatibility/history section을 분리한다.
- consumer가 제거되면 compatibility token도 freshness audit 대상이 된다.
- reusable Base gap이 없으면 BCP를 만들지 않는다.
- exact-head validation은 의미 검토를 대체하지 않고 마지막 closeout gate로만 사용한다.

## 영향 범위와 검증

### Existing Solution First

| 후보 | 판정 | 이유 |
|---|---|---|
| Handoff current-state router | `REUSE` | `maintaining-project-context-and-handoff`가 이미 소유 |
| stale/legacy reference 분류 | `REUSE` | `auditing-canonical-reference-freshness`가 이미 소유 |
| Base proposal lifecycle | `REUSE` | `managing-base-change-proposals`가 이미 소유 |
| Handoff machine-consumer inventory + compatibility-safe closeout | `ABSORB` | 기존 세 owner 사이의 호출/종료 연결이 명시적으로 부족 |
| 프로젝트별 legacy token 목록 | `PROJECT_ONLY` | Base 공용값이 아님 |

### 승인될 경우 예상 구현 범위

새 ACTIVE Skill은 만들지 않는다.

최소 후보:

- `skills/maintaining-project-context-and-handoff/SKILL.md`
  - `compatibility-safe-closeout` 또는 동등한 closeout 절차 추가
  - machine consumer inventory와 exact-head gate를 명시
- `skills/auditing-canonical-reference-freshness/SKILL.md`
  - Handoff/Active Context의 machine consumers와 compatibility-only token 분류 연결을 명시
- 기존 허용된 companion regression test
  - Handoff current truth와 historical compatibility가 섞이지 않는 계약
- 필요 시 learning log

`managing-base-change-proposals`의 상태 머신 자체를 바꿀 필요는 현재 증거만으로는 없다.

### Required Validation if Implemented

- focused RED: Handoff 교체 시 machine consumer inventory/compatibility classification contract 부재가 실패해야 함
- GREEN: 기존 Handoff/freshness owner 연동으로 통과
- Base canonical reference freshness: PASS
- Base proposal validator: PASS
- Base v9 operating contracts: PASS
- Game Project Operating System: PASS
- historical references가 current authority로 승격되지 않았는지 adversarial review
- 최소 한 개 추가 프로젝트 pilot: `NOT_RUN` 상태를 유지하다 실제 적용 뒤 갱신

## 필요한 도구·파일·권한

- 필요 항목: GitHub repository read/write, Base proposal registry, project exact-head CI evidence
- 필요한 이유: proposal 출처와 consumer contract 실패/복구를 재현 가능하게 연결하기 위해 필요
- 설치·적용 방법: 별도 설치 없음
- 설치 후 확인 명령: Base CI / proposal validator / reference freshness
- 최소 권한: proposal branch 작성 및 Draft PR 생성 권한

## 승인과 구현

- 사용자 제안 작성 요청 근거: 현재 대화 `2026-08-10 / "2번으로 해야지"` — Base 수정제안서를 먼저 작성한 뒤 프로젝트 Handoff PR을 병합하도록 요청
- 이 요청이 승인하는 범위: `submit` 모드의 proposal-only 작성/등록
- 활성 Base 구현 승인: `미승인`
- 구현 PR: `없음`
- proposal 상태: `SUBMITTED`
- 롤백: proposal PR을 병합하지 않거나, 병합 후에는 Registry 이력을 삭제하지 않고 `DEFERRED` 또는 `REJECTED`로 상태 전이한다. 활성 Base owner 파일은 이 proposal 단계에서 수정하지 않는다.

## Evidence ceiling

```yaml
source_project_failure_reproduced: true
source_project_recovery_verified: true
source_project_exact_head_ci_green: true
second_project_pilot: NOT_RUN
active_base_implementation: NOT_STARTED
human_comprehension_usability: NOT_RUN
knowledge_level: OBSERVATION
```
