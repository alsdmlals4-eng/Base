---
name: installing-game-project-operating-system
description: Use when auditing, creating, restructuring, or installing a persistent game-project repository operating system so GPT, Codex, GitHub documents, images, tests, and handoff stay aligned across new chats.
---

# Installing a Game Project Operating System

## Core principle

사용자가 규칙을 기억하게 하지 말고 저장소가 규칙을 기억하게 한다.

설치 결과는 폴더 생성이 아니라 다음 상태다.

- 새 GPT와 Codex가 같은 시작 문서를 읽는다.
- 질문별 현행 책임 원본이 하나다.
- 모든 작업이 주 책임 분야와 영향 분야를 가진다.
- 변경 시 관련 본책·상태·검증 문서를 갱신한다.
- 이미지의 승인·구현·검증·교체 상태와 캐노니컬 경로가 추적된다.
- PR 검사로 구조적 누락을 발견할 수 있다.
- 새 작업자가 과거 대화 없이 저장소만으로 작업을 재개한다.

공용 원리: `docs/knowledge/methods/GAME_PROJECT_OPERATING_SYSTEM_METHOD.md`

복사·분화 템플릿: `templates/project-operations/`

## Trigger

다음 요청에서 사용한다.

- 프로젝트 기획서·파일·이미지·팀 분야를 전면 정리해 달라는 요청
- 새 AI가 저장소만으로 작업하도록 운영체계를 설치해 달라는 요청
- `Base` 저장소를 참고해 프로젝트 전체를 정리해 달라는 요청
- 문서 갱신 누락과 이미지 중복을 GitHub에서 막고 싶다는 요청
- 프로젝트의 문서·코드·자산·테스트 책임 경계를 재설계하는 요청

사용자가 다음처럼 말한 경우 이 스킬을 우선 검토한다.

> `https://github.com/alsdmlals4-eng/Base 를 전부 살펴보고 참고해서 작업해줘.`

## Do not use

- 오탈자 한 줄 수정
- 이미 설치된 프로젝트의 작은 구현만 수행하는 작업
- 프로젝트 저장소 접근 없이 실제 설치 완료를 요구하는 경우
- 특정 프로젝트의 모든 기획을 Base 공용 저장소에 직접 넣으려는 경우

## Required inputs

가능한 범위에서 다음을 확인한다.

```yaml
target_repository:
local_checkout:
current_branch:
project_stage:
engine_and_platform:
existing_agents:
existing_documentation_map:
existing_active_context:
existing_design_docs:
existing_images_and_assets:
existing_tests_and_validation:
current_issues_plans_and_prs:
```

정보가 일부 없어도 저장소에서 조사할 수 있으면 바로 조사한다. 없는 사실을 추정해 구현 완료 또는 승인 상태로 기록하지 않는다.

## Operating constraints

1. 설치 전 기존 문서·이미지·코드·테스트를 감사한다.
2. 첫 단계에서 기존 파일을 대량 이동·삭제하지 않는다.
3. 기존 승인 이미지가 있으면 새 시안을 만들지 않는다.
4. 프로젝트 고유 정보는 대상 프로젝트에 둔다.
5. Base 전체를 복사하지 않고 필요한 규칙과 템플릿을 분화한다.
6. Markdown을 책임 원본으로 사용하고 열람본은 파생 산출물로 둔다.
7. `v2`, `final`, `latest`, 날짜별 활성 복제본을 만들지 않는다.
8. 사용자 승인, 구현, 검증 상태를 분리한다.
9. 자동화가 실제로 존재하고 실행되지 않았다면 설치·검증 완료로 보고하지 않는다.

## Phase 0 — Resolve scope

먼저 설치 대상과 작업 수준을 구분한다.

| 수준 | 의미 | 기본 행동 |
|---|---|---|
| Audit only | 현황과 문제만 조사 | 파일 변경 없이 감사 보고서·이관안 |
| Governance foundation | 시작 문서·지도·규칙·템플릿 설치 | 기존 문서는 연결하고 삭제하지 않음 |
| Full migration | 분야별 본책으로 내용 승계·경로 변경 | 사용자 승인된 이관표에 따라 수행 |
| Enforcement | PR 템플릿·검사·브랜치 보호 준비 | 저장소 권한과 CI 환경 확인 |

사용자가 `설치해줘`라고 명시하면 최소 `Governance foundation`까지 수행한다. 대량 삭제와 전체 이관은 감사 근거와 명시적 승인 또는 안전한 범위가 필요하다.

## Phase 1 — Repository audit

### 1.1 Read order

```text
최신 사용자 지시
→ 대상 프로젝트 AGENTS.md
→ README와 시작 문서
→ Documentation Map
→ Active Context·Handoff
→ 전체 기획·Roadmap
→ 관련 분야 문서
→ 이미지·자산 인덱스
→ Issue·Goal·Plan·PR
→ 실제 코드·데이터·Scene·테스트
→ 최근 커밋
```

