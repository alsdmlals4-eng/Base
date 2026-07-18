---
name: routing-project-work-by-discipline
description: Use when a game-project request must be classified into one primary discipline, affected disciplines, work level, change type, and the smallest necessary foundation and discipline skill set before planning or implementation.
---

# Routing Project Work by Discipline

## Core principle

모든 스킬을 읽지 않는다. 현재 요청에 필요한 **주 책임 분야 1개 + 영향 분야 + 최소 foundation 스킬 + 최소 분야 스킬**만 선택한다.

## Use when

- 새 L1 이상 작업 요청을 접수했다.
- 요청이 여러 분야에 걸치거나 주 책임이 모호하다.
- 어떤 본책·스킬·검증을 먼저 읽어야 하는지 판정해야 한다.
- 새 채팅에서 프로젝트 작업을 재개한다.
- 작업 범위가 바뀌어 영향 분야와 호출 스킬을 다시 계산해야 한다.

## Do not use when

- 오탈자처럼 영향이 명백한 L0 수정이다.
- 승인된 Issue·Plan에 주 책임 분야, 영향 분야와 호출 스킬이 이미 확정돼 있고 범위가 변하지 않았다.
- 단순 설명이나 대화이며 저장소 변경·결정·검증이 발생하지 않는다.
- 전체 스킬 목록을 무조건 읽기 위한 명분으로 사용하려는 경우다.

## Required inputs

```yaml
request:
project_agents:
project_start_here:
active_context:
documentation_map:
project_skill_registry:
current_stage_and_gate:
work_contract_type: github_issue/approved_direct_request
current_issue_or_approved_request:
```

## Read first

1. 최신 사용자 지시
2. 프로젝트 루트 `AGENTS.md`
3. 루트 `[기획서]/00_프로젝트_허브/START_HERE.md`
4. Active Context와 Documentation Map
5. `SKILL_REGISTRY.json`
6. 필요한 경우에만 Registry에서 생성된 사람용 Skill Map 파생본

## Process

### 1. 작업 수준 판정

- `L0`: 오탈자·명백한 형식
- `L1`: 범위가 명확한 작은 변경
- `L2`: 시스템 선택·여러 파일 영향
- `L3`: 여러 분야·핵심 구조·장기 방향
- `L4`: 여러 프로젝트에 재사용 가능한 공용 방법

### 2. 변경 유형 판정

방향, 설정, 규칙, 밸런스, UX, 코드·데이터, 자산, 사운드, 검증, 일정, 문서·경로, 스킬, PDF·발행 중 해당 유형을 선택한다.

### 3. 분야 판정

- 최종 결정을 소유하는 분야를 `primary_discipline` 하나로 지정한다.
- 입력·산출물·검증이 영향을 받는 분야만 `affected_disciplines`에 추가한다.
- 단순히 관심이 있다는 이유로 영향 분야를 늘리지 않는다.

### 4. 스킬 선택

`SKILL_REGISTRY.json`에서 다음 순서로 선택한다.

1. 요청·변경 유형과 `trigger_tags`가 일치하는 스킬
2. `do_not_use_when`에 해당하지 않는 스킬
3. 주 책임 분야의 진입 스킬 최대 1개
4. 실제 절차에 필요한 foundation 스킬만 선택
5. 검증·발행·인수인계 스킬은 해당 단계에 도달할 때만 후속 호출

기본 규칙:

- 스킬 자동 전부 로드 금지
- 주 책임 분야 스킬 없이 관련 없는 보조 스킬만 호출 금지
- 같은 책임의 중복 스킬 동시 호출 금지
- 보류·백업·제거 후보 스킬 호출 금지

### 5. 책임 원본과 검증 연결

선택한 각 스킬에 대해 다음을 연결한다.

```text
스킬
→ 먼저 읽을 본책
→ 실제 파일·데이터·자산
→ 완료 기준
→ 검증 경로
→ 작업 종료 갱신 대상
```

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
required_docs: []
actual_paths: []
validation: []
routing_reason:
```

`deferred_skills`는 현재 단계에서는 호출하지 않지만 후속 게이트에서 필요할 수 있는 스킬이다.

## Definition of Ready

- [ ] 프로젝트와 대상 저장소가 식별됐다.
- [ ] 현재 단계와 요청 범위를 확인했다.
- [ ] 주 책임 분야가 하나다.
- [ ] 필요한 스킬만 선택했다.
- [ ] 본책·실제 경로·검증이 연결됐다.

## Definition of Done

- [ ] Issue 또는 사용자가 승인한 직접 요청·Plan에 라우팅 결과가 반영됐다.
- [ ] 호출하지 않은 스킬이 명확하다.
- [ ] 범위 변경 시 다시 라우팅할 조건이 기록됐다.
- [ ] 잘못된 라우팅이나 누락이 발견되면 Learning Log에 기록했다.

## Validation

- 새 작업자가 같은 입력으로 같은 주 책임 분야와 유사한 최소 스킬 집합을 찾을 수 있는가?
- 선택한 각 스킬이 실제 책임 원본과 파일을 가리키는가?
- 불필요한 분야·스킬이 포함되지 않았는가?
- 후속 단계 스킬이 너무 일찍 호출되지 않았는가?

## Failure conditions

- 전체 skills 폴더를 기본 컨텍스트로 읽음
- 주 책임 분야를 여러 개로 지정하고 책임을 회피함
- 트리거와 무관한 스킬을 관성적으로 호출함
- 프로젝트 스킬 대신 Base 공용 스킬만으로 프로젝트 고유 결정을 수행함
- 보류·백업 스킬을 현행 스킬처럼 호출함

## Learning contract

다음이 발생하면 스킬 학습 기록을 갱신한다.

- 주 책임 분야를 잘못 판정함
- 필요한 영향 분야나 검증을 누락함
- 불필요한 스킬을 호출해 컨텍스트가 과도해짐
- 새 반복 작업 유형에 대응할 스킬이 없음
- 동일한 라우팅 예외가 반복됨

한 번의 예외는 관찰·가설로 기록하고, 반복 검증 전에는 강제 라우팅 규칙으로 승격하지 않는다.
