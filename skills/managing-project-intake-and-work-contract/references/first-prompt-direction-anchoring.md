# First-Prompt Direction Anchoring

## Purpose

`first-prompt`는 사용자의 요청을 길게 다시 쓰는 기능이 아니다. **프롬프트 전체를 어떤 방향으로 해석하고 실행해야 하는지 결정하는 핵심 문장을 프롬프트 가장 앞에 배치**하고, 그 문장이 뒤의 계약·Context·제약·검증과 정확히 일치하는지 확인하는 intake Skill Mode다.

이 reference는 `managing-project-intake-and-work-contract`가 L1 이상 지시문을 작성할 때만 사용한다. 단순 오탈자, 명백한 형식 수정, 동일 입력의 검사 재실행은 L0 예외다.

## Authority boundary

첫 문장은 높은 주목도를 얻지만 새로운 권한을 만들지 않는다.

- 앞에 배치했다고 상위 권한이 되지 않는다.
- 사용자 최신 지시, 프로젝트 `AGENTS.md`, 승인 Decision, 책임 원본, 실제 파일과 `HARD_CONSTRAINT`를 덮어쓰지 않는다.
- “항상”, “절대”, “오직”, “반드시”는 실제 권한·안전·무결성 근거가 있을 때만 사용한다.
- 뒤쪽의 명시적 제약과 충돌하면 앞 문장을 유지하는 것이 아니라 계약을 다시 작성한다.
- 순서 효과는 품질 보조 수단이며 결과 정확성이나 모델 행동을 보장하지 않는다.
- System Blueprint의 적용 범위·노드·정본 경계는 이 reference가 새로 정의하지 않는다. 적용 가능성이 있으면 `docs/operations/project-workspace/NOTION_SYSTEM_BLUEPRINT_CONTRACT.md`로 라우팅한다.

## Required input

```yaml
request:
decision_question:
intended_outcome:
dominant_criterion:
canonical_sources: []
actual_files_and_evidence: []
known_conflicts: []
hard_constraints: []
protected_scope: []
required_output:
validation:
approval_reference:
```

## Ordering contract

```text
DIRECTION_ANCHOR
→ TASK_AND_SUCCESS
→ CONTEXT_AND_SOURCES
→ CONSTRAINTS_AND_PROTECTED_SCOPE
→ OUTPUT_AND_VALIDATION
→ OPTIONAL_RESPONSE_DIVERSIFICATION
```

### `DIRECTION_ANCHOR`

첫 1~2문장에 다음 세 요소를 압축한다.

```yaml
primary_action:
intended_outcome:
dominant_criterion:
```

좋은 anchor는 뒤의 모든 섹션이 무엇을 위해 존재하는지 설명한다.

```text
승인된 프로젝트 코어를 보존하면서 검증된 기획 공백을 닫는 실행 가능한 계획을 작성하라. 코드 변경은 기획 정합성과 사용자 승인이 확인된 뒤에만 시작한다.
```

나쁜 anchor는 범위를 과장하거나 중요한 조건을 숨긴다.

```text
프로젝트를 완벽하게 만들어라.
```

### `TASK_AND_SUCCESS`

- **Task**: 수행할 행동과 대상
- 사용자·플레이어 가치
- 성공 상태와 완료 기준
- 현재 Work Mode와 허용 권한

### `CONTEXT_AND_SOURCES`

- **Context**: 현재 결정에 필요한 맥락만 포함
- **Source**: 사용자 최신 지시, GitHub 정본, 승인 Decision, 실제 코드·데이터·자산·테스트 순으로 권한 표시
- 오래된 자료·외부 사례·AI 추론은 참고 또는 `UNVERIFIED`로 분리
- 지시와 자료가 섞이지 않도록 `### Instruction` / `### Context` 또는 명확한 delimiter를 사용
- 게임 프로젝트에서 현재 작업이 플레이어가 체감하는 연결된 시스템 로직·분기·상태·다중 시스템 흐름을 의미 있게 바꾸면, current-state/reuse-first 뒤 아래 조건부 Gate를 해결하고 Blueprint 계약을 Source/Constraint에 연결한다.

### Conditional System Blueprint entry gate

`SYSTEM_BLUEPRINT_ENTRY_CHECK_REQUIRED`

`REUSE_EXISTING_BLUEPRINT_BEFORE_CREATING_NEW`

`NO_MASS_BLUEPRINT_BACKFILL`

위 literal은 추적용 참조다. 게임 프로젝트의 현재 변경이 복잡한 연결 시스템에 해당하면 **reuse-first 이후, 구현 준비 전에** `docs/operations/project-workspace/NOTION_SYSTEM_BLUEPRINT_CONTRACT.md`를 읽고 그 owner가 정의한 적용 여부·기존 Blueprint 재사용·필요 최소 범위·Home/Detail 경계를 해결한다. 비대상이면 이유를 남긴 `NOT_APPLICABLE_WITH_REASON`으로 종료한다. 세부 Blueprint 규칙을 이 reference에 복제하지 않는다.

### `CONSTRAINTS_AND_PROTECTED_SCOPE`

- **Constraints**: 안전·권한·호환성·범위·비목표
- 보호할 기존 결정·자산·파일·Schema
- 금지 행동과 승인 필요 행동
- 중단·롤백 조건

