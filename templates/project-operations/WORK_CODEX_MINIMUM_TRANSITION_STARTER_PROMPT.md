# `[프로젝트명]` Work↔Codex 최소 전환 자동 실행 시작 지시문

> `[프로젝트명]`만 실제 이름으로 바꿔 Work 채팅에 붙여넣는다.

`[프로젝트명]` 작업을 재개해. 이 메시지는 **현재 승인된 Playable Slice**에 대한 routine 권장안·Git 동기화·프로젝트 범위 로컬 컴퓨터 조작의 명시적 위임이다.

## 0. Current Base와 Project 정본 복원

```text
USE_CURRENT_BASE_PROFILE_NOT_INLINE_DUPLICATE
EXPLICIT_USER_DELEGATION_REQUIRED
CURRENT_BASE_OWNER_WINS_ON_DRIFT
CURRENT_SLICE_ONLY
NO_AUTOMATIC_SCOPE_EXPANSION
HOST_SYSTEM_TOOL_CONFIRMATION_PRECEDENCE
```

과거 채팅·Memory를 current truth로 사용하지 말고 다음을 fresh-read해.

```text
Base latest completed main / AGENTS.md / START_HERE.md / current SKILL_REGISTRY
→ templates/project-operations/CHATGPT_WORK_PROJECT_EXECUTION_INSTRUCTION_v4.9.md
→ templates/project-operations/CHATGPT_WORK_PROJECT_EXECUTION_INSTRUCTION_v4.9_COMPATIBILITY_APPENDIX.md
→ templates/project-operations/WORK_CODEX_MINIMUM_TRANSITION_VERTICAL_SLICE_PROFILE.md
→ exact Project GitHub latest completed main / AGENTS / decisions / handoff / open PR
→ exact Project Notion Home / active Domain / Visual / Asset / Flow / Production
→ actual code·data·Scene·Resource·asset·test·runtime evidence
```

이 시작문은 상세 계약의 두 번째 정본이 아니다. 위 current Base profile과 분야별 current owner가 drift 시 우선한다.

## 1. 목표와 승인 경계

```text
Work: 기획·검수·이미지·사운드·UI·Data·VFX·권리·QA 입력 완성
→ WORK_PRODUCTION_INPUT_PACKET readback
→ Codex 단일 구현 window
→ deterministic test + runtime/build + 화면 QA
→ Work final evidence/canon/merge review
→ 다운로드 가능한 실행 빌드
→ READY_FOR_USER_VERTICAL_SLICE_VALIDATION
```

```text
DELEGATED_RECOMMENDED_DEFAULT_APPROVAL
NO_ROUTINE_APPROVAL_STOPS
HIGH_RISK_DECISIONS_DEFER_AND_BUNDLE
```

현재 Slice 안의 reversible 기술 선택, 안전한 기본값, bounded 이미지·사운드 제작/선정, bug fix, test 보완, small canon sync, current-task Git/PR/merge는 다시 묻지 말고 진행해.

다음만 해당 task를 보류하고 독립 작업을 계속한 뒤 마지막에 한 번에 물어봐.

```text
IRREVERSIBLE_DATA_LOSS
ACCOUNT_OR_SECURITY_PERMISSION_EXPANSION
NEW_PAID_COST
LEGAL_OR_RIGHTS_UNCERTAINTY
PUBLIC_RELEASE_OR_EXTERNAL_PUBLICATION
PROJECT_CORE_IDENTITY_REPLACEMENT
BROAD_ENGINE_OR_SAVE_BREAKING_MIGRATION
FORCE_DIRECT_MAIN_ADMIN_BYPASS
```

## 2. Notion 감사

```text
ONE_TIME_ACTIVE_PROJECT_NOTION_AUDIT_IF_NOT_EVIDENCED
TARGETED_NOTION_AUDIT_AFTER_BASELINE
NON_SLICE_NOTION_DEBT_DOES_NOT_BLOCK_CURRENT_SLICE
```

검증된 최초 감사 evidence가 없으면 Project Home과 활성 Domain·Visual Bible·Asset Catalog·Flow·Production·Decision을 한 번 감사하고 `CURRENT_VALID / UNIQUE_PRESERVE / MISSING / STALE / DUPLICATE / CONFLICT / ORPHAN / SUPERSEDED / UNKNOWN_UNVERIFIED`로 분류해. 기존 IA를 무조건 재구축하지 말고 검증된 결함만 bounded correction하고 모든 write는 exact destination readback까지 확인해.

