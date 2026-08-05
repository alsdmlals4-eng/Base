# OMENWARD Godot Project Pilot Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Validate OMENWARD's compatibility with the Base C0 scratch-only Editor transaction Pilot while preserving `TOTAL_PLANNING`, `product_code_authority: NONE`, all current planning Decisions, and every product file unchanged.

**Architecture:** The project PR contains only operational adoption metadata, documentation, a focused contract test, and an exact-SHA caller workflow. The reusable Base workflow inventories the source checkout, copies it, disables the legacy Godot AI EditorPlugin and `_mcp_game_helper` only in the disposable copy, inspects `res://scenes/main/main.tscn` read-only, mutates only the runner-owned scratch Scene, and discards the copy after bounded evidence capture.

**Tech Stack:** Godot 4.7.1 stable, GDScript, Python 3.12/pytest, GitHub Actions reusable workflow, Base C0 descriptor and physical-evidence contracts.

## Global Constraints

- Repository: `alsdmlals4-eng/omenward`.
- Plan-creation audit baseline: `da382d52b4490acb8758a1683ea6c9e4f4bf388b`; execution starts from then-current `main`.
- Current authority: `work_mode: TOTAL_PLANNING`, `product_code_authority: NONE`.
- Existing main Scene: `res://scenes/main/main.tscn`, read-only in Program A.
- Existing source authority includes Godot AI `res://addons/godot_ai/plugin.cfg` and `_mcp_game_helper`; both remain unchanged in source and are disabled only in the disposable copy.
- Descriptor `behavior_checks` is empty because this operational PR has no product-code authority.
- Allowed source changes are exactly:
  - `.godot-live-editor/project-pilot.json`
  - `docs/GODOT_LIVE_EDITOR_ADOPTION.md`
  - `tests/test_godot_live_editor_adoption.py`
  - `.github/workflows/validate-godot-live-editor-pilot.yml`
- Forbidden changes include `project.godot`, `addons/`, `scenes/`, `scripts/`, `src/`, `data/`, `assets/`, product Resource files, current planning canon, exact game values, and Google Sheets.
- A PASS proves disposable-copy operational compatibility only. It does not authorize product implementation or mark the production adapter ready.
- Merge requires exact-head CI, protected-path proof, zero unresolved review threads, and explicit user approval.

---

## File Responsibility Map

- `.godot-live-editor/project-pilot.json`: exact Base C0 pin and planning-only Pilot classification.
- `docs/GODOT_LIVE_EDITOR_ADOPTION.md`: operational-only and no-product-authority boundary.
- `tests/test_godot_live_editor_adoption.py`: validates descriptor, empty behavior checks, immutable pin, and four-file scope.
- `.github/workflows/validate-godot-live-editor-pilot.yml`: local contract job and exact Base reusable Pilot call.

---

### Task 1: Freeze exact refs and prerequisites

**Files:**
- No writes.

**Interfaces:**
- Produces: exact `BASE_C0_SHA` and OMENWARD baseline SHA.

- [ ] **Step 1: Resolve refs and create a branch**

```bash
export BASE_C0_SHA="$(git ls-remote https://github.com/alsdmlals4-eng/Base refs/heads/main | cut -f1)"
export PROJECT_BASELINE_SHA="$(git ls-remote https://github.com/alsdmlals4-eng/omenward refs/heads/main | cut -f1)"
gh api "repos/alsdmlals4-eng/Base/contents/.github/workflows/reusable-godot-project-pilot.yml?ref=$BASE_C0_SHA" >/dev/null
git fetch origin main
git switch -c agent/adopt-base-godot-project-pilot "$PROJECT_BASELINE_SHA"
```

- [ ] **Step 2: Verify Switchy clean-Pilot prerequisite**

Fetch the merged Switchy Pilot evidence. Continue only if it pins the same Base C0 SHA and records runtime PASS, unchanged source, and no Base listener.

---

### Task 2: Write the planning-only adoption test first

