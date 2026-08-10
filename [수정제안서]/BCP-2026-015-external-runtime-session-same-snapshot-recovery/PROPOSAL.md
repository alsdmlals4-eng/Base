# BCP - OMENWARD

## 출처와 상태

- Proposal ID: `BCP-2026-015-external-runtime-session-same-snapshot-recovery`
- 사용자 표시명: `BCP - OMENWARD`
- 출처 프로젝트: `alsdmlals4-eng/omenward`
- 출처 Decision: `OMW-DEC-20260809-PLANNING-BARRACKS-ROLE-OUTPUT-RUNTIME-IMPLEMENTATION-PACKAGE-V1`
- 출처 runtime head: `bde85549560fca90f7aa25fc4842bc0a3afb92e7`
- 제출일: `2026-08-10`
- 상태: `APPROVED_FOR_IMPLEMENTATION`
- 지식 상태: `관찰`
- Existing Solution Verdict: `MATERIAL_SCOPE_EXTENSION_NOT_DUPLICATE`
- 활성 Base 구현 승인: `NOT_GRANTED_IN_THIS_STAGE`

이 제안은 OMENWARD 작업에서 확인된 **외부 Editor/MCP runtime session의 process·transport·server registry 상태가 서로 어긋날 때 같은 시점의 증거로 복구 상태를 판정하는 공용 계약**을 Base에 제안한다.

이전 Base PR #243에서 OMENWARD 내용을 BCP-013의 evidence로 넣은 것은 프로젝트별 수정제안서를 별도 생성해야 한다는 사용자 의도를 잘못 해석한 것이다. 본 제안에서는 그 파일만 제거하고 BCP-013의 기존 proposal과 다른 프로젝트 evidence를 보존한 채 OMENWARD를 별도 canonical proposal로 분리한다.

## 관찰과 증거

OMENWARD의 승인된 barracks role-output runtime 작업은 Godot 4.7.1과 HiGodot/Godot AI MCP를 persistent authoring 경로로 사용한다.

복구 과정에서 서로 다른 시점에 다음이 관찰됐다.

1. exact OMENWARD Godot 4.7.1 GUI/console process가 살아 있었다.
2. OMENWARD GUI process가 Godot-AI websocket port에 `ESTABLISHED` 연결을 가지고 있었다.
3. 잠시 뒤 `session_manage(op=list)`는 다른 프로젝트 session만 반환하고 OMENWARD를 반환하지 않았다.
4. process/transport와 registry 관측이 몇 분 떨어져 있었기 때문에 `SAME_SERVER_HANDSHAKE_REGISTRATION_FAILURE`를 확정할 수 없었다.

이 사례에서 피해야 할 잘못된 결론은 다음과 같다.

- session list에 없다는 이유만으로 Godot crash를 단정한다.
- 이전에 살아 있던 process/PID를 현재 target identity로 재사용한다.
- 과거 WS 연결이 있었다는 이유로 현재 registry registration을 가정한다.
- target session 하나가 없다는 이유로 shared automation server를 종료한다.

상세 project-specific 값은 `evidence/OMENWARD_RUNTIME_SESSION_RECOVERY_EVIDENCE.md`에 분리한다.

### Existing Solution First

현재 Base에는 인접 계약이 있지만 이번 실패 경계를 직접 소유하지 않는다.

- **BCP-2026-005 Godot Live Editor 안전 계약 v2**: operation policy, server/Editor/runtime-session binding, transport 제약, stale mutation precondition, recovery 경계를 소유하지만 process/socket/server-registry를 같은 관측창으로 묶는 liveness/registration triage는 명시하지 않는다.
- **BCP-2026-010 연속작업 실행 루프**: `BLOCKED_UNVERIFIED` 중단과 재개 권한을 소유하지만 외부 runtime session 복구 판정은 소유하지 않는다.
- **BCP-2026-013 Post-Merge Continuation-State Reconciliation**: merge 이후 live continuation truth를 다루며 외부 runtime process/transport/registry 불일치를 다루지 않는다.
- **BCP-2026-014 Handoff Machine-Consumer Compatibility Closeout**: Handoff machine consumer 호환성을 다루며 Editor/MCP registration은 대상이 아니다.

