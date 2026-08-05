# Urban-Legend Godot Project Pilot Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:test-driven-development` task by task and `superpowers:verification-before-completion` before PASS or merge claims.

**Goal:** Prove Base C0 compatibility in a disposable 괴이 기록국 copy while disabling only legacy MCP authority and preserving all project-owned Autoloads, product files, saves, and canon unchanged.

**Architecture:** Four adoption files call the immutable C0 workflow on PR and post-merge `main`. The Base runner removes only Godot AI and `_mcp_game_helper` in the copy, verifies `UrbanLegendState`, `ValidationSession`, and `GameState` remain configured, inspects `res://scenes/main_menu.tscn` read-only, and mutates only its own scratch Scene.

## Authority and scope

- Repository: `alsdmlals4-eng/urban-legend`.
- Audit baseline: `f7edb459938bb5f3e2533ad828c2fe55019cd14b`; execution starts from then-current project `main`.
- `BASE_C0_SHA` is the exact merge SHA from the Program A ledger, never later Base `main`.
- Switchy must already have a merged post-merge PASS using the same C0 SHA.
- Source Autoloads:
  - `UrbanLegendState` — preserve;
  - `ValidationSession` — preserve;
  - `GameState` — preserve;
  - `_mcp_game_helper` — disable only in copy.
- Source Godot AI plugin remains installed and is disabled only in copy.
- `behavior_checks` stays empty; existing project CI remains independent.

Allowed source changes:

```text
.godot-live-editor/project-pilot.json
docs/GODOT_LIVE_EDITOR_ADOPTION.md
tests/test_godot_live_editor_adoption.py
.github/workflows/validate-godot-live-editor-pilot.yml
```

Forbidden: `project.godot`, `addons/`, `scripts/`, `scenes/`, `data/`, `assets/`, `knowledge/base-pack/`, save/version fields, current canon, generated GDD/DOCX, and Google Sheets.

---

### Task 1: Freeze exact C0 and current project baseline

```bash
export BASE_C0_SHA="<exact Base C0 merge SHA from Program A ledger>"
test "${#BASE_C0_SHA}" -eq 40
gh api "repos/alsdmlals4-eng/Base/commits/$BASE_C0_SHA" >/dev/null
gh api "repos/alsdmlals4-eng/Base/contents/.github/workflows/reusable-godot-project-pilot.yml?ref=$BASE_C0_SHA" >/dev/null
git fetch origin main
export PROJECT_BASELINE_SHA="$(git rev-parse origin/main)"
git switch -c agent/adopt-base-godot-project-pilot "$PROJECT_BASELINE_SHA"
```

- [ ] Verify Switchy evidence uses the same C0 SHA and is PASS.
- [ ] Search for a competing urban-legend adoption PR.

---

### Task 2: Write Autoload-preservation tests first

**Create:** `tests/test_godot_live_editor_adoption.py`

RED assertions require:

- repository/project ID `alsdmlals4-eng/urban-legend` / `urban-legend`;
- exact 40-hex C0 pin;
- legacy plugin list exactly `res://addons/godot_ai/plugin.cfg`;
- legacy Autoload list exactly `_mcp_game_helper`;
- descriptor does not classify the three project-owned Autoloads as legacy;
- empty behavior checks and `FORBIDDEN` source mutation;
- workflow pin equality and no `@main`;
- document markers:

```text
PROJECT_AUTOLOADS_PRESERVED
UrbanLegendState
ValidationSession
GameState
MCP_AUTOLOAD_DISABLED_IN_DISPOSABLE_COPY_ONLY
MAIN_SCENE_READ_ONLY
SCRATCH_SCENE_MUTATION_ONLY
PRODUCTION_ADAPTER_READY: NOT_READY
```

- diff limited to the four allowed paths and no protected prefix.

Run RED and commit test-only:

```bash
python -m pytest tests/test_godot_live_editor_adoption.py -q
git add tests/test_godot_live_editor_adoption.py
git commit -m "test: require urban-legend isolated Godot Pilot"
```

---

### Task 3: Add and validate the descriptor

**Create:** `.godot-live-editor/project-pilot.json`

