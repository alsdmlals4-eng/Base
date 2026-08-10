# bcp-Blacksmith

## 출처와 상태

- Proposal ID: `BCP-2026-017-godot-pilot-failure-diagnostic-preservation`
- 사용자 표시명: `bcp-Blacksmith`
- 출처 프로젝트: `alsdmlals4-eng/Blacksmith`
- 출처 main: `68540e6cd288aff138b1ea4c5b1feeb9e0653947`
- 제출일: `2026-08-10`
- 상태: `SUBMITTED`
- 지식 상태: `관찰`
- Existing Solution Verdict: `NEW_BOUNDED_DIAGNOSTIC_GAP_NOT_DUPLICATE`
- 활성 Base 구현 승인: `NOT_GRANTED_IN_THIS_STAGE`

이 제안은 Blacksmith의 post-merge Godot Live-Editor Pilot에서 확인된 **fail-closed runtime 검증 실패 시 raw runtime-result 진단 증거가 최종 검증 호출 전에 보존되지 않을 수 있는 공용 관찰성 공백**을 Base에 제안한다.

이번 단계는 proposal storage만 수행한다. Base의 활성 Tool, Workflow, Skill, Template, Validator는 변경하지 않는다.

## 관찰과 증거

Blacksmith PR #141은 운영 handoff/current-state 정합화만 수행했고 제품 경로를 변경하지 않은 채 main `68540e6cd288aff138b1ea4c5b1feeb9e0653947`에 병합됐다.

같은 main에서 post-merge 검증 결과는 다음과 같았다.

1. Full validation run `31357963490`은 `SUCCESS`였다.
2. Godot Live-Editor Pilot run `31357963734` attempt 1은 runtime evidence 검증에서 `FAILURE`였다.
3. attempt 1 artifact `9051311634`에는 wrapper/process 실패 증거는 남았지만 검증 실패를 만든 raw `runtime-result.json`의 상세 payload가 최종 진단 bundle로 보존되지 않았다.
4. 같은 run의 failed-job rerun attempt 2는 **코드 변경 없이 같은 main SHA에서 `SUCCESS`**했다.

따라서 이 사례에서 확정할 수 있는 것은 **진단 증거 보존 공백**이다. attempt 1의 실제 transient runtime 원인은 재현되지 않았으므로 crash, race, transport, registration, timing 문제 중 어느 하나로 단정하지 않는다.

### 현재 Base 흐름에서 확인된 경계

현재 Godot pilot orchestration은 runtime result를 읽은 뒤 terminal verification을 수행한다. runtime status가 `FAIL`이면 검증이 예외/비정상 종료로 끝나며, 성공 검증 이후에 수행되는 상세 runtime bundle export 단계에 도달하지 못할 수 있다.

이 구조는 fail-closed 판정 자체로는 안전하지만, **실패 원인을 재현 없이 좁혀야 하는 다음 복구 작업에 필요한 원시 실패 payload가 사라질 수 있다.**

## Existing Solution First

현재 Base의 인접 BCP를 재조회했다.

- `BCP-2026-013-post-merge-continuation-state-reconciliation`은 post-merge 현재/역사 상태와 continuation truth를 소유한다. Blacksmith PR #141의 handoff 정합화는 이 owner와 중복되므로 새 proposal로 재제안하지 않는다.
- `BCP-2026-014-handoff-machine-consumer-compatibility-closeout`은 handoff의 machine-consumer 호환성 폐쇄를 소유한다. 이 또한 이번 제안의 대상이 아니다.
- `BCP-2026-015-external-runtime-session-same-snapshot-recovery`는 외부 Editor/MCP process·transport·server registry의 same-snapshot 복구 판정을 소유한다. 현재 제안은 session classification이 아니라 **검증 실패 payload의 artifact 보존 순서**를 다루므로 책임이 다르다.
- `BCP-2026-016-live-source-handoff-semantic-consumer-reconciliation`은 live source와 handoff semantic consumer 정합화를 소유한다. failure artifact payload 보존은 대상이 아니다.
- 기존 Godot Live Editor 안전 계약은 fail-closed 실행과 source mutation 보호를 제공한다. 이번 제안은 그 판정을 약화하지 않고 실패 관찰성만 보강하는 bounded extension이다.

따라서 새 broad Skill은 만들지 않고 기존 Godot pilot evidence/diagnostic owner가 흡수할 수 있는 proposal로만 등록한다.

## 일반화 후보

### Fail-Closed Runtime Diagnostic Preservation Contract

runtime 검증은 다음 순서를 기본으로 한다.

```text
raw runtime result 생성/수신
→ 최소 안전성 검사와 secret redaction
→ immutable diagnostic snapshot 보존
→ terminal semantic verification
→ PASS면 정상 evidence bundle 완성
→ FAIL이면 non-zero 유지 + preserved failure bundle 업로드
```

핵심 불변은 다음과 같다.

```text
PRESERVE_FAILURE_EVIDENCE
!= ACCEPT_FAILURE
!= RETRY_AS_SUCCESS
!= WEAKEN_VERIFICATION
```

### 제안하는 최소 계약

1. **Raw result first-preservation**
   - terminal verification 전에 raw runtime result 또는 의미상 동등한 immutable snapshot을 진단 위치에 보존한다.
2. **Fail-closed semantics unchanged**
   - runtime semantic status가 `FAIL`이면 최종 command/job은 여전히 non-zero/failure다.
