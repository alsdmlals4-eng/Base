# Shallow Notion Project Information Architecture Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reorganize project Notion navigation into `Project Hub → rich Human Home → 4~6 project-specific Domain workspaces → Detail/Record`, while preserving the full game/story flow, core systems and setting, and project-specific core data tables directly on every Human Home.

**Architecture:** Reuse the existing Human Home and Notion project-isolation owners. Add shallow-navigation rules to the current contracts instead of creating a new broad Skill, pilot the migration on Tetris, then roll the verified pattern across the remaining projects with per-project inventory and rollback-safe page moves.

**Tech Stack:** Markdown/JSON Base policy, Python `unittest`, GitHub Actions, Notion pages/databases/linked views, Notion page move/reparent, GitHub PR/CI.

**Spec:** `docs/superpowers/specs/2026-08-24-notion-shallow-project-information-architecture-design.md`

## Global Constraints

- Baseline Base main: `3f02864b5cd04537e1c6d14d0f3bc6a65fc898a6`.
- Navigation model: `L0 PROJECT_HUB → L1 HUMAN_PROJECT_HOME → L2 DOMAIN_WORKSPACE → L3 DETAIL_OR_RECORD`.
- `L4+ NORMAL_PAGE_NESTING = AVOID`; use an L3 database record, relation, linked/filtered view, toggle, or section before adding another navigation layer.
- `FULL_GAME_FLOW_VISIBLE_ON_HOME` is mandatory.
- `CORE_SYSTEMS_AND_SETTING_VISIBLE_ON_HOME` is mandatory.
- `PROJECT_SPECIFIC_CORE_DATA_TABLES_VISIBLE_ON_HOME` is mandatory.
- `HOME_DETAIL_LINKS_CANNOT_REPLACE_CORE_UNDERSTANDING` is mandatory.
- Project Home stays information-rich; IA simplification must not reduce it to a status/link dashboard.
- Home may summarize/project data, but must not become a second structured/runtime canon.
- L2 Domain pages are not empty folder pages; each must explain scope/current authority/status and expose its L3 owners or project-filtered views.
- Recommended L2 count is 4~6 per project, with project-specific names. No universal game taxonomy is forced.
- No project runtime/gameplay mutation is part of this migration.
- No image generation is part of this migration.
- No paid Notion feature is required; use the existing zero-incremental-cost search/fetch/view/readback path.
- Open/draft work owned by another workstream remains read-only. In particular, Coc-Fiction PR #48 and GRIMOIRE PR #151 are not modified, rebased, merged, closed, or promoted by this migration.
- Every Notion move requires pre-read inventory and destination readback; page deletion is not part of the migration.
- Connector readback does not prove pixel geometry/mobile layout; retain `UI_GEOMETRY_NOT_VERIFIED` unless a rendered surface is actually inspected.

---

### Task 1: Lock the shallow IA and rich-Home contract with RED tests

**Files:**
- Modify: `tests/test_human_home_self_contained_contract.py`
- Modify: `tests/test_notion_human_system_surface_separation.py`

**Interfaces:**
- Consumes: existing Human Home and workspace authority contracts.
- Produces: regression assertions for L0~L3 navigation and the four non-negotiable Home requirements.

- [ ] **Step 1: Add failing Human Home requirements**

Add this test to `tests/test_human_home_self_contained_contract.py`:

```python
def test_project_home_keeps_full_flow_system_setting_and_core_tables(self) -> None:
    text = POLICY.read_text(encoding="utf-8")
    for term in (
        "FULL_GAME_FLOW_VISIBLE_ON_HOME",
        "CORE_SYSTEMS_AND_SETTING_VISIBLE_ON_HOME",
        "PROJECT_SPECIFIC_CORE_DATA_TABLES_VISIBLE_ON_HOME",
        "HOME_DETAIL_LINKS_CANNOT_REPLACE_CORE_UNDERSTANDING",
    ):
        self.assertIn(term, text)
```

- [ ] **Step 2: Add failing machine-readable IA requirements**

Add this test to `tests/test_notion_human_system_surface_separation.py`:

```python
def test_workspace_authority_contract_uses_shallow_project_navigation(self) -> None:
    contract = json.loads(AUTHORITY.read_text(encoding="utf-8"))
    self.assertEqual(
        contract["notion_navigation_layers"],
        ["PROJECT_HUB", "HUMAN_PROJECT_HOME", "DOMAIN_WORKSPACE", "DETAIL_OR_RECORD"],
    )
    self.assertEqual(contract["default_navigation_depth_max"], "L3")
    self.assertEqual(contract["l4_normal_page_nesting"], "AVOID")
    self.assertEqual(contract["domain_workspace_recommended_count"], {"min": 4, "max": 6})
```

