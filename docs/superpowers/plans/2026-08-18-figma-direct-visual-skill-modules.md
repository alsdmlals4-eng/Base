# Figma-Direct Visual Skill Modules Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Preserve successful local visual-tool techniques as conditional Base art-skill modules while making direct project Figma organization the normal image-work path.

**Architecture:** Keep `designing-art-prompts-and-technique-cards` as the single primary art/image Skill. Add six reference modules for Figma placement, character expression, sprite/pose, effect stages, candidate/reuse review, and local-tool fallback; route them conditionally from the existing Skill and Registry. Figma write capability should auto-place WIP and approved visuals when available, while lack of write capability produces exact placement instructions rather than requiring localhost Tool Hub/Studio runtime.

**Tech Stack:** Markdown Skill/reference contracts, JSON Skill registry, Python `unittest`, GitHub Actions BCA visual workflow.

**Spec:** `docs/superpowers/specs/2026-08-18-figma-direct-visual-skill-modules-design.md`

## Global Constraints

- Do not create a new broad visual/Figma/Expression/Sprite Skill ID.
- Keep `designing-art-prompts-and-technique-cards` as the primary owner.
- Reuse merged PR #433 `Reusable Visual Harvest Gate` and existing Figma Visual Bible structure.
- Figma write availability changes execution convenience, not approval authority.
- New generated visuals enter `02_WIP`/review before explicit user approval.
- `APPROVED_VISUAL_REFERENCE != PROJECT_ASSET_APPROVED`.
- Local Tool Hub/Expression/Sprite runtime remains source/reference but is non-canonical and non-required for normal image work after the 2026-08-18 stop-loss.
- Do not delete Tool Hub/Studio source code in this change.
- No paid OpenAI API/API-key path.
- Do not touch unrelated open/draft PRs.

---

### Task 1: Add RED contracts for direct Figma placement and modular routing

**Files:**
- Modify: `tests/test_bca_visual_sheet_workflow.py`
- Test: `.github/workflows/validate-bca-visual-sheet-workflow.yml` already consumes this test and all art-skill paths.

**Interfaces:**
- Consumes: current `designing-art-prompts-and-technique-cards` Skill, Registry, visual policies/profile.
- Produces: failing contract that names the six required modules and placement/authority behavior.

- [ ] **Step 1: Add a failing test**

Add `test_art_skill_routes_figma_direct_visual_modules_without_new_skill` that reads:

```python
art_root = ROOT / "skills/designing-art-prompts-and-technique-cards"
art_skill = (art_root / "SKILL.md").read_text(encoding="utf-8")
registry = json.loads((ROOT / "skills/SKILL_REGISTRY.json").read_text(encoding="utf-8"))
profile = (ROOT / "templates/project-operations/FIGMA_VISUAL_BIBLE_PROFILE.md").read_text(encoding="utf-8")
visual_policy = (ROOT / "docs/VISUAL_COLLABORATION_TOOL_POLICY.md").read_text(encoding="utf-8")
image_policy = (ROOT / "docs/GPT_IMAGE_GENERATION_AND_REVIEW_POLICY.md").read_text(encoding="utf-8")
```

Require module files:

```python
modules = (
    "figma-direct-placement-and-canon.md",
    "character-identity-expression-controls.md",
    "sprite-pose-sequence-controls.md",
    "effect-stage-compositing-controls.md",
    "candidate-review-and-reusable-harvest.md",
    "local-visual-tool-lessons-and-fallback.md",
)
for module in modules:
    self.assertTrue((art_root / "references" / module).exists(), module)
    self.assertIn(f"references/{module}", art_skill)
```

Require one existing Skill owner and new triggers:

```python
entry = next(item for item in registry["skills"] if item["skill_id"] == "designing-art-prompts-and-technique-cards")
for tag in (
    "figma-direct-placement", "approved-visual-anchor", "character-expression",
    "character-pose", "sprite-sequence", "effect-stage",
    "visual-candidate-review", "visual-asset-reuse", "visual-harvest",
):
    self.assertIn(tag, entry["trigger_tags"])
self.assertFalse(any(item["skill_id"].startswith("figma-") for item in registry["skills"]))
```

Require direct placement and authority text across profile/policies/modules:

```python
figma_module = (art_root / "references/figma-direct-placement-and-canon.md").read_text(encoding="utf-8")
fallback_module = (art_root / "references/local-visual-tool-lessons-and-fallback.md").read_text(encoding="utf-8")
for token in ("FIGMA_WRITE_AVAILABLE", "AUTO_PLACE_WIP", "EXACT_PLACEMENT_GUIDANCE", "02_WIP", "01_APPROVED_REFERENCE", "04_FINAL"):
    self.assertIn(token, figma_module)
self.assertIn("explicit user approval", figma_module)
self.assertIn("PROJECT_ASSET_APPROVED", figma_module)
for text in (profile, visual_policy, image_policy):
    self.assertIn("FIGMA_DIRECT_VISUAL_ORGANIZATION", text)
self.assertIn("REFERENCE_ONLY_FOR_VISUAL_WORKFLOW", fallback_module)
self.assertIn("2026-08-18", fallback_module)
```

- [ ] **Step 2: Run/observe RED**

Run through the existing BCA workflow or equivalent:

```text
python -m unittest tests.test_bca_visual_sheet_workflow.BCAVisualSheetWorkflowTests.test_art_skill_routes_figma_direct_visual_modules_without_new_skill -v
```

Expected: FAIL because the six reference modules and new direct-placement tokens do not exist on current main.

- [ ] **Step 3: Commit RED-only state**

Production Skill/reference/policy files remain unchanged on the RED head.

### Task 2: Add six conditional visual reference modules

**Files:**
- Create: `skills/designing-art-prompts-and-technique-cards/references/figma-direct-placement-and-canon.md`
- Create: `skills/designing-art-prompts-and-technique-cards/references/character-identity-expression-controls.md`
- Create: `skills/designing-art-prompts-and-technique-cards/references/sprite-pose-sequence-controls.md`
- Create: `skills/designing-art-prompts-and-technique-cards/references/effect-stage-compositing-controls.md`
- Create: `skills/designing-art-prompts-and-technique-cards/references/candidate-review-and-reusable-harvest.md`
- Create: `skills/designing-art-prompts-and-technique-cards/references/local-visual-tool-lessons-and-fallback.md`

**Interfaces:**
- Consumes: existing Visual Bible continuity gate, #433 harvest categories, approved project canon.
- Produces: focused reference material that the main art Skill can conditionally load.

- [ ] **Step 1: Implement Figma direct placement module**

Must define observable branches:

```text
FIGMA_WRITE_AVAILABLE
  -> AUTO_PLACE_WIP under 02_WIP
  -> readback required
  -> explicit user approval
  -> promote/reorganize to appropriate 01_APPROVED_REFERENCE section and/or 04_FINAL

FIGMA_WRITE_UNAVAILABLE
  -> EXACT_PLACEMENT_GUIDANCE
  -> file/page/section/artifact name/status/reference IDs/next gate
```

- [ ] **Step 2: Implement character identity/expression module**

Preserve identity axes; separate requested facial movement, gaze, and head pose; use FACS only as optional vocabulary; reject unrequested costume/style/geometry drift.

- [ ] **Step 3: Implement sprite/pose sequence module**

Define pose intent, silhouette, identity invariants, prop/contact continuity, frame sequence, and atlas/export assumptions without inventing runtime evidence.

- [ ] **Step 4: Implement effect-stage module**

Define stage order, alpha/background, anchor/scale, reuse classification, and reference-vs-runtime boundary.

- [ ] **Step 5: Implement candidate/reuse module**