3. **Failure bundle completeness**
   - 실패 artifact는 최소한 raw runtime result, project descriptor snapshot, relevant ledger/state snapshot, wrapper failure metadata를 연결할 수 있어야 한다.
4. **Redaction before publication**
   - token, credential, secret, 민감한 절대경로 등 기존 보안 정책이 금지하는 값은 artifact 업로드 전에 제거하거나 마스킹한다.
5. **No source mutation**
   - 진단 보존은 project tracked source를 수정하지 않는다.
6. **Retry evidence separation**
   - rerun/attempt 2 성공은 attempt 1 실패를 삭제하거나 성공으로 재분류하지 않는다. attempt별 evidence identity를 유지한다.

## 판정 상태

### `RUNTIME_PASS_WITH_DIAGNOSTICS`

runtime 검증이 통과했고 정상 evidence bundle이 보존된 상태.

### `RUNTIME_FAIL_DIAGNOSTICS_PRESERVED`

runtime 검증은 실패했지만 원시 실패 payload와 필요한 snapshot이 보존되어 후속 root-cause 분석이 가능한 상태.

### `RUNTIME_FAIL_DIAGNOSTICS_INCOMPLETE`

runtime 검증이 실패했고 terminal verification 이전 payload가 소실되어 원인을 안전하게 좁힐 수 없는 상태.

### `BLOCKED_UNVERIFIED`

artifact 자체 또는 source identity를 확인할 수 없어 실패 원인·재현성을 판단할 수 없는 상태.

## 반례와 위험

### MUST_FIX — 진단 보존을 성공 판정으로 오인

실패 payload가 잘 보존됐다는 이유로 runtime gate를 PASS 처리하면 안 된다. evidence completeness와 product/runtime correctness는 별도 축이다.

### MUST_FIX — secret이 raw payload에 포함됨

"원시 결과 보존"을 이유로 secret/token/민감한 환경 값을 그대로 artifact화하면 안 된다. redaction/allowlist가 먼저다.

### MUST_FIX — tracked project source에 진단 파일 생성

project checkout의 tracked 또는 product path를 진단 저장소로 사용하면 source-delta contract를 깨뜨릴 수 있다. runner temp/artifact workspace 등 비제품 경계를 사용한다.

### SHOULD_FIX — rerun 성공이 이전 실패를 덮음

attempt별 SHA/run/attempt identity를 유지해 transient failure 자체가 감사 가능해야 한다.

### SHOULD_FIX — 너무 큰 artifact

raw dump 전체를 무제한 보관하지 않는다. 실패 원인 판정에 필요한 bounded payload와 snapshot만 보존하고 retention을 기존 CI 비용 정책에 맞춘다.

## 프로젝트 전용으로 남길 내용

Base 공용 계약으로 승격하지 않는다.

- Blacksmith PR #141 번호와 제품 상태
- Blacksmith Task2/R3/R7 상태
- run `31357963490`, `31357963734`, artifact `9051311634` 같은 실행 식별자
- Blacksmith `project.godot`, Scene, Script, data 경로
- PR #81의 reference-only 상태
- Blacksmith의 HiGodot/GUT/Hera 구체 Decision ID

이 값들은 proposal의 출처 증거일 뿐 Base 일반 규칙이 아니다.

## 향후 구현 승인 시 수용 기준

이번 단계에서는 구현하지 않는다. 별도 `APPROVED_FOR_IMPLEMENTATION`이 생기면 최소 다음을 test-first로 검증한다.

1. synthetic runtime `FAIL` fixture를 만든다.
2. 기존 terminal verifier는 여전히 non-zero를 반환한다.
3. verifier가 종료되기 전에 sanitized raw runtime result가 diagnostic bundle에 존재한다.
4. descriptor/ledger/wrapper failure metadata가 같은 attempt identity로 연결된다.
5. secret fixture는 artifact에서 redacted된다.
6. project tracked source hash/diff는 진단 단계 전후 동일하다.
7. PASS fixture의 기존 artifact/exit semantics는 회귀하지 않는다.
8. retry attempt가 별도 evidence identity로 남는다.

## 영향 범위와 비영향 범위

### 이번 proposal 단계 영향

- 새 proposal `BCP-2026-017-godot-pilot-failure-diagnostic-preservation`
- Proposal Registry entry

### 이번 proposal 단계 비영향

- Base active Godot pilot tool/workflow
- Base Skill/Registry/generated active-skill view
- Godot Live Editor 안전 계약의 권위
- HiGodot/GUT/Hera 역할
- Blacksmith 저장소 및 제품 파일
- 자동 retry 정책
- runtime FAIL 판정 기준

## 필요한 도구·권한

Proposal 저장 단계:

- Base GitHub branch/PR 쓰기
- `[수정제안서]/**` 수정 권한
- Base proposal validator/required CI

향후 구현 단계에서만:

- Godot pilot evidence/orchestration owner
- synthetic fail/pass test fixture
- artifact redaction/retention contract

## 승인과 구현

- `bcp-Blacksmith` proposal storage: 사용자의 현재 지시로 진행 승인됨
- proposal status: `SUBMITTED`
- active Base implementation: `NOT_AUTHORIZED_IN_THIS_STAGE`
- approval_ref: `null`
- implementation PR: `null`

이 proposal의 병합은 Blacksmith에서 관찰된 재사용 가능한 실패 진단 보존 후보를 Base proposal registry에 저장하는 것만 의미한다. Base 활성 구현은 별도 승인과 별도 implementation PR을 요구한다.
