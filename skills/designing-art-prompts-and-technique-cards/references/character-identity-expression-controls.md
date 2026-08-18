# Character Identity and Expression Controls

Use this module for character expression edits, identity-preserving variants, portrait/emote candidates, and similar tasks after project canon/Figma approved references are resolved.

## Core rule

A requested expression change is a **bounded delta**, not permission to redesign the character.

Default protected axes:

```text
face geometry / proportions
hairstyle and hair silhouette
costume and equipment
palette and material language
body identity
framing/camera unless requested
lighting/art style unless requested
approved project motifs
```

Only relax a protected axis when the current request or project canon explicitly changes it.

## Expression contract

Separate three controls:

1. **facial movement** — brows, eyelids, cheeks, lips, jaw;
2. **gaze** — centered, left/right/up/down, target focus;
3. **head pose** — neutral, yaw, pitch, roll.

Do not let an expression request silently change all three.

Recommended prompt shape:

```yaml
identity_reference:
protected_axes: []
requested_expression:
facial_movement:
gaze:
head_pose:
intensity:
framing:
forbidden_drift: []
output_count:
```

## FACS vocabulary

FACS/action-unit labels may be used as optional control vocabulary when they make the requested facial movement clearer. They are not assumed to be a model-native command language.

Use natural language first, then optional AU guidance, side/direction, and intensity.

Example:

```text
Preserve the approved character identity and costume.
Change only the facial expression to a restrained alert look.
Raise the upper eyelids slightly; keep gaze centered; keep head pose neutral.
Optional control vocabulary: AU5, subtle intensity.
```

## Candidate comparison

Compare candidates on:

- identity preservation;
- requested expression accuracy;
- gaze/head-pose accuracy;
- eye/eyelash/brow/hair edge integrity;
- costume/accessory drift;
- approved palette/material/light consistency;
- usability at actual portrait/UI size.

A visually attractive candidate that changes identity is `REVISION_REQUIRED`, not a better variant.

## Figma organization

New expression variants are review candidates first. Use the Figma direct placement module to place them under the project's `02_WIP` character/expression area when write access exists. Explicit user approval is required before adding the selected result to the relevant `01_APPROVED_REFERENCE` character section.

Expression approval is still separate from `PROJECT_ASSET_APPROVED` and runtime consumption.