```json
{
  "schema_version": "1",
  "project_identity": {
    "repository": "alsdmlals4-eng/urban-legend",
    "project_id": "urban-legend"
  },
  "base_pilot_commit": "BASE_C0_SHA",
  "project_state": "EXISTING_GODOT_PROJECT",
  "godot": {
    "version": "4.7.1-stable",
    "archive_sha256": "c7ff14fd28472c8d4f193043de30278dcf7e5241a1dcf7566b02e27addaa33ba"
  },
  "project_file": "project.godot",
  "main_scene_source": "application/run/main_scene",
  "legacy_editor_plugins": ["res://addons/godot_ai/plugin.cfg"],
  "legacy_autoloads": ["_mcp_game_helper"],
  "legacy_disable_mode": "TEMPORARY_COPY_ONLY",
  "source_mutation_policy": "FORBIDDEN",
  "scratch_scene_path": "res://.godot-live-editor-pilot/scratch.tscn",
  "behavior_checks": [],
  "expected_platform": "PC"
}
```

- [ ] Generate the actual file from `$BASE_C0_SHA`; never commit the literal token.
- [ ] Validate with Base C0 `load_descriptor()` at the exact SHA.
- [ ] Run focused tests and commit.

---

### Task 4: Add source and Autoload preservation documentation

**Create:** `docs/GODOT_LIVE_EDITOR_ADOPTION.md`

Document:

- source Godot AI remains installed;
- only `_mcp_game_helper` and the legacy plugin entry are disabled in the copy;
- `UrbanLegendState`, `ValidationSession`, and `GameState` must remain exact in the transformed copy;
- main menu Scene is read-only and scratch-only mutation applies;
- no campaign/save state, episodes, investigation/stabilization rules, canon, UI, assets, project settings, GDD/DOCX generation, or Sheet changes occur;
- Program B/C and production readiness remain open;
- removal is a revert of four adoption files.

- [ ] Run focused test and commit.

---

### Task 5: Add immutable PR/push workflow

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

- [ ] Generate both SHA positions from the Program A ledger value.
- [ ] Run focused tests and `git diff --check`; commit when GREEN.

---

### Task 6: Review runtime and selective-transform evidence

```bash
python -m pytest tests/test_godot_live_editor_adoption.py -q
python -m unittest discover -s tests -p 'test_*.py'
git diff --check
```

- [ ] Do not patch product files to fix unrelated historical failures.
- [ ] Verify exactly four changed paths.
- [ ] Open a Draft PR recording C0 SHA, source `project.godot` blob, no protected paths, and `NOT_READY`.
- [ ] If the project loads, require:

```yaml
project_load: PASS
main_scene_inspect: PASS
scratch_scene_rename: PASS
editor_undo: PASS
scratch_scene_save: PASS
physical_sha256: PASS
source_tree_unchanged: PASS
legacy_mutation_authority: DISABLED_IN_WORKSPACE_ONLY
project_autoloads_preserved:
  UrbanLegendState: true
  ValidationSession: true
  GameState: true
base_network_listener: false
```

- [ ] Inspect the transformed disposable `project.godot`: legacy entries absent, three project Autoload lines present and exact.
- [ ] A preserved-Autoload load failure is `PROJECT_LOAD_BLOCKED_PREEXISTING`; do not remove the Autoload to fabricate PASS.
- [ ] Require exact-head CI and zero unresolved threads.
- [ ] Merge only after explicit user approval.

---

### Task 7: Capture post-merge evidence

- [ ] Wait for the push-triggered workflow on the squash-merged urban-legend commit.
- [ ] Verify workflow source SHA equals the merged commit and uses the same C0 SHA.
- [ ] Recompute archive/final evidence hashes and inspect preserved Autoload evidence.
- [ ] Record:

```yaml
repository: alsdmlals4-eng/urban-legend
validated_pr_head_sha: exact PR head
merged_commit_sha: exact squash merge
postmerge_workflow_run_id: integer
postmerge_artifact_id: integer
base_c0_sha: exact ledger C0 SHA
result: PASS_OR_BLOCKED_PREEXISTING
```

Only this post-merge ledger entry is consumed by Base C1.
