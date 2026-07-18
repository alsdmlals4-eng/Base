# Base

여러 프로젝트가 공유하는 **[학습형] [공용] AI 작업 규칙, 기획 지식, 실행 스킬과 템플릿**의 원본 저장소입니다.

Base는 프로젝트에서 얻은 문제 해결 방법, 실패 사례와 검증 결과를 일반화해 계속 학습·갱신합니다. 각 프로젝트는 Base를 그대로 복제하지 않고, 자신의 세계관, 수치, 엔진, 파일 경로와 현재 구현 상태에 맞게 **분화·적용·검증**합니다.

Base에는 특정 프로젝트의 활성 GDD, 세계관, 밸런스, 코드와 실제 경로를 두지 않습니다. 프로젝트 고유 결정과 구현 상태는 해당 프로젝트 저장소가 책임집니다.

## 가장 먼저 읽기

새 채팅, 새 GPT, 새 Codex 또는 새 작업자는 다음에서 시작합니다.

```text
START_HERE.md
→ AGENTS.md
→ docs/DOCUMENTATION_MAP.md
→ 현재 작업에 맞는 method·skill·template·case
→ 대상 프로젝트의 현행 책임 원본과 실제 파일
```

- [Base 시작 지점](START_HERE.md)
- [공용 AI 작업 규칙](AGENTS.md)
- [문서·스킬 역할표](docs/DOCUMENTATION_MAP.md)

## 사용자가 기억할 최소 요청

다음처럼 요청하면 됩니다.

> `https://github.com/alsdmlals4-eng/Base 를 전부 살펴보고 참고해서 이 프로젝트를 작업해줘.`

저장소 접근이 가능한 AI는 `START_HERE.md`의 호출 계약에 따라 Base를 무작정 전부 복사하지 않고, 현재 작업에 필요한 공용 책임 원본과 대상 프로젝트의 현행 기준을 함께 확인합니다.

게임 프로젝트의 문서·이미지·팀 분야·GitHub 작업 흐름을 처음 설치하거나 전면 정리할 때는 다음 스킬을 사용합니다.

- `skills/installing-game-project-operating-system/SKILL.md`

이 스킬은 다음 효과를 목표로 합니다.

- GPT와 Codex가 같은 시작 문서를 읽음
- 분야별 활성 책임 원본 고정
- 변경 전 주 책임 분야·영향 분야 판정
- 관련 본책·상태·로드맵·검증 문서 동기화
- 이미지 중복과 임의 교체 방지
- PR에서 문서·이미지 갱신 누락 탐지
- 새 AI가 과거 대화 없이 저장소만으로 현재 상태 복원

## 운영 모델

```text
Base 공용 학습 데이터
→ 프로젝트별 전용 기획·스킬·구현으로 분화
→ 실제 작업·플레이테스트·검수
→ 성공·실패·미검증 사례 기록
→ 공용 원리와 프로젝트 고유 값 분리
→ Base method·skill·template·case 갱신
```

- Base는 `어떻게 판단하고 작업하며 검증할 것인가`를 학습합니다.
- 프로젝트는 `이 게임에서 무엇을 만들고 현재 어디까지 구현했는가`를 관리합니다.
- 한 번 성공한 방법은 먼저 사례·가설로 기록하고 반복 검증 뒤 공용 규칙이나 스킬로 승격합니다.

## 구조

```text
START_HERE.md      사람·AI 공용 최초 라우터
AGENTS.md          최소 공용 규칙
README.md          저장소 개요와 주요 경로
docs/              상세 작업 규칙과 공용 지식
skills/            직접 적용 가능한 실행 스킬
templates/         프로젝트에 복사·분화할 산출물 양식
```

## 프로젝트 작업 시작 순서

프로젝트 작업에서는 **현재 작업에 적용되는 공용 기준 전체와 프로젝트 현행 기준 전체**를 함께 확인합니다. `전체`는 저장소의 모든 파일을 무조건 읽는다는 뜻이 아니라 Documentation Map과 참조 관계로 관련 책임 원본과 영향 파일을 빠짐없이 선택한다는 뜻입니다.

