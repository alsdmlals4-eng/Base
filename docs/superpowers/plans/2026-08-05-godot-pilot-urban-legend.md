# Urban-Legend Godot Project Pilot Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Prove the Base C0 scratch-only Editor transaction Pilot against 괴이 기록국 while disabling only the legacy MCP authority in the disposable copy and preserving all project-owned Autoloads, source files, save/runtime contracts, and current canon unchanged.

**Architecture:** The project PR adds only a descriptor, adoption document, focused test, and exact-SHA caller workflow. The Base runner inventories the source checkout, copies it, removes the Godot AI EditorPlugin and `_mcp_game_helper` from the copy only, verifies `UrbanLegendState`, `ValidationSession`, and `GameState` remain configured, opens `res://scenes/main_menu.tscn` read-only, mutates only a runner-owned scratch Scene, and emits bounded physical evidence.

**Tech Stack:** Godot 4.7.1 stable, GDScript, Python 3.12/pytest, GitHub Actions reusable workflow, Base C0 descriptor/workspace/evidence contracts.

## Global Constraints

- Repository: `alsdmlals4-eng/urban-legend`.
- Plan-creation audit baseline: `f7edb459938bb5f3e2533ad828c2fe55019cd14b`; execution starts from then-current `main`.
- Existing main Scene: `res://scenes/main_menu.tscn`, read-only in the Pilot.
- Existing source Autoloads:
  - `UrbanLegendState`
  - `ValidationSession`
  - `GameState`
  - `_mcp_game_helper`
- Only `_mcp_game_helper` may be disabled in the disposable copy. The three project-owned Autoloads must remain byte-equivalent in the transformed `project.godot` except for line-position changes that the strict transformer should not introduce.
- Existing `res://addons/godot_ai/plugin.cfg` remains in source and is disabled only in the disposable copy.
- Descriptor `behavior_checks` is empty; existing project CI remains independent and must stay green.
- Allowed source changes are exactly:
  - `.godot-live-editor/project-pilot.json`
  - `docs/GODOT_LIVE_EDITOR_ADOPTION.md`
  - `tests/test_godot_live_editor_adoption.py`
  - `.github/workflows/validate-godot-live-editor-pilot.yml`
- Forbidden source changes include `project.godot`, `addons/`, `scripts/`, `scenes/`, `data/`, `assets/`, `knowledge/base-pack/`, save/version fields, current canon, generated GDD/DOCX, and Google Sheets.
- A successful Pilot proves only disposable-copy compatibility. It does not authorize product mutation, save migration, legacy MCP replacement, Program B, Program C, or production readiness.
- Merge requires exact-head CI, zero unresolved threads, protected-path proof, physical artifact verification, and explicit user approval.

---

## File Responsibility Map

- `.godot-live-editor/project-pilot.json`: exact Base C0 pin and declared legacy authority only.
- `docs/GODOT_LIVE_EDITOR_ADOPTION.md`: Autoload-preservation and source-protection contract.
- `tests/test_godot_live_editor_adoption.py`: validates immutable pin, legacy declaration, protected paths, and required evidence markers.
- `.github/workflows/validate-godot-live-editor-pilot.yml`: local contract job plus exact reusable Base Pilot.

---

### Task 1: Freeze exact refs and prerequisite evidence

**Files:**
- No writes.

**Interfaces:**
- Produces: exact Base C0 and project baseline SHAs.

- [ ] **Step 1: Resolve refs and create the isolated branch**

```bash
export BASE_C0_SHA="$(git ls-remote https://github.com/alsdmlals4-eng/Base refs/heads/main | cut -f1)"
export PROJECT_BASELINE_SHA="$(git ls-remote https://github.com/alsdmlals4-eng/urban-legend refs/heads/main | cut -f1)"
gh api "repos/alsdmlals4-eng/Base/contents/.github/workflows/reusable-godot-project-pilot.yml?ref=$BASE_C0_SHA" >/dev/null
git fetch origin main
git switch -c agent/adopt-base-godot-project-pilot "$PROJECT_BASELINE_SHA"
```

