# Sprite Animation → Project Figma Delivery Design

**Status:** Approved direction; implementation planning required
**Date:** 2026-08-12
**Scope owner:** Base shared-tool package

## Goal

Each project GPT can use the common Sprite Animation Studio capability while working in its own project workspace. When it generates an approved visual result—character expression changes, pose sequences, staged effects, or sprite-action frames—the project GPT sends that result to the **generation area of its own project Figma file** using the Figma tool.

The workflow is direct: there is no user ZIP download and no cross-chat archive handoff.

```text
project GPT + project context
  → generate or curate approved visual result
  → choose the appropriate Sprite Animation mode
  → validate project/Figma target and lineage
  → Figma tool uploads and places result in that project's generation area
```

## Operating boundary

- The shared Base tool provides the modes, request/lineage contract, validation, and Figma-placement instructions.
- A project GPT owns the actual project context, generated images, project ID, and its Figma destination.
- The project GPT must run the action in the same project conversation/workspace that contains the image result. A standalone local browser run or a different chat cannot silently transfer local files into a project Figma file.
- The Figma connector is used by the project GPT only after it resolves an exact registry target and validates the result. Base never stores Figma credentials or project image binaries.

## Common modes

| Mode | Use | Required review |
|---|---|---|
| `expression_variation` | Same character, emotion/expression changes | face, silhouette, costume and palette consistency |
| `pose_sequence` | Same character, action poses or sprite frames | direction, pose continuity, readable anticipation/impact/recovery |
| `effect_stages` | Effect startup, active, impact and fade frames | timing order, origin, scale and readability on the target background |
| `sprite_action` | Curated game-ready action row | full selected order, FPS, loop and atlas/Godot handoff metadata |

Every mode requires an approved anchor and a Figma lineage link. A generation result is a candidate until the project GPT or user explicitly accepts it for the project Figma generation area.

## Project Figma target registry

`docs/operations/PROJECT_FIGMA_TARGET_REGISTRY.json` records canonical project IDs and Figma file keys. It is a routing registry, not a copy of Figma content and not proof that a page exists.

The supplied project files are registered for routing only. No live connector readback has verified a delivery page or generation-area node, so all eight entries remain `REGISTERED_NO_MUTATION` with null destination IDs. A file remains fail-closed until a connector creates or resolves the destinations and records exact readback evidence.

When mutation is allowed, the project GPT creates or resolves one page named `Sprite Animation Studio` and one generation area named `Generated Assets`. Each approved result gets a new run section; old approved sections are never overwritten or deleted automatically.

## Delivery contract

The project GPT's `내보내기` action is not a file download. It is a guarded Figma delivery action:

1. Confirm the visual result belongs to the active project ID and mode.
2. Resolve the matching registry entry and confirm it is `READY_FOR_DELIVERY` with verified page and generation-area node IDs.
3. Verify the approved-anchor Figma URL, selected frame order, and asset bytes available in the current project workspace.
4. Upload supported image assets to the target Figma file and place them in `Generated Assets` with a run metadata card.
5. Return the exact Figma section URL and state what was uploaded, what was only metadata, and any validation not run.

The action blocks—not falls back to another project—when the project ID, file key, edit permission, Figma target page, image bytes, or anchor lineage is missing or conflicting.

## Explicit exclusions

- No ZIP download as the primary delivery mechanism.
- No direct cross-project Figma write and no guessed Figma destination.
- No mutation of a registry entry marked `REGISTERED_NO_MUTATION`.
- No Figma API key/token in Base, project prompts, generated images, or Git history.
- No claim that a Figma placement validates Godot import, runtime animation, licensing, or user acceptance.

## Rollback and verification

The project GPT creates a new named run section rather than replacing a prior approved result. Rollback removes or archives only that run section after review. It never removes the original anchor or unrelated project content.

Base verification covers target resolution, mode/lineage contracts, and fail-closed delivery eligibility. Project-level verification covers the real Figma upload, visual placement, project ownership, and any Godot runtime check.
