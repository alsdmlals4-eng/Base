# Base Resilient Execution and Narrative Reference Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a fresh-shell one-block PowerShell contract, live private narrative-preference reference routing, continuous-work remaining-work closure, and reusable-lesson promotion routing without duplicating existing Base governance.

**Architecture:** Keep `AGENTS.md` and the long-horizon policy thin and route narrow responsibilities to existing owners. Add one operations contract for PowerShell because it has an independent user-input/failure boundary; extend the existing serial-fiction and continuous-work owners; route reusable learning through existing Base-change and Skill-evolution owners.

**Tech Stack:** Markdown policy/Skill contracts, Python `unittest`, GitHub Actions, connected Google Drive readback evidence.

**Spec:** `docs/superpowers/specs/2026-08-18-base-resilient-execution-narrative-reference-design.md`

## Global Constraints

- Preserve existing current Base content; no whole-file simplification that removes unrelated rules.
- Do not touch other chat/project branches or open PRs; start from completed current `main`.
- No new paid API/SaaS/credit/runner path. Current paid plans remain GPT Pro + Figma Pro only.
- Do not commit the private Google Doc URL, document ID, or copied prose.
- Do not create a new broad Skill unless the existing-owner design fails under evidence.
- Apply TDD: failing contract tests before production behavior changes.
- Perform at least five complete whole-scope adversarial improvement loops after implementation.

---

### Task 1: Contract tests for the missing behavior

**Files:**
- Modify: `tests/test_base_long_horizon_work_contract.py`
- Modify: `tests/test_serial_fiction_discipline.py`

**Interfaces:**
- Consumes: current long-horizon, continuous-work, serial-fiction entrypoints.
- Produces: failing assertions naming the required PowerShell, remaining-work, lesson-promotion, line-break, and private live-reference contracts.

- [ ] **Step 1: Add failing long-horizon tests**

Require a PowerShell owner contract with `FRESH_SHELL_ASSUMPTION`, `ONE_COPY_PASTE_BLOCK`, `LOCATION_FIRST`, `NO_PRIOR_SHELL_STATE_DEPENDENCY`, `FAIL_FAST`, `NATIVE_EXIT_CODE_REQUIRED`, `ERROR_STAGE_MARKER`, and `BEGINNER_SAFE_USER_ACTION`. Require discoverability from `AGENTS.md` / `START_HERE.md`. Require continuous work to recalculate `REQUIRED_WORK_REMAINING` postmerge and requeue in-scope work when nonzero. Require `REUSABLE_LESSON_PROMOTION_GATE` to route to `managing-base-change-proposals` and `evolving-project-discipline-skills`.

- [ ] **Step 2: Add failing serial-fiction tests**

Require `PARAGRAPH_BREAK_AND_BREATH`, `LINE_BREAK_RHYTHM`, `PARAGRAPH_LENGTH_PATTERN`, `DIALOGUE_NARRATION_ALTERNATION`, and `REACTION_ISOLATION` in the serial-fiction owner/guide. Require `BASE_OWNER_NARRATIVE_REFERENCE_POINTER.md` with `LIVE_CONNECTED_DRIVE_READ`, `USER_PREFERENCE_EVIDENCE`, and title `글따라쓰기`; forbid `docs.google.com/document/d/` and the raw document ID.

- [ ] **Step 3: Commit tests only and open a draft PR**

Expected exact-head GitHub Actions result: focused contract failures caused by the missing owner files/tokens, not unrelated existing behavior.

### Task 2: Fresh PowerShell execution owner

**Files:**
- Create: `docs/operations/POWERSHELL_FRESH_SHELL_EXECUTION_CONTRACT.md`
- Modify: `AGENTS.md`
- Modify: `docs/LONG_HORIZON_WORK_EXECUTION_POLICY.md`
- Modify: `START_HERE.md`
- Modify: `docs/DOCUMENTATION_MAP.md`

**Interfaces:**
- Consumes: user-facing terminal instruction requests.
- Produces: one-copy-paste fresh-shell contract and discoverable routing.

