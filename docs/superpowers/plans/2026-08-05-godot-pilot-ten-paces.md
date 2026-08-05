# Ten Paces Godot Project Pilot Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Prove the Base C0 transaction adapter in a disposable copy of Ten Paces while preserving the source Godot AI 3.0.5 addon, `_mcp_game_helper` Autoload, combat implementation, planning canon, and active vertical-slice work unchanged.

**Architecture:** The project PR adds only a closed descriptor, adoption document, focused test, and exact-SHA caller workflow. The Base runner inventories the source checkout, copies it, removes `res://addons/godot_ai/plugin.cfg` and `_mcp_game_helper` only from the copy, opens the configured combat preview main Scene read-only, and performs mutation/Undo/save only in a runner-owned scratch Scene.

**Tech Stack:** Godot 4.7.1 stable, GDScript, Python 3.12/pytest, GitHub Actions reusable workflow, existing `res://tests/verify_step0.gd` smoke proof.

## Global Constraints

- Repository: `alsdmlals4-eng/Ten-Paces-Hidden-Moves`.
- Plan-creation audit baseline: `4b5967dee99592de4a09a611068344994e1ee026`; execution starts from then-current `main`.
- Existing `project.godot` enables `res://addons/godot_ai/plugin.cfg` and `_mcp_game_helper`.
- Source Godot AI files, plugin enablement, and Autoload remain unchanged.
- Disposable workspace must prove both legacy entries are inactive before Base adapter activation.
- Real configured main Scene is read-only; `node.rename` may target only `res://.godot-live-editor-pilot/scratch.tscn`.
- Allowed source changes are exactly:
  - `.godot-live-editor/project-pilot.json`
  - `docs/GODOT_LIVE_EDITOR_ADOPTION.md`
  - `tests/test_godot_live_editor_adoption.py`
  - `.github/workflows/validate-godot-live-editor-pilot.yml`
- Forbidden source changes include `project.godot`, `addons/`, `data/`, `src/`, `scenes/`, `assets/`, planning canon, and Google Sheets.
- Existing product smoke `res://tests/verify_step0.gd` runs as a bounded behavior check.
- This PR does not migrate, remove, update, configure, or authorize legacy Godot AI as Base v2 authority.
- Merge requires exact-head CI, zero unresolved review threads, unchanged protected paths, and explicit user approval.

---

## File Responsibility Map

- `.godot-live-editor/project-pilot.json`: legacy-conflict descriptor with exact Base C0 pin.
- `docs/GODOT_LIVE_EDITOR_ADOPTION.md`: source-preservation and temporary-disable authority boundary.
- `tests/test_godot_live_editor_adoption.py`: verifies descriptor identity, legacy declarations, immutable workflow pin, and four-file scope.
- `.github/workflows/validate-godot-live-editor-pilot.yml`: local contract job plus Base reusable Pilot job.

---

### Task 1: Freeze exact Base C0 and project refs

**Files:**
- No writes.

**Interfaces:**
- Produces: `BASE_C0_SHA` and `PROJECT_BASELINE_SHA`.

- [ ] **Step 1: Resolve immutable refs**

```bash
export BASE_C0_SHA="$(git ls-remote https://github.com/alsdmlals4-eng/Base refs/heads/main | cut -f1)"
export PROJECT_BASELINE_SHA="$(git ls-remote https://github.com/alsdmlals4-eng/Ten-Paces-Hidden-Moves refs/heads/main | cut -f1)"
gh api "repos/alsdmlals4-eng/Base/contents/.github/workflows/reusable-godot-project-pilot.yml?ref=$BASE_C0_SHA" >/dev/null
git fetch origin main
git switch -c agent/adopt-base-godot-project-pilot "$PROJECT_BASELINE_SHA"
```

- [ ] **Step 2: Confirm Switchy clean Pilot prerequisite**

Fetch the merged Switchy adoption PR and its workflow artifact. Continue only when the exact Base C0 SHA matches this plan's `BASE_C0_SHA` and Switchy evidence records `source_tree_unchanged: PASS` and `base_network_listener: false`.

