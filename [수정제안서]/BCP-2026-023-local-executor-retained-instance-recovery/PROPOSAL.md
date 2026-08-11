# BCP-2026-023 — Local executor retained-instance recovery

## 출처와 상태

- Proposal ID: `BCP-2026-023-local-executor-retained-instance-recovery`
- 사용자 표시명: `BCP - Ten Paces: retained local executor recovery`
- 출처 프로젝트: `alsdmlals4-eng/Ten-Paces-Hidden-Moves`
- 기준 커밋: `78acceab5a0689767aec9ce816e1225aa7d1f573`
- 출처 Project PR: `https://github.com/alsdmlals4-eng/Ten-Paces-Hidden-Moves/pull/163`
- 출처 Decision: `TEN-DEC-20260811-LOCAL-EXECUTOR-BOOTSTRAP-01`
- 제출일: `2026-08-12`
- 상태: `SUBMITTED`
- 지식 상태: `패턴`
- Existing Solution Verdict: `ABSORB`
- Project Application Closure: `PASS_BY_PROJECT_PR_163`
- Base active implementation authority: `NOT_GRANTED_IN_THIS_STAGE`

Ten Paces의 실제 Windows PowerShell 5.1 + Godot 4.7.1 + Godot AI 3.1.4 + Hera v1.0.0 + Codex CLI 복구에서 확인한 두 공용 경계를 기존 Base local-executor owner에 흡수하도록 제안한다.

1. fresh shell이 exact-project long-lived tool/editor를 재사용할 때 live instance가 startup 시 보존한 auth/config state를 fresh shell의 단일 추측으로 덮어쓰지 않는다.
2. native stderr 텍스트 또는 PowerShell `NativeCommandError` wrapper를 process failure 자체와 동일시하지 않고 exit code, semantic payload, command contract, 후속 readback으로 판정한다.

새 broad Skill은 만들지 않는다. `ONE_SHOT_LOCAL_EXECUTOR_BOOTSTRAP`, `PROJECT_DEDICATED_LOCAL_EXECUTION_ENVIRONMENT_FIRST`, BCP-015 same-snapshot recovery의 기존 owner 경계를 확장하는 후보이다.

## 관찰과 증거

### 프로젝트 적용과 검증

Project PR #163이 main `78acceab5a0689767aec9ce816e1225aa7d1f573`에 다음을 병합했다.

- repository-owned v5 launcher `tools/start_ten_paces_local_executor.ps1`.
- launcher regression `tests/test_local_executor_bootstrap_contract.py`.
- handoff/learning regression `tests/test_local_executor_handoff_contract.py`.
- 기존 `ten-paces-verification` owner의 `local-executor-readiness` mode.
- 기존 PR Validation에 두 contract와 launcher PowerShell parser consumer 연결.
- `LRN-TEN-LOCAL-001..004` 및 기존 Active Context/Handoff 동기화.

PR #163 exact head `0e3d81c41d92c6620559a3ccb83dca430db7f6ec`에서 18개 triggered workflow가 모두 SUCCESS였고, PR Validation은 launcher contract 10/10, handoff contract 5/5, launcher PowerShell parser를 PASS했다.

### Reused live-instance auth drift

v3에서는 exact-project Hera가 준비됐지만, 같은 long-lived editor를 새 PowerShell에서 재사용한 v4에서 `unauthorized: missing or wrong X-Hera-Token`이 재현됐다. plugin은 startup 시 auth state를 읽고 fresh shell은 다시 시작되므로 양쪽의 첫 auth assumption이 달라질 수 있었다.

v5는 **exact-project heartbeat/PID를 먼저 고정**한 뒤 현재 tool이 지원하는 source만 해당 exact instance에 대해 secret 출력 없이 검사했다.

```text
inherited env
→ project-approved dedicated source
→ tool-supported shared source
→ no-token only when no token candidate exists
```

실제 런타임은 `HERA_AUTH_SOURCE=shared_token` 다음 `HERA_EXACT_PROJECT_READY`까지 도달했고 raw token은 evidence에 저장하지 않았다.

### Native stderr semantic-state drift

project-specific `CODEX_HOME` 최초 로그인에서 Codex CLI가 정상적인 `Not logged in` 상태를 stderr로 알렸고 Windows PowerShell 5.1은 이를 `NativeCommandError` 형태로 포장했다. 초기 launcher는 wrapper 자체를 terminal failure로 오인했다.

