---
name: maintaining-project-context-and-handoff
description: Use when project state must be resumed, current canon must be compressed for a new worker, or approved planning is ready for Codex implementation.
---

# Maintaining Project Context and Handoff

## Core principle

Active Context와 Handoff는 다른 책임 원본을 복제하는 장문 문서가 아니라 **현재 상태, 읽기 순서, 미완료 작업, 위험과 다음 책임자를 연결하는 압축 라우터**다.

현재 GPT↔Codex 역할 분리는 다음이 정본이다.

```text
GPT_PLANNING_REVIEW_VISUAL_OWNER
CODEX_IMPLEMENTATION_EXECUTOR
PLANNING_ONLY_NO_CODEX_REQUIRED
IMPLEMENTATION_REQUIRES_CODEX_HANDOFF
CODEX_REHYDRATE_GITHUB_AND_NOTION
CODEX_IMAGE_GENERATION_FORBIDDEN
CODEX_VISUAL_INPUT_NOTION_APPROVED_ONLY
GPT_VISUAL_REQUEST_REQUIRED_WHEN_ASSET_MISSING
```

GPT가 Godot POC/코드를 먼저 누적하고 사용자가 요청할 때만 Codex로 넘기는 `ON_DEMAND_CODEX_HANDOFF`의 과거 기본 의미는 폐기한다. `USER_REQUESTED_CODEX_HANDOFF`와 `on-demand-codex-handoff`는 사용자가 명시적으로 인계를 요청하는 **compatibility trigger/mode**로 남지만, 실제 구현·코딩이 존재하면 `IMPLEMENTATION_READY` 뒤 Codex 인계가 정상 다음 단계다.

별도 Codex Plan은 `CODEX_PREFLIGHT_OPTIONAL`이다. 구현 owner가 Codex라는 사실과 별개로 고위험·불확실·다중 의존성에서만 읽기 전용 preflight를 추가한다.

Canonical policy: `docs/GPT_CODEX_WORKFLOW_POLICY.md`
Detailed reference: `references/gpt-codex-implementation-handoff.md`

## Skill Modes

- `context-refresh`: 실제 상태·다음 작업·위험·읽기 순서를 Active Context에 압축 반영한다.
- `session-handoff`: 새 채팅·담당자·브랜치·마일스톤 경계의 재개 스냅샷을 작성한다.
- `codex-implementation-handoff`: `IMPLEMENTATION_READY` 이후 GitHub+Notion 정본 위치·승인 Visual·Acceptance Criteria·보호 범위를 Codex 실행 계약으로 압축한다.
- `on-demand-codex-handoff`: `USER_REQUESTED_CODEX_HANDOFF` 호환 mode. GPT 구현 누적을 전제로 하지 않고 `codex-implementation-handoff`와 같은 current contract를 사용한다.
- `implementation-package-handoff`: L2 이상 구현을 마스터 구현계획과 단계별 패키지로 인계하고 선택적 Codex Plan·Build·GPT 검수·병합 Gate를 관리한다.
- `resume`: 최신 GitHub·Notion·Branch·Commit·실제 파일·runtime/session identity를 다시 확인하고 중단된 패키지나 세션을 재개한다.
- `post-merge-reconcile`: 병합으로 stale해질 수 있는 `LIVE_CONTINUATION_STATE`만 새 main의 관측 사실과 재조정한다.

필요한 Mode만 실행한다. 단순 context 갱신에서 구현 패키지를 만들지 않고 작은 구현 인계에 대형 마스터 계획을 강제하지 않는다.

## Use when

