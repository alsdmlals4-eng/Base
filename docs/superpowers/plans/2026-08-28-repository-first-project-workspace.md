# Repository-First Project Workspace Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace mandatory Notion intermediate work with repository-primary project canon, exact-commit GPT–Codex handoff, repository asset manifests and milestone human-GDD PDF review artifacts while preserving existing Notion data as read-only migration input.

**Architecture:** Add a new machine-readable authority contract and a focused human policy that supersede Notion-first lower-priority records through root `AGENTS.md`. Preserve historical Notion contracts and tests for compatibility, add new templates for AI canon, PDF export and legacy migration, and protect the new default with a focused regression test. Avoid paths owned by pre-existing open PRs.

**Tech Stack:** Markdown, JSON, Python `unittest`, GitHub Actions/Base validation

**Spec:** `docs/superpowers/specs/2026-08-28-repository-first-project-workspace-design.md`

## Global Constraints

- `REPOSITORY_PRIMARY_CANON` is the default authority model.
- Exactly two default project planning deliverables are maintained: human-facing detailed GDD PDF and AI-facing detailed planning/implementation Markdown.
- `HUMAN_GDD_PDF_DERIVED_VIEW` is not an independently editable canon.
- `CHATGPT_WORK_EXECUTION_SURFACE_NOT_CANON` and `CHATGPT_LIBRARY_REFERENCE_STORAGE_NOT_CANON` remain non-authoritative.
- Notion receives no mandatory new writes and remains `LEGACY_READ_ONLY_MIGRATION_SOURCE` only when unique unmigrated material exists.
- Codex rehydrates the repository at an exact commit and consumes visuals through repository path + manifest + SHA-256 readback.
- No existing Notion page, database or project asset is deleted by this Base change.
- Pre-existing open PRs remain read-only; PR #660 paths are not modified.
- No paid dependency, service or separately metered API is added.

---

### Task 1: Add the repository-first machine authority and RED contract

**Files:**
- Create: `docs/operations/REPOSITORY_FIRST_PROJECT_WORKSPACE_CONTRACT.json`
- Create: `tests/test_repository_first_project_workspace_contract.py`

**Interfaces:**
- Consumes: current root `AGENTS.md` and design spec
- Produces: stable JSON fields and policy tokens consumed by Tasks 2–4

- [ ] **Step 1: Write the focused contract test**

```python
from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


class RepositoryFirstProjectWorkspaceContractTests(unittest.TestCase):
    def test_machine_contract_uses_repository_primary_canon(self) -> None:
        data = json.loads(text("docs/operations/REPOSITORY_FIRST_PROJECT_WORKSPACE_CONTRACT.json"))
        self.assertEqual(1, data["schema_version"])
        self.assertEqual("REPOSITORY_PRIMARY_CANON", data["authority_model"])
        self.assertEqual("HUMAN_GDD_PDF_DERIVED_VIEW", data["human_facing_view"])
        self.assertEqual("AI_DETAILED_PLANNING_IMPLEMENTATION_MARKDOWN", data["ai_facing_canon"])
        self.assertEqual("LEGACY_READ_ONLY_MIGRATION_SOURCE", data["notion_status"])
        self.assertEqual("FORBIDDEN_BY_DEFAULT", data["new_notion_write"])
        self.assertEqual("EXACT_REPOSITORY_COMMIT", data["codex_rehydration"])
        self.assertEqual("REPOSITORY_PATH_MANIFEST_SHA256_READBACK", data["approved_visual_delivery"])
```

- [ ] **Step 2: Run the focused test and confirm RED**

Run:

```bash
python -m unittest tests.test_repository_first_project_workspace_contract -v
```

Expected: FAIL because the new contract and routed policy files do not exist.

- [ ] **Step 3: Create the minimal machine contract**

The JSON must include exact authority, deliverable, asset, migration, completion-count and supersession fields from the design spec. It must explicitly point to `docs/REPOSITORY_FIRST_PROJECT_WORKSPACE_POLICY.md` and retain legacy Notion files as discovery-only compatibility sources.

- [ ] **Step 4: Run the focused test**

Run:

```bash
python -m unittest tests.test_repository_first_project_workspace_contract -v
```

Expected: remaining failures identify the still-missing policy, templates and root routing.

