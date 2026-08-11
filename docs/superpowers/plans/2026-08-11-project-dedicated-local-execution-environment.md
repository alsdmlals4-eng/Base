# Project-Dedicated Local Execution Environment Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Strengthen Base's existing one-shot local executor bootstrap so every local handoff assumes a fresh shell, requires a project-dedicated execution environment first, creates/repairs that environment before product work when absent, and preserves project-adopted live-QA as non-authoring.

**Architecture:** Extend the existing `ONE_SHOT_LOCAL_EXECUTOR_BOOTSTRAP` owner rather than creating a second Skill. The shared GPT/Codex policy remains project-neutral. The existing Godot template may name generic Hera because it already owns Hera's shared live-QA boundary; consuming-project exact versions, paths, ports, executor homes, credentials, profiles, branches, and worktrees stay downstream project canon.

**Tech Stack:** Markdown operating policy, Python `unittest` contract tests, GitHub Actions existing one-shot bootstrap workflow.

## Global Constraints

- `PROJECT_DEDICATED_LOCAL_EXECUTION_ENVIRONMENT_FIRST` is the new shared invariant.
- `ASSUME_PREVIOUS_POWERSHELL_CLOSED` is mandatory for user-executed local handoffs.
- `CREATE_OR_REPAIR_DEDICATED_LOCAL_ENVIRONMENT_FIRST` precedes product implementation when required local components are absent.
- The user receives one self-contained copy/paste launcher before any Codex task prompt.
- Shared policy/template must not contain consuming-project exact path, port, executor-home, branch/worktree, live-QA version/profile/token literals.
- Generic Hera ownership already present in the Godot template remains `LIVE_QA_AND_OBSERVABILITY_ONLY` / non-authoring.
- HiGodot sole persistent Godot authoring authority must not be weakened.
- Bootstrap must not reset/restore/clean/stage/rewrite user work or kill unrelated processes.
- Broad Git diff/line-ending/stat dumps are not startup prerequisites.

---

### Task 1: Focused RED contract

**File:** `tests/test_one_shot_local_executor_bootstrap_contract.py`

- [x] Require `PROJECT_DEDICATED_LOCAL_EXECUTION_ENVIRONMENT_FIRST`, `ASSUME_PREVIOUS_POWERSHELL_CLOSED`, `CREATE_OR_REPAIR_DEDICATED_LOCAL_ENVIRONMENT_FIRST`, live-QA/non-authoring language, and adversarial launcher review.
- [x] Keep generic `Hera` + `LIVE_QA_AND_OBSERVABILITY_ONLY` in the existing Godot template while rejecting consuming-project concrete literals.
- [x] Observe RED before production: draft PR #288 test-only head `059f5fdc4282a1ac6b726f6af89284e55e929a28`; `Validate One-Shot Local Executor Bootstrap` failed before shared policy/template implementation.

---

### Task 2: Shared GPT/Codex policy GREEN

**File:** `docs/GPT_CODEX_WORKFLOW_POLICY.md`

- [x] Add the three new shared tokens.
- [x] Require fresh shell → exact project/worktree → dedicated editor/runtime + live-authority service + executor profile → optional adopted live-QA profile → create/repair missing components → adversarial launcher validation → one complete launcher before Codex prompt → fresh project-authorized readiness evidence inside Codex.
- [x] Preserve no reset/restore/clean/stage/rewrite, no unrelated process kill, no process/port readiness promotion, and no broad prelaunch Git/noise dump.

---

### Task 3: Godot template GREEN

**File:** `templates/project-operations/.agents/skills/godot-live-editor-operations/SKILL.md`

- [x] Require fresh PowerShell → verify/create-or-repair self-contained Godot → exact matching editor → project-scoped HiGodot → project-scoped executor profile/CODEX_HOME → adopted Hera/live-QA profile if required → exact-worktree Codex → fresh HiGodot receipt.
- [x] Add adversarial checks for wrong target, other-project editor/HiGodot/live-QA profile, port/profile collision, global executor leakage, fresh-shell loss, quoting, process-not-readiness, destructive Git commands, unrelated kills, and noisy broad diagnostics.
- [x] Preserve generic Hera ownership without consuming-project exact version/profile/token/port/path/worktree values.

---

### Task 4: Exact-head acceptance and merge

- [ ] Require exact-head success for all applicable workflows, including `Validate One-Shot Local Executor Bootstrap`, `Validate Base v9 Operating Contracts`, and `Validate Game Project Operating System`; require Dependency Review when emitted.
- [ ] Run adversarial review against parallel owner creation, consuming-project literal leakage, Hera authoring escalation, ambiguous fresh-shell semantics, missing create/repair-first behavior, Codex-before-launcher ordering, destructive Git/process side effects, and process/port readiness inference.
- [ ] Recheck same-goal open/recent PRs and untouched Base consumers/adapters.
- [ ] Merge only through normal required checks; do not bypass branch protection.
- [ ] Read merged `main` back and verify the three shared tokens plus project-neutral/non-authoring live-QA boundary.

## Downstream handoff

After merged-main readback, each consuming project performs its own separate canon/decision/sheet sync using project-owned concrete values. Those project-specific values are intentionally not part of this Base implementation plan.

## Post-change monitor loop

After implementation:

```text
attack
→ validate critique
→ same-goal open/recent PR recheck
→ untouched consumer/derivative recheck
→ classify OMISSION | CONFLICT | COMPLEMENT_GAP | DUPLICATE_WORK | NO_MATERIAL_FOLLOWUP
→ minimal follow-up if validated
→ regression recheck
→ exact-head validation
→ merge
→ merged-main readback
→ post-merge PR/canon recheck
```
