---
name: establishing-project-core
description: Use in PLAN work when a new or changing project needs its identity-defining player promise, core actions, core loop, system anchors, invariants, changeable shell, and required technical foundations proposed, stress-tested, explicitly approved, and recorded as the project core contract.
---

# Establishing Project Core

## Core principle

프로젝트 코어 확정은 아이디어를 많이 고르는 작업이 아니라 앞으로의 기획·구현·검수에서 보호할 최소 정체성 계약을 정하는 작업이다.

AI나 작업자가 스스로 코어를 확정하지 않는다. 근거를 바탕으로 제안하고 반례를 검사한 뒤 사용자의 명시적 승인을 받아야 `CORE_CONFIRMED`로 전환한다.

## Responsibility boundary

| 작업 | 책임 |
|---|---|
| 기존 프로젝트의 코어 사실 판정 | `identifying-project-core` |
| 핵심 컨셉·뾰족한 재미·제약·PoC 탐색 | `analyzing-and-refining-game-concepts` |
| 코어 제안·경계·불변 조건·승인 계약 | 이 Skill |
| 승인된 계약의 기획서 기록·발행 | `managing-design-documents` |
| 실제 구현 변경 검증 | `reviewing-and-validating-project-changes` |
| 변경안 공격·비평·개선 | `running-adversarial-review-and-refinement` |

## Work Mode and Skill Modes

기본 Work Mode는 `PLAN`이다.

- `propose`: 코어 후보와 최소 정체성 계약을 작성한다.
- `stress-test`: 제거·대체·실패·확장 반례로 후보를 공격한다.
- `confirm`: 사용자 승인·수정·기각을 기록한다.
- `lock`: 승인된 코어를 책임 원본·게이트·검수 기준에 연결한다.
- `reopen`: 새 근거 또는 명시적 방향 변경 요청이 있을 때 재검토한다.

`confirm`과 `lock`은 명시적 사용자 승인 없이 실행하지 않는다. 문서 변경은 `BUILD` 권한과 `managing-design-documents` 계약으로 수행한다.

## Required inputs

```yaml
project_goal_and_problem:
target_player_and_context:
candidate_core_concept:
pointed_fun_and_player_promise:
candidate_core_actions_and_choices:
candidate_core_loop:
major_system_relationships:
world_visual_tone_invariants:
technical_foundations:
constraints_and_production_capacity:
mvp_and_poc_evidence:
identified_existing_core:
alternatives_and_rejected_directions:
approval_authority:
```

## Core contract

### 정체성

- 프로젝트를 한 문장으로 설명하는 약속
- 대상 플레이어와 플레이 상황
- 다른 프로젝트와 구분되는 원리
- 바뀌면 다른 프로젝트가 되는 경계

### 핵심 경험

- 반복해서 보는 것
- 반복해서 판단·선택하는 것
- 반복해서 행동하는 것
- 행동 직후 받는 피드백
- 다음 행동을 부르는 동기
- 반드시 지켜야 할 감정·판타지

### 시스템 코어

- 코어 루프
- 주요 시스템의 입력·출력
- 상태와 가치가 변화하는 지점
- 판매·활용·전투·성장 등 결과 사용처
- 다른 콘텐츠가 연결되는 중심 인터페이스

### 기술 코어

- 여러 기능이 의존하는 상태·데이터·공통 시스템
- 저장·호환성·ID·Schema 경계
- 교체 가능한 구현과 교체하면 안 되는 데이터 계약
- 기술 부채가 코어로 오인되지 않도록 한 대체 가능성

### 보호 경계

- `INVARIANT`: 유지해야 하는 요소
- `CHANGEABLE`: 자유롭게 교체 가능한 외피와 콘텐츠
- `REQUIRES_REAPPROVAL`: 변경 시 코어 재승인이 필요한 요소
- `OUT_OF_SCOPE`: 현재 코어와 MVP에서 제외할 요소

## State model

```text
CORE_SEED
→ CORE_PROPOSED
→ CORE_STRESS_TESTED
→ CORE_CONFIRMED | CORE_REVISE | CORE_REJECTED
→ CORE_RECORDED
```

- `CORE_SEED`: 아이디어와 후보만 있다.
- `CORE_PROPOSED`: 코어 계약 초안이 있다.
- `CORE_STRESS_TESTED`: 제거·대체·실패 반례를 검사했다.
- `CORE_CONFIRMED`: 승인 권한자의 명시적 승인이 있다.
- `CORE_REVISE`: 핵심 경계가 모호하거나 충돌한다.
- `CORE_REJECTED`: 현재 방향으로 확정하지 않는다.
- `CORE_RECORDED`: 승인된 계약이 책임 원본과 검수 기준에 연결됐다.

## Establishment process

### 1. Collect evidence

```text
사용자 목적·승인 결정
→ 핵심 컨셉·뾰족한 재미
→ 핵심 행동·루프
→ PoC·플레이테스트 근거
→ 시스템 의존성
→ 기술 기반·제약
```

근거가 없는 아이디어는 코어가 아니라 가설로 유지한다.

### 2. Write the minimum proposal

