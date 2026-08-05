# Ten Paces Godot Project Pilot Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:test-driven-development` task by task and `superpowers:verification-before-completion` before PASS or merge claims.

**Goal:** Prove the Base C0 transaction adapter in a disposable Ten Paces copy while preserving the source Godot AI 3.0.5 addon, `_mcp_game_helper`, combat implementation, active planning, and product files unchanged.

**Architecture:** Four adoption files call the immutable Base C0 workflow on PR and post-merge `main`. The disposable workspace removes only the declared legacy plugin/Autoload, inspects the configured combat Scene read-only, mutates only a runner-owned scratch Scene, and records physical/source-integrity evidence.

## Authority and scope

- Repository: `alsdmlals4-eng/Ten-Paces-Hidden-Moves`.
- Audit baseline: `4b5967dee99592de4a09a611068344994e1ee026`; execution starts from then-current project `main`.
- `BASE_C0_SHA` is the exact merge SHA recorded by the Program A execution ledger. Never derive it from later Base `main`.
- Switchy Express must already have a merged post-merge PASS using the same C0 SHA.
- Main Scene comes from `project.godot` and is read-only.
- Source legacy authority remains installed:
  - `res://addons/godot_ai/plugin.cfg`;
  - `_mcp_game_helper`.
- The disposable copy must disable both before Base activation.
- Existing smoke check: `res://tests/verify_step0.gd`.

Allowed source changes:

```text
.godot-live-editor/project-pilot.json
docs/GODOT_LIVE_EDITOR_ADOPTION.md
tests/test_godot_live_editor_adoption.py
.github/workflows/validate-godot-live-editor-pilot.yml
```

Forbidden: `project.godot`, `addons/`, `data/`, `src/`, `scenes/`, `assets/`, planning canon, saves, and Google Sheets.

---

### Task 1: Freeze the immutable C0 value and project branch

```bash
export BASE_C0_SHA="<exact Base C0 merge SHA from Program A ledger>"
test "${#BASE_C0_SHA}" -eq 40
gh api "repos/alsdmlals4-eng/Base/commits/$BASE_C0_SHA" >/dev/null
gh api "repos/alsdmlals4-eng/Base/contents/.github/workflows/reusable-godot-project-pilot.yml?ref=$BASE_C0_SHA" >/dev/null
git fetch origin main
export PROJECT_BASELINE_SHA="$(git rev-parse origin/main)"
git switch -c agent/adopt-base-godot-project-pilot "$PROJECT_BASELINE_SHA"
```

- [ ] Verify the merged Switchy evidence ledger entry pins the same C0 SHA and is PASS.
- [ ] Search for any competing Ten Paces adoption PR; reconcile rather than duplicate.

---

### Task 2: Write the local contract test first

**Create:** `tests/test_godot_live_editor_adoption.py`

- [ ] RED assertions require:
  - repository/project ID `alsdmlals4-eng/Ten-Paces-Hidden-Moves` / `ten-paces-hidden-moves`;
  - exact lowercase 40-hex C0 pin;
  - legacy plugin list exactly `res://addons/godot_ai/plugin.cfg`;
  - legacy Autoload list exactly `_mcp_game_helper`;
  - `legacy_disable_mode: TEMPORARY_COPY_ONLY`;
  - `source_mutation_policy: FORBIDDEN`;
  - behavior check exactly:

```json
{
  "kind": "GODOT_SCRIPT",
  "target": "res://tests/verify_step0.gd",
  "timeout_seconds": 60
}
```

  - workflow `uses:` and `with.base_pilot_commit` match the descriptor SHA and contain no `@main`;
  - document markers:

```text
LEGACY_GODOT_AI_SOURCE_PRESERVED
LEGACY_DISABLED_IN_DISPOSABLE_COPY_ONLY
DUAL_MUTATION_AUTHORITY_FORBIDDEN
MAIN_SCENE_READ_ONLY
SCRATCH_SCENE_MUTATION_ONLY
PRODUCTION_ADAPTER_READY: NOT_READY
```

  - diff contains only the four allowed files.

