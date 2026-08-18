# Figma-Direct Visual Skill Modules Design

Date: 2026-08-18
Issue: #514
Base main at design start: `fcfc8a57607c740b266fdea868b747510ffb335d`

## 1. Problem

The local Tool Hub / Character Studio path reached a real Windows stop-loss after repeated launcher/runtime/delivery failures. The user explicitly chose to stop further full local visual-tool repair and keep Figma as the project-by-project visual organization surface.

However, the useful domain knowledge built into Expression Studio, Sprite Animation Studio, Effect routes, candidate review, evidence handling, and the merged reusable visual harvest pipeline remains valuable for future image work.

The goal is therefore not to revive the runtime. It is to preserve reusable visual techniques as Base Skill reference modules and make direct Figma organization the normal visual workflow.

## 2. Existing Solution First

Reuse rather than duplicate:

- primary Skill owner: `skills/designing-art-prompts-and-technique-cards/SKILL.md`;
- visual continuity/conditional router: `references/figma-visual-bible-continuity-gate.md`;
- existing broad triggers: `image-prompt`, `image-mockup`, `image-approval`, `visual-qa-and-approval`;
- project Figma structure: `templates/project-operations/FIGMA_VISUAL_BIBLE_PROFILE.md`;
- reusable harvest: merged PR #433 and `Reusable Visual Harvest Gate`;
- product asset authority: existing `PROJECT_ASSET_APPROVED` / Asset Vault / promote boundaries.

Do not create a new broad Figma Skill, Expression Skill, Sprite Skill, parallel asset canon, or a larger Registry trigger surface when the existing art Skill already routes image work correctly.

## 3. Selected Architecture

Keep one primary art/image Skill. The Figma continuity gate chooses the focused module for the current task, while the primary `SKILL.md` contains only a compact direct index of all packaged references because Base package-integrity requires every reference/script to be directly discoverable from its owning Skill.

```text
designing-art-prompts-and-technique-cards/SKILL.md
├─ compact direct module index (discoverability/package integrity only)
└─ figma-visual-bible-continuity-gate.md (conditional runtime/reading router)
   ├─ figma-direct-placement-and-canon.md
   ├─ character-identity-expression-controls.md
   ├─ sprite-pose-sequence-controls.md
   ├─ effect-stage-compositing-controls.md
   ├─ candidate-review-and-reusable-harvest.md
   └─ local-visual-tool-lessons-and-fallback.md
```

The direct index does not mean all six modules are loaded for every image task. The gate still owns progressive disclosure and selects only the relevant module.

`skills/SKILL_REGISTRY.json` remains unchanged. Existing image-related triggers are sufficient.

This structure satisfies both goals:

- low routing ambiguity / low context cost;
- Base Skill package integrity and reference discoverability.

## 4. Figma Direct Placement Contract

### Before generation or editing

1. Read current project canon/Decisions.
2. Resolve the project's configured Figma file.
3. Read the relevant `01_APPROVED_REFERENCE` node(s), including `Keep / Avoid / Do Not Drift`.
4. Check `01.10_REUSABLE_COMPONENTS`, `01.11_STRUCTURE_PATTERNS`, and `01.12_VISUAL_DNA` before creating a new visual.

### After generation

New generated output is not automatically approved.

If Figma write capability is available to GPT:

```text
new candidate
→ auto-place in 02_WIP
→ use stable artifact naming
→ add/update WIP review metadata when useful
→ read back actual placement
→ compare against approved canon
→ user review
```

If Figma write capability is unavailable:

GPT must provide exact placement guidance containing:

- project Figma file;
- page;
- section;
- recommended frame/artifact name;
- status (`DRAFT_VISUAL` or `REVIEW_CANDIDATE`);
- approved reference IDs to compare against;
- what must happen before promotion.

### After explicit user approval

Only after explicit user approval may GPT with Figma write capability move/copy/reorganize the visual into the appropriate `01_APPROVED_REFERENCE` section and, when the visual is final-use material, `04_FINAL`.

Figma visual placement or approval does not grant:

- `PROJECT_ASSET_APPROVED`;
- tracked product asset status;
- licensing/right approval;
- Godot/runtime proof;
- human playtest/runtime validation.

## 5. Module Responsibilities

### Character identity / expression

Preserve character identity, face geometry, hairstyle, costume, palette, framing, lighting, and art style unless the request explicitly changes one of those axes. Expression edits separate facial movement, gaze, and head pose. FACS/action-unit language is optional control vocabulary, not model authority.

### Sprite / pose sequence

Preserve identity across pose/action variants. Define pose intent, silhouette/readability, camera/framing invariants, frame order, contact/weapon/prop continuity, and atlas/export expectations when relevant. Do not invent animation timing or runtime validation that was not executed.

### Effect stage / compositing

