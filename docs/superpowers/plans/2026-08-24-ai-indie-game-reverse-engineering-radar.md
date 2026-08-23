# AI Indie Game Reverse-Engineering Radar Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a bounded, weekly AI-assisted solo/indie game reverse-engineering capture path that feeds the existing Base source-discovery and reuse owners without creating a new Skill, scheduler, or runtime AI framework.

**Architecture:** Add one specialty Radar subordinate to the existing periodic Watchlist and one dated Pattern Pack/evidence document subordinate to the existing reverse-engineering reuse pipeline. Guard their ownership, evidence ceilings, case taxonomy, reusable production/gameplay contracts, and project-fit routing with a focused regression test. Do not mutate project canon or runtime code.

**Tech Stack:** Markdown contracts, Python `unittest`, existing Base source/reuse owners, GitHub PR/CI.

**Spec:** `docs/superpowers/specs/2026-08-24-ai-indie-game-reverse-engineering-radar-design.md`

## Global Constraints

- Keep `PERIODIC_EXTERNAL_SOURCE_WATCHLIST.md` as source-policy owner.
- Keep scheduling `EXTERNAL_TO_BASE`; Base does not become a scheduler.
- Keep `REVERSE_ENGINEERING_REUSE_PIPELINE.md` as reuse-discovery owner.
- Keep `AI_ASSISTED_GAME_DEVELOPMENT_GUIDE.md` as AI-production authority.
- Keep `REUSABLE_MODULE_REGISTRY.md` as promotion registry; this change only records candidates/hypotheses.
- Add no new Skill, Agent, paid service, runtime AI dependency, or project gameplay implementation.
- Do not mutate Notion while the independent Notion IA draft PR is active.
- Distinguish `PRODUCTION_ASSISTED` from `RUNTIME_GENERATIVE` and upcoming/demo/released evidence.
- Popularity is a signal, not causal proof or authority.
- Follow Red → Green → Refactor: focused regression must fail before the Radar/Pattern Pack files are created.

---

### Task 1: Add the failing ownership and capture regression

**Files:**
- Create: `tests/test_ai_indie_game_reverse_engineering_radar.py`

**Interfaces:**
- Consumes: design spec and existing Base file layout.
- Produces: required path/keyword contract for the new specialty Radar and Pattern Pack.

- [ ] **Step 1: Write the failing test**

