# HiGodot 단일 실행 권위와 안전 운용 정책

## 1. 상태와 책임

```yaml
policy_state: APPROVED_FOR_IMPLEMENTATION
provider: hi-godot/godot-ai
execution_authority: SOLE_GODOT_EXECUTION_AUTHORITY
persistent_authoring_authority: SOLE_PERSISTENT_GODOT_AUTHORING_AUTHORITY
authority_count: 1
production_readiness: false
```

이 문서는 Base와 이를 채택한 Godot 프로젝트에서 MCP·EditorPlugin·CLI·테스트·live QA 공급자의 역할 경계, HiGodot 작업 위험도, 클라이언트 격리, 로컬 전송, 버전 고정, canary, project regression, rollback의 단일 공용 정본이다. `SOLE_GODOT_EXECUTION_AUTHORITY`는 **persistent Godot 저작·편집 mutation 실행 권위**를 뜻한다. 역할이 다른 검증 도구의 공존까지 금지하는 표현이 아니다.

프로젝트는 이 규칙을 복제하지 않는다. HiGodot의 실제 버전·Godot 버전·호스트·검증 증거는 `templates/project-operations/HIGODOT_ADOPTION_RECORD.json`에 기록하고, GUT·Hera 같은 별도 검증 도구의 exact pin·소비 경로·rollback은 프로젝트의 기존 third-party/addon inventory가 소유한다.

## 2. 실행 권위와 검증 역할

```yaml
HiGodot:
  provider: hi-godot/godot-ai
  role: SOLE_PERSISTENT_GODOT_AUTHORING_AUTHORITY
  authority_count: 1
  persistent_mutation: allowed_under_L0_L3

GUT:
  provider: bitwes/Gut
  role: DETERMINISTIC_GDSCRIPT_TEST_AUTHORITY_WHEN_ADOPTED
  persistent_authoring: false

Hera_Agent_Godot:
  provider: NotNull92/hera-agent-godot
  disposition: REUSE
  role_restriction: LIVE_QA_AND_OBSERVABILITY_ONLY
  persistent_source_mutation: forbidden

final_repository_change_truth:
  provider: Git
```

- `hi-godot/godot-ai`의 Godot AI addon과 MCP 서버만 persistent Scene·Node·Script·Resource·project setting·filesystem 저작 변경의 실행 권위다.
- Base custom MCP는 `ARCHIVED_REFERENCE_AFTER_POLICY_EXTRACTION`이며 실행 권위가 아니다.
- Base custom MCP Bridge와 추가 Godot mutation addon은 `STOP_AND_ARCHIVE`다.
- 한 프로젝트에 HiGodot과 기능이 겹치는 두 번째 MCP, HTTP/WebSocket Bridge, EditorPlugin 또는 CLI **persistent mutation authority**를 동시에 두지 않는다.
- GUT은 채택된 프로젝트의 반복 가능한 GDScript 테스트를 담당할 수 있으며 저작 권위가 아니다.
- Hera Agent Godot은 `REUSE`할 수 있지만 `LIVE_QA_AND_OBSERVABILITY_ONLY`로 제한한다. Hera의 persistent editor/source write 기능은 활성 Base QA 경로에서 사용하지 않는다.
- 과거 Base live-editor Adapter·Schema·Pilot·테스트는 보안·rollback·evidence 학습 자료와 역사적 실행 증거로 보존하지만, HiGodot 채택 프로젝트의 현재 persistent 실행 경로가 아니다.

### 저작 권위와 비저작 검증 도구의 경계

HiGodot의 단일 권위는 Godot 저작·편집 자동화와 persistent mutation 실행 경로에 한정된다. 동일 저작 권위를 가진 두 번째 MCP·EditorPlugin·Bridge·CLI mutation authority는 금지한다.

