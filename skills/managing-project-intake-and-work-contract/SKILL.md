---
name: managing-project-intake-and-work-contract
description: Use automatically when a project request must be routed, repository facts must be separated from user decisions, material ambiguity must be closed, a confirmed request must become an executable work contract, or approved work must be decomposed into dependency-aware execution steps.
---

# Managing Project Intake and Work Contracts

## Core principle

요청 접수는 `의도 파악 → Work Mode 자동 선택 → Skill 자동 선택 → 필요한 Skill Mode 선택 → 사실 조사 → 필요한 확인 → 실행 계약 → 필요 시 작업 분해·순서화 → 실행 보고`인 하나의 상태 흐름이다.

사용자는 Skill 이름이나 mode를 선언할 필요가 없다. Registry trigger와 현재 작업 단계로 필요한 최소 Skill·Skill Mode를 자동 선택하고, 실제 사용 이유와 얻은 결과를 최종 보고에 남긴다.

## Terminology

- `Work Mode`: AI의 현재 작업 자세·권한·증거 기준. `PLAN / BUILD / REVIEW` 중 한 시점에 하나를 주로 사용한다.
- `Skill`: 특정 책임을 수행하는 재사용 가능한 전문 작업 계약.
- `Skill Mode`: 한 Skill 안에서 선택하는 세부 절차. 이 문서의 `route`, `clarify` 등이 해당한다.
- `Prompt`: 사용자의 현재 목표·제약·산출물. Skill 선언문이 아니다.

상세 계약: `docs/WORK_MODE_AND_SKILL_ROUTING.md`

## Skill Modes

- `route`: 요청 의도·현재 단계·위험을 파악하고 Work Mode, 작업 수준, 변경 유형, 주 책임 분야와 최소 Skill 집합을 자동 판정한다.
- `clarify`: 저장소에서 확인할 사실을 먼저 조사하고 사용자만 결정할 수 있는 모호성을 닫는다. 프로젝트 방향을 바꾸는 핵심 결정은 `skills/managing-project-intake-and-work-contract/references/grill-me-protocol.md`를 사용한다.
- `contract`: 확정된 요구를 범위·제외·보호·완료·검증이 있는 실행 계약으로 변환한다.
- `decompose-and-sequence`: 승인된 계약을 검증 가능한 결과 단위로 나누고 의존성·병렬화·게이트·롤백 순서를 정한다.
- `execution-report`: 실제 실행한 Work Mode·Skill·Skill Mode, 선택 이유, 수행 내용, 결과·증거·미검증을 보고한다.

하나의 호출에서 필요한 Skill Mode만 순서대로 실행한다. 이미 확정된 단계는 반복하지 않는다. `decompose-and-sequence`는 `CONFIRMED` 이후에만 실행한다. L1 이상 작업 종료 시 `execution-report`를 실행하되 짧은 작업에서는 최종 답변의 한 섹션으로 압축할 수 있다.

## Work Mode selection

### `PLAN`

- 요구·근거·설계·정본·작업 순서를 확정한다.
- 읽기·조사·제안이 기본이며 승인 전 제품 동작·구조를 변경하지 않는다.

### `BUILD`

- 승인된 계약 범위의 코드·데이터·문서·자산을 구현한다.
- 단계별 검증·롤백을 유지한다.

### `REVIEW`

- 결과를 적대적으로 검토하고 반례·회귀·증거를 찾는다.
- 기본 읽기 전용이다. 수정까지 요청되거나 승인된 finding이 있으면 `BUILD`로 전환해 최소 수정하고 다시 `REVIEW`로 검증한다.

복합 작업은 `PLAN → BUILD → REVIEW`로 전환할 수 있지만 한 시점의 주 Work Mode는 하나다.

## Automatic selection policy

- 사용자가 Skill·Skill Mode를 언급하지 않아도 현재 요청과 Registry trigger를 비교한다.
- `load_by_default=false`는 자동 선택 금지가 아니라 trigger 불일치 시 읽지 않는다는 뜻이다.
- trigger가 일치하고 `do_not_use_when`에 걸리지 않는 최소 집합만 사용한다.
- 주 책임 분야 Skill은 최대 하나다. Foundation·검증·발행·Handoff는 현재 단계에 필요한 것만 추가한다.
- 사용자에게 “어떤 Skill을 쓸까요?”라고 선택을 전가하지 않는다.
- 사용자가 Skill을 지정해도 trigger·권한·비사용 조건과 충돌하면 그대로 실행하지 않고 이유를 설명한다.
- 새 범위·실패·정본 변경이 생기면 Work Mode와 Skill 라우팅을 다시 계산한다.
- Skill 파일을 읽은 것과 Skill 절차를 실제 실행한 것을 구분한다.

## Use when

