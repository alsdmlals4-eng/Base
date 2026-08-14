# Expression Studio Windows Subscription Import Portability Implementation Plan

**Goal:** Verify the existing no-additional-payment Expression import path on Ubuntu/Windows and fix only reproduced portability blockers by reusing merged Base primitives.

### Task 1 — RED existing endpoint test

**Files:**
- Modify `.github/workflows/validate-sprite-chatgpt-import-provenance.yml`

Rename only the workflow display/concurrency scope to Visual Studio portability, install Expression Studio dev dependencies alongside Sprite, and run existing:

`tools/expression-studio/tests/test_import_api.py::test_import_expression_candidates_without_a_provider_call`

Do not change Expression production code in this task. Record the exact Ubuntu/Windows failure boundary.

### Task 2 — Reproducible test environment

If RED proves the current Starlette TestClient dependency is absent from Expression's dev extra:

**File:**
- Modify `tools/expression-studio/pyproject.toml`

Add only the reviewed dependency already used by Sprite. Re-run the same matrix. Do not combine this with an anchor-reader fix until the next failure is observed.

### Task 3 — Windows anchor portability

If Ubuntu passes and Windows then fails reading the normal committed fixture anchor:

**File:**
- Modify `tools/expression-studio/src/expression_studio/service.py`

Replace the local POSIX-only descriptor chain with the same Base trusted-reader selection pattern already merged for Sprite:
- POSIX `read_regular_nofollow`
- Windows `read_regular_portable_nofollow`

Keep 25 MiB, SHA, supported-format and 4096px image validation unchanged. Do not modify shared staging.

### Task 4 — GREEN + adversarial review

Run the consolidated portability workflow on Ubuntu/Windows and all Base required gates. Attack:
- dependency drift/hidden environment dependency,
- Windows link/reparse anchor bypass,
- accidental paid/provider route,
- project escape,
- overlap with #373/#376/#386,
- POSIX semantic regression.

Require P0/P1=0 and unresolved review threads=0.

### Task 5 — current-main refresh + merge

Before merge, compare current main. If strict up-to-date has moved, rebuild the exact reviewed changed blobs on current main as a one-parent refresh commit, rerun all fresh checks, then squash merge with expected head SHA. Close #413 and re-read `main` files as post-change evidence.
