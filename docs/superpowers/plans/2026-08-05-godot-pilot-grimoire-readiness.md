# GRIMOIRE Godot Preproject Readiness Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Record GRIMOIRE's future Base C0 adoption contract without creating a Godot product project, running a fabricated Runtime Pilot, or changing the approved 3×3 design and product-implementation gate.

**Architecture:** The project PR adds a `NOT_CREATED` descriptor, a readiness document, a focused test that rejects runtime and installation claims, and a static CI workflow pinned to the exact Base C0 SHA. No reusable runtime workflow is called because `project.godot` does not exist and product-project creation remains separately gated.

**Tech Stack:** Python 3.12/pytest, JSON, GitHub Actions static validation, Base C0 descriptor Schema and loader.

## Global Constraints

- Repository: `alsdmlals4-eng/GRIMOIRE-`.
- Plan-creation audit baseline: `2d80e4afcfc6b530b76912826f5984cdf1184678`; execution starts from then-current `main`.
- Current authority states `product_project: NOT_CREATED`, `product_implementation: NOT_STARTED`, and `runtime_validation: NOT_RUN`.
- This PR must not create `project.godot`, Scenes, scripts, addons, exports, Resources, runtime tests, product code, or generated product assets.
- Descriptor state is exactly:
  - `project_state: NOT_CREATED`
  - `project_file: null`
  - `main_scene_source: NOT_APPLICABLE`
  - `behavior_checks: []`
  - `expected_platform: NOT_CREATED`
- Runtime fields are `NOT_APPLICABLE`, never PASS.
- Adapter installation remains `FORBIDDEN_UNTIL_PRODUCT_PROJECT_APPROVAL`.
- Allowed source changes are exactly:
  - `.godot-live-editor/project-pilot.json`
  - `docs/GODOT_LIVE_EDITOR_ADOPTION_READINESS.md`
  - `tests/test_godot_live_editor_readiness.py`
  - `.github/workflows/validate-godot-live-editor-readiness.yml`
- Current 3×3 circuit canon, Frostbloom boundary, planning Decisions, product gates, assets, and Google Sheets remain unchanged.
- Merge requires exact-head CI, zero unresolved threads, scope proof, and explicit user approval.

---

## File Responsibility Map

- `.godot-live-editor/project-pilot.json`: exact Base C0 pin with `NOT_CREATED` state.
- `docs/GODOT_LIVE_EDITOR_ADOPTION_READINESS.md`: future adoption checklist and explicit no-runtime boundary.
- `tests/test_godot_live_editor_readiness.py`: rejects product-project files, runtime workflow calls, runtime PASS, and mutable Base refs.
- `.github/workflows/validate-godot-live-editor-readiness.yml`: static local test and exact Base descriptor-Schema validation only.

---

### Task 1: Freeze exact refs and create the branch

**Files:**
- No writes.

**Interfaces:**
- Produces: `BASE_C0_SHA` and current GRIMOIRE baseline SHA.

- [ ] **Step 1: Resolve immutable refs**

```bash
export BASE_C0_SHA="$(git ls-remote https://github.com/alsdmlals4-eng/Base refs/heads/main | cut -f1)"
export PROJECT_BASELINE_SHA="$(git ls-remote https://github.com/alsdmlals4-eng/GRIMOIRE- refs/heads/main | cut -f1)"
gh api "repos/alsdmlals4-eng/Base/contents/schemas/godot-project-pilot-v1.schema.json?ref=$BASE_C0_SHA" >/dev/null
git fetch origin main
git switch -c agent/add-godot-adoption-readiness "$PROJECT_BASELINE_SHA"
```

- [ ] **Step 2: Reconfirm the project is still absent**

```bash
test ! -e project.godot
test ! -d scenes
test ! -d addons
```

If a product project has been approved and created on current `main`, stop using this plan and return to the real-project Pilot design path.

---

### Task 2: Write the no-runtime readiness test first

**Files:**
- Create: `tests/test_godot_live_editor_readiness.py`

**Interfaces:**
- Produces: RED until descriptor, readiness document, and static workflow exist.

- [ ] **Step 1: Create the failing test**

