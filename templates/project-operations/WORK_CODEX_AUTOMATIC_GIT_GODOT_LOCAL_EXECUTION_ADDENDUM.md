# Work↔Codex 자동 Git 동기화·Godot 실행·프로젝트 한정 컴퓨터 조작 Addendum

> 이 파일은 `WORK_CODEX_MINIMUM_TRANSITION_VERTICAL_SLICE_PROFILE.md`에 대한 **명시적 사용자 위임형 companion**이다. 독립 실행 정본이나 새 Skill이 아니며, current Base의 Git 동기화·Godot 저작·GUT/Hera 검증 owner를 조합한다.

## 0. Activation and authority

```text
EXPLICIT_USER_DELEGATION_REQUIRED
OPT_IN_PROFILE_NOT_GLOBAL_DEFAULT
CURRENT_SLICE_ONLY
COMPOSE_CURRENT_OWNERS_NOT_SECOND_CANON
HOST_SYSTEM_TOOL_CONFIRMATION_PRECEDENCE
CALLABLE_TOOL_ONLY_NO_CAPABILITY_CLAIM
NO_AUTOMATIC_SCOPE_EXPANSION
```

현재 사용자가 다음을 명시적으로 위임했을 때만 활성화한다.

```text
- 작업 중 GitHub/Git fetch와 안전한 pull을 자동 수행
- 정확한 프로젝트의 Godot Editor 또는 게임을 자동 실행
- 현재 프로젝트·현재 Slice 구현과 QA에 필요한 컴퓨터 조작을 자동 수행
- routine confirmation은 반복하지 않음
```

이 위임은 상위 system·developer·host·tool confirmation, repository ruleset, 현재 Project AGENTS, OS 보안 경계 또는 계정 권한을 우회하지 않는다. 현재 세션에 실제 callable local-control capability가 없으면 조작했다고 주장하지 않고 `NOT_RUN` 또는 `BLOCKED_NO_LOCAL_ACCESS`로 둔다.

Current detailed owners:

- Git/local/remote sync: `skills/synchronizing-local-and-github-state/SKILL.md`
- Safe sync procedure: `skills/synchronizing-local-and-github-state/references/safe-sync-protocol.md`
- Godot authoring and QA authority: `docs/knowledge/godot/HIGODOT_SINGLE_AUTHORITY_AND_SAFE_OPERATION.md`
- Work↔Codex execution boundary: `docs/GPT_CODEX_WORKFLOW_POLICY.md`
- Long-running recovery: `skills/managing-project-intake-and-work-contract/references/continuous-work-execution.md`

Owner detail과 이 addendum가 충돌하면 current owner가 우선한다.

## 1. Automatic Git fetch and safe pull

```text
AUTOMATIC_GIT_FETCH_AUTHORIZED
AUTOMATIC_SAFE_PULL_AUTHORIZED
FETCH_BEFORE_START_RESUME_WRITE_PR_MERGE
PULL_FAST_FORWARD_ONLY
DIRTY_OR_DIVERGED_NO_BLIND_PULL
NO_AUTOMATIC_STASH_RESET_CLEAN_REBASE_FORCE
GITHUB_CONNECTOR_REFRESH_EQUIVALENT_WHEN_NO_LOCAL_WORKTREE
EXACT_REPOSITORY_BRANCH_UPSTREAM_IDENTITY_REQUIRED
CLEAN_TRACKING_BRANCH_REQUIRED_FOR_PULL
WRONG_WORKTREE_OR_UPSTREAM_ABORTS_PULL
NO_PR_BRANCH_TAKEOVER_FROM_PULL
POST_SYNC_EXACT_SHA_READBACK
```

사용자가 “fetch와 pull을 자동으로 하라”고 위임한 경우에도 `fetch`와 `pull`을 같은 위험도로 취급하지 않는다.

