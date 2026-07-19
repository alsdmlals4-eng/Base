# [프로젝트명] Documentation Map

- 책임: 프로젝트 허브·통합검수
- 공식 위치: 저장소 루트 `[기획서]/00_프로젝트_허브/DOCUMENTATION_MAP.md`
- 마지막 검토일:
- 기준 커밋:
- Base 기준 커밋:

> 모든 파일을 무작정 읽지 않는다. 질문에 맞는 Markdown 또는 JSON 책임 원본, 최소 스킬, 실제 파일과 사람용 최신 PDF만 선택한다.

## 1. 기본 읽기 순서

```text
최신 사용자 지시
→ 프로젝트 AGENTS.md
→ START_HERE.md·ACTIVE_CONTEXT.md·HANDOFF.md
→ 이 DOCUMENTATION_MAP.md
→ DEVELOPMENT_GATES.md
→ DESIGN_DOCUMENT_REGISTRY.json
→ 현재 분야 Markdown 또는 JSON 책임 원본
→ SKILL_REGISTRY.json
→ 필요한 Foundation·분야 스킬
→ 사람 검토 시 기획서 DOCX/PDF·다이어그램·승인 이미지
→ Roadmap·Issue·Goal·Plan
→ 실제 코드·데이터·자산·테스트
```

기본 제외: `[백업]`, `[보류]`, `[제거 후보]`, archive, hold, deprecated.

## 2. 프로젝트 허브 책임

| 질문 | 현행 책임 원본 | 사람용 열람·증거 | 갱신 트리거 |
|---|---|---|---|
| 프로젝트를 어디서 시작하는가? | `START_HERE.md` |  | 시작 경로 변경 |
| 현재 무엇이 사실인가? | `ACTIVE_CONTEXT.md`·실제 파일 | 테스트·캡처 | 구현·검증·우선순위 변경 |
| 현재 요구가 확정됐는가? | `INTERVIEW_REGISTRY.json`·현재 인터뷰 기록 | 사용자 확인 근거·확정 실행 프롬프트 | 방향·범위·산출물·검증 변경 |
| 전체·분야 기획서는 어디인가? | `DESIGN_DOCUMENT_REGISTRY.json` | 각 책임 원본·PDF·Manifest·선택 파생본 | 본책 생성·통합·이동·상태 변경 |
| 왜 이 프로젝트를 만드는가? | 프로젝트 종합 기획 책임 원본 | 프로젝트 종합 PDF | 방향·대상 플레이어 변경 |
| 다음 개발 게이트는 무엇인가? | `DEVELOPMENT_GATES.md` | 게이트 검수 보고 | 게이트 판정 변경 |
| 어떤 스킬을 사용하는가? | `SKILL_REGISTRY.json` | `PROJECT_SKILL_MAP.pdf`·`.docx` | 스킬·trigger·상태 변경 |
| 스킬이 무엇을 학습했는가? | 각 Learning Log |  | 실패·중요 결정·재사용 교훈·실제 검증 |
| 승인 이미지와 자산은 어디인가? | 각 JSON `approved_visuals`·Asset Manifest | 각 `.assets/`·PDF | 승인·교체·이전 |
| 발행본이 최신인가? | 각 `_PUBLICATION_MANIFEST.json` | PDF·렌더·선택 DOCX/assets | 책임 원본·이미지·생성기 변경 |
| 운영체계가 정상인가? | Health Review | Governance Workflow | 설치·마이그레이션·주요 게이트 |

## 3. 분야별 책임·스킬·발행

| 책임 범위 | source format/path | Skill Registry ID | 진입 스킬 | 실제 파일·자산 | 테스트·검증 | 선택 DOCX | PDF | Manifest | 상태 |
|---|---|---|---|---|---|---|---|---|---|
| 프로젝트 전체 |  |  |  |  |  |  |  |  |  |
| 설정·내러티브 |  |  |  |  |  |  |  |  |  |
| 게임 디자인 |  |  |  |  |  |  |  |  |  |
| UX·UI·접근성 |  |  |  |  |  |  |  |  |  |
| 개발·엔지니어링 |  |  |  |  |  |  |  |  |  |
| 테크니컬 아트·파이프라인 |  |  |  |  |  |  |  |  |  |
| 아트 |  |  |  |  |  |  |  |  |  |
| 사운드 |  |  |  |  |  |  |  |  |  |
| QA |  |  |  |  |  |  |  |  |  |
| 프로덕션·PM |  |  |  |  |  |  |  |  |  |
| 분석·유저리서치 |  |  |  |  |  |  |  |  |  |
| 통합검수 |  |  |  |  |  |  |  |  |  |

여러 책임을 한 JSON에 통합하면 Design Document Registry의 `responsibility_coverage`에 모두 등록한다.