테스트 프레임워크, live runtime QA, 대화·서사 도구, 플랫폼 서비스, 카메라, 아이콘, 자산 제작 보조처럼 역할이 다른 도구는 `evaluating-godot-assets-and-plugins-before-creation`의 평가와 프로젝트별 채택 기록을 통과하면 공존할 수 있다. 공존 가능성은 자동 채택을 뜻하지 않는다. 실제 필요·정확한 버전·라이선스·소비 경로·검증·제거 절차가 없으면 설치하지 않는다.

## 3. Existing Solution First Gate

새 MCP·addon·CLI·framework·SDK wrapper·automation server·tool registry·Skill·Skill Mode·공용 실행 계층을 설계하거나 구현하기 전에 다음을 완료한다.

```text
current environment inventory
→ 사용자가 이미 쓰는 도구·addon·MCP·host profile 확인
→ Base와 프로젝트의 기존 구현·dependency·설정 확인
→ 같은 Goal의 open and recently merged PR 확인
→ 유지되는 외부 대안 조사
→ 기능·보안·라이선스·호환성·유지비·전환비 비교
→ REUSE / ABSORB / REFACTOR / ARCHIVE / BUILD_NEW
→ 적대적 검토
→ 사용자에게 판정·근거·미검증 보고
→ 필요한 승인 후 설계·구현
```

필수 인벤토리에는 가능한 범위에서 다음을 포함한다.

- 현재 대화와 인수인계의 확정 결정
- connected MCP와 VS Code/Codex host profile
- `project.godot`의 enabled addon
- package·dependency manifest와 lock
- 개인 설정을 노출하지 않는 범위의 MCP 등록 여부
- Base Skill Registry·프로젝트 adapter·관련 template
- 현재 branch, open and recently merged PR, 중단된 구현
- 사용자가 이미 사용 중이라고 말한 외부 도구

### 판정

```yaml
REUSE: 기존 구현을 주 실행 권위 또는 제한된 역할로 사용
ABSORB: 정책·테스트·패턴만 현행 권위에 흡수
REFACTOR: 기존 구현을 제한적으로 수정해 사용
ARCHIVE: 중복되거나 위험한 구현의 활성 권위 제거
BUILD_NEW: 대안으로 충족할 수 없는 최소 범위만 신규 제작
```

`BUILD_NEW`는 다음 중 하나를 증거로 확인하고 사용자가 비교 결과를 본 뒤 승인해야 한다.

- 필수 핵심 기능이 없음
- 차단 보안·플랫폼 결함을 설정, 격리, bounded upstream patch로 해결할 수 없음
- 라이선스가 목적과 충돌함
- 유지가 중단됐거나 현실적으로 사용할 수 없음
- 요구 Godot·OS·클라이언트·성능을 충족하지 못함

“직접 만들면 더 엄격할 수 있다”는 단독 근거로는 `BUILD_NEW`를 허용하지 않는다.

## 4. HiGodot 작업 위험도

HiGodot의 넓은 기능을 삭제하거나 숨기는 대신 요청 범위, Git 복구, diff, import, test, runtime 증거로 통제한다.

### L0_OBSERVE

Editor/session 상태, Scene hierarchy, Node property, Resource metadata, log, diagnostics, test discovery를 읽는다.

- 정확한 프로젝트와 Editor/session을 먼저 확인한다.
- 필요한 domain만 선택한다.
- 큰 tree·log는 bounded summary로 제한한다.

### L1_REVERSIBLE_WRITE

Node 생성·이름 변경, property 변경, script attach, 일반 Scene·Resource 저장처럼 국소적이고 복구 가능한 변경이다.

- 대상과 기대 결과를 기록한다.
- 실행 뒤 같은 대상 상태를 다시 읽는다.
- changed files와 diff를 검토한다.
- 관련 parse/import/test를 실행한다.

### L2_DESTRUCTIVE_OR_STRUCTURAL_WRITE

다음 기능을 **HiGodot에서 허용한다**.

