# Effect Stage and Compositing Controls

Use this module for generated VFX references, staged effect sheets, impact/charge/dissolve sequences, overlays, particles-as-concept, and compositing-oriented visual candidates.

## Separate the effect from runtime implementation

A visual effect reference defines appearance and stage relationships. It does not prove shaders, particles, draw order, performance, or game timing.

## Stage contract

Before effect production, apply `STAGING_RESEARCH_BEFORE_PRODUCTION` from
[sprite-pose-sequence-controls.md](sprite-pose-sequence-controls.md) to action-bound
effects. For standalone ambient/UI effects, record their own intended emotion,
focal hierarchy, meaningful stages and applicable outcome states instead of forcing
combat participants. A reasoned non-applicability is valid for absent branches.

Bind `resolved_event`, participant/target, actual contact or non-contact anchor,
direction, onset, peak and decay to the project's presentation contract. The effect
does not resolve the event or invent contact. `NO_VFX_TO_HIDE_POSE_ERRORS`: repair
an incorrect pose/trajectory rather than moving a flash to imply a false impact.
Keep effect, actor motion and editable result text separately controllable.

Require effect-off and effect-on comparison, `reduced_effect_review`, target-scale
crop and representative backgrounds. Protect faces, hands, action silhouettes and
decision-bearing UI when relevant. Stronger bloom, camera shake, hit-stop or sound
is not automatically better; choose an intensity budget and repetition policy from
the actual scene, accessibility requirements and timing contract. Do not invent
numeric defaults from a reference. Audio and runtime synchronization need their own
observed evidence; GIF encoding or alpha extraction cannot prove either.

Source: [Riot Art Education — Visual Effects](https://www.riotgames.com/it/artedu/visual-effects)
(accessed 2026-09-09). Adapt its explicit balance of satisfaction, accurate action/state
communication and restraint; its art language is not a mandatory project style.

```yaml
effect_id:
role:
anchor_target:
stages:
  - stage_id:
    visual_intent:
    relative_scale:
    opacity_or_density:
    dominant_shape:
    color_energy:
background_requirement: transparent | neutral_plate | scene_context
alpha_requirement:
loop_or_one_shot:
protected_project_vfx_language: []
forbidden_drift: []
```

Use the fewest stages needed to communicate the change over time.

Typical stages:

```text
anticipation / charge
initial contact / ignition
peak / impact
decay / residue
```

Do not force this sequence when the effect role needs a different structure.

## Compositing checks

Review:

- clean alpha/edge behavior when transparency is required;
- no baked background contamination in a reusable overlay;
- anchor and scale relationship to the consumer;
- stage-to-stage shape/color continuity;
- peak readability against intended backgrounds;
- additive/glow-like appearance does not erase important gameplay information;
- no accidental character/object redesign when effect overlaps the subject.

## Reuse boundary

Classify reusable effect work with the existing harvest taxonomy rather than a new VFX taxonomy.

Examples:

- stable reusable overlay bytes → `REUSE_AS_IS`;
- same effect family with color/intensity variants → `VARIANT_SEED`;
- timing/composition pattern only → `STRUCTURE_PATTERN`;
- recurring project VFX language → `STYLE_DNA`;
- effect requires semantic shader/particle reconstruction → `REBUILD_FOR_REUSE`.

## Figma organization

New effect candidates enter `02_WIP`. After explicit user approval, use the project's `01.8_VFX` or equivalent approved-reference section. `04_FINAL` may hold final visual references, but Figma placement still does not mean `PROJECT_ASSET_APPROVED` or runtime VFX verification.
