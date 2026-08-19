# Base 시작 지점

> Base v9 RC status and release boundary: `docs/BASE_RULES_VERSION.md`
> Registry-derived active Skill view: `docs/generated/BASE_ACTIVE_SKILLS.md`
> GPT-first project lifecycle: `docs/GPT_FIRST_PROJECT_WORKFLOW.md`
> Human-facing project workspace: Notion / structured-runtime truth: repository

이 문서는 새 채팅, 새 GPT, 새 Codex 또는 새 작업자가 Base와 프로젝트 작업의 책임 원본을 찾는 요청별 한 단계 라우터다. 전체 운영 설명은 `docs/OPERATING_MODEL.md`, 항상 적용되는 규칙은 `AGENTS.md`, 장기 작업은 `docs/LONG_HORIZON_WORK_EXECUTION_POLICY.md`, Work Mode·Skill 선택은 `docs/WORK_MODE_AND_SKILL_ROUTING.md`, 문서 위치는 `docs/DOCUMENTATION_MAP.md`가 책임진다.

## 사용자가 기억할 최소 요청

> `https://github.com/alsdmlals4-eng/Base 를 살펴보고 현재 프로젝트 GitHub와 Notion 정본을 함께 확인한 뒤 작업해줘.`

`살펴본다`는 모든 파일과 Skill을 무작정 읽는 뜻이 아니다. 현재 요청에 필요한 책임 원본과 최소 Skill만 `skills/SKILL_REGISTRY.json`과 `docs/generated/BASE_ACTIVE_SKILLS.md`에서 선별한다. 저장소·Notion 접근 없이 확인한 사실처럼 말하지 않는다.

## 최초 읽기 순서

```text
Base START_HERE.md · AGENTS.md
→ docs/GPT_FIRST_PROJECT_WORKFLOW.md
→ docs/OPERATING_MODEL.md
→ docs/LONG_HORIZON_WORK_EXECUTION_POLICY.md
→ docs/WORK_MODE_AND_SKILL_ROUTING.md
→ docs/DOCUMENTATION_MAP.md
→ skills/SKILL_REGISTRY.json
→ 대상 프로젝트 AGENTS.md · 프로젝트 START_HERE
→ project GitHub latest main / confirmed decisions / actual files
→ exact Project Notion Home and relevant project-filtered surfaces
→ current responsibility owner / code / data / assets / tests
```

Google Sheets는 기본 읽기 대상이 아니다. 기존 Sheet에 **고유 미이관 정보가 남아 있다고 확인된 일회성 migration 작업**에서만 `docs/PROJECT_GDD_GOOGLE_SHEETS_POLICY.md`와 `docs/DEPRECATED_PROJECT_SURFACE_RETIREMENT_POLICY.md`를 읽는다.

신규 MCP·addon·CLI·framework·Skill·Mode 또는 유사 실행 계층 제작 요청은 설계보다 먼저 Existing Solution First Gate를 통과한다. 사용자-facing localhost 도구나 독립 HTML 프로젝트 dashboard를 새 기본 surface로 만들지 않는다.

## 기본 프로젝트 작업 순서

```text
GPT PRIMARY
→ GitHub + Notion current-state audit
→ planning / research / >=3 viable alternatives / benchmark
→ system / data / UX / UI / art direction review
→ representative Notion visual checkpoint when visuals matter
→ user approval
→ approved-scope adversarial review
→ GitHub / Notion sync preparation
→ optional Codex sub-executor only when actual repository/engine work needs it
→ GPT final review
→ exact-head PR gate / merge
→ GitHub main + Notion readback
→ user-learning completion report
```

Codex는 기본 주 책임자가 아니다. 실제 저장소·Godot mutation, 다수 파일 구현·테스트, 로컬 재현이 필요할 때만 `CODEX_OPTIONAL_SUB_EXECUTOR`로 사용한다. 필요한 경우 `docs/operations/POWERSHELL_FRESH_SHELL_EXECUTION_CONTRACT.md`와 `docs/GPT_CODEX_WORKFLOW_POLICY.md`에 따라 새 PowerShell에서 **한 번에 붙여넣는 실행 블록**을 우선 제공한다.

## Base 저장소 자체를 콜드 스타트할 때

Base는 프로젝트 운영 키트의 공용 원본이다. 프로젝트 전용 상태 파일을 Base의 활성 현재 상태로 오인하지 않는다.

