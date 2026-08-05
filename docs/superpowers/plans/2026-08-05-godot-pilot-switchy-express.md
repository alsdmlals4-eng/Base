# Switchy Express Godot Project Pilot Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Adopt the merged Base C0 Pilot workflow in Switchy Express as the first clean real-project proof, without changing product files or enabling a permanent Base editor addon.

**Architecture:** The project PR adds only one closed descriptor, one adoption document, one focused Python contract test, and one caller workflow pinned to the exact Base C0 merge SHA. The reusable Base workflow copies the project to a disposable workspace, loads the real main Scene read-only, mutates only the runner-owned scratch Scene, and uploads evidence; the source checkout remains unchanged.

**Tech Stack:** Godot 4.7.1 stable, GDScript, Python 3.12/pytest, GitHub Actions reusable workflow, existing `res://tests/run_tests.gd` product test runner.

## Global Constraints

- Repository: `alsdmlals4-eng/Switchy-Express-Cargo-Puzzle`.
- Plan-creation audit baseline: `b2ecc7220f4cad546814bcce43e998a45fff5281`; execution starts from then-current `main`.
- This is the first real-project Pilot and must pass before legacy-Godot-AI project Pilots proceed.
- Existing main Scene: `res://game/main/main.tscn` read from `project.godot`.
- Existing product test runner: `res://tests/run_tests.gd`.
- Legacy Godot AI is absent; descriptor legacy plugin/autoload arrays are empty.
- Allowed source changes are exactly:
  - `.godot-live-editor/project-pilot.json`
  - `docs/GODOT_LIVE_EDITOR_ADOPTION.md`
  - `tests/test_godot_live_editor_adoption.py`
  - `.github/workflows/validate-godot-live-editor-pilot.yml`
- Forbidden source changes include `project.godot`, `game/`, `scenes/`, `data/`, `addons/`, `export_presets.cfg`, product tests, and Google Sheets.
- The workflow pins one exact merged Base C0 SHA in both `uses:` and `with.base_pilot_commit`.
- No merge occurs without exact-head CI, zero unresolved threads, source-scope proof, and explicit user approval.

---

## File Responsibility Map

- `.godot-live-editor/project-pilot.json`: immutable project identity and clean-Pilot contract.
- `docs/GODOT_LIVE_EDITOR_ADOPTION.md`: explains temporary-copy execution, evidence, exclusions, and rollback.
- `tests/test_godot_live_editor_adoption.py`: validates the descriptor, immutable Base pin, allowed workflow shape, and forbidden product changes.
- `.github/workflows/validate-godot-live-editor-pilot.yml`: runs the local contract test, then calls the exact Base C0 reusable workflow.

---

### Task 1: Freeze the current project and Base C0 SHAs

**Files:**
- No writes.

**Interfaces:**
- Consumes: merged Base C0 and current Switchy `main`.
- Produces: `BASE_C0_SHA` and `PROJECT_BASELINE_SHA` for all generated files and PR evidence.

- [ ] **Step 1: Read exact refs**

```bash
export BASE_C0_SHA="$(git ls-remote https://github.com/alsdmlals4-eng/Base refs/heads/main | cut -f1)"
export PROJECT_BASELINE_SHA="$(git ls-remote https://github.com/alsdmlals4-eng/Switchy-Express-Cargo-Puzzle refs/heads/main | cut -f1)"
printf 'BASE_C0_SHA=%s\nPROJECT_BASELINE_SHA=%s\n' "$BASE_C0_SHA" "$PROJECT_BASELINE_SHA"
```

- [ ] **Step 2: Verify Base C0 content exists at that SHA**

```bash
gh api "repos/alsdmlals4-eng/Base/contents/.github/workflows/reusable-godot-project-pilot.yml?ref=$BASE_C0_SHA" >/dev/null
gh api "repos/alsdmlals4-eng/Base/contents/schemas/godot-project-pilot-v1.schema.json?ref=$BASE_C0_SHA" >/dev/null
```

Expected: both requests succeed. Do not continue if Base C0 is only an open PR or the files are absent.

- [ ] **Step 3: Create a branch from exact current project main**

```bash
git fetch origin main
git switch -c agent/adopt-base-godot-project-pilot "$PROJECT_BASELINE_SHA"
```

---

### Task 2: Write the local adoption contract test first

**Files:**
- Create: `tests/test_godot_live_editor_adoption.py`

**Interfaces:**
- Consumes: the four planned project files.
- Produces: RED until descriptor, documentation, and workflow exist with the exact Base SHA.

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


