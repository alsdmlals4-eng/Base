---
name: managing-project-intake-and-work-contract
description: Use when routing a project request, closing material ambiguity, defining a work contract, or sequencing approved dependent work.
---

# Managing Project Intake and Work Contracts

## Core principle

요청 접수는 `의도 파악 → Work Mode 자동 선택 → Skill 자동 선택 → 필요한 Skill Mode 선택 → 사실 조사 → first-prompt 방향 고정 → 실행 계약 → Grill Me 정합성 확인 → 필요 시 작업 분해·순서화 → 실행 보고`인 하나의 상태 흐름이다.

사용자는 Skill 이름이나 mode를 선언할 필요가 없다. Registry trigger와 현재 작업 단계로 필요한 최소 Skill·Skill Mode를 자동 선택하고, 실제 사용 이유와 얻은 결과를 최종 보고에 남긴다.

모든 L1 이상 지시문 작성은 이 Skill에서 좋은 프롬프트 변환을 수행한 뒤 `Grill Me alignment gate`로 의도·기획·범위가 맞는지 확인한다. 유효한 승인 없이 제품·프로젝트 작업으로 진행하지 않는다.

## Terminology

- `Work Mode`: AI의 현재 작업 자세·권한·증거 기준. `PLAN / BUILD / REVIEW` 중 한 시점에 하나를 주로 사용한다.
- `Skill`: 특정 책임을 수행하는 재사용 가능한 전문 작업 계약.
- `Skill Mode`: 한 Skill 안에서 선택하는 세부 절차. 이 문서의 `route`, `first-prompt`, `clarify` 등이 해당한다.
- `Prompt`: 사용자의 현재 목표·제약·산출물. Skill 선언문이 아니다.
- `Direction anchor`: 지시문 가장 앞에서 핵심 행동·결과·지배 기준을 고정하는 1~2문장. 배치 순서는 권한을 만들지 않는다.

상세 계약: `docs/WORK_MODE_AND_SKILL_ROUTING.md`

승인 결정 복원·중복 질문 방지·GitHub·Google Sheets 동기화: `docs/CONFIRMED_DECISION_SYNC_POLICY.md`

프로젝트 GDD Google Sheets 역할·편집·시각화·수치화: `docs/PROJECT_GDD_GOOGLE_SHEETS_POLICY.md`

## Skill Modes

- `route`: 요청 의도·현재 단계·위험을 파악하고 Work Mode, 작업 수준, 변경 유형, 주 책임 분야와 최소 Skill 집합을 자동 판정한다.
- `first-prompt`: 핵심 방향 문장을 지시문 가장 앞에 배치하고 Task·Context·Source·Constraints·Output·Validation을 순서화한 뒤 전체 계약과 충돌하지 않는지 검사한다. 상세 절차는 `references/first-prompt-direction-anchoring.md`를 사용한다.
- `contract`: 확정된 요구를 범위·제외·보호·완료·검증이 있는 실행 계약으로 변환한다.
- `clarify`: 저장소에서 확인할 사실을 먼저 조사하고 사용자만 결정할 수 있는 모호성을 닫는다. 모든 L1 이상 지시문은 실행 전 `Grill Me alignment gate`를 거치며, 프로젝트 방향을 바꾸는 핵심 결정은 `references/grill-me-protocol.md`를 사용한다.
- `decompose-and-sequence`: 승인된 계약을 검증 가능한 결과 단위로 나누고 의존성·병렬화·게이트·롤백 순서를 정한다.
- `execution-report`: 실제 실행한 Work Mode·Skill·Skill Mode, 선택 이유, 수행 내용, 결과·증거·미검증을 보고한다.

하나의 호출에서 필요한 Skill Mode만 순서대로 실행한다. L1 이상 지시문 작성의 기본 순서는 `route → first-prompt → contract → clarify`다. 이미 exact contract already approved 상태이고 유효한 approval reference가 있으면 `clarify`는 승인 재사용을 기록하고 중복 질문하지 않는다. `decompose-and-sequence`는 `CONFIRMED` 이후에만 실행한다. L1 이상 작업 종료 시 `execution-report`를 실행하되 짧은 작업에서는 최종 답변의 한 섹션으로 압축할 수 있다.

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
- L1 이상 작업을 다른 에이전트·Codex·외부 AI에 넘기는 지시문도 먼저 이 Skill의 `first-prompt → contract → clarify`를 거친다.