- Node deletion
- file creation, modification, move, or deletion
- Scene 구조 재편
- project settings와 input map 변경
- autoload 추가·변경·제거
- Resource 교체
- script와 filesystem의 구조적 변경

필수 Gate:

1. 작업이 사용자가 이름 붙여 승인한 범위 안인지 확인한다.
2. 변경 전 Git status, 대상 Scene·Node·파일·설정을 기록한다.
3. branch, checkpoint commit 또는 정확한 backup으로 rollback 경로를 만든다.
4. 실행 뒤 전체 diff와 예상 밖 파일을 검토한다.
5. Godot import/parse와 영향 테스트를 실행한다.
6. 실제 실행하지 못한 runtime·device·human 검증은 `NOT_RUN`으로 남긴다.

사용자가 명시한 삭제·파일 쓰기는 같은 이름·대상 범위에서 다시 묻지 않는다. 작업 중 새 삭제 대상, 무관한 cleanup 또는 범위 확대가 발견되면 새 승인을 받는다.

### L3_HIGH_IMPACT_CHANGE

대규모 다중 파일 migration, 핵심 Scene·subsystem 삭제, 전역 project settings·autoload·input map 재구성, 저장소 전체 serialized asset rewrite다.

- 작성된 실행 계획
- 변경 전 적대적 검토
- 명시적 사용자 승인
- 격리 branch와 checkpoint commit
- 전체 project regression
- 검증된 rollback

을 모두 요구한다.

## 5. GUT deterministic GDScript test contract

GUT은 `ADOPTED_ACTIVE`인 프로젝트에서 반복 가능한 **GDScript** 테스트 suite의 기본 정본이 될 수 있다. 대상은 게임 규칙, 상태 전이, 저장·불러오기, 경제·전투·퍼즐, 데이터 변환, regression 가능한 UI/domain logic이다.

2026-08-07 공식 compatibility matrix를 기준으로 확인한 exact version 후보는 다음과 같다.

| Godot | GUT exact version candidate |
|---|---|
| 4.7.x | 9.7.1 |
| 4.6.x | 9.6.1 |
| 4.5.x | 9.5.0 |
| 4.3.x–4.4.x | 9.4.0 |
| 4.2.x | 9.3.0 |

이 표는 영구 상수가 아니다. Godot 또는 GUT upgrade 시 `bitwes/Gut`의 official compatibility matrix를 다시 확인하고 exact version을 재고정한다.

```yaml
gut_exact_version: required
godot_compatibility_match: required
actual_test_consumption_path: required
floating_latest: forbidden
upgrade_review: required
focused_test_after_upgrade: required
regression_after_upgrade: required
rollback_or_removal: required
```

HiGodot의 `McpTestSuite`와 GUT이 같은 GDScript test case의 두 canonical suite가 되지 않는다. GUT 채택 전에 존재하던 `McpTestSuite` 테스트는 자동 삭제하지 않고 migration input으로 보존해 이전·대체·유지 여부를 프로젝트별로 판정한다.

C#/.NET 테스트, native SDK 테스트, platform sandbox 테스트, build·packaging 테스트, 실제 device와 human validation은 GUT으로 강제 대체하지 않는다.

## 6. Hera live QA and observability contract

Hera는 실제 Editor와 running game의 상태를 읽고 플레이 경로를 실행·검증하는 데 사용한다. persistent product authoring 도구로 사용하지 않는다.

### 허용되는 acceptance QA 범위

- Editor/instance readiness와 status
- read-only Scene·Node·Resource·Theme inspection
- game run / stop
- runtime tree와 runtime UI inspection
- input injection, semantic click, input-log
- state assertion
- output와 diagnostics
- screenshot capture와 local screenshot diff
- smoke와 `game qa diagnose`
- 위 허용 operation만 포함하는 bounded batch

Screenshot diff threshold는 anti-aliasing 등 기계적 흔들림을 줄이기 위한 허용치다. 디자인 품질·구도·가독성의 human approval을 대체하지 않는다.

