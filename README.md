# Base

여러 게임 프로젝트가 공유하는 **[학습형] [공용] AI 작업 규칙, 설계 방법, 실행 스킬, 템플릿과 검증 사례**의 원본 저장소입니다.

Base는 `어떻게 판단하고 작업하며 검증할 것인가`를 관리합니다. 각 프로젝트의 세계관, 규칙, 수치, 엔진, 실제 경로, 승인 이미지와 구현 상태는 프로젝트 저장소가 책임집니다.

## 가장 먼저 읽기

```text
START_HERE.md
→ AGENTS.md
→ docs/DOCUMENTATION_MAP.md
→ skills/SKILL_REGISTRY.json
→ 현재 작업에 필요한 Method·Skill·Template·Case
→ 대상 프로젝트의 Markdown 또는 JSON 책임 원본과 실제 파일
```

- [Base 시작 지점](START_HERE.md)
- [공용 AI 작업 규칙](AGENTS.md)
- [문서·스킬 역할표](docs/DOCUMENTATION_MAP.md)
- [공용 스킬 Registry](skills/SKILL_REGISTRY.json)
- [공용 스킬 학습 기록](skills/SKILL_LEARNING_LOG.md)
- [Base 수정제안서]([수정제안서]/README.md)
- [Ouroboros 딥인터뷰 Source Audit](docs/knowledge/research/OUROBOROS_DEEP_INTERVIEW_SOURCE_AUDIT.md)

## 사용자가 기억할 최소 요청

> `https://github.com/alsdmlals4-eng/Base 를 전부 살펴보고 참고해서 이 프로젝트를 작업해줘.`

저장소 접근이 가능한 GPT·Codex는 모든 파일과 스킬을 무작정 읽지 않습니다. Registry와 Documentation Map에서 현재 작업에 필요한 책임 원본과 최소 스킬만 선택합니다.

작업에 필요한 실행 파일·라이브러리·폰트·입력 파일·인증·권한이 없으면 AI는 필요한 이유, 설치·적용 방법, 확인 명령과 최소 권한 범위를 사용자에게 요청합니다. 승인 없이 시스템 전역 설치나 권한 확대를 수행하지 않으며, 설치 완료 후 실제 환경을 다시 검증합니다.

## 프로젝트 기획서 구조

신규 프로젝트와 승인된 마이그레이션의 활성 기획서는 저장소 루트 아래에 둡니다.

```text
<repository-root>/[기획서]/
```

### AI·자동 검사

```text
DESIGN_DOCUMENT_REGISTRY.json
→ 프로젝트 종합 기획서 책임 원본
→ 분야별 Markdown 또는 JSON 책임 원본
→ 실제 코드·데이터·자산·테스트 경로
```

### 사람 열람

```text
기획서 PDF
→ 가장 먼저 보는 최신 통합본

기획서 DOCX
→ 문서 형식 검토용 파생본

기획서.assets/
→ 자동 다이어그램·승인 이미지·실제 캡처
```

### 최신성

```text
기획서_PUBLICATION_MANIFEST.json
→ JSON·생성기·DOCX·PDF·다이어그램·승인 이미지 해시
```

서술 중심 기획은 Markdown을 기본 책임 원본으로, Registry·Manifest·상태·ID·경로·게임 데이터는 JSON으로 관리합니다. 각 문서는 단일 책임 원본만 가지며 PDF는 항상 동기화합니다. DOCX와 다이어그램은 필요한 경우의 선택 파생본입니다.

`START_HERE`, `ACTIVE_CONTEXT`, `DOCUMENTATION_MAP`, 작업 절차와 Skill처럼 빠른 라우팅이 필요한 운영 문서는 Markdown을 유지할 수 있습니다.

## 프로젝트 스킬맵

```text
SKILL_REGISTRY.json
→ AI의 선택적 호출 원본

PROJECT_SKILL_MAP.pdf
→ 사람이 보는 이미지 포함 최신본

PROJECT_SKILL_MAP.md 또는 PROJECT_SKILL_MAP.docx
→ 문서 검토용 파생본

PROJECT_SKILL_MAP.assets/
→ 호출 흐름·분야 라우팅·상태 매트릭스
```

`PROJECT_SKILL_MAP.md`는 설정한 프로젝트에서만 자동 생성하며 수동 책임 원본으로 사용하지 않습니다.

## 운영 모델

```text
Base 공용 Method·Skill·Template·Test
→ Registry로 필요한 스킬만 선택
→ 프로젝트의 등록된 Markdown 또는 JSON 책임 원본과 실제 경로로 분화
→ 기획·구현·제작·검증
→ DOCX/PDF·다이어그램·승인 이미지 발행
→ 성공·실패·미검증을 Learning Log에 기록
→ 반복 검증된 공용 원리는 [수정제안서]에 먼저 제출
→ 사용자 승인 뒤 별도 구현 PR로 Base에 환류
```

## 저장소 구조

```text
START_HERE.md      새 채팅·새 AI 최초 라우터
AGENTS.md          공용 실행 규칙
README.md          저장소 개요
docs/              Method·Research·Case·체크리스트
skills/            실행 Skill·Registry·Learning Log
templates/         프로젝트 분화 템플릿
tools/             DOCX/PDF·다이어그램 생성기
tests/             운영체계·발행·Governance 회귀 테스트
[수정제안서]/      프로젝트발 Base 승격 후보·승인·구현 이력
```

