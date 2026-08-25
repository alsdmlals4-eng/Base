# GPT–Codex 단계별 구현 인계

이 reference는 `maintaining-project-context-and-handoff`의 구현 인계 상세 절차다.

Canonical policy: `docs/GPT_CODEX_WORKFLOW_POLICY.md`

## 1. 책임 분리

```text
GPT
= 기획·조사·벤치마킹·적대적 검수·구현 명세·이미지 제작/검수·최종 결과 검수

Codex Plan
= CODEX_PREFLIGHT_OPTIONAL 읽기 전용 기술 재검수

Codex Build
= 최신 GitHub + Notion 재수화 + 승인 범위 구현·코딩·테스트·runtime evidence

사용자
= 프로젝트 방향·체감·새 기획 변경·이미지 결과 승인 결정

GitHub
= 구조화·구현 정본과 PR/병합 evidence

Notion
= 사람용 기획·Flow·시각 정본과 승인 Visual의 실제 전달 위치
```

GPT가 평상시 Godot POC/코드를 구현하고 사용자가 요청할 때만 Codex로 넘기는 과거 기본 흐름은 폐기한다. **기획만이면 GPT에서 종료할 수 있고, 실제 구현·코딩이 존재하면 Codex Build가 정상 다음 단계**다.

## 2. 구현 인계 준비

`READY_FOR_IMPLEMENTATION_HANDOFF`이고 실제 repository mutation이 필요하면 `CODEX_IMPLEMENTATION_HANDOFF`를 만든다. 별도 사용자 전환 요청은 필수가 아니다.

최소 계약:

```yaml
mode: CODEX_IMPLEMENTATION_HANDOFF
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

> 이 명세는 승인된 기획 의도·성공 기준·보호 범위와 현재 정본 위치를 설명한다. 실제 구현 상태는 반드시 최신 GitHub와 관련 Notion 정본을 직접 다시 읽어 검증할 것. 명세와 current truth가 충돌하면 임의로 덮어쓰지 말고 원인을 분류할 것. 기획 변경이 필요하면 CHANGE_PROPOSAL, 이미지가 부족하면 GPT_VISUAL_REQUEST로 반환할 것.

작은 국소 변경에는 마스터 계획·상위 Issue·별도 Codex Plan을 형식적으로 강제하지 않는다.

## 3. 인계 전 GPT Gate

GPT는 다음을 확인한 뒤 구현으로 넘긴다.

- 프로젝트 core/player promise와 현재 목표가 닫힘
- 필요한 벤치마킹·대안 비교·적대적 검토 완료
- `IMPLEMENTATION_READY`
- Notion 사람용 기획·Flow·핵심 데이터가 current
- GitHub structured contract와 충돌하지 않음
- 사용해야 할 Visual이 있다면 현재 용도로 승인되고 Notion에 실제 attach/readback됨
- Acceptance Criteria와 보호 범위 존재
- 구현 전 새 사용자 결정이 필요한 conflict가 없음

하나라도 차단되면 관련 범위를 `BLOCKED`, `USER_DECISION_REQUIRED` 또는 `WAITING_GPT_VISUAL`로 유지한다.

## 4. Codex 재수화 Gate

Codex Build의 첫 단계는 `CODEX_REHYDRATE_GITHUB_AND_NOTION`이다.

```text
exact project/repository 확인
→ current main / task branch / open independent workstream 확인
→ Project AGENTS.md / Active Context / current Decision 읽기
→ relevant Notion Project Home / Domain / AI System page 읽기
→ approved Visual record + actual attach/readback 확인
→ actual code/data/Scene/Resource/config/test/runtime 읽기
→ GPT handoff와 current truth 대조
→ protected scope / Acceptance / rollback 확인
→ BUILD
```

과거 대화·stale handoff·로컬 캐시만으로 구현하지 않는다.

## 5. 이미지 소비 Gate

### 금지

Codex는 다음을 수행하지 않는다.

- 이미지 신규 생성
- 생성형 이미지 편집·스타일 변환
- 구현 편의를 위한 임시 AI art/placeholder 생성
- 승인되지 않은 이미지의 제품 경로 사용

### 허용

현재 용도로 승인되고 Notion에 실제 upload/attach/readback된 Visual을 소비한다.

- prototype: Notion에서 prototype intended use가 명시된 `APPROVED_CANDIDATE`
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

GPT가 사용자 승인 Gate를 거쳐 이미지를 제작/편집·검수하고 Notion에 승인 상태로 attach/readback하면 Codex가 해당 destination을 다시 읽고 재개한다.

## 6. L2 이상 패키지 준비 게이트

다중 의존성·고위험·Vertical Slice 구현처럼 패키지화가 필요한 경우 다음을 확인한다.

- 프로젝트 코어와 통합 설계가 승인됨
- `READY_FOR_IMPLEMENTATION_HANDOFF`
- 마스터 구현계획 존재
- 상위 구현 Issue 존재 또는 현재 정책상 동등한 추적 단위 존재
- 현재 패키지 결과·포함·제외·수정 금지 범위 존재
- 데이터·저장·ID·Schema 보호 조건 존재
- 기준 Branch/Commit과 rollback 존재
- 테스트 명령과 runtime/play evidence 기준 존재
- 사용자 기존 변경·보호 경로 파악
- 현재 repository required checks/ruleset 발견 경로 존재

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

- 스크립트 세 개 작성
- UI 파일 모음
- 여러 의존 시스템을 동시에 변경하지만 독립 결과가 없음
- 같은 Scene·Schema를 여러 패키지가 경쟁 수정

## 8. `CODEX_PREFLIGHT_OPTIONAL` Plan

별도 Codex Plan은 다음에서만 사용한다.

- 저장·Schema·마이그레이션·플랫폼 설정 같은 고위험 변경
- GPT 명세와 실제 저장소의 drift 가능성이 큼
- 여러 패키지·Scene·공용 Resource가 얽힘
- 구현 전에 기술 대안·`CHANGE_PROPOSAL` 분리가 필요함
- 사용자가 명시적으로 Plan 검토를 요청함

사용할 경우 Codex Plan은 읽기 전용이다.

```yaml
mode: PLAN_REVIEW_ONLY
file_write: FORBIDDEN
commit_push_pr_issue: FORBIDDEN
baseline_branch:
baseline_commit:
required_reading:
  github: []
  notion: []
