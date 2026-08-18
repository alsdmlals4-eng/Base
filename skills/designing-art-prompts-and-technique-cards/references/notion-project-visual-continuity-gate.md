# Notion Project Visual Continuity Gate

Use this reference only for project-scoped visual generation, editing or visual-flow review after the Visual Requirement Gate has selected a real need.

## Authority

```text
latest user decision
→ Project relation + current project canon / Decision
→ APPROVED_VISUAL_REFERENCE records in ASSET_KNOWLEDGE_MASTER
→ current Screen / flow records
→ candidate / draft material
→ external references
```

`PROJECT_RELATION_REQUIRED` is mandatory. If Project identity is missing or ambiguous, return `BLOCKED_UNVERIFIED` rather than borrowing a neighboring project's visual record.

Notion is the project operating workspace; repository code/data/scenes/resources/tests remain runtime truth.

## Required project context

Resolve when relevant:

```yaml
project_relation:
requirement_id:
responsible_document_id:
related_decision_ids: []
approved_visual_reference_ids: []
screen_id:
flow_id:
visual_map_status:
```

If a required approved direction does not exist, use `MISSING_CANON`. Do not infer canon from a draft Gallery card, archived candidate, rejected image, old chat, or another project.

## APPROVED_VISUAL_REFERENCE continuity

For each applicable `APPROVED_VISUAL_REFERENCE`, extract a bounded continuity card:

```text
Keep
→ identity, proportion, silhouette, palette, material/line language, camera/framing, lighting grammar, UI family

Avoid
→ known rejected drift, unreadable detail, pseudo-text, inconsistent icon/material language, accidental style-family changes

Do Not Drift
→ project-specific traits that must remain stable across new images/screens
```

`Keep / Avoid / Do Not Drift` is a constraint summary, not a second canon. If it disagrees with a newer project Decision, record `VISUAL_CANONICAL_CONFLICT` and stop promotion until reconciled.

## Conditional modules

Load only what the current task needs:

- character face/expression/gaze/head controls → `character-identity-expression-controls.md`
- pose/action/sprite sequence controls → `sprite-pose-sequence-controls.md`
- effect/VFX stage/compositing controls → `effect-stage-compositing-controls.md`
- candidate comparison/reuse harvest → `candidate-review-and-reusable-harvest.md`

Do not load every module by default.

## Screen / flow interpretation

For a visualized screen or flow, preserve machine-readable identifiers behind the human map:

```yaml
screen_id:
flow_id:
artifact_type:
  - SCREEN
  - INTERPRETATION_RECORD
  - VISUAL_MAP
interpretation_status:
  - CONFIRMED
  - DISCOVERED_IDEA
  - AI_ASSUMPTION
runtime_compare_required: true | false
runtime_capture_path:
runtime_compare_status:
```

`DISCOVERED_IDEA` and `AI_ASSUMPTION` must never be silently rewritten as project requirements.

If a prototype or draft shows behavior that is not established in project records, label it as a discovered idea or AI assumption. If actual runtime comparison is required, the evidence type is `RUNTIME_CAPTURE`; a Notion preview does not satisfy it.

## Candidate lifecycle

```text
Visual Requirement Gate
→ generate / edit candidate
→ DRAFT_VISUAL or GENERATED_EXPLORATION
→ attach to correct Project record
→ readback
→ Screen Interpretation Review
→ APPROVED_CANDIDATE or REVISION_REQUIRED / REJECTED
→ explicit user/project Decision
→ PROJECT_ASSET_APPROVED
→ repository implementation when required
→ APPLIED_AND_RUNTIME_VERIFIED only with runtime evidence
```

Generation or upload alone never promotes a candidate.

## Readback requirement

After upload, attachment, image replacement, status promotion or visual-map update:

1. fetch the intended Project target again;
2. verify Project relation;
3. verify expected file/preview/version/status;
4. verify an old replaced candidate is not still being presented as current;
5. record readback status.

Failure is `BLOCKED_UNVERIFIED` or an unverified delivery state, not success.

## Reuse harvest

Candidate reuse classification may use:

```text
REUSE_AS_IS
VARIANT_SEED
STRUCTURE_PATTERN
STYLE_DNA
REBUILD_FOR_REUSE
ONE_OFF_KEEP
REJECT_REUSE
```

A reuse classification does not change approval, Project authority, rights or runtime status.

## External-reference boundary

External visual sources are `REFERENCE` or `BENCHMARK` records. Record source provenance and rights/license boundary where material. Extract functional principles and use a `reference_brief`; do not copy identifiable expression or imply that visual similarity grants rights.

## Fail-closed outcomes

Return one or more of these rather than guessing:

```text
MISSING_CANON
VISUAL_CANONICAL_CONFLICT
BLOCKED_UNVERIFIED
REVISION_REQUIRED
REJECTED
```

Never promote a cross-project, inaccessible, unverified, rejected or superseded visual as `PROJECT_ASSET_APPROVED`.
