# AGENTS.md

이 파일은 현재 프로젝트의 최상위 작업 규칙이다. Base의 **[학습형] [공용] 원칙**을 프로젝트의 엔진, 구조, 세계관, 용어, 금지 범위와 검증 방식에 맞게 분화한다.

이 프로젝트 저장소는 공용 Base의 복제 원본이 아니라 **프로젝트 전용 기획·구현·검증 공간**이다. 프로젝트에서 얻은 재사용 가능한 방법과 실패 교훈은 작업 종료·인수인계 시 Base 공용 학습 데이터로 환류한다.

## Top-level continuity rule

새 채팅, 새 AI, 새 작업자가 과거 대화나 기존 작업자의 설명 없이도 저장소만으로 작업을 이어갈 수 있어야 한다.

- 프로젝트 기획서만 읽어도 핵심 플레이어 경험, 현재 방향, 확정·미확정 사항, 범위와 금지 방향을 이해할 수 있어야 한다.
- 로드맵은 현재 단계, 우선순위, 선행 조건, 다음 작업, 단계별 종료 기준과 검증을 유지한다.
- Base 스킬과 프로젝트 전용 스킬 확장은 현재 작업 구조, 입력, 절차, 산출물, 완료 기준과 실패 기준을 유지한다.
- Active Context·Handoff는 기획서를 복제하지 않고 현재 상태, 최근 결정, 다음 실행 순서와 책임 문서를 연결한다.
- Documentation Map은 질문별 현행 책임 원본과 최초 읽기 순서를 유지한다.
- 방향, 수치, 용어, 범위, 구현 상태 또는 작업 절차가 바뀌면 같은 작업 안에서 관련 기획서·로드맵·스킬·Active Context·문서 지도를 갱신한다.
- 같은 정보의 활성 복제본을 만들지 않고 현행 책임 원본 하나를 갱신한다.

완료 전에는 새 작업자가 10분 안에 프로젝트의 핵심 방향, 현재 상태, 다음 작업, 금지 범위, 책임 문서와 검증 방법을 찾을 수 있는지 확인한다.

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
5. 승인 기획서와 현재 Issue 또는 승인된 직접 요청·Goal·Plan
6. Base 로컬 사본
7. Base 원격
8. 과거 대화와 추정

## Default reading order

작업 시작 전에는 현재 작업에 적용되는 공용 Base 정보와 프로젝트 전용 정보를 모두 확인한다.

작업 계약은 `github_issue` 또는 `approved_direct_request`다. 직접 요청은 Issue가 없어도 되지만 Goal·PR에 범위·제외·완료 기준·검증을 남긴다.

작업에 필요한 도구·파일·폰트·계정 인증·저장소 또는 브랜치 권한이 없으면 사용자에게 필요한 이유, 설치·적용 방법, 확인 명령과 최소 권한 범위를 안내해 요청한다. 사용자 승인 없이 시스템 전역 설치·권한 확대·보안 또는 Branch protection 설정 변경을 하지 않으며, 설치 완료 통보 후에도 실제 경로·버전·인증을 확인한다.

```text
AGENTS.md
→ BASE_RULES_VERSION.md와 Base 로컬 사본
→ 프로젝트 Documentation Map
→ Handoff·Active Context
→ 프로젝트 방향과 관련 분야 책임 문서
→ Roadmap
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
- 현재 로드맵·구현·테스트 상태
- 프로젝트 전용 skill extension과 작업 절차
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
- 필수 도구·입력 파일:
- 필수 계정·저장소 권한:
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
- Cold-start review:

## File lifecycle

- 한 질문에 현행 책임 문서 하나를 둔다.
- `v2`, `final`, `latest`, 날짜별 활성 복제본을 만들지 않는다.
- 이전 내용은 Git 이력으로 보존한다.
- 생성·삭제·이동·이름 변경 시 참조와 동기화를 확인한다.

## End-of-work and handoff learning cycle

작업 종료와 인수인계 시 다음을 수행한다.

1. 프로젝트 고유 결정, 수치, 구현 상태를 현행 기획서·테스트·로드맵에 반영한다.
2. Active Context 또는 Handoff를 최신화한다.
3. 프로젝트 전용 skill extension과 실행 절차를 현재 구조에 맞게 갱신한다.
4. Documentation Map, README, Issue·Goal·Plan의 연결을 확인한다.
5. 이번 작업의 결과를 `프로젝트 전용`과 `공용 학습 데이터`로 분리한다.
6. 재사용 가능한 판단법·작성법·절차·체크리스트·템플릿을 Base 관련 method·skill·template에 반영한다.
7. 문제, 선택, 실제 결과, 실패, 수정 과정, 미검증 항목을 Base case 형식으로 작성하거나 기존 사례 상태를 갱신한다.
8. 한 번 성공한 방법은 `관찰`·`가설`로 기록하고 반복 검증 전에는 공용 확정 규칙으로 표시하지 않는다.
9. Base 변경 시 `docs/BASE_RULES_VERSION.md`와 로컬 사본의 동기화 필요를 기록한다.
10. 새 작업자가 콜드 스타트 질문에 답할 수 있는지 확인한다.

공용화 가능한 내용이 없으면 `공용 학습 데이터 없음 — 프로젝트 전용 또는 단발성 작업`으로 기록한다.

## Report format

```md
## 변경 파일과 이유
## 유지한 기존 동작
## 구현·문서 변경
## 검증 결과
## 미검증·사용자 확인
## 남은 위험
## 기획서·로드맵·스킬·Active Context 최신화
## 콜드 스타트 검수
## 프로젝트 전용 최신화
## Base 공용 학습 데이터
## 갱신한 기획 method·스킬·템플릿
## 작성·갱신한 사례와 지식 상태
## 후속 동기화
```