## Use when

- 새 L1 이상 요청 또는 여러 분야에 걸친 요청을 접수한다.
- 기능·게임 경험·아트 방향·아키텍처·워크플로·Base 변경을 결정한다.
- 요청이 짧거나 모호하거나 여러 파일·산출물에 영향을 준다.
- 승인된 요구를 Issue·Goal·Plan 또는 실행 프롬프트로 넘긴다.
- GPT·Codex·외부 AI용 작업 지시문을 작성하거나 개선한다.
- 큰 작업을 단계·의존성·병렬 묶음·게이트로 분해한다.
- 범위가 바뀌어 분야·Skill·검증·실행 순서를 다시 계산한다.

## Do not use when

- 오탈자나 명확한 단일 파일 기계 수정인 L0 작업이다.
- 입력과 판정 기준이 동일한 검사를 재실행한다.
- 승인된 Plan에 분야·범위·완료·검증·실행 순서가 이미 확정됐고 범위가 변하지 않았다. 이때 기존 approval reference를 재사용한다.
- 저장소 변경·결정·검증이 없는 단순 설명이다.
- 요구가 확정되지 않았는데 구현 세부 순서부터 고정하려 한다.

## Required inputs

```yaml
request:
project_agents:
project_start_here:
active_context:
current_confirmed_decisions:
project_google_sheet:
related_open_and_recent_prs:
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
approval_reference:
```

## Read first

1. 최신 사용자 지시
2. 프로젝트 `AGENTS.md`, `START_HERE`, Active Context, Documentation Map
3. `CURRENT_CONFIRMED_DECISIONS.md`, 동일 Goal의 열린·최근 병합 PR, 프로젝트 Google Sheets
4. `docs/WORK_MODE_AND_SKILL_ROUTING.md`
5. 현재 Issue·Plan·책임 원본과 실제 파일
6. `SKILL_REGISTRY.json`
7. L1 이상 지시문 작성 시 `references/first-prompt-direction-anchoring.md`
8. 필요한 경우 `references/question-and-source-model.md`
9. 종료 판정이 필요한 경우 `references/ambiguity-and-closure.md`
10. Grill Me 정합성 확인과 핵심 결정 인터뷰가 필요한 경우 `references/grill-me-protocol.md`
11. 작업 분해·순서화가 필요한 경우 `references/work-decomposition-and-sequencing.md`

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

최신 `main`, 동일 Goal의 열린·최근 병합 PR, `CURRENT_CONFIRMED_DECISIONS.md`, 분야 책임 원본, 실제 파일과 프로젝트 Google Sheets에서 확인 가능한 것은 `repository_observed` 근거로 기록하고 사용자에게 되묻지 않는다. 외부 자료와 모델 추론은 요구사항 권한이 없으며 `[확인 필요]` 또는 후보로 남긴다.

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

### 3.1 Build the first prompt

모든 L1 이상 지시문 작성은 `references/first-prompt-direction-anchoring.md`를 사용한다.

```text
DIRECTION_ANCHOR
→ TASK_AND_SUCCESS
→ CONTEXT_AND_SOURCES
→ CONSTRAINTS_AND_PROTECTED_SCOPE
→ OUTPUT_AND_VALIDATION
→ OPTIONAL_RESPONSE_DIVERSIFICATION
→ conflict scan
```

- 핵심 행동·의도한 결과·지배 기준을 1~2문장으로 압축해 지시문 가장 앞에 둔다.
- Task, Context, Source, Constraints, Output, Validation을 명확히 분리한다.
- 정석안·파격안·통합안은 설계·결정 탐색에 실제 가치가 있을 때만 같은 기준으로 비교한다.
- 앞 문장이 전체 계약을 좁히거나 과장하거나 뒤의 `HARD_CONSTRAINT`와 충돌하면 전체 지시문을 다시 작성한다.
- first-prompt는 초안이며 아직 실행 권한이 없다.

### 3.5 Apply the neutral-recommendation-gate

권장안·판정·설계 선택이 있으면 사용자안과 AI 최초안을 같은 기준으로 비교한다.

```yaml
evaluation_criteria: []
alternatives: []
counterevidence: []
benefits_costs_and_risks: []
reversibility:
unknowns_and_evidence_limits: []
recommended_conclusion:
agreement_or_disagreement_reason:
```

