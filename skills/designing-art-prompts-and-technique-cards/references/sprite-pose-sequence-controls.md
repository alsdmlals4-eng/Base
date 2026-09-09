# Sprite Pose and Sequence Controls

Use this module for sprite/action pose variants, pose sheets, key-pose sequences, animation candidate frames, and atlas-oriented visual planning.

## Preserve identity across frames

Default invariants:

```text
character proportions and silhouette identity
face/hair/costume/equipment identity
palette/material language
camera projection and scale
anchor/ground relationship
weapon/prop identity
approved line/render style
```

A pose sequence may change body configuration dramatically without changing who the character is.

## Pose contract

### Direction research before production

`STAGING_RESEARCH_BEFORE_PRODUCTION`: for action, reaction, interaction or cinematic
pose sequences, research staging before generating key poses or adding inbetweens.
Read the project's approved art, actual camera/consumer and related reference
evidence first; then relevant first-party production examples. Record the source,
inspection date, observed mechanism, limits and `ADOPT / ADAPT / REJECT` decision.
Reuse existing research only when the decision dimension, project state and source
relevance still match. Unread references and search snippets are not inspected evidence.

Compare expressive composition as well as technical continuity: intended emotion,
focal point, silhouette, eyeline, line of action, weight/support, contact placement,
negative space, crop, timing contrast and camera stability. Do not import a specific
genre's pose, contact height, camera shake or frame count as a universal rule.

```yaml
staging_research:
  source_and_evidence: []
  observed_mechanism:
  project_fit_and_difference:
  adopt_adapt_reject:
  unverified_assumptions: []
direction:
  intended_emotion:
  focal_point:
  silhouette_eyeline_and_weight:
  contact_or_interaction_region:
  camera_crop_and_protected_information:
  anticipation_action_reaction_recovery:
outcome_branches:
  - resolved_event:
    participant_roles:
    role_specific_pose_and_reaction:
    recovery_or_terminal_transition:
    applicable_or_reason_not_applicable:
```

`NO_VISUAL_RULE_INVENTION`: consume the domain's resolved event. Outcome roles can
be success/failure, attacker/defender, accepted/refused, mutual or interrupted as
appropriate; do not force a winner/loser into every interaction. A lost exchange
does not itself authorize damage, stun, displacement or death. Separate local
pose recoil from logical movement. Do not add a tie or interrupt rule merely to
complete an animation chart; cover it only if the project supports it.

Review the most informative key pose before expensive frame expansion. Then review
anticipation → action/contact → role-specific reaction → recovery/terminal state
as a sequence, at intended crop/scale. `EFFECT_OFF_REVIEW` checks body/weapon motion
without VFX; `ROLE_REVERSED_REVIEW` checks both participant assignments when relevant.
An isolated impact pose or looping GIF is not evidence of a complete outcome branch.
Missing or interrupted animation must not change damage, resources, save or progress.
Record candidate, asset approval, import, runtime and Human evidence separately.

Research starting points (accessed 2026-09-09; inspect again when material):

- [GDC: Powerful and Effective Animation for 2D/3D Games](https://www.gdcvault.com/play/1021657/Powerful-and-Effective-Animation-for): public session description identifies keyframing, anticipation, smears and timing under gameplay restrictions. Description inspected; not a claim of watching the full session.
- [Riot: VALORANT Shaders and Gameplay Clarity](https://www.riotgames.com/en/news/valorant-shaders-and-gameplay-clarity): adapt the balance of art, readability and performance; do not copy shooter-specific rendering or silhouettes.

Define the action before generating frames:

```yaml
pose_or_action_id:
intent:
start_state:
key_pose_sequence: []
end_state:
primary_silhouette_read:
weapon_or_prop_continuity:
contact_points:
camera_and_crop:
identity_reference:
output_layout: independent_frames | pose_sheet | atlas_candidate
```

Prefer a small set of meaningful key poses over many weak intermediate images when timing/interpolation will be decided later in-engine.

## Sequence continuity checks

Review:

- body/limb count and anatomy continuity;
- handedness and weapon grip;
- prop location and orientation;
- costume details and accessories;
- face/hair identity;
- ground/contact consistency;
- camera scale and crop;
- action direction and silhouette readability;
- no accidental state jump between adjacent key poses.

## Atlas and runtime boundary

A generated pose sheet or atlas candidate is visual planning/reference until export and runtime contracts are separately satisfied.

Do not invent:

- frame duration;
- interpolation behavior;
- collision/hitbox timing;
- Godot `SpriteFrames`/AnimationPlayer proof;
- actual runtime performance.

If an atlas is needed, record expected frame order, dimensions, padding/bleed assumptions, alpha requirement, and naming. Runtime import remains a later gate.

## Figma organization

Use direct Figma placement for candidate comparison. Place new pose/action candidates in `02_WIP` when write access is available. After explicit user approval, retain the selected identity/pose reference in the appropriate `01_APPROVED_REFERENCE` character/unit section; reusable pose structure may also qualify for the existing reuse-harvest process.

Figma pose approval does not grant `PROJECT_ASSET_APPROVED` or runtime animation proof.
