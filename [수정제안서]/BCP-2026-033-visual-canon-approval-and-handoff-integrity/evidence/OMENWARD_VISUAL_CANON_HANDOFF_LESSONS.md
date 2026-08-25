# OMENWARD Visual Canon / Handoff Lessons · BCP-2026-033 Evidence

## Evidence classification

```yaml
source_project: alsdmlals4-eng/omenward
source_decision: OMW-PLAN-20260825-FRONT-STATE-MINIMAP-SD-FANTASY-01
source_pr: https://github.com/alsdmlals4-eng/omenward/pull/210
source_commit_at_capture: 315d5e48b2a2d49f9d9863f3d07b66ba651bf9f7
captured_at: 2026-08-25
evidence_kind: PROJECT_DERIVED_WORKFLOW_LESSON
human_visual_approval: OBSERVED
runtime_readability: NOT_RUN
human_usability: NOT_RUN
rights_review: NOT_RUN
base_implementation_authority: NONE
```

## Existing Base overlap checked first

Fresh Base main already contains `BCP-2026-032-ai-visual-continuity-and-notion-preview-fallback`, approved for implementation from Ninja Survival evidence.

BCP-032 already owns:
- persistent protagonist visual identity via additive layers;
- inline SVG raster **preview-only transport fallback** for Notion when stronger transport is unavailable.

This OMENWARD evidence does not propose those again. Its distinct reusable issue is **how an approved visual becomes durable current canon across repository + human workspace + handoff when old visual lineage remains present**.

## What actually went wrong

### Incident 1 — project/reference context was under-read before generation

A generated visual drifted toward a generic fantasy/RPG composition. The user corrected that OMENWARD is a commander/territory/auto-battler product, not a hero-avatar adventure.

Root cause:
- generation began from incomplete product/style reconstruction rather than fresh visual owner + approved/reference asset readback.

Lesson:
- if an approved/reference visual exists, a new visual session must refetch it before generation instead of relying on prose memory.

### Incident 2 — improved composition still missed the established art lineage

A later candidate improved the commander/three-front composition but still missed the project’s existing fantasy+magic+SD lineage. The user explicitly stopped image generation and required the project and Notion mockups to be inspected first.

Lesson:
- `style = words` is weaker than `style = approved reference + explicit retained/superseded attributes`.

### Incident 3 — new current Decision coexisted with old human-facing visual material

The project retained useful older North Star and `Anime Pixel + Clean Pixel` documents. A new Decision superseded the long-road/no-minimap/standalone-style interpretation while keeping some hierarchy/faction-contrast value.

Deleting all legacy visual material would have destroyed lineage. Leaving it untouched would make the new state ambiguous.

The effective pattern was:

```text
new Decision with same ID across current surfaces
+ high-authority repository router update
+ explicit PARTIALLY_SUPERSEDED / REFERENCE_ONLY boundaries
+ current override at top of human-facing Notion surfaces
+ approved image before old North Star
+ durable Asset ID/full-res locator/hash
+ destination readback
+ new-session handoff with approved-asset refetch requirement
```

Lesson:
- current override first + explicit supersession preserves history without letting history remain current.

### Incident 4 — conversation image existence was not durable project authority

The user-approved image initially existed only as a generated conversation file. Closeout hardened it into:

- `OM-IMG-023` stable identity;
- full-resolution 1536×1024 PNG stored by durable Drive file ID;
- repository asset metadata with SHA-256 and Decision relationship;
- Notion Home/Visual Bible current inline preview;
- Notion destination fetch returning a Notion-hosted `prod-files-secure` image URL;
- exact new-session handoff/read order.

Lesson:
- visual closeout is not complete at “image exists”; asset persistence + canon placement + supersession + readback + handoff belong to one lifecycle.

## What worked

### Same Decision ID across surfaces

`OMW-PLAN-20260825-FRONT-STATE-MINIMAP-SD-FANTASY-01` ties repository spec/index, Notion current override and Sheet compatibility rows together.

### Current human visual before legacy visual

Notion Home and Visual Bible show the current approved visual/override before the older North Star. Old visual evidence remains visible as lineage.

### Full-resolution authority separate from preview

The full-resolution asset is owned by a stable Drive file ID while the repository owns metadata/hash/Decision locator. Notion hosts a convenient current preview. Temporary signed Notion URLs are not treated as durable IDs.

This transport detail itself is not a new BCP-033 invention; the inline-SVG fallback pattern is already BCP-032 territory.

### Evidence ceilings stayed separate

The user approved the visual direction/reference, but the project still marks runtime/minimap readability, human usability, player experience and rights review as `NOT_RUN`.

## Project-only material excluded from Base

- OMENWARD 3-front layout and per-front minimaps;
- 3×3 roulette;
- Omen Warden and long command flag;
- Veil world/faction language;
- Fantasy/Magic/SD Tactical Pixel style/palette;
- OMENWARD IDs, page IDs and asset IDs.

## Generic checklist candidate

```text
[ ] Was the visual/reference actually human-approved?
[ ] Stable Decision ID + Asset ID exist?
[ ] Full-resolution asset or durable locator exists?
[ ] RETAIN / SUPERSEDE / REFERENCE_ONLY boundaries explicit?
[ ] Repository current visual router points to it?
[ ] Human-facing current visual/override appears before stale visual lineage?
[ ] Destination image block and structured locator read back?
[ ] New-session handoff points to exact asset, not prose memory only?
[ ] Future generation must refetch current approved reference first?
[ ] Visual approval separated from runtime/accessibility/rights/human usability evidence?
```

## Separate operational incident — do not duplicate Base governance

During the broader project session an accidental placeholder file was briefly written to OMENWARD main and immediately reverted. This reinforces existing Base branch/PR safety rules but is not a BCP-033 scope. No new direct-main governance rule is proposed here.

## Promotion disposition

```text
reuse_mode: PROJECT_DERIVED_PATTERN_CANDIDATE
project_only_lessons: OMENWARD visual identity/art/layout remain local
base_promotion_candidate: APPROVED_VISUAL_CANON_HANDOFF_INTEGRITY
existing_related_bcp: BCP-2026-032-ai-visual-continuity-and-notion-preview-fallback
relationship_to_existing: COMPLEMENT_NOT_DUPLICATE
cross_project_validation: NOT_RUN
active_base_implementation: NOT_AUTHORIZED
```

This is sufficient for a proposal submission, not for claiming a proven Base method. Review must decide whether the new canon/handoff invariant is materially distinct enough to implement or should instead be folded into an existing owner/BCP.
