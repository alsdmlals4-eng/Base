---
name: maintaining-project-context-and-handoff
description: Use when project state must be resumed or approved planning must become a staged GPT-to-Codex Godot implementation handoff.
---

# Maintaining Project Context and Handoff

## Core principle

Active Context와 Handoff는 다른 책임 원본을 복제하는 장문 문서가 아니라 **현재 상태, 읽기 순서, 미완료 작업, 위험과 다음 책임자를 연결하는 압축 라우터**다.

GPT→Codex 인계의 기본은 `ON_DEMAND_CODEX_HANDOFF`다. GPT는 평상시 기획·조사·구조 설계뿐 아니라 승인 범위의 Godot 구현 보조·POC까지 진행할 수 있고, `USER_REQUESTED_CODEX_HANDOFF`가 발생하면 현재까지의 의도와 상태를 실행 명세로 압축한다. Codex는 이 명세를 정본 사실로 맹신하지 않고 **실제 저장소·프로젝트·Godot 상태**를 직접 확인한 뒤 구현한다.

별도 Codex Plan은 `CODEX_PREFLIGHT_OPTIONAL`이다. 고위험·불확실·다중 의존성 패키지에서만 읽기 전용 재검수로 사용하고, 명확한 저위험 패키지는 실행 명세에서 바로 Build로 갈 수 있다.

Canonical policy: `docs/GPT_CODEX_WORKFLOW_POLICY.md`

## Skill Modes

- `context-refresh`: 실제 상태·다음 작업·위험·읽기 순서를 Active Context에 압축 반영한다.
- `session-handoff`: 새 채팅·담당자·브랜치·마일스톤 경계의 재개 스냅샷을 작성한다.
- `on-demand-codex-handoff`: `USER_REQUESTED_CODEX_HANDOFF` 시 GPT의 누적 기획·구현·POC와 실제 저장소 확인 요구를 Codex 실행 명세로 압축한다.
- `implementation-package-handoff`: L2 이상·다중 의존성 구현을 마스터 구현계획과 단계별 패키지로 인계하고 선택적 Codex Plan·Build·GPT 검수·병합 게이트를 관리한다.
- `resume`: 최신 Branch·Commit·실제 파일을 다시 확인하고 중단된 패키지나 세션을 안전하게 재개한다.
- `post-merge-reconcile`: 병합으로 stale해질 수 있는 live continuation router만 새 main의 관측 사실과 재조정한다.

필요한 Mode만 실행한다. 단순 상태 갱신에서 구현 패키지 계약을 만들지 않고, 작은 Codex 인계에 대형 마스터 계획을 강제하지 않는다.

## Use when

- L1 이상 작업으로 현재 구현·검증·우선순위가 바뀌었다.
- 단계·게이트·Roadmap·다음 작업이 바뀌었다.
- 세션, 담당자, AI, 브랜치 또는 마일스톤 경계에서 인수인계가 필요하다.
- 새 채팅이 과거 대화 없이 작업을 재개해야 한다.
- Active Context가 실제 파일이나 본책과 불일치한다.
- 사용자가 Codex로 전환하거나 Codex 작업 명세·점검·개선을 요청했다.
- GPT에서 기획·구현 보조·Godot POC가 누적되어 Codex가 실제 저장소를 확인하며 통합·리팩터링·검증해야 한다.
- 전체 구현을 상위 Issue와 패키지별 Branch·PR로 나눠야 한다.
- 고위험 패키지에서 선택적 Codex Plan 보고서를 마스터 계약과 대조해야 한다.
- 구현 패키지 결과를 검수하고 다음 패키지·사용자 검수·기획 반환을 결정한다.
- 병합 직후 다음 세션이 읽을 live continuation state가 merge 전 기준을 가리킬 위험이 있다.

## Do not use when

- 저장소 상태가 바뀌지 않은 단순 설명·브레인스토밍이다.
- 오탈자처럼 다음 작업자에게 영향을 주지 않는 L0 수정이다.
- 분야 본책이나 Roadmap을 대신하는 거대한 요약본을 만들려는 경우다.
- 미검증 내용을 확정 상태로 압축하려는 경우다.
- 사용자가 Codex 전환을 요청하지 않았고 현재 GPT 작업을 계속하는 편이 더 효율적이다.
- 승인되지 않은 프로젝트 코어·주요 플레이 규칙 변경을 Codex Build에 몰래 포함하려 한다.
- Codex에 기획 방향이나 비-Godot 책임 원본 결정을 위임하려 한다.

