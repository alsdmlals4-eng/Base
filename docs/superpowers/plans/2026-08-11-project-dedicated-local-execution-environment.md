# Project-Dedicated Local Execution Environment Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Strengthen Base's existing one-shot local executor bootstrap so every local handoff assumes a fresh shell, requires a project-dedicated execution environment first, creates/repairs that environment before product work when absent, and preserves any project-adopted live-QA tool as non-authoring.

**Architecture:** Extend the existing `ONE_SHOT_LOCAL_EXECUTOR_BOOTSTRAP` owner rather than creating a second Skill. The shared policy remains project-neutral; the Godot template specifies self-contained editor + project-scoped HiGodot + project-scoped executor profile + optional adopted live-QA slot. GRIMOIRE-specific Godot paths, ports, CODEX_HOME, Hera version/token/profile remain downstream project canon.

**Tech Stack:** Markdown operating policy, Python `unittest` contract tests, GitHub Actions existing one-shot bootstrap workflow.

## Global Constraints

- `PROJECT_DEDICATED_LOCAL_EXECUTION_ENVIRONMENT_FIRST` is the new shared invariant.
- `ASSUME_PREVIOUS_POWERSHELL_CLOSED` is mandatory for user-executed local handoffs.
- `CREATE_OR_REPAIR_DEDICATED_LOCAL_ENVIRONMENT_FIRST` precedes product implementation when required local components are absent.
- The user receives one self-contained copy/paste PowerShell launcher before any Codex task prompt.
- Base must not contain GRIMOIRE-specific path, port, version, CODEX_HOME, branch/worktree, Hera product, token, or profile literals.
- Project-adopted live-QA remains non-authoring unless a separate project authority decision changes that boundary.
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

- [ ] **Step 1: Write failing assertions**

Add a test equivalent to:

```python
def test_project_dedicated_local_environment_is_required_before_local_work(self) -> None:
    policy = (ROOT / "docs/GPT_CODEX_WORKFLOW_POLICY.md").read_text(encoding="utf-8")
    godot_template = (
        ROOT
        / "templates/project-operations/.agents/skills/godot-live-editor-operations/SKILL.md"
    ).read_text(encoding="utf-8")
    combined = policy + "\n" + godot_template

    for token in (
        "PROJECT_DEDICATED_LOCAL_EXECUTION_ENVIRONMENT_FIRST",
        "ASSUME_PREVIOUS_POWERSHELL_CLOSED",
        "CREATE_OR_REPAIR_DEDICATED_LOCAL_ENVIRONMENT_FIRST",
    ):
        self.assertIn(token, combined)

    self.assertIn("live-QA", combined)
    self.assertIn("non-authoring", combined)
    self.assertIn("adversarial", combined)
```

Extend the project-neutrality assertion so shared owner/template still reject literals including:

```python
"Hera",
"1.0.0",
"HERA_SOURCE_DELTA",
```

- [ ] **Step 2: Observe RED on the branch**

Open a draft PR after committing only the spec/plan/test changes. Let the existing `Validate One-Shot Local Executor Bootstrap` workflow execute the focused unittest. Expected result: failure because the new tokens are absent from the shared policy/template.

- [ ] **Step 3: Record exact RED evidence**

Capture exact PR head SHA, failing workflow/job, and assertion/token responsible for the failure. Do not implement production policy before this failure is observed.

---

### Task 2: Extend the shared GPT/Codex workflow policy

**Files:**
- Modify: `docs/GPT_CODEX_WORKFLOW_POLICY.md`
- Test: `tests/test_one_shot_local_executor_bootstrap_contract.py`

**Interfaces:**
- Consumes: `ONE_SHOT_LOCAL_EXECUTOR_BOOTSTRAP`, `BOOTSTRAP_MINIMUM_PREFLIGHT_ONLY`.
- Produces: shared dedicated-environment-first local handoff contract.

- [ ] **Step 1: Implement the minimum policy text**

Under the existing one-shot section, add:

