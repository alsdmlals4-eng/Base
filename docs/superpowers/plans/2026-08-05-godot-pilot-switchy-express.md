# Switchy Express Godot Project Pilot Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:test-driven-development` task by task and `superpowers:verification-before-completion` before any PASS or merge claim.

**Goal:** Adopt the merged Base C0 workflow in Switchy Express as the first clean real-project proof without modifying product files or permanently installing the Base addon.

**Architecture:** The project PR adds four adoption surfaces only. A caller workflow pinned to the Program A ledger's exact `BASE_C0_SHA` runs on PRs and again after merge to `main`. The Base workflow copies the project, opens the configured main Scene read-only, mutates only its own scratch Scene, verifies Undo/save/physical bytes/source integrity, and uploads bounded evidence.

**Tech Stack:** Godot 4.7.1 stable, GDScript, Python 3.12/pytest, GitHub Actions reusable workflow, existing `res://tests/run_tests.gd`.

## Immutable authority

- Repository: `alsdmlals4-eng/Switchy-Express-Cargo-Puzzle`.
- Plan audit baseline: `b2ecc7220f4cad546814bcce43e998a45fff5281`; execution starts from then-current project `main`.
- `BASE_C0_SHA` comes only from the Program A execution ledger written immediately after Base C0 merges.
- Do **not** resolve `BASE_C0_SHA` from later Base `main`.
- Verify the recorded commit contains:
  - `.github/workflows/reusable-godot-project-pilot.yml`;
  - `schemas/godot-project-pilot-v1.schema.json`;
  - `tools/godot_multi_project_pilot.py`.
- Main Scene is `res://game/main/main.tscn` and remains read-only.
- Legacy Godot AI is absent.

## Allowed source changes

```text
.godot-live-editor/project-pilot.json
docs/GODOT_LIVE_EDITOR_ADOPTION.md
tests/test_godot_live_editor_adoption.py
.github/workflows/validate-godot-live-editor-pilot.yml
```

Forbidden: `project.godot`, `game/`, `scenes/`, `data/`, `addons/`, `export_presets.cfg`, existing product tests, saves, inputs, and Google Sheets.

---

### Task 1: Freeze the project baseline and exact C0 ledger value

- [ ] Set the reviewed C0 value explicitly:

```bash
export BASE_C0_SHA="<exact merge SHA recorded by Base C0 execution ledger>"
test "${#BASE_C0_SHA}" -eq 40
```

- [ ] Verify it is a commit and contains the C0 contract:

```bash
gh api "repos/alsdmlals4-eng/Base/commits/$BASE_C0_SHA" >/dev/null
gh api "repos/alsdmlals4-eng/Base/contents/.github/workflows/reusable-godot-project-pilot.yml?ref=$BASE_C0_SHA" >/dev/null
gh api "repos/alsdmlals4-eng/Base/contents/schemas/godot-project-pilot-v1.schema.json?ref=$BASE_C0_SHA" >/dev/null
```

- [ ] Create a branch from exact current project `main`:

```bash
git fetch origin main
export PROJECT_BASELINE_SHA="$(git rev-parse origin/main)"
git switch -c agent/adopt-base-godot-project-pilot "$PROJECT_BASELINE_SHA"
```

---

### Task 2: Write the local adoption contract test first

**Create:** `tests/test_godot_live_editor_adoption.py`

- [ ] RED tests require:
  - exact repository/project ID;
  - lowercase 40-hex Base pin;
  - `project_state: EXISTING_GODOT_PROJECT`;
  - empty legacy plugin/Autoload arrays;
  - `source_mutation_policy: FORBIDDEN`;
  - scratch path `res://.godot-live-editor-pilot/scratch.tscn`;
  - one behavior check:

```json
{
  "kind": "GODOT_SCRIPT",
  "target": "res://tests/run_tests.gd",
  "timeout_seconds": 120
}
```

  - workflow `uses:` and `with.base_pilot_commit` equal the descriptor SHA;
  - workflow contains no `@main` Base reference;
  - adoption document contains `TEMPORARY_COPY_ONLY`, `MAIN_SCENE_READ_ONLY`, `SCRATCH_SCENE_MUTATION_ONLY`, `SOURCE_TREE_UNCHANGED`, and `PRODUCTION_ADAPTER_READY: NOT_READY`;
  - git diff contains only the four allowed paths.

- [ ] Run RED:

```bash
python -m pytest tests/test_godot_live_editor_adoption.py -q
```

Expected: missing descriptor/document/workflow failures only.

- [ ] Commit test-only RED.

---

### Task 3: Add the descriptor and validate it through exact Base C0

**Create:** `.godot-live-editor/project-pilot.json`