### 금지되는 persistent authoring 범위

- Scene/Node persistent add/remove/set
- script create/edit
- project file/folder mutation
- Resource persistent write
- `theme set`
- main Scene 변경
- persistent filesystem mutation
- editor state를 변경하는 `eval`
- HiGodot과 같은 결과를 만드는 다른 persistent authoring operation

### Runtime mutation diagnostic exception

`game set` 또는 state-changing runtime `call`은 persistent source mutation은 아니지만 정상 플레이 경로를 우회할 수 있다. 따라서 일반 acceptance evidence에는 사용하지 않는다.

```yaml
hera_runtime_mutation_exception:
  mode: DIAGNOSTIC_ONLY
  acceptance_evidence: false
  reason_required: true
  restore_or_restart_required: true
```

### Hera exact pair, transport, and source-delta gate

```yaml
hera_cli_addon_pair: EXACT_MATCH_REQUIRED
transport: LOCALHOST_ONLY
shared_token: REQUIRED_FOR_BASE_ADOPTION
secret_recording: FORBIDDEN
persistent_editor_write: FORBIDDEN
acceptance_source_delta: NONE
floating_latest: forbidden
full_editor_restart_after_upgrade: required
live_qa_canary: required
rollback_or_removal: required
```

shared token 원문은 저장소·prompt·log·evidence에 기록하지 않는다. Base 채택에서는 LAN, public exposure, port forwarding, remote tunnel을 금지한다.

Hera acceptance QA 직전에 tracked source 상태를 fingerprint 또는 Git diff 기준으로 기록하고 QA 직후 다시 비교한다. **Hera-phase delta는 `NONE`이어야 한다.** 새 tracked source delta가 생기면 Hera가 제품 변경을 만든 것으로 승인하지 않고 실패로 처리해 원인을 조사한다.

### 외부 고영양가 runtime-QA 패턴 흡수

```text
EXTERNAL_RUNTIME_QA_PATTERN_ABSORB_ONLY
HERA_REMAINS_DEFAULT_LIVE_QA_PROVIDER
```

2026-08-22 외부 구현 조사에서 `mrf/godot-stagehand`와 `satelliteoflove/godot-mcp`의 공개 repository·문서·테스트 계약을 비교했다. 두 구현은 running game 관찰·입력·상태 assertion·screenshot·성능 관찰 같은 유용한 패턴을 제공하지만, Base의 현재 HiGodot/Hera 권위 구조를 자동 교체하지 않는다.

- `mrf/godot-stagehand`: runtime-only 외부 driver와 MCP/CLI scenario runner가 같은 core를 공유하고, machine-readable report·JUnit·trace·screenshot diff를 남기는 패턴은 `ABSORB`. 다만 pre-1.0 beta이며 별도 addon/server 설치가 필요하므로 Base 기본 provider로 자동 승격하지 않는다.
- `satelliteoflove/godot-mcp`: frozen/stepped game time, structured runtime-state observation, profiler window, read/write surface 분리 패턴은 `ABSORB`. persistent editor mutation 기능이 HiGodot 단일 저작 권위와 겹치므로 두 번째 기본 mutation MCP로 설치하지 않는다.
- 현재 Base의 live QA 기본 provider는 Hera이며, 외부 도구의 설치·교체는 각 프로젝트 Existing Solution First와 별도 adoption evidence가 있을 때만 다시 판단한다.

외부 도구 이름이나 tool schema를 복제하지 않고 다음 provider-neutral packet만 흡수한다.

