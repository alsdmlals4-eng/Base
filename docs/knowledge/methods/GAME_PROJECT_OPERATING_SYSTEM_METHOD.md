# 게임 프로젝트 저장소 운영체계 방법

- 상태: 공용 상위 방법·라우터
- 목적: 게임 방향, 분야별 본책, 프로젝트 스킬, 개발 게이트, 이미지·PDF, 구현·검증과 GitHub 작업을 하나의 추적 가능한 운영체계로 연결한다.
- 적용 대상: 개인 개발, 소규모 팀, AI 협업 팀과 프리프로덕션부터 출시 준비 단계의 게임 프로젝트

> 이 문서는 핵심 책임과 연결 구조만 소유한다. 안전 마이그레이션, 개발 게이트, 분야 스킬 학습과 PDF 발행의 상세 절차는 각각의 전문 Method·Skill을 따른다.

## 1. 목표 상태

```text
사용자 방향
→ 프로젝트 허브·분야별 현행 본책
→ Development Gates·Roadmap
→ Foundation·분야 프로젝트 스킬
→ Issue·Goal·Plan
→ 코드·데이터·자산
→ 테스트·플레이·캡처·PDF 증거
→ 상태·인수인계·학습 갱신
```

운영체계는 문서 수를 늘리는 것이 아니라 다음을 보장한다.

- 새 GPT와 Codex가 같은 시작 문서를 읽는다.
- 한 질문에는 현행 책임 원본 하나가 있다.
- 승인·구현·검증·미확정·보류를 혼동하지 않는다.
- 변경 전에 주 책임 분야와 영향 분야를 판정한다.
- 분야별 프로젝트 스킬이 실제 본책·파일·검증에 연결된다.
- 이미지와 PDF가 책임 원본·승인 상태·실제 결과에 연결된다.
- 변경 누락을 PR과 자동 검사에서 발견한다.
- 새 AI가 과거 대화 없이 저장소만으로 작업을 재개한다.

## 2. 전문 Method·Skill 라우팅

| 작업 | Method | 실행 Skill·템플릿 |
|---|---|---|
| 운영체계 신규 설치 | 이 문서 | `skills/installing-game-project-operating-system/`, `templates/project-operations/` |
| 기존 프로젝트 구조 재배치 | `EXISTING_PROJECT_SAFE_MIGRATION_METHOD.md` | `skills/migrating-existing-game-project-structure/` |
| 작업·제품 게이트 | `DEVELOPMENT_GATES_METHOD.md` | `templates/project-operations/DEVELOPMENT_GATES.md` |
| 분야별 프로젝트 스킬 | `DISCIPLINE_SKILL_EVOLUTION_METHOD.md` | `skills/evolving-project-discipline-skills/`, `PROJECT_SKILL_MAP.md` |
| 분야별 PDF | `DISCIPLINE_PDF_PUBLICATION_METHOD.md` | `skills/publishing-discipline-bibles/`, `PUBLICATION_MANIFEST.json` |
| 기획 책임 구조 | `PLANNING_SYSTEM_METHOD.md` | `skills/writing-game-design-documents/` |
| 인수인계 | `PROJECT_HANDOFF_CONTEXT_METHOD.md` | Handoff 템플릿 |
| Vertical Slice | `DEVELOPMENT_GATES_METHOD.md` | `skills/designing-vertical-slices/` |

## 3. 프로젝트 허브

프로젝트 허브는 부서가 아니라 사람과 AI의 통제·라우팅 계층이다.

필수 책임:

- 최초 읽기와 프로젝트 대시보드
- 현재 상태·다음 작업·보호 범위
- Documentation Map
- Development Gates와 Roadmap
- Project Skill Map
- 변경 갱신 매트릭스
- 결정·변경·출처·마이그레이션 기록
- Visual Source·Asset Manifest
- Publication Manifest
- GPT·Codex·GitHub Workflow

권장 경로는 `[기획서]/00_프로젝트_허브/`지만, 기존 프로젝트의 안정된 경로가 같은 책임을 수행하면 강제로 바꾸지 않는다.

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
| 통합검수 | 전체 결과가 서로 일치하는가? | 문서·구현·자산·검증·일정·릴리스 준비도 |

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
반복 절차 → Foundation·분야 프로젝트 스킬
이미지 상태 → Visual Source·Asset Manifest
사용자 열람본 → 분야 PDF·Publication Manifest
완료 증거 → 테스트·QA·캡처
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
- Foundation·분야 프로젝트 스킬
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

## 9. 분야별 프로젝트 스킬 연결

