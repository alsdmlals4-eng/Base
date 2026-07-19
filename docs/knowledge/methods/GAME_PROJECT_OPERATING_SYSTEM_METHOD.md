# 게임 프로젝트 저장소 운영체계 방법

- 상태: 공용 상위 Method·라우터
- 목적: 프로젝트 방향, 구조화 기획서, 사람용 문서, 선택적 스킬, 개발 게이트, 이미지, 구현·검증과 GitHub 작업을 하나의 추적 가능한 운영체계로 연결한다.

## 1. 목표 상태

```text
사용자 방향
→ 저장소 루트 [기획서]
→ DESIGN_DOCUMENT_REGISTRY.json
→ 프로젝트 전체·분야별 Markdown 또는 JSON 책임 원본
→ DOCX·PDF·다이어그램·승인 이미지
→ Development Gates·Roadmap
→ SKILL_REGISTRY.json·분야별 스킬
→ 코드·데이터·자산·테스트
→ Active Context·Handoff·Learning Log
→ GitHub Governance·통합검수
```

운영체계는 문서를 많이 만드는 것이 아니라 다음을 보장한다.

- 새 GPT와 Codex가 같은 시작 경로를 읽는다.
- 사용자가 루트 `[기획서]`에서 사람용 최신 PDF를 찾는다.
- AI는 Registry에서 문서별 Markdown 또는 JSON 책임 원본을 찾는다.
- 한 질문에는 현행 책임 원본 하나가 있다.
- 승인·구현·검증·미확정·보류를 혼동하지 않는다.
- 변경 전에 주 책임 분야와 영향 분야를 판정한다.
- 전체 스킬이 아니라 필요한 최소 스킬만 호출한다.
- 모든 의미 있는 스킬 호출이 Learning Log에 남는다.
- 이미지·PDF·선택 DOCX가 등록된 책임 원본·승인 상태·실제 결과와 연결된다.
- 누락과 오래된 파생본을 PR에서 탐지한다.
- 새 AI가 과거 대화 없이 저장소만으로 작업을 재개한다.

## 2. 전문 Method·Skill 라우팅

| 작업 | Method | 실행 Skill·Template |
|---|---|---|
| 새 요청의 분야·스킬 판정 | 스킬 진화 Method | `routing-project-work-by-discipline` |
| 운영체계 신규 설치 | 이 Method | `installing-game-project-operating-system` |
| 기존 프로젝트 구조 재배치 | 안전 마이그레이션 Method | `migrating-existing-game-project-structure` |
| 작업·제품 게이트 | Development Gates Method | `DEVELOPMENT_GATES.md` |
| Markdown·JSON 기획서·PDF | 혼용 기획서 발행 Method | `publishing-discipline-bibles` |
| 분야별 프로젝트 스킬 | Discipline Skill Evolution Method | `evolving-project-discipline-skills` |
| Active Context·Handoff | Handoff Method | `maintaining-project-context-and-handoff` |
| 운영체계 Health Review | 이 Method | `verifying-game-project-operating-system` |
| Vertical Slice | Development Gates Method | `designing-vertical-slices` |

## 3. 루트 기획서와 프로젝트 허브

```text
<repository-root>/[기획서]/
└─ 00_프로젝트_허브/
   ├─ START_HERE.md
   ├─ ACTIVE_CONTEXT.md
   ├─ DOCUMENTATION_MAP.md
   ├─ DEVELOPMENT_GATES.md
   ├─ DESIGN_DOCUMENT_REGISTRY.json
   ├─ SKILL_REGISTRY.json
   ├─ PROJECT_SKILL_MAP.md       # 선택 자동 생성
   ├─ PROJECT_SKILL_MAP.docx     # 선택 Word 검토
   ├─ PROJECT_SKILL_MAP.pdf
   ├─ PROJECT_SKILL_MAP.assets/
   └─ SKILL_MAP_PUBLICATION_MANIFEST.json
```

프로젝트 허브는 부서가 아니라 통제·라우팅 계층이다.

책임:

- 최초 읽기와 프로젝트 대시보드
- 현재 상태·다음 작업·보호 범위
- Design Document Registry와 Documentation Map
- Development Gates·Roadmap
- Skill Registry와 사람용 Skill Map
- 변경 갱신 매트릭스
- 결정·변경·출처·마이그레이션 기록
- Visual Source·Asset Manifest
- GPT·Codex·GitHub Workflow
- Health Review