- `fetch`: 원격 ref와 object를 가져오되 현재 working tree를 자동 통합하지 않는 refresh 단계다.
- `pull`: 선택된 upstream을 현재 branch에 통합하는 변경 단계다.
- 따라서 fetch는 exact repository·remote를 확인한 뒤 자동 수행하고, pull은 아래 fast-forward-only Gate를 통과할 때만 자동 수행한다.

### 1.1 Required timing

다음 경계에서 remote facts를 자동 갱신한다.

```text
Work 시작
→ 중단 후 resume
→ first persistent write 직전
→ Work→Codex handoff 직전
→ Codex mutation 직전
→ PR 생성 직전
→ merge preflight
→ post-merge main readback
```

실제 local worktree가 있으면 Git command 경로를 사용할 수 있다. connector-only면 authenticated GitHub connector로 branch/head/PR/check/main을 fresh-read하며 local fetch/pull을 실행했다고 주장하지 않는다.

### 1.2 Preflight

명령 실행 전 다음을 실제로 확인한다.

```yaml
GIT_SYNC_PREFLIGHT:
  execution_surface: LOCAL_WORKTREE | GITHUB_CONNECTOR_ONLY | HYBRID
  repository:
  worktree:
  current_branch:
  detached_head:
  intended_remote:
  upstream_branch:
  local_head:
  remote_head_before_fetch:
  tracked_changes:
  untracked_changes:
  ahead_behind:
  divergence:
  same_goal_open_prs: []
  current_task_pr:
  result: SAFE_FETCH | SAFE_FAST_FORWARD_PULL | FETCH_ONLY | LOCAL_DEFER | BLOCKED_UNVERIFIED
```

```text
EXACT_REPOSITORY_BRANCH_UPSTREAM_IDENTITY_REQUIRED
```

프로세스 존재, 폴더명 유사성, 과거 경로 또는 Memory만으로 repository·worktree·branch·upstream을 추정하지 않는다.

### 1.3 Automatic fetch

정확한 repository와 intended remote가 확인되면 다음과 동등한 fetch를 자동 수행한다.

```bash
git fetch --prune <intended-remote>
```

- remote 이름을 무조건 `origin`으로 추정하지 않는다.
- credentials를 새로 저장하거나 계정 설정을 변경하지 않는다.
- fetch 실패 시 current owner의 recovery ladder를 사용한다.
- fetch 뒤 remote main/upstream/current-task PR head를 다시 읽는다.

### 1.4 Automatic safe pull

다음 조건이 모두 참일 때만 자동 pull한다.

```text
LOCAL_WORKTREE or verified HYBRID
AND exact intended repository/worktree
AND attached branch
AND exact intended upstream
AND tracked working tree clean
AND no protected untracked collision
AND local branch not ahead
AND no divergence
AND upstream can be integrated by fast-forward only
AND current branch is not another open PR owner branch
```

조건을 통과하면 다음과 동등한 pull을 자동 수행한다.

```bash
git pull --ff-only
```

```text
PULL_FAST_FORWARD_ONLY
CLEAN_TRACKING_BRANCH_REQUIRED_FOR_PULL
```

`already up to date`도 정상 결과다. pull 후 exact local HEAD, upstream HEAD, status와 expected worktree를 다시 읽는다.

### 1.5 Unsafe local states

다음 상태에서는 blind pull을 하지 않는다.

```text
tracked dirty
untracked collision risk
detached HEAD
wrong worktree
wrong repository
missing or unexpected upstream
local ahead
diverged history
active other-worker branch
open PR owner branch not explicitly named for mutation
submodule or nested repository ambiguity
```

```text
DIRTY_OR_DIVERGED_NO_BLIND_PULL
WRONG_WORKTREE_OR_UPSTREAM_ABORTS_PULL
NO_PR_BRANCH_TAKEOVER_FROM_PULL
NO_AUTOMATIC_STASH_RESET_CLEAN_REBASE_FORCE
```

금지되는 자동 복구:

```text
git stash
git reset --hard
git clean
git rebase
force push
branch delete
uncommitted change discard
another open PR branch mutation
```

