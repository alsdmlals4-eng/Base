# Semantic Completion + Destination Freshness Gate Design

## Goal

Prevent a technically Green change from being reported as complete when approved requirements are still only mapped/implemented, required validation was not run, or GitHub/Notion destination state is stale.

## Context

Base already has planning locks, requirement coverage, exact-head validation, evidence levels, protected surfaces, and post-merge GitHub/Notion readback. The missing link is a fail-closed completion contract that converts those rules into one machine-checkable closure decision without changing the existing readiness semantics.

The change must remain executor-neutral. Claude-specific hooks, Slack bots, or a new risk vocabulary are explicitly out of scope.

## Alternatives

1. Keep current readiness validation only. Rejected because `MAPPED`/`IMPLEMENTED` can remain structurally valid while a worker still reports completion.
2. Make `validate_bundle()` require every requirement to be `VERIFIED`. Rejected because it would break valid pre-execution/readiness states.
3. Add a separate completion phase and structured verification receipt. Adopted because readiness and completion have different semantics and can evolve independently.

## Architecture

### Readiness remains unchanged

`validate_bundle(capsule)` continues to answer: "Is this approved package safe and sufficiently mapped to start?"

### Completion is additive

Add `validate_completion(capsule)` to answer: "Can this run be reported complete?"

Completion requires:

- readiness validation has no blocking findings;
- capsule declares a `verification_receipt_path`;
- receipt matches `project_id`, `package_id`, and source authority;
- coverage ledger overall status is `VERIFIED`;
- every approved requirement is `VERIFIED` or `DEFERRED_APPROVED`;
- receipt status is `VERIFIED`;
- every required check is `PASS`;
- `FAIL`, `NOT_RUN`, or `SKIPPED` on a required check blocks completion;
- non-PASS checks include a reason so omissions are auditable;
- every required destination has an actual readback;
- a required destination is `SYNCED` only when `expected_ref == observed_ref`.

### Structured receipt

Create `LOOP_VERIFICATION_RECEIPT` as a standalone contract so existing project capsules do not become invalid merely because they predate this gate. The Base template adopts the path immediately; downstream projects adopt it when completion gating is enabled or when their next approved workflow changes.

Receipt fields:

- identity: project/package/source/exact-head
- overall status
- `checks[]`: check id, required flag, PASS/FAIL/NOT_RUN/SKIPPED, evidence reference, reason
- `destinations[]`: destination id/kind, required flag, expected ref, observed ref, SYNCED/STALE/UNVERIFIED/NOT_APPLICABLE, evidence reference

## Destination freshness rule

`SYNCED` is a conclusion, not an input claim.

For GitHub/Notion post-merge work:

```text
fresh GitHub main readback
→ update applicable Notion current-state fields/content
→ re-read Notion
→ compare repository SHA/frontier or other declared expected ref
→ write/retain SYNCED only when expected == observed
→ otherwise STALE or UNVERIFIED
```

CI is not required to call Notion. The external connector/operator performs authoritative readback and records the result in the receipt; Base only validates the receipt contract and forbids a false-positive completion state.

## Compatibility

- Existing `validate_bundle()` behavior stays intact.
- Existing project capsules without the new receipt remain readiness-valid.
- They fail only when the new completion phase is explicitly invoked.
- No new active Skill is created.
- No vendor-specific lifecycle hook is made authoritative.

## COC-Fiction pilot

COC-Fiction is the first project pilot because a real stale destination was observed: repository main advanced through current chapters 016–020 while Notion still exposed the previous main/frontier as `SYNCED`.

Pilot actions after Base merge:

1. correct COC-Fiction Notion Project Registry and Continuity/Handoff to the fresh GitHub main/frontier;
2. destination readback;
3. record a project-local completion/freshness receipt only if it can be added without colliding with another protected workstream;
4. preserve all fiction/canon/manuscript content.

## Other-project rollout

Do not mass-edit every project. Audit each active project's current GitHub main against its Notion Project Registry/Home sync fields and active status. Apply a bounded correction only where there is verified stale `SYNCED` state or where a current approved workflow actually uses the Loop completion contract.

Projects with open/draft/ready work remain read-only for overlapping repository changes.

## Rollback

- Base: revert the single PR; readiness behavior remains separately testable.
- Project: revert only the project-local receipt/adapter change; Notion stale-state correction is a factual current-state update and should only be rolled back if its source evidence was wrong.

## Acceptance criteria

- focused test proves readiness accepts an in-progress mapped ledger while completion rejects it;
- completion accepts only verified/deferred requirements with a verified receipt;
- required NOT_RUN/SKIPPED/FAIL blocks completion;
- stale destination ref blocks completion;
- CLI can select readiness vs completion without changing default readiness behavior;
- existing Base Loop tests remain Green;
- COC Notion readback matches current GitHub main/frontier after correction;
- other projects are audited and only evidence-backed gaps are changed.
