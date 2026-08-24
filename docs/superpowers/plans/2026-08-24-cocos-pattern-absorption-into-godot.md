# Cocos Pattern Absorption into Godot Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Preserve Godot as the sole production/runtime engine while absorbing reusable Cocos production patterns into existing Base owners without adding a second engine, new broad Skill, paid dependency, or unsupported runtime claim.

**Architecture:** Implement this as a knowledge/governance refinement, not a new runtime subsystem. A focused regression test locks the engine-authority and evidence boundaries; a dated pattern note captures source-to-Godot translations; existing build-size, technical-release, platform-adapter, and periodic-source owners receive only the smallest necessary routing additions.

**Tech Stack:** Markdown, Python `unittest`, GitHub Actions/CI, existing Godot/Base documentation contracts.

**Spec:** `docs/superpowers/specs/2026-08-24-cocos-pattern-absorption-into-godot-design.md`

## Global Constraints

- `GODOT_ONLY_RUNTIME · ABSORB_COCOS_PATTERNS_ONLY`.
- No Cocos runtime, Cocos Creator project template, TypeScript requirement, Cocos CLI dependency, Cocos Store default, second engine-selection layer, new paid dependency, new scheduler, or active-project migration.
- Cocos evidence proves Cocos behavior only; any Godot implementation claim requires Godot official evidence or actual Base/project runtime evidence.
- Reuse existing owners first. Do not allocate new `RM-*` IDs unless a distinct interface survives overlap analysis and promotion evidence.
- PCK/deferred-content, Web readiness, and partial-rebuild effectiveness remain `TEST`/`NOT_RUN` until actual Godot project evidence exists.
- Existing open/draft/ready PRs and unrelated branches remain read-only.

---

### Task 1: Lock the Godot-only/Cocos-benchmark contract with a failing regression

**Files:**
- Create: `tests/test_cocos_pattern_absorption_into_godot.py`
- Read: `docs/superpowers/specs/2026-08-24-cocos-pattern-absorption-into-godot-design.md`
- Read: `docs/operations/base-partitions/P06_GODOT_RUNTIME_TOOLCHAIN.md`

**Interfaces:**
- Consumes: current Base documentation tree.
- Produces: a static regression contract requiring the pattern note, owner routing, source routing, and forbidden second-engine markers.

- [ ] **Step 1: Write the failing test**

Create `tests/test_cocos_pattern_absorption_into_godot.py` with `unittest` assertions that require:

```python
from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTE = ROOT / "docs" / "knowledge" / "game-development" / "reuse" / "COCOS_PATTERN_ABSORPTION_2026-08-24.md"
BUILD = ROOT / "docs" / "knowledge" / "game-development" / "GAME_BUILD_SIZE_AND_ASSET_OPTIMIZATION_GUIDE.md"
TECH = ROOT / "docs" / "knowledge" / "game-development" / "TECHNICAL_PRODUCTION_AND_RELEASE_GUIDE.md"
PLATFORM = ROOT / "docs" / "knowledge" / "game-development" / "PC_ANDROID_CROSS_PLATFORM_DELIVERY_GUIDE.md"
WATCH = ROOT / "docs" / "knowledge" / "game-development" / "PERIODIC_EXTERNAL_SOURCE_WATCHLIST.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class CocosPatternAbsorptionIntoGodotTests(unittest.TestCase):
    def test_pattern_note_keeps_godot_as_only_runtime(self) -> None:
        note = read(NOTE)
        for term in (
            "GODOT_ONLY_RUNTIME",
            "ABSORB_COCOS_PATTERNS_ONLY",
            "NO_COCOS_RUNTIME",
            "NO_TYPESCRIPT_REQUIREMENT",
            "NO_SECOND_ENGINE_SELECTION_GATE",
            "Cocos evidence != Godot runtime evidence",
        ):
            self.assertIn(term, note)

    def test_patterns_route_to_existing_owners(self) -> None:
        self.assertIn("FIRST_LOAD_BUDGET_AND_DEFERRED_CONTENT", read(BUILD))
        self.assertIn("REPRODUCIBLE_BUILD_PROFILE", read(TECH))
        self.assertIn("PLATFORM_ADAPTER_STAYS_OUTSIDE_GAME_RULES", read(PLATFORM))

    def test_unverified_godot_capabilities_remain_test_only(self) -> None:
        note = read(NOTE)
        for term in (
            "PCK_DEFERRED_CONTENT: TEST",
            "PARTIAL_REBUILD: TEST",
            "GODOT_WEB_RELEASE_READY: NOT_RUN",
            "API_EXISTS_IS_NOT_PROJECT_READY",
        ):
            self.assertIn(term, note)

    def test_cocos_uses_existing_periodic_source_pipeline(self) -> None:
        watch = read(WATCH)
        for term in (
            "Cocos Creator official docs / releases",
            "Cocos behavior",
            "Godot runtime authority",
        ):
            self.assertIn(term, watch)
        self.assertNotIn("COCOS_SPECIFIC_SCHEDULER", watch)

    def test_no_cocos_runtime_dependency_or_new_broad_skill(self) -> None:
        registry = read(ROOT / "skills" / "SKILL_REGISTRY.json")
        for forbidden in (
            '"skill_id":"cocos-game-development"',
            '"skill_id":"dual-engine-game-development"',
            '"skill_id":"cocos-godot-bridge"',
        ):
            self.assertNotIn(forbidden, registry)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the focused test and verify RED**

Run:

```bash
python -m unittest tests.test_cocos_pattern_absorption_into_godot -v
```

Expected: FAIL because `COCOS_PATTERN_ABSORPTION_2026-08-24.md` and/or the new owner markers do not exist yet. A syntax/import failure is not an acceptable RED.

- [ ] **Step 3: Commit the RED test**

```bash
git add tests/test_cocos_pattern_absorption_into_godot.py
git commit -m "test: lock Cocos pattern absorption boundary"
```

### Task 2: Add the bounded Cocos-to-Godot evidence/translation note

**Files:**
- Create: `docs/knowledge/game-development/reuse/COCOS_PATTERN_ABSORPTION_2026-08-24.md`
- Test: `tests/test_cocos_pattern_absorption_into_godot.py`

**Interfaces:**
- Consumes: approved design, official Cocos/Godot source URLs, existing Base owner paths.
- Produces: one dated evidence packet that distinguishes source behavior, transferable contract, Godot translation candidate, disposition, and evidence ceiling.

- [ ] **Step 1: Write the minimum pattern note needed by the RED test**

The note must declare:

```text
GODOT_ONLY_RUNTIME
ABSORB_COCOS_PATTERNS_ONLY
NO_COCOS_RUNTIME
NO_TYPESCRIPT_REQUIREMENT
NO_SECOND_ENGINE_SELECTION_GATE
Cocos evidence != Godot runtime evidence
PCK_DEFERRED_CONTENT: TEST
PARTIAL_REBUILD: TEST
GODOT_WEB_RELEASE_READY: NOT_RUN
API_EXISTS_IS_NOT_PROJECT_READY
```

It must include the five accepted/adapted contracts from the design, their existing Base owner, official Cocos source URL, official Godot translation source URL where applicable, and `ADOPT | ADAPT | TEST | REJECT` disposition.

- [ ] **Step 2: Run the focused test**

Run the same `unittest` command. Expected: remaining failures should now be only owner/watchlist routing markers, proving the note portion is GREEN while later tasks remain RED.

- [ ] **Step 3: Commit the evidence note**

```bash
git add docs/knowledge/game-development/reuse/COCOS_PATTERN_ABSORPTION_2026-08-24.md
git commit -m "docs: capture Cocos patterns for Godot translation"
```

### Task 3: Route the patterns into existing Base owners without creating duplicate modules

**Files:**
- Modify: `docs/knowledge/game-development/GAME_BUILD_SIZE_AND_ASSET_OPTIMIZATION_GUIDE.md`
- Modify: `docs/knowledge/game-development/TECHNICAL_PRODUCTION_AND_RELEASE_GUIDE.md`
- Modify: `docs/knowledge/game-development/PC_ANDROID_CROSS_PLATFORM_DELIVERY_GUIDE.md`
- Modify: `docs/knowledge/game-development/PERIODIC_EXTERNAL_SOURCE_WATCHLIST.md`
- Test: `tests/test_cocos_pattern_absorption_into_godot.py`

**Interfaces:**
- Consumes: Task 2 pattern note.
- Produces: canonical owner markers discoverable by current workflows while retaining each existing owner’s responsibility.

- [ ] **Step 1: Add `FIRST_LOAD_BUDGET_AND_DEFERRED_CONTENT` to the build-size owner**

Add a bounded section that separates mandatory first-session content from optional/later content and requires explicit load trigger, loading/error/retry UX, cache/memory lifecycle, package/startup measurements, and rollback. State that Godot PCK/ZIP/resource-pack use is a `TEST` candidate until project runtime evidence exists.

- [ ] **Step 2: Add `REPRODUCIBLE_BUILD_PROFILE` to the technical-release owner**

Require a named/versioned Godot export profile, deterministic CLI invocation, explicit output path, exit-code/log capture, artifact identity, and smoke/runtime verification. Explicitly state that successful CLI completion is not release PASS.

- [ ] **Step 3: Strengthen the platform owner with `PLATFORM_ADAPTER_STAYS_OUTSIDE_GAME_RULES`**

Bind platform/browser/store/lifecycle APIs to the existing adapter boundary and state that platform SDKs do not become authoritative game state.

- [ ] **Step 4: Add Cocos to the existing source watchlist with an authority ceiling**

Add `Cocos Creator official docs / releases` as an engine-behavior authority source for Cocos only. Record that it may yield `REFERENCE_ONLY`, `ADAPT_TO_EXISTING_OWNER`, or `TEST_IN_GODOT`, but never becomes `Godot runtime authority` and never creates a Cocos-specific scheduler.

- [ ] **Step 5: Run focused regressions**

```bash
python -m unittest \
  tests.test_cocos_pattern_absorption_into_godot \
  tests.test_game_build_size_asset_optimization \
  tests.test_pc_android_cross_platform_delivery -v