```python
from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DESCRIPTOR = ROOT / ".godot-live-editor/project-pilot.json"
WORKFLOW = ROOT / ".github/workflows/validate-godot-live-editor-readiness.yml"
DOC = ROOT / "docs/GODOT_LIVE_EDITOR_ADOPTION_READINESS.md"
ALLOWED = {
    ".godot-live-editor/project-pilot.json",
    "docs/GODOT_LIVE_EDITOR_ADOPTION_READINESS.md",
    "tests/test_godot_live_editor_readiness.py",
    ".github/workflows/validate-godot-live-editor-readiness.yml",
}
FORBIDDEN_RUNTIME_PATHS = {
    "project.godot",
    "export_presets.cfg",
}
FORBIDDEN_RUNTIME_PREFIXES = ("scenes/", "scripts/", "addons/", "game/", "src/")


def descriptor() -> dict:
    return json.loads(DESCRIPTOR.read_text(encoding="utf-8"))


def changed_files() -> list[str]:
    base = subprocess.check_output(["git", "merge-base", "HEAD", "origin/main"], text=True).strip()
    return subprocess.check_output(["git", "diff", "--name-only", base, "HEAD"], text=True).splitlines()


def test_descriptor_is_explicitly_preproject() -> None:
    document = descriptor()
    assert document["project_identity"] == {
        "repository": "alsdmlals4-eng/GRIMOIRE-",
        "project_id": "grimoire",
    }
    assert re.fullmatch(r"[0-9a-f]{40}", document["base_pilot_commit"])
    assert document["project_state"] == "NOT_CREATED"
    assert document["project_file"] is None
    assert document["main_scene_source"] == "NOT_APPLICABLE"
    assert document["legacy_editor_plugins"] == []
    assert document["legacy_autoloads"] == []
    assert document["behavior_checks"] == []
    assert document["expected_platform"] == "NOT_CREATED"


def test_document_rejects_runtime_and_installation_claims() -> None:
    text = DOC.read_text(encoding="utf-8")
    for marker in (
        "PRODUCT_PROJECT: NOT_CREATED",
        "RUNTIME_PILOT: NOT_APPLICABLE",
        "ADAPTER_INSTALLATION: FORBIDDEN_UNTIL_PRODUCT_PROJECT_APPROVAL",
        "RUNTIME_PASS_FORBIDDEN",
        "PRODUCTION_ADAPTER_READY: NOT_READY",
    ):
        assert marker in text


def test_workflow_is_static_and_does_not_call_runtime_pilot() -> None:
    sha = descriptor()["base_pilot_commit"]
    text = WORKFLOW.read_text(encoding="utf-8")
    assert f"ref: {sha}" in text
    assert "reusable-godot-project-pilot.yml" not in text
    assert "Godot_v4.7.1" not in text
    assert "godot_multi_project_pilot.py" not in text
    assert "@main" not in text


def test_pr_does_not_create_product_project_or_runtime_files() -> None:
    changed = changed_files()
    assert set(changed) <= ALLOWED
    assert not any(path in FORBIDDEN_RUNTIME_PATHS for path in changed)
    assert not any(path.startswith(FORBIDDEN_RUNTIME_PREFIXES) for path in changed)
    assert not (ROOT / "project.godot").exists()
```

- [ ] **Step 2: Verify RED and commit**

```bash
python -m pytest tests/test_godot_live_editor_readiness.py -q
git add tests/test_godot_live_editor_readiness.py
git commit -m "test: require GRIMOIRE Godot preproject readiness"
```

Expected: missing descriptor, document, and workflow failures only.

---

### Task 3: Generate the `NOT_CREATED` descriptor

**Files:**
- Create: `.godot-live-editor/project-pilot.json`

**Interfaces:**
- Produces: a Schema-valid preproject descriptor with no runtime action.

