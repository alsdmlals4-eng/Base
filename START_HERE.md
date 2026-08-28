# Base 시작 지점

> Base v9 RC status and release boundary: `docs/BASE_RULES_VERSION.md`
> Registry-derived active Skill view: `docs/generated/BASE_ACTIVE_SKILLS.md`
> Game-system routes: `system-design` / `difficulty-and-combat-ai` → `skills/analyzing-and-refining-game-concepts/SKILL.md`

이 문서는 새 채팅, 새 GPT, 새 Codex 또는 새 작업자가 Base와 프로젝트 작업의 책임 원본을 찾는 요청별 한 단계 라우터다. 전체 운영 설명은 `docs/OPERATING_MODEL.md`, 항상 적용되는 규칙은 `AGENTS.md`, 프로젝트 workspace·정본 계약은 `docs/DESKTOP_GPT_REPOSITORY_FIRST_WORKSPACE_POLICY.md`와 `docs/operations/PROJECT_WORKSPACE_AUTHORITY_CONTRACT_V4.json`, Work Mode·Skill 선택은 `docs/WORK_MODE_AND_SKILL_ROUTING.md`, 공용 용어 정의·컨텍스트 압축은 `docs/CONTROLLED_VOCABULARY.md`, 문서 위치는 `docs/DOCUMENTATION_MAP.md`가 책임진다.

## 사용자가 기억할 최소 요청

> `https://github.com/alsdmlals4-eng/Base 를 전부 살펴보고 참고해서 이 프로젝트를 작업해줘.`

`전부 살펴본다`는 모든 파일과 Skill을 무작정 읽는 뜻이 아니다. 현재 요청에 필요한 책임 원본과 최소 Skill만 `skills/SKILL_REGISTRY.json`과 `docs/generated/BASE_ACTIVE_SKILLS.md`에서 선별한다. 저장소 접근 없이 설치·마이그레이션·검수 완료를 주장하지 않는다.

## 최초 읽기 순서

```text
Base START_HERE.md·AGENTS.md
→ docs/DESKTOP_GPT_REPOSITORY_FIRST_WORKSPACE_POLICY.md
→ docs/operations/PROJECT_WORKSPACE_AUTHORITY_CONTRACT_V4.json
→ docs/OPERATING_MODEL.md
→ docs/WORK_MODE_AND_SKILL_ROUTING.md
→ docs/DOCUMENTATION_MAP.md
→ skills/SKILL_REGISTRY.json
→ 대상 프로젝트 AGENTS.md·프로젝트 START_HERE
→ ACTIVE_CONTEXT·승인 Decision·AI production spec·asset manifest·현재 handoff
→ 현재 책임 원본·실제 코드·데이터·자산·테스트
→ 실제 migration scope일 때만 legacy Notion/Google Sheets 고유 자료
```

`REUSE_FIRST_PREFLIGHT_REQUIRED`: 신규 또는 의미 있게 개정하는 시스템·UI/UX·시각/Asset·데이터/콘텐츠 구조·도구·workflow·Skill/Eval·QA/Test는 새 설계·제작 전에 `managing-project-intake-and-work-contract`를 통해 현재 프로젝트 구현/자산 → Project Asset/Reference/Benchmark → Base reuse handoff/profile/Registry와 축적 knowledge/case/reference → 직접 관련된 targeted cross-project evidence → 결정에 필요한 외부 benchmark 순으로 확인한다. 모든 프로젝트를 무작정 전수 검색하거나 Base reference를 프로젝트 정본보다 우선하지 않는다. 상세 계약은 `skills/managing-project-intake-and-work-contract/SKILL.md`와 `docs/knowledge/game-development/reuse/adoption/PROJECT_WORK_REUSE_HANDOFF.json`이 소유한다.