Describe effect stages, alpha/background behavior, temporal ordering, anchor/scale expectations, and reuse boundaries. Preserve distinction between effect visual reference and runtime VFX implementation.

### Candidate review / reusable harvest

Use multiple candidates only when comparison adds value. Compare identity/canon fit, requested delta, visual quality, implementation fitness, and reuse value. After primary-use success, classify with existing #433 categories such as `REUSE_AS_IS`, `VARIANT_SEED`, `STRUCTURE_PATTERN`, `STYLE_DNA`, `REBUILD_FOR_REUSE`, `ONE_OFF_KEEP`, or `REJECT_REUSE`.

### Local visual tool lessons / fallback

The local visual runtimes remain in Base as referenceable source and historical implementation evidence, but are not the canonical or required image-work path after the 2026-08-18 user-PC stop-loss. Do not require Tool Hub, localhost ports, PowerShell, Studio child processes, delivery tokens, or localhost Figma Bridge pairing for normal image generation/organization.

This status is scoped to the visual image workflow. It does not delete unrelated tooling or forbid future explicit experiments requested by the user.

The owning Skill learning log records this stop-loss and fallback so the module change is tied to observed operational evidence rather than a silent policy rewrite.

## 6. Skill Routing

Use the existing Registry entry for `designing-art-prompts-and-technique-cards` unchanged. Existing image-related triggers already route relevant tasks to the Skill.

The Skill's Figma continuity gate selects a focused module using observable task conditions:

- Figma placement/canon organization;
- character identity/expression edit;
- pose/sprite sequence;
- effect stages/compositing;
- candidate comparison/reuse harvest;
- local visual runtime status/fallback.

The main `SKILL.md` directly indexes the same six references only to satisfy package discoverability. It does not duplicate module content or replace gate-based conditional loading.

No new broad Skill ID or Registry trigger expansion is introduced.

## 7. Authority and Safety Invariants

- Latest user instruction and project canon outrank Figma.
- `02_WIP` and rejected work never become automatic generation canon.
- Explicit user approval is required before visual-reference/final promotion.
- Figma write availability changes execution convenience, not approval authority.
- `APPROVED_VISUAL_REFERENCE != PROJECT_ASSET_APPROVED`.
- Local Tool runtime code is preserved but not required by the normal image workflow.
- Unrelated QA tooling is not globally deprecated by this visual fallback.
- No paid OpenAI API or API-key fallback is introduced.
- No project-specific asset is approved by this Base change.
- A Figma write request is not placement evidence until destination readback succeeds.

## 8. Verification Contract

TDD and repository-integrity evidence must demonstrate:

1. the existing art Skill links the Figma continuity gate;
2. the continuity gate links all six focused modules;
3. the owning `SKILL.md` directly indexes all six packaged modules for package integrity;
4. existing art Skill Registry triggers remain sufficient and no new broad `figma-*`, `expression-*`, or `sprite-*` Skill ID appears;
5. Figma direct module contains write-available auto-placement and write-unavailable exact-guidance branches;
6. candidates enter `02_WIP` before approval;
7. explicit user approval gates `01_APPROVED_REFERENCE` / `04_FINAL` promotion;
8. Figma promotion remains separate from `PROJECT_ASSET_APPROVED`;
9. local Tool Hub/Studio runtime is recorded as non-canonical for normal image work while source remains preserved/referenceable;
10. owning Skill learning evidence is updated when the Skill contract changes;
11. a recognized existing BCA companion test consumes the Skill contract so canonical reference freshness remains valid;
12. CI preserves any failing visual contract rather than returning only the final unittest exit code.

Do not weaken package-integrity or reference-freshness rules to make the new modules pass.

## 9. TDD / Failure-Discovery Notes

The implementation intentionally treated repository contracts as evidence rather than paperwork:

- the first module RED exposed missing module files;
- the BCA log exposed a pre-existing failure-aggregation bug, which was fixed so earlier failing tests cannot be hidden by later successes;
- GPO then exposed the package-integrity requirement that every new reference be directly linked from `SKILL.md`;
- a focused RED was added for that direct-link requirement;
- reference freshness then required a recognized existing companion test when `SKILL.md` changed, so `tests/test_bca_visual_sheet_workflow.py` was meaningfully extended instead of weakening freshness config.

These findings are part of the final architecture.

## 10. Real-World Evidence Ceiling

This Base change can prove routing/documentation/integrity contracts. It does not by itself prove every project's Figma file is correctly structured or that every future upload succeeds.

When a future image task occurs, the preferred behavior is:

```text
Figma readback available
→ read approved canon
→ generate/edit
→ Figma write available? auto-place : provide exact placement instructions
→ user approval
→ approved visual promotion if requested/appropriate
```

Actual Figma mutation must be read back before claiming placement success.