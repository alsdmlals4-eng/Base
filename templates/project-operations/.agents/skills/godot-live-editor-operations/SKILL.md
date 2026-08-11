---
name: godot-live-editor-operations
description: Use in an installed Godot project when HiGodot authoring, deterministic GDScript testing, or bounded live runtime QA must be bootstrapped, executed, validated, resumed, recovered, or upgraded.
---

# Godot Live Editor Operations

## 책임과 단일 persistent 저작 권위

이 파일은 프로젝트에 설치되는 얇은 작업 Skill이다. 공용 정책은 다음 Base 정본에서 읽고 프로젝트에 복제하지 않는다.

- `docs/knowledge/godot/HIGODOT_SINGLE_AUTHORITY_AND_SAFE_OPERATION.md`

```yaml
provider: hi-godot/godot-ai
execution_authority: SOLE_GODOT_EXECUTION_AUTHORITY
persistent_authoring_authority: SOLE_PERSISTENT_GODOT_AUTHORING_AUTHORITY
authority_count: 1
network_mode: LOOPBACK_ONLY

gut:
  role: DETERMINISTIC_GDSCRIPT_TEST_AUTHORITY_WHEN_ADOPTED
  authoring_authority: false

hera_agent_godot:
  role_restriction: LIVE_QA_AND_OBSERVABILITY_ONLY
  persistent_source_mutation: forbidden
  authoring_authority: false
```

HiGodot Godot AI addon과 MCP 서버만 현재 Godot persistent 편집·저작 실행 권위다. Base custom MCP, Base network Bridge와 과거 live-editor Adapter는 현재 실행 fallback이 아니다. Hera는 unrestricted editor writer 또는 persistent mutation authority가 될 수 없고, 채택된 프로젝트에서 `LIVE_QA_AND_OBSERVABILITY_ONLY` 역할로만 사용한다. GUT은 채택된 프로젝트의 deterministic GDScript test를 담당하며 저작 권위를 갖지 않는다.

과거 Base 계약·Schema·Pilot·테스트는 보안·evidence·rollback의 감사 자료로만 읽는다.

프로젝트는 `HIGODOT_ADOPTION_RECORD.json`에서 HiGodot provider pin, Godot 버전, host client, enabled domain, 검증 증거와 rollback pin을 소유한다. GUT과 Hera의 exact version/pair, adoption state, consumption path, owner boundary와 rollback/removal은 프로젝트의 기존 third-party/addon inventory가 소유한다.

## 표준 작업 흐름

```text
HiGodot author
→ Godot import / parse
→ GUT deterministic GDScript test when adopted and required
→ GUT affected/full regression at the package gate
→ tracked source pre-Hera snapshot
→ Hera live QA when adopted and required
→ tracked source post-Hera snapshot
→ source-delta NONE
→ Git diff
→ adversarial review
```

GUT 또는 Hera가 현재 프로젝트 단계에 필요하지 않거나 채택되지 않았다면 억지로 설치하지 않는다. 해당 상태는 `DEFERRED` 또는 `NOT_CONFIGURED`로 기록하고, 그 도구가 필요한 acceptance criterion만 `NOT_RUN`으로 남긴다.

## Modes

`bootstrap` → `observe` → `mutate` → `deterministic-test` → `live-qa` → `validate` → `resume` → `recover`

`deterministic-test`와 `live-qa`는 저작 Mode가 아니라 검증 stage다. persistent product change는 항상 HiGodot `mutate`로 돌아간다.

## Bootstrap Gate

```text
validate Base adapter pin and generated snapshot
→ read HIGODOT_ADOPTION_RECORD.json
→ verify exact HiGodot release or commit
→ verify project.godot and active Editor/session
→ verify client profile
→ verify LOOPBACK_ONLY
→ reject duplicate Godot persistent mutation authority
→ if GUT adopted/required: verify exact Godot-compatible GUT version and test consumption
→ if Hera adopted/required: verify exact CLI/addon pair, localhost/shared token, live-QA consumption and source-delta guard
→ identify one primary HiGodot domain
→ load minimum exact operation schema
```

`ONE_SHOT_LOCAL_EXECUTOR_BOOTSTRAP`: 사용자가 local shell + Godot editor + Codex를 직접 시작해야 하는 handoff에서는 가능한 경우 one copy/paste bootstrap block을 우선한다.

