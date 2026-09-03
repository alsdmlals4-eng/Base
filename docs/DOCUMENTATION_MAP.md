# Base 문서·스킬 역할표

Base는 게임·연재소설 등 등록 프로젝트가 공유하는 **[학습형] [공용]** 작업 원칙, Skill, Template, Test와 일반화된 Case를 관리한다. 프로젝트별 실제 구현·세계관·수치·승인 자산·런타임 상태는 프로젝트 정본과 저장소가 소유한다.

## 1. 최소 시작 경로

```text
START_HERE.md
→ AGENTS.md
→ docs/OPERATING_MODEL.md
→ docs/WORK_MODE_AND_SKILL_ROUTING.md
→ docs/DOCUMENTATION_MAP.md
→ skills/SKILL_REGISTRY.json
→ docs/generated/BASE_ACTIVE_SKILLS.md
→ 현재 작업에 필요한 최소 Skill / reference / Template / Test
→ 대상 프로젝트 Project Home + repository truth
```

`SKILL_REGISTRY.json`이 active routing machine authority이고 `BASE_ACTIVE_SKILLS.md`는 생성된 사람용 view다. Archive·백업·보류·폐기 구현은 감사나 복구 요청이 없는 한 기본 읽기 대상이 아니다.

## 2. 권한 경계

### GPT / Codex 작업 책임

```text
GPT = Base·Notion·기획·검수·문서·표·이미지·운영 인프라
Codex = 실제 게임 프로젝트의 Godot 제품 구현·GDScript·Scene·Resource·runtime/play test
CODEX_NOT_GENERAL_REPOSITORY_EXECUTOR
```

Base Python test·Registry/generated·CI contract는 코드 형식이어도 GPT governance 작업이다. Codex handoff는 `ACTUAL_GODOT_PRODUCT_IMPLEMENTATION_EXISTS`일 때만 프로젝트별로 만든다.

### Base

```text
AGENTS.md / START_HERE.md / docs/OPERATING_MODEL.md
→ 공용 운영 계약

docs/DOCUMENTATION_MAP.md
→ 책임 위치

skills/SKILL_REGISTRY.json
→ active Skill routing

GitHub Issue / PR / Actions
→ 진행 중 변경·검증 증거

Git history / archive
→ 과거 구현·복구 증거
```

### 프로젝트 — V4 repository-first 정본

```text
REPOSITORY_PRIMARY_CANON
→ current planning / decisions / Markdown / JSON / game data / code / scene / resource / config / tests / evidence
→ REPOSITORY_RUNTIME_TRUTH

APPROVED_HUMAN_BLUEPRINT_PDF_CANON
→ exact repository SHA와 evidence ceiling이 연결된 사람이 보는 milestone snapshot

NOTION_LEGACY_READ_ONLY_MIGRATION_SOURCE
→ unique legacy material 발견·이관에만 사용
→ 새 기본 workspace, active decision sync, runtime handoff 정본이 아님
```

현재 machine authority는 `docs/operations/PROJECT_WORKSPACE_AUTHORITY_CONTRACT_V4.json`의 `DESKTOP_GPT_REPOSITORY_FIRST_WORKSPACE`다. 사람용 PDF는 파생본이며 repository를 대체하지 않는다.

`DOMAIN_SPLIT_CANON`, `NOTION_HUMAN_FACING_CANON`, `PROJECT_RELATION_REQUIRED`는 V3 compatibility/history와 실제 legacy migration에서만 해석한다. V3 계약은 새 작업의 active route가 아니며 V4 예외를 통과한 프로젝트만 한정된 Notion surface를 별도 owner·scope·exit 조건과 함께 둘 수 있다.

Google Sheets는 `GOOGLE_SHEETS_MIGRATION_ONLY_UNTIL_REMOVAL` source다. Figma·Figma Bridge·Expression/Sprite Studio·external HTML workspace·project-management Tool Hub·QA Evidence Studio는 active/default authority가 아니다. 상세 retirement는 `docs/DEPRECATED_PROJECT_SURFACE_RETIREMENT_POLICY.md`가 소유한다.

## 3. 현재 공용 책임 원본