- [ ] **Step 1: Generate the descriptor from `BASE_C0_SHA`**

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
        "repository": "alsdmlals4-eng/GRIMOIRE-",
        "project_id": "grimoire",
    },
    "base_pilot_commit": sha,
    "project_state": "NOT_CREATED",
    "godot": {
        "version": "4.7.1-stable",
        "archive_sha256": "c7ff14fd28472c8d4f193043de30278dcf7e5241a1dcf7566b02e27addaa33ba",
    },
    "project_file": None,
    "main_scene_source": "NOT_APPLICABLE",
    "legacy_editor_plugins": [],
    "legacy_autoloads": [],
    "legacy_disable_mode": "TEMPORARY_COPY_ONLY",
    "source_mutation_policy": "FORBIDDEN",
    "scratch_scene_path": "res://.godot-live-editor-pilot/scratch.tscn",
    "behavior_checks": [],
    "expected_platform": "NOT_CREATED",
}
path = Path(".godot-live-editor/project-pilot.json")
path.parent.mkdir(parents=True, exist_ok=True)
path.write_text(json.dumps(document, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
PY
```

- [ ] **Step 2: Validate against exact Base C0 Schema**

Checkout Base at `BASE_C0_SHA`, import `load_descriptor`, and require the descriptor to load with `is_runtime_project is False`.

- [ ] **Step 3: Run focused test and commit**

```bash
python -m pytest tests/test_godot_live_editor_readiness.py -q
git add .godot-live-editor/project-pilot.json tests/test_godot_live_editor_readiness.py
git commit -m "chore: describe GRIMOIRE Godot adoption readiness"
```

---

### Task 4: Write the future adoption checklist

**Files:**
- Create: `docs/GODOT_LIVE_EDITOR_ADOPTION_READINESS.md`

**Interfaces:**
- Produces: a future gate list without claiming current runtime capability.

- [ ] **Step 1: Write the required document**

```markdown
# GRIMOIRE Godot Live-Editor Adoption Readiness

## Current state

- `PRODUCT_PROJECT: NOT_CREATED`
- `RUNTIME_PILOT: NOT_APPLICABLE`
- `ADAPTER_INSTALLATION: FORBIDDEN_UNTIL_PRODUCT_PROJECT_APPROVAL`
- `RUNTIME_PASS_FORBIDDEN`
- `PRODUCTION_ADAPTER_READY: NOT_READY`

## What this PR proves

This repository records the Base C0 descriptor contract and future adoption checklist only. It does not create a Godot project, product code, Scene, addon, export, Runtime Pilot, or mobile proof.

## Gate before future real-project adoption

1. Product-project creation receives an explicit user Decision.
2. `project.godot` and the first approved main Scene are created through the product implementation workflow.
3. Godot version, target platform, source protection, test runner, and current main SHA are re-audited.
4. A new real-project descriptor replaces `NOT_CREATED` in a separate PR.
5. The Base C0 runtime workflow runs only after those gates.

## Protected canon

The 3×3 circuit, Stock/mana, Frostbloom, mobile-landscape direction, approved Decisions, product gates, assets, and Google Sheets are unchanged.

## Removal

Revert the four readiness files. No product migration exists.
```

- [ ] **Step 2: Run focused test and commit**

```bash
python -m pytest tests/test_godot_live_editor_readiness.py -q
git add docs/GODOT_LIVE_EDITOR_ADOPTION_READINESS.md tests/test_godot_live_editor_readiness.py
git commit -m "docs: define GRIMOIRE Godot adoption readiness"
```

---

### Task 5: Add static exact-SHA validation workflow

**Files:**
- Create: `.github/workflows/validate-godot-live-editor-readiness.yml`

**Interfaces:**
- Produces: local readiness test and Base C0 Schema validation; never invokes Godot.

- [ ] **Step 1: Generate workflow from `BASE_C0_SHA`**

```bash
export BASE_C0_SHA
python - <<'PY'
import os
from pathlib import Path
sha = os.environ["BASE_C0_SHA"]
text = f'''name: Validate Godot Live-Editor Readiness

on:
  pull_request:
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
      - uses: actions/checkout@v4
        with:
          repository: alsdmlals4-eng/Base
          ref: {sha}
          path: _base_c0
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: python -m pip install --disable-pip-version-check pytest==8.3.5 jsonschema==4.23.0
      - run: python -m pytest tests/test_godot_live_editor_readiness.py -q
      - name: Validate descriptor through Base C0
        run: |
          python - <<'PY2'
          import sys
          from pathlib import Path
          sys.path.insert(0, "_base_c0")
          from tools.godot_project_pilot_descriptor import load_descriptor
          descriptor = load_descriptor(Path(".godot-live-editor/project-pilot.json"))
          if descriptor.is_runtime_project:
              raise SystemExit("runtime project claim is forbidden")
          PY2
'''
Path(".github/workflows/validate-godot-live-editor-readiness.yml").write_text(text, encoding="utf-8")
PY
```

- [ ] **Step 2: Verify GREEN and commit**

```bash
python -m pytest tests/test_godot_live_editor_readiness.py -q
git diff --check
git add .github/workflows/validate-godot-live-editor-readiness.yml tests/test_godot_live_editor_readiness.py
git commit -m "ci: validate GRIMOIRE Godot adoption readiness"
```

---

### Task 6: Validate and merge the readiness PR independently

**Files:**
- No additional writes.

**Interfaces:**
- Produces: a merged static readiness contract and no Runtime Pilot evidence.

- [ ] **Step 1: Run current repository governance checks**

```bash
python -m pytest tests/test_godot_live_editor_readiness.py -q
python -m unittest discover -s tests -p 'test_*.py'
git diff --check
```

- [ ] **Step 2: Verify exact scope**

Expected: exactly the four readiness files. Confirm `project.godot`, Scenes, scripts, addons, and exports remain absent.

- [ ] **Step 3: Open a Draft PR**

The PR body must state:

```yaml
product_project: NOT_CREATED
runtime_pilot: NOT_APPLICABLE
runtime_evidence: NONE_BY_DESIGN
adapter_installation: FORBIDDEN_UNTIL_PRODUCT_PROJECT_APPROVAL
production_adapter_ready: NOT_READY
merge_authorization: NOT_GRANTED
```

- [ ] **Step 4: Reject any runtime-looking artifact**

No Godot binary download, runtime result, scratch Scene, ledger, or save hash is expected. Their presence is a scope violation.

- [ ] **Step 5: Merge only after explicit approval**

Refetch current main, exact head, CI, threads, and changed files. Squash merge with expected head SHA and record the resulting GRIMOIRE main SHA for Base C1.