## 4. 기본 책임 분야

| 분야 | 핵심 질문 | 주요 책임 |
|---|---|---|
| 설정·내러티브 | 이 세계에서 왜 일어나는가? | 정사, 시나리오, 캐릭터, 용어, 대사 |
| 게임 디자인 | 플레이어가 무엇을 판단하고 반복하는가? | 핵심 루프, 전투, 경제, 성장, 콘텐츠, 밸런스 |
| UX·UI·접근성 | 플레이어가 어떻게 이해하고 조작하는가? | 정보 구조, 화면 흐름, 입력, 피드백, 온보딩, 접근성 |
| 개발·엔지니어링 | 어떤 구조가 상태와 결과를 소유하는가? | 엔진, Scene, 코드, 데이터, AI, 저장, 성능, 빌드 |
| 테크니컬 아트·파이프라인 | 자산이 어떻게 엔진에 들어가는가? | 규격, Import, 피벗, 애니메이션 계약, 도구, 예산 |
| 아트 | 무엇을 어떤 시각 언어로 보여주는가? | 캐릭터, 환경, 건물, UI 그래픽, 애니메이션, VFX |
| 사운드 | 무엇을 언제 어떤 우선순위로 들려주는가? | BGM, SFX, 음성, 이벤트, 믹싱, 반복 방지 |
| QA | 의도한 기능이 실제로 작동하는가? | 자동·수동·회귀·성능·시각·오디오·호환성 테스트 |
| 프로덕션·PM | 언제 누가 무엇을 완료하는가? | 마일스톤, 일정, 의존성, 위험, 범위, 예산 |
| 분석·유저리서치 | 사용자는 어떻게 행동하고 이해하는가? | 벤치마킹, 플레이테스트, 텔레메트리, 개선안 |
| 통합검수 | 전체 결과가 서로 일치하는가? | JSON·구현·자산·발행·검증·일정·릴리스 준비도 |

작은 프로젝트는 본책을 통합할 수 있지만 `responsibility_coverage`에서 모든 책임을 보존한다.

## 5. 책임 원본 계층

```text
현재 프로젝트 상태 → ACTIVE_CONTEXT.md
프로젝트·분야 방향 → Markdown 또는 JSON 책임 원본
기획서 위치·책임 범위 → DESIGN_DOCUMENT_REGISTRY.json
사람용 최신본 → PDF·Manifest·선택 DOCX/기획서.assets
발행 최신성 → *_PUBLICATION_MANIFEST.json
작업·제품 단계 → DEVELOPMENT_GATES.md·Roadmap
현재 실행 범위 → Issue·Goal·Plan
스킬 선택·상태 → SKILL_REGISTRY.json
사람용 스킬 관계 → PROJECT_SKILL_MAP.pdf·docx·assets
반복 절차 → Foundation·분야 Skill
스킬 실행 결과 → Learning Log
이미지 상태 → JSON approved_visuals·Visual Source·Asset Manifest
완료 증거 → 테스트·QA·캡처
결정 이유 → Decision Log
과거 상태 → Git 이력
```

## 6. 구조화 기획서 계약

각 활성 책임 원본은 문서 역할에 맞게 다음을 소유한다.

- 문서 ID·종류·분야·책임·상태
- 목적·플레이어 가치·현재 목표
- Quality Bar·금지 방향
- 책임·비책임·분야 간 계약
- 전체 작업 과정
- 작업·제품 게이트 기여
- Foundation·분야 스킬·Learning Log
- 확정·구현·검증·확인 필요·보류
- 결정·실제 경로·검증 증거
- 상세 기획
- 승인 이미지·실제 캡처
- 위험·다음 작업·Ready·Done
- 부록·변경·학습 이력

사람용 파생본:

```text
기획서.json
→ 기획서.docx
→ 기획서.pdf
→ 기획서.assets/generated/*.png
→ 기획서.assets/approved/*
→ 기획서_PUBLICATION_MANIFEST.json
```

서술 중심 본책은 Registry에 등록한 Markdown을 사용할 수 있다. 같은 서술을 JSON과 중복 책임 원본으로 만들지 않는다.

## 7. 상태 언어