def test_switchy_descriptor_is_clean_and_exactly_pinned() -> None:
    document = json.loads(DESCRIPTOR.read_text(encoding="utf-8"))
    assert document["schema_version"] == "1"
    assert document["project_identity"] == {
        "repository": "alsdmlals4-eng/Switchy-Express-Cargo-Puzzle",
        "project_id": "switchy-express-cargo-puzzle",
    }
    assert re.fullmatch(r"[0-9a-f]{40}", document["base_pilot_commit"])
    assert document["project_state"] == "EXISTING_GODOT_PROJECT"
    assert document["project_file"] == "project.godot"
    assert document["legacy_editor_plugins"] == []
    assert document["legacy_autoloads"] == []
    assert document["source_mutation_policy"] == "FORBIDDEN"
    assert document["scratch_scene_path"] == "res://.godot-live-editor-pilot/scratch.tscn"
    assert document["behavior_checks"] == [
        {
            "kind": "GODOT_SCRIPT",
            "target": "res://tests/run_tests.gd",
            "timeout_seconds": 120,
        }
    ]


def test_workflow_uses_the_same_immutable_base_sha() -> None:
    document = json.loads(DESCRIPTOR.read_text(encoding="utf-8"))
    sha = document["base_pilot_commit"]
    text = WORKFLOW.read_text(encoding="utf-8")
    assert f"alsdmlals4-eng/Base/.github/workflows/reusable-godot-project-pilot.yml@{sha}" in text
    assert f"base_pilot_commit: {sha}" in text
    assert "@main" not in text
    assert "pull_request:" in text
    assert "contents: read" in text


def test_adoption_doc_preserves_product_and_readiness_boundaries() -> None:
    text = DOC.read_text(encoding="utf-8")
    for marker in (
        "TEMPORARY_COPY_ONLY",
        "MAIN_SCENE_READ_ONLY",
        "SCRATCH_SCENE_MUTATION_ONLY",
        "SOURCE_TREE_UNCHANGED",
        "PRODUCTION_ADAPTER_READY: NOT_READY",
        "PROGRAM_B_NOT_INCLUDED",
        "PROGRAM_C_NOT_INCLUDED",
    ):
        assert marker in text


def test_pr_changes_only_adoption_surfaces() -> None:
    base = subprocess.check_output(["git", "merge-base", "HEAD", "origin/main"], text=True).strip()
    changed = subprocess.check_output(["git", "diff", "--name-only", base, "HEAD"], text=True).splitlines()
    assert set(changed) <= ALLOWED
```

- [ ] **Step 2: Run the test to verify RED**

```bash
python -m pytest tests/test_godot_live_editor_adoption.py -q
```

Expected: failures for the missing descriptor, workflow, and document. The scope test may already pass because only the test file exists.

- [ ] **Step 3: Commit test-only RED**

```bash
git add tests/test_godot_live_editor_adoption.py
git commit -m "test: require Switchy Godot project Pilot adoption"
```

---

### Task 3: Generate the exact clean-Pilot descriptor

**Files:**
- Create: `.godot-live-editor/project-pilot.json`

**Interfaces:**
- Consumes: exported `BASE_C0_SHA`.
- Produces: a Schema-valid descriptor used by the reusable workflow.

- [ ] **Step 1: Generate the file from the exact SHA**

```bash
export BASE_C0_SHA
python - <<'PY'
import json
import os
from pathlib import Path

sha = os.environ["BASE_C0_SHA"]
if len(sha) != 40 or any(ch not in "0123456789abcdef" for ch in sha):
    raise SystemExit("BASE_C0_SHA must be exact lowercase 40-hex")