- [ ] **Step 2: Confirm Switchy clean-Pilot prerequisite**

Fetch the merged Switchy Pilot and evidence artifact. Require the same Base C0 SHA, runtime PASS, unchanged source, and no Base listener before continuing.

---

### Task 2: Write the Autoload-preservation contract test first

**Files:**
- Create: `tests/test_godot_live_editor_adoption.py`

**Interfaces:**
- Produces: RED until the other three adoption files exist and source-protection rules are satisfied.

- [ ] **Step 1: Create the failing test**

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
PROTECTED_PREFIXES = (
    "addons/",
    "scripts/",
    "scenes/",
    "data/",
    "assets/",
    "knowledge/base-pack/",
)
PROTECTED_FILES = {"project.godot"}


def load_descriptor() -> dict:
    return json.loads(DESCRIPTOR.read_text(encoding="utf-8"))


def changed_files() -> list[str]:
    base = subprocess.check_output(["git", "merge-base", "HEAD", "origin/main"], text=True).strip()
    return subprocess.check_output(["git", "diff", "--name-only", base, "HEAD"], text=True).splitlines()


def test_descriptor_declares_only_legacy_mcp_authority() -> None:
    document = load_descriptor()
    assert document["project_identity"] == {
        "repository": "alsdmlals4-eng/urban-legend",
        "project_id": "urban-legend",
    }
    assert re.fullmatch(r"[0-9a-f]{40}", document["base_pilot_commit"])
    assert document["legacy_editor_plugins"] == ["res://addons/godot_ai/plugin.cfg"]
    assert document["legacy_autoloads"] == ["_mcp_game_helper"]
    assert "UrbanLegendState" not in document["legacy_autoloads"]
    assert "ValidationSession" not in document["legacy_autoloads"]
    assert "GameState" not in document["legacy_autoloads"]
    assert document["behavior_checks"] == []
    assert document["source_mutation_policy"] == "FORBIDDEN"


