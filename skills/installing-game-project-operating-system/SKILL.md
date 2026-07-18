---
name: installing-game-project-operating-system
description: Use when creating or installing a persistent game-project repository operating system so GPT, Codex, GitHub documents, discipline skills, images, PDFs, tests, gates, and handoff stay aligned across new chats.
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

- 새 GPT와 Codex가 같은 시작 문서를 읽는다.
- 질문별 현행 책임 원본이 하나다.
- 작업·제품 개발 게이트가 증거와 연결된다.
- 모든 L1 이상 작업이 주 책임 분야와 영향 분야를 가진다.
- 공용 foundation 스킬과 분야별 프로젝트 스킬이 분리된다.
- 변경 시 본책·Roadmap·스킬·Manifest·PDF·상태 문서를 갱신한다.
- 이미지의 승인·구현·검증·교체 상태와 캐노니컬 경로가 추적된다.
- 분야 PDF가 전체 과정과 승인 이미지를 포함하고 최신성이 추적된다.
- PR 검사로 문서·이미지·스킬·PDF 누락을 발견할 수 있다.
- 새 작업자가 과거 대화 없이 저장소만으로 작업을 재개한다.

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
7. Markdown·구조화 데이터가 책임 원본이고 PDF·DOCX는 파생본이다.
8. `v2`, `final`, `latest`, 날짜별 활성 복제본을 만들지 않는다.
9. 승인·구현·검증·미확정·보류를 분리한다.
10. 자동화·PDF·브랜치 보호가 실행되지 않았다면 완료로 보고하지 않는다.

## Phase 0 — Resolve project mode

| 프로젝트 상태 | 사용할 경로 |
|---|---|
| 신규·내용 거의 없음 | 이 스킬 계속 진행 |
| 기존 운영 중·고유 문서/자산/이력 있음 | `migrating-existing-game-project-structure`로 전환 |
| 이미 운영체계 설치됨 | 프로젝트 AGENTS·Map·Skill Map을 읽고 일반 작업 진행 |

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
→ Project Skill Map·분야별 스킬
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

- 중복 책임 원본과 오래된 링크
- 채팅에만 남은 승인 결정
- 문서상 구현과 실제 파일 차이
- 이미지 등록과 바이너리 저장 차이
- 승인 이미지와 실제 화면 차이
- 누락된 작업·제품 게이트
- 누락·중복된 분야 스킬과 공용 절차 복제
- 분야 PDF의 전체 과정·승인 이미지·최신성 누락
- 숫자·용어·데이터 계약 충돌
- Roadmap·Issue·현재 상태 불일치
- 테스트 증거 없는 완료 표시

## Phase 2 — Design target responsibility system

### Project hub minimum responsibilities

- START_HERE
- Active Context·Handoff
- Documentation Map
- Development Gates
- Project Skill Map
- Document Update Matrix
- Decision Log·Changelog
- AI Workflow
- Publication Manifest
- Source·Migration Audit
- Lifecycle areas

모든 파일을 무조건 만들지 않는다. 기존 원본이 같은 역할을 안정적으로 수행하면 경로를 유지한다.

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
- Foundation·분야 프로젝트 스킬
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

## Phase 4 — Install project skill system

실행 스킬: `skills/evolving-project-discipline-skills/SKILL.md`

템플릿:

- `PROJECT_SKILL_MAP.md`
- `skills/FOUNDATION_SKILL.md`
- `skills/DISCIPLINE_SKILL.md`
- `skills/SKILL_LEARNING_LOG.md`

설치 규칙:

- 공용 절차는 foundation에서 한 번만 책임진다.
- 각 활성 분야는 진입 프로젝트 스킬 또는 명시적 통합 책임을 가진다.
- 분야 스킬은 본책·실제 경로·산출물·Quality Bar·검증·실패 조건을 연결한다.
- 전체 skills 폴더를 읽지 않고 현재 작업에 필요한 스킬만 선택한다.
- 실제 작업·피드백·실패 후 Learning Log와 스킬 계약을 갱신한다.

## Phase 5 — Install governance foundation

### Project AGENTS

- 기본 읽기 순서
- Base 기준 버전
- 분야·영향도 선언
- 개발 게이트와 승인
- 문서·이미지·PDF 수명주기
- 프로젝트 스킬 학습
- 작업 종료 갱신
- 실제 검증 명령

루트 AGENTS는 라우터로 유지하고 상세 정책은 허브 문서와 Skill에 둔다.

### Start and maps

- 사용자는 START_HERE에서 현재 상태를 읽는다.
- AI는 AGENTS에서 규칙을 읽는다.
- Documentation Map은 질문별 책임 원본을 연결한다.
- Project Skill Map은 foundation + 분야 스킬을 연결한다.
- Active Context는 현재 사실과 다음 작업만 압축한다.

### Status·update matrix

