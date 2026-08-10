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
   LOW_RISK_BOUNDED_UPDATE
   RULE_OR_BCP_CANDIDATE
→ validation
```

`ALREADY_COVERED` is not synonymous with `NO_CHANGE`. A candidate remains useful when it makes an existing owner's trigger, condition, failure state, counterexample, source coverage, regression case, or evidence boundary materially clearer without duplicating responsibility.

## New-rule threshold

Only create or propose a new shared rule/Skill/owner when an independent responsibility, authority, input/output, failure, or verification boundary exists that cannot be absorbed cleanly. Otherwise prefer existing-owner absorption.

## No-change threshold

`NO_CHANGE` requires all of the following to be false:

- new shared rule/BCP candidate;
- existing-owner absorption;
- evidence/reference-only retention;
- useful regression/adversarial scenario;
- source-pool coverage improvement;
- stale-reference/freshness correction.