- [ ] **Step 5: Commit**

```bash
git add docs/operations/REPOSITORY_FIRST_PROJECT_WORKSPACE_CONTRACT.json tests/test_repository_first_project_workspace_contract.py
git commit -m "test: define repository-first workspace contract"
```

### Task 2: Add the detailed workspace, handoff and migration policy

**Files:**
- Create: `docs/REPOSITORY_FIRST_PROJECT_WORKSPACE_POLICY.md`
- Create: `docs/REPOSITORY_FIRST_GPT_CODEX_HANDOFF_POLICY.md`
- Create: `templates/project-operations/AI_PROJECT_CANON_SPEC.md`
- Create: `templates/project-operations/HUMAN_GDD_PDF_EXPORT_CHECKLIST.md`
- Create: `templates/project-operations/NOTION_RETIREMENT_AND_REPOSITORY_MIGRATION_CHECKLIST.md`
- Modify: `tests/test_repository_first_project_workspace_contract.py`

**Interfaces:**
- Consumes: JSON fields from Task 1
- Produces: project installation and migration rules referenced by root routing

- [ ] **Step 1: Extend the test with policy and template assertions**

Add assertions for:

```python
for token in (
    "REPOSITORY_PRIMARY_CANON",
    "HUMAN_GDD_PDF_DERIVED_VIEW",
    "CHATGPT_WORK_EXECUTION_SURFACE_NOT_CANON",
    "CHATGPT_LIBRARY_REFERENCE_STORAGE_NOT_CANON",
    "NOTION_UNIQUE_CANON_COUNT = 0",
    "CODEX_NOTION_DEPENDENCY_COUNT = 0",
    "ACTIVE_NOTION_WRITE_REQUIREMENT_COUNT = 0",
):
    self.assertIn(token, text("docs/REPOSITORY_FIRST_PROJECT_WORKSPACE_POLICY.md"))
```

Assert that the handoff policy contains `EXACT_REPOSITORY_COMMIT`, `REPOSITORY_PATH_MANIFEST_SHA256_READBACK`, `GPT_VISUAL_REQUEST`, and `NOTION_ABSENCE_IS_NOT_A_BLOCKER`.

- [ ] **Step 2: Run the focused test and confirm RED**

Run the same focused unittest. Expected: FAIL on missing policy and template files.

- [ ] **Step 3: Write the detailed policy**

Cover authority precedence, the two default deliverables, recommended PDF gates, project canonical bundle, asset manifest schema, Work/Library boundaries, large-source-binary handling, legacy migration, completion counts, evidence ceiling and rollback.

- [ ] **Step 4: Write the GPT–Codex handoff policy**

Require repository readback, exact commit identity, approved input paths, asset-manifest SHA verification, runtime evidence return and repository canon sync. Remove Notion as a mandatory handoff gate without expanding Codex beyond actual Godot product implementation.

- [ ] **Step 5: Write the three project templates**

The AI canon template must include player experience, systems/content, implementation semantics and verification. The PDF checklist must record exact source identity and derived-view limits. The migration checklist must inventory unique/duplicate/obsolete/blocked material and compute all three zero-count exit gates.

- [ ] **Step 6: Run the focused test**

Expected: policy/template assertions PASS; root-routing assertions remain RED.

- [ ] **Step 7: Commit**

```bash
git add docs/REPOSITORY_FIRST_PROJECT_WORKSPACE_POLICY.md docs/REPOSITORY_FIRST_GPT_CODEX_HANDOFF_POLICY.md templates/project-operations/AI_PROJECT_CANON_SPEC.md templates/project-operations/HUMAN_GDD_PDF_EXPORT_CHECKLIST.md templates/project-operations/NOTION_RETIREMENT_AND_REPOSITORY_MIGRATION_CHECKLIST.md tests/test_repository_first_project_workspace_contract.py
git commit -m "docs: add repository-first project workflow"
```

### Task 3: Route Base entrypoints to the new owner

**Files:**
- Modify: `AGENTS.md`
- Modify: `README.md`
- Modify: `tests/test_repository_first_project_workspace_contract.py`

**Interfaces:**
- Consumes: policy and contract paths from Tasks 1–2
- Produces: current active authority discoverable at repository entry