- 새 L1 이상 요청 또는 여러 분야에 걸친 요청을 접수한다.
- 기능·게임 경험·아트 방향·아키텍처·워크플로·Base 변경을 결정한다.
- 요청이 짧거나 모호하거나 여러 파일·산출물에 영향을 준다.
- 승인된 요구를 Issue·Goal·Plan 또는 실행 프롬프트로 넘긴다.
- 큰 작업을 단계·의존성·병렬 묶음·게이트로 분해한다.
- 범위가 바뀌어 분야·Skill·검증·실행 순서를 다시 계산한다.

## Do not use when

- 오탈자나 명확한 단일 파일 기계 수정이다.
- 입력과 판정 기준이 같은 검사를 재실행한다.
- 승인된 Plan에 분야·범위·완료·검증·실행 순서가 이미 확정됐고 범위가 변하지 않았다.
- 저장소 변경·결정·검증이 없는 단순 설명이다.
- 요구가 확정되지 않았는데 구현 세부 순서부터 고정하려 한다.

## Required inputs

```yaml
request:
project_agents:
project_start_here:
active_context:
documentation_map:
design_document_registry:
skill_registry:
current_stage_and_gate:
current_issue_or_approved_request:
actual_code_data_assets_tests:
delivery_constraints:
known_dependencies_and_blockers:
available_people_tools_permissions:
external_deliveries:
milestone_or_deadline:
validation_environment:
rollback_constraints:
```

## Read first

1. 최신 사용자 지시
2. 프로젝트 `AGENTS.md`, `START_HERE`, Active Context, Documentation Map
3. `docs/WORK_MODE_AND_SKILL_ROUTING.md`
4. 현재 Issue·Plan·책임 원본과 실제 파일
5. `SKILL_REGISTRY.json`
6. 필요한 경우 `references/question-and-source-model.md`
7. 종료 판정이 필요한 경우 `references/ambiguity-and-closure.md`
8. Grill Me 핵심 결정 인터뷰가 필요한 경우 `references/grill-me-protocol.md`
9. 작업 분해·순서화가 필요한 경우 `references/work-decomposition-and-sequencing.md`

## Workflow

### 1. Route automatically once

- `L0`: 오탈자·명백한 형식
- `L1`: 범위가 명확한 작은 변경
- `L2`: 시스템 선택·여러 파일 영향
- `L3`: 여러 분야·핵심 구조·장기 방향
- `L4`: 여러 프로젝트에 재사용 가능한 공용 방법

최종 결정을 소유하는 `primary_discipline`은 하나만 지정한다. 실제 입력·산출물·검증이 바뀌는 분야만 `affected_disciplines`에 추가한다.

```text
요청 의도·현재 단계·위험
→ PLAN / BUILD / REVIEW
→ Registry trigger·do_not_use_when
→ 최소 Skill 집합
→ 각 Skill의 필요한 Skill Mode
```

발행·검증·Handoff Skill은 해당 단계에 도달할 때까지 `deferred_skills`에 둔다.

### 2. Inspect repository facts

현재 파일·경로·호출·데이터·테스트에서 확인 가능한 것은 `repository_observed` 근거로 기록하고 사용자에게 되묻지 않는다. 외부 자료와 모델 추론은 요구사항 권한이 없으며 `[확인 필요]` 또는 후보로 남긴다.

### 3. Build one requirement model

```text
원 요청
→ 문제·목적
→ 사용자·플레이어 경험
→ 범위·비목표
→ 제약·보호 대상
→ 산출물
→ 완료 기준
→ 검증
→ 미검증·보류
```

### 4. Ask only material user decisions

결과를 바꾸는 가장 큰 의사결정 하나씩만 묻는다. 상세 요청은 처음부터 다시 인터뷰하지 않고 현재 이해를 반증 가능한 문장으로 재진술한 뒤 틀리거나 빠진 부분만 확인한다.

### 5. Closure and confirmation

중대한 `NEEDS_CONFIRMATION`이 남아 있으면 `AWAITING_USER_CONFIRMATION`을 유지한다.

```text
[목표/경험]을 위해 [범위]를 수행하고, [제외·보호 대상]은 건드리지 않으며,
[산출물/검증]으로 완료를 판정한다.
```

### 6. Produce the executable contract

```md
# 작업 제목
## 목적
## Work Mode
## 맥락
## 목표 사용자·플레이어 경험
## 작업 범위
## 제약·제외·보호 범위
## 자동 선택 Skill·Skill Mode
## 산출물
## 완료 기준
## 테스트·검증
## 먼저 읽을 문서와 파일
## 위험·의존성·롤백
## 작업 후 Skill 실행 보고
```

### 7. Decompose and sequence

승인 계약을 활동 목록이 아니라 검증 가능한 결과 단위로 나눈다.

```yaml
step_id:
outcome:
why_now:
work_mode:
inputs:
files_or_systems:
owner_or_skill:
skill_mode:
dependencies:
parallel_with:
protected_scope:
output:
acceptance_criteria:
validation:
rollback:
```

의존성은 `BLOCKS / INFORMS / USES_OUTPUT / SHARES_RESOURCE / VALIDATES / OPTIONAL_FOLLOWUP`으로 구분한다.