---

### Task 2: Write the legacy-boundary contract test first

**Files:**
- Create: `tests/test_godot_live_editor_adoption.py`

**Interfaces:**
- Produces: RED until descriptor, document, and workflow exist correctly.

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


def load() -> dict:
    return json.loads(DESCRIPTOR.read_text(encoding="utf-8"))


def test_descriptor_declares_exact_legacy_authority() -> None:
    document = load()
    assert document["project_identity"] == {
        "repository": "alsdmlals4-eng/Ten-Paces-Hidden-Moves",
        "project_id": "ten-paces-hidden-moves",
    }
    assert re.fullmatch(r"[0-9a-f]{40}", document["base_pilot_commit"])
    assert document["legacy_editor_plugins"] == ["res://addons/godot_ai/plugin.cfg"]
    assert document["legacy_autoloads"] == ["_mcp_game_helper"]
    assert document["legacy_disable_mode"] == "TEMPORARY_COPY_ONLY"
    assert document["source_mutation_policy"] == "FORBIDDEN"
    assert document["behavior_checks"] == [
        {
            "kind": "GODOT_SCRIPT",
            "target": "res://tests/verify_step0.gd",
            "timeout_seconds": 60,
        }
    ]


def test_workflow_pin_matches_descriptor() -> None:
    sha = load()["base_pilot_commit"]
    text = WORKFLOW.read_text(encoding="utf-8")
    assert f"alsdmlals4-eng/Base/.github/workflows/reusable-godot-project-pilot.yml@{sha}" in text
    assert f"base_pilot_commit: {sha}" in text
    assert "@main" not in text


def test_document_rejects_dual_authority_and_source_migration() -> None:
    text = DOC.read_text(encoding="utf-8")
    for marker in (
        "LEGACY_GODOT_AI_SOURCE_PRESERVED",
        "LEGACY_DISABLED_IN_DISPOSABLE_COPY_ONLY",
        "DUAL_MUTATION_AUTHORITY_FORBIDDEN",
        "MAIN_SCENE_READ_ONLY",
        "SCRATCH_SCENE_MUTATION_ONLY",
        "PRODUCTION_ADAPTER_READY: NOT_READY",
    ):
        assert marker in text


def test_pr_changes_only_adoption_surfaces() -> None:
    base = subprocess.check_output(["git", "merge-base", "HEAD", "origin/main"], text=True).strip()
    changed = subprocess.check_output(["git", "diff", "--name-only", base, "HEAD"], text=True).splitlines()
    assert set(changed) <= ALLOWED
```

- [ ] **Step 2: Verify RED and commit**

```bash
python -m pytest tests/test_godot_live_editor_adoption.py -q
git add tests/test_godot_live_editor_adoption.py
git commit -m "test: require Ten Paces isolated Godot Pilot"
```

Expected: missing descriptor, document, and workflow failures only.

---

### Task 3: Generate the exact descriptor

**Files:**
- Create: `.godot-live-editor/project-pilot.json`

**Interfaces:**
- Consumes: `BASE_C0_SHA`.
- Produces: a Schema-valid legacy-conflict descriptor.

- [ ] **Step 1: Generate JSON from the immutable SHA**

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
        "repository": "alsdmlals4-eng/Ten-Paces-Hidden-Moves",
        "project_id": "ten-paces-hidden-moves",
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
    "behavior_checks": [
        {
            "kind": "GODOT_SCRIPT",
            "target": "res://tests/verify_step0.gd",
            "timeout_seconds": 60,
        }
    ],
    "expected_platform": "PC",
}
path = Path(".godot-live-editor/project-pilot.json")
path.parent.mkdir(parents=True, exist_ok=True)
path.write_text(json.dumps(document, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
PY
```

- [ ] **Step 2: Validate against Base C0 Schema and run focused test**

Use the exact Base C0 checkout and `load_descriptor()` as defined in the Base C0 plan. Then run:

