# GPT–Codex 단계별 구현 인계

이 reference는 `maintaining-project-context-and-handoff`의 `codex-implementation-handoff`, compatibility `on-demand-codex-handoff`, `implementation-package-handoff` 상세 절차다.

Canonical policy: `docs/GPT_CODEX_WORKFLOW_POLICY.md`

## 1. 책임 분리

```text
GPT
= 기획·조사·벤치마킹·적대적 검수·마스터 구현계획·구현 명세·이미지 제작/검수·최종 결과 검수

Codex Plan
= CODEX_PREFLIGHT_OPTIONAL 읽기 전용 기술 재검수와 기술 개선/변경 제안

Codex Build
= 최신 GitHub + Notion 재수화 + 승인 범위 구현·코딩·테스트·runtime evidence

사용자
= 프로젝트 방향·체감·새 기획 변경·이미지 결과 승인 결정

GitHub
= 구조화·구현 정본과 branch/commit/PR/merge evidence

Notion
= 사람용 기획·Flow·시각 정본과 승인 Visual의 실제 전달 위치
```

GPT가 평상시 Godot POC/코드를 구현하고 사용자가 요청할 때만 Codex로 넘기는 과거 기본 흐름은 폐기한다. **기획만이면 GPT에서 종료할 수 있고, 실제 구현·코딩이 존재하면 Codex Build가 정상 다음 단계**다.

`USER_REQUESTED_CODEX_HANDOFF`와 과거 `ON_DEMAND_CODEX_HANDOFF` 명칭은 explicit handoff의 compatibility alias로만 남고 정상 Build 전환의 필수조건이 아니다.

## 2. 구현 인계 준비

`READY_FOR_IMPLEMENTATION_HANDOFF` 또는 `IMPLEMENTATION_READY`이고 실제 repository/runtime mutation이 필요하면 `CODEX_IMPLEMENTATION_HANDOFF`를 만든다. 별도 사용자 전환 요청은 필수가 아니다.

최소 계약:

```yaml
mode: CODEX_IMPLEMENTATION_HANDOFF
trigger: IMPLEMENTATION_READY | USER_REQUESTED_CODEX_HANDOFF | CONTINUOUS_WORK_EXECUTOR_HANDOFF
intent_and_player_outcome:
implementation_ready: true
actual_state_verification_required: true

notion_sources:
  project_home:
  relevant_domain_pages: []
  ai_system_detail_pages: []
  approved_visual_records: []

github_sources:
  repository:
  project_agents:
  active_context:
  structured_canon: []
  implementation_paths: []
  tests_and_runtime_evidence: []

known_problems_and_improvement_goals: []
protected_behavior_and_contracts: []
priority_order: []
acceptance_criteria: []
required_tests_and_runtime_checks: []
performance_size_structure_checks: []
forbidden_or_high_risk_changes: []

visual_policy:
  generation_by_codex: FORBIDDEN
  approved_notion_visuals_only: true
  missing_visual_action: GPT_VISUAL_REQUEST

codex_preflight: CODEX_PREFLIGHT_OPTIONAL
```

명세에는 다음 의미를 고정한다.

> 이 명세는 승인된 기획 의도·성공 기준·보호 범위와 현재 정본 위치를 설명한다. 실제 구현 상태는 반드시 최신 GitHub와 관련 Notion 정본을 직접 다시 읽어 검증할 것. 명세와 current truth가 충돌하면 임의로 덮어쓰지 말고 원인을 분류할 것. 기획 변경이 필요하면 `CHANGE_PROPOSAL`, 이미지가 부족하면 `GPT_VISUAL_REQUEST`로 반환할 것.

작은 국소 변경에는 마스터 계획·상위 Issue·별도 Codex Plan을 형식적으로 강제하지 않는다.

## 3. 인계 전 GPT Gate

GPT는 다음을 확인한 뒤 구현으로 넘긴다.

- 프로젝트 core/player promise와 현재 목표가 닫힘
- 필요한 벤치마킹·대안 비교·적대적 검토 완료
- `IMPLEMENTATION_READY`
- Notion 사람용 기획·Flow·핵심 데이터 current
- GitHub structured contract와 충돌 없음
- 사용 Visual이 있다면 current-use 승인 + 실제 Notion attach/readback 확인
- Acceptance Criteria와 보호 범위 존재
- 구현 전 새 사용자 결정이 필요한 conflict 없음
- L2+이면 마스터 구현계획·package dependency·rollback 존재

차단되면 관련 범위를 `BLOCKED`, `USER_DECISION_REQUIRED`, `CHANGE_PROPOSAL` 또는 `WAITING_GPT_VISUAL`로 유지한다.

