# Game System Difficulty Workflow Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Extend the existing game-design strategy Skill with executable game-system, difficulty, and combat-AI design modes without creating a duplicate Specialist Skill.

**Architecture:** Keep `analyzing-and-refining-game-concepts` as the single primary discipline owner. Add two Skill Modes, place detailed procedures in one focused reference, provide one project-facing contract template, and synchronize machine routing, human routing, knowledge guidance, learning records, and tests.

**Tech Stack:** Markdown, JSON, Python `unittest`, GitHub Actions.

## Global Constraints

- Do not create `designing-game-difficulty` or `designing-combat-ai` Skill IDs.
- Preserve all existing Skill IDs and existing Skill Modes.
- Keep project-specific values and implementation state out of Base.
- Treat external references as evidence, not canonical project requirements.
- Do not claim Godot runtime, accessibility, performance, or player validation that was not executed.
- Apply difficulty changes to explicit variables and gates; never prescribe hidden real-time cheating as the default.

---

### Task 1: RED contract test

**Files:**
- Create: `tests/test_game_design_difficulty_workflow.py`

**Interfaces:**
- Consumes: Current Base routing, Skill, guide, registry, change and learning records.
- Produces: A failing structural contract for all new files, modes, triggers, routes, and required concepts.

- [x] **Step 1: Write the failing structural test**
- [x] **Step 2: Run the PR test suite and confirm failure is caused by missing reference/template/modes, not syntax**
- [x] **Step 3: Record the failing check in the draft PR**

### Task 2: Add the detailed design reference and project template

**Files:**
- Create: `skills/analyzing-and-refining-game-concepts/references/game-system-difficulty-and-combat-ai.md`
- Create: `templates/planning/GAME_SYSTEM_DIFFICULTY_AND_COMBAT_AI_CONTRACT.md`

**Interfaces:**
- Consumes: Player promise, core loop, target player, constraints, current enemy/combat rules, benchmark and playtest evidence.
- Produces: System boundaries, fairness rules, difficulty barrier profile, combat coordination model, pacing model, DDA policy, telemetry, playtest criteria, rollback, and Base/project classification.

- [x] **Step 1: Write the reference with `system-design` and `difficulty-and-combat-ai` procedures**
- [x] **Step 2: Define the three-layer AI boundary: individual decision, combat coordinator, pacing/difficulty director**
- [x] **Step 3: Define fixed and adaptive difficulty variables, hysteresis, cooldown, safe application timing, and anti-punishment rules**
- [x] **Step 4: Add telemetry, playtest, accessibility, performance, rollback, and promotion criteria**
- [x] **Step 5: Write the reusable project contract template with concrete fields and decision tables**

### Task 3: Extend the existing Skill and machine router

**Files:**
- Modify: `skills/analyzing-and-refining-game-concepts/SKILL.md`
- Modify: `skills/SKILL_REGISTRY.json`

**Interfaces:**
- Consumes: The new reference and template.
- Produces: Discoverable Skill Modes and automatic triggers without a new Skill ID.

- [x] **Step 1: Add `system-design` and `difficulty-and-combat-ai` to the mode sequence**
- [x] **Step 2: Add required inputs, workflow steps, output contract fields, and quality gates**
- [x] **Step 3: Add reference loading conditions**
- [x] **Step 4: Add registry triggers for system design, difficulty, combat AI, attack/threat budget, tension pacing, and DDA**
- [x] **Step 5: Add review triggers for unfair information, success punishment, oscillation, invisible adjustment, and missing evidence**

### Task 4: Synchronize human routing and knowledge guidance

**Files:**
- Modify: `START_HERE.md`
- Modify: `docs/DOCUMENTATION_MAP.md`
- Modify: `docs/knowledge/game-development/GAME_DESIGN_AND_PLAYER_EXPERIENCE_GUIDE.md`

**Interfaces:**
- Consumes: The Skill and template paths.
- Produces: Cold-start discovery and a conceptual guide that points to the executable contract.

- [x] **Step 1: Add route text and mode sequence to START_HERE**
- [x] **Step 2: Add the task, reference, and template row to Documentation Map**
- [x] **Step 3: Expand the guide with system boundary, fairness, attack budget, tension curve, fixed/adaptive difficulty, and anti-punishment guidance**
- [x] **Step 4: Preserve the distinction between guide knowledge and Skill execution authority**

### Task 5: Record learning and change state

**Files:**
- Modify: `docs/CHANGELOG.md`
- Modify: `skills/SKILL_LEARNING_LOG.md`

**Interfaces:**
- Consumes: Implemented structure and test evidence.
- Produces: Base change history and a non-overgeneralized learning state.

- [x] **Step 1: Record that the existing Skill was extended and no new independent Skill was added**
- [x] **Step 2: Record project Pilot validation as pending**
- [x] **Step 3: State that initial values remain project-specific and one success does not become a shared mandatory rule**

### Task 6: GREEN validation and reference-freshness review

**Files:**
- Test: `tests/test_game_design_difficulty_workflow.py`
- Test: `tests/test_evidence_based_game_development_knowledge.py`
- Review: all files changed in Tasks 2–5

**Interfaces:**
- Consumes: Complete branch diff.
- Produces: Passing structural tests, reference freshness decision, and a verified draft PR.

- [ ] **Step 1: Run relevant PR checks**
- [ ] **Step 2: Confirm new test passes and existing evidence-based knowledge test remains green**
- [ ] **Step 3: Search for duplicate Skill IDs and stale routes**
- [ ] **Step 4: Verify JSON parsing and Markdown path existence**
- [ ] **Step 5: Update the PR body with actual checks, unverified items, risks, and rollback**

### Task 7: Final review gate

**Files:**
- Review: PR diff and GitHub Actions evidence

**Interfaces:**
- Consumes: GREEN branch and checks.
- Produces: Draft PR ready for user review; no merge without explicit user approval.

- [ ] **Step 1: Perform adversarial review for overlap, over-prescription, inaccessible difficulty, and success-punishment risks**
- [ ] **Step 2: Apply only contract-preserving corrections**
- [ ] **Step 3: Re-run checks after the final change**
- [ ] **Step 4: Report Work Mode, Skill, Skill Mode, evidence, unverified items, and next project rollout step**