최초 감사가 유효하면 이후에는 current Slice owner·consumer만 targeted audit해. 현재 Slice와 무관한 Notion 부채는 기록하되 자동화 phase를 막지 마.

## 3. GitHub 자동 fetch·안전 pull·push

```text
AUTO_GIT_FETCH_AND_SAFE_PULL
DISCOVER_GIT_REMOTE_UPSTREAM_DEFAULT_BRANCH
EXACT_REPOSITORY_BRANCH_UPSTREAM_IDENTITY_REQUIRED
DIRTY_OR_DIVERGED_STATE_RECONCILE_NO_FORCE
AUTO_PUSH_CURRENT_TASK_BRANCH_AFTER_VERIFICATION
REMOTE_HEAD_READBACK_AFTER_PUSH
OPEN_PR_READ_ONLY_BY_DEFAULT
CURRENT_TASK_BRANCH_IDENTITY_REQUIRED
NO_DIRECT_MAIN_PUSH
NO_FORCE_PUSH
GITHUB_CONNECTOR_REFRESH_EQUIVALENT_WHEN_NO_LOCAL_WORKTREE
POST_MERGE_MAIN_READBACK_AND_SAFE_LOCAL_MAIN_REFRESH
```

local Git이 callable하면 작업 진입, resume, first write 전, Work→Codex 인계 전, Codex mutation 전, PR 생성·merge 전, post-merge에 자동 동기화해. remote 이름을 `origin`, 기본 branch를 `main`이라고 추측하지 말고 실제 repository metadata와 branch tracking 상태에서 `<intended-remote>`, `<upstream-branch>`, `<default-branch>`를 먼저 발견·검증해. `@{upstream}` 결과는 이미 `<remote>/<branch>` 형태일 수 있으므로 remote 이름을 다시 붙이지 말고 그대로 readback해.

```text
git status --short --branch
git remote -v
git branch --show-current
git rev-parse --abbrev-ref --symbolic-full-name @{upstream}
git symbolic-ref --short refs/remotes/<intended-remote>/HEAD
git fetch --prune <intended-remote>
git rev-parse HEAD
git rev-parse @{upstream}
```

`git symbolic-ref --short refs/remotes/<intended-remote>/HEAD` 결과에서 `<default-branch>`를 확인하고, 현재 branch의 configured remote/merge ref에서 `<intended-remote>`와 `<upstream-branch>`를 정규화해. fetch는 exact repository와 intended remote를 확인한 뒤 자동 수행해. clean·tracking·non-diverged 상태이며 현재 branch가 해당 upstream으로 fast-forward만 가능할 때만 다음과 동등한 pull을 자동 수행해.

```text
git pull --ff-only <intended-remote> <upstream-branch>
```

dirty·ahead·diverged·detached HEAD·wrong worktree·wrong upstream·다른 open PR 소유 branch이면 blind pull/stash/rebase/reset/clean/force를 금지해. exact SHA·diff·open PR·semantic overlap을 비교하고 현재 변경을 보존한 채 latest completed default branch에서 별도 branch/worktree로 reconcile하거나 해당 local task만 defer해.

검증된 current-task commit은 exact current-task feature branch에 자동 push하고, push 뒤 remote branch HEAD가 expected local/connector HEAD와 같은지 반드시 readback해. `NO_FORCE_PUSH`와 `NO_DIRECT_MAIN_PUSH`를 유지해. 다른 open/draft/ready PR은 사용자가 PR 번호와 허용 동작을 명시하지 않는 한 read-only로 유지해.

local worktree·CLI·auth가 없으면 `GITHUB_CONNECTOR_REFRESH_EQUIVALENT_WHEN_NO_LOCAL_WORKTREE`를 적용해 authenticated GitHub connector로 remote main/default branch·current-task branch·PR·check를 fresh-read하고 지원되는 push/PR/merge를 수행해. 이 경우 local fetch/pull·dirty-state를 실행했다고 주장하지 말고 `NOT_APPLICABLE_CONNECTOR_ONLY` 또는 `NOT_RUN`으로 기록해.

merge 뒤 remote new-main/default branch SHA를 readback하고, local default branch가 정확히 식별됐으며 clean·tracking·fast-forward 가능한 경우에만 다음과 동등하게 갱신해.

```text
git switch <default-branch>
git pull --ff-only <intended-remote> <default-branch>
```

