# 2D Character Animation Routing and Rigging Design

**Date:** 2026-09-03
**Repository:** `alsdmlals4-eng/Base`
**Approved direction:** current conversation, user instruction `권장안대로 진행해` after the Spine research and recommendation.
**Baseline:** `850204b3e5de81a4045111b4a050c46c5a292b59`

## Problem

Base has active frame/pose/atlas planning and general Godot addon evaluation, but it does not provide one bounded decision contract for choosing frame animation, Godot-native 2D rigging, an external skeletal runtime, or rig-authoring followed by baked frames. This gap can cause art to be generated as a flat image before the runtime route is known, or can make a well-known commercial tool look like a default dependency without consumer, performance, license, version, or rollback proof.

The former Sprite Animation Studio is `RETIRED_HISTORY_ONLY` in current Base. It must not be revived as the owner.

## Goals

- Route each actual 2D character consumer through materially distinct alternatives.
- Keep `FRAME` as the default unless evidence shows another route reduces total lifecycle cost while protecting player value.
- Define rig-ready source-art, state-family, interruption, domain-authority, version, license, performance, and rollback contracts.
- Treat Spine as one bounded external candidate, not a default dependency.
- Add a reusable project record and focused regression tests under existing owners.
- Make the route discoverable through the existing shared-skill routing record without creating another Skill authority.

## Non-goals

- No Spine purchase, installer, binary, addon, custom Godot build, project rollout, production asset, or project runtime change.
- No new Skill, no new `shared_skills[]` object, no new project-adapter role, and no second asset canon.
- No new workflow, provider, dashboard, or project-wide mandatory rigging dependency.
- No modification of retired Sprite Animation Studio files.
- No claim of Godot import, Windows/Android runtime, performance, Human, or release verification.

## Selected architecture

The existing `evaluating-godot-assets-and-plugins-before-creation` Skill remains the primary owner. A new subordinate reference owns the route decision and runtime trial boundary. The owning `SKILL.md` links the conditional reference directly. Its existing entry in `skills/BASE_SHARED_SKILL_ROUTES.json` is extended with focused trigger tags, the new reference, and the project record Template; no new shared Skill record is created. The existing `source-catalog.md` supplies discovery queries, while the active art Skill's `sprite-pose-sequence-controls.md` links into the same reference only when source art may need rig-ready parts.

```text
skills/evaluating-godot-assets-and-plugins-before-creation/
├─ SKILL.md
├─ LEARNING_LOG.md
└─ references/
   ├─ source-catalog.md
   └─ 2d-character-animation-routing-and-rigging.md

skills/BASE_SHARED_SKILL_ROUTES.json
└─ extend existing evaluating-godot-assets-and-plugins-before-creation record

templates/planning/2D_CHARACTER_ANIMATION_ROUTE_RECORD.md

designing-art-prompts-and-technique-cards/
└─ references/sprite-pose-sequence-controls.md
   └─ conditional route to the same animation reference

tests/
├─ test_2d_character_animation_routing_contract.py
└─ test_base_shared_skill_routes.py
```

## Alternatives considered

1. **Revive Sprite Animation Studio.** Rejected because current Base explicitly retires it and its frame-generation tool does not own runtime-route selection.
2. **Create a new animation Skill and a new shared-skill record.** Rejected because the input, evaluation, adoption, and rollback boundaries already belong to the Godot asset/plugin evaluation Skill.
3. **Add one subordinate reference and extend the existing Skill route record.** Selected as the smallest discoverable, non-duplicating architecture.
4. **Adopt Spine as the Base default.** Rejected because projects differ in style, concurrent instances, platforms, cost, and dynamic-runtime need.

## Data and control flow

```text
actual consumer + current project implementation
→ existing shared-skill trigger routes to current evaluation owner
→ FRAME / GODOT_NATIVE_RIG / EXTERNAL_RIG_RUNTIME / EXTERNAL_RIG_BAKED comparison
→ selected route + rejected-route reasons
→ rig-ready source contract when applicable
→ state family + interruption + domain boundary
→ isolated trial when external runtime is selected
→ exact version/license/platform/performance/removal evidence
→ project-specific adoption decision
```

Animation remains a presentation consumer. Domain state commits damage, cost, reward, save, and progress exactly once before or independently of visual playback.

## Error and rollback handling

Missing sources, binaries, license evidence, target-platform exports, or performance evidence fail closed as `NOT_RUN` or `BLOCKED_UNVERIFIED`. External runtime removal must preserve a frame/static fallback and leave domain state, save schema, approved source art, and unrelated project paths unchanged. Removing this Base addition consists of reverting the existing route-record additions, the subordinate reference, Template, owner links, learning receipt, and their focused tests; no project runtime migration is implied.

## Verification

- Focused unittest begins RED on the current Base contract.
- GREEN requires the new route owner, Template, owner links, learning receipt, section ownership, and evidence-ceiling markers.
- Shared-route regression requires the existing Skill record to expose focused trigger tags, the reference, and the Template while retaining exactly the existing shared Skill set.
- Negative mutations relocate route/default/domain/runtime-boundary markers and must fail.
- Canonical reference freshness, Base package integrity, whitespace, shared-route tests, whole core regression, and publication checks run on the exact PR head.
- Remote Base CI, independent review, unresolved-thread readback, ruleset reconciliation, and exact-head merge are required before integration.
- These tests are document-contract evidence only, not Godot runtime evidence.