## 4. Codex 재수화 Gate

Codex Build의 첫 단계는 `CODEX_REHYDRATE_GITHUB_AND_NOTION`이다.

```text
exact project/repository 확인
→ 최신 `main` + task branch + current open independent workstream 확인
→ Project AGENTS.md / Active Context / current Decision 읽기
→ relevant Notion Project Home / Domain / AI System page 읽기
→ approved Visual record + actual attach/readback 확인
→ actual code/data/Scene/Resource/config/test/runtime 읽기
→ GPT handoff와 current truth 대조
→ protected scope / Acceptance / rollback 확인
→ current authoring authority/session 확인
→ BUILD
```

과거 대화·stale handoff·로컬 캐시만으로 구현하지 않는다. 프로젝트가 HiGodot 또는 다른 persistent authoring authority를 채택했다면 Codex도 이를 우회하지 않는다.

## 5. 이미지 소비 Gate

### 금지

Codex는 다음을 수행하지 않는다.

- 이미지 신규 생성
- 생성형 이미지 편집·스타일 변환
- 구현 편의를 위한 임시 AI art/placeholder 생성
- 승인되지 않은 이미지의 제품 경로 사용

### 허용

현재 용도로 승인되고 Notion에 실제 upload/attach/readback된 Visual을 소비한다.

- prototype: explicit prototype use가 명시된 `APPROVED_CANDIDATE`
- production tracked asset: `PROJECT_ASSET_APPROVED` + rights/provenance + target path

코드 기반 UI layout, shader/VFX, primitive drawing, animation wiring은 구현 코드로 수행할 수 있다. 별도 image asset 자체가 필요해지면 GPT로 반환한다.

### `GPT_VISUAL_REQUEST`

```yaml
GPT_VISUAL_REQUEST:
  project:
  implementation_task:
  why_required:
  player_or_ui_role:
  asset_type:
  target_screen_or_scene:
  required_dimensions_or_ratio:
  transparency_or_format:
  visual_constraints:
  existing_approved_references: []
  notion_destination:
  acceptance_criteria: []
  can_other_independent_implementation_continue: true | false
```

GPT가 사용자 승인 Gate를 거쳐 이미지를 제작/편집·검수하고 Notion에 승인 상태로 attach/readback하면 Codex가 destination을 다시 읽고 재개한다.

## 6. L2 이상 패키지 준비 Gate

다중 의존성·고위험·Vertical Slice 구현처럼 package가 필요한 경우 다음을 확인한다.

- 프로젝트 코어와 통합 설계 승인
- `READY_FOR_IMPLEMENTATION_HANDOFF`
- 마스터 구현계획 존재
- 상위 구현 Issue 또는 동등 tracking unit 존재
- 현재 package 결과·포함·제외·수정 금지 범위 존재
- 데이터·저장·ID·Schema 보호 조건 존재
- 기준 Branch/Commit과 allowed branch/rollback 존재
- 테스트 명령과 runtime/play evidence 기준 존재
- 사용자 기존 변경·보호 경로 파악
- current repository required checks/ruleset 발견 경로 존재
- Visual dependency 상태 명시

하나라도 차단되면 `BLOCKED` 또는 `UNVERIFIED`로 유지한다.

## 7. 패키지 경계

패키지는 파일 목록이 아니라 독립 결과로 정의한다.

좋은 경계:

- 핵심 상태 모델이 테스트 가능한 상태
- 하나의 플레이 행동이 입력→반응→결과까지 동작
- 실패·복구 루프가 독립 검증됨
- 저장·불러오기 한 주기가 호환성 테스트됨
- Vertical Slice 대표 구간이 플레이 가능

나쁜 경계:

- 스크립트 몇 개 작성 자체가 결과
- UI 파일 모음만 존재
- 여러 의존 시스템을 동시에 변경하지만 독립 결과가 없음
- 같은 Scene·Schema를 여러 package가 경쟁 수정

기본 병렬성은 `SEQUENTIAL`이다. 완전히 독립적인 작업만 병렬화한다.

## 8. `CODEX_PREFLIGHT_OPTIONAL` Plan

별도 Codex Plan은 다음에서만 사용한다.

- 저장·Schema·마이그레이션·플랫폼 설정 같은 고위험 변경
- GPT 명세와 실제 저장소의 drift 가능성이 큼
- 여러 package·Scene·공용 Resource가 얽힘
- 구현 전에 기술 대안·`CHANGE_PROPOSAL` 분리가 필요함
- 사용자가 명시적으로 Plan 검토를 요청함

사용할 경우 Codex Plan은 **읽기 전용**이다.

