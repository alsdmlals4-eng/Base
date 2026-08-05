# Godot Multi-Project Pilot Program Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Execute Program A of the approved Godot production-adapter expansion by building one reusable Base Pilot runner, proving it in five real Godot projects without source product mutation, recording GRIMOIRE preproject readiness honestly, and integrating exact project evidence back into Base.

**Architecture:** The program is split into eight independently reviewable PRs. Base C0 owns the descriptor Schema, disposable-workspace runner, adapter injection, source-integrity proof, evidence format, and reusable workflow; each project PR owns only an immutable descriptor, adoption documentation, a local contract test, and a caller workflow; Base C1 consumes exact merged project evidence and decides whether Program B may begin. Existing product files and legacy Godot AI installations remain unchanged in source repositories.

**Tech Stack:** Python 3.12, JSON Schema Draft 2020-12, Godot 4.7.1 stable headless Editor, GDScript EditorPlugin APIs, GitHub Actions reusable workflows, SHA-256 evidence, Python `unittest`/`pytest`, existing Base v2 live-editor contract and transaction adapter.

## Global Constraints

- Governing design: `docs/superpowers/specs/2026-08-05-godot-multi-project-production-adapter-expansion-design.md`.
- Plan baseline Base main: `9bca3d7504fd48725715d4be27bfa8e266389223`.
- Base C0 implementation starts from the then-current Base `main`, never from this plan branch.
- Open hardening PR #166 must be merged or its four protections must be proven equivalent on then-current `main` before Base C0 production writes begin.
- Program A creates no MCP, HTTP, WebSocket, TCP, UDP, named-pipe, remote endpoint, background mutation thread, runtime debugger, arbitrary GDScript, shell, Expression, or arbitrary property path.
- Existing main Scenes are read-only. All mutation, Undo, save, ledger, and evidence actions occur only in a runner-created scratch Scene inside a disposable workspace.
- Source repositories retain their current `project.godot`, `addons/godot_ai/`, `_mcp_game_helper`, product Scenes, scripts, data, assets, saves, inputs, and export settings.
- Legacy Godot AI is disabled only in the disposable Pilot copy. A Pilot fails if both mutation authorities are active.
- Every caller pins the exact merged Base C0 commit SHA in `uses:`; floating `main`, mutable branch, and unverified fork references are forbidden.
- Project PRs are Draft-first, independently reviewable, and never auto-merged.
- Google Sheets are not changed because Program A changes no game-design Decision.
- `PRODUCTION_ADAPTER_READY` remains `NOT_READY` after Program A.
- Program B authenticated STDIO MCP and Program C runtime debugger require new designs and explicit approval after Base C1.

---

## Plan Set

| Order | PR | Repository | Plan |
|---|---|---|---|
| 1 | Base C0 | `alsdmlals4-eng/Base` | `2026-08-05-godot-multi-project-pilot-base-c0.md` |
| 2 | Clean Pilot | `alsdmlals4-eng/Switchy-Express-Cargo-Puzzle` | `2026-08-05-godot-pilot-switchy-express.md` |
| 3 | Legacy Pilot | `alsdmlals4-eng/Ten-Paces-Hidden-Moves` | `2026-08-05-godot-pilot-ten-paces.md` |
| 4 | Blocked-product Pilot | `alsdmlals4-eng/Blacksmith` | `2026-08-05-godot-pilot-blacksmith.md` |
| 5 | Planning-only Pilot | `alsdmlals4-eng/omenward` | `2026-08-05-godot-pilot-omenward.md` |
| 6 | Existing-autoload Pilot | `alsdmlals4-eng/urban-legend` | `2026-08-05-godot-pilot-urban-legend.md` |
| 7 | Preproject readiness | `alsdmlals4-eng/GRIMOIRE-` | `2026-08-05-godot-pilot-grimoire-readiness.md` |
| 8 | Base C1 | `alsdmlals4-eng/Base` | `2026-08-05-godot-multi-project-pilot-base-c1.md` |

## Dependency Graph

```text
approved design merged
        |
        v
Base C0 merged at immutable SHA
        |
        v
Switchy Express clean Pilot merged and runtime PASS
        |
        +---------------------+---------------------+---------------------+
        v                     v                     v                     v
Ten Paces Pilot       Blacksmith Pilot       OMENWARD Pilot       urban-legend Pilot
        \                     |                     |                     /
         \____________________|_____________________|____________________/
                              |
GRIMOIRE readiness -----------+
                              v
                    Base C1 evidence integration
                              v
                  Program B design decision only
```

The four legacy/project-policy Pilots may be developed in parallel only after Switchy Express proves the exact Base C0 workflow. They must pin the same Base C0 merged SHA unless a reviewed compatibility update is explicitly approved.

---

### Task 1: Freeze current authority and resolve the Base hardening prerequisite

**Files:**
- Read: `docs/knowledge/godot/GODOT_PRODUCTION_ADAPTER_READINESS.md`
- Read: `docs/superpowers/specs/2026-08-05-godot-multi-project-production-adapter-expansion-design.md`
- Inspect: Base PR #166
- Inspect: all six project `main` refs and open same-goal PRs

