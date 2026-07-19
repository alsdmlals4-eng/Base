---
name: installing-game-project-operating-system
description: Use when installing a persistent game-project repository operating system that connects schema v3 Markdown or JSON sources, current PDFs, optional derivatives, all eleven discipline skills, images, tests, gates, GitHub governance, and handoff across new chats.
---

# Installing a Game Project Operating System

## Core principle

사용자가 규칙을 기억하게 하지 말고 저장소가 규칙을 기억하게 한다.

관련 Method:

- `GAME_PROJECT_OPERATING_SYSTEM_METHOD.md`
- `DEVELOPMENT_GATES_METHOD.md`
- `DISCIPLINE_SKILL_EVOLUTION_METHOD.md`
- `DISCIPLINE_PDF_PUBLICATION_METHOD.md`

운영 중인 기존 프로젝트는 먼저 `migrating-existing-game-project-structure`를 사용한다.

## 설치 결과

- 활성 `[기획서]`가 저장소 루트에 있다.
- 프로젝트 전체와 11개 책임 분야 본책은 Registry에 등록된 단일 Markdown 또는 JSON 책임 원본이다.
- `DESIGN_DOCUMENT_REGISTRY.json`이 모든 책임과 경로를 연결한다.
- `INTERVIEW_REGISTRY.json`이 현재 인터뷰·사용자 확인·실행 프롬프트를 연결한다.
- 각 활성 기획서에 최신 PDF·Manifest와 선언한 선택 DOCX·다이어그램·승인 이미지 자산이 있다.
- `SKILL_REGISTRY.json`과 사람용 필수 PDF·선택 Markdown/DOCX/assets 스킬맵이 있다.
- 전체 스킬이 아니라 trigger에 맞는 최소 스킬만 호출된다.
- 실패·중요 결정·재사용 가능한 교훈·실제 검증 결과가 있는 스킬 호출만 Learning Log에 기록된다.
- 작업·제품 개발 게이트가 증거와 연결된다.
- 이미지의 승인·구현·검증·교체 상태와 캐노니컬 경로가 추적된다.
- PR 검사로 책임 원본·PDF·Manifest·이미지·스킬 갱신 누락을 발견한다.
- 새 AI가 과거 대화 없이 저장소만으로 작업을 재개한다.

## Trigger

- 신규 게임 프로젝트 운영체계 설치
- 문서 체계가 없는 초기 프로젝트
- GPT·Codex·GitHub가 같은 기준을 사용하게 하는 요청
- 분야별 본책·스킬·이미지·검증·사람용 문서를 연결하는 요청

## Do not use

- 이미 설치된 프로젝트의 작은 수정
- 저장소 접근 없이 실제 설치 완료 요구
- 특정 프로젝트의 세계관·수치·승인 이미지를 Base에 저장
- 감사 없이 기존 프로젝트를 대량 재배치

## Required inputs

```yaml
target_repository:
project_type: new/existing
project_stage:
engine_and_platform:
existing_agents_and_start_docs:
existing_design_documents:
existing_docx_pdf_and_images:
existing_project_skills_and_registry:
existing_tests_and_validation:
roadmap_issues_plans_prs:
protected_decisions_paths_assets:
```

## Operating constraints

1. 기존 프로젝트는 안전 마이그레이션으로 시작한다.
2. 설치 전 문서·이미지·코드·데이터·테스트·스킬·PDF를 감사한다.
3. 사용자 승인 전 기존 파일을 대량 이동·삭제·통합하지 않는다.
4. 기존 승인 이미지가 있으면 새 시안을 만들지 않는다.
5. 프로젝트 고유 정보는 대상 프로젝트에 둔다.
6. Base 전체를 복사하지 않고 필요한 Method·Skill·Template만 분화한다.
7. 신규·승인된 설치의 활성 기획서는 루트 `[기획서]`에 둔다.
8. 서술 중심 본책은 Markdown을 기본으로 하고 구조 검증 데이터는 JSON을 사용하며, 사람 기본 열람본은 최신 PDF다.
9. `v2`, `final`, `latest`, 날짜별 활성 복제본을 만들지 않는다.
10. 승인·구현·검증·미확정·보류를 분리한다.
11. 전체 skills 폴더를 기본 로드하지 않는다.
12. 자동화·렌더링·브랜치 보호가 실행되지 않았다면 완료로 보고하지 않는다.

## Phase 0 — Resolve project mode

