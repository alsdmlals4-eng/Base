# AI Bootstrap and Project Drift Hardening Implementation Plan

> **Status:** `COMPLETED_READBACK_VERIFIED` — 2026-08-22
>
> **For agentic workers:** This plan has been executed. Do not treat its checkboxes as future work. New regressions or new project drift require a new work contract.

**Goal:** Remove stale AI bootstrap from Base and verified affected projects, preserve frozen Sheet evidence, add automatic drift regression, and prove cold-start routing against actual Notion/repository authorities.

**Architecture:** Base owns stable dynamic bootstrap templates; current project planning authority is split between Notion and repository. Frozen historical artifacts remain immutable evidence, while current policies route legacy Sheets as migration-only compatibility. Projects keep their specific runtime/design constraints and receive only targeted authority/bootstrap corrections.

**Tech Stack:** Markdown, JSON, Python unittest, GitHub branch/PR/Actions, Notion readback

**Spec:** `docs/superpowers/specs/2026-08-22-ai-bootstrap-project-drift-hardening-design.md`

## Completion closeout

```text
Base PR #603
→ merged main 1786693b1ebb2e298e96ea3aa76f53a71e5f92b5
→ Codex/Copilot/project scaffold dynamic bootstrap
→ frozen Sheet history preserved
→ anti-drift regression active

Ten-Paces-Hidden-Moves PR #186
→ merged main 43a6e625c57c6f3e50b562e494fec074be553457
→ Notion/repository authority aligned
→ all 19 exact-head workflows success

Blacksmith PR #182
→ merged main aadecaf2694e1f1e5f708f2d6963a0d63f0dfb5f
→ Notion/repository authority aligned
→ exact-head project workflows success

Tetris PR #14
→ merged main 297a270f4a19e84bf8b58c596fd6bba9270201d2
→ stale permanent PR #9 protection removed
→ live PR state + DOMAIN_SPLIT_CANON
→ exact-head CI success

MylittleBoat PR #2
→ merged main 4e586bd28e2875973c5af3bae201125ebd080086
→ cold-start Notion/repository/Base bootstrap added
→ repository has no PR-triggered Actions workflow; diff/readback/mergeability/thread evidence used
```

Read-only/current classifications:

- `urban-legend`: `KEEP_COMPATIBILITY_ONLY`; active `AGENTS.md`/Documentation Map do not route through old copied AI instruction bodies.
- `Switchy-Express-Cargo-Puzzle`: `CURRENT`; Notion/repository split and migration-only Sheet route already present.
- `omenward`: `CURRENT` for this audit scope.
- `ninja-survival-godot`: `CURRENT` for authority routing; copied Base gate detail remains a future drift risk only if Base changes, not a current authority conflict.
- `Coc-Fiction`: `CURRENT`; legacy Sheets/Figma are not active authority.
- `GRIMOIRE-`: `READ_ONLY_PROTECTED`; pre-existing draft PR #151 remains untouched at head `c4ea5ca792f2b25f9759ac95756676338f6d8a67`.

Key adversarial corrections discovered during execution:

1. `docs/operations/SHEET_CONTROL_CONTRACT.json` looked stale but is frozen Base v9 historical evidence. It was restored exactly; current Sheet authority remains `docs/PROJECT_GDD_GOOGLE_SHEETS_POLICY.md`.
2. `managing-project-intake-and-work-contract` is a stable integrated project interface. Over-generalizing it away broke governance regression, so the scaffold preserves it while keeping other owner lookup dynamic.
3. Ten Paces `runtime_integration_pr: 65` is stable merged runtime evidence protected by project governance, not volatile open-PR state. It was restored after RED evidence.
4. urban-legend legacy AI documents contain historical/project-specific material; current routers already exclude them, so destructive rewrite was rejected.

## Global Constraints

- Work only from latest completed `main`; pre-existing open PRs are read-only.
- Never force-push, direct-push main, bypass rulesets, or absorb another workstream.
- `DOMAIN_SPLIT_CANON`: Notion human-facing; repository structured/runtime; Google Sheets migration compatibility only.
- Frozen release/history artifacts are not rewritten to look current.
- Preserve project-specific runtime/design constraints that do not conflict with current canon.
- Do not touch GRIMOIRE PR #151.
- Every write repo gets its own branch/PR, exact-HEAD verification, merge, and postmerge readback.

---

### Task 1: Align Base Codex and Copilot bootstrap

**Files:**
- Modify: `templates/custom-instructions.codex.md`
- Modify: `templates/copilot-instructions.md`

