# 게임 프로젝트 저장소 운영체계 방법

- 상태: 공용 상위 방법·라우터
- 목적: 게임 방향, 루트 기획서, 분야별 본책, 선택적 프로젝트 스킬, 개발 게이트, 이미지·PDF, 구현·검증과 GitHub 작업을 하나의 추적 가능한 운영체계로 연결한다.
- 적용 대상: 개인 개발, 소규모 팀, AI 협업 팀과 프리프로덕션부터 출시 준비 단계의 게임 프로젝트

> 이 문서는 핵심 책임과 연결 구조만 소유한다. 안전 마이그레이션, 개발 게이트, 분야 스킬 학습과 PDF 발행의 상세 절차는 각각의 전문 Method·Skill을 따른다.

## 1. 목표 상태

```text
사용자 방향
→ 저장소 루트 [기획서]
→ 프로젝트 허브·분야별 현행 본책
→ Development Gates·Roadmap
→ Project Skill Registry·Map
→ 필요한 Foundation·분야 프로젝트 스킬
→ Issue·Goal·Plan
→ 코드·데이터·자산
→ 테스트·플레이·캡처·PDF 증거
→ Active Context·Handoff·Learning Log 갱신
```

운영체계는 문서 수를 늘리는 것이 아니라 다음을 보장한다.

- 새 GPT와 Codex가 같은 시작 문서를 읽는다.
- 사용자가 저장소 루트에서 `[기획서]`를 즉시 찾는다.
- 한 질문에는 현행 책임 원본 하나가 있다.
- 승인·구현·검증·미확정·보류를 혼동하지 않는다.
- 변경 전에 주 책임 분야와 영향 분야를 판정한다.
- 전체 스킬이 아니라 필요한 최소 스킬만 호출한다.
- 모든 의미 있는 스킬 호출이 학습 기록으로 남는다.
- 분야별 프로젝트 스킬이 실제 본책·파일·검증에 연결된다.
- 이미지와 PDF가 책임 원본·승인 상태·실제 결과에 연결된다.
- 변경 누락을 PR과 자동 검사에서 발견한다.
- 새 AI가 과거 대화 없이 저장소만으로 작업을 재개한다.

## 2. 전문 Method·Skill 라우팅

| 작업 | Method | 실행 Skill·템플릿 |
|---|---|---|
| 새 요청의 분야·스킬 판정 | 이 문서·스킬 진화 Method | `skills/routing-project-work-by-discipline/` |
| 운영체계 신규 설치 | 이 문서 | `skills/installing-game-project-operating-system/`, `templates/project-operations/` |
| 기존 프로젝트 구조 재배치 | `EXISTING_PROJECT_SAFE_MIGRATION_METHOD.md` | `skills/migrating-existing-game-project-structure/` |
| 작업·제품 게이트 | `DEVELOPMENT_GATES_METHOD.md` | `templates/project-operations/DEVELOPMENT_GATES.md` |
| 분야별 프로젝트 스킬 | `DISCIPLINE_SKILL_EVOLUTION_METHOD.md` | `skills/evolving-project-discipline-skills/`, `PROJECT_SKILL_MAP.md`, `SKILL_REGISTRY.json` |
| Active Context·Handoff | `PROJECT_HANDOFF_CONTEXT_METHOD.md` | `skills/maintaining-project-context-and-handoff/` |
| 분야별 PDF | `DISCIPLINE_PDF_PUBLICATION_METHOD.md` | `skills/publishing-discipline-bibles/`, `PUBLICATION_MANIFEST.json` |
| 운영체계 Health Review | 이 문서·전문 Method | `skills/verifying-game-project-operating-system/`, `OPERATING_SYSTEM_HEALTH_REPORT.md` |
| 기획 책임 구조 | `PLANNING_SYSTEM_METHOD.md` | `skills/writing-game-design-documents/` |
| Vertical Slice | `DEVELOPMENT_GATES_METHOD.md` | `skills/designing-vertical-slices/` |

