# 2D Character Animation Routing Implementation Plan

> **Execution note:** Implement on a fresh branch from Base `850204b3e5de81a4045111b4a050c46c5a292b59`. Keep every pre-existing PR read-only. No project repository or runtime asset is changed.

**Goal:** Add a reusable, non-vendor-default route for 2D character animation and rigging under existing Base owners.

**Architecture:** Add one subordinate evaluation reference and one project record Template; link them from the owning Skill, its existing shared-skill routing record, the source catalog, and the sprite pose reference. Protect the route with focused section-level and shared-route tests. Do not create a new Skill, a new `shared_skills[]` record, a new project-adapter role, or a runtime dependency.

**Tech stack:** Markdown contracts, JSON shared routing, Python `unittest`, GitHub PR/Actions.

---

### Task 1: Establish RED contract

**Files:**
- Create: `tests/test_2d_character_animation_routing_contract.py`

1. Assert four routes, consumer measurements, rig-ready source fields, state/interruption contract, domain authority, external runtime trial, Spine bounded facts, Template fields, active-owner links, learning receipt, and evidence-state separation.
2. Run `python -m unittest tests.test_2d_character_animation_routing_contract -v` against the current contract snapshot.
3. Record the expected missing-owner/Template/link failures as RED.
4. Strengthen the assertions to require markers in their owning Markdown sections, then verify wrong-section relocation mutations fail.

### Task 2: Add route owner and project record

**Files:**
- Create: `skills/evaluating-godot-assets-and-plugins-before-creation/references/2d-character-animation-routing-and-rigging.md`
- Create: `templates/planning/2D_CHARACTER_ANIMATION_ROUTE_RECORD.md`

1. Define `FRAME`, `GODOT_NATIVE_RIG`, `EXTERNAL_RIG_RUNTIME`, and `EXTERNAL_RIG_BAKED` using the same consumer/value/cost/performance/license/rollback axes.
2. Add rig-ready source, state-family, interruption, domain-authority, trial, evidence-ceiling, and rollback contracts.
3. Record current official Spine/Godot findings as a dated candidate snapshot, not a permanent compatibility or price claim.

### Task 3: Connect existing active owners

**Files:**
- Modify: `skills/evaluating-godot-assets-and-plugins-before-creation/SKILL.md`
- Modify: `skills/evaluating-godot-assets-and-plugins-before-creation/references/source-catalog.md`
- Modify: `skills/designing-art-prompts-and-technique-cards/references/sprite-pose-sequence-controls.md`

1. Link the subordinate reference from its owning Skill as a conditional reference.
2. Add 2D rig/runtime search queries and a pointer from the evaluation source catalog.
3. Add a conditional rig-ready-source preflight from sprite pose/sequence planning.
4. Preserve existing content and do not modify retired Sprite Animation Studio or unrelated open-PR paths.

### Task 4: Propagate through the current shared routing authority

**Files:**
- Modify: `skills/BASE_SHARED_SKILL_ROUTES.json`
- Modify: `tests/test_base_shared_skill_routes.py`

1. Extend only the existing `evaluating-godot-assets-and-plugins-before-creation` record with focused 2D animation triggers, the new reference, the Template, and a bounded `use_when` clause.
2. Do not add another `shared_skills[]` object or project-adapter role.
3. Add a shared-route regression that verifies the tags, reference, Template, file existence, and route wording while preserving the existing shared Skill set.
4. Run canonical reference freshness and package integrity checks through the repository CI.

### Task 5: Record reusable learning

**Files:**
- Modify: `skills/evaluating-godot-assets-and-plugins-before-creation/LEARNING_LOG.md`

1. Record the missing route decision, selected existing-owner architecture, no-purchase/no-rollout boundary, and evidence ceiling.
2. State that the retired Sprite Animation Studio remains retired.
3. Record that document contracts and official Runtime CI are not project Godot runtime proof.

### Task 6: Verify and integrate safely

**Files:**
- Test: `tests/test_2d_character_animation_routing_contract.py`
- Test: `tests/test_base_shared_skill_routes.py`
- Verify: all 11 changed files through the repository's required workflows.

1. Run focused GREEN for the route contract and shared route registration.
2. Run negative mutations for route/default, domain-authority, active-owner routing, and evidence-ceiling ownership; each must fail and the restored candidate must pass.
3. Validate Python syntax, JSON parsing, Markdown whitespace/fences, relative links, canonical reference freshness, package integrity, whole core regression, and publication generation.
4. Perform five full-scope reviews: authority/concurrency, alternatives/YAGNI, current-source/license/version, runtime/domain/accessibility, and discoverability/test/rollback.
5. Create a current-task PR, read back exact changed files and head, run remote required checks, and correct every validated failure at its root cause rather than bypassing it.
6. Request an independent exact-head review and inspect submitted reviews, inline threads, rulesets, mergeability, and latest-main drift.
7. Merge by squash only if every applicable gate is satisfied without bypass.
8. After a permitted merge, read back the new `main` and changed owners; otherwise report the exact remaining merge blocker without claiming integration.
