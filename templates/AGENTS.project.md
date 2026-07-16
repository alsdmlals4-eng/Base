# AGENTS.md

이 파일은 현재 프로젝트의 최상위 작업 규칙이다. Base 공용 원칙을 프로젝트의 엔진, 구조, 용어, 금지 범위와 검증 방식에 맞게 구체화한다.

## Project

- Project name:
- Engine:
- Language:
- Genre:
- Core player promise:

## Base

- Repository: `alsdmlals4-eng/Base`
- Version record: `docs/BASE_RULES_VERSION.md`
- Local shared copy:
  - `docs/AI_SHARED_WORK_RULES.md`
  - `docs/AI_WORKFLOW_RULES.md`
  - `docs/MVP_WORKFLOW_CHECKLIST.md`
  - `docs/DOCUMENTATION_MAP.md`
  - 필요한 `skills/`와 `templates/`

일상 작업에서는 Base 원격보다 프로젝트 로컬 사본을 먼저 읽는다. GitHub와 로컬은 자동 동기화되지 않으므로 기준 커밋과 동기화 날짜를 기록한다.

## Priority

1. 최신 사용자 지시
2. 이 `AGENTS.md`
3. 프로젝트 보안·엔진·데이터 규칙
4. 승인 기획서와 현재 Issue·Goal·Plan
5. Base 로컬 사본
6. Base 원격
7. 과거 대화와 추정

## Default reading order

```text
AGENTS.md
→ BASE_RULES_VERSION.md
→ Documentation Map
→ Handoff·Active Context
→ 프로젝트 방향과 관련 분야 책임 문서
→ 현재 Issue·Goal·Plan
→ 실제 수정 대상과 연결 파일
```

저장소 전체를 무조건 읽지 않는다. `archive`, `[백업]`, `hold`, `[보류]`는 재개 결정 전까지 기본 읽기·구현 대상에서 제외한다.

## Project-specific rules

- 프로젝트 전용 용어:
- 엔진·언어 규칙:
- 데이터·저장 계약:
- UI·아트·연출 규칙:
- 금지 구조:
- 보호 경로:
- 범위 밖 리팩터링 금지:
- 정상 사용자 변경 보존:

## Request-to-work rule

L2 이상의 설계 작업은 목적·맥락·경험·범위·제약·산출물·완료 기준·검증으로 변환한 뒤 시작한다.

- Base skill:
- Project extension:
- Current executable prompt:

## Validation

- Format·lint:
- Automated tests:
- Run path:
- Save·load:
- Manual review:
- Regression scope:

## File lifecycle

- 한 질문에 현행 책임 문서 하나를 둔다.
- `v2`, `final`, `latest`, 날짜별 활성 복제본을 만들지 않는다.
- 이전 내용은 Git 이력으로 보존한다.
- 생성·삭제·이동·이름 변경 시 참조와 동기화를 확인한다.

## Report format

```md
## 변경 파일과 이유
## 유지한 기존 동작
## 구현·문서 변경
## 검증 결과
## 미검증·사용자 확인
## 남은 위험
## 프로젝트 전용 내용
## Base 반영 내용
## 후속 동기화
```