- 확정 운영 계약: `AGENTS.md`, `START_HERE.md`, `docs/OPERATING_MODEL.md`, `docs/LONG_HORIZON_WORK_EXECUTION_POLICY.md`
- GPT 주 책임 / Codex 선택 보조: `docs/GPT_FIRST_PROJECT_WORKFLOW.md`
- Notion 사람용 visual/asset/flow: `docs/knowledge/game-development/NOTION_VISUAL_ASSET_AND_FLOW_WORKFLOW.md`
- Notion/GitHub 권위 분할: `docs/operations/PROJECT_WORKSPACE_AUTHORITY_CONTRACT.json`
- 다른 프로젝트/채팅 동시 작업 격리: `docs/operations/NOTION_PROJECT_ISOLATION_AND_CORE_SYSTEM_CONTRACT.md` + long-horizon workstream isolation
- 폐기 surface 흡수·삭제: `docs/DEPRECATED_PROJECT_SURFACE_RETIREMENT_POLICY.md`
- 사용자 PowerShell 실행: `docs/operations/POWERSHELL_FRESH_SHELL_EXECUTION_CONTRACT.md`
- repository-native QA: exact commit/PR head + test/build/runtime screenshot/video/log/Actions artifact; 별도 localhost QA 앱을 요구하지 않음
- Google Sheets: `RETIRED_MIGRATION_ONLY`; 고유 정보의 일회성 이관 뒤 active reference 제거
- 독립 HTML project dashboard 및 사용자-facing local project apps: `RETIRED`
- Android 실기기 검증은 프로젝트 PC 구현 완료 후 출시 준비 직전까지 `DEFERRED_NOT_CONNECTED`로 유지할 수 있으며 PASS로 바꾸지 않는다.
- 완료된 Base 변경: `docs/CHANGELOG.md`
- 활성 Skill: `skills/SKILL_REGISTRY.json`
- 이전 Skill ID: `skills/LEGACY_SKILL_ALIASES.md`
- 검토 대기 제안: `[수정제안서]/PROPOSAL_REGISTRY.json`
- 진행 중 구현과 실제 검사: GitHub Issue·PR·Actions

## 요청별 라우팅

먼저 `managing-project-intake-and-work-contract`에서 사용자 의도·저장소/Notion 사실·범위·승인·실행 계약을 한 번만 처리한 뒤 아래 주 책임으로 이동한다.

| 요청 | 주 책임·mode | 다음 파일 |
|---|---|---|
| 신규 프로젝트 운영체계 설치 | `managing-game-project-operating-system: install / verify` | `skills/managing-game-project-operating-system/SKILL.md` |
| 기존 프로젝트 구조 감사·마이그레이션 | `managing-game-project-operating-system: audit / reconcile-legacy / migrate / verify` | `skills/managing-game-project-operating-system/SKILL.md` |
| 구형 surface·자료 흡수·삭제 | `governing-legacy-retention-and-archives` + pruning | `docs/DEPRECATED_PROJECT_SURFACE_RETIREMENT_POLICY.md` |
| 핵심 컨셉·DDD·벤치마크·플레이테스트·PoC | `analyzing-and-refining-game-concepts` | `skills/analyzing-and-refining-game-concepts/SKILL.md` |
| 게임 시스템·난이도·전투 AI | `analyzing-and-refining-game-concepts: system-design / difficulty-and-combat-ai` | `skills/analyzing-and-refining-game-concepts/SKILL.md` |
| 기존 프로젝트 코어 판정 | `identifying-project-core` | `skills/identifying-project-core/SKILL.md` |
| 기획 단계 프로젝트 코어 확정 | `establishing-project-core` | `skills/establishing-project-core/SKILL.md` |
| 튜토리얼·온보딩·첫 세션 | `analyzing-and-refining-game-concepts: tutorial-and-onboarding-design` | `skills/analyzing-and-refining-game-concepts/SKILL.md` |
| 소설·웹소설·연재소설 | `developing-and-revising-serial-fiction` | `skills/developing-and-revising-serial-fiction/SKILL.md` |
| Windows+Android delivery | 기존 기획·기술·Vertical Slice·검증 Skill | `docs/knowledge/game-development/PC_ANDROID_CROSS_PLATFORM_DELIVERY_GUIDE.md` |
| build/package/자산 용량 최적화 | 기존 기획·아트·Vertical Slice·검증 Skill | `docs/knowledge/game-development/GAME_BUILD_SIZE_AND_ASSET_OPTIMIZATION_GUIDE.md` |
| 적대적 검토·전수 감사 | `running-adversarial-review-and-refinement` | `skills/running-adversarial-review-and-refinement/SKILL.md` |
| 일반 변경·완료 주장 검증 | `reviewing-and-validating-project-changes` | `skills/reviewing-and-validating-project-changes/SKILL.md` |
| 정본·경로·ID·Schema 전파 누락 | `auditing-canonical-reference-freshness` | `skills/auditing-canonical-reference-freshness/SKILL.md` |
| 기획 책임 원본 작성·구조 변경 | `managing-design-documents` | `skills/managing-design-documents/SKILL.md` |
| 프로젝트 Skill 생성·통합·학습 | `evolving-project-discipline-skills` | `skills/evolving-project-discipline-skills/SKILL.md` |
| 현재 상태·다음 작업·Handoff | `maintaining-project-context-and-handoff` | `skills/maintaining-project-context-and-handoff/SKILL.md` |
| 실제 구현에 Codex가 필요한 경우 | `maintaining-project-context-and-handoff: on-demand-codex-handoff` | `docs/GPT_FIRST_PROJECT_WORKFLOW.md` + `docs/GPT_CODEX_WORKFLOW_POLICY.md` |
| 프로젝트 교훈의 Base 제안 | `managing-base-change-proposals` | `skills/managing-base-change-proposals/SKILL.md` |
| Vertical Slice 품질·플레이 | `designing-vertical-slices` | `skills/designing-vertical-slices/SKILL.md` |
| 이미지·시각 자산·UI 후보 | 기존 아트·UX Skill 조합 | `docs/knowledge/game-development/NOTION_VISUAL_ASSET_AND_FLOW_WORKFLOW.md` |
| 아트 프롬프트·기술 카드 | `designing-art-prompts-and-technique-cards` | `skills/designing-art-prompts-and-technique-cards/SKILL.md` |
| 게임 UX/UI 설계·감사 | `auditing-and-refining-ui-art` | `skills/auditing-and-refining-ui-art/SKILL.md` |
| Godot 에셋·플러그인 제작 전 조사 | `evaluating-godot-assets-and-plugins-before-creation` | `skills/evaluating-godot-assets-and-plugins-before-creation/SKILL.md` |
| Steam·STOVE·Google Play 권리·심사 | 기존 운영·에셋·아트·검증 Skill | `docs/knowledge/game-development/PLATFORM_REVIEW_ASSET_RIGHTS_AND_REFERENCE_PRODUCTION_GUIDE.md` |
| 사용자 학습형 완료 설명 | `creating-user-learning-notes` 또는 현재 주 책임 Skill의 완료보고 | `docs/GPT_FIRST_PROJECT_WORKFLOW.md` |