```yaml
mode: PLAN_REVIEW_ONLY
file_write: FORBIDDEN
commit_push_pr_issue: FORBIDDEN
baseline_branch:
baseline_commit:
allowed_branch:
master_plan:
package_contract:
required_reading:
  github: []
  notion: []
```

Plan 수행:

- 최신 `main` 및 target branch/current truth 확인
- GitHub+Notion 정본과 실제 파일 대조
- 선행 package와 의존성 확인
- 위험·데이터/저장 영향·rollback 분석
- Red → Green → Refactor 제안
- performance/stability/test 개선 제안
- `CHANGE_PROPOSAL`, `USER_DECISION_REQUIRED`, `WAITING_GPT_VISUAL` 분리

Plan 금지:

- 파일 생성·수정·삭제·이동
- Commit·Push·PR·Issue 변경
- 마스터 구현계획 직접 덮어쓰기
- 프로젝트 코어·MVP·플레이 규칙의 암묵 변경
- 이미지 생성·생성형 편집
- 존재하지 않는 file/API/test command 추측

Codex Plan 보고서는 필요한 경우 `templates/project-operations/CODEX_PACKAGE_PLAN_REPORT.md` 형식을 사용한다. Plan을 생략해도 Build의 GitHub+Notion 선조사는 필수다.

## 9. Plan 판정과 GPT 반영

### 기술 개선

플레이어 결과와 승인된 데이터·저장 계약을 유지하는 기술 개선은 Codex Build가 승인 범위에서 구현할 수 있다.

### `CHANGE_PROPOSAL`

프로젝트 코어, Core Loop, 플레이 규칙, MVP, 주요 UI·UX, 콘텐츠 의미, 승인 기능 제거, 호환성 파괴가 필요하면 구현과 분리한다.

### `USER_DECISION_REQUIRED`

조작감, 난이도, 보상 체감, 아트·연출·사운드, 둘 이상의 유효한 UX 선택, Vertical Slice 승인처럼 사용자 판단이 필요한 경우 사용한다.

### `WAITING_GPT_VISUAL`

승인 이미지가 없거나 current-use 승인이 불명확하면 사용한다. Codex가 이미지를 대신 만들지 않는다.

Codex Plan을 사용한 경우 Codex가 기획 책임 원본을 직접 덮어쓰지 않는다. GPT가 다음을 수행한다.

1. current GitHub+Notion 조사 근거 확인
2. 마스터 계약과 대조
3. 기술 개선 승인 범위 확인
4. `CHANGE_PROPOSAL`·사용자 결정·Visual request 분리
5. package contract·tracking checklist 갱신
6. `READY_FOR_BUILD` 판정

## 10. Codex Build 지시

```yaml
implementation:
  owner: CODEX
  actual_state_verification_required: true
  scope: APPROVED_PACKAGE_ONLY
  unrelated_changes: FORBIDDEN
  preserve_user_changes: true
visuals:
  generation_or_generative_editing: FORBIDDEN
  source: NOTION_APPROVED_ATTACHED_READBACK_ONLY
  missing: GPT_VISUAL_REQUEST
vcs:
  allowed_branch:
  main_direct_push: FORBIDDEN_UNLESS_CURRENT_REPOSITORY_POLICY_EXPLICITLY_ALLOWS_AND_TASK_AUTHORIZES
  force_push: FORBIDDEN
  amend_or_history_rewrite: FORBIDDEN
  unrelated_open_pr_mutation: FORBIDDEN
```

과거 `godot_runtime_files_only: true`는 공용 기본 제한으로 사용하지 않는다. Codex는 승인 package에 필요한 code/data/Scene/Resource/config/test/build/runtime 및 구현 구조화 문서를 수정할 수 있다. 단, 프로젝트 코어·승인 기획의 의미를 바꾸는 변경은 `CHANGE_PROPOSAL` 없이는 수행하지 않는다.

## 11. Build 전후 VCS 가드레일

### Push 전

- current `git status` 또는 동등 change inventory
- 최신 `main`, baseline branch/commit, allowed branch 확인
- changed file 목록·승인 범위 확인
- other open/draft/ready PR/worktree overlap 검사
- 사용자 기존 변경 보존 확인
- static/headless/runtime/regression 수행
- failed/not-run 명시
- 사용 Visual의 Notion 승인/readback 확인

### Git 금지

- current repository policy/task 명시 없이 main 직접 push
- force push
- 승인 없는 amend/history rewrite
- 다른 독립 PR branch 변경·흡수·close·merge
- destructive reset/restore/clean

### Push 후

- Commit SHA
- **원격 HEAD**와 local/result Commit 일치
- changed files + reason
- actual command/test/runtime 결과
- approved Notion Visual consumed
- `CHANGE_PROPOSAL`, `WAITING_GPT_VISUAL`, NOT_RUN, remaining risk
- rollback