document = {
    "schema_version": "1",
    "project_identity": {
        "repository": "alsdmlals4-eng/Switchy-Express-Cargo-Puzzle",
        "project_id": "switchy-express-cargo-puzzle",
    },
    "base_pilot_commit": sha,
    "project_state": "EXISTING_GODOT_PROJECT",
    "godot": {
        "version": "4.7.1-stable",
        "archive_sha256": "c7ff14fd28472c8d4f193043de30278dcf7e5241a1dcf7566b02e27addaa33ba",
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
            "timeout_seconds": 120,
        }
    ],
    "expected_platform": "ANDROID",
}
path = Path(".godot-live-editor/project-pilot.json")
path.parent.mkdir(parents=True, exist_ok=True)
path.write_text(json.dumps(document, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
PY
```

- [ ] **Step 2: Validate against the exact Base Schema**

```bash
rm -rf .tmp-base-c0
git clone --filter=blob:none --no-checkout https://github.com/alsdmlals4-eng/Base .tmp-base-c0
git -C .tmp-base-c0 checkout "$BASE_C0_SHA" -- schemas/godot-project-pilot-v1.schema.json tools/godot_project_pilot_descriptor.py
python - <<'PY'
from pathlib import Path
import sys
sys.path.insert(0, ".tmp-base-c0")
from tools.godot_project_pilot_descriptor import load_descriptor
print(load_descriptor(Path(".godot-live-editor/project-pilot.json")))
PY
rm -rf .tmp-base-c0
```

- [ ] **Step 3: Run focused tests and commit**

```bash
python -m pytest tests/test_godot_live_editor_adoption.py -q
git add .godot-live-editor/project-pilot.json tests/test_godot_live_editor_adoption.py
git commit -m "chore: describe Switchy isolated Godot Pilot"
```

Expected: descriptor test passes; workflow/document tests remain RED.

---

### Task 4: Add adoption documentation

**Files:**
- Create: `docs/GODOT_LIVE_EDITOR_ADOPTION.md`

**Interfaces:**
- Consumes: descriptor and approved Base design.
- Produces: truthful operator guidance and recovery boundaries.

- [ ] **Step 1: Write the document with these exact sections**

```markdown
# Switchy Express Godot Live-Editor Pilot Adoption

## Status

- `PILOT_MODE: TEMPORARY_COPY_ONLY`
- `MAIN_SCENE_READ_ONLY`
- `SCRATCH_SCENE_MUTATION_ONLY`
- `SOURCE_TREE_UNCHANGED`
- `PRODUCTION_ADAPTER_READY: NOT_READY`

## What the Pilot does

The pinned Base workflow copies this repository to a disposable workspace, opens the configured main Scene only for `scene.inspect`, switches to a runner-owned scratch Scene, proves rename/Undo/save, verifies physical bytes and atomic ledger evidence, and discards the workspace.

## What the Pilot does not do

- no permanent addon installation;
- no `project.godot`, `game/`, `scenes/`, `data/`, `export_presets.cfg`, save, input, or product test mutation;
- no MCP, HTTP, WebSocket, remote endpoint, or runtime debugger;
- no Android-device, physical-input, accessibility, performance, or human usability claim.

## Evidence

The workflow artifact must record project load, real main Scene inspect, scratch rename, Editor Undo, scratch save, physical SHA-256, unchanged source inventory, and `base_network_listener: false`.

## Follow-up gates

- `PROGRAM_B_NOT_INCLUDED`
- `PROGRAM_C_NOT_INCLUDED`
- Permanent adoption or migration requires a separate project Decision and PR.

## Removal

Delete the four adoption files in one revert. No product migration or save conversion is required.
```

- [ ] **Step 2: Run the focused test and commit**

```bash
python -m pytest tests/test_godot_live_editor_adoption.py -q
git add docs/GODOT_LIVE_EDITOR_ADOPTION.md tests/test_godot_live_editor_adoption.py
git commit -m "docs: explain Switchy isolated Godot Pilot"
```

Expected: only workflow assertions remain RED.

---

### Task 5: Add the exact caller workflow

**Files:**
- Create: `.github/workflows/validate-godot-live-editor-pilot.yml`

**Interfaces:**
- Consumes: exact Base C0 SHA and descriptor.
- Produces: local contract result plus reusable Base runtime artifact.

- [ ] **Step 1: Generate the workflow from the same SHA**

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

- [ ] **Step 2: Run local contract GREEN**

```bash
python -m pytest tests/test_godot_live_editor_adoption.py -q
git diff --check
```

Expected: all focused tests pass.

- [ ] **Step 3: Commit**

```bash
git add .github/workflows/validate-godot-live-editor-pilot.yml tests/test_godot_live_editor_adoption.py
git commit -m "ci: run Switchy isolated Godot Pilot"
```

---

### Task 6: Run the project PR and validate runtime evidence

**Files:**
- No additional product files.

**Interfaces:**
- Consumes: exact PR HEAD.
- Produces: a Draft PR with one clean real-project evidence artifact.

- [ ] **Step 1: Run local and existing project checks**

```bash
python -m pytest tests/test_godot_live_editor_adoption.py -q
python tools/validate_project_contract.py
git diff --check
```

Run the existing Godot suite when a local 4.7.1 binary is available:

```bash
Godot_v4.7.1-stable_linux.x86_64 --headless --path . --script res://tests/run_tests.gd
```

- [ ] **Step 2: Confirm exact changed-file scope**

```bash
git diff --name-only "$(git merge-base HEAD origin/main)" HEAD
```

Expected: exactly the four allowed adoption paths.

- [ ] **Step 3: Open a Draft PR**

The PR body records:

```yaml
base_c0_sha: exact 40-hex
legacy_godot_ai: ABSENT
source_product_files_changed: false
real_project_runtime: PENDING
production_adapter_ready: NOT_READY
merge_authorization: NOT_GRANTED
```

- [ ] **Step 4: Inspect workflow artifact physically**

Required final evidence:

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

Download the artifact, recompute `runtime-result.json`, saved scratch Scene, and evidence-file hashes, and record run ID plus artifact ID in the PR comment.

- [ ] **Step 5: Merge only after explicit approval**

Before merge, refetch project main, exact PR head, checks, review threads, and changed files. Squash merge with expected head SHA. Record the resulting Switchy main SHA for Base C1.