| 구분 | 책임 원본 | 책임 |
|---|---|---|
| 최초 라우터 | `START_HERE.md` | 최소 cold-start 경로와 요청 유형 라우팅 |
| 항상 적용 규칙 | `AGENTS.md` | 권한·승인·환경·비용·검증·보호·완료 불변 규칙 |
| 통합 운영 모델 | `docs/OPERATING_MODEL.md` | 생명주기·정본·상태·발행·근거·검증 |
| Work Mode / Skill | `docs/WORK_MODE_AND_SKILL_ROUTING.md` | PLAN/BUILD/REVIEW와 Skill 자동 라우팅 |
| 장기 작업 | `docs/LONG_HORIZON_WORK_EXECUTION_POLICY.md` | 현행조사→>=3 대안→creative benchmark frontier→최소 5회 전체 적대적 개선→5회 이후 오류·충돌·누락·blocker 0까지 추가 전체 루프→장기 최선안 |
| 프로젝트 workspace machine authority | `docs/operations/PROJECT_WORKSPACE_AUTHORITY_CONTRACT_V4.json` | `DESKTOP_GPT_REPOSITORY_FIRST_WORKSPACE`, `REPOSITORY_PRIMARY_CANON`, derived human PDF, legacy-only Notion migration boundary |
| 시각 협업 | `docs/DESKTOP_GPT_REPOSITORY_FIRST_WORKSPACE_POLICY.md`, `docs/VISUAL_COLLABORATION_TOOL_POLICY.md` | repository-owned visual canon·manifest·exact-SHA PDF review가 현행 owner; 뒤의 정책은 V3 compatibility/history terminology·migration reference이며 V4 기본 작업면을 되살리지 않음 |
| Notion asset/flow workflow | `docs/knowledge/game-development/NOTION_VISUAL_ASSET_AND_FLOW_WORKFLOW.md` | `V3_COMPATIBILITY_AND_HISTORY_ONLY`; legacy provenance/migration reference, active default 아님 |
| 폐기 작업면 | `docs/DEPRECATED_PROJECT_SURFACE_RETIREMENT_POLICY.md` | Figma/HTML/Sheets/Tool Hub/QA Studio/local management surface의 unique 흡수→active route 제거 |
| Google Sheets migration compatibility | `docs/PROJECT_GDD_GOOGLE_SHEETS_POLICY.md` | `MIGRATION_ONLY_UNTIL_REMOVAL`, unique/duplicate/obsolete migration, destination readback |
| 이미지 생성·검수 | `docs/GPT_IMAGE_GENERATION_AND_REVIEW_POLICY.md` | Visual Requirement Gate, candidate QA, 명시적 approval/promotion |
| Art requirement | `docs/knowledge/game-development/ART_DIRECTION_AND_ASSET_PLANNING_GUIDE.md` | Visual Requirement Gate, Delete Test, priority/disposition |
| Preferred visual references | `docs/knowledge/game-development/PREFERRED_VISUAL_STYLE_REFERENCE_LIBRARY.md` | reference-only style families; project Art Canon과 분리 |
| Pixel art system | `docs/knowledge/game-development/PIXEL_ART_STYLE_SYSTEM.md` | 재현 가능한 스타일 축·preset·검토 원칙 |
| Pixel visual reference gallery | `docs/knowledge/game-development/PIXEL_ART_VISUAL_REFERENCE_GALLERY.md` | `REFERENCE_ONLY` pixel preset image examples, provenance, license, observation data |
| UI/UX 설계·폴리싱·감사 | `skills/auditing-and-refining-ui-art/SKILL.md` | `auditing-and-refining-ui-art`가 UI 설계·폴리싱·실제 화면 감사를 소유하고 `ui-motion-and-interaction-principles.md`를 조건부 reference로 사용 |
| AI instruction/context | `docs/knowledge/ai/AI_INSTRUCTION_AND_CONTEXT_DESIGN_METHOD.md` | instruction authority·context curation·example/fixture·HARD_CONSTRAINT 설계 |
| AI model/prompt cost | `skills/optimizing-ai-model-and-prompt-costs/SKILL.md` | `optimizing-ai-model-and-prompt-costs`가 model recommendation·effort routing·prompt caching·provider/cost boundary를 소유 |
| 게임 시스템·난이도·전투 AI | `skills/analyzing-and-refining-game-concepts/SKILL.md`, `docs/knowledge/game-development/GAME_SYSTEM_DIFFICULTY_AND_COMBAT_AI_CONTRACT.md` | `system-design` / `difficulty-and-combat-ai` mode, 난이도 장벽·공정성·attack/threat budget |
| creative benchmark / reuse | `docs/knowledge/research/REVERSE_ENGINEERING_REUSE_PIPELINE.md`, `docs/knowledge/game-development/reuse/REUSABLE_MODULE_REGISTRY.md` | multi-source 원리 추출, originality/fun/creativity hypothesis, module contract와 project-specific synthesis |
| 게임 개발 knowledge hub | `docs/knowledge/game-development/README.md` | 기획·아트·개발·AI·research·release Guide routing |
| 게임 개발 Evidence Pack | `templates/research/GAME_DEVELOPMENT_EVIDENCE_PACK.md` | 외부 근거·범위·검증 상태의 공용 조사 packet |
| Game Development Case Card | `templates/research/GAME_DEVELOPMENT_CASE_CARD.md` | 게임 개발 사례의 context·transferable principle·failure condition·evidence 기록 |
| Reference Case Card | `templates/research/REFERENCE_CASE_CARD.md` | 범용 사례의 source·context·적용 한계 기록 |
| 플랫폼/권리/독립 제작 | `docs/knowledge/game-development/PLATFORM_REVIEW_ASSET_RIGHTS_AND_REFERENCE_PRODUCTION_GUIDE.md` | Steam/STOVE/Google Play, commercial/distribution rights, reference→independent production |
| PC/Android delivery | `docs/knowledge/game-development/PC_ANDROID_CROSS_PLATFORM_DELIVERY_GUIDE.md`, `templates/planning/PC_ANDROID_DELIVERY_PROFILE.md` | shared core + platform adapter + staged rollout |
| 게임 build size·asset optimization | `docs/knowledge/game-development/GAME_BUILD_SIZE_AND_ASSET_OPTIMIZATION_GUIDE.md` | build/package/download/install/patch 실측, font/texture/audio 품질 등급, store delivery evidence |
| Cloud Run / online backend | `docs/knowledge/game-development/GAME_BACKEND_CLOUD_RUN_AND_ONLINE_SERVICES_GUIDE.md` | backend capability, Cloud Run/online service boundary, cost/security/runtime evidence |
| Entitlement / DRM integrity | `docs/knowledge/game-development/GAME_ENTITLEMENT_INTEGRITY_AND_DRM_GUIDE.md` | entitlement integrity, DRM/trust boundary, platform/runtime verification |
| Godot author/test/live QA | `docs/knowledge/godot/HIGODOT_SINGLE_AUTHORITY_AND_SAFE_OPERATION.md` | `HiGodot` = authoring authority, `GUT` = test framework, `Hera` = restricted live QA; second writer 금지 |
| Local Godot reference | `docs/knowledge/godot/LOCAL_GODOT_REFERENCE_LIBRARY.md` | local reference-only shelf; missing path is non-blocking |
| repository-native evidence | `docs/DEPRECATED_PROJECT_SURFACE_RETIREMENT_POLICY.md`, `docs/knowledge/game-development/reuse/PRODUCTION_TOOL_WORKFLOW_MODULES.md` | `REPOSITORY_NATIVE_EVIDENCE_CAPTURE`: existing test/runtime/log/screenshot/CI evidence를 exact build identity에 결합 |
| CI execution/cost | `docs/CI_EXECUTION_COST_POLICY.md` | change-class validation, runner/cost gate |
| PowerShell user execution | `docs/operations/POWERSHELL_FRESH_SHELL_EXECUTION_CONTRACT.md` | fresh shell, location first, one paste block, fail-fast, direct Codex/Loop route |
| GitHub governance | `docs/GITHUB_PRO_OPERATING_POLICY.md`, `docs/GITHUB_WORK_ITEM_LIFECYCLE_POLICY.md` | GitHub Pro 저장소 운영, GitHub Pro 보호·Ruleset·자동 병합, PR/check/work-item lifecycle |
| Decision sync | `docs/CONFIRMED_DECISION_SYNC_POLICY.md` | approved Decision 정본화·중복질문 방지·Notion/repository cross-sync |
| Planning sequence/evidence | `docs/PLANNING_SEQUENCE_AND_EVIDENCE_POLICY.md` | evidence, approval bundle, `PROJECT_VISUALIZATION_NEED_MAP`, Demo-First |
| 선택형 2산출물 Master GDD | `docs/PROJECT_MASTER_GDD_TWO_ARTIFACT_POLICY.md`, `templates/project-operations/GPT_WORK_PROJECT_MASTER_GDD_TWO_ARTIFACT_INSTRUCTION.md` | `HUMAN_GAME_BLUEPRINT_GDD_LAYERED_PROFILE`을 PDF + AI Markdown 내부에 구성하며 `NO_SEPARATE_BLUEPRINT_ARTIFACT` 유지 |
| Integrated vertical slice | `templates/prompts/VERTICAL_SLICE_INTEGRATED_EXECUTION_PROMPT_v9.md` | active integrated single-attachment execution route |
| Capability composition | `docs/CAPABILITY_COMPOSITION_MAP.md` | capability 조합·금지 경계·필수 증거 |
| Project local Asset Vault | `docs/PROJECT_LOCAL_ASSET_VAULT_POLICY.md`, `tools/project_asset_vault.py` | local candidate preservation, explicit promotion, tombstone |
| Active Skill machine source | `skills/SKILL_REGISTRY.json` | trigger/status/path/mode routing |
| Active Skill generated view | `docs/generated/BASE_ACTIVE_SKILLS.md` | Registry-derived human discovery surface |
| Legacy Skill alias | `skills/LEGACY_SKILL_ALIASES.md` | historical Skill ID → current Skill/mode |
| Skill learning | `skills/SKILL_LEARNING_LOG.md` | failure·decision·verification·promotion history |
| Skill behavior eval | `skills/SKILL_BEHAVIOR_EVALS.json` | prompt routing expected/forbidden behavior |
| Local validation | `tools/run_local_validation.py` | full regression and exact trusted-main validation entrypoint |
| Base proposal registry | `[수정제안서]/PROPOSAL_REGISTRY.json` | project-derived shared change proposal lifecycle |
| Controlled vocabulary | `docs/CONTROLLED_VOCABULARY.md` | **공용 용어**와 bounded-context 정의 |
| Archived cross-project UI handoff | `docs/archive/handoffs/2026-07-29-ux-ui-common-system-expansion.md` | `COMPATIBILITY_ONLY`; historical handoff이며 active implementation authority 없음 |