안전 대체 경로:

```text
fetch-only + state report
→ 현재 변경 보존
→ latest completed main에서 별도 isolated worktree/branch
→ authenticated connector remote refresh
→ 해당 local task만 defer
→ independent ready work continue
```

사용자가 명시적으로 현재 dirty worktree를 소유하고 특정 reconciliation을 승인한 경우에도 current safe-sync owner를 적용하고 먼저 backup/commit/rollback evidence를 만든다.

### 1.6 Connector-only route

```text
GITHUB_CONNECTOR_REFRESH_EQUIVALENT_WHEN_NO_LOCAL_WORKTREE
```

현재 실행면이 connector-only면 다음을 자동 수행할 수 있다.

- latest main·branch·PR head fresh-read
- same-goal open/recent PR read-only reconciliation
- exact diff/check/thread/ruleset 확인
- approved branch/PR write와 safe merge
- post-merge main readback

이 경우:

```text
local_fetch: NOT_APPLICABLE_CONNECTOR_ONLY
local_pull: NOT_APPLICABLE_CONNECTOR_ONLY
local_dirty_state: NOT_RUN
```

으로 기록한다. Remote refresh를 local pull PASS로 바꾸지 않는다.

## 2. Automatic Godot launch

```text
AUTOMATIC_GODOT_LAUNCH_AUTHORIZED
EXACT_PROJECT_WINDOW_PROCESS_IDENTITY_REQUIRED
PROJECT_SCOPED_COMPUTER_CONTROL_AUTHORIZED
CALLABLE_TOOL_ONLY_NO_CAPABILITY_CLAIM
```

현재 Slice 구현·검증에 필요하고 local execution capability가 callable하면, 사용자에게 “Godot을 열까요?”라고 다시 묻지 않고 정확한 프로젝트의 Editor 또는 게임을 자동 실행할 수 있다.

### 2.1 Launch identity preflight

```yaml
GODOT_LAUNCH_PREFLIGHT:
  repository:
  project_directory:
  project_godot_path:
  exact_godot_binary:
  exact_godot_version:
  intended_mode: EDITOR | GAME | HEADLESS | IMPORT | TEST
  intended_scene_or_project:
  existing_editor_sessions: []
  existing_game_sessions: []
  adopted_authoring_authority:
  adopted_test_authority:
  adopted_live_qa_authority:
  result: READY | SESSION_CONFLICT | BLOCKED_UNVERIFIED | NOT_CALLABLE
```

- 프로젝트 폴더와 `project.godot`을 실제 readback한다.
- exact Godot binary/version 또는 Project adoption record를 확인한다.
- 다른 프로젝트의 Editor/game process를 process name만 보고 재사용하지 않는다.
- current Project의 기존 session이 안전하게 식별되면 재사용할 수 있다.
- session identity가 불명확하거나 사용자가 같은 창을 적극 사용 중이면 충돌로 처리한다.

### 2.2 Authorized launch examples

실제 binary 이름·절대 경로는 프로젝트 정본에서 결정한다. 아래는 의미 계약이다.

```bash
godot --editor --path <project-directory>
godot --path <project-directory>
```

필요할 때 current owner가 허용하는 동등한 exact-binary 경로로 다음을 수행할 수 있다.

- Editor 열기
- current project/game 실행·중지
- 명시된 scene 실행
- import/parse/headless test
- build/export smoke
- GUT runner 실행
- Hera live QA session 연결

Godot이 실행됐다는 사실만으로 올바른 project/session, import PASS, runtime PASS 또는 UX PASS를 주장하지 않는다. 실행 뒤 project path, Editor title/session, runtime identity와 log를 다시 확인한다.

## 3. Project-scoped computer control

```text
PROJECT_SCOPED_COMPUTER_CONTROL_AUTHORIZED
SEMANTIC_CONTROL_BEFORE_PIXEL_COORDINATE_GUI
UNRELATED_USER_SESSION_AND_PROCESS_PROTECTED
ACTIVE_USER_SESSION_CONFLICT_LOCAL_DEFER_OR_NEW_SESSION
```