`archive`, `[백업]`, `[보류]`, `hold`, `deprecated`는 기본 활성 기준에서 제외하되 고유 결정 유실 검사에는 포함한다.

### 1.2 Inventory

최소 다음 인벤토리를 만든다.

| 항목 | 현재 경로 | 주 책임 분야 | 영향 분야 | 상태 | 고유 정보 | 처리 제안 |
|---|---|---|---|---|---|---|
| 문서 |  |  |  |  |  |  |
| 이미지 |  |  |  |  |  |  |
| 코드·Scene |  |  |  |  |  |  |
| 데이터 |  |  |  |  |  |  |
| 테스트·캡처 |  |  |  |  |  |  |

### 1.3 Detect

- 중복 책임 원본
- 오래된 경로와 끊어진 링크
- 채팅에만 남은 승인 결정
- 문서상 구현과 실제 파일의 차이
- 이미지 등록과 바이너리 저장의 차이
- 승인 이미지와 실제 화면의 차이
- 분야 경계가 섞인 통합 문서
- 숫자·용어·데이터 계약 충돌
- 현재 단계와 Roadmap 불일치
- 테스트 증거 없는 완료 표시

## Phase 2 — Design the target system

### 2.1 Default structure

프로젝트 상황에 맞게 이름은 조정할 수 있지만 기본 책임은 유지한다.

```text
[기획서]/
├─ 00_프로젝트_허브/
├─ 01_설정_내러티브/
├─ 02_게임_디자인/
├─ 03_UX_UI_접근성/
├─ 04_개발_엔지니어링/
├─ 05_테크니컬아트_파이프라인/
├─ 06_아트/
├─ 07_사운드/
├─ 08_QA/
├─ 09_프로덕션_PM/
├─ 10_분석_유저리서치/
└─ 11_통합검수/
```

작은 프로젝트는 문서 수를 줄일 수 있다. 예를 들어 테크니컬 아트를 아트·개발 본책의 명시적 공동 장으로 두거나 QA와 프로덕션을 한 폴더에서 별도 장으로 관리할 수 있다. 책임 경계와 갱신 매트릭스는 유지한다.

### 2.2 Hub minimum

```text
START_HERE.md
ACTIVE_CONTEXT.md
DOCUMENTATION_MAP.md
DOCUMENTATION_SYSTEM_POLICY.md
DOCUMENT_UPDATE_MATRIX.md
DECISION_LOG.md
CHANGELOG.md
MILESTONE_GATES.md
GLOSSARY.md
AI_WORKFLOW.md
SOURCE_AUDIT.md
```

모든 파일을 무조건 만들지 않는다. 기존 책임 원본이 같은 역할을 안정적으로 수행하면 경로를 유지하고 지도에서 연결한다.

### 2.3 Discipline bible minimum

각 활성 본책은 다음을 포함한다.

- 요약과 목차
- 상태·갱신일·기준 커밋
- 확정·구현·검증·미확정 구분
- 분야 목표와 Quality Bar
- 상세 기획과 책임 경계
- 최신 이미지·캡처·자료
- 위험·의존성·다음 작업
- 완료 기준과 부록 색인

**Quality Bar(품질 기준선)**: 해당 결과가 승인되기 위해 만족해야 하는 최소 품질 기준이다.

## Phase 3 — Installation plan

`templates/project-operations/PROJECT_OPERATING_SYSTEM_INSTALLATION_PLAN.md`를 분화해 작성한다.

계획은 다음을 명시한다.

```yaml
install_scope:
files_to_create:
files_to_update:
files_to_preserve:
files_to_reclassify:
deletion_candidates:
reference_updates:
visual_migration:
github_enforcement:
validation_plan:
rollback_plan:
```

삭제 후보는 고유 결정·수치·계약이 새 원본에 승계되고 참조가 제거된 뒤에만 처리한다.

## Phase 4 — Install governance foundation

### 4.1 Project AGENTS

프로젝트 `AGENTS.md`에 다음을 연결한다.

- 기본 읽기 순서
- Base 기준 버전 또는 원격 기준
- 분야·영향도 선언
- Plan Mode와 승인 게이트
- 문서·이미지 수명주기
- 작업 종료 갱신
- 실제 검증 명령

루트 AGENTS는 라우터로 유지하고 상세 정책은 허브 문서에 둔다.

### 4.2 Start and maps

- 사용자는 `START_HERE.md`에서 프로젝트 상태를 읽는다.
- AI는 `AGENTS.md`에서 작업 규칙을 읽는다.
- `DOCUMENTATION_MAP.md`는 질문별 책임 원본을 연결한다.
- `ACTIVE_CONTEXT.md`는 현재 상태와 다음 작업만 압축한다.

### 4.3 Status and update matrix

- 분야별 본책에 공통 상태를 적용한다.
- 변경 유형별 필수 갱신 대상을 매트릭스에 기록한다.
- L1 이상 작업은 `primary_discipline`, `affected_disciplines`, `change_type`을 가진다.

### 4.4 Visual system