| 상태 | 의미 | 증거 |
|---|---|---|
| 확정 | 방향·규칙 승인 | 사용자 결정·Decision Record |
| 구현 | 실제 파일에 존재 | 코드·데이터·자산 경로 |
| 검증 | 실제 동작 확인 | 테스트·플레이·캡처 |
| 진행 중 | 부분 구현·검증 | 남은 범위 |
| 가설 | 추가 실험 필요 | 질문·성공·실패 기준 |
| 미확정 | 결정 필요 | 확인 질문 |
| 보류 | 활성 범위 제외 | 재개 조건 |
| 대체됨 | 새 원본으로 교체 | 새 ID·경로 |
| 불일치 | 원본과 실제 결과가 다름 | 차이·영향·수정 계획 |

JSON·DOCX·PDF·Skill 존재를 구현·검증 완료 증거로 사용하지 않는다.

## 8. 개발 게이트 연결

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

각 게이트는 진입·종료 기준, Quality Bar, 증거, 미검증과 다음 Greenlight를 가진다.

## 9. 선택적 프로젝트 스킬

- 공용 절차는 Foundation에 한 번만 둔다.
- 프로젝트가 선택한 각 분야는 등록된 Markdown 또는 JSON 책임 원본·경로·산출물·검증을 연결하는 진입 스킬 또는 명시적 통합 책임을 가진다.
- `SKILL_REGISTRY.json`은 trigger에 맞는 최소 스킬만 선택한다.
- `PROJECT_SKILL_MAP.pdf`는 사람용 관계·책임 지도다.
- 모든 의미 있는 호출은 Learning Log에 성공·실패·예외·피드백을 기록한다.
- 스킬 본문은 근거가 있을 때만 갱신한다.

## 10. 이미지·자산 운영

각 승인 자료는 JSON `approved_visuals`와 Manifest에 다음을 가진다.

```yaml
asset_id:
title:
path:
status:
caption:
adopted_elements:
excluded_elements:
include_in_publication:
```

기존 승인 이미지가 있으면 별도 지시 없이 새 이미지를 만들지 않는다. 콘셉트·승인·제작 준비·구현·시각 검증을 구분한다.

## 11. 발행 파이프라인

```text
Design Document Registry에서 활성 JSON 선택
→ JSON 구조 검증
→ 작업 흐름·상태·책임 다이어그램 생성
→ 승인 이미지·실제 캡처 확인
→ DOCX 생성
→ PDF 변환
→ 전 페이지 PNG 렌더 검수
→ JSON·생성기·출력·자산 SHA-256 Manifest
→ Governance 검사
```

사람 시각 검수는 실제 렌더 페이지를 확인한 경우에만 `PASSED`다.

## 12. GitHub Governance

세 검사기를 사용한다.

| 검사기 | 책임 |
|---|---|
| `check_documentation_governance.py` | 링크·금지 파일명·변경 갱신 |
| `check_skill_routing_governance.py` | Skill Registry·Learning Log·스킬맵 발행 |
| `check_design_document_publications.py` | Design Registry·JSON·DOCX·PDF·다이어그램·승인 이미지 |

GitHub Actions 파일 존재, 실제 실행, Required Status Check 강제를 서로 다른 상태로 기록한다.

## 13. 기존 프로젝트 마이그레이션

```text
Audit only
→ 기존 Markdown·DOCX·PDF·이미지·참조 지도
→ 보존하거나 승인할 Markdown/JSON 책임 구조와 발행 구조 제안
→ 고유 정보·결정·보류 보존 대조
→ 사용자 승인
→ 승인 범위만 승계
→ DOCX/PDF·링크·검증
→ 기존 원본 제거 후보 별도 승인
```

## 14. 완료 조건

- 루트 `[기획서]`와 시작 문서가 있다.
- Design Document Registry가 프로젝트 전체와 프로젝트가 선택한 분야를 책임진다.
- 모든 활성 본책에 등록된 단일 Markdown 또는 JSON 책임 원본·최신 PDF·Manifest와 선언한 선택 DOCX/다이어그램이 있다.
- Skill Registry와 사람용 스킬맵이 일치한다.
- Development Gates·Roadmap·Active Context가 연결된다.
- 승인 이미지와 실제 캡처 상태가 추적된다.
- 네 Governance Checker가 정상·실패 시나리오를 통과한다.
- 새 AI가 저장소만으로 방향·상태·기획서·스킬·검증을 찾는다.
- 실행하지 않은 테스트·렌더·브랜치 보호를 완료로 보고하지 않는다.
