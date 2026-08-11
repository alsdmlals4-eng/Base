# Pixel Art Reference Source Integration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add pixel-art/game-art technique sources to the existing Base research and art-production routing without creating a new Skill or making pixel art a universal project rule.

**Architecture:** Extend the existing active discovery seed contract with role-separated pixel-art sources, then connect those sources to the existing Art Direction and Build Size owners. Reuse the already-wired discovery-seed regression file so no new CI topology is needed.

**Tech Stack:** Markdown contracts, Python `unittest`, GitHub Actions existing Evidence Knowledge workflow, GitHub PR/Ruleset validation.

## Global Constraints

- No new ACTIVE Skill, registry identity, source domain, workflow authority, Ruleset, or Required Check topology.
- Pixel art may be a project preference; Base must not force it onto unrelated projects.
- Aseprite official docs are authoritative only for Aseprite behavior/workflow.
- Godot official docs remain the authority for Godot pixel-art rendering/import behavior and must preserve exact stable/versioned context.
- Saint11 is `PROFESSIONAL_PRACTICE`; Lospec and PixelJoint are bounded discovery/community references.
- Popularity, likes, favorites, ratings, stars, or featured status are not Evidence authority.
- Pixel art does not automatically prove smaller shipped builds; size claims require measured build/runtime evidence.
- Reference material must not be copied as identifiable finished art or a specific artist's signature style.

---

### Task 1: Lock pixel-art source behavior with a failing regression

**Files:**
- Modify: `tests/test_periodic_external_source_discovery_seeds.py`

**Interfaces:**
- Consumes: current `PERIODIC_EXTERNAL_SOURCE_DISCOVERY_SEEDS.md`, `ART_DIRECTION_AND_ASSET_PLANNING_GUIDE.md`, and `GAME_BUILD_SIZE_AND_ASSET_OPTIMIZATION_GUIDE.md`.
- Produces: a regression that requires pixel-art sources, role boundaries, existing-owner routing, and measured size claims.

- [ ] **Step 1: Add a new failing test method**

Add `test_pixel_art_sources_route_to_existing_art_and_size_owners` that reads the three files and requires at least these strings:

```text
Aseprite
https://www.aseprite.org/docs/
https://github.com/aseprite/aseprite
Saint11
https://saint11.org/blog/pixel-art-tutorials/
Lospec
https://lospec.com/
PixelJoint
https://pixeljoint.com/
AUTHORITY_TARGET
PROFESSIONAL_PRACTICE
DISCOVERY_FEED
integer scaling
nearest
pixel clusters
banding
palette
sprite sheet
BLOCKED_UNVERIFIED
```

The test must also assert that the art guide names the discovery-seed file and the size guide states that pixel art does not automatically prove a smaller shipped build.

- [ ] **Step 2: Run the existing Evidence Knowledge test set on the branch**

Use the repository's existing Evidence Knowledge GitHub Actions path by opening a draft PR after committing the RED test. Expected result: the existing tests pass and the new pixel-art test fails because the new source/routing text is not yet present.

- [ ] **Step 3: Record the exact RED head and failure reason in the PR body**

Do not count any unavailable local/container run as PASS or FAIL.

---

### Task 2: Add pixel-art/game-art active discovery sources

**Files:**
- Modify: `docs/knowledge/game-development/PERIODIC_EXTERNAL_SOURCE_DISCOVERY_SEEDS.md`

**Interfaces:**
- Consumes: source roles and new-site promotion rules from `PERIODIC_EXTERNAL_SOURCE_WATCHLIST.md`.
- Produces: immediately scannable source seeds for the periodic source system.

- [ ] **Step 1: Add an `Pixel Art / low-resolution 2D game art` section**

Define these sources and roles:

```text
Aseprite official docs + official repository
- AUTHORITY_TARGET for Aseprite behavior/workflow only
- docs, animation, tilemap, indexed color/palette, sprite-sheet, CLI/scripting, releases/source

Godot official pixel-art surfaces
- reuse existing Godot AUTHORITY_TARGET
- multiple resolutions, viewport/integer scaling, nearest texture filtering, 2D import/compression, TileSet/TileMap/atlas integration

Saint11 / Pedro Medeiros pixel-art tutorials
- PROFESSIONAL_PRACTICE
- beginner series, compact tutorials, glossary/articles, original tutorial repository

Lospec
- DISCOVERY_FEED; Lospec-authored material may be bounded PROFESSIONAL_PRACTICE
- tutorials, palettes, software/tools, scaler/rotator, restrictive-art resources

PixelJoint
- DISCOVERY_FEED / community observational reference
- gallery, challenges, forums/comments, artist pages
```

