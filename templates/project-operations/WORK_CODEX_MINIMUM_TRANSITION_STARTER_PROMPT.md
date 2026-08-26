# `[프로젝트명]` Work↔Codex 최소 전환 자동 실행 시작 지시문

> 복사 후 첫 줄의 `[프로젝트명]`만 실제 프로젝트명으로 바꾼다.

`[프로젝트명]` 작업을 재개해. 이 메시지는 현재 승인된 Playable Slice에 대한 실행·routine 권장안·프로젝트 범위 로컬 조작 위임이다.

## 0. Current authority를 먼저 복원

```text
USE_CURRENT_BASE_PROFILE_NOT_INLINE_DUPLICATE
EXPLICIT_USER_DELEGATION_REQUIRED
CURRENT_BASE_OWNER_WINS_ON_DRIFT
CURRENT_SLICE_ONLY
NO_AUTOMATIC_SCOPE_EXPANSION
HOST_SYSTEM_TOOL_CONFIRMATION_PRECEDENCE
```

과거 채팅·Memory를 current truth로 사용하지 말고 다음을 fresh-read한다.

```text
Base latest completed main
→ Base AGENTS.md / START_HERE.md / current SKILL_REGISTRY
→ templates/project-operations/CHATGPT_WORK_PROJECT_EXECUTION_INSTRUCTION_v4.9.md
→ templates/project-operations/CHATGPT_WORK_PROJECT_EXECUTION_INSTRUCTION_v4.9_COMPATIBILITY_APPENDIX.md
→ templates/project-operations/WORK_CODEX_MINIMUM_TRANSITION_VERTICAL_SLICE_PROFILE.md
→ exact Project GitHub latest completed main / AGENTS / current decisions / handoff / open PR
→ exact Project Notion Home / relevant Domain / Visual / Asset / Flow / Production
→ actual code·data·Scene·Resource·asset·test·runtime evidence
```

이 메시지에 세부 Base 계약을 복제해 두 번째 정본으로 만들지 않는다. 위 current profile과 current owner가 이 메시지의 축약 표현보다 우선한다.

## 1. 목표 흐름

```text
Work에서 현재 Slice 기획·검수·이미지·사운드·UI·Data·VFX·권리·QA 입력을 모두 준비
→ Work production-input readback
→ Codex 단일 제품 구현 window
→ deterministic test + runtime/build + 화면 QA
→ Work final evidence/canon/merge review
→ 다운로드 가능한 실행 빌드 제공
→ READY_FOR_USER_VERTICAL_SLICE_VALIDATION
```

작은 누락마다 Work↔Codex를 반복하지 않는다. Work 입력을 먼저 묶어 닫고 Codex는 가능한 독립 구현·테스트를 계속한 뒤 `CONSOLIDATED_RETURN_PACKET`으로 한 번에 반환한다.

## 2. 승인과 중단 경계

```text
DELEGATED_RECOMMENDED_DEFAULT_APPROVAL
NO_ROUTINE_APPROVAL_STOPS
HIGH_RISK_DECISIONS_DEFER_AND_BUNDLE
```

현재 Slice 안의 reversible 기술 선택, 안전한 권장 기본값, bounded 이미지·사운드 제작/선정, bug fix, test 보완, small canon sync, current-task Git/PR/merge는 다시 묻지 않고 진행한다.

다음만 실행하지 말고 해당 task만 보류한 뒤 독립 작업을 계속하고 마지막에 한 번에 묻는다.

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

## 3. Notion 최초 감사와 이후 범위 감사

```text
ONE_TIME_ACTIVE_PROJECT_NOTION_AUDIT_IF_NOT_EVIDENCED
TARGETED_NOTION_AUDIT_AFTER_BASELINE
```

현재 정본에 검증된 최초 감사 evidence가 없으면 한 번만 Project Home과 활성 Domain·Visual Bible·Asset Catalog·Flow·Production·Decision을 감사한다.

```text
CURRENT_VALID | UNIQUE_PRESERVE | MISSING | STALE | DUPLICATE | CONFLICT | ORPHAN | SUPERSEDED | UNKNOWN_UNVERIFIED
```

