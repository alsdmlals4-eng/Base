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
→ 대상 프로젝트 Project page + repository truth
```

`SKILL_REGISTRY.json`이 active routing machine authority이고 `BASE_ACTIVE_SKILLS.md`는 생성된 사람용 view다. Archive·백업·보류·폐기 구현은 감사나 복구 요청이 없는 한 기본 읽기 대상이 아니다.

## 2. 권한 경계

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

### 프로젝트

```text
NOTION_DEFAULT_PROJECT_WORKSPACE
→ Project Registry
→ Project-filtered Work / Asset / Visual Map

repository-native structured source
→ code / data / scene / resource / config / tracked implementation asset / tests
→ REPOSITORY_RUNTIME_TRUTH
```

`PROJECT_RELATION_REQUIRED`: project-scoped Work, Asset, Component, Screen, Reference, Benchmark record는 Project relation 없이 프로젝트 정본이 될 수 없다.

Google Sheets는 `COMPATIBILITY_ONLY` migration source다. Figma·Figma Bridge·Expression/Sprite Studio·visual Tool Hub는 active authority가 아니다.

## 3. 현재 공용 책임 원본

| 구분 | 책임 원본 | 책임 |
|---|---|---|
| 최초 라우터 | `START_HERE.md` | 최소 cold-start 경로와 요청 유형 라우팅 |
| 항상 적용 규칙 | `AGENTS.md` | 권한·승인·환경·비용·검증·보호·완료 불변 규칙 |
| 통합 운영 모델 | `docs/OPERATING_MODEL.md` | 생명주기·정본·상태·발행·근거·검증 |
| Work Mode / Skill | `docs/WORK_MODE_AND_SKILL_ROUTING.md` | PLAN/BUILD/REVIEW와 Skill 자동 라우팅 |
| 장기 작업 | `docs/LONG_HORIZON_WORK_EXECUTION_POLICY.md` | 현행조사→>=3 대안→벤치마킹→5회 전체 적대적 개선→장기 최선안 |
| 프로젝트 workspace machine authority | `docs/operations/PROJECT_WORKSPACE_AUTHORITY_CONTRACT.json` | `NOTION_DEFAULT_PROJECT_WORKSPACE`, `PROJECT_RELATION_REQUIRED`, `WORK_MASTER`, `ASSET_KNOWLEDGE_MASTER`, `VISUAL_MAP_DERIVED`, `REPOSITORY_RUNTIME_TRUTH` |
| 시각 협업 | `docs/VISUAL_COLLABORATION_TOOL_POLICY.md` | project-filtered human/AI view, Visual Map 파생 권위, runtime handoff |
| Notion asset/flow workflow | `docs/knowledge/game-development/NOTION_VISUAL_ASSET_AND_FLOW_WORKFLOW.md` | provenance·bounded edit·approval·version·reuse·benchmark·readback·handoff |
| Google Sheets migration compatibility | `docs/PROJECT_GDD_GOOGLE_SHEETS_POLICY.md` | `COMPATIBILITY_ONLY`, unique/duplicate/obsolete migration, destination readback |
| 이미지 생성·검수 | `docs/GPT_IMAGE_GENERATION_AND_REVIEW_POLICY.md` | Visual Requirement Gate, candidate QA, 명시적 approval/promotion |
| Art requirement | `docs/knowledge/game-development/ART_DIRECTION_AND_ASSET_PLANNING_GUIDE.md` | Visual Requirement Gate, Delete Test, priority/disposition |
| Preferred visual references | `docs/knowledge/game-development/PREFERRED_VISUAL_STYLE_REFERENCE_LIBRARY.md` | reference-only style families; project Art Canon과 분리 |
| Pixel art system | `docs/knowledge/game-development/PIXEL_ART_STYLE_SYSTEM.md` | 재현 가능한 스타일 축·preset·검토 원칙 |
| 게임 개발 knowledge hub | `docs/knowledge/game-development/README.md` | 기획·아트·개발·AI·research·release Guide routing |
| 플랫폼/권리/독립 제작 | `docs/knowledge/game-development/PLATFORM_REVIEW_ASSET_RIGHTS_AND_REFERENCE_PRODUCTION_GUIDE.md` | Steam/STOVE/Google Play, commercial/distribution rights, reference→independent production |
| PC/Android delivery | `docs/knowledge/game-development/PC_ANDROID_CROSS_PLATFORM_DELIVERY_GUIDE.md` | shared core + platform adapter + staged rollout |
| Godot authority | `docs/knowledge/godot/HIGODOT_SINGLE_AUTHORITY_AND_SAFE_OPERATION.md` | Existing Solution First, persistent authoring boundary, GUT/Hera 공존 |
| Local Godot reference | `docs/knowledge/godot/LOCAL_GODOT_REFERENCE_LIBRARY.md` | local reference-only shelf; missing path is non-blocking |
| CI execution/cost | `docs/CI_EXECUTION_COST_POLICY.md` | change-class validation, runner/cost gate |
| PowerShell user execution | `docs/operations/POWERSHELL_FRESH_SHELL_EXECUTION_CONTRACT.md` | fresh shell, location first, one paste block, fail-fast |
| GitHub governance | `docs/GITHUB_PRO_OPERATING_POLICY.md`, `docs/GITHUB_WORK_ITEM_LIFECYCLE_POLICY.md` | PR/check/work-item lifecycle |
| Decision sync | `docs/CONFIRMED_DECISION_SYNC_POLICY.md` | approved Decision 정본화·중복질문 방지 |
| Planning sequence/evidence | `docs/PLANNING_SEQUENCE_AND_EVIDENCE_POLICY.md` | evidence, approval bundle, Demo-First |
| Integrated vertical slice | `templates/prompts/VERTICAL_SLICE_INTEGRATED_EXECUTION_PROMPT_v9.md` | active integrated single-attachment execution route |
| Capability composition | `docs/CAPABILITY_COMPOSITION_MAP.md` | capability 조합·금지 경계·필수 증거 |
| Project local Asset Vault | `docs/PROJECT_LOCAL_ASSET_VAULT_POLICY.md`, `tools/project_asset_vault.py` | local candidate preservation, explicit promotion, tombstone |
| QA runtime evidence | `tools/qa-evidence-studio/README.md` | developer-owned PC runtime evidence; Android `DEFERRED_NOT_CONNECTED` |
| Active Skill machine source | `skills/SKILL_REGISTRY.json` | trigger/status/path/mode routing |
| Active Skill generated view | `docs/generated/BASE_ACTIVE_SKILLS.md` | Registry-derived human discovery surface |
| Legacy Skill alias | `skills/LEGACY_SKILL_ALIASES.md` | historical Skill ID → current Skill/mode |
| Skill learning | `skills/SKILL_LEARNING_LOG.md` | failure·decision·verification·promotion history |
| Skill behavior eval | `skills/SKILL_BEHAVIOR_EVALS.json` | prompt routing expected/forbidden behavior |
| Local validation | `tools/run_local_validation.py` | full regression and exact trusted-main validation entrypoint |
| Base proposal registry | `[수정제안서]/PROPOSAL_REGISTRY.json` | project-derived shared change proposal lifecycle |
| Controlled vocabulary | `docs/CONTROLLED_VOCABULARY.md` | cross-domain stable terms and bounded-context definitions |

## 4. 프로젝트 Notion 표준

```text
00 · PROJECT HUB
→ PROJECT REGISTRY · Master