```text
프로젝트 AGENTS.md
→ BASE_RULES_VERSION.md와 Base 기준
→ 프로젝트 START_HERE·Documentation Map
→ Handoff·Active Context
→ 프로젝트 방향과 관련 분야 본책
→ Roadmap·Issue·Goal·Plan
→ 실제 수정 대상·자산·테스트
```

## 핵심 작업 문서

| 파일 | 역할 |
|---|---|
| `START_HERE.md` | Base 호출 계약과 요청별 라우팅 |
| `AGENTS.md` | 최소 공용 작업 규칙과 학습 환류 원칙 |
| `docs/AI_SHARED_WORK_RULES.md` | 역할, 범위, 품질, 파일 수명주기, Base 승격 |
| `docs/AI_WORKFLOW_RULES.md` | 요청 분류, 공용·전용 컨텍스트 확인, 검증과 학습 환류 |
| `docs/CONTENT_DESIGN_METHOD.md` | 의도→경험→규칙→흐름→검증 기반 콘텐츠 기획 |
| `docs/AI_SKILL_ADOPTION_GUIDE.md` | 스킬·외부 모델 검토, 권한, 비용과 검증 |
| `docs/DOCUMENTATION_MAP.md` | 문서·스킬·템플릿 라우터 |
| `docs/knowledge/README.md` | 공용 methods·research·skill contracts·cases |
| `docs/knowledge/methods/GAME_PROJECT_OPERATING_SYSTEM_METHOD.md` | 분야별 본책·이미지·GitHub 운영체계 설계 방법 |
| `docs/CHANGELOG.md` | Base 버전과 변경 기록 |

## 실행 스킬

| 스킬 | 사용 시점 |
|---|---|
| `skills/installing-game-project-operating-system/` | 프로젝트 운영체계 감사·설치·이관·자동 검사 연결 |
| `skills/transforming-requests-into-prompts/` | 짧거나 모호한 요청을 실행 가능한 프롬프트로 변환 |
| `skills/designing-vertical-slices/` | 핵심 경험을 대표하는 완성 구간과 제작 파이프라인 검증 |
| `skills/writing-game-design-documents/` | 기획서 종류, 책임 원본, 로드맵과 명세 구조 설계 |
| `skills/orchestrating-deepseek-worktrees/` | 대용량 초안·분류를 격리 worktree의 외부 AI에 위임 |
| `skills/reviewing-external-ai-drafts/` | 외부 AI 결과를 실제 diff·근거·테스트로 검수 |
| `skills/designing-art-prompts-and-technique-cards/` | 아트·UI 기술 추천, 이미지 프롬프트와 QA 카드 작성 |
| `skills/promoting-project-knowledge/` | 프로젝트 교훈을 Base 학습 데이터로 환류 |

스킬은 도구 브랜드가 아니라 **사용 조건, 입력, 작업 절차, 산출물, 검증과 실패 기준**을 정의합니다.

## 게임 프로젝트 운영 키트

`templates/project-operations/`는 다음을 제공합니다.

- 프로젝트 운영체계 설치 계획
- 사용자용 `START_HERE` 대시보드
- 분야별 본책 골격
- 변경 유형별 문서 갱신 매트릭스
- GPT·Codex·GitHub Workflow
- Visual Source of Truth와 Asset Manifest
- Issue·PR 템플릿
- 문서·이미지·갱신 누락 검사 스크립트와 GitHub Actions 예시

템플릿은 대상 프로젝트 구조에 맞게 분화하며 폴더 전체를 그대로 복사하지 않습니다.

## 공용 학습 지식

`docs/knowledge/`는 다음을 관리합니다.

- `methods/`: 반복 가능한 설계·제작 판단 방법
- `research/`: 정보 수집·벤치마킹·표준·근거 평가
- `skills/`: 분야별 능력 계약과 검수 매트릭스
- `cases/`: 프로젝트와 벤치마킹에서 일반화한 성공·실패·미검증 사례

