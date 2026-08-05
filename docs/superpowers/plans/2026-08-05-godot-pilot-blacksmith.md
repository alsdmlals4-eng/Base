# Blacksmith Godot Project Pilot Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Prove that the Base C0 Pilot can load Blacksmith and exercise the scratch-only Editor transaction boundary while preserving the project's explicit product-implementation block and every protected product path.

**Architecture:** The source PR contains only operational adoption metadata, a focused contract test, documentation, and a caller workflow. The reusable Base workflow hashes the source checkout, creates a disposable copy, disables Godot AI and `_mcp_game_helper` only in that copy, inspects the configured enhancement-test Scene read-only, and performs rename/Undo/save only in the runner-owned scratch Scene.

**Tech Stack:** Godot 4.7.1 stable, GDScript, Python 3.12/pytest, GitHub Actions reusable workflow, Base C0 descriptor and evidence contracts.

## Global Constraints

- Repository: `alsdmlals4-eng/Blacksmith`.
- Plan-creation audit baseline: `b1dd945875568098b107815a03e88b0272d384e9`; execution starts from then-current `main`.
- Current authority states product implementation is `BLOCKED` during total planning.
- Protected source paths are `data/`, `scripts/`, `scenes/`, `assets/`, `addons/`, and `project.godot`.
- Existing main Scene `res://scenes/test/enhancement_test.tscn` is read-only during the Pilot.
- Existing source Godot AI and `_mcp_game_helper` remain unchanged; both are disabled only in the disposable copy.
- Descriptor `behavior_checks` is empty. The Pilot must not expand this operational PR into product testing or implementation authority.
- Allowed source changes are exactly:
  - `.godot-live-editor/project-pilot.json`
  - `docs/GODOT_LIVE_EDITOR_ADOPTION.md`
  - `tests/test_godot_live_editor_adoption.py`
  - `.github/workflows/validate-godot-live-editor-pilot.yml`
- No current planning Decision, Game Bible, R2 Registry, product data, product code, Scene, asset, addon, project setting, or Google Sheet changes are authorized.
- A successful Pilot proves only operational compatibility in a disposable copy.
- Merge requires explicit user approval.

---

## File Responsibility Map

- `.godot-live-editor/project-pilot.json`: exact Base pin and blocked-product Pilot classification.
- `docs/GODOT_LIVE_EDITOR_ADOPTION.md`: explains why the Pilot is not product implementation.
- `tests/test_godot_live_editor_adoption.py`: rejects protected-path changes, behavior-check expansion, dual authority, and floating Base refs.
- `.github/workflows/validate-godot-live-editor-pilot.yml`: local contract plus exact Base reusable workflow.

---

### Task 1: Freeze refs and prove prerequisites

**Files:**
- No writes.

**Interfaces:**
- Produces: exact `BASE_C0_SHA` and project baseline.

- [ ] **Step 1: Resolve current refs**

```bash
export BASE_C0_SHA="$(git ls-remote https://github.com/alsdmlals4-eng/Base refs/heads/main | cut -f1)"
export PROJECT_BASELINE_SHA="$(git ls-remote https://github.com/alsdmlals4-eng/Blacksmith refs/heads/main | cut -f1)"
gh api "repos/alsdmlals4-eng/Base/contents/.github/workflows/reusable-godot-project-pilot.yml?ref=$BASE_C0_SHA" >/dev/null
git fetch origin main
git switch -c agent/adopt-base-godot-project-pilot "$PROJECT_BASELINE_SHA"
```

- [ ] **Step 2: Verify clean-Pilot prerequisite**

Fetch the merged Switchy Pilot evidence and confirm it used the same Base C0 SHA. If Switchy is not merged with runtime PASS, stop.

---

### Task 2: Write the blocked-product adoption test first

**Files:**
- Create: `tests/test_godot_live_editor_adoption.py`

**Interfaces:**
- Produces: RED until the three other adoption files exist and all product boundaries are preserved.

- [ ] **Step 1: Create the test**

