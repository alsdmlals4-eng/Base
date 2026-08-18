# Candidate Review and Reusable Harvest

Use this module when multiple visual candidates must be compared, one candidate must be selected, or an approved primary-use visual may contain reusable value.

## Candidate review

Do not rank candidates by vague attractiveness alone. Compare them against the task contract.

Recommended dimensions:

```text
canon / approved-reference fit
requested delta accuracy
identity and protected-element preservation
composition / information hierarchy
actual-use readability
artifact / anatomy / edge integrity
implementation fitness
rights / reference-similarity concerns
reuse value
```

A candidate can be visually strong and still fail because it changes protected identity or does not perform the requested role.

## Candidate states

```text
GENERATED_EXPLORATION
→ IN_REVIEW
├─ REVISION_REQUIRED
├─ REJECTED
└─ APPROVED_CANDIDATE
```

`APPROVED_CANDIDATE` remains separate from `PROJECT_ASSET_APPROVED`.

When Figma write is available, candidate sets belong in `02_WIP`/comparison before explicit user approval. Keep rejected alternatives only when their reason/history or reusable parts are useful.

## Reusable Visual Harvest Gate

Primary-use success comes before reuse promotion. Reuse the existing Base classifications from merged PR #433:

- `REUSE_AS_IS`
- `VARIANT_SEED`
- `STRUCTURE_PATTERN`
- `STYLE_DNA`
- `REBUILD_FOR_REUSE`
- `ONE_OFF_KEEP`
- `REJECT_REUSE`

Do not introduce a second reuse taxonomy for Expression/Sprite/Effect work.

Ask in order:

1. Is the primary-use result already acceptable for its intended screen/scene?
2. Is this element likely to serve the same role again?
3. Does an existing reusable asset/pattern already cover it?
4. Can it be used independently without misleading derived pixels or broken context?
5. Is the cost of structuring it lower than likely future recreation cost?
6. Would promotion damage project/title-specific identity?

## Rebuild vs crop

For UI, scalable panels, structured props, or runtime behavior, prefer semantic reconstruction (`REBUILD_FOR_REUSE`) over blind raster cropping.

For visible image layers, distinguish source layers, mask/cutout work, manual/semantic rebuild, and generative occlusion recovery according to the existing harvest policy.

## Authority

Figma reuse references and local harvest records help future work start consistently. They do not grant:

- `PROJECT_ASSET_APPROVED`;
- Asset Vault `promote`;
- tracked product bytes;
- license/release clearance;
- Godot/runtime evidence.

A future generation task should prefer an existing approved/reusable reference when it satisfies the same role, but must still respect current project canon and the user's current request.