- [ ] **Step 3: Commit test-only RED**

Run the Base PR checks on the test-only head. Expected failure: the four Home tokens and shallow IA machine fields do not yet exist.

- [ ] **Step 4: Record exact RED evidence**

Record the failing test names and exact test-only head in the draft PR. Do not count unrelated green checks as TDD evidence.

---

### Task 2: Implement the Base IA contract without creating a new Skill

**Files:**
- Modify: `docs/operations/HUMAN_HOME_SELF_CONTAINED_POLICY.md`
- Modify: `docs/operations/NOTION_PROJECT_ISOLATION_AND_CORE_SYSTEM_CONTRACT.md`
- Modify: `docs/operations/PROJECT_WORKSPACE_AUTHORITY_CONTRACT.json`
- Modify: `docs/DOCUMENTATION_MAP.md`

**Interfaces:**
- Consumes: Task 1 assertions and the approved spec.
- Produces: one current Notion IA owner chain that all migrations follow.

- [ ] **Step 1: Add the four Home hard requirements to Human Home policy**

Required text:

```text
FULL_GAME_FLOW_VISIBLE_ON_HOME
CORE_SYSTEMS_AND_SETTING_VISIBLE_ON_HOME
PROJECT_SPECIFIC_CORE_DATA_TABLES_VISIBLE_ON_HOME
HOME_DETAIL_LINKS_CANNOT_REPLACE_CORE_UNDERSTANDING
```

Define full flow as the project-relevant complete session/run/story progression, not only a one-line Core Loop. Define setting as player role/world premise/core conflict when it materially gives the systems meaning.

- [ ] **Step 2: Add the L0~L3 IA contract to the existing Notion isolation owner**

Required semantics:

```text
L0 PROJECT_HUB = project selection
L1 HUMAN_PROJECT_HOME = complete human understanding
L2 DOMAIN_WORKSPACE = responsibility grouping, 4~6 recommended
L3 DETAIL_OR_RECORD = terminal normal navigation layer
L4+ NORMAL_PAGE_NESTING = AVOID
SHALLOW_BY_DEFAULT = REQUIRED
NO_EMPTY_FOLDER_PAGE = REQUIRED
NO_FIXED_UNIVERSAL_GAME_TAXONOMY = REQUIRED
```

Replace direct-child wording such as “every GAME Home has `08 · 핵심 시스템 · 상세`” with a location-independent rule: the project-filtered Core System detail/view must exist under the appropriate L2 Domain and remain reachable from Home/Domain.

- [ ] **Step 3: Extend the machine-readable authority contract**

Add exactly:

```json
"notion_navigation_layers": [
  "PROJECT_HUB",
  "HUMAN_PROJECT_HOME",
  "DOMAIN_WORKSPACE",
  "DETAIL_OR_RECORD"
],
"default_navigation_depth_max": "L3",
"l4_normal_page_nesting": "AVOID",
"domain_workspace_recommended_count": {"min": 4, "max": 6},
"domain_workspace_policy": "PROJECT_SPECIFIC_NAMES_NO_EMPTY_FOLDER",
```

Add the four Home hard requirements to `human_home_required_sections`.

- [ ] **Step 4: Update the Documentation Map project standard**

Replace the old direct `01..07+` sibling-page standard with the L0~L3 role model. Preserve the fact that Visual/Story Bible, Flow/Storyboard, Asset, Reference, Production and project-specific confirmed tables remain valid documents; only their navigation grouping changes.

- [ ] **Step 5: Run focused tests and full applicable Base CI**

Expected: Task 1 tests pass; existing Human/System separation and approved-visual/readback tests remain green.

- [ ] **Step 6: Commit the contract implementation**

Commit as one Base policy/contract change before any Notion page move.

---

### Task 3: Build a complete migration inventory before moving pages

**Files:**
- Create: `docs/operations/notion-project-ia/2026-08-24_PROJECT_IA_MIGRATION_MAP.md`

**Interfaces:**
- Consumes: current `00 · 프로젝트 허브`, all 10 Project Homes, child-page trees, and current open-PR ownership.
- Produces: explicit `current parent → target L2 Domain → L3 owner` mapping and rollback parent for every moved page.

