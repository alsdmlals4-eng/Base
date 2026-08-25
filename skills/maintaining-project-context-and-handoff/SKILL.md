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
```

GPT가 Godot POC/코드를 먼저 누적하고 사용자가 요청할 때만 Codex로 넘기는 `ON_DEMAND_CODEX_HANDOFF` 기본 의미는 폐기한다. 사용자의 명시적 인계 요청은 호환 trigger로 남을 수 있으나, **구현·코딩이 존재하면 Implementation Ready 뒤 Codex 인계가 정상 다음 단계**다.

별도 Codex Plan은 `CODEX_PREFLIGHT_OPTIONAL`이다. 구현 owner가 Codex라는 사실과 별개로, 고위험·불확실·다중 의존성에서만 읽기 전용 preflight를 추가한다.

Canonical policy: `docs/GPT_CODEX_WORKFLOW_POLICY.md`
Detailed reference: `references/gpt-codex-implementation-handoff.md`

## Skill Modes

- `context-refresh`: 실제 상태·다음 작업·위험·읽기 순서를 Active Context에 압축 반영한다.
- `session-handoff`: 새 채팅·담당자·브랜치·마일스톤 경계의 재개 스냅샷을 작성한다.
- `codex-implementation-handoff`: `IMPLEMENTATION_READY` 이후 GitHub+Notion 정본 위치·승인 Visual·Acceptance Criteria·보호 범위를 Codex 실행 계약으로 압축한다.
- `on-demand-codex-handoff`: `USER_REQUESTED_CODEX_HANDOFF` 호환 trigger. 의미는 `codex-implementation-handoff`와 동일하며 GPT 구현 누적을 전제로 하지 않는다.
- `implementation-package-handoff`: L2 이상 구현을 마스터 계획과 단계별 패키지로 인계하고 선택적 Codex Plan·Build·GPT 검수·병합 게이트를 관리한다.
- `resume`: 최신 GitHub·Notion·Branch·Commit·실제 파일을 다시 확인하고 중단된 패키지나 세션을 재개한다.
- `post-merge-reconcile`: 병합으로 stale해질 수 있는 live continuation router만 새 main의 관측 사실과 재조정한다.

필요한 Mode만 실행한다. 작은 구현 인계에 대형 마스터 계획을 강제하지 않는다.

## Use when

- L1 이상 작업으로 현재 구현·검증·우선순위가 바뀌었다.
- 단계·게이트·Roadmap·다음 작업이 바뀌었다.
- 세션, 담당자, AI, 브랜치 또는 마일스톤 경계에서 인수인계가 필요하다.
- 새 채팅이나 Codex가 과거 대화 없이 작업을 재개해야 한다.
- Active Context가 실제 GitHub/Notion/파일 상태와 불일치한다.
- `IMPLEMENTATION_READY`이고 실제 code/data/Scene/Resource/config/test/runtime 변경이 필요하다.
- 사용자가 명시적으로 Codex 인계 또는 Codex 작업 명세를 요청했다.
- 전체 구현을 상위 추적 단위와 패키지별 Branch·PR로 나눠야 한다.
- 고위험 패키지에서 선택적 Codex Plan을 current truth와 대조해야 한다.
- 구현 결과를 검수하고 다음 패키지·사용자 검수·기획 반환·Visual 반환을 결정한다.
- 병합 직후 live continuation state가 merge 전 기준을 가리킬 위험이 있다.

## Do not use when

- 저장소 구현이 없는 단순 설명·브레인스토밍·기획 문서 교정이다.
- 오탈자처럼 다음 작업자에게 영향을 주지 않는 L0 수정이다.
- 분야 본책이나 Roadmap을 대신하는 거대한 요약본을 만들려는 경우다.
- 미검증 내용을 확정 상태로 압축하려는 경우다.
- 승인되지 않은 프로젝트 코어·주요 플레이 규칙 변경을 Codex Build에 몰래 포함하려 한다.
- Codex에 기획 방향 또는 이미지 생성·편집을 위임하려 한다.

## Required inputs

```yaml
project_agents:
project_start_here:
documentation_map:
active_context:
current_stage_and_gate:
changed_or_target_files:
validation_results:
remaining_risks:
next_work:
invoked_skills:

codex_handoff:
  mode: CODEX_IMPLEMENTATION_HANDOFF
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
  package_contract:
  baseline_branch_and_commit:
  data_save_schema_constraints:
  required_tests:
  rollback:
