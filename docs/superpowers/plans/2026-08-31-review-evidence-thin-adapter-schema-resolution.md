# Review Evidence Thin-Adapter Schema Resolution Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Let the Base-owned review-evidence checker validate a repository-owned review record without requiring that repository to copy Base JSON schemas.

**Architecture:** `--root` remains the repository whose Git state, review record, and commands are examined. The checker resolves only its immutable JSON schemas from the Base repository containing `tools/check_review_evidence.py`. This preserves the thin-project adapter boundary and removes an accidental filesystem coupling without changing claim, intent, evidence-level, or command-execution behavior.

**Tech Stack:** Python standard library, `unittest`, JSON Schema validation, Git.

**Spec:** User-approved Base promotion request on 2026-08-31; `skills/reviewing-and-validating-project-changes/SKILL.md`; `tools/check_review_evidence.py`; the Omenward thin-adapter reproduction at `docs/reviews/OMENWARD_TITLE_ENTRY_REVIEW_EVIDENCE_2026-08-31.json`.

## Global Constraints

- `--root` continues to mean the target repository; no review record, command, or Git inspection may move to the Base checkout.
- The Base `review-record` and `review-result` schemas remain the only schemas for this checker.
- Do not vendor a `skills/reviewing-and-validating-project-changes/` tree into projects.
- Preserve current evidence ceilings: automated checks cannot create `HUMAN` evidence.
- Keep this Base repair separate from any Omenward PR update; PR #257 remains read-only unless the user names it and allows mutation.
- Use a separate Base branch and no direct or force push to `main`.

## Pre-build comparison

| Alternative | Result | Reason |
| --- | --- | --- |
| Resolve schemas beneath `--root` | REJECT | Requires every thin project to copy Base-owned contracts, recreating the exact Omenward failure and allowing schema drift. |
| Vendor the schema pair into every project | REJECT | Adds duplicated, version-sensitive files and makes project validation depend on manual synchronisation. |
| Resolve immutable schemas from the checker’s Base root while retaining `--root` for target state | ADOPT | Keeps one source of truth and preserves the CLI’s documented target-repository semantics. |

---

### Task 1: Prove the target repository does not need vendored schemas

**Files:**
- Modify: `tests/test_claim_evidence_binding.py`
- Test: `tests/test_claim_evidence_binding.py::ReviewRecordBehaviorTests.test_valid_record_passes_without_vendored_review_schemas`

**Interfaces:**
- Consumes: `check_review_evidence.check_record(root, record_path, base_ref, execute_checks, allowed_programs, approved_levels)`.
- Produces: a regression test that creates a target Git repository containing only a review record and its implementation files.

- [ ] **Step 1: Write the failing test**

  Create a temporary target repository exactly as the existing valid-record fixture does, but do not create `skills/reviewing-and-validating-project-changes/contracts/`. Commit the baseline and feature, then assert that `check_record(...)` returns no errors and a final status of `PASS`.

- [ ] **Step 2: Run test to verify it fails**

  Run:

  ```powershell
  & 'C:\Users\user\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -m unittest -v tests.test_claim_evidence_binding.ReviewRecordBehaviorTests.test_valid_record_passes_without_vendored_review_schemas
  ```

  Expected: FAIL with `record or schema unavailable` naming the target repository’s absent `skills/reviewing-and-validating-project-changes/contracts/review-record.schema.json`.

- [ ] **Step 3: Commit the RED test only**

  ```powershell
  git add tests/test_claim_evidence_binding.py
  git commit -m "test: reproduce review checker thin adapter schema failure"
  ```

### Task 2: Make Base own schema resolution

**Files:**
- Modify: `tools/check_review_evidence.py`
- Test: `tests/test_claim_evidence_binding.py::ReviewRecordBehaviorTests.test_valid_record_passes_without_vendored_review_schemas`

**Interfaces:**
- Consumes: immutable `RECORD_SCHEMA` and `RESULT_SCHEMA` paths relative to `ROOT`, plus a target `root` supplied by `--root`.
- Produces: a checker that reads the target review record from `root` and both schemas from `ROOT`.

- [ ] **Step 1: Apply the minimal production change**

  Replace only the two schema reads in `check_record`:

  ```python
  record_schema = read_json(ROOT / RECORD_SCHEMA)
  result_schema = read_json(ROOT / RESULT_SCHEMA)
  ```

  Leave `record = read_json(record_path)`, Git state inspection, changed-path rules, and command working directories rooted in the target repository.

- [ ] **Step 2: Run the RED regression again to verify GREEN**

  Run the same command from Task 1. Expected: PASS, with the target repository still lacking the vendored schema directory.

- [ ] **Step 3: Run the existing focused behavior suite**

  ```powershell
  & 'C:\Users\user\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -m unittest -v tests.test_claim_evidence_binding
  ```

  Expected: all tests pass; evidence-level, protected-path, dirty-worktree, and exact-Git-state checks remain unchanged.

- [ ] **Step 4: Commit the minimal repair**

  ```powershell
  git add tools/check_review_evidence.py tests/test_claim_evidence_binding.py
  git commit -m "fix: resolve review schemas from Base"
  ```

### Task 3: Verify the real thin-project boundary and publish safely

**Files:**
- Create: `docs/reviews/OMENWARD_TITLE_ENTRY_REVIEW_RESULT_2026-08-31.json` only in the Omenward follow-up branch if exact Base tool execution succeeds and scope remains unchanged.
- No Omenward open PR mutation.

**Interfaces:**
- Consumes: the committed Base checker and the existing Omenward title review record.
- Produces: external-tool evidence that is explicitly tied to the Base repair commit; it does not create runtime, human, rights, or merged-main evidence.

- [ ] **Step 1: Execute the checker against Omenward in read-only mode first**

  Run from the Omenward current worktree with the Base checker path and its existing review record. Confirm the former schema-location error is absent before interpreting any claim result.

- [ ] **Step 2: Re-run the checker with its declared safe Python validation command**

  Use the existing record, trusted base SHA, and `--execute-checks`. Do not add `--approve-level` arguments.

- [ ] **Step 3: Verify Base and project scope**

  Run `git diff --check`, the focused Base suite, and the project operating-contract validator. Record `NOT_RUN` rather than PASS for remote CI, human UX, accessibility, performance, or asset rights.

- [ ] **Step 4: Publish the Base branch as a separate PR**

  Push only the Base branch, create its PR, then read back exact head, changed paths, and remote checks. Do not merge until normal repository gates are actually satisfied.

## Plan self-review

- **Spec coverage:** The plan preserves target-root semantics, removes the duplicated-schema requirement, proves the external-project case with a RED test, retains evidence ceilings, and leaves Omenward’s open PR untouched.
- **Placeholder scan:** No placeholder implementation step remains; the exact Python expressions and test command are specified.
- **Type consistency:** The existing `check_record` signature and `ROOT / RECORD_SCHEMA` expressions match the current checker constants and tests.