```python
from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RADAR = ROOT / "docs" / "knowledge" / "game-development" / "AI_GAME_AND_AI_ASSISTED_INDIE_RADAR.md"
PACK = ROOT / "docs" / "knowledge" / "game-development" / "reuse" / "AI_ASSISTED_INDIE_PATTERN_PACK_2026-08-24.md"


class AiIndieGameReverseEngineeringRadarTests(unittest.TestCase):
    def test_specialty_radar_preserves_existing_authority_and_weekly_capture(self) -> None:
        self.assertTrue(RADAR.is_file())
        text = RADAR.read_text(encoding="utf-8")
        for required in (
            "PERIODIC_EXTERNAL_SOURCE_WATCHLIST.md",
            "REVERSE_ENGINEERING_REUSE_PIPELINE.md",
            "scheduler_authority: EXTERNAL_TO_BASE",
            "recommended_cadence: weekly",
            "PRODUCTION_ASSISTED",
            "RUNTIME_GENERATIVE",
            "popularity_is_not_authority: true",
            "compare_with_previous_scan: true",
            "ADOPT | ADAPT | TEST | REJECT | REFERENCE_ONLY",
        ):
            with self.subTest(required=required):
                self.assertIn(required, text)

    def test_pattern_pack_captures_success_failure_and_reuse_boundaries(self) -> None:
        self.assertTrue(PACK.is_file())
        text = PACK.read_text(encoding="utf-8")
        for required in (
            "Slotbound",
            "Ashen Crown",
            "Express 404",
            "Infinite Arcana",
            "Vapor World: Over the Mind",
            "HUMAN_DIRECTED_AI_BUILD_LOOP",
            "SILENT_OMISSION_GATE",
            "CONTEXT_SCOPE_AND_ARCHITECTURE_BUDGET",
            "BREADTH_AFTER_CORE_IDENTITY_LOCK",
            "PLAYER_FEEDBACK_REBUILD_LOOP",
            "AI_VISIBLE_OUTPUT_QUALITY_GATE",
            "RNG_AGENCY_AND_RECOVERY",
            "Implementation Reality Gate",
            "Adversarial review 5/5",
            "PROJECT_ADOPTION_NOT_RUN",
        ):
            with self.subTest(required=required):
                self.assertIn(required, text)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the focused test and verify RED**

Run:

```bash
python -m unittest tests.test_ai_indie_game_reverse_engineering_radar -v
```

Expected: FAIL because `AI_GAME_AND_AI_ASSISTED_INDIE_RADAR.md` and `AI_ASSISTED_INDIE_PATTERN_PACK_2026-08-24.md` do not exist yet.

- [ ] **Step 3: Commit the RED test only**

```bash
git add tests/test_ai_indie_game_reverse_engineering_radar.py
git commit -m "test: expose missing AI indie reverse-engineering radar"
```

---

### Task 2: Add the specialty weekly Radar

**Files:**
- Create: `docs/knowledge/game-development/AI_GAME_AND_AI_ASSISTED_INDIE_RADAR.md`
- Test: `tests/test_ai_indie_game_reverse_engineering_radar.py`

**Interfaces:**
- Consumes: `PERIODIC_EXTERNAL_SOURCE_WATCHLIST.md`, `PERIODIC_EXTERNAL_SOURCE_DISCOVERY_SEEDS.md`, `PERIODIC_SPECIALTY_SOURCE_RADAR.md`, `REVERSE_ENGINEERING_REUSE_PIPELINE.md`.
- Produces: weekly AI-game case packet and routing contract.

- [ ] **Step 1: Write the minimal Radar**

The document must declare:

```yaml
radar_role: ai-game-and-ai-assisted-indie-specialty-discovery
status: ACTIVE_DISCOVERY_EXTENSION
owner_policy: docs/knowledge/game-development/PERIODIC_EXTERNAL_SOURCE_WATCHLIST.md
reuse_owner: docs/knowledge/research/REVERSE_ENGINEERING_REUSE_PIPELINE.md
scheduler_authority: EXTERNAL_TO_BASE
recommended_cadence: weekly
compare_with_previous_scan: true
popularity_is_not_authority: true
new_active_skill: false
new_runtime_framework: false
```

It must define AI-use lanes, source ladder, weekly packet, release-state separation, success/failure sampling, reusable-candidate routing, and no-auto-project-adoption boundary.

- [ ] **Step 2: Run focused test**

Run:

```bash
python -m unittest tests.test_ai_indie_game_reverse_engineering_radar -v
```

Expected: first test PASS; second test still FAIL because the Pattern Pack is absent.

- [ ] **Step 3: Commit**

```bash
git add docs/knowledge/game-development/AI_GAME_AND_AI_ASSISTED_INDIE_RADAR.md
git commit -m "docs: add weekly AI game reverse-engineering radar"
```

---

### Task 3: Add the first evidence-derived Pattern Pack

**Files:**
- Create: `docs/knowledge/game-development/reuse/AI_ASSISTED_INDIE_PATTERN_PACK_2026-08-24.md`
- Test: `tests/test_ai_indie_game_reverse_engineering_radar.py`

**Interfaces:**
- Consumes: current public evidence for Slotbound, Ashen Crown, Express 404, Infinite Arcana, Vapor World; current reusable module registry and AI development guide.
- Produces: evidence-bounded production/gameplay candidate contracts and 10-project fit hypotheses.

- [ ] **Step 1: Add evidence table with source ceilings**

For each case record release state, verified development context, AI-use lane, observed loop/workflow, popularity signal only when sourced, failures/counterevidence, and disposition.

- [ ] **Step 2: Add candidate contracts**

Document:

```text
HUMAN_DIRECTED_AI_BUILD_LOOP
SILENT_OMISSION_GATE
CONTEXT_SCOPE_AND_ARCHITECTURE_BUDGET
BREADTH_AFTER_CORE_IDENTITY_LOCK
PLAYER_FEEDBACK_REBUILD_LOOP
AI_VISIBLE_OUTPUT_QUALITY_GATE
RNG_AGENCY_AND_RECOVERY
```

Each candidate must name existing Base owner overlap and must not claim module implementation or project adoption.

- [ ] **Step 3: Add project-fit map and IRG**

Route hypotheses to OMENWARD, NINJA_SURVIVAL, BLACKSMITH, GRIMOIRE, URBAN_LEGEND, MY_LITTLE_BOAT, TETRIS, SWITCHY, TEN_PACES, COC_FICTION with `ADOPT/ADAPT/TEST/REJECT/REFERENCE_ONLY` and explicit `PROJECT_ADOPTION_NOT_RUN`.

- [ ] **Step 4: Add adversarial review 5/5**

Record five independent passes: duplication, causality, solo-dev reality, player value, maintenance/rights/cost. Resolve any finding before marking 5/5.

- [ ] **Step 5: Run focused test**

Run:

```bash
python -m unittest tests.test_ai_indie_game_reverse_engineering_radar -v
```

Expected: PASS.

- [ ] **Step 6: Run adjacent contract tests**

Run:

```bash
python -m unittest tests.test_periodic_external_source_discovery_seeds tests.test_base_v9_4_ai_operations_contract -v
```

Expected: PASS; no existing source or AI-operations owner is broken.

- [ ] **Step 7: Commit**

```bash
git add docs/knowledge/game-development/reuse/AI_ASSISTED_INDIE_PATTERN_PACK_2026-08-24.md
git commit -m "docs: capture AI-assisted indie reverse-engineering patterns"
```

---

### Task 4: PR verification and scheduler handoff

**Files:**
- No Base production file mutation beyond Tasks 1–3.
- External scheduled task: update only after the Base path exists on merged `main`.

**Interfaces:**
- Consumes: completed branch and GitHub CI.
- Produces: reviewed Base change and a weekly external scan that uses the new Radar after merge.

- [ ] **Step 1: Compare branch against `main`**

Confirm only the spec, plan, test, Radar, and Pattern Pack are changed. Confirm no file from independent active PRs is modified.

- [ ] **Step 2: Review evidence/claims**

Confirm upcoming games are not described as shipped success, popularity signals have dates/source ceilings, and self-reported development claims are not presented as independent audits.

- [ ] **Step 3: Open PR**

PR body must state:

```text
no project runtime mutation
no Notion mutation
no new Skill
no Base scheduler
no paid dependency
project adoption not run
```

- [ ] **Step 4: Verify CI**

Require focused regression and applicable repository checks to pass. If CI reveals unrelated pre-existing failures, record them separately rather than weakening the new test.

- [ ] **Step 5: Merge only when current-head verification is green and the approved scope has not drifted**

Use the repository's required merge method/policy.

- [ ] **Step 6: Update the already-approved external weekly automation**

After merge, make the scheduled task explicitly read the merged Radar contract and compare each run with the prior scan. Base remains `EXTERNAL_TO_BASE` and does not claim scheduler execution.

---

## Self-review

- Spec coverage: weekly discovery, case taxonomy, source ceiling, success/failure evidence, existing-owner routing, project fit, IRG, 5-pass adversarial review, and scheduler boundary are all mapped to Tasks 1–4.
- Placeholder scan: no `TBD`, `TODO`, or unspecified implementation step remains.
- Type/name consistency: Radar and Pattern Pack paths match the regression test and spec.
