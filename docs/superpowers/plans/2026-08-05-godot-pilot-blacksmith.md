# Blacksmith Godot Project Pilot Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:test-driven-development` task by task and `superpowers:verification-before-completion` before PASS or merge claims.

**Goal:** Prove disposable-copy compatibility with Base C0 while preserving Blacksmith's explicit product-implementation block and every protected product path.

**Architecture:** Four operational adoption files call the immutable C0 workflow on PR and post-merge `main`. The Base runner disables Godot AI and `_mcp_game_helper` only in the disposable copy, inspects the configured enhancement-test Scene read-only, and mutates only its own scratch Scene.

## Authority and scope

- Repository: `alsdmlals4-eng/Blacksmith`.
- Audit baseline: `b1dd945875568098b107815a03e88b0272d384e9`; execution starts from then-current project `main`.
- Current project authority: product implementation `BLOCKED`.
- `BASE_C0_SHA` is the exact merge SHA from the Program A execution ledger, never later Base `main`.
- Switchy must already have a merged post-merge PASS using the same C0 SHA.
- Source legacy authority remains installed and is disabled only in the copy.
- `behavior_checks` stays empty; this PR gains no product-test or implementation authority.

Allowed source changes:

```text
.godot-live-editor/project-pilot.json
docs/GODOT_LIVE_EDITOR_ADOPTION.md
tests/test_godot_live_editor_adoption.py
.github/workflows/validate-godot-live-editor-pilot.yml
```

Protected: `data/`, `scripts/`, `scenes/`, `assets/`, `addons/`, `project.godot`, planning canon, and Google Sheets.

---

### Task 1: Freeze exact C0 and project baseline

```bash
export BASE_C0_SHA="<exact Base C0 merge SHA from Program A ledger>"
test "${#BASE_C0_SHA}" -eq 40
gh api "repos/alsdmlals4-eng/Base/commits/$BASE_C0_SHA" >/dev/null
gh api "repos/alsdmlals4-eng/Base/contents/.github/workflows/reusable-godot-project-pilot.yml?ref=$BASE_C0_SHA" >/dev/null
git fetch origin main
export PROJECT_BASELINE_SHA="$(git rev-parse origin/main)"
git switch -c agent/adopt-base-godot-project-pilot "$PROJECT_BASELINE_SHA"
```

- [ ] Verify the Switchy ledger entry uses the same C0 SHA and is PASS.
- [ ] Search for a competing Blacksmith adoption PR before writing.

---

### Task 2: Write the protected-path contract test first

**Create:** `tests/test_godot_live_editor_adoption.py`

RED assertions require:

- repository/project ID `alsdmlals4-eng/Blacksmith` / `blacksmith`;
- exact 40-hex C0 pin;
- legacy plugin `res://addons/godot_ai/plugin.cfg`;
- legacy Autoload `_mcp_game_helper`;
- `TEMPORARY_COPY_ONLY` and `FORBIDDEN` source mutation;
- empty `behavior_checks`;
- `expected_platform: ANDROID`;
- workflow pin equality and no `@main`;
- document markers:

```text
PRODUCT_IMPLEMENTATION_BLOCKED
OPERATIONAL_VALIDATION_ONLY
LEGACY_DISABLED_IN_DISPOSABLE_COPY_ONLY
MAIN_SCENE_READ_ONLY
SCRATCH_SCENE_MUTATION_ONLY
PRODUCTION_ADAPTER_READY: NOT_READY
```

- diff limited to the four allowed files and no protected prefix.

Run RED and commit test-only:

```bash
python -m pytest tests/test_godot_live_editor_adoption.py -q
git add tests/test_godot_live_editor_adoption.py
git commit -m "test: require Blacksmith isolated Godot Pilot"
```

---

### Task 3: Add and validate the descriptor

**Create:** `.godot-live-editor/project-pilot.json`

Required values:

```json
{
  "schema_version": "1",
  "project_identity": {
    "repository": "alsdmlals4-eng/Blacksmith",
    "project_id": "blacksmith"
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
  "expected_platform": "ANDROID"
}
```

- [ ] Generate the real file from `$BASE_C0_SHA`; never commit the literal token.
- [ ] Validate it with Base C0 `load_descriptor()` checked out at the exact SHA.
- [ ] Run focused test and commit.

---

### Task 4: Add operational-only documentation

**Create:** `docs/GODOT_LIVE_EDITOR_ADOPTION.md`

The document must state:

- product implementation remains blocked;
- no code, data, Scene, asset, addon, project setting, economy, strengthening, crafting, save, or Game Bible authority is created;
- Godot AI is preserved in source and disabled only in the copy;
- real main Scene is read-only and scratch-only mutation applies;
- evidence proves operational compatibility only;
- Program B/C and production readiness remain open;
- removal is a revert of the four adoption files.

- [ ] Run focused test and commit.

---

### Task 5: Add the immutable PR/push workflow

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

- [ ] Generate both SHA locations from the execution-ledger value.
- [ ] Run focused tests and `git diff --check`; commit when GREEN.

---

### Task 6: Review without violating the product block

```bash
python -m pytest tests/test_godot_live_editor_adoption.py -q
python -m unittest discover -s tests -p 'test_*.py'
git diff --check
```

- [ ] Separate pre-existing failures. Do not modify protected paths to manufacture PASS.
- [ ] Verify exactly four changed files.
- [ ] Open a Draft PR with exact C0 SHA, product block unchanged, no product path changes, and `NOT_READY` state.
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
product_implementation: BLOCKED_UNCHANGED
```

- [ ] A current load failure is `PROJECT_LOAD_BLOCKED_PREEXISTING`; it does not authorize source fixes in this PR.
- [ ] Require exact-head CI and zero unresolved threads.
- [ ] Merge only after explicit user approval.

---

### Task 7: Capture post-merge evidence

- [ ] Wait for the push-triggered workflow on the squash-merged Blacksmith commit.
- [ ] Verify workflow source SHA equals the merged commit and the same C0 SHA is used.
- [ ] Recompute artifact/final evidence hashes.
- [ ] Record:

```yaml
repository: alsdmlals4-eng/Blacksmith
validated_pr_head_sha: exact PR head
merged_commit_sha: exact squash merge
postmerge_workflow_run_id: integer
postmerge_artifact_id: integer
base_c0_sha: exact ledger C0 SHA
result: PASS_OR_BLOCKED_PREEXISTING
```

Only this post-merge ledger entry is consumed by Base C1.
