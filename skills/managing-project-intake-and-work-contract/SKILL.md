---
name: managing-project-intake-and-work-contract
description: Use when a project request must be routed, repository facts must be separated from user decisions, material ambiguity must be closed, a confirmed request must become an executable work contract, or approved work must be decomposed into dependency-aware execution steps.
---

# Managing Project Intake and Work Contracts

## Core principle

요청 접수는 `라우팅 → 사실 조사 → 필요한 확인 → 실행 계약 → 필요한 경우 작업 분해·순서화`인 하나의 상태 흐름이다. 같은 요청을 여러 Foundation 스킬에 다시 설명하거나 작업 수준·범위·검증·순서를 중복 판정하지 않는다.

## Modes

- `route`: 작업 수준, 변경 유형, 주 책임 분야, 영향 분야와 최소 스킬 집합을 판정한다.
- `clarify`: 저장소에서 확인할 사실을 먼저 조사하고 사용자만 결정할 수 있는 모호성을 닫는다.
- `contract`: 확정된 요구를 범위·제외·보호·완료·검증이 있는 실행 계약으로 변환한다.
- `decompose-and-sequence`: 승인된 계약을 검증 가능한 결과 단위로 나누고 의존성·병렬화·게이트·롤백 순서를 정한다.

하나의 호출에서 필요한 모드만 순서대로 실행한다. 이미 확정된 단계는 반복하지 않는다. `decompose-and-sequence`는 요구 확인을 대신하지 않으며 `CONFIRMED` 이후에만 실행한다.

## Use when

- 새 L1 이상 요청 또는 여러 분야에 걸친 요청을 접수한다.
- 기능·게임 경험·아트 방향·아키텍처·워크플로·Base 변경을 결정한다.
- 요청이 짧거나 모호하거나 여러 파일·산출물에 영향을 준다.
- 승인된 요구를 Issue·Goal·Plan 또는 실행 프롬프트로 넘겨야 한다.
- 큰 작업을 단계·의존성·병렬 묶음·게이트로 분해해야 한다.
- 범위가 바뀌어 분야·스킬·검증·실행 순서를 다시 계산해야 한다.

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
3. 현재 Issue·Plan·책임 원본과 실제 파일
4. `SKILL_REGISTRY.json`
5. 필요한 경우 `references/question-and-source-model.md`
6. 종료 판정이 필요한 경우 `references/ambiguity-and-closure.md`
7. 작업 분해·순서화가 필요한 경우 `references/work-decomposition-and-sequencing.md`

## Workflow

### 1. Route once

- `L0`: 오탈자·명백한 형식
- `L1`: 범위가 명확한 작은 변경
- `L2`: 시스템 선택·여러 파일 영향
- `L3`: 여러 분야·핵심 구조·장기 방향
- `L4`: 여러 프로젝트에 재사용 가능한 공용 방법

최종 결정을 소유하는 `primary_discipline`은 하나만 지정한다. 실제 입력·산출물·검증이 바뀌는 분야만 `affected_disciplines`에 추가한다.

Registry에서 trigger가 일치하고 비사용 조건에 걸리지 않는 최소 집합만 선택한다. 주 책임 분야 스킬은 최대 하나이며, 발행·검증·Handoff 스킬은 해당 단계에 도달할 때까지 `deferred_skills`에 둔다.

### 2. Inspect repository facts

현재 파일·경로·호출·데이터·테스트에서 확인 가능한 것은 `repository_observed` 근거로 기록하고 사용자에게 되묻지 않는다. 외부 자료와 모델 추론은 요구사항 권한이 없으며 `[확인 필요]` 또는 후보로 남긴다.

### 3. Build one requirement model

다음을 한 번만 구조화한다.

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

중대한 `NEEDS_CONFIRMATION`이 남아 있으면 `AWAITING_USER_CONFIRMATION`을 유지한다. 마지막에는 다음을 한 문장으로 재진술하고 명시적 확인을 받는다.

```text
[목표/경험]을 위해 [범위]를 수행하고, [제외·보호 대상]은 건드리지 않으며,
[산출물/검증]으로 완료를 판정한다.
```

### 6. Produce the executable contract

확인된 요구를 다음 구조로 작성한다.

