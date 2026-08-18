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