```yaml
RUNTIME_QA_SCENARIO_PACKET:
  scenario_id:
  build_or_commit:
  provider:
  launch_context:
  setup:
    mode: GAMEPLAY_PATH | DIAGNOSTIC_ONLY
  steps:
    - action:
      wait_until:
      assert_state:
      capture_when_material:
  time_semantics:
    mode: FRAME_OR_CLOCK_STEP_DETERMINISTIC | WALL_CLOCK_APPROX
  state_observation:
    structured_state_first: true
  visual_baseline:
    platform:
    resolution:
    renderer:
    baseline_id:
    pixel_sensitivity:
    image_diff_threshold:
  performance_probe:
    warmup:
    sample_count_or_duration:
    statistic: min | max | mean | median | p95
    threshold:
  artifacts:
    report:
    junit_or_machine_result:
    logs:
    screenshots:
    diff_images:
    trace:
  source_delta: NONE
```

#### `WALL_CLOCK_APPROX_REPLAY_IS_NOT_DETERMINISTIC_STATE_REPLAY`

입력과 millisecond timestamp를 기록해 wall-clock 기준으로 재생하는 방식은 재현 비용을 줄일 수 있지만 frame-perfect deterministic replay 증거가 아니다. deterministic 판정이 필요하면 seed·state checkpoint·clock/frame step·동일 입력에 대한 동일 결과처럼 프로젝트가 요구하는 인과 경계를 별도로 검증한다.

#### `STRUCTURED_STATE_BEFORE_SCREENSHOT`

질문이 위치·속도·HP·animation state·flag·signal·counter처럼 구조화된 상태로 판정 가능한 경우 먼저 structured state/assertion을 사용한다. screenshot은 layout·rendering·시각 hierarchy·VFX·겹침처럼 픽셀이 실제 판단 대상일 때 사용한다. 이 규칙은 screenshot을 금지하는 것이 아니라 토큰·시간·모호성을 줄이고 machine assertion을 우선하는 것이다.

#### `VISUAL_DIFF_TWO_AXIS_TOLERANCE`

visual regression은 최소한 다음 두 축을 구분한다.

```text
pixel_sensitivity = 한 픽셀이 얼마나 달라야 changed pixel로 셀 것인가
image_diff_threshold = 전체 픽셀 중 changed pixel을 얼마나 허용할 것인가
```

두 값을 하나의 “느슨함” 값으로 합치지 않는다. 플랫폼·해상도·renderer가 픽셀 결과를 materially 바꾸면 baseline identity에 그 축을 포함한다. visual diff PASS는 디자인 품질·가독성·접근성·재미·human approval PASS가 아니다.

#### `PERFORMANCE_SAMPLE_WINDOW`

성능 Gate는 한 순간의 숫자보다 warmup과 명시적 sample window를 사용한다.

```yaml
performance_probe:
  warmup:
  sample_count_or_duration:
  statistic: min | max | mean | median | p95
  threshold:
```

단일 frame/instant metric은 spike·GC·shader warmup·loading을 대표하지 않을 수 있다. 반대로 median/p95 smoke도 baseline variance·환경 통제·반복 run이 없는 한 완전한 statistical regression proof로 과장하지 않는다.

#### `DIAGNOSTIC_SETUP_IS_NOT_ACCEPTANCE_PATH`

runtime `set/call/eval` 또는 테스트 전용 GDScript로 wave·inventory·enemy state를 강제로 준비하는 것은 특정 상태를 빠르게 관찰하는 diagnostic setup에는 유용할 수 있다. 그러나 정상 게임 흐름을 우회했다면 그 실행만으로 실제 player-facing path의 acceptance를 증명하지 않는다. 최종 acceptance가 정상 진입 경로를 요구하면 동일 핵심 assertion을 실제 gameplay path에서 다시 검증한다.

외부 runner가 stable exit code·machine-readable report·JUnit·trace를 제공하는 패턴은 repository-native evidence에 흡수할 수 있다. 특정 provider를 설치하지 않아도 현재 Hera/GUT/CI 조합이 같은 evidence contract를 충족하면 Existing Solution First로 그대로 유지한다.

## 7. 표준 author → test → live-QA 흐름