```md
# 작업 제목
## 목적
## 맥락
## 목표 사용자·플레이어 경험
## 작업 범위
## 제약·제외·보호 범위
## 산출물
## 완료 기준
## 테스트·검증
## 먼저 읽을 문서와 파일
## 위험·의존성·롤백
## 작업 후 보고
```

인터뷰 기록의 제외·보호·보류·미검증을 누락하거나 새 요구를 발명하지 않는다.

### 7. Decompose and sequence

승인 계약을 활동 목록이 아니라 **검증 가능한 결과 단위**로 나눈다.

각 단계:

```yaml
step_id:
outcome:
why_now:
inputs:
files_or_systems:
owner_or_skill:
dependencies:
parallel_with:
protected_scope:
output:
acceptance_criteria:
validation:
rollback:
```

의존성은 `BLOCKS / INFORMS / USES_OUTPUT / SHARES_RESOURCE / VALIDATES / OPTIONAL_FOLLOWUP`으로 구분한다.

기본 순서:

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

순서는 의존성 해소, 위험 감소, 사용자 가치, 피드백 속도, 되돌리기 난이도, 자원 충돌로 결정한다. 일정 숫자를 근거 없이 발명하지 않는다.

병렬화는 입력·출력 경계가 고정되고 같은 파일·Schema·자산을 경쟁적으로 수정하지 않으며 독립 검증이 가능할 때만 허용한다.

각 작업 묶음 끝에는 진입 조건, 종료 증거, 실패·미검증 시 재계획을 둔다. 새 사실이 생기면 이후 단계를 자동 유지하지 않는다.

## State model

```text
RECEIVED
→ ROUTED
→ READY | AWAITING_USER_CONFIRMATION
→ CONFIRMED
→ CONTRACT_READY
→ EXECUTION_PLAN_READY
→ SUPERSEDED | ABANDONED
```

프로젝트가 인터뷰 Registry를 사용하는 경우 기존 `IN_PROGRESS`, `AWAITING_USER_CONFIRMATION`, `CONFIRMED`, `SUPERSEDED`, `ABANDONED` 값과 매핑한다. `EXECUTION_PLAN_READY`는 계약 이후의 파생 상태이며 원 요구 승인 상태를 바꾸지 않는다.

## Output contract

```yaml
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
remaining_unknowns: []
```

## Definition of Done

- 같은 요청의 수준·분야·범위를 여러 스킬에서 다시 판정하지 않았다.
- 저장소 사실과 사용자 판단이 구분됐다.
- 주 책임 분야와 최소 스킬 집합이 명확하다.
- 범위·제외·보호·완료·검증이 추적된다.
- 필요한 사용자 확인 전에는 구현 계약이나 실행 순서를 확정하지 않았다.
- 큰 작업은 독립 검증 가능한 결과·의존성·병렬 묶음·게이트로 분해됐다.
- 위험한 불확실성과 핵심 가치가 장식·후처리보다 앞에 배치됐다.
- 새 작업자가 같은 입력에서 동등한 계약과 실행 순서를 복원할 수 있다.

## Failure conditions

- 전체 skills 폴더를 기본 로드함
- 저장소에서 확인할 사실을 사용자에게 질문함
- 주 책임 분야를 여러 개 지정함
- 상세 요청을 무시하고 포괄 질문을 반복함
- 사용자 확인 전 실행 계약이나 구현 순서로 이동함
- 원 요청의 산출물을 문서로 임의 축소함
- 제외·보호·보류·미검증을 손실함
- 측정 불가능한 완료 기준만 작성함
- “코딩”, “문서 수정” 같은 동사만 있는 체크리스트를 만듦
- 의존성·같은 파일 충돌·검증·롤백 없이 모든 작업을 병렬화함
- 쉬운 장식 작업을 가장 위험한 가설과 핵심 경로보다 먼저 배치함
- 선행 단계 실패 후 이후 계획을 그대로 실행함

## Legacy aliases

다음 이전 Skill ID는 이 스킬의 모드로 흡수됐다.

- `routing-project-work-by-discipline` → `route`
- `conducting-deep-requirement-interviews` → `clarify`
- `transforming-requests-into-prompts` → `contract`

Templates:

- `templates/EXECUTABLE_PROMPT.md`
- `templates/planning/EXECUTION_SEQUENCE_PLAN.md`