모든 sync 경계에서 pre/post local·remote exact SHA, branch, upstream, fetch/pull/push 결과를 기록해.

## 4. Godot·컴퓨터·브라우저 자동 조작

```text
LOCAL_COMPUTER_CONTROL_DELEGATED
AUTO_LAUNCH_GODOT_WHEN_CALLABLE
EXACT_PROJECT_EDITOR_SESSION_REQUIRED
PROJECT_SCOPED_OS_AUTOMATION_ONLY
PROJECT_PROCESS_ONLY_CLOSE
PROJECT_SCOPED_BROWSER_AND_FILE_DIALOG_AUTOMATION_ALLOWED
TOOL_NOT_CALLABLE_DO_NOT_CLAIM
STABLE_ENGINE_BASELINE_NO_AUTO_UPDATE
NO_NEW_TOOL_INSTALL_OR_UPDATE_WITHOUT_CURRENT_OWNER_GATE
```

현재 host가 실제 computer/local-shell/HiGodot/Hera capability를 제공하면 별도 routine 승인 없이 다음을 수행해도 돼.

- exact repository/worktree로 이동해 terminal/PowerShell 실행
- 프로젝트에 고정된 Godot binary와 exact `project.godot`으로 Editor 실행
- 올바른 Scene import/parse/run/stop, 게임 입력 주입, runtime tree/UI/log 확인
- screenshot·screen diff·evidence 저장, 승인 asset import, internal/debug export
- exact Project GitHub/Notion의 이미 인증된 페이지 탐색·파일 업로드·file dialog 조작
- 현재 프로젝트가 직접 띄운 Godot/game/test process만 정상 종료

```text
NO_UNRELATED_APPLICATION_OR_FILE_ACCESS
NO_CREDENTIAL_OR_SECRET_CAPTURE
NO_OS_SECURITY_SETTINGS_OR_DESTRUCTIVE_SYSTEM_CHANGE
NO_REMOTE_TUNNEL_OR_PUBLIC_PORT
NO_NEW_LOGIN_PERMISSION_OR_CONSENT_GRANT
```

다른 프로젝트 session/process를 추측 재사용하지 마. 새 로그인·2FA·권한 동의·보안 설정 변경을 자동 처리하지 마. exact project/session 또는 tool capability를 확인할 수 없으면 해당 조작만 `BLOCKED_UNVERIFIED`로 두고 독립 작업을 계속해. 새 엔진·MCP·addon·CLI·software 설치/업데이트는 Existing Solution First·호환성·canary·rollback Gate 없이는 수행하지 마.

## 5. Work 준비와 Codex 단일 구현

Codex 전환 전 current profile의 `WORK_PRODUCTION_INPUT_PACKET`을 닫아.

- player promise·행동·선택·결과·실패 학습·보상
- approved scope / explicit non-scope / protected scope
- rules·UI/UX Flow·Data/State
- actual consumer가 있는 Visual·Audio·VFX와 승인 binary 또는 procedural spec
- provenance·license·rights·hash·durable locator
- deterministic test·runtime QA·build/export acceptance·rollback·evidence ceiling
- GitHub structured canon·Notion human canon write/readback

신규 제작 전에 current project → approved asset/reference → Base reuse → 직접 관련된 검증 사례 → 공식/현업 benchmark 순으로 확인하고 `ADOPT / ADAPT / REJECT`해. 중요 결정은 최소 3개 실질안을 비교해.

```text
CODEX_EXECUTOR_NOT_CALLABLE_DO_NOT_CLAIM_IMPLEMENTED
DEFER_PRODUCT_IMPLEMENTATION_CONTINUE_WORK_READY_TASKS
DURABLE_CODEX_HANDOFF_REQUIRED
```

Codex/product executor가 callable하지 않으면 구현했다고 주장하지 마. durable handoff를 정본에 남기고 product implementation만 `DEFERRED_EXTERNAL_EXECUTOR`로 두며 Work-owned ready task는 계속해. callable하면 Project GitHub·Notion을 fresh-read하고 한 implementation window에서 actual code·Scene·Resource·runtime wiring·test·build를 완료한 뒤 작은 finding을 한 건씩 되돌리지 말고 `CONSOLIDATED_RETURN_PACKET`으로 반환해.

## 6. Machine QA와 다운로드 빌드

```text
MACHINE_QA_FIRST
HUMAN_QA_DEFERRED_BY_CURRENT_USER
HUMAN_USABILITY_EVIDENCE: NOT_RUN
PLAYER_EXPERIENCE_EVIDENCE: NOT_RUN
```

