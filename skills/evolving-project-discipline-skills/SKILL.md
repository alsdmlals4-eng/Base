---
name: evolving-project-discipline-skills
description: Use when creating, separating, reviewing, consolidating, or improving Foundation and discipline project skills from actual work, validation, failures, and handoff evidence, while keeping SKILL_REGISTRY.json and generated human DOCX/PDF skill maps synchronized.
---

# Evolving Project Discipline Skills

## Core principle

공용 절차는 Foundation에서 한 번만 책임지고, 각 분야 스킬은 해당 분야의 고유 판단·JSON 본책·실제 경로·산출물·검증·학습을 책임한다.

실패, 중요한 결정, 재사용 가능한 교훈, 실제 검증 결과가 있는 호출은 Learning Log에 남긴다. 사소한 성공 호출은 기록을 강제하지 않는다. 스킬 본문은 반복 실패, 새 예외, 책임·경로·검증 변경처럼 근거가 있을 때만 갱신한다.

## 책임 구조

```text
AI·자동 검사 → SKILL_REGISTRY.json
사람 기본 열람 → PROJECT_SKILL_MAP.pdf
사람 문서 검토 → PROJECT_SKILL_MAP.docx
시각 관계 → PROJECT_SKILL_MAP.assets/
최신성 → SKILL_MAP_PUBLICATION_MANIFEST.json
```

`PROJECT_SKILL_MAP.md`는 사용하지 않는다.

## Trigger

- 프로젝트에 분야별 스킬 구조 설치
- 하나의 거대한 스킬을 분야별로 분리
- 여러 스킬의 중복 공용 절차를 Foundation으로 통합
- 실제 결과·실패·예외를 스킬에 반영
- 새 채팅이 필요한 최소 스킬을 찾지 못함
- Skill Registry와 실제 스킬 경로·상태 불일치
- 사람용 Skill Map이 Registry보다 오래됨
- Learning Log 누락
- 프로젝트 교훈의 Base 환류 판단

## Do not use

- 스킬 계약에 영향 없는 일반 구현
- 단순히 스킬 파일 수를 늘리는 작업
- 한 번의 성공을 공용 강제 규칙으로 승격
- 전체 skills 폴더를 기본 컨텍스트로 읽게 하는 작업
- Registry가 변하지 않았고 사람용 발행본이 `CURRENT`인 경우

## Required inputs

```yaml
project_start_here:
documentation_map:
skill_registry:
skill_map_publication_manifest:
design_document_registry:
relevant_design_document_json:
existing_project_skills:
learning_logs:
actual_work_examples:
validation_and_failures:
base_version:
```

## Phase 1 — Inventory

| 스킬 | 분야 | 사용 조건 | 비사용 조건 | Trigger | 입력 | 산출물 | 검증 | Learning Log | 실제 JSON·경로 | 중복 | 상태 |
|---|---|---|---|---|---|---|---|---|---|---|---|
|  |  |  |  |  |  |  |  |  |  |  | 현행/보조/백업/보류/통합 후보 |

찾을 것:

- 설명만 있고 실행 절차가 없음
- JSON 본책·실제 파일·테스트 경로가 없음
- 사용·비사용 조건이나 Trigger가 없음
- `load_by_default=true` 또는 전체 로드 요구
- 공용 체크리스트 장문 복제
- 너무 많은 분야를 한 파일이 책임
- 한 번 성공한 사례를 검증된 규칙으로 과장
- Learning Log·review trigger 누락
- 호출 결과 미기록
- 백업·보류 스킬의 기본 읽기 혼입

## Phase 2 — Foundation·분야 구조

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

필요하지 않은 폴더는 만들지 않는다. 통합 분야는 `discipline_entrypoints`에서 같은 Skill ID를 공유할 수 있지만 책임·검증 경계를 명시한다.

권장 Foundation 책임:

- 요청·컨텍스트 라우팅
- 영향도 분석
- 개발 게이트 검수
- 결정·추적성
- JSON 기획서·발행 Governance
- 검증·완료 선언
- Context·Handoff
- 외부 AI 검수
- 학습·Base 환류

분야별 하위 스킬은 실제 반복 빈도, 별도 Quality Bar와 검증 경로가 있을 때만 만든다.

## Phase 3 — Skill contract

각 스킬 필수 항목:

- Skill ID·분야·상태
- 목적
- 사용하는 조건·사용하지 않는 조건
- `trigger_tags`
- `load_by_default=false`
- 필수 입력과 먼저 읽을 JSON 책임 원본
- Foundation 의존성
- 프로젝트 고유 규칙·실제 경로
- 절차·산출물
- Ready·Done
- 자동·수동 검증
- 실패 조건
- 관련 스킬
- Learning Log·review trigger
- 마지막 검토일·기준 커밋
- 지식 상태