현재 Slice를 준비·구현·검증하기 위해 필요한 local computer 조작을 자동 수행할 수 있다. 권한은 **정확한 프로젝트와 현재 작업 surface에 한정**된다.

### 3.1 Authorized surfaces

- current project repository/worktree의 terminal
- exact Project의 Godot Editor와 running game
- adopted HiGodot authoring surface
- adopted GUT test runner
- adopted Hera live QA/observability surface
- current project 파일 선택 dialog
- current Project Notion/GitHub destination
- current task의 build/export output folder
- current Slice evidence용 screenshot/log viewer

### 3.2 Authorized operations

- 정확한 창 focus·전환
- current Project 경로 열기
- current task 명령 입력·실행
- Godot project/game run·stop
- current Slice의 정상 player path 입력
- runtime state/UI inspection
- screenshot·log·diagnostic capture
- 승인된 file upload/attach/readback
- exact current Project process의 bounded restart
- build/export 결과 열기·검증

각 operation group 뒤 대상·결과·source delta를 readback한다.

### 3.3 Control priority

```text
SEMANTIC_CONTROL_BEFORE_PIXEL_COORDINATE_GUI
```

다음 우선순위를 사용한다.

```text
CLI / Git / Godot command line
→ authenticated API/connector
→ adopted MCP with exact project/session identity
→ UI accessibility/semantic element selector
→ verified image/coordinate interaction as last bounded fallback
```

해상도·창 위치·DPI를 추측한 좌표 클릭은 마지막 fallback이다. 좌표 조작 전 exact window identity와 expected element를 확인하고, 조작 뒤 상태를 다시 읽는다.

### 3.4 Protected surfaces and forbidden actions

```text
CREDENTIAL_ACCOUNT_SECURITY_OS_SETTINGS_FORBIDDEN
UNRELATED_FILE_AND_APPLICATION_ACCESS_FORBIDDEN
UNRELATED_PROCESS_TERMINATION_FORBIDDEN
SOFTWARE_INSTALL_OR_UPDATE_REQUIRES_CURRENT_ADOPTION_AUTHORITY
PUBLIC_UPLOAD_RELEASE_PURCHASE_FORBIDDEN_WITHOUT_HIGH_RISK_APPROVAL
```

자동 조작으로 다음을 하지 않는다.

- unrelated application·browser tab·personal file 열기 또는 수정
- unrelated clipboard content 수집
- 다른 프로젝트 Editor/game/terminal 조작
- 식별되지 않은 process 종료
- OS security·firewall·network·registry·account 설정 변경
- credential·token·password 원문 읽기·기록·전송
- 사용자 승인 없는 software/plugin/addon 설치·업데이트
- 구매·결제·유료 plan 활성화
- store/public release·외부 publication
- unrelated file 이동·삭제·cleanup
- 사용자 입력을 가로채거나 장시간 desktop을 독점

software/addon 설치나 업데이트가 필요하면 current Project/Base adoption authority, exact version, source, license, compatibility, rollback을 먼저 확인한다. 새 비용·권한·보안 경계가 생기면 high-risk decision으로 defer한다.

### 3.5 Active user conflict

정확한 Project session을 사용자가 직접 조작 중이거나 자동 입력이 사용자 작업과 충돌할 가능성이 있으면:

```text
ACTIVE_USER_SESSION_CONFLICT_LOCAL_DEFER_OR_NEW_SESSION
```

을 적용한다.

```text
safe separate session/worktree 가능
→ isolated session 사용

불가능
→ local interaction task만 defer
→ deterministic/headless/connector 작업 계속
→ 사용자 작업을 강제로 종료하거나 입력을 빼앗지 않음
```

## 4. Authoring and QA boundary

자동 컴퓨터 조작은 Base의 authoring owner를 변경하지 않는다.