Define comparison dimensions and reuse existing #433 classifications rather than introducing a second taxonomy.

- [ ] **Step 6: Implement local-tool fallback module**

Record `REFERENCE_ONLY_FOR_VISUAL_WORKFLOW` after the 2026-08-18 stop-loss, preserve source/reference value, and explicitly remove Tool Hub/PowerShell/localhost delivery from the normal image-work dependency chain.

### Task 3: Route the existing Skill and Registry to the modules

**Files:**
- Modify: `skills/designing-art-prompts-and-technique-cards/SKILL.md`
- Modify: `skills/SKILL_REGISTRY.json`

**Interfaces:**
- Consumes: six Task 2 references.
- Produces: one Skill owner with conditional module routing and searchable trigger vocabulary.

- [ ] **Step 1: Add a compact conditional module routing section to SKILL.md**

The main Skill should say:

```text
Figma placement/canon -> figma-direct-placement-and-canon.md
character expression/identity edit -> character-identity-expression-controls.md
pose/sprite sequence -> sprite-pose-sequence-controls.md
effect stages -> effect-stage-compositing-controls.md
candidate comparison/reuse harvest -> candidate-review-and-reusable-harvest.md
local visual-tool status/fallback -> local-visual-tool-lessons-and-fallback.md
```

Do not duplicate full module contents in `SKILL.md`.

- [ ] **Step 2: Add Registry trigger tags to the existing art Skill entry**

Add exactly the new vocabulary from the spec; do not add another Skill entry.

### Task 4: Update Figma and image-work policies for direct placement

**Files:**
- Modify: `docs/VISUAL_COLLABORATION_TOOL_POLICY.md`
- Modify: `docs/GPT_IMAGE_GENERATION_AND_REVIEW_POLICY.md`
- Modify: `templates/project-operations/FIGMA_VISUAL_BIBLE_PROFILE.md`

**Interfaces:**
- Consumes: direct placement module and current Visual Bible pages.
- Produces: canonical policy marker `FIGMA_DIRECT_VISUAL_ORGANIZATION` and user-facing placement fallback contract.

- [ ] **Step 1: Add normal-path policy**

Record:

```text
FIGMA_DIRECT_VISUAL_ORGANIZATION
- read approved canon first
- write-capable GPT auto-places candidates in 02_WIP
- readback before placement success claim
- explicit approval before 01_APPROVED_REFERENCE/04_FINAL promotion
- no Figma placement => PROJECT_ASSET_APPROVED implication
```

- [ ] **Step 2: Add no-write fallback**

Require exact placement guidance rather than vague instructions.

- [ ] **Step 3: Record local visual runtimes as non-required for image workflow**

Do not delete or globally deprecate unrelated QA/tooling capabilities.

### Task 5: Verify GREEN, skill behavior, references, and merge

**Files:** no new production files expected after fixes.

**Interfaces:**
- Consumes: final exact PR head.
- Produces: merge-ready evidence and postmerge readback.

- [ ] **Step 1: Verify focused BCA GREEN**

Require the new test plus all existing BCA visual tests PASS.

- [ ] **Step 2: Run Base v9/GPO and reference-freshness gates**

Require applicable exact-head workflows PASS. Do not relabel unobserved runs.

- [ ] **Step 3: Adversarial review**

Check:
1. no new broad Skill ID;
2. no local Tool Hub runtime dependency in normal image path;
3. no accidental deprecation of unrelated QA tools;
4. WIP never auto-promotes;
5. Figma visual approval never collapses into product asset approval;
6. modules do not duplicate each other or #433 taxonomy;
7. future Figma write success requires actual readback.

- [ ] **Step 4: Mark ready and squash merge with exact-head protection**

- [ ] **Step 5: Postmerge readback**

Verify the merged Skill, Registry, six modules, and policy markers on `main`. Future actual image tasks then use Figma auto-placement when the connector/write capability is available, otherwise exact placement guidance.