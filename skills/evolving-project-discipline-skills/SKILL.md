---
name: evolving-project-discipline-skills
description: Use when creating, separating, reviewing, consolidating, or improving foundation and discipline-specific project skills from actual game-project work, validation, failures, and handoff evidence.
---

# Evolving Project Discipline Skills

## Core principle

공용 절차는 foundation에서 한 번만 책임지고, 각 분야 스킬은 해당 분야의 고유 판단·실제 경로·산출물·검증·학습을 책임한다.

공용 방법: `docs/knowledge/methods/DISCIPLINE_SKILL_EVOLUTION_METHOD.md`

템플릿:

- `templates/project-operations/PROJECT_SKILL_MAP.md`
- `templates/project-operations/skills/FOUNDATION_SKILL.md`
- `templates/project-operations/skills/DISCIPLINE_SKILL.md`
- `templates/project-operations/skills/SKILL_LEARNING_LOG.md`

## Trigger

- 프로젝트에 분야별 스킬 구조를 설치
- 하나의 거대한 스킬을 분야별로 분리
- 여러 스킬의 중복 공용 절차를 foundation으로 통합
- 실제 작업 결과·실패·예외를 스킬에 반영
- 새 채팅이 분야 책임 문서와 스킬을 함께 찾도록 라우팅
- 프로젝트 교훈을 Base 환류 후보로 분류

## Required inputs

```yaml
project_start_here:
documentation_map:
project_skill_map:
discipline_bibles:
existing_project_skills:
actual_work_examples:
validation_and_failures:
base_version:
```

## Phase 1 — Skill inventory

| 스킬 | 분야 | 사용 조건 | 입력 | 산출물 | 검증 | 실제 참조 | 중복 | 상태 |
|---|---|---|---|---|---|---|---|---|
|  |  |  |  |  |  |  |  | 현행/보조/백업/보류/통합 후보 |

다음을 찾는다.

- 설명만 있고 실행 절차가 없는 스킬
- 실제 본책·파일·테스트 경로가 없는 스킬
- 같은 공용 체크리스트의 장문 복제
- 도구·모델 이름만 바꾸면 같은 중복 스킬
- 너무 많은 분야를 한 파일이 책임하는 스킬
- 한 번 성공한 사례를 검증된 규칙으로 과장한 부분
- 실패 조건·사용하지 않는 조건이 없는 스킬
- 기본 읽기에서 제외해야 할 백업·보류 스킬

## Phase 2 — Design the skill map

기본 구조:

```text
skills/
├─ foundation/
├─ narrative/
├─ game-design/
├─ ux-ui-accessibility/
├─ engineering/
├─ technical-art/
├─ art/
├─ audio/
├─ qa/
├─ production/
├─ analytics-user-research/
└─ integrated-review/
```

프로젝트에 필요하지 않은 폴더는 만들지 않는다. 책임이 다른 분야에 통합돼 있으면 `PROJECT_SKILL_MAP.md`에서 통합 위치와 경계를 표시한다.

### Foundation 권장 스킬

- intake-and-context-routing
- impact-analysis
- development-gate-review
- decision-recording
- documentation-governance
- validation-and-completion
- publishing-discipline-bibles
- context-compaction-and-handoff
- external-ai-draft-review
- project-learning-and-base-promotion

### 분야별 권장 스킬

각 분야는 최소 하나의 진입 스킬을 가진다. 반복 빈도·품질 기준이 다른 작업은 하위 스킬로 분리한다.

예:

```text
game-design/
├─ designing-game-systems/
└─ balancing-gameplay-data/

art/
├─ directing-game-art/
├─ producing-character-assets/
└─ reviewing-visual-consistency/
```

## Phase 3 — Write contracts

각 스킬에 다음을 작성한다.

- 목적
- 사용하는 조건
- 사용하지 않는 조건
- 필수 입력
- 먼저 읽을 책임 원본
- foundation 의존성
- 프로젝트 고유 규칙과 실제 경로
- 작업 절차
- 산출물
- Definition of Ready·Done
- 검증 방법
- 실패 조건
- 관련 스킬
- 학습 로그와 검토 트리거

공용 설명은 참조하고 복사하지 않는다.

## Phase 4 — Apply and learn

실제 작업에서 스킬을 적용하고 다음을 기록한다.

```text
입력과 범위
→ 실제 수행
→ 결과·검증
→ 성공·실패·예외
→ 사용자 피드백
→ 스킬 계약 수정
→ 지식 상태 판정
```

지식 상태는 `관찰 / 가설 / 패턴 / 검증 / 승격 후보`를 사용한다.

한 번 성공한 방법은 관찰 또는 가설이다. 다른 조건에서 반복돼야 패턴·검증으로 올라간다.

## Phase 5 — Consolidate safely

스킬 통합 전:

- 각 스킬의 고유 입력·출력·실패 조건 추출
- 프로젝트 전용 규칙 보존
- 호출 경로와 Documentation Map 참조 확인
- 학습 로그 보존
- 통합 후 새 스킬에서 모든 기능을 찾을 수 있는지 대조

단순 이전 버전은 Git 이력으로 보존한다. 외부 승인·감사 원본은 `[백업]`, 미래 스킬은 재개 조건을 가진 `[보류]`로 둔다.

## Phase 6 — Update routing

같은 작업에서 갱신한다.

- `PROJECT_SKILL_MAP.md`
- 프로젝트 Documentation Map
- 관련 분야 본책
- START_HERE·Active Context
- AGENTS.md의 읽기 순서
- Issue·PR 템플릿 또는 검사 설정
- Handoff

새 채팅은 전체 skills 폴더가 아니라 현재 작업에 필요한 foundation + 분야 스킬만 읽게 한다.

## Phase 7 — Base promotion decision

분리:

- 프로젝트 전용: 세계관·수치·경로·승인 자산·현재 구현
- Base 후보: 반복 가능한 판단·절차·템플릿·실패 방지·검증 계약

승격 전 기존 Base method·skill·template·case와 중복을 확인한다. 한 프로젝트의 한 번 성공은 먼저 case 또는 가설로 남긴다.

## Output contract

```md
## 프로젝트 스킬 구조 검수
- 기초·공용 스킬:
- 분야별 스킬:
- 새로 작성한 스킬:
- 통합한 중복:
- 백업·보류·제거 후보:
- 실제 본책·파일·테스트 연결:
- 실행·검증 결과:
- 학습 상태 변경:
- Base 환류 후보:
- 콜드 스타트 결과:
```

## Failure conditions

- 폴더 수만 늘리고 실제 실행 계약 없음
- 모든 분야에 같은 스킬 본문 복사
- 프로젝트 고유 정보를 Base 공용 스킬에 포함
- 실제 작업·검증 없이 스킬을 검증 상태로 표시
- 실패·예외 로그를 삭제
- 오래된 스킬 참조를 Documentation Map에 남김
- 새 AI가 어떤 스킬을 읽을지 판단할 라우터가 없음
