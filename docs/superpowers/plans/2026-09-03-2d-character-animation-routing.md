# 2D Character Animation Routing Implementation Plan

> **Execution note:** Implement on a fresh branch from Base `850204b3e5de81a4045111b4a050c46c5a292b59`. Keep every pre-existing PR read-only. No project repository or runtime asset is changed.

**Goal:** Add a reusable, non-vendor-default route for 2D character animation and rigging under existing Base owners.

**Architecture:** One subordinate evaluation reference, one project record Template, conditional links from the active source catalog and sprite pose reference, one learning receipt, and focused contract tests. No new Skill or Registry entry.

**Tech stack:** Markdown contracts, Python `unittest`, GitHub PR/Actions.

---

### Task 1: Establish RED contract

**Files:**
- Create: `tests/test_2d_character_animation_routing_contract.py`

1. Assert four routes, consumer measurements, rig-ready source fields, state/interruption contract, domain authority, external runtime trial, Spine bounded facts, Template fields, active-owner links, learning receipt, and evidence-state separation.
2. Run `python -m unittest tests.test_2d_character_animation_routing_contract -v` against the current contract snapshot.
3. Record the expected missing-owner/Template/link failures as RED.

### Task 2: Add route owner and project record

**Files:**
- Create: `skills/evaluating-godot-assets-and-plugins-before-creation/references/2d-character-animation-routing-and-rigging.md`
- Create: `templates/planning/2D_CHARACTER_ANIMATION_ROUTE_RECORD.md`

1. Define `FRAME`, `GODOT_NATIVE_RIG`, `EXTERNAL_RIG_RUNTIME`, and `EXTERNAL_RIG_BAKED` using the same consumer/value/cost/performance/license/rollback axes.
2. Add rig-ready source, state-family, interruption, domain-authority, trial, evidence-ceiling, and rollback contracts.
3. Record current official Spine/Godot findings as a dated candidate snapshot, not a permanent compatibility or price claim.

### Task 3: Connect existing active owners

**Files:**
- Modify: `skills/evaluating-godot-assets-and-plugins-before-creation/references/source-catalog.md`
- Modify: `skills/designing-art-prompts-and-technique-cards/references/sprite-pose-sequence-controls.md`

1. Add 2D rig/runtime search queries and a conditional pointer from the evaluation source catalog.
2. Add a conditional rig-ready-source preflight from sprite pose/sequence planning.
3. Preserve existing content and do not modify retired Sprite Animation Studio or conflicting UI/Registry PR paths.

### Task 4: Record reusable learning

**Files:**
- Modify: `skills/evaluating-godot-assets-and-plugins-before-creation/LEARNING_LOG.md`

1. Record the missing route decision, selected existing-owner architecture, no-purchase/no-rollout boundary, and evidence ceiling.
2. State that the retired Sprite Animation Studio remains retired.

### Task 5: Verify and integrate safely

**Files:**
- Test: `tests/test_2d_character_animation_routing_contract.py`

1. Run focused GREEN.
2. Run negative mutations for route/default, domain-authority, active-owner routing, and external-runtime evidence boundaries; each must fail and the restored candidate must pass.
3. Perform five full-scope reviews: authority/concurrency, alternatives/YAGNI, current-source/license/version, runtime/domain/accessibility, discoverability/test/rollback.
4. Create a current-task PR, read back exact changed files and head, run remote required checks, inspect ruleset/review/thread state, and merge only if every required gate can be satisfied without bypass.
5. After a permitted merge, read back new `main`; otherwise report the exact remaining merge blocker without claiming integration.