`PROJECT_DEDICATED_LOCAL_EXECUTION_ENVIRONMENT_FIRST`: local handoff는 프로젝트 전용 self-contained Godot/editor, project-scoped HiGodot profile/ports, project-scoped executor profile/CODEX_HOME, 그리고 현재 acceptance에 필요한 adopted live-QA profile을 다른 프로젝트와 섞이지 않게 먼저 확립한다. 사용자가 직전 작업 뒤 PowerShell을 닫았다고 가정하는 `ASSUME_PREVIOUS_POWERSHELL_CLOSED`가 기본이다.

필수 구성요소가 없거나 identity가 불명확하면 `CREATE_OR_REPAIR_DEDICATED_LOCAL_ENVIRONMENT_FIRST`로 분류하고 제품 authoring보다 환경 생성/복구를 먼저 수행한다. 이미 실행 중인 component는 exact project/worktree/profile identity가 일치할 때만 재사용한다.

`BOOTSTRAP_MINIMUM_PREFLIGHT_ONLY`:

```text
ASSUME_PREVIOUS_POWERSHELL_CLOSED
→ exact project/worktree identity
→ verify/create-or-repair dedicated self-contained Godot/editor
→ reuse matching editor when already running
→ otherwise start the required editor
→ verify/start-or-attach the exact project-scoped HiGodot profile/ports
→ inject the exact project-scoped executor profile/CODEX_HOME
→ if Hera or another adopted live-QA tool is required: verify its exact project-approved profile/pair and non-authoring boundary
→ run only minimum startup checks needed to avoid the wrong target
→ launch Codex in the exact project/worktree
→ obtain a fresh HiGodot project/session/version/readiness receipt inside Codex
  before persistent mutation
```

사용자에게는 Codex task prompt보다 먼저 fresh shell에서 독립 실행 가능한 one-block launcher를 제공한다. matching editor 재사용은 duplicate editor startup보다 우선한다. launcher는 orchestration일 뿐 persistent Godot edit를 수행하지 않는다. process/port/editor 존재 자체는 readiness evidence가 아니며, Codex 시작 뒤 fresh HiGodot receipt를 다시 읽는다. bootstrap 단계에서 broad Git diff, repository-wide scan, 이미 분류된 line-ending/stat/index noise를 매번 재출력하지 않는다. `reset`, `restore`, `clean`, stage, rewrite로 사용자 작업을 변경하지 않고 unrelated editor/server를 kill/restart하지 않는다.

launcher handoff 전 adversarial review에서 wrong worktree/branch, 다른 프로젝트 Godot false match, duplicate editor, 다른 프로젝트 HiGodot port/profile ownership, port collision, global executor-profile leakage, fresh-shell env loss, path quoting, process-exists-but-not-ready, unrelated process kill, destructive Git side effect를 공격한다. adopted Hera/live-QA가 필요한 경우 다른 프로젝트 profile/token/port 혼입과 persistent source mutation 가능성도 함께 검증한다. validated conflict가 있으면 launcher부터 고친 뒤 handoff한다.

다음이면 관련 stage 실행 전에 중단한다.

- HiGodot authoring이 필요한데 exact pin이 없거나 실제 설치와 불일치
- 프로젝트·Editor/session을 특정할 수 없음
- `DeepSeek` 또는 미승인 host에서 HiGodot authoring 요청
- HiGodot에서 LAN, public URL, port forwarding, remote tunnel 사용
- HiGodot과 겹치는 두 번째 persistent mutation authority 활성화
- 필요한 domain·operation을 확인하지 않고 추측 호출
- 변경 전 Git 복구 지점이 필요한데 없음
- adopted GUT의 exact version이 프로젝트 Godot compatibility와 불일치
- adopted GUT에 실제 test/CI consumption path가 없음
- adopted Hera CLI/addon exact pair가 불일치
- adopted Hera가 localhost/shared-token 경계를 충족하지 않음
- adopted Hera에 실제 live-QA consumption path 또는 `hera_source_delta_guard`가 없음

GUT/Hera가 현재 요청에 필요하지 않은 `DEFERRED`/`NOT_CONFIGURED` 상태라는 이유만으로 HiGodot authoring을 막지 않는다.

## 도구와 Context 선택

HiGodot의 전체 tool catalog와 모든 Schema를 기본 Context에 넣지 않는다.

```text
작업 의도에서 domain 식별
→ readiness 확인
→ one primary domain
→ progressive schema discovery
→ minimum exact operation
→ bounded result
→ 상태 재관찰과 검증
```

