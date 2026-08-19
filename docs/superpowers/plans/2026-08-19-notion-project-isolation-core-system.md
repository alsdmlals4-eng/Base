# Notion Project Isolation + Core System Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 여러 프로젝트가 하나의 Notion workspace를 병렬 사용해도 Project namespace를 넘는 쓰기를 막고, `CORE SYSTEM · Master`와 My Little Boat Project Home을 추가한다.

**Architecture:** 기존 공용 Project/Work/Asset Master는 유지하고 Project relation을 namespace로 사용한다. 새 Core System Master에는 deterministic Record Key, Revision, Last Edited, Sync State를 두어 cross-project write를 차단하고 same-record concurrent write를 optimistic conflict detection으로 fail-closed 한다. 각 Project Home에는 자기 Project로 필터된 linked view만 노출한다.

**Tech Stack:** Base Markdown/JSON contracts + Python unittest contracts + Notion Project Registry/relations/linked database views + GitHub repository source/readback.

**Spec:** `docs/superpowers/specs/2026-08-19-notion-project-isolation-core-system-design.md`

## Global Constraints

- `DOMAIN_SPLIT_CANON`을 유지한다.
- Notion은 사람용 전체 그림/Visual/Flow/예산/Tier/핵심 시스템 정본, repository는 structured/runtime 정본이다.
- 기존 8개 Project Registry row, Work/Asset record, child page를 삭제·이동하지 않는다.
- cross-project write는 금지하며 모든 project-scoped record는 정확히 하나의 Project relation을 가져야 한다.
- same-record AI write는 pre-read + immediate re-read + Revision/Last Edited 비교 후 bounded update만 허용한다.
- stale read, duplicate Record Key, missing Project relation은 fail-closed 한다.
- `My Little Boat` repository는 `alsdmlals4-eng/MylittleBoat`, Project Key는 `MY_LITTLE_BOAT`다.

---

### Task 1: Base concurrency/core-system contract regression

**Files:**
- Create: `tests/test_notion_project_isolation_core_system_contract.py`
- Modify: `docs/operations/PROJECT_WORKSPACE_AUTHORITY_CONTRACT.json`
- Modify: `skills/managing-design-documents/SKILL.md`
- Modify: `docs/DOCUMENTATION_MAP.md`

**Interfaces:**
- Consumes: existing `DOMAIN_SPLIT_CANON`, `PROJECT_RELATION_REQUIRED`.
- Produces: `PROJECT_NAMESPACE_ISOLATION`, `CORE_SYSTEM_MASTER`, `OPTIMISTIC_CONFLICT_DETECTION`, `BOUNDED_RECORD_WRITE`, `CONFLICT_STALE_READ` discovery contract.

- [ ] Write a unittest that loads the workspace authority JSON and asserts the new concurrency/core-system tokens and required record type `SYSTEM`.
- [ ] Assert `managing-design-documents` documents exact Project resolution, deterministic Record Key, Revision/Last Edited re-read, field-level update, conflict abort, and destination readback.
- [ ] Assert `DOCUMENTATION_MAP.md` routes `CORE SYSTEM · Master` and project `08 · 핵심 시스템 · 상세` pages.
- [ ] Push RED test-only commit and confirm CI/test failure is caused by missing contract fields.
- [ ] Update the three Base authority/docs files minimally.
- [ ] Re-run exact-head CI and confirm all required workflows pass.

### Task 2: Harden existing Notion project metadata

**Notion surfaces:**
- `PROJECT REGISTRY · Master`
- `작업계획 · Master`
- `ASSET LIBRARY · Master`

**Interfaces:**
- Consumes: Project Registry relation targets.
- Produces: project namespace metadata and explicit sync state used by future writes.

- [ ] Query Project Registry and verify no duplicate/non-empty Project Key violations.
- [ ] Add only missing concurrency metadata needed at project level: `Sync State`, `Revision`, `Repo Main SHA`, `Last Synced`, `Last Edited`.
- [ ] Preserve all existing rows and options.
- [ ] Query Work/Asset masters for missing Project relations; do not auto-assign ambiguous rows.
- [ ] Record any existing invalid rows as review-required rather than guessing project ownership.

### Task 3: Create CORE SYSTEM · Master

**Notion surface:**
- Parent: `90 · SYSTEM MASTERS`
- New DB: `CORE SYSTEM · Master`

**Interfaces:**
- Consumes: Project Registry relation.
- Produces: Project-scoped system/entity/rule records and self Parent/Children relation.

- [ ] Create database with schema from the design spec.
- [ ] Add self relation `Parent / Children` after data source ID exists.
- [ ] Create a system-master table view showing Project, Record Key, Record Type, Status, Sync State, Revision, Source Path, Source SHA.
- [ ] Fetch schema back and verify all required properties/types.

### Task 4: Add My Little Boat to Project Registry and Project Home