```text
환경·권한·입력 선행 조건
→ 정본·인터페이스·Schema 계약
→ 가장 위험한 가설·기술 불확실성
→ 핵심 사용자·플레이어 경로
→ 데이터·자산·인접 시스템 통합
→ 정상·실패·경계·회귀 검증
→ 문서·발행·참조 최신성
→ 사용자 체감 검수·통합·인수인계
```

순서는 의존성 해소, 위험 감소, 사용자 가치, 피드백 속도, 되돌리기 난이도, 자원 충돌로 결정한다. 일정 숫자를 근거 없이 발명하지 않는다. 병렬화는 입력·출력 경계가 고정되고 같은 파일·Schema·자산을 경쟁적으로 수정하지 않으며 독립 검증이 가능할 때만 허용한다.

### 8. Report execution

실제로 실행한 항목마다 다음을 남긴다.

```yaml
work_mode:
skill_id:
skill_mode:
selection: automatic | user-directed
trigger_and_reason:
work_performed:
result:
evidence:
status: PASS/PARTIAL/FAIL/UNVERIFIED
```

최종 사용자 보고에는 최소한 다음이 있어야 한다.

```text
사용한 Work Mode·Skill·Skill Mode
→ 사용한 이유
→ 얻은 결과·증거
```

중요 후보를 사용하지 않았으면 `trigger 불일치 / 비사용 조건 / 현재 단계 아님 / 도구·입력 없음` 중 하나로 이유를 기록한다. 모든 Registry 항목을 나열하지 않는다.

템플릿: `templates/project-operations/SKILL_EXECUTION_REPORT.md`

## State model

```text
RECEIVED
→ ROUTED
→ READY | AWAITING_USER_CONFIRMATION
→ CONFIRMED
→ CONTRACT_READY
→ EXECUTION_PLAN_READY
→ EXECUTED
→ REPORTED
→ SUPERSEDED | ABANDONED
```

## Output contract

```yaml
work_mode:
work_level:
change_types: []
primary_discipline:
affected_disciplines: []
foundation_skills: []
discipline_skills: []
deferred_skills: []
read_first: []
actual_paths: []
requirement_status:
user_confirmation_ref:
work_contract_path:
execution_sequence_path:
steps: []
dependencies: []
parallel_batches: []
gates: []
validation: []
skill_execution_report:
  - work_mode:
    skill_id:
    skill_mode:
    selection:
    trigger_and_reason:
    result:
    evidence:
    status:
remaining_unknowns: []
```

## Definition of Done

- 사용자가 Skill을 선언하지 않아도 trigger 기반으로 Work Mode·최소 Skill·Skill Mode를 자동 선택했다.
- 같은 요청의 수준·분야·범위를 여러 Skill에서 다시 판정하지 않았다.
- 저장소 사실과 사용자 판단이 구분됐다.
- 범위·제외·보호·완료·검증이 추적된다.
- 필요한 사용자 확인 전에는 구현 계약이나 실행 순서를 확정하지 않았다.
- 큰 작업은 독립 검증 가능한 결과·의존성·병렬 묶음·게이트로 분해됐다.
- 실제 사용한 Work Mode·Skill·Skill Mode의 이유와 결과·증거를 보고했다.
- 새 작업자가 같은 입력에서 동등한 계약·라우팅·실행 보고를 복원할 수 있다.

## Failure conditions

- 사용자에게 Skill 이름이나 Skill Mode 선언을 요구함
- Work Mode와 Skill Mode를 같은 개념으로 혼용함
- 전체 skills 폴더를 기본 로드함
- trigger 없이 임의로 Skill을 호출함
- 저장소에서 확인할 사실을 사용자에게 질문함
- 주 책임 분야를 여러 개 지정함
- 상세 요청을 무시하고 포괄 질문을 반복함
- 사용자 확인 전 실행 계약이나 구현 순서로 이동함
- 원 요청의 산출물을 문서로 임의 축소함
- 제외·보호·보류·미검증을 손실함
- 측정 불가능한 완료 기준만 작성함
- 활동 이름만 있는 체크리스트를 만듦
- 의존성·같은 파일 충돌·검증·롤백 없이 모든 작업을 병렬화함
- 실제로 사용하지 않은 Skill을 사용했다고 보고함
- 사용 이유·결과·증거 없이 Skill ID만 나열함

## Legacy aliases

- `routing-project-work-by-discipline` → `route`
- `conducting-deep-requirement-interviews` → `clarify`
- `grill-me`, `grillme`, `Grill Me` → `clarify` + `references/grill-me-protocol.md`
- `transforming-requests-into-prompts` → `contract`

Templates:

- `templates/EXECUTABLE_PROMPT.md`
- `templates/planning/EXECUTION_SEQUENCE_PLAN.md`
- `templates/project-operations/GRILL_ME_DECISION_RECORD.md`
- `templates/project-operations/SKILL_EXECUTION_REPORT.md`
