# One-Shot Local Executor Bootstrap Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a reusable Base contract that prefers one copy/paste local launcher for shell + exact Godot editor + exact Codex working directory, then bind GRIMOIRE to the shared rule without weakening HiGodot authoring authority.

**Architecture:** Extend the existing GPT/Codex handoff policy and installed-project Godot operations template rather than creating a new Skill. Base owns only the generic startup invariant; GRIMOIRE owns concrete Windows paths, CODEX_HOME, worktree identity, and same-Decision-ID Sheet synchronization.

**Tech Stack:** Markdown policy, Python `unittest`, GitHub branch/PR workflow, Google Sheets authority sync, Windows PowerShell consumer example, existing Base/GRIMOIRE post-change adversarial gate.

## Global Constraints

- Shared contract token: `ONE_SHOT_LOCAL_EXECUTOR_BOOTSTRAP`.
- Base MUST NOT hard-code GRIMOIRE paths, ports, versions, CODEX_HOME, branches, or worktree names.
- Bootstrap orchestration MUST NOT become a second persistent Godot authoring authority.
- Projects declaring HiGodot as sole persistent authoring authority keep that authority unchanged.
- Bootstrap preflight is `BOOTSTRAP_MINIMUM_PREFLIGHT_ONLY`; avoid broad/noisy pre-Codex diagnostics.
- Bootstrap MUST NOT reset/restore/clean/stage/rewrite worktree state.
- Existing matching editor/process may be reused; unrelated editors/processes must not be killed.
- Runtime/session/readiness evidence is obtained after launch through the project-authorized live tool; process launch alone is not readiness evidence.
- GRIMOIRE binding uses existing Decision ID `GM-GODOT-AUTHORING-GUT-TEST-AUTHORITY-01`.
- GRIMOIRE sync ID reserved after fresh search: `GR-SYNC-20260811-20-ONE-SHOT-LOCAL-EXECUTOR-BOOTSTRAP`.
- No Task8 `.gd/.tscn/.tres/.res/project.godot` files are part of this operating-policy work unit.

---

### Task 1: RED Base Contract

**Files:**
- Modify: `tests/test_gpt_codex_workflow_contract.py`

**Interfaces:**
- Consumes: `docs/GPT_CODEX_WORKFLOW_POLICY.md`
- Consumes: `templates/project-operations/.agents/skills/godot-live-editor-operations/SKILL.md`
- Produces: a failing contract proving the new shared token and guardrails are absent before implementation.

- [ ] **Step 1: Add the focused failing test**

Append this test to `GptCodexWorkflowContractTests`:

```python
def test_one_shot_local_executor_bootstrap_is_shared_and_fail_closed(self) -> None:
    policy = (ROOT / "docs/GPT_CODEX_WORKFLOW_POLICY.md").read_text(encoding="utf-8")
    godot_template = (
        ROOT
        / "templates/project-operations/.agents/skills/godot-live-editor-operations/SKILL.md"
    ).read_text(encoding="utf-8")

    for text in (policy, godot_template):
        self.assertIn("ONE_SHOT_LOCAL_EXECUTOR_BOOTSTRAP", text)
        self.assertIn("BOOTSTRAP_MINIMUM_PREFLIGHT_ONLY", text)
        self.assertIn("reset", text)
        self.assertIn("restore", text)
        self.assertIn("clean", text)

    self.assertIn("one copy/paste", policy)
    self.assertIn("exact project/worktree", policy)
    self.assertIn("matching editor", godot_template)
    self.assertIn("fresh", godot_template)
    self.assertIn("HiGodot", godot_template)

    forbidden_project_literals = (
        "GRIMOIRE-",
        "8001",
        "9501",
        ".codex-grimoire",
        "task8-spell-use-screen-v2",
    )
    for literal in forbidden_project_literals:
        self.assertNotIn(literal, policy)
        self.assertNotIn(literal, godot_template)
```

- [ ] **Step 2: Run the focused test and observe RED**

Run:

```bash
python -m unittest tests.test_gpt_codex_workflow_contract.GptCodexWorkflowContractTests.test_one_shot_local_executor_bootstrap_is_shared_and_fail_closed -v
```

Expected: FAIL because `ONE_SHOT_LOCAL_EXECUTOR_BOOTSTRAP` is not yet present in the current policy/template.

- [ ] **Step 3: Commit RED**

```bash
git add tests/test_gpt_codex_workflow_contract.py
git commit -m "test: require one-shot local executor bootstrap"
```

---

### Task 2: Base Shared Policy GREEN

**Files:**
- Modify: `docs/GPT_CODEX_WORKFLOW_POLICY.md`
- Modify: `templates/project-operations/.agents/skills/godot-live-editor-operations/SKILL.md`
- Test: `tests/test_gpt_codex_workflow_contract.py`