**Source:**
- `alsdmlals4-eng/MylittleBoat@main`
- `AGENTS.md`, `README.md`, `docs/CONCEPT.md`, `docs/MVP_SCOPE.md`, `docs/GODOT_MVP_ROADMAP.md`.

**Interfaces:**
- Produces: Registry row `MY_LITTLE_BOAT` and project child pages.

- [ ] Re-query Project Registry for an existing `MY_LITTLE_BOAT` or same repository URL; abort duplicate creation if found.
- [ ] Create Project row with repository URL, `ACTIVE`, `GAME`, and a Project Home summary grounded only in current main.
- [ ] Create child pages `01` through `06` following current game-project pattern and `08 · 핵심 시스템 · 상세`.
- [ ] Add linked Work/Asset/Core System views filtered by the exact My Little Boat Project page URL.
- [ ] Read back Registry properties, Home content, child-page references and view filters.

### Task 5: Add project-specific 08 Core System pages

**Projects:** all active GAME rows in Project Registry.

**Interfaces:**
- Consumes: Core System Master and each Project page URL.
- Produces: one `08 · 핵심 시스템 · 상세` page per game project.

- [ ] Search each Project Home for an existing `08` page before creation.
- [ ] Create missing `08` page without replacing existing child pages.
- [ ] Add one linked Core System view filtered by that exact Project relation.
- [ ] Add a short project-specific explanation of what belongs in the page.
- [ ] Read back each `08` page and verify no unfiltered Master view is exposed.

### Task 6: Populate OMENWARD core system records

**Source:** current `main` `docs/OMENWARD_GDD_CURRENT_CANON.md` and current approved owners referenced there.

**Interfaces:**
- Produces deterministic `OMENWARD::*` records.

- [ ] Create top-level records for core loop, MapRun/Stage, pressures, resources/reels/deployment, building tiers, mana/tactics, merchant, onboarding, hero/meta.
- [ ] Create building child records for Vault, Farm, General Barracks, Special Barracks, Defense Tower, Command Post, Mana Tower.
- [ ] Encode current Special Barracks T1 TokenSource rule from current canon; do not restore superseded no-TokenSource wording.
- [ ] Create troop/branch role records where current main supports them; keep unresolved numerics `PROVISIONAL` or `DEFERRED`.
- [ ] Read back and verify every row has Project=OMENWARD, unique Record Key, source path/SHA, Revision=1, Sync State=SYNCED.

### Task 7: Populate TEN_PACES core system records

**Source:** current `main` `docs/01_GAME_DESIGN.md`, `docs/03_CONTENT_CATALOG.md`, `docs/03_TEN_MARTIAL_MANUALS_CATALOG.md`, current decision owners.

**Interfaces:**
- Produces deterministic `TEN_PACES::*` records.

- [ ] Create battlefield/3-3-4 loop, route-node cadence, combat/resource/resolution top-level records.
- [ ] Create five stat records: 외공, 근골, 신법, 내공, 심안 with current derived maxima/rules.
- [ ] Create route node records for rest/training/information/short event and major-duel cadence.
- [ ] Create 10 current martial manual records.
- [ ] Create each manual’s 3/5/7/9/10-star skill/effect records with status inherited from source authority.
- [ ] Preserve `APPROVED_DRAFT_PLANNING`, `POC_HYPOTHESIS`, and deferred boundaries rather than upgrading them to confirmed.
- [ ] Read back Project, Record Key uniqueness, source SHA/status and representative skill rows.

### Task 8: Populate MY_LITTLE_BOAT core system records

**Source:** current `main` project docs.

**Interfaces:**
- Produces deterministic `MY_LITTLE_BOAT::*` records.

- [ ] Create core emotional promise and voyage loop records.
- [ ] Create mood selection, photo, appreciation mode, speed control, five-minute timer, voyage record, bottle letter, scenery, companion affection, album records.
- [ ] Create platform/input and forbidden-direction rule records.
- [ ] Keep not-yet-verified Godot runtime behavior distinct from documented MVP intent.
- [ ] Read back all records and verify Project namespace and source paths.

### Task 9: Cross-project collision audit and merge

**Validation:**

- [ ] Query Project Registry for duplicate `Project Key` and duplicate repository URLs.
- [ ] Query Core System Master for missing Project relation, missing Record Key, duplicate `(Project, Record Key)`, invalid Revision/Sync State.
- [ ] Verify linked Core System views on representative OMENWARD, TEN_PACES, MY_LITTLE_BOAT pages use exact Project relation filters.
- [ ] Re-fetch all modified Project Homes and `90 · SYSTEM MASTERS` to confirm no existing child page/database was deleted or moved unexpectedly.
- [ ] Run Base exact-head required workflows and merge only when Green.
- [ ] After merge, re-fetch Base main authority contract and Notion pages; report any post-merge CI that actually exists separately from pre-merge evidence.