- L1 이상 작업으로 현재 구현·검증·우선순위가 바뀌었다.
- 단계·Gate·Roadmap·다음 작업이 바뀌었다.
- 세션, 담당자, AI, 브랜치 또는 마일스톤 경계에서 인수인계가 필요하다.
- 새 채팅이나 Codex가 과거 대화 없이 작업을 재개해야 한다.
- Active Context가 실제 GitHub/Notion/파일 상태와 불일치한다.
- `IMPLEMENTATION_READY`이고 실제 code/data/Scene/Resource/config/test/runtime 변경이 필요하다.
- 사용자가 명시적으로 Codex 인계 또는 Codex 작업 명세를 요청했다.
- 전체 구현을 상위 추적 단위와 패키지별 Branch·PR로 나눠야 한다.
- 고위험 패키지에서 선택적 Codex Plan을 current truth와 대조해야 한다.
- 구현 패키지 결과를 검수하고 다음 패키지·사용자 검수·기획 반환·Visual 반환을 결정한다.
- 병합 직후 다음 세션이 읽을 `LIVE_CONTINUATION_STATE`가 merge 전 기준을 가리킬 위험이 있다.

## Do not use when

- 저장소 구현이 없는 단순 설명·브레인스토밍·기획 문서 교정이다.
- 오탈자처럼 다음 작업자에게 영향을 주지 않는 L0 수정이다.
- 분야 본책이나 Roadmap을 대신하는 거대한 요약본을 만들려는 경우다.
- 미검증 내용을 확정 상태로 압축하려는 경우다.
- 승인되지 않은 프로젝트 코어·주요 플레이 규칙 변경을 Codex Build에 몰래 포함하려 한다.
- Codex에 기획 방향 또는 이미지 생성·생성형 편집을 위임하려 한다.

## Required inputs

```yaml
project_agents:
project_start_here:
documentation_map:
active_context:
handoff:
current_stage_and_gate:
roadmap_issue_plan:
changed_or_target_files:
validation_results:
remaining_risks:
next_work:
invoked_skills:

codex_handoff:
  mode: CODEX_IMPLEMENTATION_HANDOFF
  trigger: IMPLEMENTATION_READY | USER_REQUESTED_CODEX_HANDOFF | CONTINUOUS_WORK_EXECUTOR_HANDOFF
  implementation_ready: true
  actual_state_verification_required: true
  notion_sources:
    project_home:
    relevant_domain_pages: []
    ai_system_detail_pages: []
    approved_visual_records: []
  github_sources:
    repository:
    structured_canon: []
    implementation_paths: []
    tests_and_runtime_evidence: []
  protected_behavior_and_contracts: []
  acceptance_criteria: []
  required_tests_and_runtime_checks: []
  forbidden_or_high_risk_changes: []
  visual_policy:
    generation_by_codex: FORBIDDEN
    approved_notion_visuals_only: true
    missing_visual_action: GPT_VISUAL_REQUEST
  codex_preflight: CODEX_PREFLIGHT_OPTIONAL

implementation_handoff:
  integrated_design:
  project_core_status:
  master_implementation_plan:
  parent_implementation_issue_or_tracking_unit:
  package_contract:
  baseline_branch_and_commit:
  allowed_package_branch:
  codex_plan_report:
  data_save_schema_constraints:
  required_tests:
  rollback:
  merge_execution: AGENT_MERGE_REQUIRED | AUTO_MERGE_BLOCKED
```

## Read first

1. 프로젝트 `AGENTS.md`
2. 프로젝트 `START_HERE.md` 또는 current router
3. Documentation Map
4. 현재 Active Context·Handoff·Decision·Requirement
5. 관련 Notion Project Home·Domain·AI/System page
6. 현재 구현에 필요한 승인 Visual record와 실제 attach/readback 상태
7. GitHub 분야 본책·실제 code/data/Scene/Resource/config/test/runtime evidence
8. 최신 `main`, 현재 branch/commit, 다른 open independent workstream
9. `docs/GPT_CODEX_WORKFLOW_POLICY.md`
10. L2 이상이면 `references/gpt-codex-implementation-handoff.md`
11. 존재하는 경우 마스터 구현계획·현재 package contract·Codex Plan report

## Process

### 1. Authority / runtime truth 확인

실제 code·data·asset·test와 Notion/GitHub 문서 상태를 비교한다. 확인하지 못한 결과는 `[미검증]`, `UNVERIFIED` 또는 `BLOCKED_UNVERIFIED`로 남긴다.

Codex 인계에서는 다음 의미를 고정한다.