```text
[대상 플레이어]는 [핵심 행동과 선택]을 반복하며
[고유한 감정·성취]를 경험한다.
이 경험은 [코어 루프와 중심 시스템]으로 유지되며,
[불변 조건]이 사라지면 같은 프로젝트로 보지 않는다.
```

기능 목록 전체를 코어로 복사하지 않는다.

### 3. Separate invariants and shell

```text
INVARIANT
- 핵심 제작 행동
- 반복 성장과 위험
- 가치·특성 변화
- 결과의 판매·의뢰·전투 활용

CHANGEABLE
- 스킨 종류
- 고객 대사
- UI 배치
- 이벤트 개수
- 세부 수치와 연출
```

### 4. Stress-test

1. 한 핵심 행동을 제거해도 같은 경험인가?
2. 중심 시스템을 대체해도 정체성이 유지되는가?
3. 위험·선택·피드백이 없어도 핵심 재미가 남는가?
4. 너무 넓어 일반적인 장르 설명이 되지 않았는가?
5. 너무 좁아 하나의 구현 방식에 종속되지 않았는가?
6. 기술 부채나 임시 구조를 불변 조건으로 고정하지 않았는가?
7. MVP에서 최소한으로 재현하고 관찰할 수 있는가?
8. 확장 콘텐츠가 코어를 강화하는지 대체하는지 판정 가능한가?

치명적 반례가 남으면 `CORE_CONFIRMED`로 전환하지 않는다.

### 5. User confirmation

```yaml
proposal:
must_remain:
may_change:
requires_reapproval:
evidence:
unverified:
alternatives:
approval_request:
```

사용자 응답을 다음 중 하나로 기록한다.

- `APPROVE`
- `APPROVE_WITH_CHANGES`
- `REVISE`
- `REJECT`
- `DEFER`

침묵·추정·모호한 긍정을 승인으로 사용하지 않는다.

### 6. Record and connect

승인 후 다음에 연결한다.

- 프로젝트 종합 기획 책임 원본
- 핵심 컨셉·코어 루프·시스템 책임 원본
- 개발 게이트와 MVP·PoC 범위
- 변경 영향·적대적 검토·회귀 기준
- Active Context의 현재 상태와 금지 방향

같은 내용을 여러 파일에 독립 원본으로 복제하지 않는다. Registry가 가리키는 한 책임 원본에 기록하고 다른 문서는 참조한다.

## Core change policy

확정된 코어는 영구 불변이 아니지만 일반 기능 수정과 같은 방식으로 바꾸지 않는다. 다음 조건에서만 `reopen`한다.

- 사용자가 프로젝트 방향 변경을 명시했다.
- PoC·플레이테스트가 핵심 가설을 반복 반증했다.
- 제작·기술·법적 제약으로 핵심 경험이 성립하지 않는다.
- 현재 구현이 코어와 장기간 충돌해 정체성이 이미 변했다.
- 기존 코어 문장끼리 모순된다.

재확정 전에는 기존 코어와 새 후보를 구분하고 영향·마이그레이션·중단 기준을 제시한다.

## Output contract

```md
# 프로젝트 코어 확정 계약
## 상태
## 프로젝트 정체성 한 문장
## 대상 플레이어와 핵심 약속
## 핵심 행동·선택·피드백
## 코어 루프
## 중심 시스템과 의존 관계
## 기술 코어와 대체 가능한 구현
## 불변 조건
## 변경 가능한 외피
## 재승인이 필요한 변경
## 코어 기능과 MVP 지원 기능
## PoC·플레이테스트 근거
## 반례·실패 조건
## 제외한 후보와 이유
## 미검증·보류
## 사용자 승인 기록
## 책임 원본·게이트·검수 연결
```

## Definition of Done

- 코어를 정체성·경험·시스템·기술·보호 경계로 구분했다.
- 불변 조건과 변경 가능한 외피가 명확하다.
- 제거·대체·실패 반례를 검사했다.
- 코어 기능과 MVP 지원 기능을 분리했다.
- 사용자 명시적 승인 또는 수정·기각 상태가 기록됐다.
- 승인된 코어만 책임 원본과 게이트에 연결했다.
- 재승인 조건과 코어 변경 정책이 있다.

## Failure conditions

- AI가 사용자 승인 없이 `CORE_CONFIRMED`로 표시한다.
- 기능 목록 전체를 코어로 고정한다.
- 장르명이나 홍보 문구를 코어 계약으로 대체한다.
- 현재 임시 코드 구조를 영구 기술 코어로 확정한다.
- 코어와 MVP 범위를 혼동한다.
- 변경 가능한 UI·대사·스킨·분량을 불변 조건으로 만든다.
- PoC 반증을 무시하고 기존 방향을 확정한다.
- 승인된 코어를 여러 문서에 독립 원본으로 복제한다.
- 일반 기능 변경으로 코어를 암묵적으로 바꾼다.

## Learning

- Learning Log: `skills/SKILL_LEARNING_LOG.md`
- 현재 지식 상태: `HYPOTHESIS`
- 검토 트리거: 과도한 코어 범위, 승인 없는 확정, 코어와 MVP 혼동, PoC 반증 무시