## 기본 책임 분야

1. 설정·내러티브
2. 게임 디자인
3. UX·UI·접근성
4. 개발·엔지니어링
5. 테크니컬 아트·콘텐츠 파이프라인
6. 아트
7. 사운드
8. QA
9. 프로덕션·PM
10. 분석·유저리서치
11. 통합검수

작은 프로젝트는 본책을 통합할 수 있지만 `responsibility_coverage`에서 모든 책임을 보존합니다.

## 핵심 Method

| Method | 역할 |
|---|---|
| `GAME_PROJECT_OPERATING_SYSTEM_METHOD.md` | 프로젝트 허브·본책·스킬·이미지·GitHub 운영체계 |
| `DEVELOPMENT_GATES_METHOD.md` | 작업 게이트와 제품 마일스톤 Greenlight |
| `EXISTING_PROJECT_SAFE_MIGRATION_METHOD.md` | 기존 프로젝트의 안전한 구조 마이그레이션 |
| `DISCIPLINE_SKILL_EVOLUTION_METHOD.md` | 선택적 호출·분야별 학습·Base 환류 |
| `DISCIPLINE_PDF_PUBLICATION_METHOD.md` | Markdown·JSON 책임 원본에서 최신 PDF와 선택 파생본 발행 |
| `PROJECT_HANDOFF_CONTEXT_METHOD.md` | 새 AI 콜드 스타트와 인수인계 |

## 주요 실행 스킬

| Skill | 사용할 때 |
|---|---|
| `routing-project-work-by-discipline` | 주 책임 분야·영향 분야·최소 스킬 판정 |
| `conducting-deep-requirement-interviews` | 저장소 사실 조사·사용자 결정·마지막 확인을 실행 전에 연결 |
| `installing-game-project-operating-system` | 신규·미설치 프로젝트 운영체계 설치 |
| `migrating-existing-game-project-structure` | 기존 프로젝트 안전 감사·재배치 |
| `evolving-project-discipline-skills` | 분야별 스킬 생성·통합·학습 |
| `publishing-discipline-bibles` | Markdown·JSON 기획서의 PDF·선택 파생본 발행·검수 |
| `maintaining-project-context-and-handoff` | 현재 상태·다음 작업·위험 압축 |
| `verifying-game-project-operating-system` | 설치·마이그레이션·주요 게이트 후 Health Review |
| `promoting-project-knowledge` | 프로젝트 교훈을 Base 수정제안서로 분리·제출 |
| `reviewing-and-implementing-base-change-proposals` | 승인된 제안만 별도 PR로 검토·구현 |
| `designing-vertical-slices` | 대표 구간의 목표 품질·파이프라인 검증 |
| `writing-game-design-documents` | 기획 책임 원본과 추적 구조 설계 |

## 게임 프로젝트 운영 키트

`templates/project-operations/`에는 다음이 있습니다.

- 루트 `[기획서]`·시작 문서·Documentation Map
- `DESIGN_DOCUMENT_REGISTRY.json`
- `DESIGN_DOCUMENT.json`
- Markdown/JSON → PDF·Manifest·선택 DOCX/다이어그램 생성 파이프라인
- `SKILL_REGISTRY.json`과 사람용 스킬맵 발행 구조
- Development Gates·Document Update Matrix
- Foundation·분야 스킬·Learning Log
- Visual Source of Truth·Asset Manifest
- Issue·PR·CODEOWNERS·세 종류 Governance Checker
- 운영체계 Health Review

템플릿 폴더를 그대로 복사하지 않습니다. 기존 프로젝트는 `Audit only`로 현재 책임·참조·고유 정보를 조사하고 승인된 범위만 변경합니다.

## 개발 게이트

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

## 선택적 호출과 항상 학습

- 전체 skills 폴더를 기본 로드하지 않습니다.
- 활성 스킬도 `load_by_default=false`입니다.
- 주 책임 분야 스킬은 최대 하나, Foundation 스킬은 필요한 최소 개수만 선택합니다.
- 실패, 중요한 결정, 재사용 가능한 교훈, 실제 검증 결과가 있는 호출을 Learning Log에 기록합니다.
- 스킬 본문은 근거가 있을 때만 갱신합니다.

## 자동 검증

Base는 다음을 회귀 테스트합니다.

- 루트 `[기획서]`와 중첩 복제본
- Skill Registry·분야 진입·Learning Log
- Skill Map 필수 PDF·Manifest와 설정한 선택 Markdown/DOCX/다이어그램 최신성
- Design Document Registry·책임 범위
- Markdown·JSON 책임 원본·PDF·선택 파생본·승인 이미지 해시
- 생성기 변경 후 미재생성
- 등록되지 않은 Markdown 본책과 수동 변경된 파생본 탐지
- DOCX/PDF 실제 생성과 PDF 전 페이지 렌더
- whitespace와 기본 구조

파일이 존재한다는 사실과 실제 실행·Required Check 강제 상태를 구분합니다.
