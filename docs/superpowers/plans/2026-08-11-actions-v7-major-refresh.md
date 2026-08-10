# Actions v7 Major Refresh Implementation Plan

> **Execution:** Use the approved Base plan with Superpowers TDD, exact-head CI, adversarial review, and post-merge reconciliation.

**Goal:** Replace the stale, old-base Dependabot PRs for `actions/checkout` and `actions/setup-node` with one current-main, immutable-SHA refresh that updates every active Base consumer and its regression contracts.

**Baseline:** `main@c8fe6af90be0526327dcfa22ebd65d6ada27ce9b`.

**Official reviewed targets:**
- `actions/checkout` v7.0.1 → `3d3c42e5aac5ba805825da76410c181273ba90b1`
- `actions/setup-node` v7.0.0 → `820762786026740c76f36085b0efc47a31fe5020`

## Constraints

- Keep full immutable commit SHA pins.
- Preserve `package-manager-cache: false` on Base publication setup-node steps.
- Do not copy whole files from old Dependabot branches if current main changed independently.
- Do not change frozen release locks or Registry.
- Update all active workflow, template, checker, and regression consumers of the retired pins.
- Exclude history-only references unless they are active execution contracts.
- Close Dependabot PR #130 and #133 only after this replacement PR exists and links preserve provenance.

## Task 1 — TDD RED

- Add a regression in an already-required governance test module that declares the reviewed v7 SHA pair.
- Require active workflow/template/checker surfaces to contain no retired checkout/setup-node SHA.
- Push test-only change and prove exact-head CI fails because current active consumers still use the retired pins.

## Task 2 — Minimal current-main propagation

- Replace checkout pin in all current active `.github/workflows/*.yml` consumers.
- Replace checkout pin in active project-operation workflow templates.
- Replace checkout pin in `tools/check_ci_required_gate_topology.py` and its direct tests/contracts.
- Replace setup-node pin in the canonical publication workflow.
- Update the official Action allowlist regression to the reviewed v7 values.
- Preserve unrelated bytes and behavior, including setup-node `package-manager-cache: false`.

## Task 3 — Replacement lifecycle

- Open one Draft replacement PR from the current-main branch.
- Add provenance links to #130 and #133.
- Close #130 and #133 as superseded only after the replacement PR exists.

## Task 4 — Verification and merge

- Run canonical-reference freshness and required CI on the exact head.
- Confirm workflow topology and immutable-action allowlist pass.
- Adversarially review for untouched consumers, unrelated BOM/format drift, cache behavior changes, and stale Action refs.
- Require final `ci-gate=success`, zero unresolved review threads, and unchanged reviewed head.
- Squash merge, then re-read new main and confirm retired pins are absent from active execution surfaces.
