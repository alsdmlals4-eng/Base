---
name: installing-game-project-operating-system
description: Use when creating or installing a persistent game-project repository operating system so GPT, Codex, GitHub documents, selective discipline skills, images, PDFs, tests, gates, and handoff stay aligned across new chats.
---

# Installing a Game Project Operating System

## Core principle

사용자가 규칙을 기억하게 하지 말고 저장소가 규칙을 기억하게 한다.

공용 Method:

- `docs/knowledge/methods/GAME_PROJECT_OPERATING_SYSTEM_METHOD.md`
- `docs/knowledge/methods/DEVELOPMENT_GATES_METHOD.md`
- `docs/knowledge/methods/DISCIPLINE_SKILL_EVOLUTION_METHOD.md`
- `docs/knowledge/methods/DISCIPLINE_PDF_PUBLICATION_METHOD.md`

복사·분화 템플릿: `templates/project-operations/`

운영 중인 기존 프로젝트는 먼저 `skills/migrating-existing-game-project-structure/SKILL.md`를 사용한다.

## 설치 결과

폴더 생성이 아니라 다음 상태를 만든다.

- 활성 `[기획서]`가 저장소 루트 바로 아래에 있다.
- 새 GPT와 Codex가 같은 시작 문서를 읽는다.
- 질문별 현행 책임 원본이 하나다.
- 작업·제품 개발 게이트가 증거와 연결된다.
- 사람용 Project Skill Map과 기계 판독 Skill Registry가 있다.
- 전체 스킬이 아니라 trigger에 맞는 최소 스킬만 호출된다.
- 공용 Foundation 스킬과 분야별 프로젝트 스킬이 분리된다.
- 모든 의미 있는 스킬 호출이 Learning Log에 기록된다.
- 변경 시 본책·Roadmap·Registry·스킬·Manifest·PDF·상태 문서를 갱신한다.
- 이미지의 승인·구현·검증·교체 상태와 캐노니컬 경로가 추적된다.
- 분야 PDF가 전체 과정과 승인 이미지를 포함하고 최신성이 추적된다.
- PR 검사로 문서·이미지·스킬·PDF 누락을 발견할 수 있다.
- 새 작업자가 과거 대화 없이 저장소만으로 작업을 재개한다.
- 설치 후 Health Review로 실제 연결 상태를 확인한다.

## Trigger

- 신규 게임 프로젝트의 운영 구조 설치
- 문서 체계가 없는 초기 프로젝트
- Base를 참고해 프로젝트 작업 구조를 설계
- GPT·Codex·GitHub가 같은 기준을 사용하게 하는 요청
- 분야별 본책·스킬·이미지·PDF·검증을 연결하는 요청

이미 운영 중이며 기존 문서·자산·이력이 있는 프로젝트는 안전 마이그레이션 스킬로 라우팅한다.

## Do not use

- 오탈자 한 줄 수정
- 이미 설치된 프로젝트의 작은 구현만 수행
- 저장소 접근 없이 실제 설치 완료 요구
- 특정 프로젝트의 GDD·수치·이미지를 Base에 직접 저장
- 감사 없이 기존 프로젝트 폴더를 대량 재배치

## Required inputs

```yaml
target_repository:
local_checkout:
current_branch:
project_type: new/existing
project_stage:
engine_and_platform:
existing_agents:
existing_start_and_map:
existing_active_context:
existing_design_docs:
existing_project_skills:
existing_skill_registry:
existing_skill_learning_logs:
existing_images_and_assets:
existing_pdfs_and_publication_manifest:
existing_tests_and_validation:
current_roadmap_issues_plans_prs:
```

정보가 없어도 저장소에서 조사할 수 있으면 조사한다. 없는 사실을 승인·구현·검증 완료로 기록하지 않는다.

## Operating constraints

1. 기존 프로젝트는 안전 마이그레이션 스킬로 시작한다.
2. 설치 전 현재 문서·이미지·코드·데이터·테스트·PDF·스킬을 감사한다.
3. 첫 단계에서 기존 파일을 대량 이동·삭제하지 않는다.
4. 기존 승인 이미지가 있으면 새 시안을 만들지 않는다.
5. 프로젝트 고유 정보는 대상 프로젝트에 둔다.
6. Base 전체를 복사하지 않고 필요한 Method·Skill·Template만 분화한다.
7. 신규·승인된 설치의 활성 기획서는 루트 `[기획서]`에 둔다.
8. Markdown·구조화 데이터가 책임 원본이고 PDF·DOCX는 파생본이다.
9. `v2`, `final`, `latest`, 날짜별 활성 복제본을 만들지 않는다.
10. 승인·구현·검증·미확정·보류를 분리한다.
11. 전체 skills 폴더를 기본 로드하지 않는다.
12. 모든 의미 있는 스킬 호출은 Learning Log에 기록한다.
13. 자동화·PDF·브랜치 보호가 실행되지 않았다면 완료로 보고하지 않는다.