## Required inputs

```yaml
project_agents:
project_start_here:
documentation_map:
active_context:
handoff:
current_stage_and_gate:
roadmap_issue_plan:
changed_files:
validation_results:
remaining_risks:
next_work:
invoked_skills:
codex_handoff:
  mode: ON_DEMAND_CODEX_HANDOFF
  trigger: USER_REQUESTED_CODEX_HANDOFF
  current_intent_and_behavior:
  actual_state_verification_required: true
  repository_and_project_scope: []
  godot_scope: []
  known_problems_and_improvement_goals: []
  protected_behavior_and_contracts: []
  acceptance_criteria: []
  required_tests_and_runtime_checks: []
  forbidden_or_high_risk_changes: []
  codex_preflight: CODEX_PREFLIGHT_OPTIONAL | REQUIRED_BY_RISK
implementation_handoff:
  integrated_design:
  project_core_status:
  master_implementation_plan:
  parent_implementation_issue:
  package_contract:
  baseline_branch_and_commit:
  allowed_package_branch:
  codex_plan_report:
  godot_runtime_scope:
  protected_non_godot_scope:
  data_save_schema_constraints:
  required_tests:
  merge_execution: AGENT_MERGE_REQUIRED | AUTO_MERGE_BLOCKED
```

## Read first

1. 프로젝트 `AGENTS.md`
2. 루트 `[기획서]/00_프로젝트_허브/START_HERE.md`
3. Documentation Map
4. 현재 Active Context·Handoff
5. 변경된 분야 본책과 실제 파일
6. Roadmap·Issue·Plan·검증 결과
7. Codex 인계 시 `docs/GPT_CODEX_WORKFLOW_POLICY.md`
8. L2 이상 패키지 인계 시 `references/gpt-codex-implementation-handoff.md`
9. 존재하는 경우 마스터 구현계획·현재 패키지 계약·Codex Plan 보고서

## Process

### 1. Runtime truth 확인

실제 코드·데이터·자산·테스트와 문서 상태를 비교한다. 확인하지 못한 결과는 `[미검증]` 또는 `UNVERIFIED`로 남긴다.

Codex 인계에서는 다음 문장을 계약으로 고정한다.

> 이 명세는 현재까지의 기획 의도와 예상 상태를 설명한다. 실제 구현 상태는 반드시 현재 GitHub 저장소, 로컬 프로젝트 파일 및 Godot 프로젝트를 직접 조사하여 검증할 것. 명세와 실제 구현이 충돌하면 임의로 덮어쓰지 말고 원인을 분석한 뒤 가장 안전한 개선안을 선택할 것.

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
- 사용자 체감 검수

### 3. 책임 원본 갱신

먼저 해당 분야 본책, Roadmap, Decision, Manifest와 Project Skill을 갱신한다. Active Context에 전문을 복사하지 않고 경로와 현재 차이만 기록한다.

### 4. `context-refresh`

다음만 유지한다.

- 프로젝트 한 줄 방향과 현재 단계
- 이번 작업에서 실제로 바뀐 것
- 현재 구현·검증 상태
- 가장 중요한 미확정·위험
- 다음 우선 작업과 선행 조건
- 변경 금지·보호 경로
- 먼저 읽을 3~7개 책임 원본
- 호출할 Skill과 검증 경로

### 5. `session-handoff`

```text
현재 상태
→ 이번 작업 결과
→ 남은 작업
→ 위험·미검증
→ 다음 작업자의 첫 행동
→ 검증·롤백
```

과거 대화 전체, 도구 호출 로그, 이미 본책에 반영된 전문은 포함하지 않는다.

### 5.1 `post-merge-reconcile`

이 mode는 `LIVE_CONTINUATION_STATE`에만 조건부로 적용한다. 날짜·commit·당시 CI를 설명하는 `PRE_MERGE_SNAPSHOT`과 Change Log·승인 기록은 유효한 historical snapshot이므로 현재 상태로 덮어쓰거나 자동 수정하지 않는다.

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

- `OBSERVE_POST_MERGE_TRUTH`는 merge 직후와 resume 시점의 실제 원격 상태를 다시 읽는 절차다. merge 전 예상 SHA나 PR 본문을 현재 사실로 재사용하지 않는다.
- live router가 없거나 다음 세션의 판단에 영향을 주지 않으면 이 mode를 호출하지 않는다.
- 자동 project-state writeback, 자기 자신의 SHA를 다시 쓰는 loop, 날짜가 찍힌 history의 현재화는 금지한다.
- reconciliation이 필요하지만 같은 PR에서 안전하게 갱신할 수 없으면 `IN_PROGRESS`와 다음 확인 행동만 남기고 별도 범위로 추적한다.