| 프로젝트 상태 | 사용할 경로 |
|---|---|
| 신규·내용 거의 없음 | 이 스킬 계속 진행 |
| 기존 운영 중·고유 문서·자산·이력 있음 | 안전 마이그레이션으로 전환 |
| 이미 운영체계 설치됨 | 프로젝트 Registry와 현행 원본을 읽고 일반 작업 |

설치 수준:

- `Audit only`: 구조·문제·이관 계획만 작성
- `Governance foundation`: 시작 문서·Registry·게이트·스킬 계약 설치
- `Approved migration`: 승인된 처리표 기반 내용 승계
- `Enforcement`: Issue·PR·검사·브랜치 보호 연결

## Phase 1 — Repository audit

읽기 순서:

```text
최신 사용자 지시
→ AGENTS·README·START_HERE
→ Active Context·Handoff·Roadmap
→ 기존 기획서·DOCX·PDF·이미지·부록
→ Development Gates
→ Skill Registry·스킬·Learning Log
→ 실제 코드·데이터·Scene·테스트
→ Issue·Plan·PR·최근 커밋
```

조사:

- 루트가 아닌 기획서 위치·중첩 복제본
- 중복 책임 원본·오래된 링크
- Markdown·DOCX·PDF에만 남은 고유 결정
- 문서상 구현과 실제 파일 차이
- 승인 이미지와 실제 캡처 차이
- 누락된 개발 게이트·분야 책임
- 누락·중복된 분야 스킬과 과다 호출
- 사람용 기획서의 전체 과정·승인 이미지·최신성 누락
- 테스트 증거 없는 완료 표시

## Phase 2 — Install root planning structure

```text
[기획서]/
├─ 00_프로젝트_허브/
│  ├─ START_HERE.md
│  ├─ ACTIVE_CONTEXT.md
│  ├─ DOCUMENTATION_MAP.md
│  ├─ DEVELOPMENT_GATES.md
│  ├─ DESIGN_DOCUMENT_REGISTRY.json
│  ├─ SKILL_REGISTRY.json
│  ├─ INTERVIEW_REGISTRY.json
│  ├─ INTERVIEWS/
│  ├─ EXECUTABLE_PROMPTS/
│  ├─ PROJECT_SKILL_MAP.md       # 선택 자동 생성
│  ├─ PROJECT_SKILL_MAP.docx     # 선택 Word 검토
│  ├─ PROJECT_SKILL_MAP.pdf
│  ├─ PROJECT_SKILL_MAP.assets/
│  └─ SKILL_MAP_PUBLICATION_MANIFEST.json
└─ 분야별 폴더/
```

운영 라우터와 프로젝트 종합·11개 분야 기획 본책은 Markdown 단일 책임 원본으로 유지한다. Registry·Manifest·상태·ID·경로·게임 데이터만 JSON으로 관리한다.

## Phase 3 — Install project and discipline design bibles

프로젝트 전체와 11개 책임 분야를 `DESIGN_DOCUMENT_REGISTRY.json`에 모두 등록한다. 11개 분야는 모든 프로젝트에 독립 본책으로 적용한다.

각 활성 본책:

```text
분야_기획서.md 또는 분야_기획서.json
분야_기획서.docx              # 선택 출력 또는 PDF 생성 중간물
분야_기획서.pdf
분야_기획서.assets/generated/  # 필요한 문서만
분야_기획서.assets/approved/   # 승인 이미지가 있는 문서만
분야_기획서_PUBLICATION_MANIFEST.json
```

작은 프로젝트도 11개 독립 책임 원본을 유지하며, 범위가 작으면 본책 안에서 `해당 없음`과 재개 조건을 명시한다.

구조화 JSON 책임 원본 최소 내용(`source_format: json`일 때):

- 목적·플레이어 가치·현재 목표
- Quality Bar·금지 방향
- 책임·협업 경계
- 분야 전체 작업 과정
- 작업·제품 게이트
- Foundation·분야 스킬
- 확정·구현·검증·확인 필요·보류
- 결정·실제 경로·검증 증거
- 상세 기획
- 승인 이미지·실제 캡처
- 위험·다음 작업·Ready·Done

## Phase 4 — Generate human publications

설치 파일:

- `tools/build_design_documents.py`
- `tools/design_document_diagrams.py`

실행:

```text
python tools/build_design_documents.py \
  --registry "[기획서]/00_프로젝트_허브/DESIGN_DOCUMENT_REGISTRY.json" \
  --source-commit <commit>
```

생성:

- 임시 또는 Registry가 선언한 선택 DOCX
- PDF
- 작업 흐름·상태·책임 다이어그램
- 승인 이미지 포함
- 입력·생성기·출력·이미지 해시 Manifest
- PDF 전 페이지 자동 렌더 검수