기존 GitHub Pro 상세 프로필·예산 라우팅은 `GITHUB_REPOSITORY_GOVERNANCE_PROFILE.md`와 `GITHUB_USAGE_BUDGET.md` 이름으로도 계속 발견 가능해야 한다.

Skill 수 자체는 목표·완료조건·경고 임계값이 아니다. 책임 중복·trigger 충돌·사용되지 않는 mode·과도한 컨텍스트 비용처럼 **실제 구조 문제**가 있을 때 consolidation 또는 새 Skill 필요성을 판단한다.

## 4. Legacy Notion migration reference

이 절의 V3 Notion IA·record·flow 예시는 이미 존재하는 legacy workspace를 읽고 고유 자료를 repository로 이관할 때만 참고한다. 새 프로젝트 또는 새 project work의 기본 진입점은 `docs/DESKTOP_GPT_REPOSITORY_FIRST_WORKSPACE_POLICY.md`와 `docs/operations/PROJECT_WORKSPACE_AUTHORITY_CONTRACT_V4.json`이다. V3 내용을 신규 Notion workspace·active decision sync·Codex handoff의 기본 계약으로 복원하지 않는다.

```text
L0 · PROJECT_HUB
→ 프로젝트 선택

L1 · HUMAN_PROJECT_HOME
→ 전체 게임/작품 Flow
→ 핵심 시스템 + 필요한 설정/플레이어 역할
→ 프로젝트 고유 핵심 데이터 표
→ UX/UI/Visual + 승인 anchor
→ AI가 이해한 핵심 + 내가 수정하는 방법
→ 구현/검증 상태·blocker·다음 작업
→ 4~6개 L2 Domain drilldown

L2 · DOMAIN_WORKSPACE
→ 프로젝트 의미에 맞춘 책임 그룹
→ 빈 폴더 금지
→ current authority/상태/결정/위험 + L3 owner/view

L3 · DETAIL_OR_RECORD
→ Visual/Story Bible, Flow/Storyboard, Asset, Reference, Production, Core System, 대표 Encounter, confirmed table, DB record/view 등 실제 상세 owner
```

