# Single-Chat Partition & Self-Contained Notion Home Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the nine-chat Part execution contract with one-chat sequential P01→P09 maintenance, allow evidence-driven cross-Part repairs, enforce true full-scope adversarial loops, make Notion Home pages self-contained, and onboard the new Tetris project without inventing canon.

**Architecture:** Keep P01..P09 as responsibility/learning views and checkpoints, but move execution authority to one coordinator chat. Preserve independent open workstream protection separately from Part boundaries. GitHub remains structured/runtime truth; Notion becomes a complete human-facing projection with child pages reserved for depth/evidence.

**Tech Stack:** Markdown, JSON contracts, Python unittest regression contracts, GitHub Actions, Notion.

**Spec:** `docs/superpowers/specs/2026-08-19-single-chat-partition-and-self-contained-notion-home-design.md`

## Global Constraints

- Latest user instruction outranks older Partition isolation rules.
- `FULL_LOOP_COUNT_MINIMUM: 5` remains required and means five complete full-scope lifecycles.
- Other open/draft/ready workstreams remain read-only unless ownership is explicitly transferred.
- Completed/merged `main` is the normal cross-Part integration surface.
- No new paid service/API/SaaS.
- Do not invent Tetris game design/runtime facts not present in repository/user instruction.
- Notion child pages may contain detail, but Base/Project Home must remain understandable without opening them.

---

### Task 1: Encode the new execution and adversarial contracts

**Files:**
- Modify: `AGENTS.md`
- Modify: `docs/operations/BASE_PARTITION_MANIFEST.json`
- Modify: `docs/operations/BASE_PARTITION_OPERATING_MODEL.md`
- Modify: `templates/prompts/BASE_PARTITION_OPTIMIZATION_PROMPT.md`
- Modify: `templates/prompts/BASE_PARTITION_INTEGRATION_PROMPT.md`
- Modify: `skills/running-adversarial-review-and-refinement/SKILL.md`
- Test: `tests/test_base_partition_contract.py`
- Test: `tests/test_neutral_adversarial_feature_lifecycle.py`

**Interfaces:**
- Consumes: latest user instruction and current Partition/adversarial contracts.
- Produces: `SINGLE_COORDINATOR_CHAT_SEQUENTIAL_PARTS`, `PART_BOUNDARY_IS_FOCUS_NOT_REPAIR_PROHIBITION`, and `FULL_LOOP_IS_NOT_A_REVIEW_LENS` contracts.

- [ ] Add failing tests requiring one-chat sequential P01→P09 execution, cross-Part repair authority with active-workstream protection, and rejection of lens-counted pseudo-loops.
- [ ] Run the focused contract tests and record RED.
- [ ] Update the canonical contracts with the minimal semantic changes.
- [ ] Run focused tests until GREEN.
- [ ] Verify current open P03/P08 PRs remain untouched.

### Task 2: Add self-contained Notion Home policy

**Files:**
- Modify: `docs/operations/PROJECT_WORKSPACE_AUTHORITY_CONTRACT.json` if needed for machine-readable ownership.
- Modify: `skills/managing-game-project-operating-system/SKILL.md`
- Modify: `tests/test_notion_project_isolation_core_system_contract.py`
- Modify/Create: a focused human-facing Home contract document only if no existing owner can express the requirement cleanly.

**Interfaces:**
- Consumes: `NOTION_HUMAN_FACING_CANON` and repository structured/runtime authority.
- Produces: Home-page completeness contract for Base and projects.

- [ ] Add RED tests that child-page navigation is optional for basic project understanding and that Home exposes direction/core loop/systems/UX/visual/runtime/evidence/decisions/risks/next work.
- [ ] Update the existing project operating owner rather than creating a duplicate Skill.
- [ ] Run focused tests to GREEN.

### Task 3: Update Base Notion Home

**Files:**
- Notion: `Base · 작업 시스템 & Skill 지도`

**Interfaces:**
- Consumes: merged/current Base Skills, modules, Part map, and execution rules.
- Produces: self-contained human-facing Base operating manual.