```text
PROJECT_DEDICATED_LOCAL_EXECUTION_ENVIRONMENT_FIRST
ASSUME_PREVIOUS_POWERSHELL_CLOSED
CREATE_OR_REPAIR_DEDICATED_LOCAL_ENVIRONMENT_FIRST
```

Define the sequence:

```text
fresh user shell
→ resolve exact approved project/worktree
→ verify dedicated project-local editor/runtime + live-authority service + executor profile
→ verify adopted project live-QA profile when required
→ create/repair missing dedicated components before product work
→ adversarially validate launcher
→ provide one complete copy/paste block before the Codex prompt
→ Codex obtains fresh project-authorized readiness evidence
```

State that the live-QA slot is project-defined and non-authoring by default. Keep all project/tool literals out of the shared owner.

- [ ] **Step 2: Preserve fail-closed boundaries**

Explicitly retain:

```text
no reset/restore/clean/stage/rewrite
no unrelated process kill
no process/port == readiness promotion
no broad Git diff or known line-ending/stat noise startup dump
```

- [ ] **Step 3: Run focused GREEN via CI**

Expected `Validate One-Shot Local Executor Bootstrap`: success on the new exact head.

---

### Task 3: Extend the Godot live-editor operations template

**Files:**
- Modify: `templates/project-operations/.agents/skills/godot-live-editor-operations/SKILL.md`
- Test: `tests/test_one_shot_local_executor_bootstrap_contract.py`

**Interfaces:**
- Consumes: Base shared dedicated-environment policy.
- Produces: Godot-specific generic bootstrap ordering without project literals.

- [ ] **Step 1: Implement the Godot bootstrap sequence**

Extend the Bootstrap Gate with the generic order:

```text
ASSUME_PREVIOUS_POWERSHELL_CLOSED
→ verify/create-or-repair dedicated self-contained Godot
→ reuse/start exact matching editor
→ verify/start-or-attach exact project-scoped HiGodot profile/ports
→ inject project-scoped CODEX_HOME/executor profile
→ verify project-adopted live-QA profile when required
→ launch Codex in exact project/worktree
→ obtain fresh HiGodot project/session/version/readiness receipt
→ use live-QA only within its existing non-authoring authority
```

- [ ] **Step 2: Add adversarial launcher checks**

Cover wrong worktree/editor, duplicate editor, other-project HiGodot port ownership, project port collision, global executor-profile leakage, other-project live-QA profile/token/port, quoting/path-space failure, process-but-not-ready, destructive Git commands, unrelated process kill, and noisy broad prelaunch diagnostics.

- [ ] **Step 3: Keep Base project-neutral**

Do not mention GRIMOIRE, concrete ports, `.codex-grimoire`, Task8, Hera, Hera version, or `HERA_SOURCE_DELTA` in the shared template.

---

### Task 4: Verify Base exact-head acceptance

**Files:**
- No new product files.

**Interfaces:**
- Consumes: Tasks 1–3 exact head.
- Produces: merge-ready Base policy branch.

- [ ] **Step 1: Wait for exact-head workflows**

Require success for all applicable workflows, including:

```text
Validate One-Shot Local Executor Bootstrap
Validate Base v9 Operating Contracts
Validate Game Project Operating System
Dependency Review
```

- [ ] **Step 2: Adversarially review the PR**

Attack at minimum:

```text
parallel second bootstrap owner
project-specific literal leakage
live-QA promoted to source authoring
fresh-shell requirement ambiguous
missing create/repair-first behavior
Codex prompt appearing before launcher
reset/restore/clean or unrelated process kill authorization
readiness inferred from process/port existence
```

Classify `OMISSION | CONFLICT | COMPLEMENT_GAP | DUPLICATE_WORK | NO_MATERIAL_FOLLOWUP`.

- [ ] **Step 3: Recheck same-goal PRs and untouched consumers**

Confirm no competing open PR and inspect current Base project adapters/templates inheriting the policy.

- [ ] **Step 4: Merge only after exact-head success**

Use normal required-check/branch-protection flow. Do not bypass required checks.

- [ ] **Step 5: Merged-main readback**