- 지원되는 경우 rollup domain과 deferred schema loading을 사용한다.
- 한 authoring 단계에는 one primary domain만 둔다.
- 실패 후 무관한 도구를 순차 추측하지 않는다.
- mutation 재시도 전 target 상태를 다시 읽는다.
- HiGodot이 반환한 session·operation·Node reference를 사용한다.
- 큰 Scene tree·log·catalog는 필요한 부분만 요약한다.
- GUT/Hera의 전체 command surface도 요청과 무관하게 선로딩하지 않는다.

## HiGodot Operation Levels

### L0_OBSERVE

Editor/session, Scene hierarchy, Node·Resource·setting·log·diagnostics·test 상태를 읽는다.

- active project와 Editor/session을 확인한다.
- 필요한 범위만 읽는다.
- mutation 준비 관찰이면 대상 경로·현재 값·dirty/import 상태를 기록한다.

### L1_REVERSIBLE_WRITE

Node 생성·rename, property 변경, script attach, 일반 Scene·Resource 저장처럼 국소적이고 Git 또는 Editor undo로 복구 가능한 변경이다.

- target과 expected result를 기록한다.
- 실행 뒤 같은 대상을 재관찰한다.
- changed files와 diff를 검토한다.
- 관련 Godot parse/import/test를 실행한다.

### L2_DESTRUCTIVE_OR_STRUCTURAL_WRITE

다음 HiGodot 기능은 금지하지 않고 사용한다.

- Node deletion
- file write, creation, modification, move, or deletion
- Scene 구조 변경
- project settings와 input map 변경
- autoload 추가·변경·제거
- script·Resource 교체와 구조적 filesystem 변경

필수 절차:

1. 사용자가 명시한 이름·대상·범위 안인지 확인한다.
2. 변경 전 Git status, 대상 Scene·Node·파일·setting을 기록한다.
3. branch, checkpoint commit 또는 exact backup으로 rollback을 확보한다.
4. 한 bounded operation group만 실행한다.
5. 전체 diff와 예상 밖 변경을 검토한다.
6. Godot import/parse와 영향 테스트를 실행한다.
7. runtime·device·human 미실행은 `NOT_RUN`으로 남긴다.

사용자가 요청한 Node deletion이나 file write는 같은 명명 범위에서 중복 질문하지 않는다. 새 삭제 대상, unrelated cleanup, project-wide 범위 확대는 사용자 승인을 다시 받는다.

### L3_HIGH_IMPACT_CHANGE

대규모 migration, 핵심 Scene·subsystem 삭제, 전역 project settings·autoload·input map 재구성, 저장소 전체 serialized asset rewrite다.

- written plan
- 적대적 사전 검토
- 명시적 사용자 승인
- isolated branch
- checkpoint commit
- full project regression
- rollback 검증

없이는 실행하지 않는다.

## GUT deterministic-test stage

GUT이 `ADOPTED_ACTIVE`이고 현재 변경에 GDScript regression evidence가 필요한 경우에만 사용한다.

```text
verify exact Godot-compatible GUT version
→ identify smallest affected GDScript test set
→ run focused tests
→ on failure return to HiGodot authoring/investigation
→ at package/release gate run affected or full regression
→ retain configured JUnit evidence when the project contract requires it
```

규칙:

- 동일 GDScript test case를 GUT과 HiGodot `McpTestSuite`의 두 canonical suite로 만들지 않는다.
- 기존 `McpTestSuite` test는 자동 삭제하지 않고 migration input으로 분류한다.
- C#/.NET, native SDK, platform sandbox, build/package, device, human test를 GUT으로 강제 대체하지 않는다.
- GUT test가 실패하면 Hera로 우회해 acceptance PASS를 만들지 않는다. 원인을 진단하고 필요한 제품 수정은 HiGodot으로 수행한 뒤 GUT을 다시 실행한다.

## Hera live-QA stage

Hera가 `ADOPTED_ACTIVE`이고 실행 가능한 game에서 runtime QA가 필요한 경우에만 사용한다.

```yaml
role_restriction: LIVE_QA_AND_OBSERVABILITY_ONLY
persistent mutation authority: forbidden
acceptance_source_delta: NONE
```

### Acceptance QA에서 허용

- Editor/instance status와 readiness
- read-only Scene·Node·Resource·Theme inspection
- game run / stop
- runtime tree와 runtime UI inspection
- input injection, semantic click, input-log
- state assertion
- output와 diagnostics
- screenshot capture와 local screenshot diff
- smoke와 `game qa diagnose`
- 위 허용 operation만 포함한 bounded batch