## Phase 4 — Register selective routing

`SKILL_REGISTRY.json`에 활성 스킬을 등록하고 11개 분야의 `discipline_entrypoints`를 연결한다.

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

## Phase 5 — Generate human Skill Map

Registry 변경 후 실행:

```text
python tools/build_project_skill_map.py \
  --registry "[기획서]/00_프로젝트_허브/SKILL_REGISTRY.json" \
  --output-dir "[기획서]/00_프로젝트_허브" \
  --project-name "프로젝트명" \
  --source-commit <commit>
```

생성:

- `PROJECT_SKILL_MAP.docx`
- `PROJECT_SKILL_MAP.pdf`
- `PROJECT_SKILL_MAP.assets/skill-flow.png`
- `PROJECT_SKILL_MAP.assets/discipline-routing.png`
- `PROJECT_SKILL_MAP.assets/skill-matrix.png`
- `SKILL_MAP_PUBLICATION_MANIFEST.json`

사람은 PDF를 먼저 보고, AI는 Registry를 읽는다. DOCX를 직접 고쳐 책임 원본으로 사용하지 않는다.

## Phase 6 — Apply and always learn

```text
라우팅 결과
→ 필요한 Foundation + 주 책임 분야 스킬 호출
→ 실제 수행
→ 결과·검증
→ 성공·실패·예외·사용자 피드백 기록
→ 과다 호출·누락 검증 기록
→ 스킬 변경 필요성 판정
→ 필요 시 계약·테스트·Registry 수정
→ 사람용 Skill Map 재생성
→ 지식 상태 판정
```

지식 상태:

```text
관찰 → 가설 → 패턴 → 검증 → 승격 후보
```

변경 근거가 없으면 Learning Log에 `스킬 변경 없음`과 이유를 남긴다.

## Phase 7 — Consolidate safely

통합 전:

- 고유 입력·출력·실패 조건 추출
- 프로젝트 전용 규칙 보존
- JSON 본책·Documentation Map·Issue·PR 참조 확인
- Learning Log와 지식 상태 보존
- Registry와 사람용 발행본 경로 확인
- 통합 후 새 스킬에서 모든 책임을 찾을 수 있는지 대조

이전 버전은 Git 이력으로 보존한다. 외부 승인·감사 원본은 `[백업]`, 미래 스킬은 재개 조건을 가진 `[보류]`로 둔다.

## Phase 8 — Update routing and governance

같은 작업에서 갱신:

- `SKILL_REGISTRY.json`
- 관련 `SKILL.md`
- Learning Log
- `PROJECT_SKILL_MAP.docx/.pdf/.assets`
- `SKILL_MAP_PUBLICATION_MANIFEST.json`
- Documentation Map·START_HERE
- 관련 기획서 JSON
- Active Context·Handoff
- Issue·PR·Governance 설정

## Phase 9 — Health Review

다음 상황에서 `verifying-game-project-operating-system`을 호출한다.

- 스킬 구조 설치·마이그레이션 직후
- 주요 개발 게이트 전
- 새 채팅이 스킬을 찾지 못함
- 같은 실패·누락 반복
- 90일 이상 활성 스킬 미검토
- Registry·사람용 발행본·실제 경로 불일치

자동화 가능한 결함은 Governance Checker와 회귀 테스트로 승격한다.

## Output contract

```md
## 프로젝트 스킬 구조 검수
- Foundation 스킬:
- 분야별 스킬:
- Skill Registry 상태:
- 사람용 DOCX/PDF·다이어그램 상태:
- 새로 작성·통합한 스킬:
- 백업·보류·제거 후보:
- JSON 본책·실제 파일·테스트 연결:
- 선택적 호출 검증:
- 실행·검증 결과:
- Learning Log:
- 학습 상태 변경:
- 스킬 변경 없음과 이유:
- Base 환류 후보:
- 콜드 스타트 결과:
```

## Failure conditions

- 파일 수만 늘리고 실행 계약 없음
- 모든 분야에 같은 스킬 본문 복사
- 전체 skills 폴더 기본 로드
- Trigger 없이 호출
- Registry 변경 후 DOCX/PDF·다이어그램 미재생성
- 사람용 DOCX를 별도 책임 원본으로 수정
- 실제 결과 없이 지식 상태를 검증으로 승격
- Learning Log 누락