project page
  PROJECT BOUNDARY

  01 · PROJECT CONTROL
  → WORK_MASTER filtered by Project

  [large visual gap]

  02 · ASSET / LIBRARY / BENCHMARK
  → ASSET_KNOWLEDGE_MASTER filtered by Project

  [large visual gap]

  03 · VISUAL MAP
  → semantic Mermaid / Screen relationships
  → approved project visual Gallery

90 · SYSTEM MASTERS
→ unfiltered registry / work / asset masters
```

### Work Master

사람 view: 작업, 상태, 영역, 우선순위, 시작/종료, 완료 기준, 검증/증거, 담당자.

System metadata: Task ID, Project relation, implementation evidence locator 등.

### Asset & Knowledge Master

`Record Type`:

```text
ASSET
COMPONENT
SCREEN
REFERENCE
BENCHMARK
```

Human Gallery: Preview, Name, Usage, Style, Approved, Reuse.

AI/System view: Project, Asset ID, Version, Status, Category, Prompt, AI Note, Source, Rights / License, Hash, Implementation Path, Decision.

Benchmark Decision:

```text
ADOPT / ADAPT / TEST / REFERENCE_ONLY / AVOID / IGNORE
```

### Visual Map

`VISUAL_MAP_DERIVED`는 사람용 파생 표현이다. Game은 screen/navigation/system flow를, narrative project는 canon/character/clue/scene/continuity 관계를 표현할 수 있다. semantic record와 그림이 충돌하면 그림을 재생성·수정한다.

## 5. 이미지·시각 checkpoint

`Intermediate visual checkpoint`는 특정 Figma page가 아니라 **현재 Project relation 안에서의 중간 시각 의사결정 Gate**다.

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
→ runtime QA
```

## 6. Legacy·compatibility·폐기

### Google Sheets

기존 unique material이 남아 있을 때만 `COMPATIBILITY_ONLY`. migration은 unique / duplicate / obsolete를 분류하고, 올바른 Project destination에 옮긴 뒤 readback한다.

### Figma / local visual-delivery tools

다음 active execution surfaces는 폐기됨:

- Figma Bridge
- Project Figma target/workspace/tool-route registries
- Expression Studio
- Sprite Animation Studio
- visual-delivery Tool Hub
- Figma-only templates/workflows/tests

재사용할 가치는 구현이 아니라 `NOTION_VISUAL_ASSET_AND_FLOW_WORKFLOW.md`에 흡수된 project identity, provenance, bounded identity-preserving edits, approval, version/replacement, reuse classification, Screen/Flow ID, readback, explicit runtime handoff다.

Git history가 복구 기록이다. historical plan/spec/learning entry는 current authority가 아니며, 새 workflow가 그것을 참조할 필요는 없다.

### QA Evidence Studio

QA Evidence Studio는 위 폐기 범위에 포함되지 않는다. 실제 PC build에 배치된 UI/asset의 developer-owned evidence를 기록하는 독립 runtime QA 도구다.

## 7. 프로젝트 정본과 발행

한 질문에는 active canonical owner 하나만 둔다. Notion은 planning/catalog/visual collaboration surface이고 repository는 runtime truth를 소유한다.

```text
DESIGN_DOCUMENT_REGISTRY.json
→ registered Markdown/JSON owner
→ code/data/asset/test consumers
```

PDF/DOCX/dashboard는 선언된 publication/derived surface일 뿐 독립 canon이 아니다.

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
