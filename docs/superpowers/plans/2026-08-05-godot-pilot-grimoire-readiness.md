# GRIMOIRE Godot Preproject Readiness Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:test-driven-development` task by task and `superpowers:verification-before-completion` before readiness or merge claims.

**Goal:** Record future Base C0 adoption readiness without creating a Godot product project, running a fabricated Runtime Pilot, or changing approved design and product gates.

**Architecture:** Four static readiness files pin the exact Base C0 merge SHA from the Program A ledger. CI runs on PR and post-merge `main`, validates the `NOT_CREATED` descriptor through that exact Base checkout, and never downloads or executes Godot.

## Authority and scope

- Repository: `alsdmlals4-eng/GRIMOIRE-`.
- Audit baseline: `2d80e4afcfc6b530b76912826f5984cdf1184678`; execution starts from then-current project `main`.
- Current authority:
  - `product_project: NOT_CREATED`;
  - `product_implementation: NOT_STARTED`;
  - `runtime_validation: NOT_RUN`.
- `BASE_C0_SHA` is the exact merge SHA from the Program A execution ledger, never later Base `main`.
- No `project.godot`, Scene, script, addon, export, Resource, product code, or Runtime Pilot is created.

Allowed source changes:

```text
.godot-live-editor/project-pilot.json
docs/GODOT_LIVE_EDITOR_ADOPTION_READINESS.md
tests/test_godot_live_editor_readiness.py
.github/workflows/validate-godot-live-editor-readiness.yml
```

Forbidden: product-project files, 3×3/Frostbloom canon changes, assets, implementation gates, and Google Sheets.

---

### Task 1: Freeze immutable C0 and confirm project absence

```bash
export BASE_C0_SHA="<exact Base C0 merge SHA from Program A ledger>"
test "${#BASE_C0_SHA}" -eq 40
gh api "repos/alsdmlals4-eng/Base/commits/$BASE_C0_SHA" >/dev/null
gh api "repos/alsdmlals4-eng/Base/contents/schemas/godot-project-pilot-v1.schema.json?ref=$BASE_C0_SHA" >/dev/null
git fetch origin main
export PROJECT_BASELINE_SHA="$(git rev-parse origin/main)"
git switch -c agent/add-godot-adoption-readiness "$PROJECT_BASELINE_SHA"
test ! -e project.godot
test ! -d scenes
test ! -d addons
```

- [ ] If a product project now exists through an approved decision, stop and replace this plan with a real-project Pilot plan.
- [ ] Search for a competing readiness/adoption PR before writing.

---

### Task 2: Write the no-runtime contract test first

**Create:** `tests/test_godot_live_editor_readiness.py`

RED assertions require:

- repository/project ID `alsdmlals4-eng/GRIMOIRE-` / `grimoire`;
- exact 40-hex C0 pin;
- `project_state: NOT_CREATED`;
- `project_file: null`;
- `main_scene_source: NOT_APPLICABLE`;
- empty legacy arrays and behavior checks;
- `expected_platform: NOT_CREATED`;
- document markers:

```text
PRODUCT_PROJECT: NOT_CREATED
RUNTIME_PILOT: NOT_APPLICABLE
ADAPTER_INSTALLATION: FORBIDDEN_UNTIL_PRODUCT_PROJECT_APPROVAL
RUNTIME_PASS_FORBIDDEN
PRODUCTION_ADAPTER_READY: NOT_READY
```

- workflow checks out Base at the descriptor SHA, contains no reusable runtime workflow, Godot download, or Pilot runner invocation, and contains no `@main`;
- diff contains only the four readiness paths;
- `project.godot`, product Scenes/scripts/addons/exports remain absent.

Run RED and commit test-only:

```bash
python -m pytest tests/test_godot_live_editor_readiness.py -q
git add tests/test_godot_live_editor_readiness.py
git commit -m "test: require GRIMOIRE Godot preproject readiness"
```

---

### Task 3: Add and validate the `NOT_CREATED` descriptor

**Create:** `.godot-live-editor/project-pilot.json`

