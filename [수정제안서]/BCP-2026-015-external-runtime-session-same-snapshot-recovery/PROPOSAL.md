# BCP - OMENWARD

## 출처와 상태

- Proposal ID: `BCP-2026-015-external-runtime-session-same-snapshot-recovery`
- 사용자 표시명: `BCP - OMENWARD`
- 출처 프로젝트: `alsdmlals4-eng/omenward`
- 출처 Decision: `OMW-DEC-20260809-PLANNING-BARRACKS-ROLE-OUTPUT-RUNTIME-IMPLEMENTATION-PACKAGE-V1`
- 출처 runtime head: `bde85549560fca90f7aa25fc4842bc0a3afb92e7`
- 제출일: `2026-08-10`
- 상태: `SUBMITTED`
- 지식 상태: `관찰`
- Existing Solution Verdict: `MATERIAL_SCOPE_EXTENSION_NOT_DUPLICATE`
- 활성 Base 구현 승인: `NOT_GRANTED_IN_THIS_STAGE`

이 제안은 OMENWARD 작업에서 확인된 **외부 Editor/MCP runtime session의 process·transport·server registry 상태가 서로 어긋날 때, 같은 시점의 증거로 복구 상태를 판정하는 공용 계약**을 Base에 제안한다.

이 파일은 기존 BCP-013의 내용을 변경하거나 확장하는 evidence가 아니다. 이전에 OMENWARD 내용을 BCP-013의 `evidence/BCP-OMENWARD.md`로 넣은 것은 프로젝트별 수정제안서를 별도 생성해야 한다는 사용자 의도를 잘못 해석한 것이므로, 해당 파일은 제거하고 BCP-013의 기존 소유 경계를 복구한다.

## Existing Solution First

현재 Base에는 인접한 계약이 존재하지만 이번 실패 경계를 직접 소유하지 않는다.

### BCP-2026-005 — Godot Live Editor 안전 계약 v2

BCP-005는 다음을 이미 소유한다.

- `effect_kind`, `idempotency`, `approval_policy`, `execution_mode`, `rollback_policy` 분리
- automation server / Editor instance / runtime session / contract snapshot binding
- transport 인증 및 session 제약
- stale observation을 mutation precondition으로 사용하지 않는 규칙
- 장기 task와 Editor recovery 경계

그러나 **외부 Editor process가 살아 있고 transport도 연결되어 보이는데 server의 session registry에는 target project가 보이지 않는 상황**에서 process, socket, handshake log, registry를 같은 관측창으로 묶어 원인을 분류하는 recovery protocol은 명시하지 않는다.

### BCP-2026-010 — 연속작업 실행 루프

BCP-010은 `BLOCKED_UNVERIFIED`에서 연속 실행을 중단하고 검증 가능한 다음 작업을 보존하는 실행 권한을 소유한다. 하지만 외부 runtime session 자체의 liveness/registration 복구 판정은 소유하지 않는다.

### BCP-2026-013 — Post-Merge Continuation-State Reconciliation

BCP-013은 merge/integration 이후 live continuation truth를 다시 읽는 lifecycle을 소유한다. 이번 문제는 merge 이후 문서 freshness가 아니라 **동일 시점 외부 process/transport/registry 관측 불일치**이므로 별도 실패 경계다.

### BCP-2026-014 — Handoff Machine-Consumer Compatibility Closeout

BCP-014는 Handoff를 읽는 machine consumer와 historical compatibility를 다룬다. Editor/MCP runtime session registration은 대상이 아니다.

따라서 새 broad Skill을 제안하지는 않지만, 기존 Godot Live Editor/외부 runtime automation owner가 흡수할 수 있는 **별도 canonical BCP**로 등록한다.

## 프로젝트 관찰

OMENWARD의 승인된 barracks role-output runtime 작업은 Godot 4.7.1과 HiGodot/Godot AI MCP를 persistent authoring 경로로 사용한다.

복구 과정에서 다음 사실이 서로 다른 시점에 관찰됐다.

1. exact OMENWARD Godot 4.7.1 GUI process와 console process가 살아 있었다.
2. OMENWARD GUI process가 Godot-AI websocket port에 `ESTABLISHED` 연결을 가지고 있었다.
3. 잠시 뒤 `session_manage(op=list)`는 다른 프로젝트 session만 반환하고 OMENWARD를 반환하지 않았다.
4. process/transport 관측과 registry 관측이 몇 분 떨어져 있었기 때문에 `SAME_SERVER_HANDSHAKE_REGISTRATION_FAILURE`를 확정할 수 없었다.

즉 다음과 같은 잘못된 결론을 피해야 했다.