**Interfaces:**
- Produces shared token: `ONE_SHOT_LOCAL_EXECUTOR_BOOTSTRAP`
- Produces guardrail token: `BOOTSTRAP_MINIMUM_PREFLIGHT_ONLY`
- Produces startup sequence: exact target resolve → matching editor reuse/start → minimum preflight → Codex exact working directory → fresh live receipt before mutation.

- [ ] **Step 1: Extend `docs/GPT_CODEX_WORKFLOW_POLICY.md`**

Add a subsection under the executor/handoff policy with these exact semantics:

```markdown
### ONE_SHOT_LOCAL_EXECUTOR_BOOTSTRAP

When a local executor handoff requires the user to start a shell, an engine/editor,
and Codex, prefer one copy/paste launcher block instead of three independent manual
startup steps.

`BOOTSTRAP_MINIMUM_PREFLIGHT_ONLY`:

```text
resolve exact approved project/worktree inputs
→ reuse exact matching editor when already running
→ otherwise start the required editor
→ perform only minimum startup checks needed to avoid the wrong target
→ launch Codex in the exact project/worktree
→ obtain fresh project-authorized runtime/session/readiness evidence inside Codex
  before persistent mutation
```

The launcher is orchestration, not readiness evidence. Do not front-load broad Git
diffs, repository scans, known line-ending/stat noise, or long diagnostics merely to
open Codex. Do not reset, restore, clean, stage, or rewrite user work as part of
bootstrap. Do not kill unrelated editors/servers. Project-specific paths, ports,
versions, host profiles, and worktree names remain project-local inputs.
```

- [ ] **Step 2: Extend the Godot installed-project template**

Add a `ONE_SHOT_LOCAL_EXECUTOR_BOOTSTRAP` paragraph to the `bootstrap` mode in `templates/project-operations/.agents/skills/godot-live-editor-operations/SKILL.md`:

```markdown
When the user must launch the local toolchain manually, prefer one copy/paste
bootstrap block: exact project/worktree identity → matching Godot editor reuse-or-start
→ `BOOTSTRAP_MINIMUM_PREFLIGHT_ONLY` → Codex launch in the exact project/worktree.
The block must not make persistent Godot edits itself. After Codex starts, obtain a
fresh HiGodot project/session/version/readiness receipt before any persistent mutation.
Do not reset/restore/clean user work or kill unrelated editor/server processes merely
to satisfy bootstrap.
```

- [ ] **Step 3: Run focused GREEN**

Run:

```bash
python -m unittest tests.test_gpt_codex_workflow_contract.GptCodexWorkflowContractTests.test_one_shot_local_executor_bootstrap_is_shared_and_fail_closed -v
```

Expected: PASS.

- [ ] **Step 4: Run the full GPT/Codex contract suite**

Run:

```bash
python -m unittest tests.test_gpt_codex_workflow_contract -v
```

Expected: all tests PASS.

- [ ] **Step 5: Run Base operating-contract validation**

Run the repository's current Base v9 operating-contract suite and generated-artifact checks exactly as defined by current `main`; do not weaken or skip Required Check topology.

- [ ] **Step 6: Commit GREEN**

```bash
git add docs/GPT_CODEX_WORKFLOW_POLICY.md templates/project-operations/.agents/skills/godot-live-editor-operations/SKILL.md
git commit -m "docs: add one-shot local executor bootstrap"
```

---

### Task 3: GRIMOIRE Concrete Consumer

**Files:**
- Create: `docs/planning/sync/GR-SYNC-20260811-20-ONE-SHOT-LOCAL-EXECUTOR-BOOTSTRAP.md`
- Modify: `docs/DEVELOPMENT_GATES.md`
- Modify: `docs/planning/CURRENT_CONFIRMED_DECISIONS.md`
- Test: existing planning/current-state contract tests selected by current repository conventions.

**Interfaces:**
- Consumes Base shared `ONE_SHOT_LOCAL_EXECUTOR_BOOTSTRAP`.
- Produces GRIMOIRE-specific convention under `GM-GODOT-AUTHORING-GUT-TEST-AUTHORITY-01`.

- [ ] **Step 1: Fresh-read GRIMOIRE authority immediately before writing**

Recheck:

```text
Base latest main
GRIMOIRE default branch/latest main/open PRs
Google Sheet 00_프로젝트_허브
GM-GODOT-AUTHORING-GUT-TEST-AUTHORITY-01 current rows
GR-SYNC-20260811-20 exact string remains unused
```

If Sync20 has appeared, stop and select the next unused sequential Sync ID before writing.

- [ ] **Step 2: Add the sync record**

Record:

