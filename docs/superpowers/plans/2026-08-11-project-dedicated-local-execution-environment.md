# Project-Dedicated Local Execution Environment Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Strengthen Base's existing one-shot local executor bootstrap so every local handoff assumes a fresh shell, requires a project-dedicated execution environment first, creates/repairs that environment before product work when absent, and preserves project-adopted live-QA as non-authoring.

**Architecture:** Extend the existing `ONE_SHOT_LOCAL_EXECUTOR_BOOTSTRAP` owner rather than creating a second Skill. The shared GPT/Codex policy remains project-neutral. The existing Godot template may name generic Hera because it already owns Hera's shared live-QA boundary, but GRIMOIRE-specific Godot paths, ports, CODEX_HOME, Hera exact project version/profile/token/port, branch, and worktree values stay downstream project canon.

**Tech Stack:** Markdown operating policy, Python `unittest` contract tests, GitHub Actions existing one-shot bootstrap workflow.

## Global Constraints

- `PROJECT_DEDICATED_LOCAL_EXECUTION_ENVIRONMENT_FIRST` is the new shared invariant.
- `ASSUME_PREVIOUS_POWERSHELL_CLOSED` is mandatory for user-executed local handoffs.
- `CREATE_OR_REPAIR_DEDICATED_LOCAL_ENVIRONMENT_FIRST` precedes product implementation when required local components are absent.
- The user receives one self-contained copy/paste PowerShell launcher before any Codex task prompt.
- Base shared policy/template must not contain GRIMOIRE-specific path, port, CODEX_HOME, branch/worktree, Hera exact project version/profile/token/port literals.
- Generic Hera ownership already present in the Godot template remains allowed and must stay `LIVE_QA_AND_OBSERVABILITY_ONLY` / non-authoring.
- HiGodot sole persistent Godot authoring authority must not be weakened.
- Bootstrap must not reset/restore/clean/stage/rewrite user work or kill unrelated processes.
- Broad Git diff/line-ending/stat dumps are not startup prerequisites.

---

### Task 1: Extend the focused bootstrap contract test

**Files:**
- Modify: `tests/test_one_shot_local_executor_bootstrap_contract.py`

**Interfaces:**
- Consumes: existing Base policy and Godot template text.
- Produces: focused RED assertions for the new dedicated-environment invariant.

- [x] **Step 1: Write failing assertions**

Require:

```text
PROJECT_DEDICATED_LOCAL_EXECUTION_ENVIRONMENT_FIRST
ASSUME_PREVIOUS_POWERSHELL_CLOSED
CREATE_OR_REPAIR_DEDICATED_LOCAL_ENVIRONMENT_FIRST
live-QA
non-authoring
adversarial
```

Keep generic `Hera` + `LIVE_QA_AND_OBSERVABILITY_ONLY` in the existing Godot template, while rejecting GRIMOIRE-specific literals such as concrete project ports, `.codex-grimoire`, Task8 worktree names, or `Hera 1.0.0`.

- [x] **Step 2: Observe RED on the branch**

Draft PR #288 at head `059f5fdc4282a1ac6b726f6af89284e55e929a28` ran `Validate One-Shot Local Executor Bootstrap` and failed before shared policy/template implementation.

- [x] **Step 3: Record exact RED evidence**

The focused workflow failure is the required pre-production RED. No policy/template implementation existed on that exact test head.

---

### Task 2: Extend the shared GPT/Codex workflow policy

**Files:**
- Modify: `docs/GPT_CODEX_WORKFLOW_POLICY.md`
- Test: `tests/test_one_shot_local_executor_bootstrap_contract.py`

**Interfaces:**
- Consumes: `ONE_SHOT_LOCAL_EXECUTOR_BOOTSTRAP`, `BOOTSTRAP_MINIMUM_PREFLIGHT_ONLY`.
- Produces: shared dedicated-environment-first local handoff contract.

- [x] **Step 1: Implement minimum policy text**

Add the three new shared tokens and require:

```text
fresh user shell
→ exact approved project/worktree
→ dedicated editor/runtime + live-authority service + executor profile
→ optional adopted live-QA profile when required
→ create/repair missing components before product work
→ adversarial launcher validation
→ one complete launcher before Codex prompt
→ fresh project-authorized readiness evidence inside Codex
```

- [x] **Step 2: Preserve fail-closed boundaries**

Retain no reset/restore/clean/stage/rewrite, no unrelated process kill, no process/port readiness promotion, and no broad prelaunch Git/noise dump.

---

### Task 3: Extend the Godot live-editor operations template