- [ ] Run RED and commit test-only:

```bash
python -m pytest tests/test_godot_live_editor_adoption.py -q
git add tests/test_godot_live_editor_adoption.py
git commit -m "test: require Ten Paces isolated Godot Pilot"
```

---

### Task 3: Add and validate the descriptor

**Create:** `.godot-live-editor/project-pilot.json`

Required values:

```json
{
  "schema_version": "1",
  "project_identity": {
    "repository": "alsdmlals4-eng/Ten-Paces-Hidden-Moves",
    "project_id": "ten-paces-hidden-moves"
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
  "behavior_checks": [
    {
      "kind": "GODOT_SCRIPT",
      "target": "res://tests/verify_step0.gd",
      "timeout_seconds": 60
    }
  ],
  "expected_platform": "PC"
}
```

- [ ] Generate the file from `$BASE_C0_SHA`; never commit the literal token.
- [ ] Check out Base at that SHA and require `load_descriptor()` success.
- [ ] Run focused tests and commit.

---

### Task 4: Add the coexistence-boundary document

**Create:** `docs/GODOT_LIVE_EDITOR_ADOPTION.md`

Document:

- source Godot AI and `_mcp_game_helper` remain unchanged;
- only disposable-copy entries are disabled;
- legacy execution never proves Base v2 completion;
- real combat Scene is read-only;
- rename/Undo/save occur only on scratch Scene;
- combat, route, reward, save, UI, data, planning Decisions, and Sheet remain unchanged;
- Program B/C and production readiness remain excluded;
- removal is one revert of the four adoption files.

- [ ] Run focused test and commit.

---

### Task 5: Add the exact caller workflow

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

- [ ] Generate both SHA locations from `$BASE_C0_SHA`; never commit the literal token.
- [ ] Run focused tests and `git diff --check`; commit when GREEN.

---

### Task 6: Validate the PR and legacy-disable evidence

Run:

```bash
python -m pytest tests/test_godot_live_editor_adoption.py -q
python tools/check_project_operating_system.py --root . --config .github/documentation-governance.json
python tools/check_canonical_reference_freshness.py --root . --config .github/reference-freshness.json
python -m unittest discover -s tests -p "test_project_governance.py"
git diff --check
```

- [ ] Verify exactly four changed paths and no protected path.
- [ ] Open a Draft PR recording exact C0 SHA, source `project.godot` blob, no product mutation, and `NOT_READY` state.
- [ ] PR artifact must prove:

```yaml
project_load: PASS
main_scene_inspect: PASS
scratch_scene_rename: PASS
editor_undo: PASS
scratch_scene_save: PASS
physical_sha256: PASS
source_tree_unchanged: PASS
legacy_mutation_authority: DISABLED_IN_WORKSPACE_ONLY
legacy_plugin_removed_from_source: false
legacy_autoload_removed_from_source: false
base_network_listener: false
```

- [ ] Physically verify the disposable `project.godot` removed only the two declared legacy entries and the source blob is unchanged.
- [ ] Require exact-head CI and zero unresolved threads.
- [ ] Merge only after explicit user approval.

---

### Task 7: Capture post-merge evidence

- [ ] Wait for the workflow triggered by push to the squash-merged `main` commit.
- [ ] Require its source SHA to equal the merged Ten Paces commit.
- [ ] Recompute artifact and final evidence hashes.
- [ ] Record in Program A ledger:

```yaml
repository: alsdmlals4-eng/Ten-Paces-Hidden-Moves
validated_pr_head_sha: exact PR head
merged_commit_sha: exact squash merge
postmerge_workflow_run_id: integer
postmerge_artifact_id: integer
base_c0_sha: exact ledger C0 SHA
result: PASS
```

These identifiers are the only Base C1 inputs for Ten Paces.