## 3. 루트 기획서와 프로젝트 허브

신규 프로젝트와 승인된 마이그레이션의 활성 기획서는 저장소 루트 바로 아래에 둔다.

```text
<repository-root>/[기획서]/
└─ 00_프로젝트_허브/
```

중첩 `docs/[기획서]`, `src/[기획서]`를 별도 현행 원본으로 만들지 않는다. 운영 중인 기존 프로젝트의 경로는 감사와 사용자 승인 없이 강제 이동하지 않는다.

프로젝트 허브는 부서가 아니라 사람과 AI의 통제·라우팅 계층이다.

필수 책임:

- 최초 읽기와 프로젝트 대시보드
- 현재 상태·다음 작업·보호 범위
- Documentation Map
- Development Gates와 Roadmap
- Project Skill Map·Skill Registry
- 변경 갱신 매트릭스
- 결정·변경·출처·마이그레이션 기록
- Visual Source·Asset Manifest
- Publication Manifest
- GPT·Codex·GitHub Workflow
- 운영체계 Health Review

## 4. 기본 책임 분야

프로젝트 규모에 따라 폴더·본책을 통합할 수 있지만 다음 책임은 누락하지 않는다.

| 분야 | 핵심 질문 | 주요 책임 |
|---|---|---|
| 설정·내러티브 | 이 세계에서 왜 일어나는가? | 세계관 정사, 시나리오, 캐릭터, 용어, 대사 |
| 게임 디자인 | 플레이어가 무엇을 보고 판단하고 반복하는가? | 핵심 루프, 전투, 경제, 성장, 콘텐츠, 밸런스 |
| UX·UI·접근성 | 플레이어가 어떻게 이해하고 조작하는가? | 정보 구조, 화면 흐름, 입력, 피드백, 온보딩, 접근성 |
| 개발·엔지니어링 | 어떤 구조가 상태와 결과를 소유하는가? | 엔진, Scene, 코드, 데이터, AI, 저장, 성능, 빌드 |
| 테크니컬 아트·파이프라인 | 자산이 어떻게 엔진에 들어가는가? | 규격, Import, 피벗, 애니메이션 계약, 도구, 예산 |
| 아트 | 무엇을 어떤 시각 언어로 보여주는가? | 캐릭터, 환경, 건물, UI 그래픽, 애니메이션, VFX |
| 사운드 | 무엇을 언제 어떤 우선순위로 들려주는가? | BGM, SFX, 음성, 이벤트 연결, 믹싱, 반복 방지 |
| QA | 의도한 기능이 실제로 작동하는가? | 자동·수동·회귀·성능·시각·오디오·호환성 테스트 |
| 프로덕션·PM | 언제 누가 무엇을 완료하는가? | 마일스톤, 일정, 의존성, 위험, 범위, 예산 상태 |
| 분석·유저리서치 | 사용자는 어떻게 행동하고 이해하는가? | 벤치마킹, SWOT, 플레이테스트, 텔레메트리, 개선안 |
| 통합검수 | 전체 결과가 서로 일치하는가? | 문서·구현·자산·검증·일정·스킬·PDF·릴리스 준비도 |

분야를 독립시킬 기준:

- 전문 판단과 Quality Bar가 다름
- 변경 빈도·담당자가 다름
- 독립 제작·검증 파이프라인이 있음
- 늦게 발견하면 비용이 크게 증가함

## 5. 책임 원본 계층

**SSOT(Single Source of Truth)**: 같은 질문에 대해 현재 공식 답을 소유하는 책임 원본을 하나만 두는 원칙이다.