**Interfaces:**
- Consumes: approved design and current repository state.
- Produces: an execution ledger containing exact baseline SHAs, open dependency disposition, and allowed first PR.

- [ ] **Step 1: Re-read current Base and project refs**

```bash
git ls-remote https://github.com/alsdmlals4-eng/Base refs/heads/main
git ls-remote https://github.com/alsdmlals4-eng/Ten-Paces-Hidden-Moves refs/heads/main
git ls-remote https://github.com/alsdmlals4-eng/Blacksmith refs/heads/main
git ls-remote https://github.com/alsdmlals4-eng/omenward refs/heads/main
git ls-remote https://github.com/alsdmlals4-eng/urban-legend refs/heads/main
git ls-remote https://github.com/alsdmlals4-eng/GRIMOIRE- refs/heads/main
git ls-remote https://github.com/alsdmlals4-eng/Switchy-Express-Cargo-Puzzle refs/heads/main
```

Record the seven exact SHAs. Do not reuse design-time baselines as execution authority.

- [ ] **Step 2: Inspect same-goal PRs**

```bash
gh pr list --repo alsdmlals4-eng/Base --state all --search 'Godot multi-project Pilot OR editor transaction hardening'
for repo in Ten-Paces-Hidden-Moves Blacksmith omenward urban-legend GRIMOIRE- Switchy-Express-Cargo-Puzzle; do
  gh pr list --repo "alsdmlals4-eng/$repo" --state all --search 'Godot live editor OR project Pilot'
done
```

Expected: no competing Program A implementation PR. If one exists, stop and reconcile rather than duplicating it.

- [ ] **Step 3: Resolve PR #166 as a hard gate**

Check whether current Base `main` includes all four protections:

```text
operation IDs containing digits accepted safely
atomic replacement never unlinks the prior record before rename
approval-required mutation rechecks token binding and expiry at runtime
output validation enforces types plus save-mode/hash cross-field semantics
```

Run:

```bash
python -m pytest tests/test_godot_editor_transaction_adapter.py -q
python -m pytest tests/test_godot_editor_transaction_adapter_runtime.py -q
```

Expected: the four hardening regressions pass on current `main`. If not, Base C0 is blocked until PR #166 is rebased, reviewed, and separately approved or an equivalent focused hardening PR is merged.

- [ ] **Step 4: Record the prerequisite result in the Base C0 PR body**

Use exactly one state:

```yaml
editor_adapter_hardening: MERGED_PR_166
editor_adapter_hardening: EQUIVALENT_MAIN_PROOF
editor_adapter_hardening: BLOCKED
```

Do not start Base C0 production code in `BLOCKED` state.

---

### Task 2: Execute Base C0 and obtain the immutable workflow SHA

**Files:**
- Follow: `docs/superpowers/plans/2026-08-05-godot-multi-project-pilot-base-c0.md`

**Interfaces:**
- Consumes: current hardened transaction adapter.
- Produces: merged Base C0 commit containing the descriptor Schema, runner, evidence contract, reusable workflow, tests, and documentation.

- [ ] **Step 1: Execute Base C0 test-first**

Use a new branch from exact current Base `main`. Follow every RED/GREEN task in the Base C0 plan.

- [ ] **Step 2: Verify exact-head Base CI**

Required:

```text
Validate Base v9 Operating Contracts: SUCCESS
Validate Game Project Operating System: SUCCESS
focused multi-project Pilot tests: SUCCESS
adversarial multi-project Pilot tests: SUCCESS
unresolved review threads: 0
```

- [ ] **Step 3: Obtain explicit merge approval and merge**

After approval, squash merge with expected head SHA.

- [ ] **Step 4: Record immutable Base C0 SHA**

```bash
git ls-remote https://github.com/alsdmlals4-eng/Base refs/heads/main
```

This SHA becomes `base_pilot_commit` and the exact reusable-workflow `uses:` pin in all project descriptors and workflows.

---

### Task 3: Prove the clean baseline in Switchy Express

**Files:**
- Follow: `docs/superpowers/plans/2026-08-05-godot-pilot-switchy-express.md`

**Interfaces:**
- Consumes: exact Base C0 merge SHA.
- Produces: the first real-project runtime evidence proving the reusable workflow without legacy Godot AI conflict.

- [ ] **Step 1: Create a Draft PR from current Switchy `main`**

Only add the descriptor, adoption document, focused contract test, and caller workflow.

- [ ] **Step 2: Verify runtime evidence**

Required evidence states:

```yaml
project_load: PASS
main_scene_inspect: PASS
scratch_scene_rename: PASS
editor_undo: PASS
scratch_scene_save: PASS
physical_sha256: PASS
source_tree_unchanged: PASS
base_network_listener: false
legacy_mutation_authority: ABSENT
```

- [ ] **Step 3: Merge only after explicit approval**

The exact Base C0 pin and evidence artifact ID must be included in the PR record.

---