- [ ] Expand active Skill explanations to purpose, trigger, operation, output, expected effect, and related modules/tests.
- [ ] Expand module flow to describe input/process/output/failure impact at each stage.
- [ ] Expand P01..P09 descriptions to responsibility, workflow, dependencies, expected effect, and current status.
- [ ] Replace nine-chat wording with one-chat sequential Part operation.
- [ ] Replace mandatory cross-Part deferral wording with evidence-driven repair authority plus active-workstream protection.
- [ ] Read back the page.

### Task 4: Establish Project Home completeness and update representative projects

**Files:**
- Notion: representative existing Project Home pages used to verify the pattern.

**Interfaces:**
- Consumes: current project canon and existing child pages.
- Produces: Home pages that explain the project without mandatory navigation.

- [ ] Update at least the currently inspected OMENWARD Home with current core loop, major systems, UX/visual state, implementation/evidence status, key decisions, risks, and next work already present in its canon.
- [ ] Preserve child pages as detail/evidence surfaces.
- [ ] Do not invent project facts absent from current sources.
- [ ] Read back the updated Home.

### Task 5: Onboard Tetris to Notion

**Files:**
- Notion data source: `PROJECT REGISTRY · Master`
- Notion: new `Tetris` Project Home

**Interfaces:**
- Consumes: `alsdmlals4-eng/Tetris` repository metadata and user statement that production has started.
- Produces: an ACTIVE GAME registry record and self-contained initial Home with explicit unknown states.

- [ ] Confirm repository/default branch/current commit availability.
- [ ] Create `Tetris` registry entry with repository URL, `ACTIVE`, `GAME`, and no fabricated SHA.
- [ ] Create initial Home describing current stage, known facts, undefined areas, evidence state, and next canon-building steps.
- [ ] Read back the page.

### Task 6: Reconcile provided P01..P09 completion results

**Files:**
- CP0 and owner-correct files identified by deduplicated cross-Part findings.

**Interfaces:**
- Consumes: provided P01/P02/P04/P05/P06/P07/P09 merged packets and P03/P08 open blockers.
- Produces: one deduplicated Integration finding set without mutating unrelated active PR branches.

- [ ] Re-pin latest `main`.
- [ ] Treat merged Part results as completed-main evidence only.
- [ ] Re-check P03 #537 and P08 #535 without editing their branches.
- [ ] Deduplicate CP0 requests for Manifest path drift, legacy Sheet/Figma authority, Registry wording, freshness companion ownership, validation-consumption proof, and P01/P07 dependency declaration.
- [ ] Implement only changes justified by the current integration goal and current-main evidence.

### Task 7: Full verification and adversarial convergence

**Files:**
- All changed files from Tasks 1–6.

**Interfaces:**
- Consumes: exact candidate head and Notion readback evidence.
- Produces: merge-ready exact head.

- [ ] Run focused Partition/adversarial/Notion project tests.
- [ ] Run Base v9/global integrity and changed-domain Required CI.
- [ ] Run full adversarial improvement loop 1 over the entire resulting state.
- [ ] Run full adversarial improvement loop 2 over the entire resulting state.
- [ ] Run full adversarial improvement loop 3 over the entire resulting state.
- [ ] Run full adversarial improvement loop 4 over the entire resulting state.
- [ ] Run full adversarial improvement loop 5 over the entire resulting state.
- [ ] If any valid blocker remains, continue loop 6..N until zero.
- [ ] Confirm no loop is counted by merely assigning a different review lens.
- [ ] Confirm unresolved review threads = 0 and exact-head checks are current.

### Task 8: Merge and post-merge readback

**Files:**
- GitHub PR / `main`
- Notion Base Home / representative Project Home / Tetris Home

**Interfaces:**
- Produces: durable Base policy and final user-facing state.

- [ ] Squash merge exact head after all gates.
- [ ] Read new Base `main` and canonical contracts back.
- [ ] Update Notion Base Home to the merged SHA if needed.
- [ ] Re-read Tetris Project Home and representative project Home.
- [ ] Report completed changes, tests, NOT_RUN, remaining active PRs, trade-offs, and revisit conditions.
