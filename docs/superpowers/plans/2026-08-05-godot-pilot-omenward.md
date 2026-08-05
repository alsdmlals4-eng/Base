# OMENWARD Godot Project Pilot Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:test-driven-development` task by task and `superpowers:verification-before-completion` before PASS or merge claims.

**Goal:** Validate OMENWARD's disposable-copy compatibility with Base C0 while preserving `TOTAL_PLANNING`, `product_code_authority: NONE`, current Decisions, and every product file unchanged.

**Architecture:** Four operational adoption files call the immutable C0 workflow on PR and post-merge `main`. The Base runner disables Godot AI and `_mcp_game_helper` only in the disposable copy, inspects `res://scenes/main/main.tscn` read-only, and mutates only its own scratch Scene.

## Authority and scope

- Repository: `alsdmlals4-eng/omenward`.
- Audit baseline: `da382d52b4490acb8758a1683ea6c9e4f4bf388b`; execution starts from then-current project `main`.
- Project authority remains `TOTAL_PLANNING` with `product_code_authority: NONE`.
- `BASE_C0_SHA` is the exact merge SHA recorded by the Program A execution ledger, never later Base `main`.
- Switchy must already have a merged post-merge PASS using the same C0 SHA.
- Existing legacy plugin/Autoload remain unchanged in source and are disabled only in the copy.
- `behavior_checks` is empty because this operational PR has no product-code authority.

Allowed source changes:

```text
.godot-live-editor/project-pilot.json
docs/GODOT_LIVE_EDITOR_ADOPTION.md
tests/test_godot_live_editor_adoption.py
.github/workflows/validate-godot-live-editor-pilot.yml
```

Forbidden: `project.godot`, `addons/`, `scenes/`, `scripts/`, `src/`, `data/`, `assets/`, Resources, exact values, planning canon, and Google Sheets.

---

### Task 1: Freeze immutable C0 and current project baseline

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
- [ ] Search for a competing OMENWARD adoption PR before writing.

---

### Task 2: Write the planning-authority test first

**Create:** `tests/test_godot_live_editor_adoption.py`

RED assertions require:

- repository/project ID `alsdmlals4-eng/omenward` / `omenward`;
- exact 40-hex C0 pin;
- legacy plugin `res://addons/godot_ai/plugin.cfg`;
- legacy Autoload `_mcp_game_helper`;
- empty behavior checks;
- `source_mutation_policy: FORBIDDEN`;
- workflow pin equality and no `@main`;
- document markers:

```text
TOTAL_PLANNING_UNCHANGED
PRODUCT_CODE_AUTHORITY: NONE
OPERATIONAL_VALIDATION_ONLY
LEGACY_DISABLED_IN_DISPOSABLE_COPY_ONLY
MAIN_SCENE_READ_ONLY
SCRATCH_SCENE_MUTATION_ONLY
PRODUCTION_ADAPTER_READY: NOT_READY
```

- diff limited to the four allowed paths and no protected prefix.

Run RED and commit test-only:

```bash
python -m pytest tests/test_godot_live_editor_adoption.py -q
git add tests/test_godot_live_editor_adoption.py
git commit -m "test: require OMENWARD isolated Godot Pilot"
```

---

### Task 3: Add and validate the descriptor

**Create:** `.godot-live-editor/project-pilot.json`

```json
{
  "schema_version": "1",
  "project_identity": {
    "repository": "alsdmlals4-eng/omenward",
    "project_id": "omenward"
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

- [ ] Generate the real file from `$BASE_C0_SHA`; never commit the literal token.
- [ ] Validate with Base C0 `load_descriptor()` checked out at the exact SHA.
- [ ] Run focused tests and commit.

---

### Task 4: Add no-product-authority documentation

**Create:** `docs/GODOT_LIVE_EDITOR_ADOPTION.md`

Document:

- `TOTAL_PLANNING` and `product_code_authority: NONE` remain unchanged;
- no product code, Scene, Resource, game data, exact value, art, map, roulette, economy, save, or canon authority is created;
- legacy authority is source-preserved and disposable-copy-disabled only;
- real main Scene is read-only; scratch-only mutation applies;
- PASS means operational compatibility only;
- Program B/C and production readiness remain open;
- removal is a revert of the four adoption files.

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

- [ ] Generate both SHA positions from the execution ledger.
- [ ] Run focused tests and `git diff --check`; commit when GREEN.

---

### Task 6: Review without adding product authority

```bash
python -m pytest tests/test_godot_live_editor_adoption.py -q
python -m unittest discover -s tests -p 'test_*.py'
git diff --check
```

- [ ] Separate pre-existing failures and do not patch product files in this PR.
- [ ] Verify exactly four changed paths.
- [ ] Open a Draft PR with C0 SHA, `TOTAL_PLANNING_UNCHANGED`, `product_code_authority: NONE`, and `NOT_READY`.
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
base_network_listener: false
product_code_authority: NONE_UNCHANGED
```

- [ ] A current load failure is `PROJECT_LOAD_BLOCKED_PREEXISTING`; no source fix is authorized.
- [ ] Require exact-head CI and zero unresolved threads.
- [ ] Merge only after explicit user approval.

---

### Task 7: Capture post-merge evidence

- [ ] Wait for the push-triggered workflow on the squash-merged OMENWARD commit.
- [ ] Verify workflow source SHA equals the merged commit and uses the same C0 SHA.
- [ ] Recompute artifact and final evidence hashes.
- [ ] Record:

```yaml
repository: alsdmlals4-eng/omenward
validated_pr_head_sha: exact PR head
merged_commit_sha: exact squash merge
postmerge_workflow_run_id: integer
postmerge_artifact_id: integer
base_c0_sha: exact ledger C0 SHA
result: PASS_OR_BLOCKED_PREEXISTING
```

Only this post-merge ledger entry is consumed by Base C1.