```python
from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DESCRIPTOR = ROOT / ".godot-live-editor/project-pilot.json"
WORKFLOW = ROOT / ".github/workflows/validate-godot-live-editor-pilot.yml"
DOC = ROOT / "docs/GODOT_LIVE_EDITOR_ADOPTION.md"
ALLOWED = {
    ".godot-live-editor/project-pilot.json",
    "docs/GODOT_LIVE_EDITOR_ADOPTION.md",
    "tests/test_godot_live_editor_adoption.py",
    ".github/workflows/validate-godot-live-editor-pilot.yml",
}
PROTECTED_PREFIXES = ("data/", "scripts/", "scenes/", "assets/", "addons/")
PROTECTED_FILES = {"project.godot"}


def descriptor() -> dict:
    return json.loads(DESCRIPTOR.read_text(encoding="utf-8"))


def changed_files() -> list[str]:
    base = subprocess.check_output(["git", "merge-base", "HEAD", "origin/main"], text=True).strip()
    return subprocess.check_output(["git", "diff", "--name-only", base, "HEAD"], text=True).splitlines()


def test_descriptor_preserves_blocked_product_state() -> None:
    document = descriptor()
    assert document["project_identity"] == {
        "repository": "alsdmlals4-eng/Blacksmith",
        "project_id": "blacksmith",
    }
    assert re.fullmatch(r"[0-9a-f]{40}", document["base_pilot_commit"])
    assert document["legacy_editor_plugins"] == ["res://addons/godot_ai/plugin.cfg"]
    assert document["legacy_autoloads"] == ["_mcp_game_helper"]
    assert document["behavior_checks"] == []
    assert document["source_mutation_policy"] == "FORBIDDEN"
    assert document["expected_platform"] == "ANDROID"


def test_adoption_document_rejects_product_authority() -> None:
    text = DOC.read_text(encoding="utf-8")
    for marker in (
        "PRODUCT_IMPLEMENTATION_BLOCKED",
        "OPERATIONAL_VALIDATION_ONLY",
        "LEGACY_DISABLED_IN_DISPOSABLE_COPY_ONLY",
        "MAIN_SCENE_READ_ONLY",
        "SCRATCH_SCENE_MUTATION_ONLY",
        "PRODUCTION_ADAPTER_READY: NOT_READY",
    ):
        assert marker in text


def test_workflow_uses_exact_base_pin() -> None:
    sha = descriptor()["base_pilot_commit"]
    text = WORKFLOW.read_text(encoding="utf-8")
    assert f"alsdmlals4-eng/Base/.github/workflows/reusable-godot-project-pilot.yml@{sha}" in text
    assert f"base_pilot_commit: {sha}" in text
    assert "@main" not in text


def test_pr_does_not_touch_protected_product_paths() -> None:
    changed = changed_files()
    assert set(changed) <= ALLOWED
    assert not any(path in PROTECTED_FILES for path in changed)
    assert not any(path.startswith(PROTECTED_PREFIXES) for path in changed)
```

- [ ] **Step 2: Verify RED and commit**

```bash
python -m pytest tests/test_godot_live_editor_adoption.py -q
git add tests/test_godot_live_editor_adoption.py
git commit -m "test: require Blacksmith isolated Godot Pilot"
```

---

### Task 3: Generate the exact descriptor

**Files:**
- Create: `.godot-live-editor/project-pilot.json`

**Interfaces:**
- Produces: a blocked-product, temporary-copy-only descriptor.

- [ ] **Step 1: Generate JSON from `BASE_C0_SHA`**

```bash
export BASE_C0_SHA
python - <<'PY'
import json, os
from pathlib import Path
sha = os.environ["BASE_C0_SHA"]
if len(sha) != 40 or any(c not in "0123456789abcdef" for c in sha):
    raise SystemExit("invalid BASE_C0_SHA")
document = {
    "schema_version": "1",
    "project_identity": {
        "repository": "alsdmlals4-eng/Blacksmith",
        "project_id": "blacksmith",
    },
    "base_pilot_commit": sha,
    "project_state": "EXISTING_GODOT_PROJECT",
    "godot": {
        "version": "4.7.1-stable",
        "archive_sha256": "c7ff14fd28472c8d4f193043de30278dcf7e5241a1dcf7566b02e27addaa33ba",
    },
    "project_file": "project.godot",
    "main_scene_source": "application/run/main_scene",
    "legacy_editor_plugins": ["res://addons/godot_ai/plugin.cfg"],
    "legacy_autoloads": ["_mcp_game_helper"],
    "legacy_disable_mode": "TEMPORARY_COPY_ONLY",
    "source_mutation_policy": "FORBIDDEN",
    "scratch_scene_path": "res://.godot-live-editor-pilot/scratch.tscn",
    "behavior_checks": [],
    "expected_platform": "ANDROID",
}
path = Path(".godot-live-editor/project-pilot.json")
path.parent.mkdir(parents=True, exist_ok=True)
path.write_text(json.dumps(document, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
PY
```

- [ ] **Step 2: Validate with Base C0 loader and commit**

```bash
python -m pytest tests/test_godot_live_editor_adoption.py -q
git add .godot-live-editor/project-pilot.json tests/test_godot_live_editor_adoption.py
git commit -m "chore: describe Blacksmith isolated Godot Pilot"
```