```text
요구와 승인 범위
→ HiGodot L0 observe
→ HiGodot L1/L2/L3 persistent authoring
→ target 재관찰
→ Git diff
→ Godot import / parse
→ adopted GUT focused GDScript tests
→ package gate의 affected/full GUT regression
→ tracked source pre-Hera snapshot
→ adopted Hera live run / input / inspect / assert / diagnostics / screenshot
→ tracked source post-Hera snapshot
→ Hera-phase delta NONE
→ 전체 Git diff
→ adversarial review
```

GUT 또는 Hera가 현재 단계에 필요하지 않거나 채택되지 않았다면 강제 설치하지 않는다. `DEFERRED` 또는 `NOT_CONFIGURED`로 기록하며 해당 도구가 필요한 acceptance criteria만 `NOT_RUN`으로 남긴다.

## 8. HiGodot 도구 선택과 Context 제어

HiGodot 도구가 많다는 이유로 전체 schema를 기본 로드하지 않는다.

```text
작업 domain 식별
→ Editor/session readiness 확인
→ one primary domain 선택
→ minimum exact schema 또는 progressive schema discovery
→ 한 bounded operation group 실행
→ 결과 재관찰·검증
→ 이유를 기록한 경우에만 domain 전환
```

- 지원되는 경우 domain rollup과 deferred/progressive schema discovery를 사용한다.
- one primary domain 원칙을 유지한다.
- 실패 뒤 무관한 도구를 연속 추측 호출하지 않는다.
- mutation 재시도 전에 현재 상태를 다시 읽는다.
- 반환된 session, operation ID, Node reference를 사용하고 경로를 추측하지 않는다.
- 전체 Scene tree·log·tool catalog를 Context에 그대로 넣지 않고 필요한 부분만 요약한다.

## 9. 클라이언트 격리

HiGodot 서버가 같은 VS Code host 뒤의 실제 모델을 신뢰성 있게 구분한다고 가정하지 않는다.

```yaml
Godot Authoring:
  intended_client: GPT
  MCP registration: present

Codex CLI:
  intended_client: Codex
  MCP registration: present

DeepSeek Analysis:
  intended_client: DeepSeek
  MCP registration: absent
  credential: absent
  godot_read: false
  godot_write: false
```

- DeepSeek Analysis profile에는 HiGodot MCP를 등록하지 않는다.
- 프로젝트 공용 `.vscode/mcp.json`이나 `.codex/config.toml`을 활성 권위로 commit하지 않는다.
- 개인 host 설정과 credential은 프로젝트 정본·공개 저장소·evidence에 복사하지 않는다.

## 10. 로컬 전송 경계

HiGodot은 다음 경계를 유지한다.

```yaml
network_mode: LOOPBACK_ONLY
lan: LAN_FORBIDDEN
public_url: PUBLIC_URL_FORBIDDEN
port_forwarding: PORT_FORWARDING_FORBIDDEN
remote_tunnel: REMOTE_TUNNEL_FORBIDDEN
shared_or_public_pc: FORBIDDEN
```

- 로컬 개발 PC와 현재 사용자 계정에서만 실행한다.
- HiGodot의 LAN allow-list나 외부 URL 서버 모드를 사용하지 않는다.
- 공유 계정·공용 PC에서 사용하지 않는다.
- 필요하지 않을 때 Godot addon과 MCP server를 종료하거나 비활성화한다.
- 인증 강화를 위해 두 번째 Base Bridge나 fork를 즉시 만들지 않는다. upstream 개선 또는 bounded patch도 Existing Solution First Gate와 버전 검토를 통과해야 한다.

Hera는 제6절의 `LOCALHOST_ONLY`와 shared-token 경계를 추가로 따른다. GUT은 테스트 runner이며 별도 network authority를 갖지 않는다.

## 10A. 작업 소유 Godot 프로세스 정리 계약

### `TASK_LAUNCHED_GODOT_PROCESS_OWNERSHIP`