### Acceptance QA에서 금지

- persistent Scene/Node add/remove/set
- script create/edit
- project file/folder mutation
- Resource persistent write
- `theme set`
- main Scene 변경
- persistent filesystem mutation
- editor state를 바꾸는 `eval`
- HiGodot authoring과 동일 결과를 만드는 다른 write operation

이 금지는 Hera의 제품 기능 자체를 삭제한다는 뜻이 아니라 Base의 **동시 활성 권위 경계**다. persistent product change가 필요하면 Hera에서 쓰지 않고 HiGodot `mutate`로 돌아간다.

### Runtime mutation diagnostic exception

`game set` 또는 state-changing runtime `call`은 정상 플레이 경로를 우회할 수 있으므로 다음 경우에만 허용한다.

```yaml
mode: DIAGNOSTIC_ONLY
reason_required: true
acceptance_evidence: false
restore_or_restart_required: true
```

진단 뒤 restore/restart하고 실제 정상 입력 경로로 acceptance flow를 다시 실행한다.

### source-delta guard

Hera acceptance 단계 직전에 tracked source fingerprint 또는 Git diff snapshot을 잡고, Hera 단계 직후 같은 기준으로 다시 비교한다.

```text
pre-Hera tracked source snapshot
→ Hera live QA only
→ post-Hera tracked source snapshot
→ source-delta NONE required
```

새 tracked source delta가 있으면 `FAIL_HERA_SOURCE_DELTA`로 처리하고 어떤 operation이 만들었는지 조사한다. 그 변경을 Hera가 작성한 정상 제품 diff로 승인하지 않는다.

Screenshot diff threshold는 anti-aliasing 등 기계적 흔들림을 줄이는 값일 뿐 스타일·구도·가독성의 human approval을 대체하지 않는다.

## Client Boundary

```yaml
Codex CLI:
  HiGodot MCP: enabled

GPT Godot Authoring profile:
  HiGodot MCP: enabled

DeepSeek Analysis profile:
  HiGodot MCP: absent
  credential: absent
  Godot access: forbidden
```

프로젝트 공용 `.vscode/mcp.json` 또는 `.codex/config.toml`을 만들지 않는다. 개인 host profile을 프로젝트 정본으로 복사하거나 credential을 evidence에 기록하지 않는다.

Hera shared token 원문 역시 프로젝트 정본, prompt, log, evidence에 기록하지 않는다.

## Provider Adoption and Upgrade

`managing-game-project-operating-system`이 설치·exact pin·canary·rollback과 third-party adoption state를 소유한다.

### HiGodot

```text
release and security diff
→ isolated fixture
→ addon import/startup
→ read canary
→ destructive canary and exact restore
→ representative project canary
→ project regression
→ staged adoption
```

### GUT

```text
Godot/GUT version change
→ official compatibility matrix recheck
→ exact version pin
→ focused test
→ affected/full regression
→ staged adoption
```

### Hera

```text
CLI/addon release change
→ exact pair review
→ full Editor restart
→ localhost/shared-token status smoke
→ live-QA canary
→ source-delta NONE
→ staged adoption
```

floating latest와 자동 무검토 업데이트는 금지한다. connection 성공, tools/list, test discovery 또는 한 번의 smoke만으로 runtime·regression·production readiness를 PASS로 올리지 않는다.

## Existing Owner Routing

- 대안 조사·채택 판정: `evaluating-godot-assets-and-plugins-before-creation`
- 설치·provider pin·upgrade·rollback: `managing-game-project-operating-system`
- runtime 재현·원인 격리: `diagnosing-game-engine-runtime-failures`
- static·runtime·regression 검증: `reviewing-and-validating-project-changes`
- UI·screenshot·engine/physical input 구분: `auditing-and-refining-ui-art`
- pending task·checkpoint·resume: `maintaining-long-running-task-continuity`
- 외부 계약·Schema·catalog freshness: `auditing-canonical-reference-freshness`
- 반복 증거 기반 Skill 승격 판정: `evolving-project-discipline-skills`

현재 주 책임 owner가 작업 범위와 승인 경계를 정하고, 이 Skill은 HiGodot authoring과 채택된 GUT/Hera 검증 증거를 묶는다.

## Mode Rules

### `bootstrap`

