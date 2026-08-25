# Notion System Blueprint Contract Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [x]`) syntax for completed tracking.

**Goal:** Add a Notion-facing System Blueprint contract that visualizes core gameplay/system logic as bounded nodes while preserving GitHub as structured/runtime canon and avoiding a third source of truth.

**Architecture:** Extend the existing Project Home / AI Workspace / repository authority model rather than introducing a new visual-scripting runtime. Human-facing Blueprint nodes summarize player action, trigger, condition, state/data mutation, feedback, and validation; detailed implementation mapping remains in the project AI/System surface and repository canon. Blueprint applicability is gated to complex, connected systems so trivial edits remain lightweight.

**Tech Stack:** Notion human-facing pages, Base Markdown governance/docs, Mermaid/structured node notation, GitHub PR workflow.

**Spec:** Approved in-chat design from 2026-08-25: `Notion System Blueprint = human-readable node view + implementation contract; not a Godot/Unreal visual scripting replacement`.

## Global Constraints

- Project Home remains human-facing; operational metadata such as PASS/NOT_RUN/SHA/PR/CI stays in AI/System/Handoff unless translated into human meaning.
- Repository remains structured/runtime canon for code, data, scenes, resources, tests, and implementation truth.
- Blueprint is a derived view/contract, not an independent third canon.
- Apply Blueprint only to connected systems/flows (core loop, combat, economy, AI, progression, complex UI/UX, reusable modules), not trivial copy/value/style edits.
- Existing open/draft/ready PRs are read-only unless explicit absorption authorization exists.
- No new paid dependency, visual-scripting engine, or custom graph runtime is introduced.

---

### Task 1: Define the System Blueprint contract in Base

**Files:**
- Canonical contract: `docs/operations/project-workspace/NOTION_SYSTEM_BLUEPRINT_CONTRACT.md` (P01 Project Planning/Notion owner).
- Consumer integration: `docs/knowledge/game-development/NOTION_VISUAL_ASSET_AND_FLOW_WORKFLOW.md` (P05 Notion Visual Flow consumer).

**Interfaces:**
- Consumes: Project Home human-facing authority, repository structured/runtime authority, existing planning and implementation reality gates.
- Produces: canonical Blueprint applicability rules, node schema, authority boundary, validation/rollback rules.

- [x] **Step 1: Read the current authority owners and same-goal open/recent PRs**

Confirmed exact `main`, P01/P05 ownership, and protected PR #674 / #660 as read-only.

- [x] **Step 2: Add the minimal contract**

Defined `Node ID`, `Type`, `Intent/Player Meaning`, `Trigger/Input`, `Condition`, `State/Data Change`, `Output/Next`, `Feedback`, `Owner`, `Godot Mapping`, `Validation`.

- [x] **Step 3: Add an applicability gate**

Complex multi-state/multi-system logic uses Blueprint; trivial copy, isolated numeric tuning, cosmetic-only edits, and already-proven repetitive implementation are exempt.

- [x] **Step 4: Verify authority semantics**

Blueprint is a derived human/implementation view and cannot override repository runtime truth or approved project canon.

- [x] **Step 5: Commit the Base contract changes**

Committed on `feat/notion-system-blueprint-contract`.

### Task 2: Add Blueprint presentation rules to the Notion operating surface

**Files:**
- Updated: `P01 · Project Planning, Operations & Notion`.
- Created under P01: `System Blueprint · Node Contract & Template`.
- `Base · 작업 시스템 & Skill 지도` did not require duplicate Blueprint content because P01 remains the semantic entry point.

- [x] **Step 1: Read the latest P01 and Base Notion guide**

Confirmed current Home/Registry/AI Workspace boundaries before editing.

- [x] **Step 2: Add Project Home placement rule**

Blueprint is placed near Core Loop / Flow / Visual material when the applicability gate passes.

- [x] **Step 3: Add detailed Blueprint page rule**

Detailed surfaces retain stable Node IDs, conditions, state/data ownership, Godot mapping, edge cases and validation; Home shows the readable human projection.

- [x] **Step 4: Add node lifecycle rule**

Approved system-flow changes update the human Blueprint in the same approval unit; runtime evidence remains repository/AI-System owned.

- [x] **Step 5: Read back the destination pages**

P01 and the child Blueprint template were fetched after writes and the parent/entry boundary was verified.

### Task 3: Validate with one project pattern without mass-editing every project

**Files:**
- Pilot: `십보강호 · Home`.

- [x] **Step 1: Select a representative current Home from latest Notion state**

Selected 십보강호 because its approved duel-decision flow already existed and could be converted without new design decisions.

- [x] **Step 2: Convert one existing approved flow into Blueprint node form**

Converted the existing `관찰 → 가설 → 3/3/4 계획 → COMMIT → 거리·합·대응·중단 → Combat Review → 다음 가설` flow only.

- [x] **Step 3: Check readability and duplication**

Removed stable `BP-*` IDs from the Home-facing graph/table after adversarial review; Home now exposes human-readable stages and player meaning while detail contracts retain stable-ID capability.

- [x] **Step 4: Record NOT_RUN ceilings**

No Godot/runtime/device/human-play claim was promoted. Runtime and human/device validation remain `NOT_RUN` for this workflow change.

### Task 4: Adversarial review, PR, and post-change readback

- [x] **Step 1: Run five full adversarial review passes and continue until clean candidate**

Minimum five whole-state loops were completed and review continued after findings changed the candidate. Validated corrections covered node vocabulary, canonical path ownership, Home metadata leakage, P01/P05 semantic ownership, stale plan references, and stale PR metadata.

- [x] **Step 2: Reconcile current `main` and same-goal PR state**

PR #674 and #660 remained read-only; no open PR delta was absorbed or modified.

- [x] **Step 3: Verify Implementation Reality Gate**

Notion and repository document writes/readbacks were performed. Runtime/human/device claims remain explicitly unverified.

- [x] **Step 4: Open a focused PR**

PR #675 records before/after, expected effect, risks, rollback, Notion destinations, open-PR protection and evidence ceilings.

- [x] **Step 5: Final readback**

Branch/PR, P01 Blueprint template, and the representative 십보강호 Home were read back after semantic writes. Final-head CI is rechecked after this completion-status commit before readiness is claimed.

## Completion candidate

- Canonical owner: P01 `docs/operations/project-workspace/NOTION_SYSTEM_BLUEPRINT_CONTRACT.md`
- P05 consumer: `NOTION_VISUAL_ASSET_AND_FLOW_WORKFLOW.md`
- Notion generic template: `System Blueprint · Node Contract & Template`
- Representative pilot: `십보강호 · Home`
- Runtime / human-device evidence: `NOT_RUN`
- Merge/readiness: gated by final-head CI and final clean review.
