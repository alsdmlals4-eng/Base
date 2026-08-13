# Base Controlled Vocabulary and IRG Implementation Plan

## Status

Approved for implementation from `main@39936ff6a83410b4169878c1335de9eb3e4c25cf`. The GitHub connector blocks executable test-file writes in this session, so the planned semantic regression is `BLOCKED_TOOL_POLICY`; existing exact-head governance and Vertical Slice regressions remain required.

## Goal

Create a thin controlled-vocabulary index, name the existing completion-claim contract `Implementation Reality Gate`, preserve current owners, and add deterministic regressions where the execution surface permits them.

## Scope

Create `docs/CONTROLLED_VOCABULARY.md`; update the existing routing, Vertical Slice, claim-verification, and changelog documents named in the approved design. Do not add a Skill, Work Mode, Registry entry, Schema, or project migration.

## Sequence

1. Define the semantic regression before implementation; record the connector block without claiming RED execution.
2. Add the vocabulary canon and one-step routes.
3. Add the IRG alias to the existing verification owner and refine the product-experiment distinction table.
4. Run focused and Base-wide exact-head validation.
5. Perform adversarial review, merge the reviewed head, and read back the new main.

## Verification

- Existing `tests.test_v9_governance_documents`
- Existing `tests.test_vertical_slice_v9_contract`
- Existing `tests.test_neutral_adversarial_feature_lifecycle`
- Base v9 exact-head Actions
- Game Project Operating System exact-head Actions
- changed-path and open-PR overlap checks
- post-merge main readback
- New semantic test: `BLOCKED_TOOL_POLICY`, not reported as run or passed

## Rollback

Revert the single squash merge. No Registry, product data, runtime, or migration state is introduced.