- [ ] **Step 1: Implement minimal contract**

The first executable phase sets error behavior and location explicitly, validates the expected workspace, checks commands before use, checks native exit codes, emits stage markers, and never depends on prior shell variables/functions/current directory.

- [ ] **Step 2: Add beginner-safe failure output requirements**

Errors identify the failed stage and current location and provide simple numbered remediation without exposing secrets. Multiple manual PowerShell blocks/windows are not the default.

- [ ] **Step 3: Wire thin entrypoint pointers**

Add only stable owner links/tokens to higher-level docs; do not duplicate the whole contract.

### Task 3: Narrative paragraph/breath and live preference evidence

**Files:**
- Create: `docs/knowledge/serial-fiction/BASE_OWNER_NARRATIVE_REFERENCE_POINTER.md`
- Modify: `docs/knowledge/serial-fiction/README.md`
- Modify: `docs/knowledge/serial-fiction/SERIAL_FICTION_WRITING_AND_REVISION_GUIDE.md`
- Modify: `skills/developing-and-revising-serial-fiction/SKILL.md`

**Interfaces:**
- Consumes: connected Drive source titled `글따라쓰기`, when accessible and relevant.
- Produces: structural preference evidence for paragraph breaks, breath, dialogue/narration alternation, reaction isolation, and beat spacing.

- [ ] **Step 1: Add private live-source pointer**

Store only role/title/resolution behavior, never URL/ID/content. The source is user preference evidence, not canon or a public benchmark.

- [ ] **Step 2: Add paragraph/breath craft contract**

Line breaks are pacing and attention decisions. Analyze distributions and transitions rather than enforcing fixed paragraph quotas. Preserve scene comprehension and mobile/read-aloud rhythm; avoid fragmentation for its own sake.

- [ ] **Step 3: Preserve originality boundary**

Extract structural patterns; never copy distinctive phrases or imitate an identifiable writer/work style.

### Task 4: Continuous closure and reusable lesson promotion

**Files:**
- Modify: `skills/managing-project-intake-and-work-contract/references/continuous-work-execution.md`
- Modify: `docs/LONG_HORIZON_WORK_EXECUTION_POLICY.md`

**Interfaces:**
- Consumes: merge/postmerge state plus incidents, fixes, repeated patterns, and reusable implementation results.
- Produces: remaining-work requeue and smallest-owner promotion decision.

- [ ] **Step 1: Extend postmerge closure**

After readback, compute `REQUIRED_WORK_REMAINING`. If greater than zero, derive only in-scope ready/deferred work and continue. Stop only on zero or a real global terminal blocker/user decision boundary.

- [ ] **Step 2: Add reusable lesson routing**

Use `REUSE_EXISTING_OWNER → EXTEND_REFERENCE_OR_MODE → EXTRACT_MODULE → BASE_CHANGE_PROPOSAL → NEW_SKILL_LAST`. Do not turn one success into a general rule.

### Task 5: GREEN, five full loops, merge, postmerge

**Files:**
- All changed files above; no unrelated paths.

**Interfaces:**
- Consumes: exact PR head and latest main.
- Produces: merged, read-back current contract with no blocking findings.

- [ ] **Step 1: Verify focused and related CI GREEN**

Inspect failures instead of weakening assertions to obtain a pass.

- [ ] **Step 2: Run full adversarial improvement loops 1-5**

Each loop re-reviews the full scope: intent, authority/routing, privacy/copyright, execution/failure recovery, Tool Hub/Loop Engineering boundaries, cost/security, content preservation, tests, long-term maintainability, and completion. Fix validated findings and reverify before the next loop.

- [ ] **Step 3: Reconcile latest main and review PR**

Confirm no unrelated open PR is modified, no content loss, unresolved review threads = 0, exact-head checks pass, and no stronger alternative emerged.

- [ ] **Step 4: Merge and postmerge readback**

Merge using the expected head SHA, read current main back, verify relevant postmerge workflows/evidence, promote/supersede lessons as appropriate, and report `REQUIRED_WORK_REMAINING` separately from external blockers and optional backlog.