HiGodot provider pin, addon 활성 상태, MCP host, project·Editor/session, client profile, network mode와 domain readiness를 검증한다. adopted GUT/Hera가 현재 요청에 필요한 경우 해당 exact pin/pair와 consumption/security/source-delta gate도 검증한다. local user startup이 필요한 경우 `PROJECT_DEDICATED_LOCAL_EXECUTION_ENVIRONMENT_FIRST`와 `ASSUME_PREVIOUS_POWERSHELL_CLOSED`를 적용한다. 필요한 dedicated component가 없으면 `CREATE_OR_REPAIR_DEDICATED_LOCAL_ENVIRONMENT_FIRST`로 제품 작업보다 먼저 복구하고, fresh PowerShell one-block launcher → exact matching editor reuse/start → project-scoped HiGodot → project-scoped executor profile/CODEX_HOME → adopted Hera/live-QA profile when required → exact project/worktree Codex launch → fresh HiGodot receipt 순서를 유지한다.

### `observe`

필요한 HiGodot domain의 최소 operation으로 현재 상태를 읽고 bounded output을 만든다.

### `mutate`

HiGodot에서만 L1/L2/L3를 분류하고 해당 Gate를 충족한 operation을 실행한다. stale target 또는 scope mismatch는 중단한다.

### `deterministic-test`

채택된 GUT으로 affected GDScript tests를 먼저 실행하고 필요한 package/release gate에서 regression을 실행한다. 실패는 HiGodot authoring/investigation으로 되돌린다.

### `live-qa`

채택된 Hera를 `LIVE_QA_AND_OBSERVABILITY_ONLY`로 사용한다. pre/post source-delta guard와 acceptance-operation allowlist를 지키며 persistent product write는 실행하지 않는다.

### `validate`

HiGodot 응답만 신뢰하지 않고 Git diff, Godot 재관찰, import/parse, adopted GUT tests, adopted Hera live QA, 가능한 runtime 결과를 교차 검증한다. 실행하지 않은 stage는 `NOT_RUN`으로 남긴다.

### `resume`

HiGodot이 반환한 기존 session·operation·job identity를 조회하고 initiating mutation을 중복 실행하지 않는다. GUT/Hera 검증 재개는 이전 제품 mutation을 다시 실행하지 않고 현재 Git·Editor·runtime 상태를 재관찰한 뒤 이어간다.

### `recover`

현재 Git·Scene·filesystem·Editor 상태를 다시 읽고 rollback 또는 forward recovery를 선택한다. addon 시작 실패 시 Godot recovery mode와 해당 도구의 비활성화/rollback 절차를 사용하되 두 번째 persistent mutation addon으로 우회하지 않는다.

## Output

```yaml
mode:
provider: hi-godot/godot-ai
provider_pin:
project_identity:
editor_session:
client_profile:
operation_level:
primary_domain:
operation:
requested_scope:
changed_targets:
git_checkpoint:
rollback:
import_and_parse:
gut:
  adoption_state:
  exact_version:
  focused_tests:
  regression:
hera:
  adoption_state:
  cli_addon_pair:
  role_restriction: LIVE_QA_AND_OBSERVABILITY_ONLY
  live_qa:
  source-delta:
tests:
runtime:
human:
unverified:
production_readiness: false
```

## Failure Conditions

- HiGodot 외 두 번째 Godot persistent mutation authority
- Hera unrestricted persistent editor/source writer 활성화
- Hera `DIAGNOSTIC_ONLY` runtime mutation을 acceptance evidence로 사용
- Hera acceptance 전후 source-delta 검사를 생략하거나 `NONE`이 아닌데 PASS 처리
- GUT/McpTestSuite에 같은 GDScript case를 두 canonical suite로 유지
- GUT으로 C#/.NET·native·platform test authority를 강제 대체
- adopted GUT/Hera exact pin·pair 또는 actual consumption 없음
- DeepSeek HiGodot MCP 등록 또는 credential
- non-loopback HiGodot/Hera transport
- shared token 원문을 저장소·prompt·log·evidence에 기록
- exact pin·rollback 없음
- 전체 tool/schema 선로딩
- wrong-tool wandering 또는 상태 재관찰 없는 retry
- 사용자 범위를 넘는 Node deletion·file write·project settings·autoload 변경
- L2에서 diff·rollback·import/test 누락
- L3에서 계획·명시 승인·full regression 누락
- connection·정적 파일 존재를 runtime·human·production PASS로 보고
