# Executable Review Evidence Binding Implementation Plan

> Required execution disciplines: TDD, systematic debugging, adversarial review, verification before completion, and post-merge readback.

**Goal:** Make BCP-2026-027 completion claims executable and fail-closed without adding another ACTIVE Skill.

**Architecture:** A task record describes approved claims, scope, Acceptance mappings, and reviewed commands. A canonical Python tool resolves exact Git state, runs approved commands, applies Evidence ceiling, verifies that the commands did not alter the reviewed repository state, and emits a machine-readable result. Existing post-merge verification remains separate.

**Tech stack:** Python 3.12+, standard library, `jsonschema==4.26.0`, Git, unittest, GitHub Actions.

## Global constraints

- Preserve the 30 ACTIVE Skills and PLAN / BUILD / REVIEW modes.
- Do not change game product code, Godot projects, data, scenes, or assets.
- Do not execute shell strings or unreviewed programs.
- Do not promote TEST to RUNTIME, RENDER, or HUMAN without required evidence.
- Do not claim integration before merged state, merge SHA, main readback, and post-merge checks.

### Task 1 — Reproduce the missing executable-evidence gap

**Files:**

- Test: `tests/test_claim_evidence_binding.py`
- Required-CI consumer: `tests/test_skill_implementation_evidence.py`

- [x] Add positive and adversarial behavior cases.
- [x] Run the initial PR checks.
- [x] Record the observed failure rather than weakening assertions.

Observed initial failure: the new packaged script was not linked from its owning Skill, so Game Project OS package integrity failed.

### Task 2 — Implement exact-Git and fresh-execution verification

**Files:**

- Create: `tools/check_review_evidence.py`
- Create: `skills/reviewing-and-validating-project-changes/contracts/review-record.schema.json`
- Create: `skills/reviewing-and-validating-project-changes/contracts/review-result.schema.json`
- Create: `templates/quality/REVIEW_EVIDENCE_RECORD.json`
- Preserve compatibility: `skills/reviewing-and-validating-project-changes/scripts/verify_evidence.py`

- [x] Validate input and generated result Schemas.
- [x] Resolve exact base SHA, HEAD, ancestry, clean worktree, and actual diff.
- [x] Enforce slash-aware allowed/protected paths and Acceptance implementation paths.
- [x] Execute only reviewed argv with `shell=False`, timeout, allowlist, exit-code, and marker checks.
- [x] Recheck base SHA, HEAD, changed-file set, and clean worktree after command execution.
- [x] Apply default TEST ceiling and explicit per-check RUNTIME/RENDER approval.
- [x] Keep integration `BLOCKED_UNVERIFIED` pre-merge.

### Task 3 — Connect the existing owner without registry churn

**Files:**

- Modify: `skills/reviewing-and-validating-project-changes/SKILL.md`
- Modify: `skills/reviewing-and-validating-project-changes/LEARNING_LOG.md`
- Modify: `.github/reference-freshness.json`

- [x] Link the canonical tool, schemas, template, and compatibility entrypoint.
- [x] Register the new tests as valid Skill-change companions.
- [x] Evaluate implementation-evidence index changes and revert them as unnecessary broad churn.
- [x] Preserve ACTIVE Skill count and the existing generated evidence view.

### Task 4 — Validate and adversarially review

- [x] Run Base v9 operating contracts on intermediate exact heads.
- [x] Run Skill Behavior Evidence and observe canonical RED for slash-crossing `*`.
- [x] Fix slash-aware glob semantics.
- [x] Add and fix post-command repository mutation detection.
- [ ] Run all required workflows to completion on the final exact head.
- [ ] Confirm current main and open-PR path overlap again.
- [ ] Inspect final PR diff for unresolved P0/P1 findings.
- [ ] Resolve all blocking findings and rerun required checks.

Attack cases:

- forged/confident PASS;
- test definition without execution;
- stale/no-op base or dirty worktree;
- hidden path drift and protected changes;
- single-star scope widening across directories;
- zero exit without success marker;
- command-generated repository mutation after a success marker;
- arbitrary executable;
- Evidence-level inflation;
- pre-merge integration overclaim;
- bracketed repository paths.

### Task 5 — Integrate and read back

- [ ] Add exact-head pre-merge evidence document.
- [ ] Update PR #330 description with exact final evidence and truthful boundaries.
- [ ] Mark PR ready only after exact-head checks are green.
- [ ] Squash merge with expected head SHA.
- [ ] Read PR merged state and merge SHA.
- [ ] Read canonical files from new `main`.
- [ ] Observe post-merge workflows.
- [ ] If merge identity must be recorded in the evidence document, use a one-file closeout PR rather than inventing future evidence.

## Completion criteria

- Material implementation/verification claims are checked against actual diff and fresh execution.
- Scope globs do not silently widen a single-directory allowance into nested directories.
- A check cannot retain PASS after changing the reviewed repository state.
- `NOT_RUN`, `CLAIM_UNVERIFIED`, and `BLOCKED_UNVERIFIED` remain fail-closed.
- The existing Skill owner and topology are preserved.
- All final exact-head required checks pass.
- The feature is merged and independently read back from `main`.