- "session list에 없으니 Godot가 crash했다"
- "process가 전에 살아 있었으니 지금도 같은 process가 살아 있다"
- "WS 연결이 있었으니 registry에도 반드시 등록돼 있다"
- "target session이 없으니 shared Godot-AI server를 재시작하면 된다"

이 사례의 상세 project-specific 증거는 `evidence/OMENWARD_RUNTIME_SESSION_RECOVERY_EVIDENCE.md`에 둔다.

## 일반화 후보

### Same-Snapshot External Runtime Session Recovery Contract

외부 Editor/MCP session이 사라졌거나 registry와 runtime 상태가 충돌할 때 다음 네 증거를 **가능한 한 동일한 짧은 관측창에서** 확인한다.

```text
TARGET_PROCESS_IDENTITY
+ TARGET_TRANSPORT_OWNERSHIP
+ SERVER_HANDSHAKE_AND_SESSION_LOGS
+ IMMEDIATE_SESSION_REGISTRY_READ
= RECOVERY_CLASSIFICATION
```

필수 관측:

1. **Target process identity**
   - 현재 process 존재 여부
   - executable/version
   - project root 또는 동등한 target identity
   - command line 또는 target을 식별할 수 있는 현재 값
2. **Transport ownership**
   - 해당 current process가 실제로 기대 transport를 소유하는지
   - 연결 상태가 현재 시점에 live인지
3. **Server-side bounded logs**
   - connection / handshake / authentication / reconnect / session registration 관련 최근 로그
   - 과거 run 전체가 아니라 현재 관측창에 연결되는 bounded evidence
4. **Immediate registry read**
   - 위 관측 직후 session registry/list를 읽어 exact target이 등록되어 있는지 확인

### 판정 상태

#### `EXACT_SESSION_RECOVERED`

```text
current exact target process present
AND expected transport present
AND registry contains exact target session
```

이 경우에만 persistent authoring 또는 target-specific executor를 재개한다.

#### `SAME_SERVER_HANDSHAKE_REGISTRATION_BLOCKER`

```text
current exact target process present
AND expected transport is live from that process
AND immediate registry omits exact target
AND bounded server logs are consistent with the same observation window
```

이 상태에서는 process 재시작이나 executor/session-selection patch보다 handshake/registration 원인을 먼저 진단한다.

#### `PROCESS_OR_TRANSPORT_BLOCKER`

```text
current exact target process missing
OR expected transport not owned/live
```

이 경우 registry omission을 handshake 문제로 확정하지 않는다. process/transport 복구가 먼저다.

#### `BLOCKED_UNVERIFIED`

동일 관측창을 만들 수 없거나 required evidence 중 하나가 없으면 원인을 추정하지 않는다.

### Process disappearance wording

관측했던 process가 이후 사라졌다면 다음처럼만 기록한다.

```text
PROCESS_EXITED_OR_NO_LONGER_RUNNING
REASON = UNVERIFIED
```

crash, kill, timeout, 정상 종료 등 원인은 별도 증거 없이 추정하지 않는다.

## Shared Server 보호 규칙

여러 프로젝트 Editor가 같은 automation server를 사용할 수 있으므로 한 target session의 omission만으로 shared server를 종료하거나 재시작하지 않는다.

```text
ONE_TARGET_SESSION_MISSING
!= SHARED_SERVER_SAFE_TO_RESTART
```

필수 보호 경계:

- unrelated project session과 Editor를 보존한다.
- target root가 다른 session을 대신 선택하지 않는다.
- exact target registration이 확인되기 전에 다른 project session에 mutation을 보내지 않는다.
- root-cause evidence 전에 session-selection/executor matching logic을 패치하지 않는다.
- server restart가 필요하더라도 영향받는 session inventory와 명시적 안전 근거를 먼저 확보한다.

## Stale Identity 방지

PID, websocket connection, session id, Editor instance id는 시간이 지나면 current authority가 아니다.

```text
PAST_PID != CURRENT_TARGET
PAST_WS_CONNECTION != CURRENT_TRANSPORT_PROOF
PAST_SESSION_ID != CURRENT_REGISTRY_PROOF
```

Handoff에는 과거 관측값을 historical evidence로 남길 수 있지만, 다음 실행에서 current target identity로 재사용하기 전에 fresh-read해야 한다.

## Recovery 후 실행 Gate

외부 runtime session 복구 성공과 제품/runtime 작업 완료는 분리한다.

```text
SESSION_RECOVERY_GREEN
→ exact target verified
→ approved executor/runtime work may resume
→ project tests/runtime validation still required separately
```

session recovery가 Green이어도 제품 기능, GUT, import, smoke, human QA 또는 release readiness를 자동 PASS로 승격하지 않는다.

## 적용 조건