**Files:**
- Create: `tests/test_godot_live_editor_adoption.py`

**Interfaces:**
- Produces: RED until descriptor, documentation, and workflow are present and product paths remain untouched.

- [ ] **Step 1: Add the failing test**

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
PROTECTED_PREFIXES = ("addons/", "scenes/", "scripts/", "src/", "data/", "assets/")
PROTECTED_FILES = {"project.godot"}


def load_descriptor() -> dict:
    return json.loads(DESCRIPTOR.read_text(encoding="utf-8"))


def changed_files() -> list[str]:
    base = subprocess.check_output(["git", "merge-base", "HEAD", "origin/main"], text=True).strip()
    return subprocess.check_output(["git", "diff", "--name-only", base, "HEAD"], text=True).splitlines()


def test_descriptor_preserves_planning_only_authority() -> None:
    document = load_descriptor()
    assert document["project_identity"] == {
        "repository": "alsdmlals4-eng/omenward",
        "project_id": "omenward",
    }
    assert re.fullmatch(r"[0-9a-f]{40}", document["base_pilot_commit"])
    assert document["legacy_editor_plugins"] == ["res://addons/godot_ai/plugin.cfg"]
    assert document["legacy_autoloads"] == ["_mcp_game_helper"]
    assert document["behavior_checks"] == []
    assert document["source_mutation_policy"] == "FORBIDDEN"
    assert document["expected_platform"] == "PC"


def test_document_denies_product_code_authority() -> None:
    text = DOC.read_text(encoding="utf-8")
    for marker in (
        "TOTAL_PLANNING_UNCHANGED",
        "PRODUCT_CODE_AUTHORITY: NONE",
        "OPERATIONAL_VALIDATION_ONLY",
        "LEGACY_DISABLED_IN_DISPOSABLE_COPY_ONLY",
        "MAIN_SCENE_READ_ONLY",
        "SCRATCH_SCENE_MUTATION_ONLY",
        "PRODUCTION_ADAPTER_READY: NOT_READY",
    ):
        assert marker in text


def test_workflow_uses_exact_base_pin() -> None:
    sha = load_descriptor()["base_pilot_commit"]
    text = WORKFLOW.read_text(encoding="utf-8")
    assert f"alsdmlals4-eng/Base/.github/workflows/reusable-godot-project-pilot.yml@{sha}" in text
    assert f"base_pilot_commit: {sha}" in text
    assert "@main" not in text


def test_pr_changes_only_operational_adoption_files() -> None:
    changed = changed_files()
    assert set(changed) <= ALLOWED
    assert not any(path in PROTECTED_FILES for path in changed)
    assert not any(path.startswith(PROTECTED_PREFIXES) for path in changed)
```

- [ ] **Step 2: Verify RED and commit**

```bash
python -m pytest tests/test_godot_live_editor_adoption.py -q
git add tests/test_godot_live_editor_adoption.py
git commit -m "test: require OMENWARD isolated Godot Pilot"
```

Expected: missing descriptor, document, and workflow failures only.

---

### Task 3: Generate the exact planning-only descriptor

**Files:**
- Create: `.godot-live-editor/project-pilot.json`

**Interfaces:**
- Produces: a Schema-valid descriptor with no product behavior commands.

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
        "repository": "alsdmlals4-eng/omenward",
        "project_id": "omenward",
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
    "expected_platform": "PC",
}
path = Path(".godot-live-editor/project-pilot.json")
path.parent.mkdir(parents=True, exist_ok=True)
path.write_text(json.dumps(document, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
PY
```

- [ ] **Step 2: Validate with the exact Base C0 loader**

Checkout only the Base C0 Schema and descriptor loader at `BASE_C0_SHA`, call `load_descriptor(Path('.godot-live-editor/project-pilot.json'))`, and require success.

- [ ] **Step 3: Run focused test and commit**