> Handoff는 승인된 의도·정본 위치·보호 범위·Acceptance Criteria를 전달한다. 실제 구현 상태는 최신 GitHub와 관련 Notion을 직접 다시 읽어 검증할 것. 충돌하면 임의로 덮어쓰지 말고 기술 drift / 기획 drift / visual missing을 분류하고 `CHANGE_PROPOSAL` 또는 `GPT_VISUAL_REQUEST`를 사용한다.

### 2. 상태 분리

다음을 혼용하지 않는다.

- 확정
- 구현
- 검증
- 진행 중
- 미확정
- 보류
- 불일치
- 기술 개선
- 기획 변경 제안
- `WAITING_GPT_VISUAL`
- 사용자 체감 검수

### 3. 책임 원본 갱신

해당 owner 본책, Decision, Requirement, Roadmap, Manifest를 먼저 갱신한다. Active Context에는 전문을 복사하지 않고 경로와 현재 차이만 기록한다.

### 4. `context-refresh`

다음만 유지한다.

- 프로젝트 한 줄 방향과 현재 단계
- 이번 작업에서 실제로 바뀐 것
- 현재 구현·검증 상태
- 가장 중요한 미확정·위험
- 다음 우선 작업과 선행 조건
- 변경 금지·보호 경로
- 먼저 읽을 3~7개 책임 원본
- 필요한 Codex/Skill/검증 경로

### 5. `session-handoff`

```text
현재 상태
→ 이번 작업 결과
→ 남은 작업
→ 위험·미검증
→ 다음 작업자의 첫 행동
→ 읽을 GitHub/Notion 정본
→ 검증·rollback
```

과거 대화 전체, 도구 호출 로그, 이미 본책에 반영된 전문은 포함하지 않는다.

### 6. `codex-implementation-handoff`

실제 구현이 존재하면 다음을 압축한다.

```text
player outcome / intent
→ GitHub 정본 위치
→ Notion 기획·Flow·AI/System 세부 위치
→ 승인 Visual 위치와 current-use 승인 상태
→ 실제 확인해야 할 code/data/Scene/Resource/config/test 범위
→ known problem / improvement goal
→ protected behavior / data contract
→ Acceptance Criteria
→ test/runtime/play criteria
→ high-risk / forbidden change
→ visual missing action = GPT_VISUAL_REQUEST
→ completion report fields
```

이 단계는 current `CODEX_IMPLEMENTATION_HANDOFF`다. 과거 이름 `ON_DEMAND_CODEX_HANDOFF`는 명시적 사용자 trigger를 위한 compatibility alias일 뿐, 평상시 GPT가 제품 구현을 누적한다는 의미가 아니다.

Codex는 Handoff 뒤 `CODEX_REHYDRATE_GITHUB_AND_NOTION`을 수행한다.

### 7. Visual Gate

Codex는 이미지 생성·생성형 편집을 하지 않는다. 현재 용도가 승인되고 Notion에 upload/attach/readback된 Visual만 사용한다.

Visual이 없으면:

```yaml
GPT_VISUAL_REQUEST:
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
```

GPT가 이미지 제작·검수·Notion delivery를 끝내면 Codex가 해당 Notion destination을 fresh-read하고 재개한다. 독립 구현이 가능하면 Visual 대기 때문에 전체 작업을 멈추지 않는다.

### 8. 구현 범위·패키지 판정

작은 국소 변경은 단일 실행 명세로 충분할 수 있다. L2 이상·다중 의존성·여러 Scene/Schema/Resource가 얽힌 작업만 마스터 구현계획과 독립 package로 분해한다.

필수:

- `CORE_CONFIRMED`
- `READY_FOR_IMPLEMENTATION_HANDOFF`
- 승인된 통합 설계 명세
- 마스터 구현계획
- 상위 구현 Issue 또는 동등한 tracking unit
- 현재 package result/include/exclude/protected scope
- 데이터·저장·ID·Schema 보호 조건
- 기준 Branch·Commit과 allowed package branch
- required tests/runtime evidence
- rollback