```text
현재 프로젝트 상태 → Active Context
프로젝트 약속 → 방향서
분야 방향·품질·전체 과정 → 분야별 본책
세부 수치·스키마·계약 → 부록·실제 데이터
작업·제품 단계 → Development Gates·Roadmap
현재 실행 범위 → Issue·Goal·Plan
스킬 선택·상태 → Skill Registry·Project Skill Map
반복 절차 → Foundation·분야 프로젝트 스킬
스킬 실행 결과 → Learning Log
이미지 상태 → Visual Source·Asset Manifest
사용자 열람본 → 분야 PDF·Publication Manifest
완료 증거 → 테스트·QA·캡처
운영체계 상태 → Health Review
결정 이유 → Decision Log
과거 상태 → Git 이력
```

다른 문서는 원본 경로, 현재 작업에 필요한 요약과 차이만 기록한다.

## 6. 분야별 본책 계약

본책은 분야 전체의 활성 진입점이다.

필수 내용:

- 한눈에 보기·상태·기준 커밋
- 분야 목적·플레이어 가치·Quality Bar·금지 방향
- 책임과 다른 분야의 입력·출력
- 분야 전체 작업 과정
- 현재 작업·제품 게이트 기여
- Registry ID와 필요한 Foundation·분야 프로젝트 스킬
- 확정·구현·검증·미확정·보류
- 실제 코드·데이터·자산·테스트
- 승인 이미지·실제 캡처
- 위험·다음 작업·완료 기준
- PDF 발행 상태·부록·변경·학습 이력

세부 수치·스키마·화면별 명세·테스트 케이스는 부록과 실제 원본에 둔다.

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
| 대체됨 | 새 원본으로 교체 | 새 경로 |
| 불일치 | 원본과 실제 결과가 다름 | 차이·영향·수정 계획 |

문서, 스킬 또는 PDF 존재를 구현·검증 완료 증거로 사용하지 않는다.

## 8. 개발 게이트 연결

작업 실행:

```text
Intake·Context
→ Definition of Ready
→ Planning·Approval
→ Implementation
→ Verification
→ Documentation
→ Integration·Completion
```

제품 단계:

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

각 단계는 진입·종료 기준, Quality Bar, 증거, 미검증과 다음 Greenlight를 가진다.

## 9. 선택적 스킬 호출과 항상 학습

프로젝트는 사람용 `PROJECT_SKILL_MAP.md`와 기계 판독용 `SKILL_REGISTRY.json`을 함께 둔다.

기본 정책:

- 전체 skills 폴더 기본 로드 금지
- 기본 선택 없음
- trigger 일치 필수
- 주 책임 분야 스킬 최대 하나
- Foundation 스킬은 실제 절차에 필요한 최소 개수
- 검증·PDF·Handoff 스킬은 해당 단계에서만 호출
- 보류·백업·제거 후보 스킬 호출 금지

모든 의미 있는 스킬 호출은 Learning Log에 결과·실패·예외·사용자 피드백과 변경 필요성을 기록한다. 스킬 본문은 매번 무조건 수정하지 않고 반복 실패, 새 예외, 책임·경로·검증 변경처럼 근거가 있을 때 갱신한다.

지식 상태는 `관찰 → 가설 → 패턴 → 검증 → 승격 후보`로 관리한다. 프로젝트 고유 수치·경로·승인 자산은 Base 공용 스킬에 넣지 않는다.

## 10. 이미지·자산 운영

활성 이미지마다 다음을 관리한다.

```yaml
asset_id:
purpose:
status:
canonical_path:
approved_reference:
implemented_path:
latest_capture:
visual_dna:
replacement_requires_approval:
```

- 항목별 캐노니컬 경로는 하나다.
- 기존 승인 이미지가 있으면 별도 지시 없이 새 시안을 만들지 않는다.
- 콘셉트·방향 승인·제작 준비·구현·시각 검증을 구분한다.
- 이미지 전체가 아니라 채택 요소와 비채택 요소를 기록한다.
- 이전 상태는 Git 이력으로 보존한다.

## 11. 분야 PDF 운영

분야 PDF는 Markdown과 승인 이미지에서 생성하는 읽기 전용 최신 통합본이다.