package_contract:
```

Plan을 생략해도 Build의 실제 GitHub+Notion 선조사는 필수다.

## 9. Plan 판정

### 기술 개선

플레이어 결과와 승인된 데이터·저장 계약을 유지하면 Codex가 승인 범위 안에서 구현하고 결과 보고에 근거를 남긴다.

### `CHANGE_PROPOSAL`

프로젝트 코어, Core Loop, 플레이 규칙, MVP, 주요 UI·UX, 콘텐츠 의미, 승인 기능 제거, 호환성 파괴가 필요하면 구현과 분리한다.

### `USER_DECISION_REQUIRED`

조작감, 난이도, 보상 체감, 아트·연출·사운드, 둘 이상의 유효한 UX 선택, Vertical Slice 승인처럼 사용자 판단이 필요한 경우 사용한다.

### `WAITING_GPT_VISUAL`

승인 이미지가 없거나 현재 용도 승인이 불명확하면 사용한다. Codex가 이미지를 대신 만들지 않는다.

## 10. Codex Build 지시

Codex Build에는 다음을 고정한다.

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
  main_direct_push: FORBIDDEN_UNLESS_CURRENT_REPOSITORY_POLICY_EXPLICITLY_ALLOWS_AND_TASK_AUTHORIZES
  force_push: FORBIDDEN
  unrelated_open_pr_mutation: FORBIDDEN
```

Codex는 지정 패키지에 필요한 코드·데이터·Scene·Resource·config·test·구현 문서를 수정할 수 있다. 과거의 `godot_runtime_files_only` 제한은 공용 기본값으로 사용하지 않는다. 단, 기획 책임 원본·프로젝트 코어·승인 결정은 `CHANGE_PROPOSAL` 없이 변경하지 않는다.

## 11. 구현 결과 검수

Codex는 다음을 반환한다.

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

GPT는 다음을 검수한다.

- 승인된 패키지 범위
- 기술 개선과 기획 변경 구분
- 데이터·저장 호환성
- 정상·실패·경계·회귀 테스트
- actual runtime/play evidence
- 승인된 Notion Visual만 사용했는지
- Codex가 이미지를 생성·편집하지 않았는지
- 미실행 검증·위험·rollback

## 12. 패키지 종료 상태

- `PACKAGE_APPROVED`
- `PACKAGE_APPROVED_WITH_TECHNICAL_CHANGES`
- `USER_REVIEW_REQUIRED`
- `CHANGE_PROPOSAL`
- `WAITING_GPT_VISUAL`
- `REVISE`
- `BLOCKED`
- `UNVERIFIED`

`PACKAGE_APPROVED*`만 다음 패키지와 병합 적격성 검토에 진입한다.

## 13. 병합 게이트

기본 정책은 `AUTO_MERGE_AFTER_REQUIRED_CHECKS`와 `AGENT_MERGE_REQUIRED`다.

`APPROVED_ITEM_INHERITS_MERGE_AUTHORITY`: 이미 사용자의 명시적 승인이 완료된 동일 범위는 추가 확인·재승인·병합 승인 요청 없이 검증 후 병합할 수 있다.

병합 전에는 **현재 repository의 실제 required checks, ruleset, merge method**를 발견한다. 공용 문서에서 과거 특정 check 이름을 영구 고정하지 않는다.

허용 조건:

- `PACKAGE_APPROVED` 또는 `PACKAGE_APPROVED_WITH_TECHNICAL_CHANGES`
- PR이 Draft가 아님
- HEAD SHA가 검수 뒤 바뀌지 않음
- 현재 Required Check 성공
- unresolved review thread 0
- current repository가 허용한 병합 방식
- `USER_REVIEW_REQUIRED`·`CHANGE_PROPOSAL`·`WAITING_GPT_VISUAL` 없음

상태:

- `AUTO_MERGE_ELIGIBLE`
- `AUTO_MERGE_ENABLED`
- `AUTO_MERGE_BLOCKED`
- `UNVERIFIED_REPOSITORY_SETTING`

## 14. GitHub 구조

L2 이상 패키지 작업의 기본 구조:

```text
상위 구현 추적 단위
├─ PKG-00 Branch / PR
├─ PKG-01 Branch / PR
├─ PKG-02 Branch / PR
└─ Vertical Slice 통합 Branch / PR
```

기본 병렬성은 `SEQUENTIAL`이다. 완전히 독립적인 작업만 병렬 허용한다. 다른 독립 open/draft/ready PR은 read-only로 보호한다.

## 15. 중단·재개

중단 시 Handoff에 다음을 남긴다.

- 마지막 승인 범위와 Commit
- GitHub/Notion 다시 읽기 경로
- 현재 패키지 상태
- Push된 Commit·테스트·runtime evidence
- 사용한 승인 Visual
- `GPT_VISUAL_REQUEST` / `WAITING_GPT_VISUAL`
- `CHANGE_PROPOSAL`·사용자 결정
- 병합 상태와 차단 원인
- 다음 첫 행동
- rollback

재개 시 최신 GitHub·Notion을 다시 대조하고 오래된 Plan이나 과거 대화만 그대로 사용하지 않는다.