기본 프로젝트 작업 계약은 `DESKTOP_GPT_REPOSITORY_FIRST_WORKSPACE`다. repository가 `REPOSITORY_PRIMARY_CANON`, 사람용 상세 기획서 PDF가 `HUMAN_GDD_PDF_DERIVED_VIEW`, AI용 상세 기획·구현 명세 Markdown이 repository canon이다. `NO_NEW_NOTION_WRITE_BY_DEFAULT`이며 기존 `NOTION_DEFAULT_PROJECT_WORKSPACE`는 `NOTION_DEFAULT_PROJECT_WORKSPACE_RETIRED`다. legacy Notion과 Google Sheets는 **현재 작업이 실제 migration scope일 때만** `templates/project-operations/NOTION_TO_REPOSITORY_MIGRATION_CHECKLIST.md`, `docs/PROJECT_GDD_GOOGLE_SHEETS_POLICY.md`, `docs/DEPRECATED_PROJECT_SURFACE_RETIREMENT_POLICY.md`를 읽어 고유 자료를 repository 또는 명시적 non-canon 보관소로 이관한다. 통합 Vertical Slice 실행이 승인된 경우에만 `templates/prompts/VERTICAL_SLICE_INTEGRATED_EXECUTION_PROMPT_v9.md`를 사용한다. 이 Prompt와 과거 v6~v8 자료는 최신 사용자 결정·프로젝트 정본보다 높은 권한을 갖지 않는다.

신규 MCP·addon·CLI·framework·Skill·Mode 또는 유사 실행 계층 제작 요청은 설계보다 먼저 `evaluating-godot-assets-and-plugins-before-creation: inventory-current-environment / disposition`으로 라우팅하고 `docs/knowledge/godot/HIGODOT_SINGLE_AUTHORITY_AND_SAFE_OPERATION.md`의 Existing Solution First Gate를 통과한다. 이미 사용 중인 도구·연결된 MCP·enabled addon·dependency·관련 PR·외부 대안을 확인하지 않은 `BUILD_NEW`는 시작하지 않는다.

## Base 저장소 자체를 콜드 스타트할 때

Base는 프로젝트 운영 키트의 공용 원본이다. 프로젝트 전용 상태 파일을 Base의 활성 현재 상태로 오인하지 않는다.

- `templates/project-operations/`: 대상 프로젝트에 설치할 Template이며 Base의 활성 상태가 아니다.
- 확정된 운영 계약: `AGENTS.md`, `START_HERE.md`, `docs/DESKTOP_GPT_REPOSITORY_FIRST_WORKSPACE_POLICY.md`, `docs/operations/PROJECT_WORKSPACE_AUTHORITY_CONTRACT_V4.json`, `docs/OPERATING_MODEL.md`, `docs/DOCUMENTATION_MAP.md`
- 사용자 PowerShell 실행이 필요한 작업: `docs/operations/POWERSHELL_FRESH_SHELL_EXECUTION_CONTRACT.md` — 새 PowerShell 기준, 위치 세팅 우선, 한 번에 붙여넣는 단일 블록, stage별 오류 위치 표시
- `RETIRED_HISTORY_ONLY`: 폐기된 Tool Hub·Expression Studio·Sprite Animation Studio의 과거 설계와 migration 증거는 Git 이력·명시적 archive에서만 찾는다. 현재 실행 경로·신규 설치 경로로 안내하지 않는다.
- `QA_EVIDENCE_STUDIO_RETIRED_FROM_ACTIVE_PROJECT_FLOW`: historical implementation `tools/qa-evidence-studio/README.md` is history/reference only; active project QA uses repository-native evidence and does not route through this tool.
- Android 실기기 검증은 프로젝트 PC 구현 완료 후 출시 준비 직전까지 `DEFERRED_NOT_CONNECTED`로 유지할 수 있으며, 이를 PASS나 누락으로 바꾸지 않는다.
- 완료된 Base 변경: `docs/CHANGELOG.md`.
- 활성 Skill: `skills/SKILL_REGISTRY.json`.
- 이전 Skill ID: `skills/LEGACY_SKILL_ALIASES.md`.
- 검토 대기 제안: `[수정제안서]/PROPOSAL_REGISTRY.json`과 개별 `PROPOSAL.md`.
- 진행 중 구현과 실제 검사: GitHub PR·Actions. 단, open/draft/ready 상태만으로 active worker라고 추정하지 않고 사용자 지시·현재 세션·Resource Lock 등 current-owner evidence를 확인한다.

활성 Base 인터뷰가 없으면 `등록 없음`, 제출 제안의 우선순위가 승인되지 않았으면 `사용자 검토 대기·우선순위 미확정`으로 답한다.

## 요청별 라우팅

먼저 `managing-project-intake-and-work-contract`에서 사용자 의도·저장소 사실·범위·승인·실행 계약을 한 번만 처리한 뒤 아래 주 책임으로 이동한다. 각 행은 다음 한 파일만 가리키며 상세 절차를 이 문서에 복제하지 않는다.