### 6. `on-demand-codex-handoff`

`USER_REQUESTED_CODEX_HANDOFF`가 확인되면 GPT의 작업 기록을 그대로 복사하지 않고 실행에 필요한 계약으로 압축한다.

```text
현재까지 구현된 기능과 의도
→ GitHub·프로젝트에서 확인해야 할 범위
→ Godot Scene·Script·Resource·project.godot 확인 범위
→ 현재 알려진 문제와 개선 목표
→ 반드시 유지해야 할 기존 동작·데이터 계약
→ 수정 우선순위
→ Acceptance Criteria
→ 테스트·실행·회귀 검증 조건
→ 성능·용량·구조 점검 항목
→ 임의로 크게 바꾸면 안 되는 부분
→ 완료 후 changed files·이유·남은 문제 보고
```

이 단계는 `ON_DEMAND_CODEX_HANDOFF`이며, 평상시 GPT 작업에 Codex를 자동 삽입하지 않는다.

### 7. 구현 범위·패키지 판정

작은 국소 변경은 단일 실행 명세로 충분할 수 있다. L2 이상·다중 의존성·여러 Scene/Schema/Resource가 얽힌 작업만 마스터 구현계획과 독립 패키지로 분해한다.

패키지 인계라면 다음을 확인한다.

- `CORE_CONFIRMED`
- `READY_FOR_IMPLEMENTATION_HANDOFF`
- 승인된 통합 설계 명세
- 마스터 구현계획
- 상위 구현 Issue 또는 생성 계약
- 현재 패키지 결과·포함·제외·수정 금지 범위
- 데이터·저장·ID·Schema 보호 조건
- 기준 Branch·Commit과 패키지 Branch
- 필요한 Godot·회귀 테스트

차단 항목이 있으면 `BLOCKED` 또는 `UNVERIFIED`로 유지한다.

### 8. 마스터 구현계획과 패키지 분해

전체 설계는 한 번 확정된 마스터 계획으로 유지하고 구현은 독립 검증 가능한 결과 단위로 나눈다.

```text
상위 구현 Issue
├─ 패키지 Branch / PR
├─ 패키지 Branch / PR
└─ Vertical Slice 통합 Branch / PR
```

기본 병렬성은 `SEQUENTIAL`이다. 같은 Scene·Schema·Resource를 경쟁 수정하지 않고 독립 검증 가능한 도구·자산 파이프라인만 병렬 허용한다.

Template:

- `templates/project-operations/MASTER_IMPLEMENTATION_PLAN.md`
- `templates/project-operations/IMPLEMENTATION_PACKAGE_CONTRACT.md`

### 9. `CODEX_PREFLIGHT_OPTIONAL` 읽기 전용 재검수

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
```

사용할 경우 Codex는 최신 저장소, 실제 파일, 선행 패키지, 의존성, 위험, Red → Green → Refactor, 테스트와 롤백을 조사해 `templates/project-operations/CODEX_PACKAGE_PLAN_REPORT.md` 형식으로 제출한다.

Plan을 생략해도 Codex Build의 실제 저장소·프로젝트·Godot 상태 선조사 의무는 유지한다.

### 10. 기술 개선·기획 변경 판정

- 동일한 플레이어 결과와 데이터 계약을 유지하는 구조·성능·안정성·테스트 개선은 기술 변경으로 검토한다.
- 프로젝트 코어, Core Loop, 플레이 규칙, MVP, 주요 UI·UX, 콘텐츠 의미, 승인 기능 제거, 저장 호환성 파괴는 `CHANGE_PROPOSAL`이다.
- 조작감·난이도·보상 체감·아트·연출·사운드·Vertical Slice 판단은 `USER_DECISION_REQUIRED`다.

Codex가 Plan 문서를 직접 갱신하지 않는다. 필요한 경우 GPT가 마스터 계약과 대조한 뒤 패키지 Plan·Issue·체크리스트를 갱신한다.

### 11. Codex Build 인계

```yaml
branch:
  create_or_switch: FORBIDDEN
  allowed_branch: <GPT가 지정한 패키지 Branch>
  push_target: ALLOWED_BRANCH_ONLY