포함:

- 분야 목적·역할·플레이어 가치
- 승인 결정과 전체 작업 흐름
- 단계별 입력·산출물·관련 게이트·스킬
- 실제 파일·자산·테스트 경로
- 승인 이미지·다이어그램·실제 캡처
- 현재 구현·검증 상태
- 위험·보류·다음 작업

Publication Manifest는 입력 파일, 승인 이미지, 출력 PDF, content hash, 생성기, 상태와 시각 검수를 기록한다.

## 12. 변경 추적과 GitHub

모든 L1 이상 작업은 다음을 선언한다.

```yaml
primary_discipline:
affected_disciplines:
change_type:
design_sources:
foundation_skills:
discipline_skills:
implementation_paths:
asset_paths:
test_paths:
required_evidence:
```

권장 추적:

```text
결정 ID
→ 분야 본책
→ Issue·Plan
→ 실제 코드·데이터·자산
→ 테스트·캡처
→ 현재 상태·PDF
```

GitHub는 Issue·PR 계약, CODEOWNERS, Actions, Required Status Check와 이력을 관리한다. 파일 존재와 실제 실행·브랜치 보호 강제를 구분한다.

## 13. 자동화 경계

자동 검사 적합:

- 루트 `[기획서]` 존재와 중첩 복제본
- 필수 시작 문서와 링크
- 금지 활성 버전 파일명
- Asset ID·캐노니컬 경로 중복
- Skill Registry JSON·중복 ID·경로·trigger·Learning Log
- 전체 스킬 자동 로드 금지와 분야 진입 스킬
- 스킬 변경 시 Registry·Map·Learning Log 동기화
- 변경 유형별 본책 갱신
- PDF 입력 해시·헤더·Manifest·시각 검수 상태
- 코드·데이터 자동 테스트

사람·AI 통합검수 필요:

- 플레이 재미와 명확성
- 스킬 책임·호출 범위 적합성
- 학습 기록이 실제 개선으로 이어졌는지
- 이미지가 프로젝트 방향에 맞는지
- 상충하는 기획의 의미 판단
- Vertical Slice·릴리스 Quality Bar 충족
- 예산·일정·출시 승인

## 14. 설치·이관 원칙

신규 설치는 루트 `[기획서]`, Project Skill Registry·Map, Learning Log와 두 Governance Checker를 함께 연결한다.

기존 프로젝트는 바로 이동·삭제하지 않는다.

```text
저장소 감사
→ 문서·이미지·스킬·코드·테스트 인벤토리
→ 주 책임 분야·영향 분야 분류
→ 고유 결정·수치·계약 확인
→ 목표 구조·Registry·보존 대조 계획
→ 사용자 승인
→ 경로·참조·자동화 설치
→ 통합검수·Health Review
→ 완전히 흡수된 중복만 제거
```

## 15. 콜드 스타트·Health Review 완료 기준

새 작업자가 10분 안에 다음을 답해야 한다.

1. 저장소 루트 `[기획서]`는 어디인가?
2. 게임의 핵심 약속과 대상 플레이어는 누구인가?
3. 현재 개발 단계와 다음 게이트는 무엇인가?
4. 현재 최우선 작업과 선행 조건은 무엇인가?
5. 무엇이 확정·구현·검증·미확정인가?
6. 분야별 현행 책임 본책과 Registry 진입 스킬은 어디인가?
7. 현재 요청에 필요한 최소 스킬은 무엇인가?
8. 최신 이미지와 실제 게임 캡처는 어디인가?
9. 관련 코드·데이터·테스트와 최신 PDF는 어디인가?
10. 작업 종료 시 무엇을 갱신하고 어떤 Learning Log를 남기는가?

답할 수 없거나 자동 검사·콜드 스타트가 실패하면 운영체계 설치가 완료된 것이 아니다. `skills/verifying-game-project-operating-system/SKILL.md`로 원인과 수정 책임을 기록한다.