차단 항목이 있으면 `BLOCKED` 또는 `UNVERIFIED`로 유지한다.

Template:

- `templates/project-operations/MASTER_IMPLEMENTATION_PLAN.md`
- `templates/project-operations/IMPLEMENTATION_PACKAGE_CONTRACT.md`

### 9. `CODEX_PREFLIGHT_OPTIONAL`

Codex Plan은 고위험·불확실·다중 의존성 또는 사용자가 명시적으로 요청한 경우에만 별도 preflight로 실행한다.

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

Plan은 최신 GitHub+Notion, 실제 파일, 선행 package, 의존성, 위험, Red → Green → Refactor, test와 rollback을 조사한다.

Plan 금지:

- 파일 생성·수정·삭제·이동
- Commit·Push·PR·Issue 변경
- 마스터 구현계획 직접 덮어쓰기
- 프로젝트 코어·MVP·플레이 규칙의 암묵 변경
- 이미지 생성·생성형 편집
- 존재하지 않는 파일·API·test command 추측

Plan을 생략해도 Codex Build의 current truth 조사는 필수다.

### 10. 기술 개선·기획 변경 판정

- 동일한 플레이어 결과와 데이터 계약을 유지하는 구조·성능·안정성·테스트 개선은 기술 변경으로 Codex가 구현할 수 있다.
- 프로젝트 코어, Core Loop, 플레이 규칙, MVP, 주요 UI·UX, 콘텐츠 의미, 승인 기능 제거, 저장 호환성 파괴는 `CHANGE_PROPOSAL`이다.
- 조작감·난이도·보상 체감·아트·연출·사운드·Vertical Slice 판단은 `USER_DECISION_REQUIRED`다.
- 필요한 이미지가 없으면 `WAITING_GPT_VISUAL`이다.

### 11. Codex Build 인계

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

Codex는 current GitHub+Notion을 조사한 뒤 승인 범위의 code/data/Scene/Resource/config/test/build/runtime 구현·검증·Commit/Push/PR 작업을 현재 repository policy에 맞게 수행한다.

### 12. 구현 결과 검수와 승인 Gate

Codex 결과:

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

GPT는 Commit·**원격 HEAD**·diff·test/runtime evidence와 승인 Intent를 확인하고 다음으로 판정한다.

- `PACKAGE_APPROVED`
- `PACKAGE_APPROVED_WITH_TECHNICAL_CHANGES`
- `USER_REVIEW_REQUIRED`
- `CHANGE_PROPOSAL`
- `WAITING_GPT_VISUAL`
- `REVISE`
- `BLOCKED`
- `UNVERIFIED`

### 13. `resume`

최신 `main`, package branch, 원격 HEAD, 마지막 승인 Commit, GitHub+Notion Handoff, 실제 파일을 다시 대조한다. 오래된 Plan이나 과거 대화만 그대로 실행하지 않는다.

외부 Editor/MCP/runtime session을 다루는 인계에서 **stale PID/session** 값과 historical evidence는 current authority가 아니다.

```text
historical evidence
→ fresh-read
→ current process, transport ownership, server registration, exact target session
→ project/session/version/readiness
→ mutation allowed or BLOCKED_UNVERIFIED
```

같은 관측창의 증거가 없으면 원인을 확정하지 않고 `BLOCKED_UNVERIFIED`로 남긴다. 이 Handoff는 **외부 transport 복구 진단 절차를 중복 소유하지 않는다**. 해당 runtime/tool owner의 recovery contract를 연결한다.

### 14. `post-merge-reconcile`

이 mode는 `LIVE_CONTINUATION_STATE`에만 조건부로 적용한다. 날짜·commit·당시 CI를 설명하는 `PRE_MERGE_SNAPSHOT`, Change Log, 승인 기록은 유효한 historical snapshot이므로 현재 상태로 덮어쓰거나 자동 수정하지 않는다.

```text
merge
→ OBSERVE_POST_MERGE_TRUTH (최신 main·정확한 merge SHA·원격 CI·열린 후속 PR)
→ live router가 stale인지 판정
→ 필요한 최소 reconciliation을 IN_PROGRESS로 기록
→ PRE_MERGE_SNAPSHOT 보존
→ 실제 post-merge CI 상태 기록
→ 검증
→ close
```

