# Pixel Art Reference Source Integration Design

## Goal

Add durable, role-separated reference sources for pixel art and low-resolution 2D game art without creating a new broad Skill or turning the user's current pixel-art preference into a universal Base art rule.

## Existing Solution First

Reuse these current owners without duplicating their policy text:

- `docs/knowledge/game-development/PERIODIC_EXTERNAL_SOURCE_WATCHLIST.md` for source roles and evidence ceilings.
- `docs/knowledge/game-development/PERIODIC_EXTERNAL_SOURCE_DISCOVERY_SEEDS.md` for immediately useful discovery sources and explicit consumer routing.
- `docs/knowledge/game-development/ART_DIRECTION_AND_ASSET_PLANNING_GUIDE.md` for art-direction and production decisions.
- `docs/knowledge/game-development/GAME_BUILD_SIZE_AND_ASSET_OPTIMIZATION_GUIDE.md` for pixel-art texture protection and measured build-size claims.
- `skills/designing-art-prompts-and-technique-cards/SKILL.md` for technique-card production and visual QA.

The current Art Guide already owns visual direction/production trade-offs, and the current Build Size Guide already contains a `2D·pixel art 보호` section plus measured download/install/runtime/patch evidence. Therefore the smallest change is to add pixel-art sources and name these existing consumers from the discovery-seed contract rather than duplicating the same rules into multiple canonical files.

No new ACTIVE Skill, registry identity, source domain, workflow authority, Ruleset, or Required Check topology is needed.

## Source roles

### Aseprite official docs and source repository

- Role: `AUTHORITY_TARGET` for Aseprite product behavior and production workflow only.
- Surfaces: docs, animation, tilemap, indexed color/palette, sprite-sheet export, CLI/scripting, releases/source repository.
- Use for: sprite/animation organization, reusable cels/tags, tile workflows, palette/indexed-color choices, export automation, sprite-sheet metadata.
- Ceiling: Aseprite behavior is not a universal pixel-art rule. Source/binary licensing must be checked separately; repository popularity is not authority.

### Godot official docs — pixel-art rendering surfaces

This is not a new source family. Reuse the existing Godot official authority and explicitly scan:

- multiple resolutions for pixel art,
- viewport stretch and integer scaling,
- nearest texture filtering,
- 2D texture/import/compression behavior,
- TileMap/TileSet and sprite/atlas integration when relevant.

Use current stable/versioned docs and preserve exact Godot version. Do not turn one recommended baseline resolution into a universal project constant.

### Saint11 / Pedro Medeiros pixel-art tutorials

- Role: `PROFESSIONAL_PRACTICE`.
- Surfaces: beginner series, compact tutorials, glossary/articles, original tutorial repository when useful.
- Use for: cluster thinking, shading, anti-aliasing/banding, line work, color, animation, low-resolution readability, export habits.
- Ceiling: creator practice and educational material, not a universal hard rule. Preserve game/style/context and avoid copying identifiable finished designs.

### Lospec

- Role: `DISCOVERY_FEED` plus bounded `PROFESSIONAL_PRACTICE` for Lospec-authored educational/tool material.
- Surfaces: tutorial index, palette list, software list, pixel editor/tools, scaler/rotator, Blender toolkit where relevant.
- Use for: technique discovery, palette candidates, restrictive-art tooling, comparison vocabulary.
- Ceiling: community/tutorial aggregation, palettes, gallery popularity, or tool output are not proof that a choice fits the project. Trace third-party tutorials to their original authors when possible.

### PixelJoint

- Role: `DISCOVERY_FEED` / community observational reference.
- Surfaces: gallery, weekly challenges, forums/comments, artist pages.
- Use for: visual vocabulary, readability comparisons, cluster/style examples, anti-examples, critique questions.
- Ceiling: ratings, favorites, featured status, or community popularity are not quality authority or market evidence. Never copy identifiable artwork or a specific artist's signature style.

## Explicit consumers

The discovery seed must route pixel-art findings to existing owners:

```text
art direction / visual-system fit
→ ART_DIRECTION_AND_ASSET_PLANNING_GUIDE.md

pixel technique card / prompt / visual QA
→ designing-art-prompts-and-technique-cards

Godot render/import/version behavior
→ existing Godot source owner + project implementation owner

build-size motivation
→ GAME_BUILD_SIZE_AND_ASSET_OPTIMIZATION_GUIDE.md
```

The art Guide remains responsible for whether pixel art is appropriate for a project. A project may declare pixel art as its preferred visual direction, but Base itself does not force pixel art onto unrelated projects.

## Pixel-art technique routing

The sources should support these technique questions without creating a new owner:

```text
canvas/base resolution
→ sprite scale and silhouette
→ pixel clusters and line economy
→ palette/value grouping
→ dithering/AA/banding decisions
→ tile/grid reuse
→ frame count/timing/animation readability
→ sprite sheet/tag/slice export
→ Godot nearest/integer scaling/render/import settings
→ build-size/runtime validation
→ rights/provenance and similarity QA
```

## Evidence and adversarial boundaries

Reject these overgeneralizations:

- pixel art automatically means a smaller shipped build,
- fewer colors automatically means better readability,
- nearest filtering is correct for every 2D texture,
- a Lospec palette is automatically suitable or licensed for product use,
- community likes/ratings prove quality,
- one Saint11 tutorial is a mandatory production law,
- Aseprite is required for all pixel-art work,
- a low base resolution is always better,
- copying a tutorial/gallery example is acceptable because it is educational/reference material.

When size is a motivation, route to the existing Build Size owner and require its actual measurement model. Existing measured evidence, not pixel-art aesthetics alone, owns byte-saving claims.

## Testing

Extend the already-wired discovery-seed regression to require:

- Aseprite, Godot pixel-art surfaces, Saint11, Lospec, and PixelJoint;
- source roles and claim ceilings;
- explicit routing to the existing Art Guide, Build Size Guide, and art technique Skill;
- the existing Art Guide's Visual Requirement ownership and the existing Build Size Guide's `2D·pixel art 보호`/measurement contract;
- no universal pixel-art default or unmeasured size claim.

## Automation consumer

After merge, update the existing source-scan and weekly-review automation prompts without changing their schedules so pixel-art/game-art sources are actually scanned and routed into the existing art/build-size owners.

## Expected direction

Move Base from generic art references toward a reusable pixel-art production evidence path: visual technique + production tooling + engine rendering + measured size/readability validation, while preserving project-specific art-direction decisions.