기존 IA를 무조건 재구축하지 말고 검증된 결함만 bounded correction한다. 모든 write는 정확한 destination readback까지 확인한다. 최초 감사가 이미 유효하면 매 작업마다 전수 재감사하지 않고 current Slice owner·consumer만 targeted audit한다.

## 4. GitHub 자동 fetch·안전 pull·push

```text
AUTO_GIT_FETCH_AND_SAFE_PULL
DIRTY_OR_DIVERGED_STATE_RECONCILE_NO_FORCE
AUTO_PUSH_CURRENT_TASK_BRANCH_AFTER_VERIFICATION
OPEN_PR_READ_ONLY_BY_DEFAULT
CURRENT_TASK_BRANCH_IDENTITY_REQUIRED
NO_DIRECT_MAIN_PUSH
POST_MERGE_MAIN_READBACK_AND_SAFE_LOCAL_MAIN_REFRESH
```

로컬 Git surface가 실제로 callable하면 작업 진입, first persistent write 전, Codex 인계 전, PR 전, merge 전, post-merge 시점에 remote/local 상태를 자동 동기화한다.

```text
git status --short --branch
git remote -v
git fetch --prune origin
```

현재 branch가 clean하고 upstream과 divergence가 없으며 fast-forward만으로 갱신될 때만 다음을 실행한다.

```text
git pull --ff-only
```

dirty·ahead/behind 동시 존재·diverged·충돌·다른 worktree 소유가 확인되면 blind pull, 자동 rebase, reset, clean, force를 하지 않는다. 현재 변경을 보존하고 exact SHA·diff·open PR·semantic overlap을 비교해 latest completed main 기준의 안전한 별도 branch/reconciliation 경로를 사용한다.

현재 task가 소유한 feature branch identity를 먼저 확인한다. 검증된 current-task commit은 그 branch에만 자동 push하고 exact remote HEAD를 readback한다. `main`에는 직접 push하지 않는다. 병합 뒤에는 remote new-main SHA를 먼저 읽고, local `main`이 clean하고 fast-forward 가능한 경우에만 안전하게 refresh한다. local auth/CLI가 없고 연결된 GitHub connector가 같은 capability를 제공하면 connector fallback을 사용한다. 다른 open/draft/ready PR은 사용자에게 PR 번호와 허용 동작이 명시되지 않는 한 read-only다.

## 5. Godot 자동 실행과 프로젝트 범위 컴퓨터 조작

```text
LOCAL_COMPUTER_CONTROL_DELEGATED
AUTO_LAUNCH_GODOT_WHEN_CALLABLE
EXACT_PROJECT_EDITOR_SESSION_REQUIRED
PROJECT_SCOPED_OS_AUTOMATION_ONLY
PROJECT_PROCESS_ONLY_CLOSE
TOOL_NOT_CALLABLE_DO_NOT_CLAIM
STABLE_ENGINE_BASELINE_NO_AUTO_UPDATE
NO_NEW_TOOL_INSTALL_OR_UPDATE_WITHOUT_CURRENT_OWNER_GATE
```

현재 host가 실제 computer/local-shell/HiGodot/Hera capability를 제공하면 별도 routine 승인 없이 다음 프로젝트 범위 행동을 수행해도 된다.

- exact repository/worktree로 이동하고 terminal/PowerShell 명령 실행
- 프로젝트에 고정된 Godot binary와 exact `project.godot`을 찾아 Editor 실행
- 올바른 Scene을 열고 import/parse/run/stop 수행
- 프로젝트 게임 창에 keyboard/mouse/gamepad 입력 주입
- runtime tree·state·UI·log·diagnostics 확인
- screenshot·screen diff·evidence 파일 저장
- 승인된 프로젝트 파일을 import하고 export preset으로 내부 검증 빌드 생성
- 현재 프로젝트가 직접 띄운 Godot/game/test process만 정상 종료

다음 경계는 유지한다.

```text
NO_UNRELATED_APPLICATION_OR_FILE_ACCESS
NO_CREDENTIAL_OR_SECRET_CAPTURE
NO_OS_SECURITY_SETTINGS_OR_DESTRUCTIVE_SYSTEM_CHANGE
NO_REMOTE_TUNNEL_OR_PUBLIC_PORT
```

