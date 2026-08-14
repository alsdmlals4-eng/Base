# Base Controlled Vocabulary and IRG Implementation Plan

## Status

Approved implementation, resumed after interruption and rebased onto `main@b1317f2c1b83e57f016ce4efd4e169bf7c0acd90`.

The earlier connector limitation on executable test writes no longer applies to this execution surface: `tests/test_controlled_vocabulary_contract.py` was created successfully. Completion still requires fresh exact-head CI; file creation alone is not test execution evidence.

## Goal

Create a thin controlled-vocabulary index, distinguish industry/common terms from Base-local aliases, name the existing completion-claim contract `Implementation Reality Gate`, preserve current owners, and protect the semantics with an executable regression.

## Scope

Create:

- `docs/CONTROLLED_VOCABULARY.md`
- approved design and implementation records
- `tests/test_controlled_vocabulary_contract.py`

Modify:

- `START_HERE.md` for one-step terminology routing
- `docs/DOCUMENTATION_MAP.md` so the new public canon is registered in the repository's document-location/authority map

Protect:

- `AGENTS.md`
- `skills/**`
- Skill Registry/generated maps
- schemas/workflows/release locks
- project code/data/assets

## Sequence

1. Rebase/sync the dedicated feature branch with current `main` without dropping the existing vocabulary work.
2. Add the semantic regression for discoverability, product-stage distinctions, and IRG fail-closed/local-alias boundaries.
3. Refine the vocabulary so `IRG` is explicitly `BASE_LOCAL_ALIAS`, not an industry standard, while preserving existing owners.
4. Reconcile the design record with the actual reviewed scope and current Base.
5. Attack canonical discoverability; because `docs/DOCUMENTATION_MAP.md` owns document location/responsibility, register the new vocabulary there and make the regression require both routes.
6. Run exact-head CI and inspect all check conclusions, PR threads, same-goal PR overlap, changed paths, and current-main freshness.
7. Run the adversarial review loop: attack → validate critique → minimal fix → regression recheck.
8. Convert the PR from Draft only after the reviewed exact HEAD is green and no merge blocker remains.
9. Squash merge the reviewed exact HEAD and read back the new `main`.

## Verification

Required fresh evidence on the final PR HEAD:

- `tests/test_controlled_vocabulary_contract.py`
- `START_HERE.md` and `docs/DOCUMENTATION_MAP.md` both route to `docs/CONTROLLED_VOCABULARY.md`
- Base v9 contract / adversarial gate
- Game Project Operating System checks including `ci-gate`
- documentation validation and other automatically selected repository checks
- changed-path scope inspection
- same-goal open/recent PR overlap check
- unresolved review thread check
- PR mergeability/current-main freshness
- post-merge main readback

Skipped checks are interpreted according to workflow conditions and are not promoted to PASS for capabilities they did not execute.

## Adversarial acceptance

MUST reject or fix:

- `IRG` being presented as an external industry standard
- Prototype/PoC/Vertical Slice/MVP/Demo collapsing into one linear stage
- Checklist being treated as Gate
- test-file existence being reported as execution
- static PASS being promoted to runtime/render/UX/fun PASS
- a new Terminology/IRG Skill or Registry entry
- a new canonical terminology document missing from `docs/DOCUMENTATION_MAP.md`
- stale-main CI being reused as final evidence
- design/plan scope claiming files that the actual PR does not touch

## Rollback

Revert the single squash merge. No Registry, product data, runtime, schema, workflow, or migration state is introduced.