```text
HiGodot = sole persistent Godot authoring authority when adopted
GUT = deterministic GDScript test authority when adopted
Hera = live QA and observability only
Git = final repository change truth
```

- Hera로 persistent Scene/Node/Script/Resource/file mutation을 하지 않는다.
- Hera QA 전후 tracked source delta는 `NONE`이어야 한다.
- diagnostic runtime mutation을 normal-path acceptance로 사용하지 않는다.
- screenshot diff를 design/readability/accessibility/fun/Human approval PASS로 승격하지 않는다.
- GUT/Hera가 미채택이면 current project의 evidence-equivalent machine route를 사용하며, 없으면 `NOT_RUN`이다.

## 5. Execution receipt

```yaml
LOCAL_EXECUTION_RECEIPT:
  execution_surface:
  repository:
  worktree:
  branch:
  intended_remote:
  upstream:
  pre_fetch_local_head:
  remote_head_before_fetch:
  fetch_result:
  pull_result: FAST_FORWARD | UP_TO_DATE | FETCH_ONLY | NOT_APPLICABLE_CONNECTOR_ONLY | SKIPPED_DIRTY | SKIPPED_DIVERGED | SKIPPED_DETACHED | SKIPPED_WRONG_UPSTREAM | BLOCKED
  post_sync_local_head:
  post_sync_remote_head:
  exact_godot_binary_and_version:
  project_directory:
  editor_or_game_session_identity:
  automatic_launch_operations: []
  computer_control_operations: []
  source_delta_before_after:
  unrelated_surface_touched: false
  tests_and_runtime_evidence: []
  not_run: []
  blockers: []
```

```text
POST_SYNC_EXACT_SHA_READBACK
EXACT_PROJECT_WINDOW_PROCESS_IDENTITY_REQUIRED
```

receipt가 없으면 fetch/pull/Godot launch/computer control을 완료했다고 보고하지 않는다.

## 6. Stage integration

### Work start and resume

```text
exact Project identity
→ automatic remote refresh
→ safe local pull Gate
→ exact post-sync SHA
→ Project GitHub·Notion·Base fresh-read
→ current Slice work
```

### Work→Codex handoff

```text
fetch and safe-pull preflight
→ exact baseline
→ clean or isolated Codex worktree
→ WORK_PRODUCTION_INPUT_PACKET
→ one Codex implementation window
```

### Codex implementation and QA

```text
exact repository/worktree/session
→ automatic Godot launch when callable
→ product implementation through adopted authority
→ deterministic tests
→ runtime/Hera/build QA
→ LOCAL_EXECUTION_RECEIPT
→ CONSOLIDATED_RETURN_PACKET
```

### PR and merge

```text
fetch current remote state
→ safe reconciliation
→ exact head tests/checks
→ PR
→ fetch current main and PR head before merge
→ required checks/thread/ruleset Gate
→ safe merge
→ remote/new-main readback
→ local fetch + safe fast-forward pull when applicable
→ post-merge receipt
```

## 7. Completion and evidence ceiling

현재 자동화 단계의 완료 조건에 다음을 추가한다.

```text
required Git remote refresh completed
safe local sync completed or correctly classified as not applicable/deferred
exact pre/post sync SHAs recorded
Godot launch actually executed when required and callable
exact project/session identity verified
required project-scoped computer operations read back
unrelated_surface_touched = false
credential/account/OS/security boundary preserved
machine QA complete
Human/Player evidence remains NOT_RUN until user play
```

다음은 완료가 아니다.

```text
fetch command attempted
pull command attempted
a Godot process exists
mouse click was sent
window screenshot exists
```

실제 readback과 evidence가 필요하다. 자동 로컬 조작이 callable하지 않거나 안전 preflight를 통과하지 못하면 해당 항목은 `NOT_RUN`, `LOCAL_DEFER` 또는 `BLOCKED_UNVERIFIED`이며, 가능한 독립 작업은 계속한다.