```json
{
  "schema_version": "1",
  "project_identity": {
    "repository": "alsdmlals4-eng/GRIMOIRE-",
    "project_id": "grimoire"
  },
  "base_pilot_commit": "BASE_C0_SHA",
  "project_state": "NOT_CREATED",
  "godot": {
    "version": "4.7.1-stable",
    "archive_sha256": "c7ff14fd28472c8d4f193043de30278dcf7e5241a1dcf7566b02e27addaa33ba"
  },
  "project_file": null,
  "main_scene_source": "NOT_APPLICABLE",
  "legacy_editor_plugins": [],
  "legacy_autoloads": [],
  "legacy_disable_mode": "TEMPORARY_COPY_ONLY",
  "source_mutation_policy": "FORBIDDEN",
  "scratch_scene_path": "res://.godot-live-editor-pilot/scratch.tscn",
  "behavior_checks": [],
  "expected_platform": "NOT_CREATED"
}
```

- [ ] Generate the real file from `$BASE_C0_SHA`; never commit the literal token.
- [ ] Check out Base at that SHA and require `load_descriptor(...).is_runtime_project is False`.
- [ ] Run focused test and commit.

---

### Task 4: Add the future adoption checklist

**Create:** `docs/GODOT_LIVE_EDITOR_ADOPTION_READINESS.md`

Document:

- current project/runtime/installation states shown above;
- this PR proves only descriptor/readiness compatibility;
- no Godot product files or runtime evidence exist;
- future real adoption requires explicit product-project approval, first approved `project.godot` and main Scene, fresh version/platform/source/test audit, a separate descriptor transition PR, and then the Base runtime workflow;
- 3×3, Stock/mana, Frostbloom, mobile direction, approved Decisions, assets, and Sheet remain unchanged;
- removal is a revert of the four readiness files.

- [ ] Run focused test and commit.

---

### Task 5: Add static PR/push validation workflow

**Create:** `.github/workflows/validate-godot-live-editor-readiness.yml`

```yaml
name: Validate Godot Live-Editor Readiness

on:
  pull_request:
    branches: [main]
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read

jobs:
  readiness-contract:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
          persist-credentials: false
      - uses: actions/checkout@v4
        with:
          repository: alsdmlals4-eng/Base
          ref: BASE_C0_SHA
          path: _base_c0
          persist-credentials: false
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: python -m pip install --disable-pip-version-check pytest==8.3.5 jsonschema==4.23.0
      - run: python -m pytest tests/test_godot_live_editor_readiness.py -q
      - name: Validate preproject descriptor
        run: |
          python - <<'PY'
          import sys
          from pathlib import Path
          sys.path.insert(0, "_base_c0")
          from tools.godot_project_pilot_descriptor import load_descriptor
          descriptor = load_descriptor(Path(".godot-live-editor/project-pilot.json"))
          if descriptor.is_runtime_project:
              raise SystemExit("runtime project claim is forbidden")
          PY
```

- [ ] Generate `ref:` from the Program A ledger SHA; never commit the literal token.
- [ ] Workflow must contain no Godot binary, reusable runtime workflow, Pilot runner, scratch Scene, or artifact pretending to be runtime evidence.
- [ ] Run focused test and `git diff --check`; commit when GREEN.

---

### Task 6: Review and merge readiness independently

```bash
python -m pytest tests/test_godot_live_editor_readiness.py -q
python -m unittest discover -s tests -p 'test_*.py'
git diff --check
```

- [ ] Verify exactly four readiness files and continued absence of product project files.
- [ ] Open a Draft PR stating:

```yaml
product_project: NOT_CREATED
runtime_pilot: NOT_APPLICABLE
runtime_evidence: NONE_BY_DESIGN
adapter_installation: FORBIDDEN_UNTIL_PRODUCT_PROJECT_APPROVAL
production_adapter_ready: NOT_READY
```

- [ ] Reject any runtime-looking artifact or PASS claim.
- [ ] Require exact-head CI and zero unresolved threads.
- [ ] Merge only after explicit user approval.

---

### Task 7: Capture post-merge static evidence

- [ ] Wait for the push-triggered readiness workflow on the squash-merged GRIMOIRE commit.
- [ ] Verify workflow source SHA equals the merged commit and Base checkout ref equals the ledger C0 SHA.
- [ ] Record:

```yaml
repository: alsdmlals4-eng/GRIMOIRE-
validated_pr_head_sha: exact PR head
merged_commit_sha: exact squash merge
postmerge_workflow_run_id: integer
postmerge_artifact_id: null
base_c0_sha: exact ledger C0 SHA
project_state: NOT_CREATED
result: NOT_APPLICABLE
```

This static post-merge entry is the only GRIMOIRE input to Base C1.
