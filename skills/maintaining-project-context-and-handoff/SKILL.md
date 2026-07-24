---
name: maintaining-project-context-and-handoff
description: Use when a game-project task changes current status, next work, risks, decisions, gates, or ownership; when a new chat or worker must resume; or when approved planning must be converted into a staged GPT-to-Codex Godot implementation handoff without duplicating canonical documents.
---

# Maintaining Project Context and Handoff

## Core principle

Active Context와 Handoff는 다른 책임 원본을 복제하는 장문 문서가 아니라 **현재 상태, 읽기 순서, 미완료 작업, 위험과 다음 책임자를 연결하는 압축 라우터**다.

GPT→Codex 구현 인계에서는 GPT가 기획·비-Godot 파일·GitHub 계약과 Plan 문서를 책임지고, Codex Plan은 읽기 전용 재검수, Codex Build는 지정 Branch의 Godot 구현만 담당한다.

Canonical policy: `docs/GPT_CODEX_WORKFLOW_POLICY.md`

## Skill Modes

- `context-refresh`: 실제 상태·다음 작업·위험·읽기 순서를 Active Context에 압축 반영한다.
- `session-handoff`: 새 채팅·담당자·브랜치·마일스톤 경계의 재개 스냅샷을 작성한다.
- `implementation-package-handoff`: 승인된 통합 설계를 마스터 구현계획과 단계별 Godot 구현 패키지로 인계하고 Codex Plan·Build·GPT 검수·사용자 승인 게이트를 관리한다.
- `resume`: 최신 Branch·Commit·실제 파일을 다시 확인하고 중단된 패키지나 세션을 안전하게 재개한다.

필요한 Mode만 실행한다. 단순 상태 갱신에서 구현 패키지 계약을 만들지 않는다.

## Use when

- L1 이상 작업으로 현재 구현·검증·우선순위가 바뀌었다.
- 단계·게이트·Roadmap·다음 작업이 바뀌었다.
- 세션, 담당자, AI, 브랜치 또는 마일스톤 경계에서 인수인계가 필요하다.
- 새 채팅이 과거 대화 없이 작업을 재개해야 한다.
- Active Context가 실제 파일이나 본책과 불일치한다.
- GPT가 기획과 비-Godot 작업을 마치고 Codex에 Godot 구현만 넘긴다.
- 전체 구현을 상위 Issue와 패키지별 Branch·PR로 나눠야 한다.
- Codex Plan 보고서를 마스터 계약과 대조하고 구현 시작 여부를 판정한다.
- 구현 패키지 결과를 검수하고 다음 패키지·사용자 검수·기획 반환을 결정한다.

## Do not use when

- 저장소 상태가 바뀌지 않은 단순 설명·브레인스토밍이다.
- 오탈자처럼 다음 작업자에게 영향을 주지 않는 L0 수정이다.
- 분야 본책이나 Roadmap을 대신하는 거대한 요약본을 만들려는 경우다.
- 미검증 내용을 확정 상태로 압축하려는 경우다.
- 프로젝트 코어·통합 설계·패키지 범위가 승인되지 않았는데 Codex Build부터 시작하려 한다.
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
  user_merge_approval:
```

## Read first

1. 프로젝트 `AGENTS.md`
2. 루트 `[기획서]/00_프로젝트_허브/START_HERE.md`
3. Documentation Map
4. 현재 Active Context·Handoff
5. 변경된 분야 본책과 실제 파일
6. Roadmap·Issue·Plan·검증 결과
7. 구현 인계 시 `docs/GPT_CODEX_WORKFLOW_POLICY.md`
8. 구현 인계 시 `references/gpt-codex-implementation-handoff.md`
9. 마스터 구현계획·현재 패키지 계약·Codex Plan 보고서

## Process

### 1. Runtime truth 확인

실제 코드·데이터·자산·테스트와 문서 상태를 비교한다. 확인하지 못한 결과는 `[미검증]` 또는 `UNVERIFIED`로 남긴다.

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

### 6. `implementation-package-handoff` 준비 게이트

다음을 확인한다.

- `CORE_CONFIRMED`
- `READY_FOR_IMPLEMENTATION_HANDOFF`
- 승인된 통합 설계 명세
- 마스터 구현계획
- 상위 구현 Issue 또는 생성 계약
- 현재 패키지 결과·포함·제외·수정 금지 범위
- 데이터·저장·ID·Schema 보호 조건
- 기준 Branch·Commit과 패키지 Branch
- Codex Plan 읽기 전용 보고 Template
- 필요한 Godot·회귀 테스트

차단 항목이 있으면 `BLOCKED` 또는 `UNVERIFIED`로 유지한다.

### 7. 마스터 구현계획과 패키지 분해

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

### 8. Codex Plan 읽기 전용 재검수

Codex Plan에 다음을 고정한다.

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

Codex는 최신 저장소, 실제 파일, 선행 패키지, 의존성, 위험, Red → Green → Refactor, 테스트와 롤백을 조사해 `templates/project-operations/CODEX_PACKAGE_PLAN_REPORT.md` 형식으로 제출한다.

### 9. 기술 개선·기획 변경 판정

- 동일한 플레이어 결과와 데이터 계약을 유지하는 구조·성능·안정성·테스트 개선은 기술 변경으로 검토한다.
- 프로젝트 코어, Core Loop, 플레이 규칙, MVP, 주요 UI·UX, 콘텐츠 의미, 승인 기능 제거, 저장 호환성 파괴는 `CHANGE_PROPOSAL`이다.
- 조작감·난이도·보상 체감·아트·연출·사운드·Vertical Slice 판단은 `USER_DECISION_REQUIRED`다.

Codex가 Plan 문서를 직접 갱신하지 않는다. GPT가 마스터 계약과 대조한 뒤 패키지 Plan·Issue·체크리스트를 갱신하고 `READY_FOR_BUILD`를 판정한다.

### 10. Codex Build 인계

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

Codex는 Godot 런타임 구현·테스트·Commit·지정 Branch Push를 수행한다. 필요한 비-Godot 변경은 직접 수정하지 않고 GPT에 반환한다.

### 11. 구현 결과 검수와 승인 게이트

GPT는 Commit·원격 HEAD·diff·테스트 증거를 확인하고 다음으로 판정한다.

- `PACKAGE_APPROVED`
- `PACKAGE_APPROVED_WITH_TECHNICAL_CHANGES`
- `USER_REVIEW_REQUIRED`
- `CHANGE_PROPOSAL`
- `REVISE`
- `BLOCKED`
- `UNVERIFIED`

사용자의 명시적 승인 전에는 PR을 병합하지 않는다.

### 12. `resume`

최신 `main`, 패키지 Branch, 원격 HEAD, 마지막 승인 Commit, Plan과 실제 파일을 다시 대조한다. 오래된 Plan을 그대로 실행하지 않는다.

### 13. 콜드 스타트 검수

새 작업자가 10분 안에 다음을 찾는지 확인한다.

- 무엇을 만드는가?
- 현재 어디까지 됐는가?
- 다음 작업은 무엇인가?
- 무엇을 바꾸면 안 되는가?
- 관련 본책·Skill·실제 파일·검증은 어디인가?
- 현재 패키지·Branch·Commit·Plan 상태는 무엇인가?
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
- [ ] 구현 인계라면 프로젝트 코어·마스터 계획·패키지 계약이 승인됐다.
- [ ] Codex Plan과 Build 권한이 분리됐다.

## Definition of Done

- [ ] Active Context가 실제 상태와 일치한다.
- [ ] Handoff가 다음 작업자의 첫 행동을 명확히 한다.
- [ ] 전문 중복 없이 책임 원본을 연결한다.
- [ ] `[백업]`, `[보류]`, 제거 후보가 기본 읽기에 혼입되지 않는다.
- [ ] 콜드 스타트 질문에 답할 수 있다.
- [ ] 구현 패키지의 Branch·Commit·Plan·검증·승인 상태가 추적된다.
- [ ] 기술 개선·기획 변경·사용자 판단이 구분됐다.
- [ ] 인수인계 실패나 누락을 Learning Log에 기록했다.

## Validation

- 본책과 Active Context의 상태가 충돌하지 않는가?
- 실제 파일·검증 경로가 존재하는가?
- 다음 작업의 선행 조건과 완료 기준이 명확한가?
- 새 채팅이 과거 대화 없이 작업을 시작할 수 있는가?
- 기본 읽기 문서가 과도하게 많지 않은가?
- Codex Plan이 파일을 수정하지 않았는가?
- Codex Build가 지정 Branch와 Godot 범위만 수정했는가?
- Commit SHA·원격 HEAD·테스트 결과를 실제 확인했는가?
- 사용자 승인 전 PR을 병합하지 않았는가?

## Failure conditions

- Active Context가 분야 본책의 복제본이 됨
- 과거 대화나 도구 로그 전체를 필수 컨텍스트로 만듦
- 실제 확인 없이 구현·검증 완료로 기록함
- 다음 작업·위험·보호 범위를 누락함
- 오래된 경로나 보류 문서를 기본 읽기에 남김
- 승인 전 Codex Build 시작
- Codex Plan이 파일·Issue·PR을 수정함
- 기술 개선을 이유로 프로젝트 코어·MVP·플레이 규칙을 암묵 변경함
- Codex가 비-Godot 책임 원본을 수정함
- 지정 Branch 밖 Push·force push·amend·PR 병합
- 사용자 승인 전 PR 병합

## Learning contract

다음이 발생하면 학습 기록을 갱신한다.

- 새 채팅이 핵심 상태나 다음 작업을 찾지 못함
- Active Context와 실제 파일이 반복 충돌함
- 필수 문서가 너무 많아 콜드 스타트가 느림
- 인수인계 후 동일 질문이 반복됨
- 롤백·검증 경로가 부족해 작업이 중단됨
- Codex Plan과 실제 구현의 차이가 반복 발생함
- 비-Godot 파일 혼입 또는 승인 기획의 암묵 변경이 발생함
- 패키지 경계가 너무 커 회귀·롤백이 실패함
