# Base

여러 프로젝트가 공유하는 **[학습형] [공용] AI 작업 규칙, 기획 지식, 실행 스킬과 템플릿**의 원본 저장소입니다.

Base는 프로젝트에서 얻은 문제 해결 방법, 실패 사례, 검증 결과를 일반화해 계속 학습·갱신하는 곳입니다. 각 프로젝트 저장소는 Base를 그대로 복제하는 곳이 아니라, 공용 지식을 자신의 세계관, 수치, 엔진, 파일 경로와 현재 구현 상태에 맞게 **분화·적용·검증하는 전용 작업 공간**입니다.

Base에는 특정 프로젝트의 활성 GDD, 세계관, 밸런스, 코드, 파일 경로를 두지 않습니다. 각 프로젝트는 필요한 Base 문서를 로컬 사본 또는 기준 커밋으로 연결하고, 프로젝트 전용 결정과 구현 상태는 자체 저장소에서 관리합니다.

## 운영 모델

```text
Base 공용 학습 데이터
→ 프로젝트별 전용 기획·스킬·구현으로 분화
→ 실제 작업·플레이테스트·검수
→ 성공·실패·미검증 사례 기록
→ 공용 원리와 프로젝트 고유 값 분리
→ Base method·skill·template·case 갱신
```

- Base는 `어떻게 판단하고 작업하며 검증할 것인가`를 학습한다.
- 프로젝트는 `이 게임에서 무엇을 만들고 현재 어디까지 구현했는가`를 관리한다.
- 프로젝트의 구체 결과는 프로젝트에 남기고, 반복 가능한 원리와 검증 방법만 Base로 환류한다.
- 한 번 성공한 방법은 먼저 사례·가설로 기록하고 반복 검증 뒤 공용 규칙이나 스킬로 승격한다.

## 구조

```text
AGENTS.md          최소 공용 규칙
docs/              상세 작업 규칙과 공용 지식
skills/            직접 적용 가능한 실행 스킬
templates/         프로젝트에 복사할 산출물 양식
```

## 시작 순서

Base 자체를 정비할 때:

```text
README.md
→ AGENTS.md
→ docs/DOCUMENTATION_MAP.md
→ 작업에 맞는 docs/knowledge 문서 또는 skills/<name>/SKILL.md
```

프로젝트 작업을 시작할 때는 **현재 작업에 적용되는 공용 기준 전체와 프로젝트 현행 기준 전체**를 함께 확인합니다. 이는 저장소 모든 파일을 무조건 읽는다는 뜻이 아니라, Documentation Map을 기준으로 관련 책임 원본과 영향 파일을 빠짐없이 읽는다는 뜻입니다.

```text
프로젝트 AGENTS.md
→ BASE_RULES_VERSION.md와 Base 로컬 사본
→ 프로젝트 Documentation Map
→ Handoff·Active Context
→ 프로젝트 방향과 관련 분야 책임 문서
→ 현재 Issue·Goal·Plan
→ 실제 수정 대상과 연결 파일
```

## 핵심 작업 문서

| 파일 | 역할 |
|---|---|
| `AGENTS.md` | 최소 공용 작업 규칙과 학습 환류 원칙 |
| `docs/AI_SHARED_WORK_RULES.md` | 역할, 범위, 품질, 파일 수명주기, Base 승격 |
| `docs/AI_WORKFLOW_RULES.md` | 요청 분류, 공용·전용 컨텍스트 확인, 검증과 학습 환류 |
| `docs/CONTENT_DESIGN_METHOD.md` | 의도→경험→규칙→흐름→검증 기반 콘텐츠 기획 |
| `docs/AI_SKILL_ADOPTION_GUIDE.md` | 스킬·외부 모델 검토, 권한, 비용, compact, 검증 |
| `docs/DOCUMENTATION_MAP.md` | 문서·스킬·템플릿 라우터 |
| `docs/knowledge/README.md` | 학습형 공용 methods·research·skill contracts·cases |
| `docs/CHANGELOG.md` | Base 버전 기록 |

## 실행 스킬

| 스킬 | 사용 시점 |
|---|---|
| `skills/transforming-requests-into-prompts/` | 짧거나 모호한 요청을 실행 가능한 프롬프트로 변환 |
| `skills/designing-vertical-slices/` | 핵심 경험을 대표하는 완성 구간과 제작 파이프라인 검증 |
| `skills/writing-game-design-documents/` | 기획서 종류, 책임 원본, 로드맵과 명세 구조 설계 |
| `skills/orchestrating-deepseek-worktrees/` | 대용량 초안·분류를 격리 worktree의 외부 AI에 위임 |
| `skills/reviewing-external-ai-drafts/` | 외부 AI 결과를 실제 diff·근거·테스트로 검수 |
| `skills/designing-art-prompts-and-technique-cards/` | 아트·UI 기술 추천, 이미지 프롬프트와 QA 카드 작성 |
| `skills/promoting-project-knowledge/` | 작업 종료·인수인계에서 프로젝트 교훈을 Base 학습 데이터로 환류 |

스킬은 도구 브랜드가 아니라 **사용 조건, 입력, 작업 절차, 산출물, 검증, 실패 기준**을 정의합니다.

## 공용 학습 지식

`docs/knowledge/`는 다음을 관리합니다.

- `methods/`: 반복 가능한 설계·제작 판단 방법
- `research/`: 정보 수집·벤치마킹·표준·근거 평가
- `skills/`: 분야별 능력 계약과 검수 매트릭스
- `cases/`: 프로젝트와 벤치마킹에서 일반화한 성공·실패·미검증 사례