다른 프로젝트 Editor/session/process를 추측 재사용하지 않는다. exact project/session identity를 확인할 수 없으면 해당 로컬 조작만 `BLOCKED_UNVERIFIED`로 두고 독립 작업을 계속한다. 도구가 노출되지 않았으면 컴퓨터를 조작하거나 Godot을 실행했다고 주장하지 않는다. 설치된 stable engine baseline을 새 버전 존재만으로 바꾸지 않으며, 새 MCP·addon·CLI·소프트웨어 설치 또는 업데이트는 current Base/Project owner의 Existing Solution First·호환성·rollback Gate 없이는 자동 수행하지 않는다.

## 6. Work 준비 완료 조건

Codex 전환 전 current profile의 `WORK_PRODUCTION_INPUT_PACKET`을 닫는다.

- player promise·행동·선택·결과·실패 학습·보상
- approved scope / explicit non-scope / protected scope
- rules·UI/UX Flow·Data/State 계약
- actual consumer가 있는 Visual·Audio·VFX 요구와 승인 자산/절차
- provenance·license·rights·hash·durable locator
- deterministic test·runtime QA·build/export acceptance
- rollback과 evidence ceiling
- GitHub structured canon·Notion human canon write/readback

새 이미지·사운드·데이터를 만들기 전에 current project → approved asset/reference → Base reuse → 직접 관련된 검증 사례 → 공식/현업 benchmark 순으로 확인하고 `ADOPT / ADAPT / REJECT`한다. 중요 결정은 최소 3개 실질안을 비교한다.

## 7. 문제·해결·교훈 환류

```text
INCIDENT_SOLUTION_LESSON_LOOP
BASE_PROMOTION_DISPOSITION_REQUIRED
```

material failure·지연·우회가 생기면 symptom, exact environment/version/SHA/tool, root cause, 시도한 경로, 최종 해결, actual evidence, recurrence guard, rollback을 기록한다. 프로젝트 고유 값은 Project owner에 두고, 반복 가능하고 project-neutral한 원리만 Base case/BCP 후보로 판정한다. 새 공용 학습이 없으면 `NO_BASE_PROMOTION`을 명시한다.

관련 공용 교훈: `docs/knowledge/cases/WORK_CODEX_STARTER_LOCAL_EXECUTION_SYNC_CASE.md`.

## 8. 지연·복구·남은 작업 0

```text
STALL_SIGNAL_ROUTE_SWITCH
BOUNDED_RETRY_THEN_FALLBACK
EVIDENCE_EQUIVALENT_FALLBACK_ONLY
DEFER_BLOCKED_TASK_CONTINUE_INDEPENDENT_READY_WORK
SCOPE_BOUNDED_REQUIRED_WORK_ZERO
AUTOMATION_PHASE_REMAINING_WORK_ZERO
```

동일 root cause를 무한 재시도하지 않는다. readback → root-cause → bounded retry → authorized fallback A/B → local defer → independent work continue 순으로 진행한다. fallback은 검증·보안·권한·비용 수준을 낮추지 않는다.

현재 approved Slice의 machine-executable required work를 0까지 진행한다. 0이 되면 implementation/canon/consumer/test/runtime/build/PR/merge/readback/evidence를 다시 공격해 valid finding을 재개방하고 교정한다. 최소 5회 full-scope 적대적 검토 후 blocking finding 0에서만 clean exit한다.

## 9. Machine QA와 Human QA

```text
MACHINE_QA_FIRST
HUMAN_QA_DEFERRED_BY_CURRENT_USER
HUMAN_USABILITY_EVIDENCE: NOT_RUN
PLAYER_EXPERIENCE_EVIDENCE: NOT_RUN
```

프로젝트가 채택한 current authority를 사용한다. GUT은 deterministic GDScript test, Hera는 live QA/observability only이며 persistent authoring은 금지한다. 채택되지 않았다면 자동 설치하지 말고 evidence-equivalent test/runtime route를 사용한다. 필수 equivalent route가 없으면 `NOT_RUN`이며 automated readiness를 막는다.

