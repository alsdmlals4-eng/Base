# Figma-Direct Visual Skill Modules Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Preserve successful local visual-tool techniques as conditional Base art-skill modules while making direct project Figma organization the normal image-work path.

**Architecture:** Keep `designing-art-prompts-and-technique-cards` and its existing Registry triggers. The owning `SKILL.md` directly indexes six packaged modules for discoverability/package integrity, while `figma-visual-bible-continuity-gate.md` remains the conditional loader/router. Figma write capability auto-places WIP when available; otherwise GPT returns exact placement guidance.

**Tech Stack:** Markdown Skill/reference contracts, Python `unittest`, GitHub Actions BCA visual workflow, Base package-integrity/reference-freshness contracts.

**Spec:** `docs/superpowers/specs/2026-08-18-figma-direct-visual-skill-modules-design.md`

## Global Constraints

- Do not create a new broad visual/Figma/Expression/Sprite Skill ID.
- Do not expand the Skill Registry when existing image triggers already route correctly.
- Direct links in `SKILL.md` are a compact discoverability index; actual module loading remains conditional through the Figma continuity gate.
- Reuse merged PR #433 `Reusable Visual Harvest Gate` and existing Figma Visual Bible structure.
- New generated visuals enter `02_WIP`/review before explicit user approval.
- Figma write success requires readback before a placement success claim.
- `APPROVED_VISUAL_REFERENCE != PROJECT_ASSET_APPROVED`.
- Local Tool Hub/Expression/Sprite runtime remains source/reference but is non-canonical and non-required for normal image work after the 2026-08-18 stop-loss.
- Do not delete Tool Hub/Studio source code or globally deprecate unrelated QA tools.
- Do not weaken package-integrity/reference-freshness contracts.
- No paid OpenAI API/API-key path.
- Do not touch unrelated open/draft PRs.

---

### Task 1: Add a consumed RED contract and correct BCA failure aggregation

**Files:**
- Create: `tests/test_figma_direct_visual_skill_modules.py`
- Modify: `.github/workflows/validate-bca-visual-sheet-workflow.yml`

- [x] **Step 1: Add RED tests before module/gate edits**

The first tests required six missing reference modules and failed on baseline.

- [x] **Step 2: Wire the new test into BCA CI**

The new suite is included in PR path filtering, `py_compile`, and `unittest` execution.

- [x] **Step 3: Observe genuine RED in logs**

RED head `b93ae2815b2124607b4bfd6c4453941ad374096e`, BCA run `32085253147`: the new suite produced `1 failure + 2 errors` because modules were absent, while later tests caused the workflow itself to appear successful.

- [x] **Step 4: Fix the discovered BCA evidence bug**

The prior workflow used `set +e` and returned only the final unittest exit status. Head `4eafd8efd2b4d3070c06ae0ecf12d48b69921c1a`, BCA run `32085309940` exposed `Run BCA contract tests = failure` by accumulating any compile/test failure with `status=1`.

### Task 2: Add focused modules and conditionally route them

**Files:**
- Create six reference modules under `skills/designing-art-prompts-and-technique-cards/references/`.
- Modify: `references/figma-visual-bible-continuity-gate.md`
- Modify: owning `SKILL.md` only as a compact direct reference index.
- Modify: owning `LEARNING_LOG.md` with the observed stop-loss/fallback lesson.

- [x] **Step 1: Implement Figma direct placement**

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

Add a condition-to-reference table and `FIGMA_DIRECT_VISUAL_ORGANIZATION` marker. Registry remains unchanged.

- [x] **Step 8: Observe package-integrity RED and add direct Skill index**

Exact head `5ac2c8a22aacbd0ca6b250d512588ea95c856f60`, GPO run `32085663918` failed one test: `SkillPackageIntegrityTests.test_every_packaged_reference_or_script_is_linked_from_its_skill`, listing the six new references. This proved gate-only indirect links were insufficient for Base package integrity.

A focused direct-link RED was then added at head `afc8677da41449155cfb93ccb54212330a192599`; BCA run `32085949687` correctly failed.

The GREEN fix added a compact direct index to `SKILL.md`; module contents remain out of the main body and conditional loading remains in the gate.

- [x] **Step 9: Update owning Skill learning evidence**

`LEARNING_LOG.md` records the 2026-08-18 stop-loss, Figma-direct fallback, direct package index requirement, readback rule, and unchanged Registry ownership.

- [x] **Step 10: Observe reference-freshness RED and update a recognized companion**

Head `65375c5c7fd000967c8282d870381f7fd1b2e660`, BCA run `32086075373`: functional BCA tests passed but reference freshness failed because `SKILL.md` changed without one of the existing recognized companion tests.

Do not weaken freshness config. Extend `tests/test_bca_visual_sheet_workflow.py` with a meaningful package-index/gate assertion.

Head `f665935e7f61e0be310884b33fce19e4c8e04836`, BCA run `32086212109`: BCA contract tests PASS and reference freshness PASS.

### Task 3: Final exact-head validation, adversarial review, merge, and postmerge readback

- [ ] **Step 1: Freeze final documentation-aligned exact head**

Spec/plan must reflect:
- compact direct index in `SKILL.md`;
- conditional loading in the Figma gate;
- unchanged Registry;
- owning Learning Log update;
- recognized BCA companion update;
- BCA failure aggregation correction.

- [ ] **Step 2: Verify all final exact-head workflows**

Require fresh runs on the documentation-aligned head:
- BCA Visual and Sheet Workflow: contract PASS + reference freshness PASS;
- Base v9: `base-v9-contract` PASS + `adversarial-gate` PASS;
- Game Project Operating System: docs/Ubuntu/publication/Windows smoke and final `ci-gate` PASS;
- Integrated Vertical Slice Prompt: PASS when triggered;
- Dependency Review: PASS when triggered.

No pre-documentation run is reused as final merge authority.

- [ ] **Step 3: Adversarial review final exact diff**

Check:
1. no new broad Skill ID or Registry trigger expansion;
2. `SKILL.md` direct index stays compact and does not duplicate module bodies;
3. normal image work does not depend on Tool Hub/PowerShell/localhost delivery;
4. unrelated QA tooling is not deprecated;
5. WIP never auto-promotes;
6. Figma visual approval never collapses into product asset approval;
7. modules reuse #433 taxonomy;
8. Figma write success requires actual readback;
9. existing continuity gate authority/access-fail-closed behavior remains;
10. package integrity/reference freshness pass without weakened rules;
11. BCA CI cannot mask an earlier failing contract.

Resolve any Critical/Important finding before merge.

- [ ] **Step 4: Update PR evidence, mark ready, and squash merge with exact-head protection**

- [ ] **Step 5: Postmerge readback**

Verify merged `main` contains:
- existing art Skill as single owner;
- compact direct module index;
- unchanged Registry ownership;
- continuity-gate conditional routing;
- six visual modules;
- local stop-loss Learning Log evidence;
- corrected BCA failure aggregation;
- dedicated + existing BCA contract consumers.

Future image work then follows:

```text
read project Figma canon
→ generate/edit
→ write available? auto-place in WIP + readback : exact placement guidance
→ user approval
→ approved visual organization
→ separate product asset/runtime gates when needed
```