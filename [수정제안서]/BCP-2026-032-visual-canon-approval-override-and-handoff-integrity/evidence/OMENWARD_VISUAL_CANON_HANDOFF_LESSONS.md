# OMENWARD Visual Canon / Handoff Lessons · BCP-2026-032 Evidence

## Evidence classification

```yaml
source_project: alsdmlals4-eng/omenward
source_decision: OMW-PLAN-20260825-FRONT-STATE-MINIMAP-SD-FANTASY-01
source_pr: https://github.com/alsdmlals4-eng/omenward/pull/210
source_commit_at_capture: 315d5e48b2a2d49f9d9863f3d07b66ba651bf9f7
captured_at: 2026-08-25
evidence_kind: PROJECT_DERIVED_WORKFLOW_LESSON
runtime_evidence: NOT_APPLICABLE_TO_VISUAL_APPROVAL
human_visual_approval: OBSERVED
base_implementation_authority: NONE
```

## What actually went wrong

### Incident 1 — project identity was under-read before generation

A generated visual drifted toward a generic fantasy/RPG composition. The user corrected that OMENWARD is a commander/territory/auto-battler experience, not a hero-avatar adventure. The root cause was not image-model quality alone; it was **insufficient refetch of project/Notion visual authority before generation**.

Lesson:
- visual generation must begin from current project visual owner + approved/reference assets, not from generic genre inference or conversation memory alone.

### Incident 2 — a subsequent generation still missed the established art lineage

After the battlefield/commander intent improved, the generated art style still did not match the older approved fantasy+magic+SD lineage. The user explicitly stopped image generation and required the assistant to inspect the project and Notion mockups first.

Lesson:
- a prose style label is weaker than an actual approved/reference visual. When a project has visual references, the generation gate should refetch them and record which qualities are retained/superseded.

### Incident 3 — current Decision existed while older human-facing visuals remained prominent

The repository/Notion had accumulated older North Star and `Anime Pixel + Clean Pixel` language. A new user Decision superseded long-road/no-minimap/standalone-style assumptions, but old content remained useful historical evidence.

A destructive rewrite was not required. The effective fix was:
- current Decision in high-authority repository routers;
- explicit `PARTIALLY_SUPERSEDED`/`REFERENCE_ONLY` relationships;
- a current override at the top of Notion Visual surfaces;
- the approved new image before the old North Star;
- durable Asset ID + full-resolution locator + hash;
- handoff instructing new sessions to refetch the approved asset before generation.

Lesson:
- **current override first + explicit supersession** preserves lineage without allowing stale visuals to dominate.

### Incident 4 — image existence is not enough for a durable handoff

The approved image originally existed as a conversation-generated file. That is insufficient as a cross-session project authority.

Closeout hardened it by creating:
- stable `OM-IMG-023` identity;
- full-resolution Drive file with stable file ID;
- repository metadata/hashes/Decision relationship;
- Notion-native inline preview on Visual Bible and Home;
- destination readback showing an actual Notion-hosted image block;
- a new-session handoff with exact read order and superseded assumptions.

Lesson:
- visual closeout should treat **asset persistence + human-surface placement + readback + handoff** as one lifecycle.

## What worked

### 1. Same Decision ID across surfaces

`OMW-PLAN-20260825-FRONT-STATE-MINIMAP-SD-FANTASY-01` ties together:
- repository structured visual specification;
- current decision routing;
- Notion current override;
- Sheet compatibility log;
- approved image record.

This made later readback and conflict classification deterministic.

### 2. Human-facing current visual before legacy material

The Notion Home and Visual Bible now show the approved current visual before the older North Star. Older visual evidence is still available below, but the page no longer requires the reader to understand chronology manually.

### 3. Full-resolution authority separate from inline preview

The human page uses a Notion-native inline preview while a stable Drive file ID owns the full-resolution 1536×1024 PNG. The repository records SHA-256 and locators rather than forcing a large binary into Git history.

This preserves human usability and repository cleanliness without making temporary signed Notion URLs into durable identifiers.

### 4. Evidence ceilings stayed separate

The user approved visual direction/reference, but the project still marks:
- runtime readability `NOT_RUN`;
- minimap readability `NOT_RUN`;
- human usability `NOT_RUN`;
- player experience `NOT_RUN`;
- rights review `NOT_RUN`.

This prevented a visual approval from becoming a fake product PASS.

## What should not be generalized

Do not promote these OMENWARD specifics to Base:
- three Front-State panels;
- per-front minimaps;
- 3×3 roulette;
- Omen Warden commander;
- long command flag;
- Fantasy/Magic/SD Tactical Pixel style;
- faction palettes/shape language;
- Drive/Notion IDs;
- OMENWARD Decision/Asset identifiers.

Only the **approval persistence / supersession / refetch / readback / handoff** workflow is a Base candidate.

## Failure-prevention checklist candidate

A generic future visual closeout could ask:

```text
[ ] Did a human actually approve this visual/reference/direction?
[ ] Does it have a stable Decision ID and Asset ID?
[ ] Is the full-resolution asset or durable locator preserved?
[ ] Are adopted vs superseded vs reference-only parts explicit?
[ ] Does the repository's current visual router point to it?
[ ] Does the human-facing Home/Bible show the current visual before stale visuals?
[ ] Was the human-facing image block read back after write?
[ ] Does the new-session handoff point to the exact asset, not just prose?
[ ] Must the next generation refetch this approved asset first?
[ ] Are visual approval, runtime readability, accessibility, rights and human usability still separate evidence states?
```

## Related project-only operational incident

During the same broader visual planning session, an accidental placeholder file was briefly written to OMENWARD `main` and immediately reverted. This reinforces existing Base branch/PR safety rules but is **not the primary BCP-032 problem**, because Base already owns direct-main/open-PR safety. BCP-032 should not duplicate that governance scope.

## Promotion disposition

```text
reuse_mode: PROJECT_DERIVED_PATTERN_CANDIDATE
project_only_lessons: OMENWARD visual identity/art/layout remain local
base_promotion_candidate: APPROVED_VISUAL_CANON_CLOSEOUT_INVARIANT
cross_project_validation: NOT_RUN
active_base_implementation: NOT_AUTHORIZED
```

The evidence is strong enough to submit a Base proposal because the workflow problem is generic, but not strong enough to claim the Base method is implemented or proven across multiple projects. Cross-project adoption/regression evidence belongs to a later approval/implementation gate.