- [ ] **Step 1: Fetch the Project Hub and all 10 Project Homes**

Record exact Home IDs and direct child pages.

- [ ] **Step 2: Inventory every direct child page under each Home**

Classify each page:

```text
UNIQUE_CURRENT
DUPLICATE_PROJECTION
STALE_CURRENT
HISTORICAL
SYSTEM_ONLY
```

No page is moved before it has one classification and a target owner.

- [ ] **Step 3: Choose 4~6 L2 Domain names per project**

Use project semantics rather than a forced global taxonomy. The map must include the Tetris/TEN_PACES/Blacksmith/COC-Fiction examples from the spec only as starting patterns, not mandatory names.

- [ ] **Step 4: Record rollback metadata**

For every move record:

```text
page_id
current_parent_id
target_domain_id_or_planned_name
classification
reason
home_projection_that_must_remain
rollback_parent_id
```

- [ ] **Step 5: Protect active work**

Mark pages whose current meaning depends on Coc-Fiction PR #48 or GRIMOIRE PR #151 as `ACTIVE_OTHER_WORKER_READ_ONLY`. Structural move may occur only if it does not promote branch-only content or alter those PRs’ semantic authority; otherwise defer that page until the owner workstream closes.

---

### Task 4: Pilot the physical migration on Tetris

**Files/Notion surfaces:**
- `Tetris · Home`
- Create 4~6 L2 Domain pages under Tetris Home
- Reparent existing Tetris detail pages under those Domains

**Interfaces:**
- Consumes: Task 3 Tetris mapping.
- Produces: first verified shallow project tree and a rollback-safe migration pattern.

- [ ] **Step 1: Re-fetch Tetris Home and every page to be moved immediately before writes**

Abort on unexpected parent/content drift.

- [ ] **Step 2: Create only the required non-empty Domain pages**

Recommended pilot domains:

```text
01 · Direction · Planning
02 · Combat Design · Data
03 · Visual · UX · Assets
04 · Production · Validation
05 · Reference · Benchmark
```

Each Domain page must be created with a short responsibility summary and its intended L3 contents; do not create blank folder pages.

- [ ] **Step 3: Move Tetris L3 pages to their Domains**

Target mapping:

```text
Direction · Planning
  프로젝트 전체 작업계획
  Production Content Lock
  Final Planning Completeness Audit

Combat Design · Data
  핵심 시스템 · 상세
  세계관 · 전투 판타지
  대표 전투 · Gatebreaker Encounter
  Vertical Slice · First Run Flow

Visual · UX · Assets
  비주얼 바이블
  UI · 퍼즐 전투 Flow Map
  에셋 라이브러리
  오디오 바이블
  P0 이미지 제작 패키지

Production · Validation
  Production · Handoff

Reference · Benchmark
  Reference · Benchmark 도서관
```

- [ ] **Step 4: Rewrite the Home drilldown area to show only the L2 Domains**

Do not remove from Home: full game flow, Shared Turn Time/Line/Chain/Action relationships, current setting/player role, core data table, Visual direction, AI interpretation, edit guide, current state/evidence ceiling.

- [ ] **Step 5: Read back Tetris Home, every L2 Domain, and representative L3 pages**

Acceptance:

```text
Home direct navigation choices = 4..6 Domains
full game flow still visible on Home
core systems + setting still visible on Home
project-specific core data table still visible on Home
no moved L3 page lost
no L4 normal page nesting introduced
```

- [ ] **Step 6: Run a whole-pilot adversarial review**

If a Home requirement is lost, rollback the affected move or restore the projection before fleet rollout.

---

### Task 5: Migrate the remaining 9 project Homes with project-specific Domains

**Files/Notion surfaces:**
- GRIMOIRE
- Switchy Express
- 괴이기록국
- 닌자 서바이벌
- 마이 리틀 보트
- 블랙스미스
- 십보강호
- 오멘워드
- COC-Fiction

**Interfaces:**
- Consumes: verified Tetris migration pattern and each project’s Task 3 map.
- Produces: shallow L0~L3 navigation across the fleet without flattening project-specific meaning.

- [ ] **Step 1: Process one project at a time**

For each project: fresh Home/child fetch → create only necessary L2 Domains → move mapped L3 pages → rewrite Home drilldowns → destination readback.