### `OUTPUT_AND_VALIDATION`

- **Output**: 결과 형식, 상태 용어, 파일·Artifact
- **Validation**: 정상·실패·경계·회귀 검사와 실행 증거
- 실행하지 않은 항목은 `NOT_RUN` 또는 `BLOCKED_UNVERIFIED`
- 설명 산출물과 실제 구현 완료를 구분

### `OPTIONAL_RESPONSE_DIVERSIFICATION`

설계·전략·기획처럼 첫 답변이 하나의 관성적 해법으로 굳을 위험이 있을 때만 사용한다.

```text
정석안: 검증된 기본 구조와 낮은 위험
파격안: 핵심 가정을 바꾸는 높은 차별성
통합안: 두 안의 장점을 결합하되 복잡성을 통제
```

세 안은 같은 평가 기준, 같은 제약, 같은 반증 자료로 비교한다. 마지막에는 추천안·추천 이유·포기하는 이점·검증 방법을 제시한다.

다음에는 사용하지 않는다.

- 오탈자·번역·정해진 형식 변환 같은 기계적 작업
- 이미 승인된 구현 계약
- 실제로 동등한 대안이 없는 안전·법적·무결성 규칙
- 선택지를 늘리는 것이 결정 비용만 키우는 경우

## Explicit instruction structure

첫 프롬프트는 역할극 문장보다 실행 인터페이스를 우선한다.

```text
### Direction anchor
[핵심 행동 + 결과 + 지배 기준]

### Instruction
[Task / success / permissions]

### Context and Source
[정본 / 실제 파일 / 참고 / 충돌]

### Constraints
[HARD_CONSTRAINT / protected scope / exclusions]

### Output and Validation
[Output / Validation / status vocabulary]
```

“전문가처럼 행동해”만으로는 Task, Context, Source, Constraints, Output, Validation을 대체할 수 없다.

## Grill Me alignment gate

모든 L1 이상 지시문 작성은 좋은 프롬프트 변환 뒤 `Grill Me alignment gate`를 통과한다.

```text
route
→ repository facts
→ first-prompt
→ contract
→ Grill Me alignment gate
→ CONFIRMED
→ execution
```

- 의도·기획·범위·우선순위·정본 충돌이 남으면 가장 큰 결정 질문 하나씩 묻는다.
- 계약이 완전하지만 승인되지 않았다면 direction anchor와 핵심 계약을 보여 주고 한 번 승인받는다.
- exact contract already approved 상태이며 유효한 approval reference가 있으면 중복 질문하지 않는다.
- 승인되지 않은 중대한 지시문은 `AWAITING_USER_CONFIRMATION`으로 유지하고 실행하지 않는다.
- Grill Me는 사용자가 기술 세부를 대신 설계하게 만드는 절차가 아니다. 저장소와 테스트로 판정 가능한 사실은 먼저 조사한다.

## conflict scan

작성 후 다음을 순서대로 검사한다.

```yaml
anchor_matches_task:
anchor_matches_output:
source_authority_preserved:
hard_constraints_preserved:
later_instruction_conflict:
protected_scope_visible:
user_decisions_visible:
counterevidence_preserved:
alternative_criteria_symmetric:
unverified_claims_labeled:
system_blueprint_entry_resolved_if_applicable:
approval_state_valid:
```

다음 중 하나라도 실패하면 지시문을 실행하지 않고 anchor 또는 전체 계약을 수정한다.

- 첫 문장이 뒤의 범위보다 넓거나 좁다.
- 첫 문장이 제약·비목표·미검증을 사실상 무효화한다.
- Context 안의 문장이 Instruction처럼 오인될 수 있다.
- 예시가 정본보다 높은 권한을 갖는다.
- 정석안·파격안·통합안에 서로 다른 평가 기준을 적용한다.
- 적용 대상인 복잡한 게임 시스템 작업에서 Blueprint 계약 확인·기존 Blueprint 재사용 판정·필요 최소 범위가 빠져 구현 의미가 모호하다.
- Grill Me 확인 없이 기획이나 구현으로 진행한다.

## Output contract

```yaml
direction_anchor:
task_and_success:
context_and_sources:
constraints_and_protected_scope:
output_and_validation:
optional_response_diversification:
conflict_scan:
approval_state: CONFIRMED | AWAITING_USER_CONFIRMATION | REUSED_APPROVAL
approval_reference:
```

## Definition of Done

- 핵심 방향 문장이 실제 프롬프트의 첫 지시 섹션에 있다.
- Task, Context, Source, Constraints, Output, Validation이 빠짐없이 연결된다.
- 순서가 권한을 왜곡하지 않는다.
- 게임 프로젝트의 현재 작업이 `SYSTEM_BLUEPRINT_ENTRY_CHECK_REQUIRED` 적용 대상이면 기존 Blueprint 계약에서 적용 결과를 해결했고, 비대상이면 이유 있는 `NOT_APPLICABLE_WITH_REASON`으로 가볍게 종료했다.
- 필요할 때만 정석안·파격안·통합안을 생성하고 같은 기준으로 비교한다.
- conflict scan이 통과했다.
- Grill Me alignment gate 또는 기존 approval reference로 의도·기획 정합성이 확인됐다.
- 승인 전 실행하지 않았다.