- 사용자안이 검토를 통과하면 근거와 함께 동의한다.
- 다른 안이 더 강하면 차이를 만드는 증거와 함께 권장한다.
- 반대를 위한 반대를 만들지 않는다.
- 증거 부족은 `BLOCKED_UNVERIFIED`로 남긴다.
- L1 이상 기능·설계·아키텍처·정책·방향 결정은 `running-adversarial-review-and-refinement`의 `attack → validate-critique → decision-report`를 PLAN 사전판정 지원 Skill로 실행한다.
- 이 판정의 승인 finding은 `refine-approved-findings`에서 주 책임 분야 Skill BUILD로 한 번만 구현·수정하고, `regression-recheck → decision-report`로 복귀한다.

### 4. Run the Grill Me alignment gate

좋은 프롬프트 변환과 실행 계약 작성 뒤, 실행 전 `Grill Me alignment gate`로 의도·기획 정합성을 확인한다.

- 결과를 바꾸는 가장 큰 의사결정 하나씩만 묻는다.
- 기존 Decision이 유효하면 다시 묻지 않는다.
- 프로젝트 방향을 바꾸지 않는 기술 세부·초기 수치는 `RECOMMENDED_DEFAULT`, 코어·중요 기획·방향성·정본 충돌은 `USER_DECISION_REQUIRED`로 분류한다.
- 상세 요청은 처음부터 다시 인터뷰하지 않고 direction anchor와 현재 이해를 반증 가능한 문장으로 재진술한 뒤 틀리거나 빠진 부분만 확인한다.
- 계약이 완전하지만 승인되지 않았다면 direction anchor·범위·보호 대상·산출물·검증을 한 번 보여 주고 명시적 승인을 받는다.
- exact contract already approved 상태이면 approval reference를 기록하고 중복 질문 없이 `REUSED_APPROVAL`로 통과한다.
- 중대한 승인 또는 확인이 없으면 `AWAITING_USER_CONFIRMATION`을 유지하고 BUILD·위임·실행으로 이동하지 않는다.

### 5. Closure and confirmation

중대한 `NEEDS_CONFIRMATION`이 남아 있으면 `AWAITING_USER_CONFIRMATION`을 유지한다.

```text
[목표/경험]을 위해 [범위]를 수행하고, [제외·보호 대상]은 건드리지 않으며,
[산출물/검증]으로 완료를 판정한다.
```

확인 결과는 `CONFIRMED` 또는 `REUSED_APPROVAL`과 approval reference로 기록한다.

### 6. Produce the executable contract

```md
# 작업 제목
## Direction Anchor
## 목적
## Work Mode
## 맥락·정본·실제 근거
## 목표 사용자·플레이어 경험
## 작업 범위
## 제약·제외·보호 범위
## 자동 선택 Skill·Skill Mode
## 산출물
## 완료 기준
## 테스트·검증
## 먼저 읽을 문서와 파일
## 위험·의존성·롤백
## Grill Me 정합성·승인 근거
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

## Project GDD Google Sheets handling

프로젝트가 구성된 Sheet를 사용하면 이를 `USER_FACING_GDD_WORKSPACE`로 읽는다. 최신 GitHub 정본·실제 파일과 Sheet를 비교하고, Sheet에만 있는 사용자 수정은 `PROPOSED_SHEET_CHANGE`로 보존한다. 기술 기본값과 중요 기획 결정을 분리하고 승인된 변경만 GitHub 정본·Commit·Sheet에 반영한 뒤 재조회한다.

## State model

```text
RECEIVED
→ ROUTED
→ PROMPT_DRAFTED
→ READY | AWAITING_USER_CONFIRMATION
→ CONFIRMED | REUSED_APPROVAL
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
direction_anchor:
prompt_contract:
prompt_conflict_scan:
requirement_status:
approval_state:
approval_reference:
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
- 모든 L1 이상 지시문 작성에서 `first-prompt → contract → clarify`가 실행됐다.
- direction anchor가 지시문 가장 앞에 있고 전체 범위·제약·산출물과 일치한다.
- Task·Context·Source·Constraints·Output·Validation이 추적된다.
- 범위·제외·보호·완료·검증이 추적된다.
- 권장안이 있으면 사용자안과 AI 최초안에 동일한 평가 기준·대안·반증·위험·되돌리기 난이도를 적용했다.
- 필요한 사용자 확인 전에는 구현 계약이나 실행 순서를 확정하지 않았다.
- Grill Me alignment gate 또는 유효한 approval reference가 실행 전에 확인됐다.
- 기존 승인 계약에는 중복 질문하지 않았다.
- 큰 작업은 독립 검증 가능한 결과·의존성·병렬 묶음·게이트로 분해됐다.
- 실제 사용한 Work Mode·Skill·Skill Mode의 이유와 결과·증거를 보고했다.
- 새 작업자가 같은 입력에서 동등한 계약·라우팅·실행 보고를 복원할 수 있다.