`SHALLOW_BY_DEFAULT`: 일반 navigation은 L3에서 끝낸다. L4+ 일반 page nesting은 `L4_EXCEPTION_REVIEW_REQUIRED`이며 DB Record/Relation/linked view/toggle/section으로 해결할 수 없는 실제 owner 분리가 필요할 때만 예외로 둔다.

`FULL_GAME_FLOW_VISIBLE_ON_HOME`, `CORE_SYSTEMS_AND_SETTING_VISIBLE_ON_HOME`, `PROJECT_SPECIFIC_CORE_DATA_TABLES_VISIBLE_ON_HOME`, `HOME_DETAIL_LINKS_CANNOT_REPLACE_CORE_UNDERSTANDING`은 구조 단순화보다 우선한다. Home을 짧게 만들기 위해 전체 Flow·핵심 시스템/설정·핵심 데이터 표를 하위 페이지로 밀어내지 않는다.

### 4.1 게임 프로젝트 Domain starting pattern

고정 taxonomy가 아니라 starting pattern이다. 필요하지 않은 Domain은 만들지 않고 프로젝트 의미가 겹치면 합친다.

```text
PROJECT HOME
├ Direction · Planning
├ Design · Canon · Data
├ Visual · UX · Assets
├ Production · Validation
├ Reference · Benchmark
└ optional Content · World
```