주요 라우팅:

- 프로젝트 운영체계: `docs/knowledge/methods/GAME_PROJECT_OPERATING_SYSTEM_METHOD.md`
- 전체 기획 체계: `docs/knowledge/methods/PLANNING_SYSTEM_METHOD.md`
- 프로젝트 인수인계: `docs/knowledge/methods/PROJECT_HANDOFF_CONTEXT_METHOD.md`
- AI 아트 프롬프트: `docs/knowledge/methods/AI_ART_PROMPT_TECHNIQUE_METHOD.md`
- 규칙·UI·연출·QA 추적성: `docs/knowledge/cases/TEN_PACES_RULE_PRESENTATION_TRACEABILITY_CASE.md`
- 이미지 목적·기준 교체: `docs/knowledge/cases/OMENWARD_UNIT_ROSTER_TO_BATTLEFIELD_SPRITE_REFERENCE_CASE.md`

실행 가능한 절차는 루트 `skills/`에 두고, 넓은 분야의 역량 지도와 참고 계약은 `docs/knowledge/skills/`에 둡니다.

## 주요 템플릿

| 파일 | 역할 |
|---|---|
| `templates/project-operations/README.md` | 게임 프로젝트 운영체계 키트 인덱스 |
| `templates/EXECUTABLE_PROMPT.md` | 목적·맥락·경험·범위·제약·산출물·완료·검증 |
| `templates/ai/PROJECT_AI_COLLABORATION_PROFILE.md` | 프로젝트별 GPT·DeepSeek·Codex 역할과 worktree 정책 |
| `templates/ai/DEEPSEEK_WORK_PACKAGE.md` | 외부 AI 대량 작업 입력·출력 계약 |
| `templates/ai/EXTERNAL_AI_DRAFT_REVIEW.md` | 외부 초안 검수 |
| `templates/planning/VERTICAL_SLICE_PLAN.md` | 버티컬 슬라이스 범위와 품질 기준 |
| `templates/planning/DESIGN_DOCUMENT_SYSTEM.md` | 기획서 책임 지도·로드맵·스킬 연결 |
| `templates/planning/ART_DIRECTION_BRIEF.md` | 아트 방향, 디자인 기술, 프롬프트 사례와 QA |
| `templates/skills/PROJECT_SKILL_EXTENSION.md` | Base 스킬의 프로젝트 전용 확장 |
| `templates/KNOWLEDGE_CASE_STUDY.md` | 일반화된 사례 연구 |

## 작업 종료·인수인계

1. 프로젝트 고유 결정과 구현 상태를 프로젝트 본책·Roadmap·테스트·Active Context에 반영합니다.
2. 공용으로 재사용할 수 있는 판단법, 절차, 템플릿과 체크리스트를 분리합니다.
3. 검증된 공용 데이터는 기존 Base method·skill·template에 반영합니다.
4. 문제, 선택, 결과, 실패와 미검증 항목은 사례로 기록합니다.
5. 미검증 내용은 확정 규칙이 아니라 `관찰` 또는 `가설`로 남깁니다.
6. Base 변경 뒤 프로젝트 로컬 사본과 기준 버전의 동기화 필요를 기록합니다.

## 동기화와 문서 수명주기

GitHub와 로컬 파일은 자동 양방향 동기화되지 않습니다. 로컬 변경은 commit·push, 원격 변경은 fetch·pull이 필요합니다.

- 한 주제에는 현행 책임 원본 하나만 유지합니다.
- `v2`, `final`, `latest`, 날짜별 활성 복제본을 만들지 않습니다.
- 이전 내용은 Git 이력으로 보존합니다.
- `archive`, `[백업]`, `hold`, `[보류]`는 활성 작업의 기본 읽기에서 제외합니다.
- 통합이 끝난 중복 파일은 참조와 고유 정보 확인 후 제거합니다.