## Phase 0 — Resolve project mode

| 프로젝트 상태 | 사용할 경로 |
|---|---|
| 신규·내용 거의 없음 | 이 스킬 계속 진행 |
| 기존 운영 중·고유 문서/자산/이력 있음 | `migrating-existing-game-project-structure`로 전환 |
| 이미 운영체계 설치됨 | 프로젝트 AGENTS·Map·Registry를 읽고 일반 작업 진행 |

설치 수준:

| 수준 | 의미 | 기본 행동 |
|---|---|---|
| Audit only | 현황과 문제 조사 | 파일 변경 없이 보고서·설계안 |
| Governance foundation | 시작 문서·지도·게이트·스킬 계약 설치 | 기존 원본 연결, 삭제 없음 |
| Approved migration | 승인된 처리표 기반 내용 승계·경로 변경 | 보존 대조 필수 |
| Enforcement | Issue·PR·검사·브랜치 보호 | 실제 실행·강제 상태 검증 |

## Phase 1 — Repository audit

### Read order

```text
최신 사용자 지시
→ 대상 프로젝트 AGENTS.md
→ README·START_HERE
→ Base version·Documentation Map
→ Active Context·Handoff
→ 방향·전체 기획·Roadmap
→ 분야별 본책·부록
→ Development Gates
→ Project Skill Map·Skill Registry·Learning Logs
→ Visual Source·Manifest·승인 이미지
→ PDF·Publication Manifest
→ Issue·Goal·Plan·PR
→ 실제 코드·데이터·Scene·테스트
→ 최근 커밋
```

`[백업]`, `[보류]`, `[제거 후보]`, archive·hold·deprecated는 기본 활성 기준에서 제외하되 고유 정보 감사에는 포함한다.

### Inventory

| 항목 | 현재 경로 | 주 책임 | 영향 분야 | 상태 | 고유 정보 | 참조 | 처리 제안 |
|---|---|---|---|---|---|---|---|
| 문서·스킬·PDF·이미지·코드·데이터·테스트 |  |  |  |  |  |  |  |

### Detect

- 활성 `[기획서]`가 루트가 아닌 위치에 있거나 중첩 복제됨
- 중복 책임 원본과 오래된 링크
- 채팅에만 남은 승인 결정
- 문서상 구현과 실제 파일 차이
- 이미지 등록과 바이너리 저장 차이
- 승인 이미지와 실제 화면 차이
- 누락된 작업·제품 게이트
- 누락·중복된 분야 스킬과 공용 절차 복제
- Skill Registry·Map·실제 경로 불일치
- trigger·비사용 조건·Learning Log 누락
- 전체 스킬 자동 로드 또는 불필요한 과다 호출
- 분야 PDF의 전체 과정·승인 이미지·최신성 누락
- 숫자·용어·데이터 계약 충돌
- Roadmap·Issue·현재 상태 불일치
- 테스트 증거 없는 완료 표시

## Phase 2 — Design target responsibility system

### Root planning folder

신규 프로젝트의 목표:

```text
<repository-root>/[기획서]/
└─ 00_프로젝트_허브/
```

기존 프로젝트는 안전 마이그레이션 감사와 사용자 승인 후에만 이동한다. 중첩 현행 기획서 복제본은 만들지 않는다.

### Project hub minimum responsibilities

- START_HERE
- Active Context·Handoff
- Documentation Map
- Development Gates
- Project Skill Map
- Skill Registry
- Document Update Matrix
- Decision Log·Changelog
- AI Workflow
- Publication Manifest
- Source·Migration Audit
- Lifecycle areas
- Operating System Health Review

모든 파일을 무조건 만들지 않는다. 기존 원본이 같은 역할을 안정적으로 수행하면 감사·승인 후 경로를 유지하고 Map에서 연결한다.

### Discipline responsibilities

1. 설정·내러티브
2. 게임 디자인
3. UX·UI·접근성
4. 개발·엔지니어링
5. 테크니컬 아트·파이프라인
6. 아트
7. 사운드
8. QA
9. 프로덕션·PM
10. 분석·유저리서치
11. 통합검수

작은 프로젝트는 문서를 통합할 수 있지만 책임, 입력·출력, 프로젝트 스킬과 갱신 매트릭스는 유지한다.

### Discipline bible minimum

- 한눈에 보기·목차
- 목적·Quality Bar·금지 방향
- 책임·협업 경계
- 전체 작업 과정
- 작업·제품 개발 게이트
- Registry ID와 필요한 Foundation·분야 프로젝트 스킬
- 확정·구현·검증·미확정·보류
- 최신 이미지·실제 캡처
- 실제 파일·테스트
- 위험·다음 작업·완료 기준
- PDF 발행 상태·부록·변경·학습 이력

