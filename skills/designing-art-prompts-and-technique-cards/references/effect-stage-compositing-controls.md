# Effect Stage and Compositing Controls

Use this module for generated VFX references, staged effect sheets, impact/charge/dissolve sequences, overlays, particles-as-concept, and compositing-oriented visual candidates.

## Separate the effect from runtime implementation

A visual effect reference defines appearance and stage relationships. It does not prove shaders, particles, draw order, performance, or game timing.

## Stage contract

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
