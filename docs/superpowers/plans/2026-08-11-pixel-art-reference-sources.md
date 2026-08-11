# Pixel Art Reference Source Integration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add pixel-art/game-art technique sources to the existing Base research and art-production routing without creating a new Skill or making pixel art a universal project rule.

**Architecture:** Extend the existing active discovery seed contract with role-separated pixel-art sources and explicit links to the already-existing Art Direction, Build Size, art-technique Skill, and Godot consumers. Reuse the already-wired discovery-seed regression file, so no new CI topology or duplicated owner policy is needed.

**Tech Stack:** Markdown contracts, Python `unittest`, GitHub Actions existing Evidence Knowledge workflow, GitHub PR/Ruleset validation.

## Global Constraints

- No new ACTIVE Skill, registry identity, source domain, workflow authority, Ruleset, or Required Check topology.
- Pixel art may be a project preference; Base must not force it onto unrelated projects.
- Aseprite official docs are authoritative only for Aseprite behavior/workflow.
- Godot official docs remain the authority for Godot pixel-art rendering/import behavior and must preserve exact stable/versioned context.
- Saint11 is `PROFESSIONAL_PRACTICE`; Lospec and PixelJoint are bounded discovery/community references.
- Popularity, likes, favorites, ratings, stars, or featured status are not Evidence authority.
- Pixel art does not automatically prove smaller shipped builds; size claims route to the existing measured Build Size owner.
- Reference material must not be copied as identifiable finished art or a specific artist's signature style.

---

### Task 1: Lock pixel-art source behavior with a failing regression

**Files:**
- Modify: `tests/test_periodic_external_source_discovery_seeds.py`

**Interfaces:**
- Consumes: current discovery seeds plus existing Art and Build Size owners.
- Produces: a regression that requires new source identities, role boundaries, explicit consumer routing, and preservation of existing owner contracts.

- [ ] **Step 1: Add a new failing test method**

Require in the discovery seed:

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
ART_DIRECTION_AND_ASSET_PLANNING_GUIDE.md
GAME_BUILD_SIZE_AND_ASSET_OPTIMIZATION_GUIDE.md
designing-art-prompts-and-technique-cards
BLOCKED_UNVERIFIED
```

Also confirm the current Art Guide still owns `Visual Requirement Gate` and the current Build Size Guide still contains `2D·pixel art 보호`, `DOWNLOAD`, `INSTALLED`, `RUNTIME`, and `PATCH` measurement language.

- [ ] **Step 2: Run the existing Evidence Knowledge workflow on a draft PR**

Expected RED: all existing tests pass and only the new pixel-art source test fails because the new source section is absent.

- [ ] **Step 3: Record exact RED head and failure reason**

Do not count unavailable local/container runs as PASS or FAIL.

---

### Task 2: Add pixel-art/game-art active discovery sources and consumer routing

**Files:**
- Modify: `docs/knowledge/game-development/PERIODIC_EXTERNAL_SOURCE_DISCOVERY_SEEDS.md`

**Interfaces:**
- Consumes: source roles/new-site promotion rules from `PERIODIC_EXTERNAL_SOURCE_WATCHLIST.md` and existing art/build-size owners.
- Produces: immediately scannable pixel-art source seeds plus explicit owner routing.

- [ ] **Step 1: Add `Pixel Art / low-resolution 2D game art` sources**

Define:

```text
Aseprite official docs + official repository
- AUTHORITY_TARGET for Aseprite behavior/workflow only
- docs, animation, tilemap, indexed color/palette, sprite sheet, CLI/scripting, releases/source

Godot official pixel-art surfaces
- reuse existing Godot AUTHORITY_TARGET
- multiple resolutions, viewport/integer scaling, nearest filtering, 2D import/compression, TileSet/TileMap/atlas integration

Saint11 / Pedro Medeiros
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

Cover canvas/base resolution, sprite scale/silhouette, pixel clusters, palette/value grouping, dithering/AA/banding, tile/grid reuse, frame timing/readability, sprite sheet/tag/slice export, Godot filtering/integer scaling, build-size evidence, rights/provenance.

- [ ] **Step 3: Add explicit existing consumers**

Route:

```text
art fit → ART_DIRECTION_AND_ASSET_PLANNING_GUIDE.md
technique cards / visual QA → designing-art-prompts-and-technique-cards
Godot behavior → existing Godot authority + project implementation owner
size motivation → GAME_BUILD_SIZE_AND_ASSET_OPTIMIZATION_GUIDE.md
```

- [ ] **Step 4: Add evidence ceilings**

State that popularity is not authority, tutorials are not universal laws, Aseprite is not mandatory, palettes are not automatically project-fit/licensed, community examples cannot be copied, pixel art is not a Base-wide default, and size benefits remain `BLOCKED_UNVERIFIED` until measured through the existing size owner.

---

### Task 3: GREEN validation and adversarial review

**Files:**
- Re-run: `tests/test_periodic_external_source_discovery_seeds.py`
- Validate through existing Evidence Knowledge, Base v9, and Game Project OS workflows.

**Interfaces:**
- Consumes: Task 2 exact branch head.
- Produces: reviewed exact-head evidence for merge.

- [ ] **Step 1: Commit the minimal production change**
- [ ] **Step 2: Confirm Evidence Knowledge regression is GREEN**
- [ ] **Step 3: Run Base v9 and Game Project OS required checks**
- [ ] **Step 4: Perform adversarial review**

Attack:

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

### Task 4: Post-merge consumer connection

**Files:**
- No repository file unless a post-merge omission is found.
- Update existing `Base 개선 소스 스캔` and `주간 작업 개선 보고서` automation prompts only.

**Interfaces:**
- Consumes: merged main pixel-art discovery contract.
- Produces: periodic scans that actually inspect and correctly classify the new sources.

- [ ] **Step 1: Read merged main and same-goal PR state**
- [ ] **Step 2: Update both automation prompts without changing schedules**
- [ ] **Step 3: Require reports to distinguish tool/engine authority, professional technique, community discovery, measured size evidence, and unverified scope**
- [ ] **Step 4: Close `POST_CHANGE_MONITOR_LOOP` with `NO_MATERIAL_FOLLOWUP` or a bounded follow-up finding**