다음 상황에 사용한다.

- Godot/Unity/기타 Editor와 외부 automation server가 별도 process/session registry를 유지하는 경우
- MCP/WebSocket/HTTP/STDIO bridge가 Editor process와 server-side session을 별도로 추적하는 경우
- process는 살아 있는데 session registry에서 target이 보이지 않는 경우
- reconnect 후 이전 session identity를 재사용해도 되는지 판단해야 하는 경우
- shared automation server가 여러 project Editor를 동시에 다루는 경우

## 비사용 조건

다음에는 이 계약을 강제하지 않는다.

- 단일 process 안에서 session registry 자체가 없는 단순 CLI 작업
- repository 문서 freshness만의 문제
- 이미 exact target session이 검증되어 있고 runtime 기능 실패를 디버깅하는 경우
- server가 프로젝트별 완전 격리 instance이고 shared-session 영향이 존재하지 않는 경우

## 반례와 위험

### MUST_FIX — 시간차가 큰 증거를 같은 원인으로 묶는 오류

process/WS를 먼저 보고 몇 분 뒤 registry를 보면 중간 상태 변화를 놓칠 수 있다. 같은 관측창이 아니면 `SAME_SERVER_HANDSHAKE_REGISTRATION_BLOCKER`를 확정하지 않는다.

### MUST_FIX — registry omission을 crash로 오인

registry에 없다는 사실은 process crash 증거가 아니다. process와 transport를 별도로 확인한다.

### MUST_FIX — shared server를 target 전용으로 오인

다른 프로젝트 session이 살아 있을 수 있으므로 target 하나의 복구를 위해 shared server를 무조건 종료하면 안 된다.

### MUST_FIX — stale PID/session id를 current authority로 재사용

과거 PID와 session id는 historical evidence일 뿐이다. 재개 시 fresh target identity를 다시 읽는다.

### SHOULD_FIX — 로그 범위가 너무 넓어 원인이 섞임

가능하면 observation timestamp 주변의 bounded server logs를 사용하고 다른 project connection 이벤트와 구분한다.

## 제안되는 Base 흡수 위치

새 broad Skill을 만들지 않는다. 구현 승인 시 우선 다음 기존 owner를 검토한다.

1. `BCP-2026-005-godot-live-editor-contract-v2`가 구현한 Godot Live Editor 안전 계약과 관련 validator/reference
2. 외부 runtime session을 다루는 기존 project adapter/template contract
3. `maintaining-project-context-and-handoff`에는 stale PID/session을 current authority로 재사용하지 않는 continuation 문구만 최소 연결

BCP-010/013/014의 책임은 변경하지 않는다.

## 검증 시나리오

### Scenario A — exact session recovered

Given the exact current project Editor process and its expected transport,
when the immediate session registry contains the exact project session,
then recovery is Green and target-specific execution may resume.

### Scenario B — live transport but registry omission

Given the exact current project process owns a live transport,
when the immediate registry omits the target in the same observation window,
then classify a handshake/registration blocker instead of a generic crash.

### Scenario C — process disappeared

Given a process was observed earlier,
when the current snapshot no longer contains it,
then record that it exited or is no longer running and keep the reason unverified.

### Scenario D — shared server has unrelated sessions

Given a shared server contains another project's healthy session,
when the target project session is missing,
then do not restart/kill the shared server solely from the target omission.

### Scenario E — stale identity after handoff

Given a handoff contains a PID/session id from a previous execution,
when a new execution begins,
then current process/transport/registry truth must be read before that identity is used for mutation.

## 영향 범위와 검증

이번 단계는 proposal storage만 수행한다.

- 새 canonical proposal `BCP-2026-015-external-runtime-session-same-snapshot-recovery`
- OMENWARD project-specific evidence
- Proposal Registry entry
- 잘못 배치했던 BCP-013의 OMENWARD evidence 제거 및 기존 BCP-013 소유 경계 복구

이번 단계에서 변경하지 않는다.

- Base active Skill/Method/Template/Test/Workflow
- BCP-005/010/013/014의 기존 canonical proposal 본문
- release lock / generated view
- OMENWARD runtime 제품 코드

## 승인과 구현

- proposal storage 및 별도 `BCP - OMENWARD` 생성: 사용자 지시로 승인됨
- active Base implementation: `NOT_AUTHORIZED_IN_THIS_STAGE`
- approval_ref: `null`
- implementation PR: `null`
- 상태: `SUBMITTED`

이 제안의 병합은 공용 개선 후보를 독립 수정제안서로 저장하는 것만 의미한다. 실제 Base 활성 계약 반영은 별도 `APPROVED_FOR_IMPLEMENTATION` 결정과 구현 검증을 거쳐야 한다.