Tetris처럼 전투 구조가 핵심이면 `Combat Design · Data`, TEN_PACES라면 `Combat · Martial Arts · Route`, Blacksmith라면 `Enhancement · Durability · Economy`처럼 프로젝트 고유 언어를 사용한다. 4~6개 L2 Domain을 권장한다.

기존 문서 책임은 사라지지 않는다. 다음은 적절한 L2 아래 L3 owner로 이동할 수 있다.

```text
프로젝트 전체 작업계획
Visual/Story Bible
UI·게임플레이 Flow / Storyboard
Asset Library
Reference · Benchmark
Production · Handoff
Core System detail
대표 Encounter / First Run / World content
프로젝트 고유 예산·Tier·로스터·경제·성장표
```

### 4.2 Coc-Fiction / 서사 프로젝트 Domain starting pattern

```text
COC-Fiction Home
├ Direction · Planning
├ Story · Canon · Events
├ Characters · Factions · World
├ Visual · Storyboard · Assets
├ Production · Continuity · Validation
└ Reference · Benchmark
```

서사 프로젝트는 게임 UI Flow를 억지로 사용하지 않는다. `CANON / CHARACTER / FACTION / SCENE / CLUE / LOCATION / REFERENCE / BENCHMARK` record를 Project-filtered view로 분리한다. Home에는 Part/story 상위 Flow, 핵심 인물·세력·관계·사건/세계 규칙의 대표 데이터가 직접 보여야 한다.

### 4.3 Work Master

사람 view: 작업, 상태, 영역, 우선순위, 시작/종료, 완료 기준, 검증/증거, 담당자.

System metadata: Task ID, Project relation, implementation evidence locator 등.

### 4.4 Asset & Knowledge Master

게임 기본 `Record Type`:

```text
ASSET
COMPONENT
SCREEN
REFERENCE
BENCHMARK
```

서사 확장 `Record Type`:

```text
CANON
CHARACTER
FACTION
SCENE
CLUE
LOCATION
```

Human Gallery: Preview, Name, Usage, Style, Approved, Reuse처럼 현재 판단에 필요한 최소 정보.

AI/System view: Project, Asset ID, Version, Status, Category, Prompt, AI Note, Source, Rights / License, Hash, Implementation Path, Decision 등.

Benchmark Decision:

```text
ADOPT / ADAPT / TEST / REFERENCE_ONLY / AVOID / IGNORE
```

### 4.5 Visual Map / Storyboard

`VISUAL_MAP_DERIVED`는 structured Screen/relationship records에서 생성될 수 있다는 뜻이다. **승인된 Notion Map/Storyboard는 사람이 보는 시각 기획의 우선 표현**이다. Game은 screen/navigation/system flow를, narrative project는 canon/character/faction/clue/scene/continuity 관계를 표현한다. 시각 편집이 구조화 의미를 바꾸면 repository record를 동기화하고, runtime 변경이 생기면 Notion 표현을 다시 갱신한다.

### 4.6 사람용 확정표

