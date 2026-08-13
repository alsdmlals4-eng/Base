# Base Controlled Vocabulary and IRG Implementation Plan

## Goal

Create a thin controlled-vocabulary index, name the existing completion-claim contract `Implementation Reality Gate`, preserve current owners, and add deterministic regressions.

## Scope

Create `docs/CONTROLLED_VOCABULARY.md`; update the existing routing, Vertical Slice, claim-verification, governance-test, and changelog documents named in the approved design. Do not add a Skill, Work Mode, Registry entry, Schema, or project migration.

## Sequence

1. Add the governance regression first and confirm the missing vocabulary document causes the expected RED result.
2. Add the vocabulary canon and one-step routes.
3. Add the IRG alias to the existing verification owner and refine the product-experiment distinction table.
4. Run focused and Base-wide exact-head validation.
5. Perform adversarial review, merge the reviewed head, and read back the new main.

## Verification

- `tests.test_v9_governance_documents`
- `tests.test_vertical_slice_v9_contract`
- `tests.test_neutral_adversarial_feature_lifecycle`
- Base v9 exact-head Actions
- changed-path and open-PR overlap checks
- post-merge main readback

## Rollback

Revert the single squash merge. No Registry, product data, runtime, or migration state is introduced.