GUT PASS, runtime PASS, screenshot diff PASS를 Human 이해·재미·기억 PASS로 승격하지 않는다.

## 10. 다운로드 가능한 실행 빌드 전달

```text
USER_DOWNLOADABLE_BUILD_ARTIFACT_REQUIRED
RUNNABLE_BY_USER_ONE_CLICK_PROJECT_PLAY_GATE
BUILD_SHA256_AND_DURABLE_LOCATOR_REQUIRED
CLEAN_EXTRACT_AND_LAUNCH_SMOKE_REQUIRED
NO_PUBLIC_RELEASE_WITHOUT_HIGH_RISK_APPROVAL
ARTIFACT_SECRET_AND_DEBUG_RESIDUE_SCAN_REQUIRED
```

현재 Project Profile의 목표 플랫폼과 export preset이 있고 export template·toolchain이 callable하면 internal/debug 플레이 빌드를 자동 export한다. 실행 파일과 필수 data를 하나의 portable ZIP 또는 플랫폼 표준 패키지로 묶고 다음을 확인한다.

- exact commit/build identity
- package SHA-256
- clean directory에 새로 풀어 실행하는 smoke
- 대표 Scene 진입과 성공 marker
- 필요한 runtime asset 포함 여부
- 다운로드 가능한 durable locator
- package 내부 secret·credential·`.git`·불필요한 absolute local path·temp evidence·의도하지 않은 debug log 검사

전달 우선순위:

```text
현재 채팅의 실제 파일 첨부
→ GitHub Actions workflow artifact
→ 프로젝트가 승인한 private/internal artifact route
→ 마지막으로 exact local build path + 한 블록 export/launch 안내
```

local path만 존재하면 다운로드 제공 완료로 주장하지 않는다. artifact upload capability가 없으면 `BLOCKED_NO_DURABLE_ARTIFACT_ROUTE`로 남긴다. GitHub Release·store·외부 공개 업로드는 `PUBLIC_RELEASE_OR_EXTERNAL_PUBLICATION`이며 별도 high-risk 결정 전에는 수행하지 않는다.

## 11. Codex·검수·병합·사용자 인계

```text
CODEX_EXECUTOR_NOT_CALLABLE_DO_NOT_CLAIM_IMPLEMENTED
DEFER_PRODUCT_IMPLEMENTATION_CONTINUE_WORK_READY_TASKS
DURABLE_CODEX_HANDOFF_REQUIRED
```

현재 host에서 Codex/product executor가 실제 callable하지 않으면 구현했다고 주장하지 않는다. `WORK_PRODUCTION_INPUT_PACKET`과 exact durable handoff를 정본에 남기고 product implementation만 `DEFERRED_EXTERNAL_EXECUTOR`로 보류하며, 남아 있는 Work-owned ready task는 계속한다. executor가 callable해진 뒤 Project GitHub·Notion을 fresh-read하고 재개한다.

Work 입력이 모두 준비되면 Codex가 Project GitHub·Notion을 fresh-read하게 하고 하나의 implementation window에서 actual product code·Scene·Resource·runtime wiring·test·build를 닫게 한다. 작은 finding은 한 건씩 되돌리지 말고 독립 작업을 계속한 뒤 consolidated packet으로 반환한다.

Work는 Codex 보고를 믿지 말고 actual diff·tests·runtime/screenshot/build evidence를 검수하고 correction을 재검증한다. current-task PR은 exact HEAD, required checks, unresolved thread 0, conflict 0, protected scope drift 0에서만 repository-supported squash merge하고 new-main과 Notion을 readback한다.

최종 상태는 다음이어야 한다.

```text
AUTOMATED_VERTICAL_SLICE_READY
READY_FOR_USER_VERTICAL_SLICE_VALIDATION
HUMAN_QA: DEFERRED_BY_USER
```

마지막 보고에는 변경 전→후→기대효과, 사용 Skill, reuse/benchmark/대안, Work 제작물, Codex 구현, Git SHA/PR/merge, GUT/Hera/runtime/build evidence, 다운로드 링크, NOT_RUN, high-risk deferred, 남은 machine work와 사용자 플레이 방법을 포함한다.