| 요청 | 주 책임·mode | 다음 파일 |
|---|---|---|
| 신규 프로젝트 운영체계 설치 | `managing-game-project-operating-system: install / verify` | `skills/managing-game-project-operating-system/SKILL.md` |
| 기존 프로젝트 구조 감사·마이그레이션 | `managing-game-project-operating-system: audit / reconcile-legacy / migrate / verify` | `skills/managing-game-project-operating-system/SKILL.md` |
| 신규 MCP·addon·CLI·framework·Skill·Mode 제작 전 현재 환경·기존 대안 조사 | `evaluating-godot-assets-and-plugins-before-creation: inventory-current-environment / disposition` | `docs/knowledge/godot/HIGODOT_SINGLE_AUTHORITY_AND_SAFE_OPERATION.md` + `skills/evaluating-godot-assets-and-plugins-before-creation/SKILL.md` |
| HiGodot 도입·exact pin·canary·업데이트·rollback | `managing-game-project-operating-system: install / verify` + Godot 평가 Skill | `docs/knowledge/godot/HIGODOT_SINGLE_AUTHORITY_AND_SAFE_OPERATION.md` + `templates/project-operations/HIGODOT_ADOPTION_RECORD.json` |
| Godot 구현·GDScript 테스트·실행 QA | HiGodot persistent authoring → adopted GUT deterministic test → adopted Hera `LIVE_QA_AND_OBSERVABILITY_ONLY` | `docs/knowledge/godot/HIGODOT_SINGLE_AUTHORITY_AND_SAFE_OPERATION.md` + `templates/project-operations/.agents/skills/godot-live-editor-operations/SKILL.md` |
| 구형 자료 분류·보존·Archive·승인 삭제 | `governing-legacy-retention-and-archives` | `skills/governing-legacy-retention-and-archives/SKILL.md` |
| 핵심 컨셉·DDD·벤치마크·플레이테스트·PoC | `analyzing-and-refining-game-concepts` | `skills/analyzing-and-refining-game-concepts/SKILL.md` |
| 실무 개발 용어 정의·컨텍스트 압축·용어 충돌 확인 | 기존 주 책임 Skill + 공용 통제 어휘 색인 | `docs/CONTROLLED_VOCABULARY.md` |
| 튜토리얼·온보딩·첫 세션 학습·성장 체감 | `analyzing-and-refining-game-concepts: tutorial-and-onboarding-design` | `skills/analyzing-and-refining-game-concepts/SKILL.md` |
| 소설·웹소설·연재소설 기획·각색·원고 퇴고·POV·회차 pacing·독자 반응 진단 | `developing-and-revising-serial-fiction` | `skills/developing-and-revising-serial-fiction/SKILL.md` + `docs/knowledge/serial-fiction/README.md` |
| Windows+Android 동시 목표·공용 코어·입력/UI/lifecycle·STOVE·Google Play·Steam 출시 wave | `analyzing-and-refining-game-concepts` + 기존 기술·Vertical Slice·검증 Skill | `docs/knowledge/game-development/PC_ANDROID_CROSS_PLATFORM_DELIVERY_GUIDE.md` + `templates/planning/PC_ANDROID_DELIVERY_PROFILE.md` |
| 게임 build/package/download/install/patch·font/texture/audio 자산 용량 최적화 | 기존 기획·아트·Vertical Slice·검증 Skill 조합 | `docs/knowledge/game-development/GAME_BUILD_SIZE_AND_ASSET_OPTIMIZATION_GUIDE.md` + `templates/planning/PC_ANDROID_DELIVERY_PROFILE.md` |
| 게임 시스템·난이도·전투 AI | `analyzing-and-refining-game-concepts: system-design / difficulty-and-combat-ai` | `skills/analyzing-and-refining-game-concepts/SKILL.md` |
| 기존 프로젝트 코어 판정 | `identifying-project-core` | `skills/identifying-project-core/SKILL.md` |
| 기획 단계 프로젝트 코어 확정 | `establishing-project-core` | `skills/establishing-project-core/SKILL.md` |
| 적대적 검토·저장소 전수 감사·승인 finding 개선 | `running-adversarial-review-and-refinement` | `skills/running-adversarial-review-and-refinement/SKILL.md` |
| 일반 변경·외부 AI 결과 검증 | `reviewing-and-validating-project-changes` | `skills/reviewing-and-validating-project-changes/SKILL.md` |
| 정본·경로·ID·Schema 전파 누락 | `auditing-canonical-reference-freshness` | `skills/auditing-canonical-reference-freshness/SKILL.md` |
| 기획 책임 원본 작성·구조 변경·발행 | `managing-design-documents` | `skills/managing-design-documents/SKILL.md` |
| 프로젝트 Skill 생성·통합·학습 | `evolving-project-discipline-skills` | `skills/evolving-project-discipline-skills/SKILL.md` |
| 현재 상태·다음 작업·Handoff | `maintaining-project-context-and-handoff` | `skills/maintaining-project-context-and-handoff/SKILL.md` |
| 실제 게임 프로젝트 Godot 제품 구현·Codex 인계 | `maintaining-project-context-and-handoff: codex-godot-implementation-handoff` | `docs/GPT_CODEX_WORKFLOW_POLICY.md` + `templates/project-operations/CODEX_IMPLEMENTATION_WORK_INSTRUCTION.md` |
| 프로젝트 교훈의 Base 제안·승인 구현 | `managing-base-change-proposals` | `skills/managing-base-change-proposals/SKILL.md` |
| Vertical Slice 품질·플레이·제작 파이프라인 | `designing-vertical-slices` | `skills/designing-vertical-slices/SKILL.md` |
| 프로젝트별 필요 이미지·시각 자산·UI 컴포넌트 선정·우선순위·제작 방식 | 기존 아트·UX·자산 평가 Skill 조합 | `docs/knowledge/game-development/ART_DIRECTION_AND_ASSET_PLANNING_GUIDE.md`의 `Visual Requirement Gate` |
| 아트 프롬프트·기술 카드 | `designing-art-prompts-and-technique-cards` | `skills/designing-art-prompts-and-technique-cards/SKILL.md` |
| Godot 에셋·플러그인 제작 전 조사·라이선스·구매 판단 | `evaluating-godot-assets-and-plugins-before-creation` | `skills/evaluating-godot-assets-and-plugins-before-creation/SKILL.md` |
| Steam·STOVE·Google Play 등급·설문·자산 권리·참조 독립 제작 | 기존 프로젝트 운영·에셋 평가·아트·Vertical Slice·검증 Skill 조합 | `docs/knowledge/game-development/PLATFORM_REVIEW_ASSET_RIGHTS_AND_REFERENCE_PRODUCTION_GUIDE.md` |
| 게임 UX/UI 설계·폴리싱·구현 결과 감사 | `auditing-and-refining-ui-art` | `skills/auditing-and-refining-ui-art/SKILL.md` |
| 외부 AI 작업 공간 운용 | `orchestrating-deepseek-worktrees` | `skills/orchestrating-deepseek-worktrees/SKILL.md` |
| AI 모델·추론 effort·Prompt cache·실측 비용 최적화 | `optimizing-ai-model-and-prompt-costs` | `skills/optimizing-ai-model-and-prompt-costs/SKILL.md` |