## Failure conditions

- 사용자에게 Skill 이름이나 Skill Mode 선언을 요구함
- Work Mode와 Skill Mode를 같은 개념으로 혼용함
- 전체 skills 폴더를 기본 로드함
- trigger 없이 임의로 Skill을 호출함
- L1 이상 지시문을 intake·좋은 프롬프트 변환 없이 바로 작성하거나 실행함
- 핵심 방향 문장을 뒤쪽에 숨기거나 전체 계약과 다르게 작성함
- 앞 문장의 순서를 근거로 `HARD_CONSTRAINT`·정본·상위 지시를 덮어씀
- Task·Context·Source·Constraints·Output·Validation 중 필요한 항목을 누락함
- 기계적 작업에도 정석안·파격안·통합안을 강제함
- 저장소에서 확인할 사실을 사용자에게 질문함
- 주 책임 분야를 여러 개 지정함
- 상세 요청을 무시하고 포괄 질문을 반복함
- exact contract already approved인데 approval reference를 무시하고 중복 질문함
- Grill Me alignment gate 또는 유효 승인 없이 실행 계약·BUILD·위임으로 이동함
- 원 요청의 산출물을 문서로 임의 축소함
- 제외·보호·보류·미검증을 손실함
- 측정 불가능한 완료 기준만 작성함
- 활동 이름만 있는 체크리스트를 만듦
- 의존성·같은 파일 충돌·검증·롤백 없이 모든 작업을 병렬화함
- 실제로 사용하지 않은 Skill을 사용했다고 보고함
- 사용 이유·결과·증거 없이 Skill ID만 나열함
- 사용자의 선호나 AI 최초안에 근거 없이 동의함
- 적대적 검토를 반대를 위한 반대로 오용함

## Legacy aliases

- `routing-project-work-by-discipline` → `route`
- `conducting-deep-requirement-interviews` → `clarify`
- `grill-me`, `grillme`, `Grill Me` → `clarify` + `references/grill-me-protocol.md`
- `transforming-requests-into-prompts` → `first-prompt` + `contract` + `clarify`
- `[좋은 프롬프트]`, `좋은 프롬프트`, `퍼스트 프롬프트`, `first prompt` → `first-prompt` + `contract` + `clarify`

Templates:

- `templates/EXECUTABLE_PROMPT.md`
- `templates/planning/EXECUTION_SEQUENCE_PLAN.md`
- `templates/project-operations/GRILL_ME_DECISION_RECORD.md`
- `templates/project-operations/SKILL_EXECUTION_REPORT.md`

## Base v9.4 지시 권위·Context 큐레이션

L1 이상 Prompt 계약에서 강한 지시를 추가하기 전에 `HARD_CONSTRAINT / RECOMMENDED_DEFAULT / JUDGMENT_SPACE`로 권위를 분류한다. 보안·권한·데이터 무결성·비가역 변경·저장 호환성·법적 경계는 완화하지 않는다.

입력·출력·불변조건·실패조건·검증을 예시보다 먼저 정의하는 Interface-first 계약을 사용한다. 예시는 정상·실패·경계·회귀 Fixture 또는 Golden Set으로 보존한다.

Direction anchor와 first-prompt 순서화는 `references/first-prompt-direction-anchoring.md`를 따른다. Context 큐레이션은 현재 `decision_question`을 고정한 뒤 권위·freshness·representation·deduplication·known conflicts·반대 근거·`progressive_load_trigger`·`refresh_trigger`를 기록한다. 상세 Method: `docs/knowledge/game-development/AI_INSTRUCTION_AND_CONTEXT_DESIGN_METHOD.md`.
