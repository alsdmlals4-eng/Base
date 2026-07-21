---
name: managing-base-change-proposals
description: Use when extracting reusable project knowledge, submitting a Base change proposal, reviewing an existing proposal, or implementing only a user-approved proposal through a separate change branch and PR.
---

# Managing Base Change Proposals

## Core principle

프로젝트 교훈의 추출·제출·검토·승인된 구현은 하나의 BCP 생명주기다. 하나의 상태 머신으로 추적하되, 제안 PR과 활성 Base 구현 PR의 승인 경계는 절대 합치지 않는다.

## Modes

- `extract`: 프로젝트 결과에서 공용 원리와 프로젝트 전용 값을 분리한다.
- `submit`: `[수정제안서]`에 제안과 증거를 등록한다.
- `review`: 중복·반례·위험을 검토하고 승인·보류·거절 판정을 제안한다.
- `implement`: `APPROVED_FOR_IMPLEMENTATION`과 재현 가능한 `approval_ref`가 있는 범위만 별도 구현 PR로 반영한다.
- `verify`: 구현·회귀·Registry·제안서 연결과 롤백 가능성을 확인한다.

## State model

```text
DRAFT
→ SUBMITTED
→ UNDER_REVIEW
→ APPROVED_FOR_IMPLEMENTATION | DEFERRED | REJECTED
→ IMPLEMENTING
→ IMPLEMENTED
```

`APPROVED_FOR_IMPLEMENTATION`과 비어 있지 않은 `approval_ref` 없이 `implement` 모드로 이동하지 않는다.

## Required inputs

```yaml
project_goal_and_acceptance:
actual_changes_and_validation:
project_current_sources:
base_version_and_applied_assets:
proposal_registry:
proposal_path:
evidence_paths:
source_project_commit:
current_base_owner_sources:
user_approval_ref:
implementation_scope:
protected_and_excluded_scope:
```

## Workflow

### 1. Extract reusable knowledge

- 프로젝트 고유 이름·세계관·수치·경로·ID·자산을 분리한다.
- 반복 가능한 문제 해결 원리, 사용 조건, 비사용 조건, 실패 조건과 검증 방법만 공용 후보로 만든다.
- 한 번의 성공이나 미검증 추측은 `관찰`·`가설` case로 남긴다.
- 기존 Base의 같은 책임 원본과 중복·충돌을 먼저 확인한다.

### 2. Submit proposal only

1. `[수정제안서]/PROPOSAL_REGISTRY.json`에서 ID를 정한다.
2. `templates/BASE_CHANGE_PROPOSAL.md`로 출처·관찰·일반화 후보·반례·영향·검증·롤백을 작성한다.
3. 제안 PR에는 원칙적으로 `[수정제안서]/**`만 포함한다.
4. 상태를 `SUBMITTED` 또는 `UNDER_REVIEW`로 둔다.
5. 승인 전에는 활성 Method·Skill·Template·Tool·Schema·Test를 변경하지 않는다.

### 3. Review

- 제안 ID·상태·출처 커밋과 실제 증거를 확인한다.
- 프로젝트 전용 값이 공용 규칙에 유입되지 않았는지 검사한다.
- 기존 Base 책임과 중복·충돌·대체 관계를 찾는다.
- 성공 증거뿐 아니라 반례·비사용 조건·보안·라이선스·비용·호환성·마이그레이션·롤백을 평가한다.
- `APPROVED_FOR_IMPLEMENTATION`, `DEFERRED`, `REJECTED` 중 하나를 사용자에게 제안한다.
- 사용자의 명시적 결정과 근거를 `approval_ref`에 기록한다.

### 4. Implement approved scope

1. 승인 상태와 `approval_ref`를 기계적으로 확인한다.
2. 제안 PR과 분리된 별도 구현 PR을 사용한다.
3. 승인 범위·제외 범위·보호 대상을 작업 계약으로 옮긴다.
4. 필요한 Method·Skill·Template·Tool·Schema·Test만 변경한다.
5. 기준·대표·변형·반례·회귀 시나리오를 검증한다.
6. 제안서와 Registry에 구현 PR·커밋·검증을 연결한다.
7. 실패하면 부분 반영 상태를 숨기지 않고 롤백·복구 방법을 기록한다.

### 5. Verify lifecycle integrity

- 제안과 구현 PR이 분리됐는가?
- 승인 근거가 재현 가능한가?
- 승인 범위를 벗어난 변경이 없는가?
- 프로젝트 고유 값이 Base에 들어오지 않았는가?
- 테스트와 반례가 실제 실행됐는가?
- Proposal Registry·제안서·구현 PR·Changelog가 연결됐는가?

## Output contract

```md
## Base 변경 제안 생명주기
## 공용화 가능한 원리
## 프로젝트 전용으로 남긴 요소
## 제안 ID·상태·출처
## 중복·충돌·반례·위험
## 사용자 승인 상태와 근거
## 승인된 구현 범위·제외·보호
## 실제 변경·검증·롤백
## 제안 PR·구현 PR·Registry 연결
## 미검증·후속 조건
```

## Definition of Done

- 공용 원리와 프로젝트 전용 값이 분리됐다.
- 미검증 교훈을 확정 규칙으로 승격하지 않았다.
- 제안과 구현이 다른 승인 단계와 PR에 있다.
- 구현은 승인된 최소 범위만 포함한다.
- Proposal Registry·제안서·구현·검증이 추적된다.
- 거절·보류·구현 이력을 삭제하지 않았다.

## Failure conditions

- 신규 제안과 활성 Base 변경을 같은 PR에 넣음
- 사용자 승인 없이 구현 상태로 이동함
- 프로젝트 고유 코드·아트·수치·경로를 공용 규칙으로 복사함
- 한 번의 성공을 검증된 스킬로 승격함
- 반례·비사용 조건·롤백을 누락함
- 실행하지 않은 테스트나 권한 확인을 통과 처리함
- 거절·보류 기록을 삭제함

## Legacy aliases

- `promoting-project-knowledge` → `extract`, `submit`
- `reviewing-and-implementing-base-change-proposals` → `review`, `implement`, `verify`

Templates:

- `templates/KNOWLEDGE_CASE_STUDY.md`
- `templates/BASE_CHANGE_PROPOSAL.md`