Expected: descriptor assertions pass; document/workflow remain RED.

---

### Task 4: Write the operational-only adoption document

**Files:**
- Create: `docs/GODOT_LIVE_EDITOR_ADOPTION.md`

**Interfaces:**
- Produces: explicit separation between operational validation and blocked product implementation.

- [ ] **Step 1: Add the required content**

```markdown
# Blacksmith Godot Live-Editor Pilot Adoption

## Status

- `PRODUCT_IMPLEMENTATION_BLOCKED`
- `OPERATIONAL_VALIDATION_ONLY`
- `LEGACY_GODOT_AI_SOURCE_PRESERVED`
- `LEGACY_DISABLED_IN_DISPOSABLE_COPY_ONLY`
- `MAIN_SCENE_READ_ONLY`
- `SCRATCH_SCENE_MUTATION_ONLY`
- `PRODUCTION_ADAPTER_READY: NOT_READY`

## Boundary

This Pilot does not authorize product code, data, Scene, asset, addon, project setting, economy, strengthening, crafting, save, or Game Bible changes. It only tests whether the Base transaction adapter can operate in a disposable copy while the source tree remains byte-identical.

## Execution

The pinned Base workflow inventories source bytes, copies the repository, disables only `godot_ai` and `_mcp_game_helper` in the copy, inspects the configured enhancement-test Scene read-only, mutates only a runner-owned scratch Scene, verifies Undo/save/hash/ledger, and discards the copy.

## Evidence and removal

Evidence is a workflow artifact. Revert the four adoption files to remove this integration; no product migration or save conversion is required.
```

- [ ] **Step 2: Run focused test and commit**

```bash
python -m pytest tests/test_godot_live_editor_adoption.py -q
git add docs/GODOT_LIVE_EDITOR_ADOPTION.md tests/test_godot_live_editor_adoption.py
git commit -m "docs: define Blacksmith Godot Pilot boundary"
```

---

### Task 5: Generate the exact caller workflow

**Files:**
- Create: `.github/workflows/validate-godot-live-editor-pilot.yml`

**Interfaces:**
- Produces: local scope test and reusable runtime Pilot.

- [ ] **Step 1: Write the workflow from the same immutable SHA**

```bash
export BASE_C0_SHA
python - <<'PY'
import os
from pathlib import Path
sha = os.environ["BASE_C0_SHA"]
text = f'''name: Validate Godot Live-Editor Pilot

on:
  pull_request:
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
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: python -m pip install --disable-pip-version-check pytest==8.3.5
      - run: python -m pytest tests/test_godot_live_editor_adoption.py -q

  project-pilot:
    needs: adoption-contract
    uses: alsdmlals4-eng/Base/.github/workflows/reusable-godot-project-pilot.yml@{sha}
    with:
      base_pilot_commit: {sha}
      descriptor_path: .godot-live-editor/project-pilot.json
      artifact_retention_days: 14
'''
Path(".github/workflows/validate-godot-live-editor-pilot.yml").write_text(text, encoding="utf-8")
PY
```

- [ ] **Step 2: Run GREEN and commit**

```bash
python -m pytest tests/test_godot_live_editor_adoption.py -q
git diff --check
git add .github/workflows/validate-godot-live-editor-pilot.yml tests/test_godot_live_editor_adoption.py
git commit -m "ci: run Blacksmith isolated Godot Pilot"
```

---

### Task 6: Validate the Draft PR without violating the product block

**Files:**
- No additional writes.

**Interfaces:**
- Produces: exact runtime evidence or a bounded pre-existing load blocker.

- [ ] **Step 1: Run project governance tests**

```bash
python -m pytest tests/test_godot_live_editor_adoption.py -q
python -m unittest discover -s tests -p 'test_*.py'
git diff --check
```

Do not change product paths to fix an unrelated existing test failure. Separate pre-existing failures in the PR body.

- [ ] **Step 2: Confirm exact four-file scope**

No `data/`, `scripts/`, `scenes/`, `assets/`, `addons/`, or `project.godot` path may appear in the diff.

- [ ] **Step 3: Open a Draft PR and inspect evidence**

Required PASS evidence when the project loads:

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

If the current project has a pre-existing load failure, record `PROJECT_LOAD_BLOCKED_PREEXISTING` with bounded logs and keep product files unchanged.

- [ ] **Step 4: Merge only after explicit approval**

Refetch exact head, current main, checks, review threads, and changed files. Squash merge with expected head SHA and record the merged project SHA plus run/artifact IDs for Base C1.