```yaml
decision_id: GM-GODOT-AUTHORING-GUT-TEST-AUTHORITY-01
sync_id: GR-SYNC-20260811-20-ONE-SHOT-LOCAL-EXECUTOR-BOOTSTRAP
change_type: OPERATING_FLOW_COMPLEMENT
product_decision_change: false
shared_base_owner: ONE_SHOT_LOCAL_EXECUTOR_BOOTSTRAP
project_shell: Windows PowerShell
project_bootstrap_contract:
  - one copy/paste PowerShell block
  - exact requested GRIMOIRE worktree
  - exact matching Godot editor reuse-or-start
  - GRIMOIRE CODEX_HOME
  - Codex `-C <exact worktree>`
  - requested sandbox mode
  - fresh godot-ai receipt before persistent mutation
noise_guard:
  - no broad pre-Codex git diff/stat dump solely for known LF/CRLF/index noise
  - no reset/restore/clean during bootstrap
```

Do not hard-code Task8 V2 as the only future worktree; concrete execution packets supply the active worktree.

- [ ] **Step 3: Update current GRIMOIRE consumers**

In `docs/DEVELOPMENT_GATES.md` and `docs/planning/CURRENT_CONFIRMED_DECISIONS.md`, add the same Decision/Sync and the concise invariant:

```text
PowerShell launcher → exact Godot worktree reuse/start → exact CODEX_HOME/Codex -C → fresh HiGodot receipt
```

Preserve:

```text
SOLE_PERSISTENT_GODOT_AUTHORING_AUTHORITY = HiGodot
GUT = deterministic test authority
Hera = live QA/observability only
```

- [ ] **Step 4: Run focused/current planning contracts**

Run the repository tests that validate `DEVELOPMENT_GATES.md`, `CURRENT_CONFIRMED_DECISIONS.md`, sync uniqueness, and Godot authoring authority. Expected: PASS with no evidence promotion to human/device/performance/export/full-slice.

- [ ] **Step 5: Commit and open GRIMOIRE PR**

Use a docs-only branch based on the freshly re-read `main`. No Task8 product source belongs in this PR.

---

### Task 4: Same-Decision-ID Sheet Sync

**Files:**
- Google Sheet: `GRIMOIRE: 세계를 다시 쓰는 법`

**Interfaces:**
- Consumes merged/readback GRIMOIRE docs state from Task 3.
- Produces Sheet current-state text using existing Decision ID `GM-GODOT-AUTHORING-GUT-TEST-AUTHORITY-01` and Sync20.

- [ ] **Step 1: Fresh-read target cells/decision row immediately before write**

Read:

```text
00_프로젝트_허브!A1:K2
02_현재_확정결정 row containing GM-GODOT-AUTHORING-GUT-TEST-AUTHORITY-01
99_변경이력 next append row
```

- [ ] **Step 2: Update only affected current consumers**

Record the one-shot bootstrap rule and fresh Base observation. Do not use this sync to claim Task8 product completion or to fabricate `expected_version/actual_version` fields that were not surfaced.

- [ ] **Step 3: Explicit Sheet readback**

Read back every written range and require exact Decision ID + Sync20 match.

Expected: `SHEET_WRITE_READBACK_PASS`.

---

### Task 5: Adversarial Validation, PR, Merge, and Post-Merge Readback

**Files:**
- No new owner files unless a validated omission is found.

**Interfaces:**
- Consumes Base and GRIMOIRE branch heads.
- Produces merged-main evidence and post-change classification.

- [ ] **Step 1: Attack the Base change**

Try to prove:

```text
project-specific literals leaked into Base
launcher is being treated as readiness evidence
bootstrap can reset/clean work
bootstrap kills unrelated editor/server
new duplicate Skill/owner was created
Godot authoring authority was weakened
broad/noisy git diagnostics remain mandatory before Codex startup
```

- [ ] **Step 2: Validate same-goal open/recent PRs and untouched consumers**

Recheck Base and GRIMOIRE same-goal PRs, `docs/WORK_MODE_AND_SKILL_ROUTING.md`, handoff references, Godot live-editor consumers, current planning consumers, and Sheet current state.

Classify follow-up as exactly one of:

```text
OMISSION
CONFLICT
COMPLEMENT_GAP
DUPLICATE_WORK
NO_MATERIAL_FOLLOWUP
```

- [ ] **Step 3: Run exact-head CI**

Require applicable Base/GRIMOIRE required checks at the exact reviewed heads. `NOT_RUN` or skipped evidence is not PASS.

- [ ] **Step 4: Merge only after all repository gates pass**

Use repository-approved merge mode; do not bypass required checks or unresolved threads.

- [ ] **Step 5: Post-merge main readback**

Re-read both merged default branches, recheck same-goal open PRs, and verify the Sheet points at merged/current authority rather than branch-only state.

- [ ] **Step 6: Completion classification**

If no material follow-up remains, record `NO_MATERIAL_FOLLOWUP`. Do not create churn merely to satisfy the monitor loop.