- [ ] **Step 1: Add RED assertions for root routing**

Assert that `AGENTS.md` contains:

```text
REPOSITORY_PRIMARY_PROJECT_CANON
HUMAN_GDD_PDF_DERIVED_VIEW
CHATGPT_WORK_EXECUTION_SURFACE_NOT_CANON
CHATGPT_LIBRARY_REFERENCE_STORAGE_NOT_CANON
NOTION_DEFAULT_PROJECT_WORKSPACE_LEGACY_ALIAS
POSTMERGE_REPOSITORY_AND_DERIVED_VIEW_READBACK_LOOP
```

Assert that `README.md` links to the new machine contract and describes Notion as legacy read-only rather than the default workspace.

- [ ] **Step 2: Run the focused test and confirm RED**

Expected: FAIL on root routing.

- [ ] **Step 3: Update `AGENTS.md`**

Add the new owner paths to the detailed-owner list. Replace section 5 default-workspace bullets with repository-primary authority, two deliverables, Work/Library non-canon boundaries, repository asset delivery and legacy Notion migration. Preserve the old Notion token only as `NOTION_DEFAULT_PROJECT_WORKSPACE_LEGACY_ALIAS` so historical tests and records stay discoverable without restoring the old behavior. Replace the postmerge Notion loop with repository and derived-view readback.

- [ ] **Step 4: Update `README.md`**

Change the first-read sequence, project default workspace, asset workflow, integrated flow and project authority examples. Link the new owner and retain old Notion links only under legacy migration/history.

- [ ] **Step 5: Run focused and compatibility tests**

```bash
python -m unittest tests.test_repository_first_project_workspace_contract -v
python -m unittest tests.test_agents_always_on_context_contract -v
python -m unittest tests.test_notion_project_workspace_contract -v
python -m unittest tests.test_gpt_codex_workflow_contract -v
```

Expected: PASS. Historical tests may still find legacy tokens, but the new test proves those tokens no longer own the default.

- [ ] **Step 6: Commit**

```bash
git add AGENTS.md README.md tests/test_repository_first_project_workspace_contract.py
git commit -m "docs: route projects to repository-first canon"
```

### Task 4: Validate, review and deliver

**Files:**
- Modify only if validation reveals a current-task defect

**Interfaces:**
- Consumes: exact branch HEAD from Tasks 1–3
- Produces: reviewed PR, required checks and postmerge readback

- [ ] **Step 1: Run full local validation when the environment supports the repository**

```bash
python -m pip install --requirement .github/validation-requirements.txt
python tools/run_local_validation.py --trusted-history-commit 7cfc75d607d1ed4d0f8323d4389e64da93df00c8
```

If the current connector environment cannot materialize the repository, record local validation as `NOT_RUN_ENVIRONMENT_UNAVAILABLE` and use required GitHub Actions as the executable verification path. Do not report local PASS.

- [ ] **Step 2: Perform five whole-state adversarial review loops**

Review lenses:

1. authority ambiguity and stale Notion restoration;
2. data-loss and migration rollback;
3. Codex asset/input determinism;
4. PDF becoming accidental second canon;
5. open-PR concurrency, cost and evidence inflation.

Every valid finding is corrected and the focused tests are rerun.

- [ ] **Step 3: Open a pull request**

Use a body that records source main, changed authority, protected legacy data, exact validation evidence, open-PR read-only boundary, evidence ceiling and rollback.

- [ ] **Step 4: Verify exact-head required checks and review state**

Confirm current main, exact PR head, changed files, workflow results, unresolved review threads, review submissions and repository squash-only settings.

- [ ] **Step 5: Squash merge only when all required gates pass**

Use expected head SHA. Never use admin bypass, merge commit, rebase merge or force update.

- [ ] **Step 6: Postmerge readback**

Read current `main` and verify:

```text
REPOSITORY_PRIMARY_PROJECT_CANON
HUMAN_GDD_PDF_DERIVED_VIEW
NOTION_DEFAULT_PROJECT_WORKSPACE_LEGACY_ALIAS
POSTMERGE_REPOSITORY_AND_DERIVED_VIEW_READBACK_LOOP
```

Recompute remaining work. This Base merge does not claim any individual project has reached the three Notion-retirement zero counts.
