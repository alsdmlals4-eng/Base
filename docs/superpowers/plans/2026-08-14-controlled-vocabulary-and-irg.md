# Base Controlled Vocabulary and IRG Implementation Plan

## Status

Approved implementation, resumed after interruption and rebased onto `main@b1317f2c1b83e57f016ce4efd4e169bf7c0acd90`.

The earlier connector limitation on executable test writes no longer applies to this execution surface: `tests/test_controlled_vocabulary_contract.py` was created successfully. A later adversarial read of the CI workflows found that file was not in the explicit unittest lists, so earlier green workflows were not accepted as execution evidence for this regression. The minimal CI consumer is now part of the approved implementation scope.

## Goal

Create a thin controlled-vocabulary index, distinguish industry/common terms from Base-local aliases, name the existing completion-claim contract `Implementation Reality Gate`, preserve current owners, and protect the semantics with an executable regression that the repository actually runs.

## Scope

Create:

- `docs/CONTROLLED_VOCABULARY.md`
- approved design and implementation records
- `tests/test_controlled_vocabulary_contract.py`

Modify:

- `START_HERE.md` for one-step terminology routing
- `docs/DOCUMENTATION_MAP.md` so the new public canon is registered in the repository's document-location/authority map
- `.github/workflows/validate-game-project-operating-system.yml` only to compile and run `tests/test_controlled_vocabulary_contract.py` inside the existing `ubuntu-contract`

Protect:

- `AGENTS.md`
- `skills/**`
- Skill Registry/generated maps
- schemas/release locks
- all workflow behavior outside the single semantic-regression consumer hook
- project code/data/assets

## Sequence

1. Rebase/sync the dedicated feature branch with current `main` without dropping the existing vocabulary work.
2. Add the semantic regression for discoverability, product-stage distinctions, and IRG fail-closed/local-alias boundaries.
3. Refine the vocabulary so `IRG` is explicitly `BASE_LOCAL_ALIAS`, not an industry standard, while preserving existing owners.
4. Reconcile the design record with the actual reviewed scope and current Base.
5. Attack canonical discoverability; because `docs/DOCUMENTATION_MAP.md` owns document location/responsibility, register the new vocabulary there and make the regression require both routes.
6. Reject the first apparent green as insufficient after confirming the repository workflows explicitly enumerate tests and did not call the new regression.
7. Add the new regression to the existing Game Project OS `ubuntu-contract` compile and unittest lists without changing other CI behavior.
8. Run fresh exact-head CI and inspect the semantic test consumer, all required check conclusions, PR threads, same-goal PR overlap, changed paths, and current-main freshness.
9. Run the adversarial review loop: attack → validate critique → minimal fix → regression recheck.
10. Convert the PR from Draft only after the reviewed exact HEAD is green and no merge blocker remains.
11. Squash merge the reviewed exact HEAD and read back the new `main`.

## Verification

Required fresh evidence on the final PR HEAD:

- `tests/test_controlled_vocabulary_contract.py` exists and is explicitly invoked by Game Project OS `ubuntu-contract`
- the `Run contract and governance regression tests` step succeeds on that exact HEAD
- `START_HERE.md` and `docs/DOCUMENTATION_MAP.md` both route to `docs/CONTROLLED_VOCABULARY.md`
- Base v9 contract / adversarial gate
- Game Project Operating System required jobs including `ci-gate`; because this PR modifies a workflow, use the repository's elevated CI classification rather than the earlier docs/code classification
- documentation/publication/platform checks exactly as selected by that final classifier
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
- a semantic regression existing but remaining absent from the explicit CI consumer list
- static PASS being promoted to runtime/render/UX/fun PASS
- a new Terminology/IRG Skill or Registry entry
- a new canonical terminology document missing from `docs/DOCUMENTATION_MAP.md`
- stale-main or pre-consumer CI being reused as final evidence
- design/plan scope claiming files that the actual PR does not touch

## Rollback

Revert the single squash merge. No Registry, product data, runtime, schema, or migration state is introduced. The vocabulary, routes, semantic test, and its single Game Project OS consumer hook roll back together.