**Files:**
- Modify: `templates/project-operations/.agents/skills/godot-live-editor-operations/SKILL.md`
- Test: `tests/test_one_shot_local_executor_bootstrap_contract.py`

**Interfaces:**
- Consumes: Base shared dedicated-environment policy and existing generic Hera live-QA authority.
- Produces: Godot-specific generic bootstrap ordering without consuming-project literals.

- [x] **Step 1: Implement the Godot bootstrap sequence**

Require fresh PowerShell → verify/create-or-repair self-contained Godot → exact matching editor → project-scoped HiGodot → project-scoped executor profile/CODEX_HOME → adopted Hera/live-QA profile if required → exact-worktree Codex → fresh HiGodot receipt.

- [x] **Step 2: Add adversarial launcher checks**

Cover wrong target, other-project editor/HiGodot/live-QA profile, port/profile collision, global executor leakage, fresh-shell loss, quoting, process-not-readiness, destructive Git commands, unrelated kills, and noisy broad diagnostics.

- [x] **Step 3: Preserve generic Hera ownership without project leakage**

Generic Hera may remain in the shared Godot template because it is an existing Base owner. Do not add GRIMOIRE-specific exact version/profile/token/port/path/worktree values.

---

### Task 4: Verify Base exact-head acceptance

**Files:**
- No new product files.

- [ ] Wait for exact-head success of all applicable workflows, including `Validate One-Shot Local Executor Bootstrap`, `Validate Base v9 Operating Contracts`, `Validate Game Project Operating System`, and `Dependency Review` when emitted.
- [ ] Adversarially attack parallel owner creation, project-literal leakage, Hera authoring escalation, ambiguous fresh-shell semantics, missing create/repair-first behavior, Codex-before-launcher ordering, destructive Git/process side effects, and process/port readiness inference.
- [ ] Recheck same-goal open/recent PRs and untouched Base consumers/adapters.
- [ ] Mark PR ready and merge only through normal required checks; do not bypass branch protection.
- [ ] Read merged `main` back and verify the three shared tokens plus project-neutral/non-authoring live-QA boundary.

---

### Task 5: Downstream GRIMOIRE consumer sync

**Files (GRIMOIRE separate branch):**
- Modify: `docs/DEVELOPMENT_GATES.md`
- Modify: `docs/planning/CURRENT_CONFIRMED_DECISIONS.md`
- Create: `docs/planning/sync/GR-SYNC-20260811-20-PROJECT-DEDICATED-LOCAL-ENVIRONMENT.md`
- Update another current-state owner only if fresh search proves it consumes the same tool-authority state.

- [ ] Fresh-read GRIMOIRE main/open PRs/Sheet immediately before write and confirm Sync20 collision-free.
- [ ] Under `GM-GODOT-AUTHORING-GUT-TEST-AUTHORITY-01`, document fresh PowerShell → self-contained GRIMOIRE Godot 4.7.1 → project HiGodot 3.1.4 profile/ports → project CODEX_HOME → Hera 1.0.0 exact pair when required → Codex exact worktree → fresh godot-ai receipt → Hera `LIVE_QA_AND_OBSERVABILITY_ONLY` → `HERA_SOURCE_DELTA: NONE`.
- [ ] Do not claim fixed current ports/token values without a fresh project authority read.
- [ ] Explicitly route missing dedicated components to environment creation/repair before product work.
- [ ] Preserve Task8 factual state; this docs-only sync does not mark Task8 merged/complete and does not mutate protected Godot source.
- [ ] PR / exact-head CI / merge / merged-main readback.

---

### Task 6: Google Sheet same-Decision synchronization

- [ ] Fresh-read target cells immediately before write.
- [ ] Update the `GM-GODOT-AUTHORING-GUT-TEST-AUTHORITY-01` row and current hub fields with only merged/readback facts, same Sync20 ID, current Base observed SHA, and Hera non-authoring role.
- [ ] Do not promote Task8 beyond merged-main evidence.
- [ ] Read back all written cells and confirm GitHub/Sheet Decision ID + Sync ID agreement.

---

### Task 7: Post-change monitor loop

- [ ] Attack old-shell assumptions, cross-project tool reuse, live-QA isolation omissions, Codex-before-bootstrap ordering, and authority escalation.
- [ ] Validate critique, recheck same-goal open/recent PRs, and inspect untouched derivatives/adapters.
- [ ] Classify exactly `OMISSION | CONFLICT | COMPLEMENT_GAP | DUPLICATE_WORK | NO_MATERIAL_FOLLOWUP`.
- [ ] Apply only validated minimal follow-up, rerun regressions/exact-head validation, and re-read merged canon/Sheet.
