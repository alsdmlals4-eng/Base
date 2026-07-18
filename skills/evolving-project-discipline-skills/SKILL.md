---
name: evolving-project-discipline-skills
description: Use when creating, separating, reviewing, consolidating, or improving foundation and discipline-specific project skills from actual game-project work, validation, failures, and handoff evidence.
---

# Evolving Project Discipline Skills

## Core principle

공용 절차는 foundation에서 한 번만 책임지고, 각 분야 스킬은 해당 분야의 고유 판단·실제 경로·산출물·검증·학습을 책임한다.

모든 의미 있는 스킬 호출은 결과를 Learning Log에 남긴다. 스킬 본문은 반복 실패, 새 예외, 책임·경로·검증 변경처럼 실제 근거가 있을 때만 갱신한다.

공용 방법: `docs/knowledge/methods/DISCIPLINE_SKILL_EVOLUTION_METHOD.md`

템플릿:

- `templates/project-operations/PROJECT_SKILL_MAP.md`
- `templates/project-operations/SKILL_REGISTRY.json`
- `templates/project-operations/skills/FOUNDATION_SKILL.md`
- `templates/project-operations/skills/DISCIPLINE_SKILL.md`
- `templates/project-operations/skills/SKILL_LEARNING_LOG.md`

## Trigger

- 프로젝트에 분야별 스킬 구조를 설치
- 하나의 거대한 스킬을 분야별로 분리
- 여러 스킬의 중복 공용 절차를 foundation으로 통합
- 실제 작업 결과·실패·예외를 스킬에 반영
- 새 채팅이 분야 책임 문서와 필요한 스킬만 찾도록 라우팅
- Skill Registry와 Project Skill Map의 불일치를 수정
- 스킬 호출은 있었지만 Learning Log가 누락됨
- 프로젝트 교훈을 Base 환류 후보로 분류

## Do not use

- 스킬 구조나 실행 계약에 영향 없는 일반 구현 작업
- 단순히 스킬 파일 수를 늘리려는 작업
- 한 번의 성공을 공용 강제 규칙으로 승격하려는 경우
- 전체 skills 폴더를 기본 컨텍스트로 읽게 하려는 경우

## Required inputs

```yaml
project_start_here:
documentation_map:
project_skill_map:
skill_registry:
discipline_bibles:
existing_project_skills:
skill_learning_logs:
actual_work_examples:
validation_and_failures:
base_version:
```

## Phase 1 — Skill inventory

| 스킬 | 분야 | 사용 조건 | 비사용 조건 | trigger tags | 입력 | 산출물 | 검증 | Learning Log | 실제 참조 | 중복 | 상태 |
|---|---|---|---|---|---|---|---|---|---|---|---|
|  |  |  |  |  |  |  |  |  |  |  | 현행/보조/백업/보류/통합 후보 |

다음을 찾는다.

- 설명만 있고 실행 절차가 없는 스킬
- 실제 본책·파일·테스트 경로가 없는 스킬
- 사용하지 않는 조건이나 trigger tags가 없는 스킬
- `load_by_default=true`이거나 전체 로드를 요구하는 스킬
- 같은 공용 체크리스트의 장문 복제
- 도구·모델 이름만 바꾸면 같은 중복 스킬
- 너무 많은 분야를 한 파일이 책임하는 스킬
- 한 번 성공한 사례를 검증된 규칙으로 과장한 부분
- Learning Log·review trigger가 없는 스킬
- 호출됐지만 실행 결과가 기록되지 않은 스킬
- 기본 읽기에서 제외해야 할 백업·보류 스킬

## Phase 2 — Design the skill map and registry

기본 구조:

```text
skills/
├─ SKILL_REGISTRY.json
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

프로젝트에 필요하지 않은 폴더는 만들지 않는다. 책임이 다른 분야에 통합돼 있으면 `PROJECT_SKILL_MAP.md`와 `SKILL_REGISTRY.json`에서 통합 위치와 경계를 표시한다.

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

후보를 모두 만들지 않는다. 실제 반복 작업, 별도 품질 기준과 검증 경로가 있을 때만 현행 스킬로 채택한다.

## Phase 3 — Write contracts

각 스킬에 다음을 작성한다.

- skill ID와 분야
- 목적
- 사용하는 조건
- 사용하지 않는 조건
- trigger tags와 `load_by_default=false`
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
- Learning Log와 검토 트리거
- 마지막 검토일·기준 커밋
- 현재 지식 상태

공용 설명은 참조하고 복사하지 않는다.

## Phase 4 — Register selective routing

`SKILL_REGISTRY.json`에 활성 스킬을 등록한다.

필수 항목:

```json
{
  "skill_id": "example-skill",
  "layer": "foundation-or-discipline",
  "discipline": "responsible-discipline",
  "path": "skills/.../SKILL.md",
  "status": "ACTIVE",
  "load_by_default": false,
  "trigger_tags": ["concrete-trigger"],
  "use_when": ["specific condition"],
  "do_not_use_when": ["specific exclusion"],
  "learning_log": "skills/.../LEARNING_LOG.md",
  "review_triggers": ["failure or change"],
  "last_reviewed_at": "YYYY-MM-DD",
  "last_reviewed_commit": "commit",
  "knowledge_state": "OBSERVATION"
}
```

`discipline_entrypoints`에서 11개 책임 분야가 어떤 현행 진입 스킬을 사용하는지 연결한다. 통합 분야는 같은 skill ID를 공유할 수 있지만 책임 장과 검증 경계를 설명한다.

## Phase 5 — Apply and always learn

실제 작업에서 선택된 스킬만 적용한다.

```text
라우팅 결과
→ 필요한 foundation + 주 책임 분야 스킬 호출
→ 실제 수행
→ 결과·검증
→ 성공·실패·예외 기록
→ 사용자 피드백
→ 스킬 변경 필요성 판정
→ 필요 시 계약·회귀 테스트 수정
→ 지식 상태 판정
```

지식 상태는 `관찰 / 가설 / 패턴 / 검증 / 승격 후보`를 사용한다.

한 번 성공한 방법은 관찰 또는 가설이다. 다른 조건에서 반복돼야 패턴·검증으로 올라간다.

변경할 근거가 없으면 Learning Log에 `스킬 변경 없음`과 이유를 남긴다.

## Phase 6 — Consolidate safely

스킬 통합 전:

- 각 스킬의 고유 입력·출력·실패 조건 추출
- 프로젝트 전용 규칙 보존
- 호출 경로와 Documentation Map 참조 확인
- Learning Log와 지식 상태 보존
- Registry·Map·Issue·PR·자동 검사 참조 확인
- 통합 후 새 스킬에서 모든 기능을 찾을 수 있는지 대조

단순 이전 버전은 Git 이력으로 보존한다. 외부 승인·감사 원본은 `[백업]`, 미래 스킬은 재개 조건을 가진 `[보류]`로 둔다.

## Phase 7 — Update routing and governance

같은 작업에서 갱신한다.

- `SKILL_REGISTRY.json`
- `PROJECT_SKILL_MAP.md`
- 프로젝트 Documentation Map
- 관련 분야 본책
- 루트 `[기획서]/00_프로젝트_허브/START_HERE.md`
- Active Context·Handoff
- AGENTS.md의 읽기 순서
- Issue·PR 템플릿 또는 검사 설정
- 스킬 Learning Log

새 채팅은 전체 skills 폴더가 아니라 현재 작업에 필요한 foundation + 분야 스킬만 읽게 한다.

## Phase 8 — Health review

다음 상황에서 `verifying-game-project-operating-system`을 호출한다.

- 스킬 구조 설치·마이그레이션 직후
- 주요 개발 게이트 전
- 새 채팅이 스킬을 찾지 못함
- 같은 실패·누락이 반복됨
- 90일 이상 활성 스킬 검토 기록이 없음
- Registry와 Map 또는 실제 경로가 불일치함

검수 결과가 자동화 가능한 구조적 실패라면 governance checker와 회귀 테스트 후보로 반영한다.

## Phase 9 — Base promotion decision

분리:

- 프로젝트 전용: 세계관·수치·경로·승인 자산·현재 구현
- Base 후보: 반복 가능한 판단·절차·템플릿·실패 방지·검증 계약·회귀 테스트

승격 전 기존 Base Method·Skill·Template·Case와 중복을 확인한다. 한 프로젝트의 한 번 성공은 먼저 Case 또는 가설로 남긴다.

## Output contract

```md
## 프로젝트 스킬 구조 검수
- 기초·공용 스킬:
- 분야별 스킬:
- Skill Registry 상태:
- 새로 작성한 스킬:
- 통합한 중복:
- 백업·보류·제거 후보:
- 실제 본책·파일·테스트 연결:
- 선택적 호출 검증:
- 실행·검증 결과:
- 누락된 Learning Log:
- 학습 상태 변경:
- 스킬 변경 없음과 이유:
- Base 환류 후보:
- 콜드 스타트 결과:
```

## Failure conditions

- 폴더 수만 늘리고 실제 실행 계약 없음
- 모든 분야에 같은 스킬 본문 복사
- 전체 스킬을 기본 로드
- trigger와 무관한 스킬 호출
- 프로젝트 고유 정보를 Base 공용 스킬에 포함
- 실제 작업·검증 없이 스킬을 검증 상태로 표시
- 스킬 호출 결과·실패·예외를 기록하지 않음
- 실패·예외 Learning Log를 삭제
- 오래된 Registry·Map·Documentation Map 참조를 남김
- 새 AI가 어떤 스킬을 읽을지 판단할 라우터가 없음