- 여러 분야 공통 절차는 foundation에 한 번만 둔다.
- 각 분야는 본책·실제 경로·산출물·검증을 연결하는 진입 스킬을 가진다.
- 새 채팅은 Project Skill Map에서 현재 작업에 필요한 foundation + 분야 스킬만 읽는다.
- 실제 작업 후 Learning Log에 성공·실패·예외·사용자 피드백을 기록한다.
- 지식 상태는 `관찰 → 가설 → 패턴 → 검증 → 승격 후보`로 관리한다.
- 프로젝트 고유 수치·경로·승인 자산은 Base 공용 스킬에 넣지 않는다.

## 10. 이미지·자산 운영

활성 이미지마다 다음을 관리한다.

```yaml
asset_id:
purpose:
owner_discipline:
status:
canonical_path:
approved_elements:
rejected_elements:
visual_dna:
implemented_path:
latest_capture:
replacement_requires_approval:
```

원칙:

- 기존 승인 이미지가 있으면 별도 지시 없이 새 시안을 만들지 않는다.
- 한 항목에는 캐노니컬 경로 하나만 사용한다.
- 콘셉트·방향 승인·제작 준비·구현·시각 검증을 구분한다.
- 이미지 전체가 아니라 채택·비채택 요소를 기록한다.
- 등록됐지만 파일이 없으면 `MIGRATION_PENDING`이다.
- 이전 상태는 Git 이력으로 보존한다.

## 11. 분야별 PDF 운영

PDF는 분야 Markdown·활성 부록·승인 이미지와 실제 캡처에서 생성하는 읽기 전용 통합본이다.

반드시 포함:

- 분야 목적·전체 과정·게이트·프로젝트 스킬
- 승인 결정·실제 경로
- 승인 이미지·상태 캡션·실제 캡처
- 구현·검증·미검증·보류
- 다음 작업·부록·기준 커밋

Publication Manifest에서 입력 경로, 출력 PDF, 입력 해시, 생성기, 상태와 시각 검수를 추적한다. 생성·렌더링을 검증하지 못했으면 `CURRENT`로 표시하지 않는다.

## 12. 수명주기·컨텍스트 효율

- `[현행]`: 현재 책임 원본과 실행 스킬
- `[백업]`: 외부 원본·감사·승인 근거처럼 Git 이력만으로 부족한 자료
- `[보류]`: 이유·재개 조건·책임 원본·선행 작업이 있는 미래 항목
- `[제거 후보]`: 고유 정보·참조·복구·승인을 확인하기 전 삭제하지 않는 후보

단순 이전 버전은 Git 이력으로 보존한다. 기본 작업 컨텍스트는 Documentation Map에서 현재 작업에 필요한 현행 문서와 스킬만 선택한다.

## 13. 기존 프로젝트 적용 경계

기존 프로젝트는 다음 순서를 따른다.

```text
내용 보존
→ 책임·참조·고유 정보 감사
→ 중복·충돌·누락 분석
→ 변경 전후 보존 대조를 포함한 제안
→ 사용자 승인
→ 승인 범위만 변경
→ 링크·스킬·PDF·콜드 스타트 검증
```

Base 예시 경로와 명칭을 강제하지 않는다. 프로젝트 고유 결정·구현·승인 자산·실패·보류를 보존한다.

## 14. GitHub 운영

권장 구성:

- Issue Form: 목표·분야·Ready·스킬·검증
- PR Template: 게이트·본책·스킬·Manifest·PDF·보존 대조
- CODEOWNERS: 분야별 본책·스킬·자동화 리뷰
- Governance Checker: 필수 경로, 링크, 금지 파일명, 자산·PDF 최신성, 변경 갱신 누락
- GitHub Actions·Required Status Checks·브랜치 보호

`파일 존재`, `실행 확인`, `강제됨`을 서로 다른 상태로 기록한다.

## 15. 작업 종료

작업 종료 시 확인한다.

1. 실제 결과와 승인·구현·검증 상태
2. 관련 본책·Roadmap·Development Gates
3. Documentation Map·Project Skill Map
4. 분야 스킬·Learning Log
5. Visual Source·Asset Manifest
6. PDF·Publication Manifest
7. Active Context·Handoff·Decision Log·Changelog
8. 미검증·불일치·위험·다음 작업
9. 보존·참조·콜드 스타트
10. 프로젝트 전용 교훈과 Base 환류 후보

## 16. 완료 판단 질문

- 새 AI가 10분 안에 방향·상태·다음 게이트를 찾는가?
- 각 분야의 본책·프로젝트 스킬·실제 검증 경로가 연결되는가?
- 승인 이미지와 최신 PDF를 찾을 수 있는가?
- 백업·보류·제거 후보가 기본 컨텍스트에서 제외되는가?
- PR이 관련 본책·스킬·Manifest·PDF 누락을 발견할 수 있는가?
- 실행하지 않은 검증을 완료로 표시하지 않았는가?

하나라도 답하지 못하면 운영체계 설치·마이그레이션은 완료되지 않았다.