`VISUAL_SOURCE_OF_TRUTH.md`와 `ASSET_MANIFEST.yml`을 프로젝트 상황에 맞게 설치한다.

- 기존 승인 이미지 목록 작성
- 캐노니컬 경로 지정
- 참고·비참고 요소 기록
- Visual DNA와 실제 캡처 연결
- 새 이미지 임의 생성 금지
- 대체·이전 대기 상태 기록

### 4.5 User-readable derivatives

- Markdown을 책임 원본으로 유지한다.
- PDF·HTML·DOCX 생성 경로와 명령을 기록한다.
- 생성 도구가 없으면 열람본 자동 생성은 `미설치`로 표시한다.
- 이미지 캡션과 원본 경로를 포함한다.

## Phase 5 — Install GitHub workflow

템플릿 경로:

```text
templates/project-operations/github/
```

대상 프로젝트에 맞게 다음을 분화한다.

- Issue template: 목표, 분야, 범위, 완료 기준, 검증
- PR template: 영향 분야, 본책 갱신, 이미지·자산, 테스트, 미검증
- governance config: 경로와 변경 규칙
- governance checker: 필수 파일·링크·금지 파일명·갱신 누락 검사
- GitHub Actions workflow: PR에서 검사 실행
- CODEOWNERS 제안
- 브랜치 보호에 필요한 status check 이름

브랜치 보호 설정은 저장소 권한과 GitHub UI/API 지원이 필요하다. 파일을 추가한 것과 보호 규칙이 실제 활성화된 것을 구분한다.

## Phase 6 — Migrate content

승인된 이관표에 따라 수행한다.

```text
기존 문서
→ 주 책임 분야 1개 지정
→ 영향 분야 연결
→ 고유 결정·수치·계약 승계
→ 본책 부록 색인 등록
→ Documentation Map 갱신
→ 기존 참조 교체
→ 통합검수
→ 완전히 흡수된 중복 제거
```

여러 분야를 한 파일이 책임하던 경우 내용을 요소 단위로 분해한다. 예:

```text
UI 행동·정보 구조 → UX·UI 또는 게임
시각 언어·VFX → 아트
Import·규격·성능 → 테크니컬 아트
오디오 → 사운드
검증 → QA
전체 일치성 → 통합검수
```

원본 문서에 고유 수치·데이터 계약이 남으면 해당 분야 부록으로 유지한다.

## Phase 7 — Validation

### Structural checks

- 필수 시작 문서 존재
- 문서 지도 링크 유효
- 분야별 활성 원본 중복 없음
- 금지된 활성 버전 파일명 없음
- 캐노니컬 이미지 경로 중복 없음
- Manifest 경로 유효
- 문서 파생본 생성 상태 명시

### Traceability checks

샘플 결정 3개 이상을 선택해 다음 경로가 이어지는지 확인한다.

```text
결정
→ 본책
→ Issue·Plan
→ 실제 구현·자산
→ 테스트·캡처
→ 현재 상태
```

### Cold-start test

새 작업자 관점에서 10분 안에 다음을 찾는다.

- 핵심 게임 약속
- 현재 개발 단계
- 최우선 작업
- 확정·구현·검증·미확정
- 분야별 책임 원본
- 최신 이미지와 실제 캡처
- 실제 코드·데이터·테스트
- 작업 종료 갱신 경로

### Runtime truth

문서 감사만 수행했다면 런타임 검증 완료로 쓰지 않는다. 실제 엔진 실행·테스트·플레이를 수행하지 못했으면 미검증으로 남긴다.

## Output contract

```md
## 설치 범위
## 저장소 감사 결과
## 적용한 분야와 책임 경계
## 생성·갱신한 시작 문서와 본책
## 이미지·자산 운영체계
## GitHub Issue·PR·자동 검사
## 기존 문서 승계·보존·삭제 후보
## 실행한 구조 검증
## 실행한 런타임 검증
## 미검증 항목과 남은 위험
## 콜드 스타트 테스트 결과
## 다음 작업
```

## Failure conditions

- Base 전체를 대상 프로젝트에 복사함
- 저장소 감사 없이 폴더부터 대량 생성함
- 기존 승인 이미지를 확인하지 않고 새 시안을 만듦
- 같은 정보를 여러 본책에 전문 복사함
- Markdown와 DOCX를 둘 다 독립 원본으로 운영함
- 문서 존재를 구현·검증 완료로 표시함
- 기존 고유 결정 확인 없이 파일을 삭제함
- GitHub workflow 파일만 추가하고 브랜치 보호까지 활성화됐다고 보고함
- 자동 검사 없이 `항상 최신`을 보장한다고 주장함
- 프로젝트 저장소 접근 없이 설치 완료를 주장함

## Handoff

설치 후 프로젝트에 다음을 남긴다.

- Base 기준 커밋과 적용 날짜
- 설치된 운영체계 버전
- 프로젝트가 Base에서 추가·대체한 규칙
- 미설치 자동화와 수동 절차
- 다음 검토 트리거
- Base로 환류할 공용 교훈 후보