후속 버전은 다음을 분리했다.

```text
process exit code
+ semantic payload
+ supported command contract
+ post-login status verification
```

그 결과 official Codex login 뒤 exact Ten Paces project에서 interactive session과 Sandbox ready까지 진입했다.

### Existing Solution First

- one-shot/dedicated-local-executor owner는 fresh shell, exact target, ports/profile isolation을 이미 소유한다.
- BCP-015는 process/transport/registry same-snapshot 및 stale identity를 소유한다.
- BCP-022는 semantic content change와 stat-only Git dirtiness를 분리한다.

그러나 current Base 검색에서는 **retained live auth/config source recovery**와 **native stderr semantic result classification**을 직접 소유하는 계약을 찾지 못했다. 따라서 `ABSORB`형 material extension이다.

## 일반화 후보

### Exact-instance retained-state recovery

```text
RESOLVE_EXACT_TARGET_INSTANCE
→ READ_SUPPORTED_CLIENT_STATE_FRESHLY
→ PROBE_ONLY_DOCUMENTED_AUTH_OR_CONFIG_SOURCES_AGAINST_EXACT_INSTANCE
→ ADOPT_FIRST_VERIFIED_SOURCE_IN_CURRENT_SHELL
→ READ_ONLY_READINESS
→ PERSISTENT_WORK
```

- historical PID/session/port는 current authority가 아니다.
- project identity 확정 전에 credential/config 후보를 다른 live instance에 보내지 않는다.
- source 후보는 tool의 documented/project-approved resolver에 한정한다.
- raw secret은 evidence에 저장하지 않고 source label/redacted receipt만 기록한다.
- known source가 모두 실패하면 unrelated process 종료나 강제 rotation 대신 fail closed한다.
- 새 exact instance에는 project-approved state를 주입할 수 있지만 already-running instance에서는 startup-retained state를 고려한다.

### Native process result classification

```text
PROCESS_EXIT_STATUS
+ SEMANTIC_PAYLOAD
+ COMMAND_CONTRACT
+ OPTIONAL_POSTCONDITION_READBACK
= RESULT_CLASSIFICATION
```

stderr 존재만으로 failure를 확정하지 않는다. known status payload는 semantic classifier로 구분하고 unknown nonzero는 fail closed한다. side effect가 있는 command는 가능한 경우 postcondition readback으로 확인한다. shell/version별 native stream 차이는 regression 범위에 둔다.

### Bootstrap과 readiness 분리

```text
PROCESS_STARTED_OR_REUSED
!= AUTHENTICATED_EXACT_INSTANCE_READY
!= PRODUCT_GREEN
```

retained-state recovery는 orchestration/recovery 계약이며 제품 테스트 PASS가 아니다.

## 프로젝트 전용으로 남길 내용

공용화하지 않는다.

- Ten Paces local/Godot/CODEX_HOME 경로.
- HiGodot HTTP 8003 / WS 9503.
- 특정 Hera PID/동적 port 및 이번에 선택된 `shared_token` source label.
- Ten Paces Decision ID, 버전 pin, launcher implementation details.
- project-specific credential file path.

## 적용 조건과 비사용 조건

### 적용 조건

- fresh shell/agent가 이전 shell과 별도로 시작한다.
- exact project의 long-lived editor/server/daemon을 재사용할 수 있다.
- live instance가 startup 시 auth/config/environment를 읽어 retained state를 가진다.
- CLI/bridge가 복수 supported auth/config source를 정의한다.
- native CLI가 stderr를 status/informational channel로도 사용할 수 있다.
- wrong-target fail-closed와 secret non-disclosure가 중요하다.

### 비사용 조건

- every invocation이 fully ephemeral이고 retained state가 없다.
- single process가 동일 environment를 끝까지 공유하여 drift가 생길 수 없다.
- remote auth probe 실패가 rate limit/account lockout을 유발할 수 있다. 이때는 provider의 official status/login flow를 사용한다.
- project/runtime identity를 먼저 신뢰할 수 있게 고정할 방법이 없다. 이 경우 auth probing 없이 `BLOCKED_UNVERIFIED`다.

## 반례와 위험

