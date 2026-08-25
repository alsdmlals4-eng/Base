# Notion System Blueprint Contract Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

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
- Modify: the existing Base planning/Notion authority owner identified from current `main`.
- Create only if no canonical owner exists: `docs/NOTION_SYSTEM_BLUEPRINT_CONTRACT.md`.

**Interfaces:**
- Consumes: Project Home human-facing authority, repository structured/runtime authority, existing planning and implementation reality gates.
- Produces: canonical Blueprint applicability rules, node schema, authority boundary, validation/rollback rules.

- [ ] **Step 1: Read the current authority owners and same-goal open/recent PRs**

Confirm exact `main`, relevant policy/skill owners, and that no active same-goal PR should be modified.

- [ ] **Step 2: Add the minimal contract**

Define node fields: `Node ID`, `Type`, `Intent/Player Meaning`, `Trigger/Input`, `Condition`, `State/Data Change`, `Output/Next`, `Feedback`, `Owner`, `Godot Mapping`, `Validation`.

- [ ] **Step 3: Add an applicability gate**

Require Blueprint for multi-state/multi-system logic; explicitly exempt trivial copy, simple numeric changes, cosmetic-only edits, and already-proven repetitive implementation.

- [ ] **Step 4: Verify authority semantics**

Check that Blueprint is labeled derived human/implementation view and cannot override repository runtime truth or approved project canon.

- [ ] **Step 5: Commit the Base contract changes**

Commit on `feat/notion-system-blueprint-contract` with a focused message.

### Task 2: Add Blueprint presentation rules to the Notion operating surface

**Files:**
- Update: `P01 · Project Planning, Operations & Notion` in Notion.
- Update: `Base · 작업 시스템 & Skill 지도` only if needed for discoverability.

**Interfaces:**
- Consumes: Task 1 Blueprint contract.
- Produces: human-facing placement and rendering rules for Project Home and detailed Blueprint pages.

- [ ] **Step 1: Read the latest P01 and Base Notion guide**

Confirm current Home/Registry/AI Workspace boundaries before editing.

- [ ] **Step 2: Add Project Home placement rule**

Place `핵심 System Blueprint` near Core Loop/Flow/Visual at the top-level human view; use bounded Mermaid/node flow or equivalent readable node representation.

- [ ] **Step 3: Add detailed Blueprint page rule**

Store node table, conditions, state/data ownership, Godot mapping, edge cases, and validation criteria in the detailed human/AI implementation surface without leaking raw operational metadata into Home.

- [ ] **Step 4: Add node lifecycle rule**

Require Blueprint updates when an approved system-flow decision changes; runtime implementation evidence remains in GitHub/AI Workspace.

- [ ] **Step 5: Read back the destination pages**

Verify the new guidance is visible, unambiguous, and does not displace existing human-facing content.

### Task 3: Validate with one project pattern without mass-editing every project

**Files:**
- Read: a current Project Home with clear system flow (e.g. 십보강호 or 블랙스미스).
- Update only if a safe, representative insertion can be made without inventing project-specific design decisions.

**Interfaces:**
- Consumes: Blueprint contract and Notion presentation rules.
- Produces: feasibility evidence and a reusable project template pattern.

- [ ] **Step 1: Select a representative current Home from latest Notion state**

Choose a project whose existing approved flow can be represented without adding new gameplay decisions.

- [ ] **Step 2: Convert one existing approved flow into Blueprint node form**

Use only existing approved facts; do not invent conditions, values, or mappings that are not currently canonical.

- [ ] **Step 3: Check readability and duplication**

Confirm the Home still reads as a human design overview and the Blueprint links/summarizes rather than duplicating the full implementation record.

- [ ] **Step 4: Record NOT_RUN ceilings**

If no runtime execution or device test is performed, leave those verification claims as `NOT_RUN` in the system/evidence layer.

### Task 4: Adversarial review, PR, and post-change readback

**Files:**
- Review all changed Base and Notion surfaces.

**Interfaces:**
- Consumes: Tasks 1–3 outputs.
- Produces: clean change set, rollback path, PR, and verified destination state.

- [ ] **Step 1: Run five full adversarial review passes**

Attack: third-canon risk, graph bloat, AI misinterpretation, Home clutter, unnecessary mandatory work.

- [ ] **Step 2: Reconcile current `main` and same-goal PR state**

Do not absorb open/draft/ready PR work; rebase/update only this new branch if required by current completed main.

- [ ] **Step 3: Verify Implementation Reality Gate**

Claim only document/Notion readback that was actually performed; runtime behavior remains unverified unless executed.

- [ ] **Step 4: Open a focused PR**

Summarize before/after, expected effect, risks, rollback, Notion destinations, and verification evidence.

- [ ] **Step 5: Final readback**

Confirm branch/PR state and Notion content after writes; report remaining non-Blueprint project work separately.