## 12. 구현 결과 검수

Codex 반환:

```yaml
codex_result:
  baseline_and_final_commit:
  changed_files_and_reasons: []
  tests_passed: []
  tests_failed: []
  tests_not_run: []
  runtime_or_play_evidence: []
  approved_notion_visuals_consumed: []
  visual_requests_waiting: []
  technical_improvements: []
  change_proposals: []
  remaining_risks: []
  rollback:
```

GPT 검수:

- 지정 Branch·Commit·변경 파일·**원격 HEAD**
- 승인된 package scope
- 기술 개선과 기획 변경 구분
- 데이터·저장 호환성
- 정상·실패·경계·회귀 test
- actual runtime/play evidence
- 승인된 Notion Visual만 사용했는지
- Codex가 이미지를 생성·편집하지 않았는지
- NOT_RUN·위험·rollback

## 13. 패키지 종료 상태

- `PACKAGE_APPROVED`
- `PACKAGE_APPROVED_WITH_TECHNICAL_CHANGES`
- `USER_REVIEW_REQUIRED`
- `CHANGE_PROPOSAL`
- `WAITING_GPT_VISUAL`
- `REVISE`
- `BLOCKED`
- `UNVERIFIED`

`PACKAGE_APPROVED*`만 다음 package와 병합 적격성 검토에 진입한다.

## 14. 병합 Gate

기본 정책은 `AUTO_MERGE_AFTER_REQUIRED_CHECKS`와 `AGENT_MERGE_REQUIRED`다.

`APPROVED_ITEM_INHERITS_MERGE_AUTHORITY`: 이미 사용자의 명시적 승인이 완료된 동일 범위는 **추가 확인·재승인·병합 승인 요청 없이** 검증 후 병합할 수 있다. **별도 사용자 병합 승인**은 기본 필수가 아니다.

병합 전에는 current repository의 실제 required checks, ruleset, merge method를 발견한다. 공용 문서에서 과거 특정 check 이름을 영구 고정하지 않는다.

```yaml
merge_policy: AUTO_MERGE_AFTER_REQUIRED_CHECKS
reviewed_head_sha:
current_head_sha:
required_checks_observed: []
required_checks_passed:
unresolved_review_threads:
ruleset:
merge_method:
user_review_required:
change_proposal:
waiting_gpt_visual:
merge_gate:
```

허용 조건:

- `PACKAGE_APPROVED` 또는 `PACKAGE_APPROVED_WITH_TECHNICAL_CHANGES`
- PR이 Draft가 아님
- reviewed HEAD == current HEAD
- current Required Check 성공
- unresolved review thread 0
- current repository가 허용한 병합 방식
- `USER_REVIEW_REQUIRED`·`CHANGE_PROPOSAL`·`WAITING_GPT_VISUAL` 없음

상태:

- `AUTO_MERGE_ELIGIBLE`
- `AUTO_MERGE_ENABLED`
- `AUTO_MERGE_BLOCKED`
- `UNVERIFIED_REPOSITORY_SETTING`

## 15. GitHub 구조

L2 이상 package 작업의 기본 구조:

```text
상위 구현 추적 단위
├─ PKG-00 Branch / PR
├─ PKG-01 Branch / PR
├─ PKG-02 Branch / PR
└─ Vertical Slice 통합 Branch / PR
```

기본 병렬성은 `SEQUENTIAL`이다. 완전히 독립적인 작업만 병렬 허용한다. 다른 독립 open/draft/ready PR은 read-only로 보호한다.

## 16. 중단·재개

중단 시 Handoff에 다음을 남긴다.

- 마지막 승인 범위와 Commit
- GitHub/Notion 다시 읽기 경로
- 현재 package 상태
- Codex Plan 사용 여부와 결과
- Push된 Commit·test·runtime evidence
- 사용한 승인 Visual
- `GPT_VISUAL_REQUEST` / `WAITING_GPT_VISUAL`
- `CHANGE_PROPOSAL`·사용자 결정
- 병합 상태와 차단 원인
- 다음 첫 행동
- rollback

재개 시 최신 `main`, package branch, 원격 HEAD, GitHub+Notion current truth를 다시 대조하고 오래된 Plan이나 과거 대화만 그대로 사용하지 않는다.

외부 editor/MCP/runtime을 사용한 경우 stale PID/session과 historical evidence를 current readiness로 재사용하지 않는다. `current process, transport ownership, server registration, exact target session`과 project/session/version/readiness를 fresh-read한다. 증거가 없으면 `BLOCKED_UNVERIFIED`로 남기고 runtime owner의 recovery contract를 따른다.
