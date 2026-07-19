---
name: promoting-project-knowledge
description: Use at the end of project work or during handoff when reusable rules, methods, checklists, templates, skills, or cases should be separated from project-specific results and submitted as a Base change proposal without changing active Base contracts before user approval.
---

# Promoting Project Knowledge

## Core principle

Base는 **[학습형] [공용] 데이터 원본**이고 프로젝트는 공용 지식을 실제 조건에 맞게 **분화·적용·검증하는 전용 작업 공간**이다.

프로젝트의 구체 해답을 복사하지 않는다. 작업에서 확인한 반복 가능한 문제 해결 원리, 적용 조건, 실패 조건과 검증 방법을 공용 학습 후보로 추출하고, 먼저 Base의 `[수정제안서]`에 제출한다. 사용자 승인 전에는 활성 Method·Skill·Template·Tool·Schema·Test를 변경하지 않는다.

## Use when

- 작업 종료 보고를 작성할 때
- Active Context·Handoff를 갱신할 때
- 반복 가능한 기획·작업·검수 방법을 발견했을 때
- 기존 Base 규칙이나 스킬의 누락·중복·실패를 확인했을 때
- 프로젝트 결과를 다른 프로젝트에서도 재사용할 수 있는지 판단할 때

## Required inputs

- 이번 작업의 목표와 완료 기준
- 실제 변경 파일과 검증 결과
- 프로젝트의 현행 기획서·Active Context·Handoff
- 적용한 Base method·skill·template과 기준 버전
- 성공, 실패, 수정 과정과 미검증 항목

## Learning gate

모든 프로젝트 결과는 사례로 기록할 수 있지만, 확정 규칙·method·skill로 승격하려면 다음을 모두 만족해야 한다.

- 특정 프로젝트 이름과 수치 없이 설명 가능
- 반복 실패를 예방하거나 품질을 안정적으로 높임
- 사용 조건과 사용하지 않을 조건이 명확함
- 실행 또는 판단 절차를 재현할 수 있음
- 실제 작업·테스트 근거가 있음
- 기존 Base 책임 문서와 중복·충돌을 검토함

검증 전 내용은 `관찰`·`가설` case로 기록하고, 프로젝트의 `확인 필요` 또는 `보류`에도 연결한다. 한 번 성공한 방법을 곧바로 검증된 공용 스킬로 표시하지 않는다.

## Classify destination

| 내용 | 위치 |
|---|---|
| 모든 작업의 짧은 필수 규칙 | `AGENTS.md` 또는 공용 작업 규칙 |
| 반복 가능한 판단·설계법 | `docs/knowledge/methods/` |
| 조사·출처·근거 평가 | `docs/knowledge/research/` |
| 직접 실행하는 단계형 절차 | `skills/<name>/SKILL.md` |
| 분야별 역량·검수 지도 | `docs/knowledge/skills/` |
| 복사할 출력 양식 | `templates/` |
| 구체 문제·결정·결과·실패 | `docs/knowledge/cases/` |

## Process

### 1. 프로젝트 전용 원본 최신화

1. 확정된 프로젝트 결정, 수치, 구현 상태를 현행 기획서·테스트·로드맵에 반영한다.
2. Active Context 또는 Handoff를 최신화한다.
3. 프로젝트의 Documentation Map, Issue·Goal·Plan과 실제 파일 상태를 맞춘다.

### 2. 공용 학습 데이터 추출

1. 이번 작업에서 발생한 문제, 제약, 선택, 결과, 실패와 수정 과정을 기록한다.
2. 프로젝트 고유 이름·세계관·수치·경로·ID·자산을 분리한다.
3. 다른 프로젝트에서도 반복될 판단법, 절차, 체크리스트, 템플릿과 실패 방지 교훈을 추출한다.
4. Base에서 같은 책임을 가진 현행 문서를 찾고 중복·충돌을 확인한다.
5. 기존 문서를 갱신할지 새 유형이 필요한지 판단한다.

### 3. Base 수정제안서 작성

1. `[수정제안서]/PROPOSAL_REGISTRY.json`에서 다음 BCP ID를 정한다.
2. `templates/BASE_CHANGE_PROPOSAL.md`로 출처·관찰·일반화 후보·반례·영향·검증·롤백을 작성한다.
3. 제안 PR에는 `[수정제안서]/**`만 포함한다.
4. 사용자 검토 전 상태는 `SUBMITTED` 또는 `UNDER_REVIEW`로 둔다.
5. 승인 전에는 관련 method·skill·template을 미리 고치지 않는다.

사용자가 구현을 승인하면 `reviewing-and-implementing-base-change-proposals`를 별도로 호출한다.

### 4. 사례와 증거 연결

모든 공용화 작업에는 최소 하나의 사례 또는 기존 사례 상태 갱신이 연결되어야 한다.

사례에는 다음을 기록한다.

- 출처와 확인 날짜
- 문제와 제약
- 관찰 근거
- 검토한 대안
- 결정과 이유
- 실제 결과
- 실패와 수정 과정
- 미검증 항목
- 재사용 가능한 원칙
- 프로젝트 전용으로 남길 요소
- 현재 지식 상태
- 후속 검증 조건

형식은 `templates/KNOWLEDGE_CASE_STUDY.md`를 사용한다.

### 5. 제안 라우팅·동기화

1. 프로젝트 Documentation Map·Active Context에서 BCP 경로를 연결한다.
2. 제안 Registry와 제안서의 ID·상태·출처 커밋을 맞춘다.
3. 제안 PR과 이후 구현 PR을 분리한다.
4. 인수인계에 `프로젝트 전용`, `Base 제안`, `승인 상태`, `미검증·후속 검증`을 구분한다.

공용화 가능한 내용이 없으면 억지로 Base를 수정하지 않고 `공용 학습 데이터 없음 — 프로젝트 전용 또는 단발성 작업`으로 기록한다.

## Do not promote

- 프로젝트 전체 GDD와 현재 밸런스
- 고유 세계관·캐릭터·파일 경로
- 일회성 함수명·씬명·데이터 ID
- 검증되지 않은 가설을 확정 규칙으로 표시한 내용
- 비공개 원문과 권한 없는 자료
- 외부 작품의 코드·아트·문구·UI 복제본

검증되지 않은 가설 자체는 삭제하지 않는다. 프로젝트 기록과 Base case의 `관찰`·`가설` 상태로 보존한다.

## Output contract

```md
## 프로젝트 전용 최신화
## Base 공용 학습 데이터
## 작성한 Base 수정제안서와 상태
## 작성·갱신한 사례와 지식 상태
## 검증 근거
## 미검증·후속 검증
## 제안 PR·후속 구현 조건
```

## Validation scenarios

1. 특정 카드 UI 사례는 프로젝트에 남기고, “상시 정보와 상세 정보를 분리하는 판단법”만 method로 일반화하며 실제 카드 사례는 case로 기록한다.
2. 한 번 성공한 프롬프트는 `가설` case로 기록하고, 여러 캐릭터·모델·화면에서 반복 검증한 뒤 skill을 보완한다.
3. 기존 method와 같은 내용이면 새 파일을 만들지 않고 현행 원본과 관련 case를 갱신한다.
4. 작업 결과가 프로젝트 세계관과 파일 경로에만 의존하면 Base를 수정하지 않고 프로젝트 전용으로 보고한다.

Templates:

- `templates/KNOWLEDGE_CASE_STUDY.md`
- `templates/skills/PROJECT_SKILL_EXTENSION.md`
- `templates/BASE_CHANGE_PROPOSAL.md`
