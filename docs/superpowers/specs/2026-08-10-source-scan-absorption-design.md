# Absorption-First Periodic Source Scan Design

## Decision ladder

```text
latest main + same-goal open/recent PRs
→ source/original-source verification
→ Base overlap: NONE | PARTIAL | ALREADY_COVERED | CONFLICT
→ adversarial review
→ REJECT/IGNORE only when not useful
→ otherwise choose smallest retained outcome:
   REFERENCE_ONLY
   EVIDENCE_ONLY_UPDATE
   ABSORB_EXISTING_OWNER
   INCREMENTAL_IMPROVEMENT
   LOW_RISK_BOUNDED_UPDATE
   RULE_OR_BCP_CANDIDATE
→ if Base changes: branch → PR → adversarial regression review → related CI/exact-head validation → merge gate
```

`ALREADY_COVERED` is not synonymous with `NO_CHANGE`. A candidate remains useful when it makes an existing owner's trigger, condition, failure state, counterexample, source coverage, regression case, evidence boundary, freshness check, checklist/template, or validation scenario materially clearer without duplicating responsibility.

## Existing-owner and incremental-improvement threshold

Prefer `ABSORB_EXISTING_OWNER` when an existing Skill/mode/reference/owner already owns the responsibility. If no Skill/owner change is justified, still test for `INCREMENTAL_IMPROVEMENT` through bounded improvements such as:

- regression tests or counterexamples;
- adversarial questions and failure states;
- source/reference coverage;
- stale/freshness/path corrections;
- checklist/template/evidence-field clarification;
- small validation-contract improvements.

Incremental improvement is a search and retention obligation, not a change quota. Do not create duplicate prose, redundant files, cosmetic rewrites, or ungrounded churn merely to avoid `NO_CHANGE`.

## New-rule threshold

Only create or propose a new shared rule/Skill/owner when an independent responsibility, authority, input/output, failure, or verification boundary exists that cannot be absorbed cleanly. Otherwise prefer existing-owner absorption or bounded incremental improvement.

## PR gate

A scan may discover and classify evidence without repository mutation. Once it changes Base, the change must use a separate branch and PR, re-check same-goal open/recent PRs, run adversarial review, execute the relevant tests on the exact head, and pass the existing merge gate. A periodic scan must not use its discovery result as authority to write directly to `main`.

## No-change threshold

`NO_CHANGE` requires all of the following to be false:

- new shared rule/BCP candidate;
- existing-owner absorption;
- evidence/reference-only retention;
- useful regression/adversarial scenario;
- source-pool coverage improvement;
- stale-reference/freshness/path correction;
- checklist/template/evidence-field clarification;
- bounded incremental improvement.