### Task 4: Execute the four policy/legacy Pilots

**Files:**
- Follow the Ten Paces, Blacksmith, OMENWARD, and urban-legend plans.

**Interfaces:**
- Consumes: exact Base C0 SHA and successful Switchy evidence.
- Produces: four independent evidence packages proving temporary legacy disablement and source-policy compliance.

- [ ] **Step 1: Create four independent Draft PRs**

Do not stack project PRs on one another. Each branch starts from that project's then-current `main`.

- [ ] **Step 2: Preserve project-specific gates**

```yaml
Ten_Paces:
  product_change: FORBIDDEN
  legacy_godot_ai_temp_disable: REQUIRED
Blacksmith:
  product_implementation: BLOCKED
  protected_paths_changed: false
OMENWARD:
  product_code_authority: NONE
  product_files_changed: false
urban_legend:
  non_mcp_autoloads_preserved_in_workspace: true
  source_project_godot_changed: false
```

- [ ] **Step 3: Reject false PASS**

A project with a pre-existing load failure records `PROJECT_LOAD_BLOCKED_PREEXISTING` plus bounded logs. It must not patch source product files inside the Pilot PR to manufacture a PASS.

- [ ] **Step 4: Merge each PR independently after approval**

A PASS in one project does not authorize merging another project PR.

---

### Task 5: Record GRIMOIRE preproject readiness without creating a product project

**Files:**
- Follow: `docs/superpowers/plans/2026-08-05-godot-pilot-grimoire-readiness.md`

**Interfaces:**
- Consumes: current GRIMOIRE authority stating `product_project: NOT_CREATED`.
- Produces: a machine-readable readiness descriptor and tests that reject runtime or installation claims.

- [ ] **Step 1: Add only readiness surfaces**

No `project.godot`, Scene, addon, workflow runtime invocation, or product code is added.

- [ ] **Step 2: Verify false runtime claims fail tests**

Expected descriptor state:

```json
{
  "project_state": "NOT_CREATED",
  "runtime_pilot": "NOT_APPLICABLE",
  "adapter_installation": "FORBIDDEN_UNTIL_PRODUCT_PROJECT_APPROVAL"
}
```

- [ ] **Step 3: Merge independently after approval**

---

### Task 6: Integrate exact evidence in Base C1

**Files:**
- Follow: `docs/superpowers/plans/2026-08-05-godot-multi-project-pilot-base-c1.md`

**Interfaces:**
- Consumes: exact merged project PR SHAs, workflow run IDs, artifact IDs, manifest hashes, and result hashes.
- Produces: Base evidence index, updated readiness document, and an explicit Program B decision state.

- [ ] **Step 1: Verify every external evidence reference**

For each real project, fetch the merged commit, workflow run, jobs, artifact metadata, and bounded evidence files. Recompute hashes rather than trusting PR prose.

- [ ] **Step 2: Build the evidence matrix**

Use only these result states:

```text
PASS
BLOCKED_PREEXISTING
NOT_APPLICABLE
NOT_RUN
FAIL
```

- [ ] **Step 3: Update Base readiness without overclaiming**

Even if all five real-project Pilots pass:

```yaml
program_a_multi_project_pilots: PASS
production_transport: NOT_IMPLEMENTED
runtime_debugger: NOT_IMPLEMENTED
windows_production_operation: NOT_RUN
human_editor_usability: HUMAN_NOT_RUN
production_adapter_ready: NOT_READY
```

- [ ] **Step 4: Decide only whether Program B design may start**

Allowed decisions:

```yaml
program_b_design_gate: OPEN
program_b_design_gate: BLOCKED
```

`OPEN` authorizes design work only, not transport implementation.

---

### Task 7: Run the final program-level adversarial review

**Files:**
- Read all eight PRs and the Base C1 evidence index.

**Interfaces:**
- Consumes: complete Program A evidence.
- Produces: a final attack/validation record with no unresolved P0/P1 findings before claiming Program A complete.

- [ ] **Step 1: Attack the authority boundary**

Attempt to prove any of the following occurred:

```text
source project.godot changed
product Scene mutated
legacy and Base mutation authorities active together
floating workflow ref used
artifact hash accepted without byte verification
main Scene mutated instead of scratch Scene
pre-existing project failure patched inside adoption PR
GRIMOIRE runtime PASS fabricated
network listener created by Base
project PR auto-merged
```

- [ ] **Step 2: Validate each critique against exact commits and artifacts**

Classify findings as `P0`, `P1`, `P2`, `REJECTED_CRITIQUE`, or `NOT_REPRODUCED`.

- [ ] **Step 3: Re-run regression gates**

```bash
python -m pytest tests/test_godot_multi_project_pilot.py -q
python -m pytest tests/test_godot_multi_project_pilot_adversarial.py -q
python -m pytest tests/test_local_validation.py tests/test_v9_machine_contracts.py -q
```

- [ ] **Step 4: Stop before Program B implementation**

Program A completion does not automatically invoke or implement Program B. Return to brainstorming with the exact Program A evidence and obtain a new design approval.