commit:
  godot_runtime_files_only: true
  unrelated_changes: FORBIDDEN
  preserve_user_changes: true
  force_push: FORBIDDEN
  amend: FORBIDDEN
  independent_commits: REQUIRED
pull_request:
  create_or_update: FORBIDDEN
  merge: FORBIDDEN
```

Codex는 먼저 실제 저장소·프로젝트·Godot 상태를 조사하고, 승인 범위 안에서 Godot 런타임 구현·테스트·Commit·지정 Branch Push를 수행한다. 필요한 비-Godot 변경은 직접 수정하지 않고 GPT에 반환한다.

### 12. 구현 결과 검수와 승인 게이트

GPT는 Commit·원격 HEAD·diff·테스트 증거를 확인하고 다음으로 판정한다.

- `PACKAGE_APPROVED`
- `PACKAGE_APPROVED_WITH_TECHNICAL_CHANGES`
- `USER_REVIEW_REQUIRED`
- `CHANGE_PROPOSAL`
- `REVISE`
- `BLOCKED`
- `UNVERIFIED`

기본 병합 정책은 `AUTO_MERGE_AFTER_REQUIRED_CHECKS`와 `AGENT_MERGE_REQUIRED`다. 별도 사용자 병합 승인은 필요하지 않다.

`APPROVED_ITEM_INHERITS_MERGE_AUTHORITY`: 사용자의 명시적 승인이 완료된 항목은 동일 승인 범위의 구현·검증·PR에 병합 권한이 상속된다. 동일 범위에 대해 추가 확인·재승인·병합 승인 요청 없이 동일 HEAD, 필수 검사·독립 검토 통과, unresolved thread 0, P0/P1 없음, 열린 `USER_REVIEW_REQUIRED`·`CHANGE_PROPOSAL` 없음이 확인되면 담당 에이전트가 저장소의 허용된 방식으로 병합한다.

새 범위·새 기획 결정·새 차단 finding은 기존 승인을 확장 해석하지 않는다.

### 13. `resume`

최신 `main`, 패키지 Branch, 원격 HEAD, 마지막 승인 Commit, 실행 명세와 실제 파일을 다시 대조한다. 오래된 Plan이나 과거 대화만 그대로 실행하지 않는다.

외부 Editor/MCP runtime session을 다루는 인계에서 stale PID/session 값은 historical evidence일 뿐 current authority가 아니다. 새 실행에서 target 선택이나 mutation을 하기 전 current process, transport ownership, server registration, exact target session을 fresh-read한다. 같은 관측창의 증거가 없으면 원인을 확정하지 않고 `BLOCKED_UNVERIFIED`로 남기며, 이 Handoff는 외부 transport 복구 진단 절차를 중복 소유하지 않는다.

### 14. 콜드 스타트 검수

새 작업자가 10분 안에 다음을 찾는지 확인한다.

- 무엇을 만드는가?
- 현재 어디까지 됐는가?
- 다음 작업은 무엇인가?
- 무엇을 바꾸면 안 되는가?
- 관련 본책·Skill·실제 파일·검증은 어디인가?
- 현재 Branch·Commit·실행 명세·패키지 상태는 무엇인가?
- 사용자 결정이나 `CHANGE_PROPOSAL`이 남았는가?

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
## 검증·미검증·롤백
```

### On-demand Codex Handoff

```yaml
mode: ON_DEMAND_CODEX_HANDOFF
trigger: USER_REQUESTED_CODEX_HANDOFF
intent_and_current_behavior:
actual_state_verification_required: true
repository_and_project_scope: []
godot_scope: []
known_problems_and_improvement_goals: []
protected_behavior_and_contracts: []
priority_order: []
acceptance_criteria: []
required_tests_and_runtime_checks: []
performance_size_structure_checks: []
forbidden_or_high_risk_changes: []
codex_preflight: CODEX_PREFLIGHT_OPTIONAL
completion_report:
  changed_files_and_reasons: []
  tests_run: []
  tests_failed: []
  tests_not_run: []
  remaining_risks: []
```

### 구현 패키지 Handoff

```yaml
master_plan:
parent_issue:
package_id:
package_status:
baseline_branch:
baseline_commit:
allowed_branch:
codex_plan_status:
technical_improvements: []
change_proposals: []
user_decisions: []
changed_files: []
commit_sha:
remote_head:
tests_run: []
tests_failed: []
tests_not_run: []
package_gate:
next_package_or_action:
rollback:
```

## Definition of Ready