예산표·Tier표·로스터표·경제표·성장표처럼 사람이 비교하고 직접 수정하기 쉬운 표현은 Notion을 기본 위치로 둔다. Home에는 **핵심 대표 표/관계**를 직접 보여주고 전체 raw table은 적절한 L3 owner/linked view에 둔다.

```text
CONFIRMED HUMAN TABLE
→ Project
→ Decision ID / canonical repository path
→ CONFIRMED / PROVISIONAL / DEFERRED / REJECTED 구분
→ source main SHA 또는 freshness locator
→ Notion last sync
```

표 자체가 machine data를 중복 소유하지 않는다. machine-consumed JSON·game data는 repository에 두고, Notion에서 의미가 바뀌면 repository에 동기화한 뒤 구현한다.

## 5. 이미지·시각 checkpoint

`Intermediate visual checkpoint`는 특정 product page가 아니라 **현재 Project relation 안에서의 중간 시각 의사결정 Gate**다.

- `MISSING_CANON`: 비교할 승인 시각 기준이 부족함.
- `DRAFT_VISUAL`: 탐색/검토용이며 project asset approval이 아님.
- `PROJECT_ASSET_APPROVED`: 명시적 project approval을 획득한 자산 상태.
- `APPLIED_AND_RUNTIME_VERIFIED`: repository/runtime 적용과 별도 증거가 확인된 상태.

Context token은 필요할 때 `GDD`, `EXTERNAL_COLLABORATION`, `BOTH`를 유지할 수 있으나, 세 context 모두 Notion Project relation과 repository truth를 우회하지 않는다.

```text
generate / edit
→ Project target
→ candidate
→ readback
→ review / approval
→ version / replacement
→ repository implementation
→ REPOSITORY_NATIVE_EVIDENCE_CAPTURE
```

## 6. Legacy·compatibility·폐기

### Google Sheets

기존 unique material이 남아 있을 때만 `MIGRATION_ONLY_UNTIL_REMOVAL`. 상세 migration contract는 `docs/PROJECT_GDD_GOOGLE_SHEETS_POLICY.md`가 소유한다. migration은 unique / duplicate / obsolete를 분류하고, 올바른 Project destination에 옮긴 뒤 readback한다. 완료 후 active reference에서 제거한다.

### 폐기된 프로젝트 작업면

다음은 active/default execution surface가 아니다.

- Figma / dedicated Figma Bridge / project Figma target-workspace registries
- external HTML workspace / catalog / dashboard
- localhost Expression Studio
- localhost Sprite Animation Studio
- project-management / visual-delivery Tool Hub
- QA Evidence Studio
- Google Sheets after unique migration

재사용할 가치는 구현 자체가 아니라 current Notion/repository/PowerShell/Loop owner에 흡수된 project identity, provenance, bounded identity-preserving edits, approval, version/replacement, reuse classification, Screen/Flow ID, readback, evidence ceiling, explicit runtime handoff다.

Git history가 복구 기록이다. historical plan/spec/learning entry는 current authority가 아니며, 새 workflow가 그것을 참조할 필요는 없다.

### `REPOSITORY_NATIVE_EVIDENCE_CAPTURE`

별도 QA GUI/app을 기본 경로로 사용하지 않는다.

```text
project/build identity
→ acceptance contract
→ tests / GUT / Godot·Hera runtime / logs / screenshot·video / CI artifact
→ exact commit/PR identity
→ optional exact-SHA derived PDF or V4 exception/migration link
→ PASS | FAIL | BLOCKED | NOT_RUN + evidence ceiling
```

## 7. 프로젝트 정본과 발행

도메인별 active canonical owner는 하나만 둔다.

```text
사람용 전체 그림 / Visual / 예산·Tier·비교표 / Flow·Wireframe / Markdown / JSON / game data / code / scene / resource / test
→ REPOSITORY_PRIMARY_CANON

사람용 milestone 검토
→ APPROVED_HUMAN_BLUEPRINT_PDF_CANON (exact source SHA)

실제 V4 exception 또는 legacy migration source
→ NOTION_LEGACY_READ_ONLY_MIGRATION_SOURCE

실제 구현·runtime 상태
→ REPOSITORY_RUNTIME_TRUTH
```

승인 결정 복원 경로는 다음을 유지한다.

```text
GitHub 추적 근거
→ CURRENT_CONFIRMED_DECISIONS.md
→ 분야 책임 원본 / structured data
→ 필요한 exact-SHA derived PDF 또는 실제 exception/migration readback
```