프로젝트가 채택한 current test/runtime authority를 사용해. GUT은 deterministic test, Hera는 live QA/observability only이며 persistent authoring은 금지해. 미채택 도구를 자동 설치하지 말고 evidence-equivalent route를 사용해. 필수 route가 없으면 `NOT_RUN`이며 automated readiness를 막아. GUT/runtime/screenshot PASS를 Human 이해·재미·기억 PASS로 승격하지 마.

```text
USER_DOWNLOADABLE_BUILD_ARTIFACT_REQUIRED
RUNNABLE_BY_USER_ONE_CLICK_PROJECT_PLAY_GATE
BUILD_SHA256_AND_DURABLE_LOCATOR_REQUIRED
CLEAN_EXTRACT_AND_LAUNCH_SMOKE_REQUIRED
NO_PUBLIC_RELEASE_WITHOUT_HIGH_RISK_APPROVAL
ARTIFACT_SECRET_AND_DEBUG_RESIDUE_SCAN_REQUIRED
```

목표 플랫폼·export preset·template·toolchain이 callable하면 internal/debug 빌드를 자동 export하고 executable+data를 portable ZIP 또는 플랫폼 표준 패키지로 묶어. exact commit/build, SHA-256, clean directory extract/launch smoke, 대표 Scene·success marker, runtime asset, secret/credential/`.git`/불필요한 absolute path/temp evidence/의도하지 않은 debug log를 검사해.

전달은 `현재 채팅 실제 첨부 → GitHub Actions artifact → 승인된 private/internal artifact route` 순으로 해. local path만 있으면 다운로드 제공 완료로 주장하지 말고 `BLOCKED_NO_DURABLE_ARTIFACT_ROUTE`로 남겨. GitHub Release·store·공개 배포는 high-risk 결정 전에는 하지 마.

## 7. 복구·교훈·완료

```text
STALL_SIGNAL_ROUTE_SWITCH
BOUNDED_RETRY_THEN_FALLBACK
EVIDENCE_EQUIVALENT_FALLBACK_ONLY
DEFER_BLOCKED_TASK_CONTINUE_INDEPENDENT_READY_WORK
SCOPE_BOUNDED_REQUIRED_WORK_ZERO
AUTOMATION_PHASE_REMAINING_WORK_ZERO
INCIDENT_SOLUTION_LESSON_LOOP
BASE_PROMOTION_DISPOSITION_REQUIRED
```

동일 root cause를 무한 재시도하지 말고 readback → root-cause → bounded retry → authorized fallback A/B → local defer → independent work 순으로 진행해. material failure는 environment/version/SHA/tool, root cause, attempts, final solution, evidence, recurrence guard, rollback을 Project owner에 기록하고 project-neutral 반복 원리만 Base case/BCP 후보로 판정해. 새 공용 학습이 없으면 `NO_BASE_PROMOTION`으로 닫아. 관련 사례: `docs/knowledge/cases/WORK_CODEX_STARTER_LOCAL_EXECUTION_SYNC_CASE.md`.

현재 approved Slice의 machine-executable required work를 0까지 진행해. 0이면 implementation/canon/consumer/test/runtime/build/PR/merge/readback/evidence를 재검사하고 valid finding을 다시 열어 교정해. 최소 5회 full-scope 적대적 검토 후 blocking finding 0에서만 clean exit해.

Work는 Codex 보고가 아니라 actual diff·tests·runtime/screenshot/build evidence를 검수해. current-task PR은 exact HEAD, required checks, unresolved thread 0, conflict 0, protected drift 0에서만 squash merge하고 new-main·Notion을 readback해.

```text
AUTOMATED_VERTICAL_SLICE_READY
READY_FOR_USER_VERTICAL_SLICE_VALIDATION
HUMAN_QA: DEFERRED_BY_USER
DO_NOT_AUTO_ADVANCE_TO_NEXT_SLICE_BEFORE_USER_VALIDATION
```

사용자가 실제 빌드를 플레이하기 전에는 다음 Slice로 자동 진입하지 마. 마지막 보고에 변경 전→후→기대효과, 사용 Skill, reuse/benchmark/대안, Work 제작물, Codex 구현, Git SHA/PR/merge, GUT/Hera/runtime/build evidence, 다운로드 링크, NOT_RUN, high-risk deferred, 남은 machine work와 사용자 실행 방법을 포함해.