## 보조 라우트

| 요청 | 다음 책임 |
|---|---|
| 로컬·GitHub drift | `synchronizing-local-and-github-state` |
| 긴 작업 checkpoint·재개 | `maintaining-long-running-task-continuity` |
| 구조 단순화·동작 보존 리팩터링 | `simplifying-skill-bodies` / `refactoring-with-contract-preservation` |
| 불필요 자료 판정 | `pruning-stale-and-nonfunctional-material` |
| 게임 사용자 연구 | `governing-game-user-research-coverage` |
| 사용자 학습 자료 | `creating-user-learning-notes` |
| 프로젝트 상태·관계 시각화 | Notion Project Home / Core System / Visual Map; 독립 HTML dashboard는 사용하지 않음 |
| Godot·Unity 런타임 오류 | `diagnosing-game-engine-runtime-failures` |
| Godot live Editor·Scene·Resource 자동화 | 프로젝트가 채택한 persistent authoring authority + deterministic tests + 필요 시 live QA |

전체 원문 책임 매핑은 `docs/SKILL_COVERAGE_MAP.md`, 기계 검증은 `skills/SKILL_COVERAGE.json`을 사용한다. 활성 Skill의 trigger·비사용 조건·입력·출력·실패·검증은 `skills/SKILL_REGISTRY.json`과 해당 `SKILL.md`가 책임진다.

## 일반 프로젝트 읽기 순서

```text
프로젝트 AGENTS.md
→ 프로젝트 START_HERE / ACTIVE_CONTEXT / DOCUMENTATION_MAP / DEVELOPMENT_GATES
→ CURRENT_CONFIRMED_DECISIONS
→ DESIGN_DOCUMENT_REGISTRY / 현재 분야 책임 원본
→ actual code / data / scenes / resources / assets / tests
→ exact Project Notion Home / project-filtered Work·Asset·Core System·Visual surfaces
→ 관련 Issue / PR / Plan
```

변경 후 정본·Notion·실제 구현의 영향 범위를 대조한다. 과거 Skill ID는 `skills/LEGACY_SKILL_ALIASES.md`에서 현행 Skill·mode로 해석한다.

## Cloud Run 게임 백엔드 진입

서버 기능이 감지되면 `docs/knowledge/game-development/GAME_BACKEND_CLOUD_RUN_AND_ONLINE_SERVICES_GUIDE.md`에서 적합성 Gate를 시작한다. 실제 배포·부하·장애·비용 검증 전에는 `PRODUCTION_READY`를 선언하지 않는다.

## 게임 권한·무결성·DRM 진입

entitlement, Play Integrity, Steam DRM Wrapper, STOVE 기능, anti-tamper, offline license 또는 고가치 서버 권위 질문은 `docs/knowledge/game-development/GAME_ENTITLEMENT_INTEGRITY_AND_DRM_GUIDE.md`에서 시작한다. platform sandbox와 사람 복구 증거 전에는 `PRODUCTION_READY`를 선언하지 않는다.