```json
{
  "schema_version": "1",
  "project_identity": {
    "repository": "alsdmlals4-eng/Switchy-Express-Cargo-Puzzle",
    "project_id": "switchy-express-cargo-puzzle"
  },
  "base_pilot_commit": "BASE_C0_SHA",
  "project_state": "EXISTING_GODOT_PROJECT",
  "godot": {
    "version": "4.7.1-stable",
    "archive_sha256": "c7ff14fd28472c8d4f193043de30278dcf7e5241a1dcf7566b02e27addaa33ba"
  },
  "project_file": "project.godot",
  "main_scene_source": "application/run/main_scene",
  "legacy_editor_plugins": [],
  "legacy_autoloads": [],
  "legacy_disable_mode": "TEMPORARY_COPY_ONLY",
  "source_mutation_policy": "FORBIDDEN",
  "scratch_scene_path": "res://.godot-live-editor-pilot/scratch.tscn",
  "behavior_checks": [
    {
      "kind": "GODOT_SCRIPT",
      "target": "res://tests/run_tests.gd",
      "timeout_seconds": 120
    }
  ],
  "expected_platform": "ANDROID"
}
```

- [ ] Generate the actual file programmatically, replacing the displayed token with `$BASE_C0_SHA`; never commit the literal token.
- [ ] Check out Base at `$BASE_C0_SHA`, import `load_descriptor`, and require success.
- [ ] Run the focused test; descriptor assertions should be GREEN while missing document/workflow remain RED.
- [ ] Commit descriptor plus test state.

---

### Task 4: Add adoption documentation

**Create:** `docs/GODOT_LIVE_EDITOR_ADOPTION.md`

Required sections:

```text
Status
TEMPORARY_COPY_ONLY
MAIN_SCENE_READ_ONLY
SCRATCH_SCENE_MUTATION_ONLY
SOURCE_TREE_UNCHANGED
PRODUCTION_ADAPTER_READY: NOT_READY
What the Pilot does
What the Pilot does not do
Evidence and physical hashes
Program B/C exclusions
Removal by reverting the four adoption files
```

The document must state there is no permanent addon installation and no product, Android-device, physical-input, accessibility, performance, or human-usability claim.

- [ ] Run the focused test; only workflow assertions should remain RED.
- [ ] Commit documentation.

---

### Task 5: Add the immutable caller workflow

**Create:** `.github/workflows/validate-godot-live-editor-pilot.yml`

```yaml
name: Validate Godot Live-Editor Pilot

on:
  pull_request:
    branches: [main]
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read

jobs:
  adoption-contract:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
          persist-credentials: false
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: python -m pip install --disable-pip-version-check pytest==8.3.5
      - run: python -m pytest tests/test_godot_live_editor_adoption.py -q

  project-pilot:
    needs: adoption-contract
    uses: alsdmlals4-eng/Base/.github/workflows/reusable-godot-project-pilot.yml@BASE_C0_SHA
    with:
      base_pilot_commit: BASE_C0_SHA
      descriptor_path: .godot-live-editor/project-pilot.json
      artifact_retention_days: 14
```

- [ ] Generate the workflow programmatically from `$BASE_C0_SHA`; never commit the literal token.
- [ ] Run focused tests and `git diff --check`; all GREEN.
- [ ] Commit workflow.

---

### Task 6: Review the PR and pre-merge evidence

- [ ] Run:

```bash
python -m pytest tests/test_godot_live_editor_adoption.py -q
python tools/validate_project_contract.py
git diff --check
git diff --name-only "$(git merge-base HEAD origin/main)" HEAD
```

- [ ] Expected diff: exactly four allowed paths.
- [ ] Open a Draft PR with exact project baseline, exact C0 SHA, `legacy_godot_ai: ABSENT`, no product files changed, and `production_adapter_ready: NOT_READY`.
- [ ] PR workflow must prove:

```yaml
project_load: PASS
main_scene_inspect: PASS
scratch_scene_rename: PASS
editor_undo: PASS
scratch_scene_save: PASS
physical_sha256: PASS
source_tree_unchanged: PASS
legacy_mutation_authority: ABSENT
base_network_listener: false
```

- [ ] Download the PR artifact and recompute final evidence and saved scratch Scene hashes.
- [ ] Require zero unresolved review threads and exact-head required checks.
- [ ] Merge only after explicit user approval.

---

### Task 7: Capture post-merge evidence for Base C1

- [ ] Wait for `Validate Godot Live-Editor Pilot` on the **merged main commit** triggered by `push`.
- [ ] Verify the workflow source SHA equals the squash-merged Switchy commit.
- [ ] Download and physically reverify the push artifact.
- [ ] Record in the Program A evidence ledger:

```yaml
repository: alsdmlals4-eng/Switchy-Express-Cargo-Puzzle
validated_pr_head_sha: exact PR head
merged_commit_sha: exact squash merge
postmerge_workflow_run_id: integer
postmerge_artifact_id: integer
base_c0_sha: exact ledger C0 SHA
result: PASS
```

- [ ] These identifiers, not the later project `main`, are the Base C1 inputs.