- `OBSERVE_POST_MERGE_TRUTH`는 merge 직후와 resume 시점의 실제 원격 상태를 다시 읽는다. merge 전 예상 SHA나 PR 본문을 current truth로 재사용하지 않는다.
- live router가 없거나 다음 세션 판단에 영향을 주지 않으면 이 mode를 호출하지 않는다.
- 자동 project-state writeback, 자기 자신의 SHA를 다시 쓰는 loop, 날짜가 찍힌 history의 현재화는 금지한다.
- same PR에서 안전하게 갱신할 수 없으면 `IN_PROGRESS`와 다음 확인 행동만 남기고 별도 범위로 추적한다.

### 15. 콜드 스타트 검수

새 작업자가 10분 안에 다음을 찾는지 확인한다.

- 무엇을 만드는가?
- 현재 어디까지 됐는가?
- 다음 작업은 무엇인가?
- 무엇을 바꾸면 안 되는가?
- 관련 GitHub/Notion 본책·Skill·실제 파일·검증은 어디인가?
- 현재 Branch·Commit·실행 명세·package 상태는 무엇인가?
- 사용자 결정, `CHANGE_PROPOSAL`, `WAITING_GPT_VISUAL`이 남았는가?

## Output contract

### 일반 Context·Handoff

```md
## 현재 상태
## 이번 작업 결과
## 확정·구현·검증·미확정
## 다음 작업과 선행 조건
## 보호 범위
## 먼저 읽을 책임 원본
## 호출 Skill
## 검증·미검증·rollback
```

### Codex Implementation Handoff

```yaml
mode: CODEX_IMPLEMENTATION_HANDOFF
trigger: IMPLEMENTATION_READY | USER_REQUESTED_CODEX_HANDOFF | CONTINUOUS_WORK_EXECUTOR_HANDOFF
notion_sources: {}
github_sources: {}
approved_visual_records: []
protected_behavior_and_contracts: []
acceptance_criteria: []
required_tests_and_runtime_checks: []
forbidden_or_high_risk_changes: []
visual_policy:
  generation_by_codex: FORBIDDEN
  approved_notion_visuals_only: true
  missing_visual_action: GPT_VISUAL_REQUEST
```

## Merge boundary

기본 정책은 `AUTO_MERGE_AFTER_REQUIRED_CHECKS`와 `AGENT_MERGE_REQUIRED`다.

`APPROVED_ITEM_INHERITS_MERGE_AUTHORITY`: 이미 명시적으로 승인된 동일 범위의 구현·검증·PR은 현재 exact HEAD·required check·독립 검토·unresolved thread·차단 상태를 확인한 뒤 **추가 확인·재승인·병합 승인 요청 없이** 허용된 방식으로 병합할 수 있다. **별도 사용자 병합 승인**은 기본 필수가 아니다.

새 범위·새 기획 결정·새 P0/P1·`USER_REVIEW_REQUIRED`·`CHANGE_PROPOSAL`·`WAITING_GPT_VISUAL`은 기존 승인을 확장 해석하지 않는다.

다른 독립 open/draft/ready PR·branch·worktree는 read-only로 보호한다.

## Definition of Ready

- [ ] 실제 변경 대상과 현재 검증 결과를 확인했다.
- [ ] 관련 GitHub/Notion 책임 원본을 식별했다.
- [ ] 다음 작업과 미완료 범위가 있다.
- [ ] 구현 task이면 `CODEX_IMPLEMENTATION_HANDOFF`와 `IMPLEMENTATION_READY`가 있다.
- [ ] L2 이상이면 프로젝트 코어·마스터 계획·package contract가 승인됐다.
- [ ] `CODEX_PREFLIGHT_OPTIONAL` 사용 여부를 위험 기반으로 판정했다.
- [ ] Visual dependency가 있다면 current-use 승인·Notion attach/readback 또는 `WAITING_GPT_VISUAL` 상태가 있다.

