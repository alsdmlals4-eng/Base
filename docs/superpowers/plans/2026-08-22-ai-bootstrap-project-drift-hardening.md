# AI Bootstrap and Project Drift Hardening Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Remove stale AI bootstrap and Sheet authority from Base and verified affected projects, add automatic drift regression, and prove cold-start routing against actual Notion/repository authorities.

**Architecture:** Base owns stable dynamic bootstrap templates and migration compatibility rules; projects own their specific runtime/design constraints while routing human-facing planning to Notion and structured/runtime truth to repository. Legacy references are preserved only when needed for compatibility, never as competing active canon.

**Tech Stack:** Markdown, JSON, Python unittest, GitHub branch/PR/Actions, Notion readback

**Spec:** `docs/superpowers/specs/2026-08-22-ai-bootstrap-project-drift-hardening-design.md`

## Global Constraints

- Work only from latest completed `main`; pre-existing open PRs are read-only.
- Never force-push, direct-push main, bypass rulesets, or absorb another workstream.
- `DOMAIN_SPLIT_CANON`: Notion human-facing; repository structured/runtime; Google Sheets migration compatibility only.
- Preserve project-specific runtime/design constraints that do not conflict with current canon.
- Do not touch GRIMOIRE PR #151.
- Every write repo gets its own branch/PR, exact-HEAD verification, merge, and postmerge readback.

---

### Task 1: Align Base Codex and Copilot bootstrap

**Files:**
- Modify: `templates/custom-instructions.codex.md`
- Modify: `templates/copilot-instructions.md`

**Produces:** short dynamic authority bootstrap without fixed product roles or stale mandatory file lists.

- [ ] Replace fixed `Codex = 구현 담당` identity with capability/permission-driven role selection.
- [ ] Route Base work through current Base `AGENTS.md`/`START_HERE.md` and project work through project `AGENTS.md`/Active Context/domain canon.
- [ ] Remove mandatory reads of deprecated fixed files; progressive-load current owner docs only.
- [ ] Preserve user-change protection, scope control, evidence/reporting, and permission boundaries.
- [ ] Read back both files and scan for stale literals.

### Task 2: Align project AGENTS scaffold and Sheet machine contract

**Files:**
- Modify: `templates/AGENTS.project.md`
- Modify: `docs/operations/SHEET_CONTROL_CONTRACT.json`

**Produces:** new-project scaffold that cannot reintroduce Sheet-first or fixed local-copy authority.

- [ ] Add `DOMAIN_SPLIT_CANON` block to project scaffold.
- [ ] Replace fixed Base-local-copy file list with adopted-version + progressive owner lookup.
- [ ] Add dynamic current open-PR protection rule without PR-number literals.
- [ ] Convert Sheet contract to schema v2 `MIGRATION_ONLY_UNTIL_REMOVAL` compatibility contract while preserving held-project inventory.
- [ ] Read back JSON and validate parseability/authority values.

### Task 3: Add anti-drift regression and update guide

**Files:**
- Create: `tests/test_ai_bootstrap_drift_contract.py`
- Modify: `docs/CUSTOM_INSTRUCTIONS_GUIDE.md`

**Produces:** automatic detection of stale fixed-role, fixed-file, Sheet-primary and scaffold regressions.

- [ ] Write unittest assertions for GPT/Codex/Copilot/project scaffold/Sheet contract.
- [ ] Update guide to mark Codex/Copilot audit completed and explain repository-wide vs path-specific/bootstrap responsibilities.
- [ ] Ensure core-regression unittest discovery executes the new test.

### Task 4: Base adversarial validation and merge

- [ ] Full loop 1: authority duplication/conflict.
- [ ] Full loop 2: deprecated Sheet/HTML/fixed-file active routes.
- [ ] Full loop 3: volatile PR/project-state leakage into templates.
- [ ] Full loop 4: runtime/evidence claim boundary.
- [ ] Full loop 5: cold-start from no chat memory.
- [ ] Compare to latest main; reconcile if main advanced.
- [ ] Open Base PR; inspect exact diff, reviews, threads, workflow runs.
- [ ] Merge exact verified head; postmerge readback.

### Task 5: Project preflight and targeted corrections

**Repositories:**
- `Ten-Paces-Hidden-Moves`
- `Blacksmith`
- `Tetris`
- `MylittleBoat`
- `urban-legend`

**Read-only verification:**
- `Switchy-Express-Cargo-Puzzle`
- `omenward`
- `ninja-survival-godot`
- `Coc-Fiction`
- `GRIMOIRE-`

- [ ] For each repo, read latest `main`, open PRs, `AGENTS.md`, current Notion Project Home where relevant.
- [ ] Classify each finding `CURRENT / STALE_AUTHORITY / STALE_VOLATILE_STATE / COMPATIBILITY_ONLY / BLOCKED_BY_OPEN_PR`.
- [ ] Create one independent branch/PR per stale repo; do not bulk-synchronize unrelated content.
- [ ] Preserve unique project-specific constraints and only change the stale authority/bootstrap region.

### Task 6: Project adversarial validation and merge

For each write repo:

- [ ] Full loop 1: project-specific authority regression.
- [ ] Full loop 2: legacy route remains active.
- [ ] Full loop 3: volatile state hard-coded.
- [ ] Full loop 4: structured/runtime truth confused with Notion planning.
- [ ] Full loop 5: new-chat cold-start finds current Project Home and repository truth.
- [ ] Verify exact changed files, CI/checks when available, unresolved threads 0.
- [ ] Reconcile latest main, exact-head merge, postmerge readback.

### Task 7: Final cross-project cold-start audit

- [ ] Simulate Base-only request from no prior context.
- [ ] Simulate project request for at least Ten-Paces, Blacksmith, MylittleBoat, and one already-current repo.
- [ ] Confirm routing reaches current Notion Project Home for human planning and repository for structured/runtime facts.
- [ ] Confirm no active path requires Google Sheets, deprecated HTML dashboard, fixed old Base copies, or a closed PR number.
- [ ] Report remaining compatibility-only/historical artifacts separately from active blockers.