```bash
python -m pytest tests/test_godot_live_editor_adoption.py -q
```

- [ ] **Step 3: Commit**

```bash
git add .godot-live-editor/project-pilot.json tests/test_godot_live_editor_adoption.py
git commit -m "chore: describe Ten Paces isolated Godot Pilot"
```

---

### Task 4: Document the coexistence boundary

**Files:**
- Create: `docs/GODOT_LIVE_EDITOR_ADOPTION.md`

**Interfaces:**
- Produces: operator and reviewer guidance with no migration claim.

- [ ] **Step 1: Write the exact boundary document**

Required content:

```markdown
# Ten Paces Godot Live-Editor Pilot Adoption

## Status

- `LEGACY_GODOT_AI_SOURCE_PRESERVED`
- `LEGACY_DISABLED_IN_DISPOSABLE_COPY_ONLY`
- `DUAL_MUTATION_AUTHORITY_FORBIDDEN`
- `MAIN_SCENE_READ_ONLY`
- `SCRATCH_SCENE_MUTATION_ONLY`
- `PRODUCTION_ADAPTER_READY: NOT_READY`

## Execution

The pinned Base workflow hashes this checkout, copies it to a disposable workspace, removes only the `godot_ai` EditorPlugin entry and `_mcp_game_helper` Autoload from the copy, activates the Base transaction adapter, inspects the configured combat preview Scene read-only, mutates only a runner-owned scratch Scene, verifies Undo/save/physical hashes/ledger, and proves the source checkout unchanged.

## Non-migration

This PR does not remove, upgrade, configure, or authorize Godot AI 3.0.5. Existing Codex/MCP use remains a legacy external workflow and cannot prove Base v2 completion.

## Protected product boundaries

No combat, route, reward, save, UI, data, Scene, addon, project setting, planning Decision, or Google Sheet changes are included.

## Removal

Revert the four adoption files. No product migration or save conversion is required.
```

- [ ] **Step 2: Run focused tests and commit**

```bash
python -m pytest tests/test_godot_live_editor_adoption.py -q
git add docs/GODOT_LIVE_EDITOR_ADOPTION.md tests/test_godot_live_editor_adoption.py
git commit -m "docs: define Ten Paces Godot Pilot boundary"
```

---

### Task 5: Add the exact caller workflow

**Files:**
- Create: `.github/workflows/validate-godot-live-editor-pilot.yml`

**Interfaces:**
- Produces: local contract job and reusable runtime job.

- [ ] **Step 1: Generate the workflow from `BASE_C0_SHA`**

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
git commit -m "ci: run Ten Paces isolated Godot Pilot"
```

---

### Task 6: Validate runtime evidence and project scope

**Files:**
- No additional writes.

**Interfaces:**
- Produces: one Draft PR and one physically verified legacy-disable evidence artifact.

- [ ] **Step 1: Run focused and existing governance checks**

```bash
python -m pytest tests/test_godot_live_editor_adoption.py -q
python tools/check_project_operating_system.py --root . --config .github/documentation-governance.json
python tools/check_canonical_reference_freshness.py --root . --config .github/reference-freshness.json
python -m unittest discover -s tests -p "test_project_governance.py"
git diff --check
```

- [ ] **Step 2: Confirm changed-file scope**

Expected: exactly the four adoption paths; no protected product path.

- [ ] **Step 3: Open a Draft PR and inspect evidence**

Required runtime evidence:

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

Also verify the behavior check `res://tests/verify_step0.gd` passed in the source checkout and did not write tracked bytes.

- [ ] **Step 4: Adversarially inspect the disposable transform**

Download evidence and confirm the workspace `project.godot` lacks only the two declared legacy entries while the source blob SHA for `project.godot` remains identical to project `main`.

- [ ] **Step 5: Merge only after explicit approval**

Refetch main/head/checks/threads/scope, squash merge with expected head SHA, and record the resulting project main SHA plus workflow run/artifact IDs for Base C1.