## 4. 작업 유형별 최소 읽기

| 작업 | JSON·현행 원본 | Foundation 스킬 | 분야 스킬 | 후속 호출 | 검증 |
|---|---|---|---|---|---|
| 새 요청·분야 판정 | START_HERE·Active Context·Registry | routing-project-work-by-discipline | 주 책임 분야 진입 스킬 | 대상이면 conducting-deep-requirement-interviews → 요구 변환 | 라우팅·확인 추적성 |
| 방향·핵심 경험 변경 | 프로젝트 종합 책임 원본 | 기획 책임 구조 | 영향 분야 | 발행·Handoff | 사용자 승인·원본 해시 |
| 시스템·수치 변경 | 게임 디자인·개발 책임 원본 | 영향도 분석 | 게임 디자인·개발 | QA·통합검수·발행 | 데이터·플레이 회귀 |
| UI·UX 변경 | UX·게임 디자인 책임 원본 | 영향도 분석 | UX·UI | 시각 QA·발행 | 사용성·접근성 |
| 코드·데이터·저장 변경 | 개발 책임 원본 | 개발 게이트 | 개발 | QA·Handoff | 자동 테스트·저장 호환성 |
| 이미지·자산·VFX 변경 | 아트·테크니컬 아트 책임 원본 | 자산 계약 | 아트·테크니컬 아트 | 발행·시각 검수 | Asset Manifest·실제 캡처 |
| 사운드 변경 | 사운드 책임 원본 | 영향도 분석 | 사운드 | 오디오 QA·발행 | 이벤트·믹싱·반복 |
| 일정·범위 변경 | 프로덕션 책임 원본 | 개발 게이트 | 프로덕션 | Handoff | Roadmap·Greenlight |
| 기획서 발행 | Design Document Registry·대상 책임 원본 | publishing-discipline-bibles | 해당 분야 | 통합검수 | PDF/Manifest·해시·전 페이지 렌더 |
| 분야 스킬 변경 | 대상 JSON·실제 작업·검증 | evolving-project-discipline-skills | 해당 분야 | 스킬맵 재생성·Health Review | Registry·Log·선택적 호출 |
| 기존 구조 마이그레이션 | 전체 감사 자료 | migrating-existing-game-project-structure | 영향 분야 | 발행·Health Review | 보존 대조·링크·콜드 스타트 |
| 운영체계 Health Review | 모든 활성 Registry·검사 결과 | verifying-game-project-operating-system | 통합검수 | 결함 관련 스킬 | 구조·발행·Workflow |

## 5. AI용·사람용 경계

```text
AI 기획 원본 → *.json
사람 기본 열람 → *.pdf
사람 문서 검토 → *.docx
시각 자료 → *.assets/
최신성 → *_PUBLICATION_MANIFEST.json
```

DOCX·PDF를 직접 고쳐 책임 원본으로 사용하지 않는다. 기획 Markdown은 Registry에 등록하고, `PROJECT_SKILL_MAP.md`는 선택적 자동 생성 파생본으로만 사용한다.

## 6. 상태와 수명주기

| 구분 | 위치 | 기본 읽기 | 사용 조건 |
|---|---|---|---|
| 현행 | Registry에서 `ACTIVE/CURRENT` | 포함 | 현재 작업 관련 |
| 백업 | `[백업]` | 제외 | 감사·출처·사용자 요청 |
| 보류 | `[보류]` | 제외 | 재개 승인·조건 충족 |
| 제거 후보 | `[제거 후보]` | 제외 | 고유 정보·참조·복구·승인 검수 |

## 7. 자동 검수 경로

| 검사 | 책임 |
|---|---|
| `check_documentation_governance.py` | 링크·금지 파일명·변경 갱신 |
| `check_skill_routing_governance.py` | Skill Registry·Learning Log·스킬맵 발행 |
| `check_design_document_publications.py` | Design Registry·JSON·DOCX·PDF·자산·Manifest |

## 8. 콜드 스타트 검수

새 AI가 10분 안에 다음을 찾을 수 있어야 한다.

- 저장소 루트 `[기획서]`
- 프로젝트 목적과 핵심 경험
- 현재 구현·검증 상태
- 다음 작업·선행 조건·게이트
- 변경 금지 결정·자산
- 프로젝트 전체·분야별 Markdown 또는 JSON 책임 원본
- 사람용 최신 DOCX/PDF·승인 이미지
- 현재 요청에 필요한 최소 스킬
- 실제 코드·데이터·자산·테스트
- 보류·확인 필요·미검증
- 작업 종료 갱신 대상과 Learning Log

답하지 못한 질문은 이 지도 또는 연결된 Registry·JSON·실제 증거를 보강한다.