플랫폼·자산 Guide는 새 광역 Skill이 아니다. 프로젝트의 `ASSET_RIGHTS_AND_PROVENANCE_RECORD`와 `GAME_RELEASE_COMPLIANCE_EVIDENCE_PACK`을 기존 책임 경로가 생산·검증하며, 필수 증거가 없으면 `RELEASE_BLOCKED_UNVERIFIED`다.

PC·Android Delivery Guide도 새 광역 Skill이 아니다. `analyzing-and-refining-game-concepts`의 `constrain / poc-contract / production-gate`와 기존 기술·Vertical Slice·검증 책임이 `templates/planning/PC_ANDROID_DELIVERY_PROFILE.md`를 생산·검증하며, 실제 Windows build·Android 실기기·모바일 UI/입력/lifecycle·성능·계정 Gate가 없으면 `DUAL_TARGET_CONDITIONAL` 또는 `BLOCKED_UNVERIFIED`다.

게임 빌드 용량·자산 최적화 Guide도 새 광역 Skill이 아니다. 프로젝트 단계에 따라 기존 기획·아트·Vertical Slice·검증 책임이 `GAME_BUILD_SIZE_AND_ASSET_OPTIMIZATION_GUIDE.md`를 사용하고 `PC_ANDROID_DELIVERY_PROFILE.md`의 프로젝트별 실측값을 생산·검증한다. 실제 build·store-served size·Steam patch·Android device·사람 품질 증거가 없으면 해당 항목은 `NOT_RUN`, `DEVICE_NOT_RUN`, `STORE_NOT_RUN`, `HUMAN_NOT_RUN` 또는 `BLOCKED_UNVERIFIED`로 유지한다.