## Phase 3 — Install Development Gates

템플릿: `templates/project-operations/DEVELOPMENT_GATES.md`

작업 게이트:

```text
Intake·Context
→ Definition of Ready
→ Planning·Approval
→ Implementation
→ Verification
→ Documentation
→ Integration·Completion
```

제품 게이트:

```text
Concept
→ Prototype
→ Graybox
→ First Playable
→ Vertical Slice
→ Production
→ Alpha
→ Feature Complete
→ Content Complete
→ Beta
→ Release Candidate
```

현재 단계, 다음 Greenlight, 진입·종료 기준, Quality Bar, 증거와 미검증을 기록한다.

## Phase 4 — Install selective project skill system

실행 스킬: `skills/evolving-project-discipline-skills/SKILL.md`

템플릿:

- `PROJECT_SKILL_MAP.md`
- `SKILL_REGISTRY.json`
- `skills/FOUNDATION_SKILL.md`
- `skills/DISCIPLINE_SKILL.md`
- `skills/SKILL_LEARNING_LOG.md`

설치 규칙:

- 공용 절차는 Foundation에서 한 번만 책임진다.
- 각 활성 분야는 진입 프로젝트 스킬 또는 명시적 통합 책임을 가진다.
- 분야 스킬은 본책·실제 경로·산출물·Quality Bar·검증·실패 조건을 연결한다.
- Registry에 skill ID, layer, discipline, path, status, trigger tags, 사용·비사용 조건, Learning Log, review trigger와 지식 상태를 등록한다.
- `load_all_skills=false`, `default_selection=none`, `load_by_default=false`를 기본값으로 둔다.
- 새 요청은 `routing-project-work-by-discipline`로 최소 스킬 집합을 판정한다.
- 검증·PDF·Handoff 스킬은 해당 단계에서만 후속 호출한다.
- 모든 의미 있는 실제 작업 후 Learning Log에 결과와 변경 필요성을 기록한다.
- 스킬 본문은 근거가 있을 때만 갱신한다.

## Phase 5 — Install governance foundation

### Project AGENTS

- 루트 `[기획서]`와 기본 읽기 순서
- Base 기준 버전
- 분야·영향도·변경 유형 선언
- Skill Registry 기반 선택적 호출
- 개발 게이트와 승인
- 문서·이미지·PDF 수명주기
- 모든 스킬 호출의 Learning Log
- 작업 종료 갱신
- 실제 검증 명령

루트 AGENTS는 라우터로 유지하고 상세 정책은 허브 문서와 Skill에 둔다.

### Start and maps

- 사용자는 루트 `[기획서]/00_프로젝트_허브/START_HERE.md`에서 상태를 읽는다.
- AI는 `AGENTS.md`에서 실행 규칙을 읽는다.
- `DOCUMENTATION_MAP.md`는 질문별 책임 원본을 연결한다.
- `SKILL_REGISTRY.json`은 trigger 기반 후보를 기계 판독한다.
- `PROJECT_SKILL_MAP.md`는 사람용 책임·관계를 설명한다.
- `ACTIVE_CONTEXT.md`는 현재 상태와 다음 작업만 압축한다.

### Lifecycle

- `[현행]`: 활성 책임 원본·스킬
- `[백업]`: 외부 원본·감사·승인 근거
- `[보류]`: 재개 조건이 있는 미래 항목
- `[제거 후보]`: 보존·참조·복구·승인 대기

## Phase 6 — Install visual and publication systems

- Visual Source와 Asset Manifest를 설치한다.
- 기존 승인 이미지에 새 시안을 임의 생성하지 않는다.
- 캐노니컬 경로, 채택·비채택 요소, 실제 캡처와 Visual DNA를 연결한다.
- 분야 PDF 발행 계획과 Publication Manifest를 설치한다.
- PDF는 전체 과정과 승인 이미지를 포함한다.
- 입력 hash, PDF header와 visual review를 추적한다.
- 생성 파이프라인이 없으면 `NOT_BUILT`로 남긴다.

## Phase 7 — Install GitHub workflow

대상 프로젝트에 맞게 분화한다.

- Issue Form: 목표, 분야, 범위, Ready, 선택 스킬, 검증
- PR Template: 게이트, 본책, Registry, 스킬, Learning Log, Manifest, PDF, 미검증
- CODEOWNERS: 분야 본책·스킬·자동화 책임
- Documentation Governance Checker
- Skill Routing Governance Checker
- GitHub Actions Workflow
- Required Status Check·브랜치 보호 계획

두 Checker는 최소 다음을 검사한다.