- [ ] 실제 변경 파일과 검증 결과를 확인했다.
- [ ] 관련 본책·Roadmap·Skill의 책임을 식별했다.
- [ ] 다음 작업과 미완료 범위가 있다.
- [ ] Codex 인계라면 `USER_REQUESTED_CODEX_HANDOFF`와 실행 명세가 있다.
- [ ] L2 이상 패키지 인계라면 프로젝트 코어·마스터 계획·패키지 계약이 승인됐다.
- [ ] `CODEX_PREFLIGHT_OPTIONAL` 사용 여부를 위험 기반으로 판정했다.
- [ ] Codex Plan을 사용하면 Plan과 Build 권한이 분리됐다.

## Definition of Done

- [ ] Active Context가 실제 상태와 일치한다.
- [ ] Handoff가 다음 작업자의 첫 행동을 명확히 한다.
- [ ] 전문 중복 없이 책임 원본을 연결한다.
- [ ] `[백업]`, `[보류]`, 제거 후보가 기본 읽기에 혼입되지 않는다.
- [ ] 콜드 스타트 질문에 답할 수 있다.
- [ ] Codex 인계에서 실제 저장소·프로젝트·Godot 상태 재조사가 요구된다.
- [ ] 구현 패키지의 Branch·Commit·Plan 사용 여부·검증·승인 상태가 추적된다.
- [ ] 기술 개선·기획 변경·사용자 판단이 구분됐다.
- [ ] 인수인계 실패나 누락을 Learning Log에 기록했다.
- [ ] `LIVE_CONTINUATION_STATE`와 `PRE_MERGE_SNAPSHOT`을 구분했고, post-merge truth 재관측 여부를 판정했다.

## Validation

- 본책과 Active Context의 상태가 충돌하지 않는가?
- 실제 파일·검증 경로가 존재하는가?
- 다음 작업의 선행 조건과 완료 기준이 명확한가?
- 새 채팅이 과거 대화 없이 작업을 시작할 수 있는가?
- 기본 읽기 문서가 과도하게 많지 않은가?
- Codex Plan을 사용했다면 파일을 수정하지 않았는가?
- Codex Build가 실제 상태를 재조사하고 지정 Branch와 Godot 범위만 수정했는가?
- Commit SHA·원격 HEAD·테스트 결과를 실제 확인했는가?
- `AGENT_MERGE_REQUIRED`와 `APPROVED_ITEM_INHERITS_MERGE_AUTHORITY` 조건을 실제 확인했는가?
- live router가 있다면 `OBSERVE_POST_MERGE_TRUTH` 뒤에만 reconciliation을 판단했는가?

## Failure conditions

- Active Context가 분야 본책의 복제본이 됨
- 과거 대화나 도구 로그 전체를 필수 컨텍스트로 만듦
- 실제 확인 없이 구현·검증 완료로 기록함
- 다음 작업·위험·보호 범위를 누락함
- 오래된 경로나 보류 문서를 기본 읽기에 남김
- 사용자가 Codex 전환을 요청하지 않았는데 모든 작업에 Codex를 강제함
- 저위험 명확 작업에 `CODEX_PREFLIGHT_OPTIONAL` Plan을 의무화함
- Codex Plan이 파일·Issue·PR을 수정함
- 기술 개선을 이유로 프로젝트 코어·MVP·플레이 규칙을 암묵 변경함
- Codex가 비-Godot 책임 원본을 수정함
- 지정 Branch 밖 Push·force push·amend
- 이미 승인된 동일 범위에 대해 추가 확인·재승인·병합 승인 요청을 반복함
- historical snapshot을 live router처럼 덮어쓰거나, post-merge reconciliation으로 자동 writeback/self-SHA loop를 만듦
- 게이트 미통과, P0/P1 잔존 또는 허용되지 않은 방식의 PR 병합

## Learning contract

다음이 발생하면 학습 기록을 갱신한다.

- 새 채팅이 핵심 상태나 다음 작업을 찾지 못함
- Active Context와 실제 파일이 반복 충돌함
- 필수 문서가 너무 많아 콜드 스타트가 느림
- 인수인계 후 동일 질문이 반복됨
- 롤백·검증 경로가 부족해 작업이 중단됨
- GPT 명세와 실제 저장소 차이가 반복 발생함
- 불필요한 Codex Plan이 반복되어 비용·지연만 증가함
- 비-Godot 파일 혼입 또는 승인 기획의 암묵 변경이 발생함
- 패키지 경계가 너무 커 회귀·롤백이 실패함