Verify `main` contains the three shared tokens and the project-neutral live-QA boundary.

---

### Task 5: Downstream GRIMOIRE consumer sync

**Files (GRIMOIRE repository, separate branch):**
- Modify: `docs/DEVELOPMENT_GATES.md`
- Modify: `docs/planning/CURRENT_CONFIRMED_DECISIONS.md`
- Create: `docs/planning/sync/GR-SYNC-20260811-20-PROJECT-DEDICATED-LOCAL-ENVIRONMENT.md`
- Update other current-state consumer only if fresh search proves it is a live owner of the same tool-authority state.

**Interfaces:**
- Consumes: merged Base dedicated-environment invariant.
- Produces: GRIMOIRE-specific local bootstrap under `GM-GODOT-AUTHORING-GUT-TEST-AUTHORITY-01`.

- [ ] **Step 1: Fresh-read GRIMOIRE main/open PRs/Sheet before write**

Confirm no collision for `GR-SYNC-20260811-20-PROJECT-DEDICATED-LOCAL-ENVIRONMENT`.

- [ ] **Step 2: Record concrete GRIMOIRE sequence**

Document:

```text
new PowerShell every local work session
→ self-contained GRIMOIRE Godot 4.7.1
→ project-specific HiGodot 3.1.4 profile/ports
→ project CODEX_HOME
→ Hera 1.0.0 exact pair when live QA is required
→ Codex exact worktree
→ fresh godot-ai receipt
→ Hera LIVE_QA_AND_OBSERVABILITY_ONLY
→ HERA_SOURCE_DELTA: NONE
```

Do not claim fixed HiGodot ports or Hera token/port values unless fresh current project authority provides them.

- [ ] **Step 3: Explicit absence rule**

If any dedicated component is missing, create/repair the dedicated environment first; do not send a product prompt that assumes it exists.

- [ ] **Step 4: Preserve Task8 factual state**

This operating-policy sync does not itself mark Task8 merged/complete and does not mutate `.gd/.tscn/.tres/.res/project.godot`.

- [ ] **Step 5: PR / CI / merge / merged-main readback**

Use the project's normal exact-head gates.

---

### Task 6: Google Sheet same-Decision synchronization

**Files:**
- Google Sheet `02_현재_확정결정` row(s) for `GM-GODOT-AUTHORING-GUT-TEST-AUTHORITY-01`
- Google Sheet `00_프로젝트_허브` current operating-state fields where stale
- Google Sheet `99_변경이력` new Sync20 row if that sheet's current schema uses one-row-per-sync logging

**Interfaces:**
- Consumes: merged GRIMOIRE main readback.
- Produces: same Decision ID and Sync20 state across GitHub + Sheet.

- [ ] **Step 1: Fresh-read target cells immediately before write**

Do not overwrite concurrent Sheet edits.

- [ ] **Step 2: Write only verified facts**

Record the dedicated local environment policy and Hera non-authoring role. Update stale Base observed SHA to the then-current Base main. Do not promote Task8 beyond merged-main evidence.

- [ ] **Step 3: Read back all written cells**

Require same Decision ID and Sync20 identifier on the intended project tool-authority surface.

---

### Task 7: Post-change monitor loop

**Files:**
- No new file unless a validated follow-up requires one.

**Interfaces:**
- Consumes: merged Base + merged GRIMOIRE + Sheet readback.
- Produces: final operating-flow closure.

- [ ] **Step 1: Attack**

Try to prove a launcher can still assume an old shell, silently use another project's toolchain, omit live-QA isolation, or place the Codex prompt before bootstrap.

- [ ] **Step 2: Validate critique and recheck consumers**

Recheck same-goal open/recent PRs and untouched derivative/adapters.

- [ ] **Step 3: Classify**

Use exactly:

```text
OMISSION
CONFLICT
COMPLEMENT_GAP
DUPLICATE_WORK
NO_MATERIAL_FOLLOWUP
```

- [ ] **Step 4: Minimal follow-up only if validated**

Then rerun applicable regressions, exact-head/readback, and post-merge PR/canon recheck.