- 루트 `[기획서]`와 중첩 복제본
- 필수 시작 문서·링크·금지 파일명
- Asset ID·캐노니컬 경로
- Skill Registry JSON·중복 ID·경로·trigger·Learning Log
- 분야 진입 스킬과 전체 스킬 자동 로드 금지
- 스킬 변경 시 Registry·Map·Learning Log 동기화
- 변경 유형별 본책 갱신
- PDF 입력 hash·header·visual review·Manifest

브랜치 보호 설정은 파일 존재와 실제 활성 상태를 구분한다.

## Phase 8 — Validate

### Structural checks

- 루트 `[기획서]` 존재·중첩 복제 없음
- 필수 시작 문서 존재
- Documentation Map·Skill Registry 링크 유효
- 분야별 활성 원본 중복 없음
- 금지 활성 버전 파일명 없음
- 캐노니컬 이미지·Skill ID 중복 없음
- 활성 스킬 경로·Learning Log 존재
- 모든 11개 책임 분야 진입 스킬 등록
- 전체 스킬 자동 로드 금지
- PDF Manifest·입력·출력 상태 유효

### Traceability checks

샘플 결정 3개 이상을 선택한다.

```text
결정
→ 본책
→ Issue·Plan
→ 실제 구현·자산
→ 테스트·캡처
→ 현재 상태·PDF
```

샘플 작업 3개 이상에서 라우팅 결과를 확인한다.

```text
요청
→ 주 책임 분야
→ 최소 Foundation·분야 스킬
→ 실제 파일·검증
→ Learning Log
```

### Regression tests

- 정상 구성 통과
- 중첩 `[기획서]` 실패
- `load_all_skills=true` 실패
- 분야 진입 스킬 누락 실패
- Learning Log 경로 누락 실패
- 스킬 변경 후 Registry·Map·Log 미갱신 실패
- 금지 활성 파일명·PDF stale 실패

### Cold-start test

새 작업자 관점에서 10분 안에 다음을 찾는다.

- 루트 `[기획서]`
- 핵심 게임 약속
- 현재 개발 단계와 최우선 작업
- 확정·구현·검증·미확정
- 분야별 책임 본책·Registry 진입 스킬
- 현재 요청에 필요한 최소 스킬
- 최신 이미지·실제 캡처·PDF
- 실제 코드·데이터·테스트
- 작업 종료 갱신·Learning Log

## Phase 9 — Operating System Health Review

`skills/verifying-game-project-operating-system/SKILL.md`와 `OPERATING_SYSTEM_HEALTH_REPORT.md`를 사용한다.

설치 상태는 다음을 구분한다.

- 설계됨
- 설치됨
- 실행 확인
- 강제됨
- 미검증

Workflow 파일·Registry·PDF 계획이 있다는 사실만으로 실행 확인이나 강제 상태로 표시하지 않는다.

## Output contract

```md
## 설치 범위
## 루트 기획서 위치
## 저장소 감사 결과
## 적용한 분야와 책임 경계
## 생성·갱신한 시작 문서와 본책
## Skill Registry·Map·선택적 호출
## 분야·Foundation 스킬과 Learning Log
## 개발 게이트
## 이미지·자산·PDF 운영체계
## GitHub Issue·PR·자동 검사
## 기존 문서 승계·보존·삭제 후보
## 실행한 구조·회귀 검증
## 실행한 런타임 검증
## 운영체계 Health Review
## 미검증 항목과 남은 위험
## 콜드 스타트 테스트 결과
## 다음 작업
```

## Failure conditions

- Base 전체를 대상 프로젝트에 복사함
- 저장소 감사 없이 폴더부터 대량 생성함
- 신규 설치인데 `[기획서]`를 중첩 경로에 둠
- 기존 승인 이미지를 확인하지 않고 새 시안을 만듦
- 같은 정보를 여러 본책에 전문 복사함
- 전체 skills 폴더를 기본 로드함
- Registry·Map·Learning Log 없이 스킬 폴더만 만듦
- trigger·비사용 조건 없는 스킬을 활성화함
- 스킬 호출 결과를 기록하지 않음
- Markdown와 PDF를 둘 다 독립 원본으로 운영함
- 문서 존재를 구현·검증 완료로 표시함
- 기존 고유 결정 확인 없이 파일을 삭제함
- Workflow 파일만 추가하고 브랜치 보호까지 활성화됐다고 보고함
- 자동 검사 없이 `항상 최신`을 보장한다고 주장함
- 저장소 접근 없이 설치 완료를 주장함

## Handoff

설치 후 프로젝트에 다음을 남긴다.

- Base 기준 커밋과 적용 날짜
- 설치된 운영체계 버전
- 루트 `[기획서]` 경로
- 프로젝트가 Base에서 추가·대체한 규칙
- Skill Registry·Map·Learning Log 경로
- 미설치 자동화와 수동 절차
- Health Review 결과
- 다음 검토 트리거
- Base로 환류할 공용 교훈 후보