Work 또는 자동화가 Godot 검증을 시작하기 전에 exact repository/worktree/`project.godot` identity와 현재 실행 중인 process/session을 기록한다. 이번 작업이 직접 시작한 다음 항목만 task-owned 대상으로 관리한다.

- Godot Editor instance
- game window 또는 headless/runtime process
- debug/test runner와 이번 실행에서 파생된 child process
- 검증을 위해 직접 시작한 HiGodot addon/MCP server 또는 Hera/live-QA server

PID 하나나 stale session/port만 신뢰하지 않는다. 가능한 project path, launch time, parent-child relation, session/port를 함께 대조한다.

### 종료 순서

필요한 evidence를 확보했고 같은 작업에서 더 이상 Godot이 필요하지 않으면 다음 순서를 적용한다.

```text
evidence/readback capture
→ graceful stop of game/debug/test
→ no-longer-needed task-owned Editor/server stop
→ child process·project lock·session/port residual check
→ cleanup evidence 기록
```

`graceful stop`을 우선한다. 강제 종료는 정상 종료에 실패한 hung task-owned process에 한정하고 이유·대상·결과를 기록한다. 같은 bounded 검증 묶음에서 재실행이 예정돼 있으면 매 assertion 뒤 Editor를 반복 재시작하지 않고 마지막 사용 시점에 정리한다.

### 보호 대상과 실패 안전

- 사용자가 작업 전에 열어 둔 `pre-existing` Godot instance는 보존한다.
- 다른 프로젝트·repository·worktree의 Editor/game/server를 종료하지 않는다.
- 다른 승인 workstream이나 사용자가 직접 소유한 debug session을 종료하지 않는다.
- 이번 작업이 시작했다는 증거가 없는 process를 종료하지 않는다.
- `process-name 전체 종료 금지`: `godot*` 같은 이름 기반 broad kill을 사용하지 않는다.
- port-wide destructive cleanup을 사용하지 않는다.

소유권을 안전하게 구분할 수 없으면 broad kill 대신 `PROCESS_OWNERSHIP_UNVERIFIED`로 남기고 process·project lock·session/port 잔여와 수동 확인 필요성을 보고한다. 이 상태에서 residual check를 PASS로 과장하지 않는다.

## 11. 도입 기록

프로젝트별 `HIGODOT_ADOPTION_RECORD.json`은 다음을 소유한다.

- exact release or commit
- Godot version
- Codex·GPT host 등록 상태와 DeepSeek 금지
- network mode
- enabled·unverified domain
- 설치·connection·runtime·regression 상태
- verification evidence
- rollback release or commit
- production readiness

GUT·Hera는 기존 project third-party/addon inventory에서 다음 공통 필드를 기록한다.

```yaml
addon_or_tool_name:
role:
exact_version_or_pair:
source:
license:
godot_compatibility:
adoption_state:
consumption_path:
owner_boundary:
validation:
rollback_or_removal:
unverified:
```

`NOT_CONFIGURED`, `NOT_RUN`, `PARTIAL`, `PASS`, `FAIL`을 구분한다. 연결 성공, tools/list, test discovery 또는 한 번의 live QA 성공은 production readiness 증거가 아니다. 설치됐지만 소비 경로가 없으면 `INSTALLED_UNUSED`로 판정해 제거하거나 필요 시점까지 `DEFERRED`로 되돌린다.

## 12. 업데이트와 Rollback

자동 무검토 업데이트는 금지한다.

### HiGodot

```text
새 release 확인
→ release note·dependency·schema·transport·security diff
→ 호환성·적대적 검토
→ 격리 fixture 설치
→ Godot import와 plugin startup smoke
→ read canary
→ destructive canary와 exact restore
→ 대표 프로젝트 canary
→ project regression
→ 프로젝트별 단계적 적용
→ 이전 package·pin·rollback 증거 유지
```

- exact release or commit을 고정한다.
- 새 버전의 destructive canary는 삭제·파일 쓰기·project settings 변경 후 원복까지 검증한다.
- 최소 한 대표 프로젝트의 project regression 전에는 전체 프로젝트에 확산하지 않는다.
- rollback package와 이전 pin을 보존한다.