따라서 새 broad Skill을 만들지는 않지만 기존 Godot Live Editor/외부 runtime automation owner가 흡수할 수 있는 **별도 canonical BCP**로 등록한다.

## 일반화 후보

### Same-Snapshot External Runtime Session Recovery Contract

외부 Editor/MCP session이 사라졌거나 registry와 runtime 상태가 충돌할 때 다음 네 증거를 가능한 한 동일한 짧은 관측창에서 확인한다.

```text
TARGET_PROCESS_IDENTITY
+ TARGET_TRANSPORT_OWNERSHIP
+ SERVER_HANDSHAKE_AND_SESSION_LOGS
+ IMMEDIATE_SESSION_REGISTRY_READ
= RECOVERY_CLASSIFICATION
```

필수 관측은 다음과 같다.

1. **Target process identity**
   - current process 존재 여부
   - executable/version
   - project root 또는 동등한 target identity
   - command line 또는 현재 target 식별값
2. **Transport ownership**
   - current target process가 기대 transport를 실제 소유하는지
   - 연결 상태가 현재 시점에 live인지
3. **Server-side bounded logs**
   - connection / handshake / authentication / reconnect / session registration 관련 최근 로그
   - 현재 관측창에 연결되는 bounded evidence
4. **Immediate registry read**
   - 위 관측 직후 exact target session이 registry/list에 존재하는지 확인

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
AND bounded server logs belong to the same observation window
```

이 상태에서는 process 재시작이나 executor/session-selection patch보다 handshake/registration 원인을 먼저 진단한다.

#### `PROCESS_OR_TRANSPORT_BLOCKER`

```text
current exact target process missing
OR expected transport not owned/live
```

registry omission을 handshake 문제로 확정하지 않는다.

#### `BLOCKED_UNVERIFIED`

동일 관측창을 만들 수 없거나 required evidence 중 하나가 없으면 원인을 추정하지 않는다.

### Process disappearance wording

이전에 관측했던 process가 현재 보이지 않으면 다음처럼만 기록한다.

```text
PROCESS_EXITED_OR_NO_LONGER_RUNNING
REASON = UNVERIFIED
```

별도 증거 없이 crash, kill, timeout, 정상 종료를 확정하지 않는다.

### Shared Server 보호

```text
ONE_TARGET_SESSION_MISSING
!= SHARED_SERVER_SAFE_TO_RESTART
```

- unrelated project session과 Editor를 보존한다.
- target root가 다른 session을 대신 선택하지 않는다.
- exact target registration 전 다른 project session에 mutation을 보내지 않는다.
- root-cause evidence 전에 session-selection/executor matching logic을 패치하지 않는다.
- server restart가 필요하다면 영향받는 session inventory와 안전 근거를 먼저 확보한다.

### Stale Identity 방지

```text
PAST_PID != CURRENT_TARGET
PAST_WS_CONNECTION != CURRENT_TRANSPORT_PROOF
PAST_SESSION_ID != CURRENT_REGISTRY_PROOF
```

Handoff에는 과거 값을 historical evidence로 남길 수 있지만 새 실행에서 current identity로 사용하기 전에 fresh-read한다.

### Recovery와 제품 Green 분리

```text
SESSION_RECOVERY_GREEN
→ exact target verified
→ approved runtime work may resume
→ project tests/runtime validation remain separate
```

session recovery Green은 제품 기능, GUT, import, smoke, human QA, release readiness를 자동 PASS로 승격하지 않는다.

## 프로젝트 전용으로 남길 내용

Base 공용 규칙으로 승격하지 않는다.

- OMENWARD PR #175 / Issue #176 번호
- 특정 Windows PID
- WS9500 자체
- 특정 session id
- OMENWARD local path
- barracks role-output 기능과 일곱 runtime gap
- FV metric과 provisional numerics

Base에 일반화하는 것은 same-snapshot process/transport/log/registry 증거, fail-closed 분류, shared-session 보호, stale identity 방지다.

## 적용 조건과 비사용 조건

### 적용 조건

- Godot/Unity/기타 Editor와 외부 automation server가 별도 process/session registry를 유지한다.
- MCP/WebSocket/HTTP/STDIO bridge가 Editor process와 server-side session을 별도로 추적한다.
- process는 살아 있는데 session registry에서 target이 보이지 않는다.
- reconnect 후 과거 session identity를 재사용해도 되는지 판단해야 한다.
- shared automation server가 여러 project Editor를 동시에 다룬다.

### 비사용 조건

- session registry가 없는 단순 CLI 작업
- repository 문서 freshness만의 문제
- exact target session이 이미 검증되어 있고 제품 runtime 기능 자체를 디버깅하는 경우
- 프로젝트별 완전 격리 server라 shared-session 영향이 없는 경우

## 반례와 위험

### MUST_FIX — 시간차가 큰 증거를 같은 원인으로 묶는 오류

process/WS와 registry를 몇 분 간격으로 보면 중간 변화를 놓친다. 같은 관측창이 아니면 `SAME_SERVER_HANDSHAKE_REGISTRATION_BLOCKER`를 확정하지 않는다.

### MUST_FIX — registry omission을 crash로 오인

registry omission은 process crash 증거가 아니다. process와 transport를 별도 확인한다.

### MUST_FIX — shared server를 target 전용으로 오인

다른 프로젝트 session이 살아 있을 수 있으므로 target 하나의 복구를 위해 shared server를 무조건 종료하지 않는다.

### MUST_FIX — stale PID/session id 재사용

과거 PID와 session id는 historical evidence다. 재개 시 fresh identity를 다시 읽는다.

### SHOULD_FIX — 로그 범위가 너무 넓어 원인이 섞임

observation timestamp 주변 bounded server logs를 사용하고 다른 project connection event와 구분한다.

## 영향 범위와 검증

이번 단계는 proposal storage만 수행한다.

- 새 canonical proposal `BCP-2026-015-external-runtime-session-same-snapshot-recovery`
- OMENWARD project-specific evidence
- Proposal Registry BCP-015 entry
- 잘못 배치했던 BCP-013의 OMENWARD evidence 제거 및 기존 BCP-013 소유 경계 복구

구현 승인 시 우선 다음 기존 owner 흡수를 검토한다.

1. BCP-005가 구현한 Godot Live Editor 안전 계약의 validator/reference
2. 외부 runtime session을 다루는 기존 project adapter/template contract
3. `maintaining-project-context-and-handoff`에는 stale PID/session을 current authority로 재사용하지 않는 문구만 최소 연결

필수 검증 시나리오:

- exact target process + transport + registry present → `EXACT_SESSION_RECOVERED`
- exact target process + transport present + same-window registry omission → handshake/registration blocker
- process missing → process exited/no longer running, reason unverified
- unrelated healthy session present → shared server 자동 종료 금지
- handoff의 과거 PID/session id → fresh-read 전 mutation 금지

이번 proposal-only 단계에서는 Base active Skill/Method/Template/Test/Workflow, BCP-005/010/013/014 본문, release lock, generated view, OMENWARD 제품 코드를 변경하지 않는다.

## 필요한 도구·파일·권한

Proposal 저장 단계:

- Base GitHub branch/PR 쓰기
- `[수정제안서]/**` 수정 권한
- Base proposal validator와 required GitHub Actions

향후 구현 단계에서만 필요할 수 있는 항목:

- 기존 Godot Live Editor contract/validator 파일
- project adapter/template contract
- process/socket/session registry를 재현할 수 있는 격리 test harness

이번 proposal 병합은 외부 runtime server 설치나 production 권한 확대를 요구하지 않는다.

## 승인과 구현

- 기존 BCP-013 복구 및 별도 `BCP - OMENWARD` proposal storage: 사용자 지시로 승인됨
- proposal status: `APPROVED_FOR_IMPLEMENTATION`
- active Base implementation: `AUTHORIZED_MINIMAL_ABSORB_2026_08_10`
- approval_ref: `[수정제안서]/BCP-2026-015-external-runtime-session-same-snapshot-recovery/PROPOSAL.md#승인과-구현`
- implementation PR: `null`

사용자는 2026-08-10 KST 대화에서 `좋아 다 승인할게 [연속작업] 진행해`로 이 제안의 최소 기존-owner 흡수를 승인했다. 구현은 별도 PR에서 same-snapshot 분류·shared server 보호·stale identity 차단만 다루며, 외부 server 설치·restart·production 권한 확대는 제외한다.