```

Expected: PASS.

- [ ] **Step 6: Commit owner routing**

```bash
git add \
  docs/knowledge/game-development/GAME_BUILD_SIZE_AND_ASSET_OPTIMIZATION_GUIDE.md \
  docs/knowledge/game-development/TECHNICAL_PRODUCTION_AND_RELEASE_GUIDE.md \
  docs/knowledge/game-development/PC_ANDROID_CROSS_PLATFORM_DELIVERY_GUIDE.md \
  docs/knowledge/game-development/PERIODIC_EXTERNAL_SOURCE_WATCHLIST.md
git commit -m "docs: absorb Cocos production patterns into Godot owners"
```

### Task 4: Validate overlap, evidence ceilings, and final branch readiness

**Files:**
- Read: `docs/knowledge/game-development/reuse/REUSABLE_MODULE_REGISTRY.md`
- Optionally modify: `docs/operations/base-partitions/learning/P06_LEARNING_LOG.md` only if a reusable lesson survives review.
- Test: repository-required validation suites.

**Interfaces:**
- Consumes: Tasks 1-3.
- Produces: evidence that no duplicate module/Skill/engine authority was introduced and that completion claims remain within IRG limits.

- [ ] **Step 1: Existing Solution First / module overlap review**

Confirm the new contracts remain existing-owner reuse. Do not add a new `RM-*` ID unless the registry cannot express the reusable boundary and promotion evidence already meets the design threshold.

- [ ] **Step 2: Run at least five full adversarial review loops**

Each loop rechecks the entire change against:

```text
second-engine creep
renaming duplication
false portability
API-exists-equals-ready
premature abstraction
package-limit staleness
cost/toolchain expansion
project migration drift
```

Any valid finding resets the loop count after correction.

- [ ] **Step 3: Run focused tests and repository-required CI**

At minimum rerun the focused `unittest` set from Task 3. Then use the repository’s PR validation/`ci-gate` and required checks as the authoritative hosted verification.

- [ ] **Step 4: Verify Implementation Reality Gate claim ceiling**

Allowed completion claims:

```text
Cocos pattern research documented
translation contracts installed in existing owners
Godot remains sole runtime authority
static regressions/required CI pass
```

Forbidden without later project pilots:

```text
Godot deferred-content production ready
Godot Web release ready
partial rebuild speedup proven
browser/mobile performance proven
project adoption complete
```

- [ ] **Step 5: Commit any final correction/learning note**

Only if the adversarial review produced a necessary owner correction or reusable P06 learning record.

- [ ] **Step 6: Prepare PR for exact-HEAD review**

Review changed files, required checks, unresolved threads, and latest-main drift before any merge decision. Do not mutate unrelated open PRs.