- **MUST_FIX — credential guessing loop:** documented/project-approved source 외 임의 파일·환경변수·계정을 전수 탐색하지 않는다.
- **MUST_FIX — secret disclosure:** source label은 허용해도 raw token/password/key/cookie는 로그·Handoff·BCP에 저장하지 않는다.
- **MUST_FIX — wrong instance probing:** exact project/process/registry identity가 먼저다.
- **MUST_FIX — stderr 무시로 역과잉 교정:** stderr를 무조건 성공으로 무시하지 않는다. unknown nonzero는 fail closed한다.
- **SHOULD_FIX — shell/version 과잉 일반화:** Windows PowerShell 5.1 관찰을 모든 shell에 그대로 가정하지 않는다.
- **Counterexample — remote auth provider:** 실패 probe가 외부 lockout을 만들 수 있으면 후보 순회를 사용하지 않는다.

## 영향 범위와 검증

Existing Solution Verdict는 `ABSORB`다. 승인된 별도 구현 단계가 있다면 최소 후보 owner는 one-shot launcher/recovery contract, project-dedicated local environment reference, BCP-015의 exact-instance recovery 경계와 관련 generic project adapter/test consumer다. **이번 proposal-only 단계에서는 active Base 파일을 수정하지 않는다.**

후속 구현 검증 시나리오:

- fresh shell + exact long-lived instance + same source → reuse PASS.
- first documented source mismatch + second documented source match → exact instance 유지 + source label만 출력.
- no source authenticates → fail closed, unrelated process untouched.
- foreign instance → credential probing 없음.
- native CLI known status on stderr → expected semantic state 판정.
- unknown nonzero → terminal failure.
- side-effecting auth flow success → postcondition status readback.
- secret literal output/evidence = 0.
- orchestration PASS가 project/product PASS를 자동 승격하지 않음.

### Benchmark

2026-08-12 공식 1차 출처 대조:

- Microsoft PowerShell command guidance는 native stderr가 PowerShell Error stream에 연결되지만 많은 native command가 추가 정보에도 stderr를 사용할 수 있어 혼동이 생길 수 있음을 설명한다. explicit 실행·redirect 제어가 필요할 때 `Start-Process`도 제공한다.
  - https://learn.microsoft.com/en-us/powershell/scripting/learn/shell/running-commands
- Godot command-line reference는 `--recovery-mode`가 tool scripts/editor plugins를 비활성화하고, `--quit-after`가 iteration 수이며, `--script`가 standalone tool이고, `--path`가 project를 고정함을 명시한다. capability/context-aware launcher가 필요한 근거다.
  - https://docs.godotengine.org/en/latest/tutorials/editor/command_line_tutorial.html
- GitHub required-check guidance는 current/latest validation identity가 중요하고 이전 commit의 성공은 현재 required check를 충족하지 못한다고 명시한다. historical runtime locator를 current truth로 재사용하지 않는 본 제안과 같은 freshness 원리다.
  - https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/troubleshooting-required-status-checks

### Regression / rollback

기존 one-shot, same-snapshot/stale-identity, unrelated-process 보호와 proposal lifecycle은 유지한다. 후속 구현이 credential handling을 과도하게 넓히거나 native classification을 불안정하게 만들면 retained-state/native-result extension만 되돌리고 기존 exact-instance contract는 보존한다.

## 필요한 도구·파일·권한

- 필요 항목: `[수정제안서]/**` proposal-only write/PR/merge 권한.
- 필요한 이유: 검증된 Ten Paces 공용 후보와 Registry identity 보존.
- 설치·적용 방법: 추가 설치 없음.
- 설치 후 확인 명령: `python tools/check_base_change_proposals.py --root . --base-ref <latest-main>` 및 현행 Base proposal CI.
- 최소 권한: proposal 파일+Registry 저장/병합. Base active Skill/Docs/Template/Test/Tool/Workflow 구현 권한은 이 단계에 포함되지 않는다.

## 승인과 구현

- 사용자 승인 근거: 2026-08-12 Ten Paces 인수인계 지시와 `단일파일_실행_프로젝트병합_Base수정제안서전용_통합작업지시문_v5.0.md`가 **proposal storage/merge authority**를 부여함.
- Base active implementation authority: `NOT_GRANTED_IN_THIS_STAGE`.
- Proposal 상태: `SUBMITTED`.
- 구현 PR: `없음`.
- implementation status: `NOT_STARTED_IN_THIS_STAGE`.
- implementation boundary: `SEPARATE_FOLLOWUP_STAGE`.
- 롤백: proposal이 채택되지 않아도 evidence/status를 lifecycle에 따라 보존하고 active Base 구현은 수행하지 않는다.