L1 이상 작업은 `primary_discipline`, `affected_disciplines`, `change_type`, `foundation_skills`, `discipline_skills`를 가진다.

## Phase 6 — Install visual system

`VISUAL_SOURCE_OF_TRUTH.md`와 `ASSET_MANIFEST.yml`을 분화한다.

- 기존 승인 이미지 인벤토리
- Asset ID·캐노니컬 경로
- 참고·비참고 요소
- Visual DNA·실제 캡처
- 새 이미지 임의 생성 금지
- 대체·이전 대기 상태

## Phase 7 — Install user-readable PDF publications

실행 스킬: `skills/publishing-discipline-bibles/SKILL.md`

- 분야 Markdown과 활성 부록을 책임 원본으로 사용
- 승인 이미지와 실제 캡처 포함
- 분야 목적부터 전체 과정·현재 상태·다음 작업까지 구성
- 재현 가능한 생성 명령
- Publication Manifest에 입력·출력·해시·시각 검수 기록
- 파이프라인 미설치 시 `NOT_BUILT`
- 원본 변경 시 `STALE` 또는 재생성
- 렌더링 검수 전 `CURRENT` 금지

## Phase 8 — Install GitHub workflow

대상 프로젝트에 맞게 분화한다.

- Issue Form: 목표·분야·Ready·스킬·검증
- PR Template: 게이트·본책·스킬·Manifest·PDF·미검증
- Governance config·checker
- GitHub Actions
- CODEOWNERS
- Required Status Check 이름

`파일 존재`, `실행 확인`, `강제됨`을 구분한다.

## Phase 9 — Migrate content when approved

기존 프로젝트는 안전 마이그레이션 Skill과 승인된 처리표를 따른다.

```text
기존 원본
→ 주 책임 분야 지정
→ 고유 결정·수치·계약 추출
→ 본책·스킬·Manifest·PDF 계획으로 승계
→ Documentation Map·참조 갱신
→ 변경 전후 보존 대조
→ 통합검수
→ 완전히 흡수된 중복만 제거 후보 처리
```

## Phase 10 — Validation

### Structural

- 필수 시작·게이트·스킬 지도 존재
- 분야별 활성 원본·진입 스킬 중복 없음
- 링크·Manifest·캐노니컬 경로 유효
- 금지 활성 버전 파일명 없음
- 백업·보류·제거 후보 기본 읽기 제외

### PDF

- 책임 Markdown·승인 이미지·PDF 존재
- Publication Manifest 입력 해시 일치
- 실제 PDF 헤더
- 목차·표·이미지·링크·한글 렌더링 검수
- 원본 변경 PR에서 PDF·Manifest 동기화

### Traceability

결정 3개 이상:

```text
결정
→ 본책
→ 프로젝트 스킬
→ Issue·Plan
→ 구현·자산
→ 테스트·캡처
→ PDF·현재 상태
```

### Cold start

새 작업자가 10분 안에 찾는다.

- 핵심 게임 약속
- 현재 단계·다음 게이트
- 최우선 작업
- 승인·구현·검증·미확정·보류
- 분야별 본책·프로젝트 스킬
- 최신 승인 이미지·실제 캡처·PDF
- 실제 파일·테스트
- 작업 종료 갱신 경로

### Runtime truth

문서 감사만 수행했다면 런타임 검증 완료로 쓰지 않는다.

## Output contract

```md
## 설치 범위·프로젝트 유형
## 저장소 감사·보존 결과
## 적용한 분야·책임 원본
## 개발 게이트
## Foundation·분야 프로젝트 스킬
## 이미지·자산 운영체계
## 분야 PDF·Publication Manifest
## GitHub Issue·PR·자동 검사
## 기존 문서 승계·백업·보류·제거 후보
## 실행한 구조·PDF·런타임 검증
## 미검증·남은 위험
## 콜드 스타트 결과
## 다음 작업·Base 동기화
```

## Failure conditions

- 기존 프로젝트를 신규처럼 취급해 폴더부터 대량 생성
- Base 전체 복사
- 고유 결정·보류·참조 감사 없는 삭제·통합
- 승인 이미지 확인 없는 새 시안
- 공용 절차를 모든 분야 스킬에 장문 복사
- Markdown와 PDF·DOCX를 독립 원본으로 운영
- PDF가 요약만 포함하거나 승인 이미지를 누락
- 문서·PDF 존재를 구현·검증 완료로 표시
- Workflow 파일만 추가하고 브랜치 보호까지 활성화됐다고 보고
- 실제 검증 없이 `항상 최신`을 보장한다고 주장

## Handoff

- Base 기준 커밋·적용 날짜
- 설치된 운영체계 상태
- 프로젝트가 추가·대체한 규칙
- 현재 게이트·다음 Greenlight
- 프로젝트 스킬 지도·학습 상태
- PDF 생성·검수·강제 상태
- 미설치 자동화와 수동 절차
- 다음 검토 트리거
- Base 환류 후보