def test_document_requires_project_autoload_preservation() -> None:
    text = DOC.read_text(encoding="utf-8")
    for marker in (
        "PROJECT_AUTOLOADS_PRESERVED",
        "UrbanLegendState",
        "ValidationSession",
        "GameState",
        "MCP_AUTOLOAD_DISABLED_IN_DISPOSABLE_COPY_ONLY",
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


def test_pr_changes_only_adoption_surfaces() -> None:
    changed = changed_files()
    assert set(changed) <= ALLOWED
    assert not any(path in PROTECTED_FILES for path in changed)
    assert not any(path.startswith(PROTECTED_PREFIXES) for path in changed)
```

- [ ] **Step 2: Verify RED and commit**

```bash
python -m pytest tests/test_godot_live_editor_adoption.py -q
git add tests/test_godot_live_editor_adoption.py
git commit -m "test: require urban-legend isolated Godot Pilot"
```

Expected: missing descriptor, document, and workflow failures only.

---

### Task 3: Generate the exact descriptor

**Files:**
- Create: `.godot-live-editor/project-pilot.json`

**Interfaces:**
- Produces: a descriptor that disables only the MCP Autoload and Godot AI plugin in the disposable copy.

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
        "repository": "alsdmlals4-eng/urban-legend",
        "project_id": "urban-legend",
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

- [ ] **Step 2: Validate using the exact Base C0 Schema/loader**

Checkout the Schema and `tools/godot_project_pilot_descriptor.py` at `BASE_C0_SHA`, call `load_descriptor()` on this file, and require success.

- [ ] **Step 3: Run focused test and commit**

```bash
python -m pytest tests/test_godot_live_editor_adoption.py -q
git add .godot-live-editor/project-pilot.json tests/test_godot_live_editor_adoption.py
git commit -m "chore: describe urban-legend isolated Godot Pilot"
```

---

### Task 4: Document Autoload and source preservation

**Files:**
- Create: `docs/GODOT_LIVE_EDITOR_ADOPTION.md`

**Interfaces:**
- Produces: operator guidance that distinguishes the project state owners from the legacy MCP helper.

- [ ] **Step 1: Write the required document**

```markdown
# 괴이 기록국 Godot Live-Editor Pilot Adoption

## Status

- `LEGACY_GODOT_AI_SOURCE_PRESERVED`
- `MCP_AUTOLOAD_DISABLED_IN_DISPOSABLE_COPY_ONLY`
- `PROJECT_AUTOLOADS_PRESERVED`
- `UrbanLegendState`
- `ValidationSession`
- `GameState`
- `MAIN_SCENE_READ_ONLY`
- `SCRATCH_SCENE_MUTATION_ONLY`
- `PRODUCTION_ADAPTER_READY: NOT_READY`

## Execution boundary

The exact Base C0 workflow hashes this source checkout, copies it, disables only `res://addons/godot_ai/plugin.cfg` and `_mcp_game_helper` in the copy, verifies the three project-owned Autoloads remain configured, opens `res://scenes/main_menu.tscn` read-only, mutates only a runner-owned scratch Scene, verifies Undo/save/physical hashes/ledger, and proves the source checkout unchanged.

## Protected behavior

This PR does not change campaign/save state, episodes, investigation/stabilization rules, current canon, UI, assets, project settings, GDD/DOCX generation, or Google Sheets. A Pilot PASS is not a product implementation or migration approval.

## Follow-up and removal

Permanent adapter installation, legacy MCP migration, transport, debugger, or save/runtime changes require separate approval. Revert the four adoption files to remove this Pilot integration.
```

- [ ] **Step 2: Run focused test and commit**

```bash
python -m pytest tests/test_godot_live_editor_adoption.py -q
git add docs/GODOT_LIVE_EDITOR_ADOPTION.md tests/test_godot_live_editor_adoption.py
git commit -m "docs: define urban-legend Godot Pilot boundary"
```

---

### Task 5: Add the exact caller workflow

**Files:**
- Create: `.github/workflows/validate-godot-live-editor-pilot.yml`

**Interfaces:**
- Produces: local contract validation and Base reusable runtime evidence.

- [ ] **Step 1: Generate workflow from `BASE_C0_SHA`**

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
git commit -m "ci: run urban-legend isolated Godot Pilot"
```

---

### Task 6: Validate runtime and transformed Autoload evidence

**Files:**
- No additional writes.

**Interfaces:**
- Produces: one Draft PR and one evidence artifact proving selective legacy disablement.

- [ ] **Step 1: Run focused and existing project gates**

```bash
python -m pytest tests/test_godot_live_editor_adoption.py -q
python -m unittest discover -s tests -p 'test_*.py'
git diff --check
```

Run the repository's existing workflows unchanged. Do not patch product files to make unrelated historical tests pass.

- [ ] **Step 2: Confirm exact four-file scope and open a Draft PR**

The PR body records exact Base C0 SHA, source `project.godot` blob SHA, no protected paths changed, and merge authorization not granted.

- [ ] **Step 3: Physically inspect the workflow artifact**

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
project_autoloads_preserved:
  UrbanLegendState: true
  ValidationSession: true
  GameState: true
base_network_listener: false
```

Inspect the transformed disposable `project.godot` evidence and verify `_mcp_game_helper` plus the Godot AI plugin are absent while the three project Autoload lines remain exact. Verify the source `project.godot` blob SHA did not change.

- [ ] **Step 4: Handle bounded pre-existing failure honestly**

If one preserved Autoload prevents load in the current Linux headless environment, record `PROJECT_LOAD_BLOCKED_PREEXISTING` with bounded logs. Do not remove that project Autoload or edit source to fabricate a PASS.

- [ ] **Step 5: Merge only after explicit approval**

Refetch current main, exact head, CI, review threads, scope, and evidence. Squash merge with expected head SHA and record the merged project SHA plus workflow run/artifact IDs for Base C1.