```

## Read first

1. 프로젝트 `AGENTS.md`
2. 프로젝트 `START_HERE.md` 또는 current router
3. Documentation Map
4. 현재 Active Context·Decision·Requirement
5. 관련 Notion Project Home·Domain·AI/System page
6. 현재 구현에 필요한 승인 Visual record와 실제 attach/readback 상태
7. GitHub 분야 본책·실제 code/data/Scene/Resource/config/test/runtime evidence
8. 현재 branch/commit/open independent workstream
9. `docs/GPT_CODEX_WORKFLOW_POLICY.md`
10. L2 이상이면 `references/gpt-codex-implementation-handoff.md`

## Process

### 1. Authority / runtime truth 확인

실제 code·data·asset·test와 Notion/GitHub 문서 상태를 비교한다. 확인하지 못한 결과는 `[미검증]` 또는 `UNVERIFIED`로 남긴다.

Codex 인계에서는 다음 의미를 고정한다.

> Handoff는 승인된 의도·정본 위치·보호 범위·Acceptance Criteria를 전달한다. 실제 구현 상태는 최신 GitHub와 관련 Notion을 직접 다시 읽어 검증할 것. 충돌하면 임의로 덮어쓰지 말고 기술 drift / 기획 drift / visual missing을 분류하고 CHANGE_PROPOSAL 또는 GPT_VISUAL_REQUEST를 사용한다.

### 2. 상태 분리

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
- 실제로 바뀐 것
- 현재 구현·검증 상태
- 중요한 미확정·위험
- 다음 우선 작업과 선행 조건
- 변경 금지·보호 경로
- 먼저 읽을 3~7개 책임 원본
- 필요한 Codex/검증 경로

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
→ 실제 확인해야 할 code/data/Scene/Resource/test 범위
→ known problem / improvement goal
→ protected behavior / data contract
→ Acceptance Criteria
→ test/runtime/play criteria
→ high-risk / forbidden change
→ visual missing action = GPT_VISUAL_REQUEST
→ completion report fields
```

Codex는 이 Handoff 뒤 `CODEX_REHYDRATE_GITHUB_AND_NOTION`을 수행한다.

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

GPT가 이미지 제작·검수·Notion delivery를 끝내면 Codex가 해당 Notion destination을 fresh-read하고 재개한다.

### 8. 구현 범위·패키지 판정

작은 국소 변경은 단일 실행 명세로 충분할 수 있다. L2 이상·다중 의존성·여러 Scene/Schema/Resource가 얽힌 작업만 마스터 구현계획과 독립 패키지로 분해한다.

필수:

- `CORE_CONFIRMED`
- `READY_FOR_IMPLEMENTATION_HANDOFF`
- 승인된 통합 설계
- 명확한 package result/include/exclude/protected scope
- 데이터·저장·ID·Schema 보호 조건
- 기준 Branch·Commit
- required tests/runtime evidence
- rollback

차단 항목이 있으면 `BLOCKED` 또는 `UNVERIFIED`로 유지한다.

### 9. `CODEX_PREFLIGHT_OPTIONAL`

고위험·불확실·다중 의존성에서만 별도 읽기 전용 재검수를 실행한다.

```yaml
mode: PLAN_REVIEW_ONLY
file_write: FORBIDDEN
commit_push_pr_issue: FORBIDDEN
baseline_branch:
baseline_commit:
required_reading:
  github: []
  notion: []
```

Plan을 생략해도 Codex Build의 current truth 조사는 필수다.

### 10. Codex Build 결과

Codex는 승인된 구현 범위의 code/data/Scene/Resource/config/test/build/runtime를 수정하고 다음을 반환한다.

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

### 11. GPT 최종 검수

- 지정 scope / Acceptance Criteria
- 기술 개선 vs 기획 변경
- 데이터·저장 호환성
- 정상·실패·경계·회귀 test
- runtime/play evidence
- 승인된 Notion Visual만 사용했는지
- Codex image-generation 금지 준수
- 미실행 검증·위험·rollback

종료 상태:

- `PACKAGE_APPROVED`
- `PACKAGE_APPROVED_WITH_TECHNICAL_CHANGES`
- `USER_REVIEW_REQUIRED`
- `CHANGE_PROPOSAL`
- `WAITING_GPT_VISUAL`
- `REVISE`
- `BLOCKED`
- `UNVERIFIED`

### 12. `post-merge-reconcile`

`LIVE_CONTINUATION_STATE`에만 적용한다. 날짜·commit·당시 CI를 설명하는 historical snapshot을 current state로 덮어쓰지 않는다.

```text
merge
→ OBSERVE_POST_MERGE_TRUTH
→ live router stale 여부 판정
→ 필요한 최소 reconciliation
→ historical snapshot 보존
→ destination readback
```

자동 project-state writeback, 자기 SHA를 다시 쓰는 loop, 날짜가 찍힌 history의 현재화는 금지한다.

## Merge boundary

`AUTO_MERGE_AFTER_REQUIRED_CHECKS`와 `AGENT_MERGE_REQUIRED`를 유지한다.

병합 전 current HEAD, actual required checks, unresolved threads, ruleset, allowed merge method를 발견한다. `APPROVED_ITEM_INHERITS_MERGE_AUTHORITY`가 적용되는 동일 승인 범위는 추가 사용자 병합 승인을 요구하지 않는다.

다른 독립 open/draft/ready PR·branch·worktree는 read-only로 보호한다.

## Verification

- Handoff가 다른 본책의 전문 복사본이 아닌가
- GitHub + Notion 둘 다 current source로 연결되는가
- 구현 작업이 Codex Build로 라우팅되는가
- GPT가 제품 구현 owner로 되돌아가지 않는가
- Codex image generation/editing이 금지되는가
- 승인 Visual delivery/readback와 GPT visual request loop가 닫히는가
- latest branch/commit/runtime truth를 확인하는가
- `NOT_RUN`을 PASS로 승격하지 않는가
- 다른 active workstream을 침범하지 않는가

## Learning Checkpoint

실행 후 `LEARNING_LOG.md`에 현재 Gate와 결과를 남긴다. 반복 가능한 공용 패턴만 Base 승격 후보로 취급하고 프로젝트 전용 사실은 해당 프로젝트에 남긴다.