사람 시각 검수는 모든 페이지를 렌더해 직접 확인한다.

## Phase 5 — Install eleven-discipline project skill system

- 공용 절차는 `skills/foundation/`에 한 번만 둔다.
- 11개 분야 모두 1:1 진입 스킬을 가진다.
- `SKILL_REGISTRY.json`은 AI 라우터다.
- `PROJECT_SKILL_MAP.pdf`와 선택 `md/docx/assets`는 사람용 파생본이다.
- `PROJECT_SKILL_MAP.md`는 수동 책임 원본으로 만들지 않는다. schema v3에서는 Registry에서 생성한 선택 요약만 허용한다.
- 실패, 중요한 결정, 재사용 가능한 교훈, 실제 검증 결과가 있는 호출은 Learning Log에 기록한다.

## Phase 6 — Install Development Gates

```text
Intake·Context
→ Definition of Ready
→ Planning·Approval
→ Implementation
→ Verification
→ Documentation
→ Integration·Completion
```

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

## Phase 7 — Install image and asset governance

- Visual Source of Truth
- Asset Manifest
- Asset ID·캐노니컬 경로
- 채택·비채택 요소
- 콘셉트·승인·제작·구현·시각 검증 상태
- 실제 게임 캡처
- 대용량 원본의 Git LFS 검토

책임 원본 또는 구조화 Asset Manifest에서 사람용 PDF와 선택 DOCX에 포함할 승인 자료를 지정한다.

## Phase 8 — Install GitHub governance

설치:

- Issue Form
- PR Template
- CODEOWNERS
- `documentation-governance.json`
- `check_documentation_governance.py`
- `check_skill_routing_governance.py`
- `check_design_document_publications.py`
- GitHub Actions

검사:

- 루트 `[기획서]`와 중첩 복제본
- Skill Registry·Learning Log·스킬맵 발행
- Design Document Registry·책임 범위
- JSON·DOCX·PDF·다이어그램·승인 이미지 해시
- 생성기 변경 후 미재생성
- 등록되지 않은 Markdown 본책과 수동 변경된 파생본 탐지
- 링크·파일명·Manifest·문서 갱신 누락

Workflow 파일 존재, 실제 실행, Required Status Check 강제를 별도 상태로 기록한다.

## Phase 9 — Existing content migration

기존 본책마다 다음을 대조한다.

```text
기존 고유 문장·표·결정·이미지·보류
→ 보존하거나 승인된 Markdown/JSON 책임 원본 위치
→ DOCX/PDF 출력 위치
→ 링크·코드·Issue 참조
→ 보존·검증 결과
```

모든 고유 정보와 참조가 검증되기 전에는 기존 원본을 삭제하지 않는다. 검증 후에도 사용자 승인 전에는 제거 후보로 유지한다.

## Phase 10 — Cold-start and Health Review

새 AI가 저장소만 보고 다음에 답할 수 있어야 한다.

- 프로젝트 목적과 핵심 경험
- 현재 구현·검증 상태
- 다음 우선 작업과 게이트
- 변경 금지 결정·자산
- 프로젝트 전체·분야별 Markdown 또는 JSON 책임 원본 위치
- 사람용 최신 PDF·DOCX·승인 이미지 위치
- 필요한 분야 스킬과 검증 방법
- 보류·확인 필요·미검증 위치

`verifying-game-project-operating-system`으로 `PASS / PARTIAL / FAIL / NOT_RUN`을 기록한다.

## Completion criteria

- 루트 `[기획서]`가 있다.
- Design Document Registry가 프로젝트 전체와 11개 책임 분야를 모두 책임진다.
- 모든 활성 본책에 등록된 단일 책임 원본·최신 PDF·Manifest와 선언한 선택 DOCX/다이어그램이 있다.
- Skill Registry와 사람용 스킬맵 발행이 일치한다.
- Development Gates·Roadmap·Active Context가 연결된다.
- 승인 이미지와 실제 캡처 상태가 추적된다.
- 네 Governance Checker가 정상·실패 시나리오에서 검증됐다.
- 새 채팅이 저장소만으로 작업을 재개한다.
- 실행하지 않은 렌더링·테스트·브랜치 보호를 완료로 보고하지 않았다.

## Learning update

설치·마이그레이션 후 Learning Log에 기록한다.

- 누락된 JSON 필드·책임 범위
- DOCX/PDF 레이아웃 결함
- 승인 이미지 경로 문제
- 다이어그램 개선점
- 불필요하게 호출한 스킬
- 콜드 스타트 실패
- 생성기·검사기 갱신 필요성