```bash
python -m pytest tests/test_godot_live_editor_adoption.py -q
git add .godot-live-editor/project-pilot.json tests/test_godot_live_editor_adoption.py
git commit -m "chore: describe OMENWARD isolated Godot Pilot"
```

---

### Task 4: Document the no-product-authority boundary

**Files:**
- Create: `docs/GODOT_LIVE_EDITOR_ADOPTION.md`

**Interfaces:**
- Produces: a clear operational validation contract.

- [ ] **Step 1: Write the required document**

```markdown
# OMENWARD Godot Live-Editor Pilot Adoption

## Status

- `TOTAL_PLANNING_UNCHANGED`
- `PRODUCT_CODE_AUTHORITY: NONE`
- `OPERATIONAL_VALIDATION_ONLY`
- `LEGACY_GODOT_AI_SOURCE_PRESERVED`
- `LEGACY_DISABLED_IN_DISPOSABLE_COPY_ONLY`
- `MAIN_SCENE_READ_ONLY`
- `SCRATCH_SCENE_MUTATION_ONLY`
- `PRODUCTION_ADAPTER_READY: NOT_READY`

## Boundary

This adoption PR does not authorize product code, Scene, Resource, game data, exact values, art assets, map systems, roulette systems, economy, save, or planning-canon changes. It validates only a disposable project copy.

## Execution

The exact Base C0 workflow inventories the source tree, copies the project, disables the legacy EditorPlugin and `_mcp_game_helper` in the copy only, inspects `res://scenes/main/main.tscn` read-only, performs rename/Undo/save only on a runner-owned scratch Scene, verifies physical evidence, and proves the source checkout unchanged.

## Follow-up

Permanent adoption, legacy MCP migration, authenticated transport, runtime debugger, or product integration requires separate planning and approval.

## Removal

Revert the four adoption files. No product or save migration is required.
```

- [ ] **Step 2: Run test and commit**

```bash
python -m pytest tests/test_godot_live_editor_adoption.py -q
git add docs/GODOT_LIVE_EDITOR_ADOPTION.md tests/test_godot_live_editor_adoption.py
git commit -m "docs: define OMENWARD Godot Pilot boundary"
```

---

### Task 5: Add the exact caller workflow

**Files:**
- Create: `.github/workflows/validate-godot-live-editor-pilot.yml`

**Interfaces:**
- Produces: local contract validation and reusable Base runtime evidence.

- [ ] **Step 1: Generate workflow from the immutable SHA**

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

- [ ] **Step 2: Verify GREEN and commit**

```bash
python -m pytest tests/test_godot_live_editor_adoption.py -q
git diff --check
git add .github/workflows/validate-godot-live-editor-pilot.yml tests/test_godot_live_editor_adoption.py
git commit -m "ci: run OMENWARD isolated Godot Pilot"
```

---

### Task 6: Validate the Draft PR and runtime evidence

**Files:**
- No additional writes.

**Interfaces:**
- Produces: an operational compatibility result without product implementation claims.

- [ ] **Step 1: Run focused and existing documentation/governance checks**

```bash
python -m pytest tests/test_godot_live_editor_adoption.py -q
python -m unittest discover -s tests -p 'test_*.py'
git diff --check
```

Separate any pre-existing failure; do not change product files to make this Pilot pass.

- [ ] **Step 2: Verify exact four-file scope and open a Draft PR**

The PR body records `TOTAL_PLANNING_UNCHANGED`, `product_code_authority: NONE`, exact Base C0 SHA, no product paths changed, and merge authorization not granted.

- [ ] **Step 3: Inspect the workflow artifact physically**

Required evidence when the project loads:

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

A pre-existing load failure is `PROJECT_LOAD_BLOCKED_PREEXISTING`; it is not permission to edit product files.

- [ ] **Step 4: Merge only after explicit approval**

Refetch current main, exact head, CI, review threads, and changed files. Squash merge with expected head SHA and record the merged project SHA plus workflow run/artifact IDs for Base C1.