## Definition of Done

- [ ] Active Context가 실제 상태와 일치한다.
- [ ] Handoff가 다음 작업자의 첫 행동을 명확히 한다.
- [ ] 전문 중복 없이 책임 원본을 연결한다.
- [ ] `[백업]`, `[보류]`, 제거 후보가 기본 읽기에 혼입되지 않는다.
- [ ] 콜드 스타트 질문에 답할 수 있다.
- [ ] Codex 인계에서 GitHub+Notion current truth 재조사가 요구된다.
- [ ] package Branch·Commit·Plan 사용 여부·검증·승인 상태가 추적된다.
- [ ] 기술 개선·기획 변경·Visual 반환·사용자 판단이 구분됐다.
- [ ] 인수인계 실패나 누락을 Learning Log에 기록했다.
- [ ] `LIVE_CONTINUATION_STATE`와 `PRE_MERGE_SNAPSHOT`을 구분했고 post-merge truth 재관측 여부를 판정했다.

## Validation

- 본책과 Active Context의 상태가 충돌하지 않는가?
- 실제 GitHub/Notion/파일·검증 경로가 존재하는가?
- 다음 작업의 선행 조건과 완료 기준이 명확한가?
- 새 채팅/Codex가 과거 대화 없이 작업을 시작할 수 있는가?
- 기본 읽기 문서가 과도하게 많지 않은가?
- Codex Plan을 사용했다면 파일·Issue·PR을 수정하지 않았는가?
- Codex Build가 current GitHub+Notion을 재수화하고 승인 범위만 수정했는가?
- Codex가 이미지를 생성·생성형 편집하지 않았는가?
- Commit SHA·원격 HEAD·test/runtime 결과를 실제 확인했는가?
- `AGENT_MERGE_REQUIRED`와 `APPROVED_ITEM_INHERITS_MERGE_AUTHORITY` 조건을 실제 확인했는가?
- live router가 있다면 `OBSERVE_POST_MERGE_TRUTH` 뒤에만 reconciliation을 판단했는가?

## Failure conditions

- Active Context가 분야 본책의 복제본이 됨
- 과거 대화나 도구 로그 전체를 필수 context로 만듦
- 실제 확인 없이 구현·검증 완료로 기록함
- 다음 작업·위험·보호 범위를 누락함
- 오래된 경로나 보류 문서를 기본 읽기에 남김
- 구현이 있는데 사용자 Codex 요청이 없다는 이유로 GPT가 제품 BUILD를 직접 수행함
- 저위험 명확 작업에 `CODEX_PREFLIGHT_OPTIONAL` Plan을 의무화함
- Codex Plan이 파일·Issue·PR을 수정함
- 기술 개선을 이유로 프로젝트 코어·MVP·플레이 규칙을 암묵 변경함
- Codex가 이미지 생성·생성형 편집 또는 승인되지 않은 Visual을 사용함
- 다른 독립 open PR/worktree를 변경·흡수함
- force push·history rewrite·destructive reset/restore/clean
- 이미 승인된 동일 범위에 대해 추가 확인·재승인·병합 승인 요청을 반복함
- historical snapshot을 live router처럼 덮어쓰거나 post-merge reconciliation으로 self-SHA writeback loop를 만듦
- Gate 미통과, P0/P1 잔존 또는 허용되지 않은 방식으로 병합함

## Learning contract

다음이 발생하면 `LEARNING_LOG.md`를 갱신한다.

- 새 채팅/Codex가 핵심 상태나 다음 작업을 찾지 못함
- Active Context와 실제 GitHub/Notion/파일이 반복 충돌함
- 필수 문서가 너무 많아 콜드 스타트가 느림
- 인수인계 후 동일 질문이 반복됨
- rollback·검증 경로 부족으로 작업이 중단됨
- GPT 명세와 actual repository/Notion 차이가 반복됨
- 불필요한 Codex Plan이 반복되어 비용·지연만 증가함
- Codex 이미지 생성/승인 Visual drift가 발생함
- package 경계가 너무 커 회귀·rollback이 실패함
