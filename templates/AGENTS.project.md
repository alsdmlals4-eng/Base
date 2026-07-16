# AGENTS.md

이 파일은 현재 프로젝트의 최상위 작업 규칙이다. Base의 **[학습형] [공용] 원칙**을 프로젝트의 엔진, 구조, 세계관, 용어, 금지 범위와 검증 방식에 맞게 분화한다.

이 프로젝트 저장소는 공용 Base의 복제 원본이 아니라 **프로젝트 전용 기획·구현·검증 공간**이다. 프로젝트에서 얻은 재사용 가능한 방법과 실패 교훈은 작업 종료·인수인계 시 Base 공용 학습 데이터로 환류한다.

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
  - 필요한 `docs/knowledge/`, `skills/`, `templates/`

일상 작업에서는 Base 원격보다 프로젝트 로컬 사본을 먼저 읽는다. GitHub와 로컬은 자동 동기화되지 않으므로 기준 커밋과 동기화 날짜를 기록한다.

## Priority

1. 최신 사용자 지시
2. 이 `AGENTS.md`
3. 프로젝트 보안·엔진·데이터 규칙
4. 프로젝트 Active Context·Handoff
5. 승인 기획서와 현재 Issue·Goal·Plan
6. Base 로컬 사본
7. Base 원격
8. 과거 대화와 추정

## Default reading order

작업 시작 전에는 현재 작업에 적용되는 공용 Base 정보와 프로젝트 전용 정보를 모두 확인한다.

```text
AGENTS.md
→ BASE_RULES_VERSION.md와 Base 로컬 사본
→ 프로젝트 Documentation Map
→ Handoff·Active Context
→ 프로젝트 방향과 관련 분야 책임 문서
→ 현재 Issue·Goal·Plan
→ 실제 수정 대상과 연결 파일
```

### Base 공용 확인 범위

- 관련 공용 작업 규칙
- 해당 분야 method·research
- 실행 skill과 검수 matrix
- 사용할 template
- 유사 성공·실패·미검증 case

### 프로젝트 전용 확인 범위

- 프로젝트 방향과 플레이어 경험
- 실제 기획·데이터·UI·아트·연출 규칙
- 현재 구현·테스트·로드맵 상태
- 실제 파일, 호출, 참조, 저장·호환성 영향

`모두 확인`은 저장소 전체를 무조건 읽는다는 뜻이 아니다. Documentation Map과 참조 관계로 현재 작업에 적용되는 공용·전용 현행 책임 원본과 영향 파일을 빠짐없이 확인한다.

`archive`, `[백업]`, `hold`, `[보류]`는 재개 결정 전까지 기본 읽기·구현 대상에서 제외한다.

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

## End-of-work and handoff learning cycle

작업 종료와 인수인계 시 다음을 수행한다.

1. 프로젝트 고유 결정, 수치, 구현 상태를 현행 기획서·테스트·로드맵에 반영한다.
2. Active Context 또는 Handoff를 최신화한다.
3. 이번 작업의 결과를 `프로젝트 전용`과 `공용 학습 데이터`로 분리한다.
4. 재사용 가능한 판단법·작성법·절차·체크리스트·템플릿을 Base 관련 method·skill·template에 반영한다.
5. 문제, 선택, 실제 결과, 실패, 수정 과정, 미검증 항목을 Base case 형식으로 작성하거나 기존 사례 상태를 갱신한다.
6. 한 번 성공한 방법은 `관찰`·`가설`로 기록하고 반복 검증 전에는 공용 확정 규칙으로 표시하지 않는다.
7. Base 변경 시 `docs/BASE_RULES_VERSION.md`와 로컬 사본의 동기화 필요를 기록한다.

공용화 가능한 내용이 없으면 `공용 학습 데이터 없음 — 프로젝트 전용 또는 단발성 작업`으로 기록한다.

## Report format

```md
## 변경 파일과 이유
## 유지한 기존 동작
## 구현·문서 변경
## 검증 결과
## 미검증·사용자 확인
## 남은 위험
## 프로젝트 전용 최신화
## Base 공용 학습 데이터
## 갱신한 기획 method·스킬·템플릿
## 작성·갱신한 사례와 지식 상태
## 후속 동기화
```