### GUT

Godot engine 또는 GUT 버전이 바뀌면 official compatibility matrix를 다시 확인하고, focused test와 regression을 실행한 뒤 새 exact version을 채택한다. 제거·rollback 경로를 유지한다.

### Hera

CLI와 addon을 같은 exact version pair로 갱신하고 Godot Editor를 완전히 재시작한다. status smoke, live-QA canary, source-delta `NONE`을 확인한 뒤 채택한다. 이전 pair 또는 제거 절차를 rollback으로 유지한다.

Windows·Android·실제 Editor UI·사람 사용성처럼 실행하지 않은 환경은 `NOT_RUN`이다.

## 13. 기존 자체 구현 처리

```yaml
Base_PR_198:
  disposition: SUPERSEDED_BY_HIGODOT_POLICY_AFTER_EXTRACTION
  merge: false

Base_PR_201:
  disposition: ARCHIVED_REFERENCE_AFTER_POLICY_EXTRACTION
  merge: false

Base_PR_202:
  disposition: STOP_AND_ARCHIVE
  merge: false
```

이 정책이 검토되고 필요한 교훈이 보존되기 전에는 PR을 삭제하지 않는다. PR을 닫거나 branch를 삭제하거나 merge하는 행위는 별도 사용자 결정이다.

## 14. 실패 조건

- 현재 사용 도구·addon·MCP·CLI·관련 PR을 확인하지 않고 신규 구현 시작
- disposition·비교 근거·사용자 승인 없이 `BUILD_NEW`
- HiGodot과 겹치는 두 번째 활성 persistent mutation authority
- Hera를 unrestricted editor/source writer로 사용
- Hera `DIAGNOSTIC_ONLY` runtime mutation 결과를 acceptance evidence로 사용
- Hera acceptance QA 전후 tracked source delta 검사를 생략하거나 delta가 있는데 통과 처리
- Hera shared token 원문을 저장소·prompt·log·evidence에 기록
- GUT과 HiGodot `McpTestSuite`에 같은 GDScript case를 두 canonical test로 유지
- GUT으로 C#/.NET·native·platform test authority를 강제 대체
- Godot/GUT 호환성 또는 Hera CLI/addon exact pair를 확인하지 않고 floating latest 사용
- 사용자가 허용한 HiGodot Node 삭제·파일 쓰기·project settings 기능을 일괄 금지
- L2/L3 작업에서 rollback·diff·import·test 누락
- DeepSeek profile에 HiGodot 등록 또는 credential 제공
- LAN·public URL·port forwarding·remote tunnel 사용
- connection 성공을 runtime·regression·production readiness로 승격
- 과거 Base Adapter·MCP 파일 존재를 현재 실행 권위로 해석
- HiGodot 단일 권위를 비저작 검증 도구 전면 금지로 오해
- 역할이 다른 도구라는 이유만으로 평가·소비 경로·rollback 없이 일괄 설치
- task ownership 확인 없이 Godot process-name 전체 종료 또는 port-wide destructive cleanup 실행
- pre-existing 또는 다른 프로젝트 instance를 작업용 process로 오인해 종료
- Godot을 실행한 뒤 task-owned process 종료와 residual check 증거 없이 cleanup PASS 주장

## 15. 실행 보고

```yaml
provider: hi-godot/godot-ai
provider_pin:
project_and_editor_identity:
client_profile:
operation_level: L0/L1/L2/L3
primary_domain:
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
  live_qa:
  source_delta:
tests:
runtime:
human:
godot_process_cleanup:
  task_owned_processes_started: []
  task_owned_processes_stopped: []
  preexisting_or_unrelated_preserved: []
  residual_check: PASS | PARTIAL | NOT_RUN | NOT_APPLICABLE
  residual_risk: []
unverified:
production_readiness: false
```