**Produces:** short dynamic authority bootstrap without fixed product roles or stale mandatory file lists.

- [x] Replace fixed `Codex = 구현 담당` identity with capability/permission-driven role selection.
- [x] Route Base work through current Base `AGENTS.md`/`START_HERE.md` and project work through project `AGENTS.md`/Active Context/domain canon.
- [x] Remove mandatory reads of deprecated fixed files; progressive-load current owner docs only.
- [x] Preserve user-change protection, scope control, evidence/reporting, and permission boundaries.
- [x] Read back both files and scan for stale literals.

### Task 2: Align project AGENTS scaffold and verify Sheet history/current policy split

**Files:**
- Modify: `templates/AGENTS.project.md`
- Read/verify unchanged frozen history: `docs/operations/SHEET_CONTROL_CONTRACT.json`
- Read/verify current owner: `docs/PROJECT_GDD_GOOGLE_SHEETS_POLICY.md`

**Produces:** new-project scaffold that cannot reintroduce Sheet-first or fixed local-copy authority while preserving v9 evidence.

- [x] Add `DOMAIN_SPLIT_CANON` block to project scaffold.
- [x] Replace fixed Base-local-copy file list with adopted-version + progressive owner lookup.
- [x] Add dynamic current open-PR protection rule without PR-number literals.
- [x] Preserve frozen v9 Sheet contract exactly (`schema_version=1`, `USER_FACING_GDD_WORKSPACE`, held `HOLD`).
- [x] Verify current Sheet policy remains `MIGRATION_ONLY_UNTIL_REMOVAL`, Notion-first, repository-runtime.

### Task 3: Add anti-drift regression and update guide

**Files:**
- Create: `tests/test_ai_bootstrap_drift_contract.py`
- Modify: `docs/CUSTOM_INSTRUCTIONS_GUIDE.md`

**Produces:** automatic detection of stale fixed-role, fixed-file, active Sheet-primary, historical rewrite and scaffold regressions.

- [x] Write unittest assertions for GPT/Codex/Copilot/project scaffold.
- [x] Assert frozen Sheet history and current migration-only policy as separate layers.
- [x] Update guide to mark Codex/Copilot audit completed and explain repository-wide vs path-specific/bootstrap responsibilities.
- [x] Ensure core-regression unittest discovery executes the new test.

### Task 4: Base adversarial validation and merge

- [x] Full loop 1: authority duplication/conflict.
- [x] Full loop 2: deprecated Sheet/HTML/fixed-file active routes.
- [x] Full loop 3: volatile PR/project-state leakage into templates.
- [x] Full loop 4: runtime/evidence claim boundary.
- [x] Full loop 5: cold-start from no chat memory.
- [x] Compare to latest main; reconcile if main advanced.
- [x] Update current-task PR; inspect exact diff, reviews, threads, workflow runs.
- [x] Merge exact verified head; postmerge readback.

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

- [x] For each repo, read latest `main`, open PRs, `AGENTS.md`, current Notion Project Home where relevant.
- [x] Classify each finding `CURRENT / STALE_AUTHORITY / STALE_VOLATILE_STATE / COMPATIBILITY_ONLY / BLOCKED_BY_OPEN_PR`.
- [x] Create one independent branch/PR per stale write repo; do not bulk-synchronize unrelated content. `urban-legend` was reclassified `KEEP_COMPATIBILITY_ONLY`, so no destructive PR was created.
- [x] Preserve unique project-specific constraints and only change the stale authority/bootstrap region.

### Task 6: Project adversarial validation and merge

For each write repo:

- [x] Full loop 1: project-specific authority regression.
- [x] Full loop 2: legacy route remains active.
- [x] Full loop 3: volatile state hard-coded.
- [x] Full loop 4: structured/runtime truth confused with Notion planning.
- [x] Full loop 5: new-chat cold-start finds current Project Home and repository truth.
- [x] Verify exact changed files, CI/checks when available, unresolved threads 0.
- [x] Reconcile latest main, exact-head merge, postmerge readback.

### Task 7: Final cross-project cold-start audit

- [x] Simulate Base-only request from no prior context.
- [x] Simulate project request for Ten-Paces, Blacksmith, MylittleBoat, and already-current Switchy Express.
- [x] Confirm routing reaches current Notion Project Home for human planning and repository for structured/runtime facts.
- [x] Confirm no active path in corrected/current routes requires Google Sheets, deprecated HTML dashboard, fixed old Base copies, or a closed PR number.
- [x] Report remaining compatibility-only/historical artifacts separately from active blockers.
