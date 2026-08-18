# Figma-Direct Visual Skill Modules Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Preserve successful local visual-tool techniques as conditional Base art-skill modules while making direct project Figma organization the normal image-work path.

**Architecture:** Keep `designing-art-prompts-and-technique-cards` and its existing Registry triggers unchanged. Its existing `figma-visual-bible-continuity-gate.md` becomes the conditional router for six focused modules, avoiding new broad Skills and trigger ambiguity. Figma write capability auto-places WIP when available; otherwise GPT returns exact placement guidance.

**Tech Stack:** Markdown Skill/reference contracts, Python `unittest`, GitHub Actions BCA visual workflow.

**Spec:** `docs/superpowers/specs/2026-08-18-figma-direct-visual-skill-modules-design.md`

## Global Constraints

- Do not create a new broad visual/Figma/Expression/Sprite Skill ID.
- Do not expand the Skill Registry when existing image triggers already route correctly.
- Reuse merged PR #433 `Reusable Visual Harvest Gate` and existing Figma Visual Bible structure.
- New generated visuals enter `02_WIP`/review before explicit user approval.
- Figma write success requires readback before a placement success claim.
- `APPROVED_VISUAL_REFERENCE != PROJECT_ASSET_APPROVED`.
- Local Tool Hub/Expression/Sprite runtime remains source/reference but is non-canonical and non-required for normal image work after the 2026-08-18 stop-loss.
- Do not delete Tool Hub/Studio source code or globally deprecate unrelated QA tools.
- No paid OpenAI API/API-key path.
- Do not touch unrelated open/draft PRs.

---

### Task 1: Add a consumed RED contract and correct BCA failure aggregation

**Files:**
- Create: `tests/test_figma_direct_visual_skill_modules.py`
- Modify: `.github/workflows/validate-bca-visual-sheet-workflow.yml`

**Interfaces:**
- Consumes: existing art Skill, Figma continuity gate, Registry, Visual Bible profile.
- Produces: focused contract proving module presence, Figma placement branches, harvest authority, source retention, and no duplicate Skill owner.

- [x] **Step 1: Add RED tests before module/gate edits**

The tests require six missing reference modules and therefore fail on the baseline.

- [x] **Step 2: Wire the new test into BCA CI**

Add the test path to PR filtering, `py_compile`, and `unittest` execution.

- [x] **Step 3: Observe RED**

Initial BCA log showed the new suite actually failed with missing module files (`1 failure + 2 errors`) while existing visual suites passed.

- [x] **Step 4: Fix the discovered CI evidence bug without touching Skill production**

The prior workflow used `set +e` and returned only the final unittest exit status, masking earlier failures. Change each compile/test command to `... || status=1` and exit the accumulated status. A subsequent run must expose BCA `Run BCA contract tests = failure` while modules remain absent.

### Task 2: Add focused modules and route them from the existing continuity gate

**Files:**
- Create: `skills/designing-art-prompts-and-technique-cards/references/figma-direct-placement-and-canon.md`
- Create: `skills/designing-art-prompts-and-technique-cards/references/character-identity-expression-controls.md`
- Create: `skills/designing-art-prompts-and-technique-cards/references/sprite-pose-sequence-controls.md`
- Create: `skills/designing-art-prompts-and-technique-cards/references/effect-stage-compositing-controls.md`
- Create: `skills/designing-art-prompts-and-technique-cards/references/candidate-review-and-reusable-harvest.md`
- Create: `skills/designing-art-prompts-and-technique-cards/references/local-visual-tool-lessons-and-fallback.md`
- Modify: `skills/designing-art-prompts-and-technique-cards/references/figma-visual-bible-continuity-gate.md`

**Interfaces:**
- Consumes: existing Visual Bible page/approval contract and #433 harvest taxonomy.
- Produces: conditional module router under the existing art Skill.

- [x] **Step 1: Implement Figma direct placement**

Contract:

```text
FIGMA_WRITE_AVAILABLE
→ AUTO_PLACE_WIP in 02_WIP
→ readback
→ explicit user approval
→ appropriate 01_APPROVED_REFERENCE and/or 04_FINAL organization

FIGMA_WRITE_UNAVAILABLE
→ EXACT_PLACEMENT_GUIDANCE
→ project file/page/section/name/status/reference IDs/next gate
```

- [x] **Step 2: Implement character identity/expression controls**

Preserve identity axes; separate facial movement, gaze, head pose; keep FACS optional.

- [x] **Step 3: Implement sprite/pose sequence controls**

Preserve identity, pose intent, silhouette, props/contact, frame order, atlas assumptions; do not invent runtime proof.

- [x] **Step 4: Implement effect-stage/compositing controls**

Define stage order, alpha/background, anchor/scale, and reference-vs-runtime boundary.

- [x] **Step 5: Implement candidate review/reusable harvest**

Reuse #433 classifications; no second taxonomy.

- [x] **Step 6: Implement local-tool fallback**

Record `REFERENCE_ONLY_FOR_VISUAL_WORKFLOW`, preserve source directories, remove Tool Hub/PowerShell/localhost delivery from the normal image-work dependency chain, and leave unrelated QA tooling intact.

- [x] **Step 7: Route modules from the existing Figma continuity gate**

Add a condition-to-reference table and `FIGMA_DIRECT_VISUAL_ORGANIZATION` marker. Do not modify the main Skill or Registry.

- [x] **Step 8: Verify focused GREEN**

BCA run on implementation head must pass the new suite, all existing BCA visual suites, and reference freshness with the corrected failure aggregator.

### Task 3: Final exact-head validation, adversarial review, merge, and postmerge readback

**Files:** no new production files expected after any review fixes.

**Interfaces:**
- Consumes: final exact PR head.
- Produces: merged reusable visual module package.

- [ ] **Step 1: Verify exact-head workflows**

Require:
- BCA Visual and Sheet Workflow: PASS;
- Base v9 `base-v9-contract` and `adversarial-gate`: PASS;
- Game Project Operating System applicable jobs and final `ci-gate`: PASS;
- Integrated Vertical Slice Prompt when triggered: PASS;
- Dependency Review when triggered: PASS.

- [ ] **Step 2: Adversarial review**

Check:
1. no new broad Skill ID or Registry trigger expansion;
2. normal image work does not depend on Tool Hub/PowerShell/localhost delivery;
3. unrelated QA tooling is not deprecated;
4. WIP never auto-promotes;
5. Figma visual approval never collapses into product asset approval;
6. modules do not duplicate #433 taxonomy;
7. Figma write success requires actual readback;
8. existing continuity gate authority and access-fail-closed behavior were preserved;
9. BCA CI cannot mask an earlier failing contract.

- [ ] **Step 3: Update PR evidence, mark ready, and squash merge with exact-head protection**

- [ ] **Step 4: Postmerge readback**

Verify merged `main` contains the six modules, continuity-gate routing, corrected BCA failure aggregation, and unchanged existing art Skill/Registry ownership.

Future image work then follows:

```text
read project Figma canon
→ generate/edit
→ write available? auto-place in WIP + readback : exact placement guidance
→ user approval
→ approved visual organization
→ separate product asset/runtime gates when needed
```