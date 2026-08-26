# Engine Baseline, Adapter, and Work Routing Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add an engine-neutral implementation/runtime policy above the current Godot adapter, pin production engine baselines behind a canary gate, and route long noncoding project work through ChatGPT Work.

**Architecture:** Keep existing Godot project/tool contracts intact as the current adapter specialization. Add one provider-neutral policy owner and make P06/P08 consume it; no portfolio migration or broad vocabulary rewrite occurs.

**Tech Stack:** Markdown policy docs, Python `unittest` contract tests, Notion Base maintenance pages.

**Spec:** `docs/superpowers/specs/2026-08-26-engine-baseline-adapter-work-routing-design.md`

## Global Constraints

- Existing Godot projects remain unchanged.
- `CODEX_GODOT_PRODUCT_IMPLEMENTATION_OWNER` stays as compatibility vocabulary.
- No path owned by pre-existing PR #660 is modified.
- No new paid dependency, MCP server, or engine is installed.
- Notion remains human-facing canon; repository remains implementation/runtime truth.
- Work is an execution surface, not canon.

---

### Task 1: Contract test

**Files:**
- Create: `tests/test_engine_adapter_and_work_routing_contract.py`

**Interfaces:**
- Consumes: current P06/P08 and absence of the new engine policy.
- Produces: regression expectations for the new policy and routing terms.

- [x] **Step 1: Write the failing test.**
- [x] **Step 2: Verify RED because the new policy and routing vocabulary are absent.**
- [ ] **Step 3: Keep the test unchanged while implementing the minimum policy/doc changes.**
- [ ] **Step 4: Run focused regression and verify GREEN.**

### Task 2: Engine-neutral baseline owner

**Files:**
- Create: `docs/knowledge/game-development/ENGINE_BASELINE_AND_ADAPTER_POLICY.md`

**Interfaces:**
- Consumes: existing Godot/HiGodot/GUT/Hera authority and AI game-engine machine-boundary lessons.
- Produces: `ENGINE_NEUTRAL_PRODUCT_IMPLEMENTATION_CORE`, `STABLE_ENGINE_BASELINE`, Godot default adapter, canary promotion, migration Reality Gate.

- [ ] **Step 1: Add the minimal provider-neutral policy.**
- [ ] **Step 2: Explicitly preserve existing Godot adapter/tooling contracts.**
- [ ] **Step 3: Add Work/Notion/GitHub authority boundary.**

### Task 3: P06 adapter correction

**Files:**
- Modify: `docs/operations/base-partitions/P06_GODOT_RUNTIME_TOOLCHAIN.md`

**Interfaces:**
- Consumes: new engine policy.
- Produces: current Godot adapter responsibilities without claiming Godot-specific details are the reusable core.

- [ ] **Step 1: Add neutral-core/current-adapter section.**
- [ ] **Step 2: Add stable baseline and canary update gate.**
- [ ] **Step 3: Keep existing HiGodot/runtime UI contracts unchanged.**

### Task 4: P08 Chat/Work/Codex routing

**Files:**
- Modify: `docs/operations/base-partitions/P08_AI_OPERATIONS_EXECUTORS.md`

**Interfaces:**
- Consumes: current GPT/Codex ownership and project canon.
- Produces: quick Chat, long multi-step Work, generic Codex game implementation, current Godot adapter compatibility.

- [ ] **Step 1: Add `CODEX_GAME_PRODUCT_IMPLEMENTATION_OWNER` while retaining the Godot owner token.**
- [ ] **Step 2: Add `CHAT_QUICK_DISCUSSION_DEFAULT` and `WORK_LONG_MULTISTEP_NONCODING_DEFAULT`.**
- [ ] **Step 3: Add `ENGINE_ADAPTER_SELECTED_FROM_PROJECT_CANON`.**
- [ ] **Step 4: State that Work does not replace Notion/GitHub authority.**

### Task 5: Notion read/write/readback

**Files:**
- Update: Base Notion `P06 · Godot, Runtime & Technical Toolchain`
- Update: Base Notion `P08 · AI Operations & External Executors`

**Interfaces:**
- Consumes: merged-intent Base policy wording.
- Produces: human-facing maintenance pages aligned with repository policy.

- [ ] **Step 1: Add current engine-neutral/Godot-adapter baseline note to P06.**
- [ ] **Step 2: Add Chat/Work/Codex routing note to P08.**
- [ ] **Step 3: Fetch both pages and verify destination readback.**

### Task 6: Verification and merge

**Files:**
- No new production paths.

**Interfaces:**
- Consumes: Tasks 1–5.
- Produces: exact-head evidence and merged current policy if repository gates allow it.

- [ ] **Step 1: Run focused contract suite / GitHub CI.**
- [ ] **Step 2: Confirm no pre-existing open PR path was modified.**
- [ ] **Step 3: Perform five whole-state adversarial review lenses: authority, compatibility, update churn, Work/canon boundary, migration overreach.**
- [ ] **Step 4: Mark PR ready only after GREEN and readback.**
- [ ] **Step 5: Merge by squash only if required checks/ruleset permit and exact head is unchanged.**
- [ ] **Step 6: Post-merge main and Notion readback.**