- [ ] **Step 2: Preserve project-specific Human Home content**

Examples of required Home-visible data:

```text
TEN_PACES: 10칸 / 3·3·4 / 상대 15 / Route 8 / 무공·기술 예산
Blacksmith: 강화 / CURRENT·MAX 내구 / 파괴 / 수리 / 경제·고객 보조축
Omenward: Forecast / 3×3 징조륜 / 병종·건물 / 비가역 전선 / 20 Stage
GRIMOIRE: 글자·문법 / 주문 설계 / 마나·불안정도 / 마도서 학습 흐름
COC-Fiction: Part 흐름 / 주요 인물 / 세력·관계 / 사건·세계 규칙 / 정본화 상태
```

- [ ] **Step 3: Keep open-owner content read-only**

For GRIMOIRE, do not treat PR #151 branch-only component-sheet work as current Home truth. For COC-Fiction, do not promote PR #48 branch-only Ch026–030 state beyond its actual merged/approved status.

- [ ] **Step 4: Validate each project immediately after migration**

Do not wait until the end to discover a broken parent/link. Verify Home → Domain → L3 navigation, Home richness, and source/status ceilings for each project before moving to the next.

---

### Task 6: Remove navigation drift and duplicate-current projections revealed by the migration

**Files/Notion surfaces:** migrated Home/L2/L3 pages only.

**Interfaces:**
- Consumes: migration inventory classifications.
- Produces: one current owner per question and historical material clearly separated from current guidance.

- [ ] **Step 1: Resolve `DUPLICATE_PROJECTION` items**

Keep the Human Home summary/projection and one detailed owner. Remove duplicate current explanations from sibling pages only when destination readback proves the surviving owner is complete.

- [ ] **Step 2: Resolve `STALE_CURRENT` items**

Convert stale mutable SHA/PR/current-state prose to live-read locators or historical labels; do not replace it with another hard-coded current value unless the value is itself canonical content.

- [ ] **Step 3: Preserve `HISTORICAL` material**

Keep it as labeled historical/toggle/archive material when it has provenance value; do not let it compete with current authority.

- [ ] **Step 4: Re-run the four Home hard gates across all 10 Homes**

A project fails migration if any one of full flow, systems+setting, core data tables, or self-contained understanding disappeared from Home.

---

### Task 7: Full review, PR, merge, and postmerge fleet readback

**Files:** all Base files changed by Tasks 1~2 plus the migration map/spec/plan.

**Interfaces:**
- Consumes: completed Base contract and Notion fleet migration.
- Produces: merged Base policy plus verified Notion structure.

- [ ] **Step 1: Refresh Base main and all open PRs**

Confirm this workstream has no same-goal Base PR and keep unrelated project PRs read-only.

- [ ] **Step 2: Run full applicable Base CI on the exact implementation head**

Required outcome: all required checks green; no unresolved review threads.

- [ ] **Step 3: Run minimum five whole-result adversarial reviews**

Every counted loop re-reviews the complete result:

```text
user intent
Base authority/consumer consistency
10 Home richness
L0~L3 navigation depth
L2 domain quality/no empty folders
SSoT/duplicate-current risk
Notion move/readback integrity
open PR concurrency
cost/rollback
IRG/evidence ceiling
```

If a material finding changes the final candidate, fix it and restart the clean-count sequence from `0/5`.

- [ ] **Step 4: Mark PR ready and squash merge the exact reviewed head**

Use expected-head protection. Do not change PR metadata after the final synthetic merge checks if that would invalidate the checked merge ref.

- [ ] **Step 5: Postmerge GitHub readback**

Read the new Base `main` copies of the Human Home policy, Notion isolation contract, machine authority contract, and regression tests.

- [ ] **Step 6: Postmerge Notion fleet readback**

Re-fetch Project Hub and all 10 Homes, then verify each Home has 4~6 L2 Domain drilldowns and still satisfies the four Home hard gates. Sample at least one Domain and one L3 owner per project.

- [ ] **Step 7: Final evidence ceiling**

Report `UI_GEOMETRY_NOT_VERIFIED` unless actual rendered desktop/mobile Notion views were inspected. Do not infer gameplay/runtime/Human usability PASS from an IA migration.

- [ ] **Step 8: Final user report**

Report `작업 전 → 개선된 구조/기능 → 실제 예 → 기대효과 → 아직 검증되지 않은 범위`, plus remaining work and any deferred pages protected by active owner PRs.