- [ ] **Step 2: Add technique questions**

Require scanning for canvas/base resolution, sprite scale/silhouette, pixel clusters, palette/value grouping, dithering/AA/banding, tile/grid reuse, animation frame timing/readability, sprite-sheet export, Godot filtering/integer scaling, and rights/provenance.

- [ ] **Step 3: Add evidence ceilings**

State explicitly that popularity is not authority, tutorials are not universal laws, Aseprite is not mandatory, one palette is not automatically project-fit/licensed, and community/tutorial examples must not be copied as identifiable finished work.

---

### Task 3: Connect sources to the existing art owner

**Files:**
- Modify: `docs/knowledge/game-development/ART_DIRECTION_AND_ASSET_PLANNING_GUIDE.md`

**Interfaces:**
- Consumes: the periodic discovery seed source pool.
- Produces: a pixel-art technique routing contract owned by the existing Art Direction guide.

- [ ] **Step 1: Add a bounded `Pixel-art / low-resolution 2D technique route` section**

State that when a project declares pixel art or low-resolution 2D as a preferred direction, the guide may use the discovery-seed sources for technique/reference research.

- [ ] **Step 2: Preserve project-specific authority**

State that pixel art is not a Base-wide default and that readability, identity, production capacity, platform/viewing distance, accessibility, animation cost, and technical constraints still decide the actual project direction.

- [ ] **Step 3: Route source roles**

Use Aseprite for tool/export workflow, Godot for engine/render/import behavior, Saint11 for professional technique reference, Lospec for palette/tutorial/tool discovery, and PixelJoint for community visual comparison/critique questions.

---

### Task 4: Harden the size claim for pixel art

**Files:**
- Modify: `docs/knowledge/game-development/GAME_BUILD_SIZE_AND_ASSET_OPTIMIZATION_GUIDE.md`

**Interfaces:**
- Consumes: existing download/installed/runtime/patch measurement model.
- Produces: a pixel-art-specific claim ceiling for build-size motivation.

- [ ] **Step 1: Extend `2D·pixel art 보호`**

Add that lower source resolution, limited palettes, or indexed authoring can reduce some source or texture data in some pipelines, but they do not automatically prove a smaller shipped build because engine resources, atlas padding, lossless compression, import settings, duplicated variants, audio/video, and package structure can dominate.

- [ ] **Step 2: Require actual measurements**

Require before/after `sprite_and_2d_art`, delivered/install/runtime values where relevant, and visual/readability checks before claiming size improvement.

---

### Task 5: GREEN validation and adversarial review

**Files:**
- Re-run: `tests/test_periodic_external_source_discovery_seeds.py`
- Validate through existing Evidence Knowledge, Base v9, and Game Project OS workflows.

**Interfaces:**
- Consumes: Tasks 1-4 exact branch head.
- Produces: reviewed exact-head evidence for merge.

- [ ] **Step 1: Commit the minimal production changes**
- [ ] **Step 2: Confirm Evidence Knowledge regression is GREEN**
- [ ] **Step 3: Run Base v9 and Game Project OS required checks**
- [ ] **Step 4: Perform adversarial review**

Attack at least:

```text
pixel-art-as-universal-default
size-saving-overclaim
palette-license-overclaim
community-popularity-as-authority
creator-style-copying
Aseprite-required overreach
Godot-version staleness
new-Skill inflation
discovery-source consumer omission
```

- [ ] **Step 5: Recheck same-goal PRs, unresolved review threads, mergeability, and latest main**
- [ ] **Step 6: Mark ready and expected-head squash merge only if all required gates pass**

---

### Task 6: Post-merge consumer connection

**Files:**
- No repository file unless a post-merge omission is found.
- Update the existing `Base 개선 소스 스캔` and `주간 작업 개선 보고서` automation prompts only.

**Interfaces:**
- Consumes: merged main pixel-art discovery/source contract.
- Produces: periodic scans that actually inspect the new sources.

- [ ] **Step 1: Read merged main and same-goal PR state**
- [ ] **Step 2: Update both automation prompts without changing their schedules**
- [ ] **Step 3: Require reports to distinguish technique reference, engine/tool authority, community discovery, measured size evidence, and unverified scope**
- [ ] **Step 4: Close the post-change adversarial loop with `NO_MATERIAL_FOLLOWUP` or a bounded follow-up finding**