활성 Skill의 trigger·비사용 조건·입력·출력·실패·검증은 `skills/SKILL_REGISTRY.json`과 해당 `SKILL.md`가 책임진다. Skill 이름을 사용자에게 고르게 하거나 전체 Skill을 기본 로드하지 않는다.

작성 산출물 Template은 소유 Skill이 `templates/planning/GAME_SYSTEM_DIFFICULTY_AND_COMBAT_AI_CONTRACT.md`로 연결한다.

## 보조 라우트

| 요청 | 다음 책임 |
|---|---|
| 로컬·GitHub drift | `synchronizing-local-and-github-state` |
| 긴 작업 checkpoint·재개 | `maintaining-long-running-task-continuity` |
| 구조 단순화·동작 보존 리팩터링 | `simplifying-skill-bodies` / `refactoring-with-contract-preservation` |
| 불필요 자료 판정 | `pruning-stale-and-nonfunctional-material` |
| 게임 사용자 연구 11영역 | `governing-game-user-research-coverage` |
| 사용자 학습 자료 | `creating-user-learning-notes` |
| 프로젝트 상태·사람용 시각화 | `building-project-visual-dashboards` — repository 정본에서 생성한 `HUMAN_GDD_PDF_DERIVED_VIEW`가 기본이며 외부 HTML/Notion workspace를 새 정본으로 만들지 않음 |
| Godot·Unity 런타임 오류 | `diagnosing-game-engine-runtime-failures` |
| Godot live Editor·MCP·addon·Scene·Resource 자동화 | HiGodot persistent authoring → GUT deterministic GDScript test → Hera live QA (`LIVE_QA_AND_OBSERVABILITY_ONLY`) |

Godot 자동화는 `docs/knowledge/godot/HIGODOT_SINGLE_AUTHORITY_AND_SAFE_OPERATION.md`와 `templates/project-operations/.agents/skills/godot-live-editor-operations/SKILL.md`를 함께 읽는다. 세 도구를 모든 프로젝트에 일괄 설치하지 않으며, GUT과 Hera는 프로젝트가 실제 소비 경로를 갖춘 경우에만 선택적으로 채택한다.

전체 원문 책임 매핑은 `docs/SKILL_COVERAGE_MAP.md`, 기계 검증은 `skills/SKILL_COVERAGE.json`을 사용한다.

## 일반 프로젝트 읽기 순서

```text
프로젝트 AGENTS.md
→ 프로젝트 START_HERE.md
→ ACTIVE_CONTEXT.md·DOCUMENTATION_MAP.md·DEVELOPMENT_GATES.md
→ CURRENT_CONFIRMED_DECISIONS·AI production spec·현재 Codex handoff
→ DESIGN_DOCUMENT_REGISTRY.json·현재 책임 원본
→ ASSET_MANIFEST.json·실제 파일·자산·테스트
→ SKILL_REGISTRY.json·필요한 Skill과 mode
→ Roadmap·Issue·Plan·실행 순서
→ 실제 migration scope일 때만 legacy Notion/Google Sheets 고유 자료
```

변경 후 `DOCUMENT_UPDATE_MATRIX.md`로 영향 범위를 확인한다. 과거 Skill ID는 `skills/LEGACY_SKILL_ALIASES.md`에서 현재 Skill·mode로 해석하며, 새 문서와 Registry에는 현행 ID만 사용한다.

## Cloud Run 게임 백엔드 진입

서버 기능이 감지되면 `docs/knowledge/game-development/GAME_BACKEND_CLOUD_RUN_AND_ONLINE_SERVICES_GUIDE.md`를 읽고 `SERVER_FEATURE_DETECTED`에서 적합성 Gate를 시작한다. 선택 뒤 프로젝트 정본은 `templates/project-operations/GAME_BACKEND_SERVICE_CONTRACT.md`에 두며 실제 배포·부하·장애·비용 검증 전에는 `PRODUCTION_READY`를 선언하지 않는다.

## 게임 권한·무결성·DRM 진입

entitlement, Play Integrity, Steam DRM Wrapper, STOVE 기능, anti-tamper, offline license 또는 고가치 서버 권위 질문은 `docs/knowledge/game-development/GAME_ENTITLEMENT_INTEGRITY_AND_DRM_GUIDE.md`에서 시작한다. 프로젝트 상태는 `templates/project-operations/GAME_ENTITLEMENT_AND_INTEGRITY_RECORD.md`에 두며 platform sandbox와 사람 복구 증거 전에는 `PRODUCTION_READY`를 선언하지 않는다.
