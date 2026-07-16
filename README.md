# Base

여러 프로젝트가 공유하는 **AI 작업 규칙, 공용 기획 지식, 실행 가능한 스킬과 템플릿**의 원본 저장소입니다.

Base에는 특정 프로젝트의 활성 GDD, 세계관, 밸런스, 코드, 파일 경로를 두지 않습니다. 각 프로젝트는 필요한 Base 문서를 로컬 사본 또는 기준 커밋으로 연결하고, 프로젝트 전용 결정과 구현 상태는 자체 저장소에서 관리합니다.

## 구조

```text
AGENTS.md          최소 공용 규칙
docs/              상세 작업 규칙과 공용 지식
skills/            직접 적용 가능한 실행 스킬
templates/         프로젝트에 복사할 산출물 양식
```

## 시작 순서

```text
README.md
→ AGENTS.md
→ docs/DOCUMENTATION_MAP.md
→ 작업에 맞는 docs/knowledge 문서 또는 skills/<name>/SKILL.md
```

프로젝트 작업에서는 Base 원격보다 프로젝트의 `AGENTS.md`, Handoff·Active Context, 현재 Issue·Goal, Base 로컬 사본을 우선합니다.

## 핵심 작업 문서

| 파일 | 역할 |
|---|---|
| `AGENTS.md` | 최소 공용 작업 규칙 |
| `docs/AI_SHARED_WORK_RULES.md` | 역할, 범위, 품질, 파일 수명주기, Base 승격 |
| `docs/AI_WORKFLOW_RULES.md` | 요청 분류부터 검증까지의 공통 흐름 |
| `docs/CONTENT_DESIGN_METHOD.md` | 의도→경험→규칙→흐름→검증 기반 콘텐츠 기획 |
| `docs/AI_SKILL_ADOPTION_GUIDE.md` | 외부 스킬 검토, 권한, compact, 검증 |
| `docs/DOCUMENTATION_MAP.md` | 문서·스킬·템플릿 라우터 |
| `docs/knowledge/README.md` | methods·research·skill contracts·cases 지식 베이스 |
| `docs/CHANGELOG.md` | Base 버전 기록 |

## 실행 스킬

| 스킬 | 사용 시점 |
|---|---|
| `skills/transforming-requests-into-prompts/` | 짧거나 모호한 요청을 실행 가능한 프롬프트로 변환 |
| `skills/designing-vertical-slices/` | 핵심 경험을 대표하는 완성 구간과 제작 파이프라인 검증 |
| `skills/writing-game-design-documents/` | 기획서 종류, 책임 원본, 로드맵과 명세 구조 설계 |
| `skills/promoting-project-knowledge/` | 프로젝트 교훈을 Base 규칙·method·skill·case로 승격 |

스킬은 도구 브랜드가 아니라 **사용 조건, 입력, 작업 절차, 산출물, 검증, 실패 기준**을 정의합니다.

## 공용 지식

`docs/knowledge/`는 다음을 관리합니다.

- `methods/`: 반복 가능한 설계·제작 판단 방법
- `research/`: 정보 수집·벤치마킹·근거 평가
- `skills/`: 분야별 능력 계약과 검수 매트릭스
- `cases/`: 프로젝트와 벤치마킹에서 일반화한 사례

실행 가능한 절차는 루트 `skills/`에 두고, 넓은 분야의 역량 지도와 참고 계약은 `docs/knowledge/skills/`에 둡니다.

## 주요 템플릿

| 파일 | 역할 |
|---|---|
| `templates/EXECUTABLE_PROMPT.md` | 목적·맥락·경험·범위·제약·산출물·완료·검증 |
| `templates/planning/VERTICAL_SLICE_PLAN.md` | 수직 슬라이스 범위와 품질 기준 |
| `templates/planning/DESIGN_DOCUMENT_SYSTEM.md` | 프로젝트 기획서 종류와 책임 원본 지도 |
| `templates/skills/PROJECT_SKILL_EXTENSION.md` | Base 스킬의 프로젝트 전용 확장 |
| `templates/CONTENT_DESIGN_BRIEF.md` | 핵심 재미·첫 10분·PoC |
| `templates/KNOWLEDGE_CASE_STUDY.md` | 일반화된 사례 연구 |

## 공용화 기준

```text
프로젝트 문제
→ 프로젝트 전용 해결과 검증
→ 고유 정보와 공용 원칙 분리
→ 기존 Base 책임 문서와 중복 확인
→ 규칙·method·skill·template·case 중 적절한 위치에 반영
→ 프로젝트 로컬 사본과 버전 기록의 동기화 확인
```

검증되지 않은 아이디어는 프로젝트의 `확인 필요` 또는 `보류`에 남깁니다. 특정 프로젝트의 이름, 수치, 세계관, 엔진 경로와 일회성 구현 세부는 Base로 승격하지 않습니다.

## 동기화

GitHub와 로컬 파일은 자동 양방향 동기화되지 않습니다. 로컬 변경은 commit·push, 원격 변경은 fetch·pull이 필요합니다. 프로젝트에 `docs/BASE_RULES_VERSION.md`가 있으면 기준 Base 커밋과 동기화 날짜를 기록합니다.

## 문서 수명주기

- 한 주제에는 현행 책임 문서 하나만 유지합니다.
- `v2`, `final`, `latest`, 날짜별 활성 복제본을 만들지 않습니다.
- 이전 내용은 Git 이력으로 보존합니다.
- `archive`, `[백업]`, `hold`, `[보류]`는 활성 작업의 기본 읽기에서 제외합니다.
- 통합이 끝난 중복 파일은 참조 확인 후 제거합니다.