주요 추가 라우팅:

- AI 아트 프롬프트·디자인 기술: `docs/knowledge/methods/AI_ART_PROMPT_TECHNIQUE_METHOD.md`
- FACS 프롬프트 참고표: `docs/knowledge/research/FACS_ACTION_UNIT_PROMPT_REFERENCE.md`
- FACS 표정 편집 사례: `docs/knowledge/cases/FACS_EXPRESSION_EDITING_PROMPT_CASE.md`
- 캐릭터 포스터 사례: `docs/knowledge/cases/CHARACTER_PROMO_POSTER_LAYOUT_CASE.md`
- 규칙·UI·연출·QA 추적성 사례: `docs/knowledge/cases/TEN_PACES_RULE_PRESENTATION_TRACEABILITY_CASE.md`
- 선택적 하이라이트 Vertical Slice 사례: `docs/knowledge/cases/TEN_PACES_OPTIONAL_HIGHLIGHT_VERTICAL_SLICE_CASE.md`
- 내부 데이터의 세계관 문구 변환 사례: `docs/knowledge/cases/DIEGETIC_OPPONENT_INFORMATION_CASE.md`

실행 가능한 절차는 루트 `skills/`에 두고, 넓은 분야의 역량 지도와 참고 계약은 `docs/knowledge/skills/`에 둡니다.

## 주요 템플릿

| 파일 | 역할 |
|---|---|
| `templates/EXECUTABLE_PROMPT.md` | 목적·맥락·경험·범위·제약·산출물·완료·검증 |
| `templates/ai/PROJECT_AI_COLLABORATION_PROFILE.md` | 프로젝트별 GPT·DeepSeek·Codex 역할과 worktree 정책 |
| `templates/ai/DEEPSEEK_WORK_PACKAGE.md` | 외부 AI 대량 작업 입력·출력 계약 |
| `templates/ai/EXTERNAL_AI_DRAFT_REVIEW.md` | Codex·책임자의 외부 초안 검수 |
| `templates/planning/VERTICAL_SLICE_PLAN.md` | 수직 슬라이스 범위와 품질 기준 |
| `templates/planning/DESIGN_DOCUMENT_SYSTEM.md` | 프로젝트 기획서 종류와 책임 원본 지도 |
| `templates/planning/ART_DIRECTION_BRIEF.md` | 아트 방향, 디자인 기술, 프롬프트 사례, QA |
| `templates/planning/ART_TECHNIQUE_CARD.md` | 아트·UI 디자인 기술 카드 |
| `templates/planning/EXPRESSION_CONTROL_CARD.md` | 캐릭터 표정·FACS 보조 제어 카드 |
| `templates/planning/CHARACTER_PROMO_POSTER_BRIEF.md` | 캐릭터 포스터·상세 페이지 정보 슬롯 설계 |
| `templates/skills/PROJECT_SKILL_EXTENSION.md` | Base 스킬의 프로젝트 전용 확장 |
| `templates/CONTENT_DESIGN_BRIEF.md` | 핵심 재미·첫 10분·PoC |
| `templates/KNOWLEDGE_CASE_STUDY.md` | 일반화된 사례 연구 |

## 작업 종료·인수인계

작업 종료와 인수인계에서는 다음을 수행합니다.

1. 프로젝트 고유 결정과 구현 상태를 프로젝트 기획서·로드맵·테스트·Active Context에 반영합니다.
2. 공용으로 재사용할 수 있는 판단법, 절차, 템플릿, 체크리스트를 분리합니다.
3. 검증된 공용 데이터는 기존 Base method·skill·template에 반영합니다.
4. 문제, 선택, 결과, 실패와 미검증 항목은 `templates/KNOWLEDGE_CASE_STUDY.md` 형식으로 사례화합니다.
5. 미검증 내용은 확정 규칙이 아니라 `관찰` 또는 `가설` 사례로 남깁니다.
6. Base 변경 뒤 프로젝트 로컬 사본과 버전 기록의 동기화 필요를 남깁니다.

## 공용화 기준

```text
프로젝트 문제
→ 프로젝트 전용 해결과 검증
→ 고유 정보와 공용 원리 분리
→ 기존 Base 책임 문서와 중복 확인
→ 규칙·method·skill·template·case 중 적절한 위치에 반영
→ 프로젝트 로컬 사본과 버전 기록의 동기화 확인
```

검증되지 않은 아이디어는 프로젝트의 `확인 필요` 또는 `보류`, 혹은 Base의 `관찰`·`가설` 사례에 남깁니다. 특정 프로젝트의 이름, 수치, 세계관, 엔진 경로와 일회성 구현 세부는 Base로 승격하지 않습니다.

## 동기화

GitHub와 로컬 파일은 자동 양방향 동기화되지 않습니다. 로컬 변경은 commit·push, 원격 변경은 fetch·pull이 필요합니다. 프로젝트에 `docs/BASE_RULES_VERSION.md`가 있으면 기준 Base 커밋과 동기화 날짜를 기록합니다.

## 문서 수명주기

- 한 주제에는 현행 책임 문서 하나만 유지합니다.
- `v2`, `final`, `latest`, 날짜별 활성 복제본을 만들지 않습니다.
- 이전 내용은 Git 이력으로 보존합니다.
- `archive`, `[백업]`, `hold`, `[보류]`는 활성 작업의 기본 읽기에서 제외합니다.
- 통합이 끝난 중복 파일은 참조 확인 후 제거합니다.