`DESIGN_DOCUMENT_REGISTRY.json`은 registered Markdown/JSON owner와 publication 경로를 관리한다. PDF/DOCX/dashboard는 선언된 publication/derived surface일 뿐 독립 canon이 아니다.

## 8. 검증

실행하지 않은 항목을 PASS로 보고하지 않는다.

```text
contract/diff review
→ static/format/schema
→ focused tests
→ runtime/build/render when available
→ regression
→ exact-head PR checks
→ merge
→ postmerge main + Notion readback
```

Notion page·image upload 성공은 Godot runtime proof가 아니다. Upload/attach 작업은 destination readback을 해야 완료로 보고할 수 있다.

## 9. 현재 비용 경계

```text
ZERO_INCREMENTAL_COST_REQUIRED
CURRENT_PAID_PLANS: GPT_PRO
PAID_PLAN_COUNT: 1
```

Notion은 Free 범위에서 사용한다. paid Notion AI, separately metered API/storage/automation, 신규 유료 SaaS/runner/compute는 새 사용자 승인 없이는 기본 경로에 넣지 않는다.

## 10. 기존 공용 라우팅 발견성 보존

Notion 전환은 기존 Base의 공용 능력을 삭제하거나 숨기는 작업이 아니다. 아래 라우팅 표현은 계속 발견 가능해야 한다.

- **공용 용어**: `docs/CONTROLLED_VOCABULARY.md`에서 stable term과 bounded-context 의미를 찾는다.
- 승인 Decision 복원: `→ CURRENT_CONFIRMED_DECISIONS.md`를 거쳐 분야 정본과 사람용 Notion 표현을 교차검증한다.
- 저장소 전체 감사: `repository-wide-audit`는 별도 신규 Skill이 아니라 기존 REVIEW/검증 능력의 통합 mode로 라우팅한다.
- 프로젝트 설치 템플릿: **프로젝트 설치 템플릿을 활성 상태 문서로 오인하지 않는다**. Template은 소비될 때만 프로젝트 상태가 된다.
- Codex handoff: **GPT→Codex 단계별 Godot 구현 인계**는 기존 `implementation-package-handoff` mode를 사용하며, `USER_REQUESTED_CODEX_HANDOFF`가 있을 때만 생성한다. 계획/검토 작업은 자동으로 Codex 구현 승인이 되지 않는다.
- Codex preflight: `CODEX_PREFLIGHT_OPTIONAL`; 명시적 handoff가 없으면 계획/검토 단계에서 별도 구현 preflight를 강제하지 않는다.
- GitHub governance: **GitHub Pro 저장소 운영**과 **GitHub Pro 보호·Ruleset·자동 병합**은 기존 GitHub governance owner로 라우팅하며 `GITHUB_REPOSITORY_GOVERNANCE_PROFILE.md`, `GITHUB_USAGE_BUDGET.md`를 호환 발견 경로로 유지한다.
- 기획 인터뷰: **Grill Me 핵심 의사결정 인터뷰**는 `clarify` + `references/grill-me-protocol.md`로 라우팅하고 `docs/PLANNING_FIRST_GRILL_ME_BATCH_POLICY.md`의 승인 배치 정책을 함께 적용한다.
- 연재소설: `developing-and-revising-serial-fiction`이 서사 개발·수정의 active owner이며 Coc-Fiction Notion Storyboard/Character/Faction 표면과 조합한다.

<!-- FEDERATED_DUAL_CANON_ROUTE -->

> V4 authority route: `FEDERATED_DUAL_CANON_SINGLE_FACT_OWNER`. `REPOSITORY_EXECUTION_DATA_CANON` owns editable structured, execution, runtime, work-status, and evidence facts. Only a `USER_APPROVED_AND_MANIFEST_REGISTERED` `APPROVED_HUMAN_BLUEPRINT_PDF_CANON` owns the immutable human visual/review baseline. `ONE_EDITABLE_OWNER_PER_ATOMIC_FACT`; `CANDIDATE_PDF_NOT_CANON` and PDF annotations do not mutate repository-owned facts. See `docs/operations/PROJECT_WORKSPACE_AUTHORITY_CONTRACT_V4.json` and `docs/DESKTOP_GPT_REPOSITORY_FIRST_WORKSPACE_POLICY.md`.
