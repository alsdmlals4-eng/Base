# Project Visual Flow Workspace Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Extend the existing Base visual collaboration contract so AI-generated game screens, GPT interpretation records, Figma flows/prototypes, and runtime comparisons form one project Visual Flow Workspace without creating a second canon or a new Figma-specific Skill.

**Architecture:** Reuse the existing visual policy, image-generation Skill, UX/UI Skill, visual artifact registry, image review plan, and optional Sheet visual index. Add only the missing cross-links and machine-checkable tokens; keep runtime evidence and canonical decisions outside Figma.

**Tech Stack:** Markdown, JSON, Python `unittest`, existing GitHub Actions validation workflows.

## Global Constraints

- No new `figma-*` Skill or ACTIVE Skill identity.
- Figma remains a noncanonical visual workspace; GitHub decisions/canonical docs and actual runtime evidence keep authority.
- Prototype evidence never proves Godot runtime, physical input, performance, accessibility, persistence, or domain-rule completion.
- `DISCOVERED_IDEA` and `AI_ASSUMPTION` never become requirements without a user Decision.
- Google Sheets stores only Artifact ID, link/status, decision/canon references, and next gate; it does not duplicate full visual records.
- Actual Figma/Godot execution not performed in this Base policy change remains `NOT_RUN` or `UNVERIFIED`.

---

### Task 1: Lock the canonical visual-workspace policy

**Files:**
- Modify: `docs/VISUAL_COLLABORATION_TOOL_POLICY.md`
- Test: `tests/test_visual_collaboration_capability_contract.py`

**Interfaces:**
- Consumes: existing `DRAFT_VISUAL → ... → VALIDATED` lifecycle and noncanonical Figma boundary.
- Produces: canonical terms `Project Visual Flow Workspace`, `INTERPRETATION_RECORD`, artifact type vocabulary, and runtime drift classifications.

- [ ] **Step 1: Write failing policy assertions**

Add assertions requiring these tokens in `docs/VISUAL_COLLABORATION_TOOL_POLICY.md`:

```python
for token in (
    "Project Visual Flow Workspace",
    "INTERPRETATION_RECORD",
    "DISCOVERED_IDEA",
    "AI_ASSUMPTION",
    "PROTOTYPE_FLOW",
    "RUNTIME_CAPTURE",
    "COMPARE_BOARD",
    "IMPLEMENTATION_GAP",
    "AI_MOCKUP_ERROR",
):
    self.assertIn(token, text)
```

Also assert prototype/runtime separation remains explicit.

- [ ] **Step 2: Run the focused test and confirm RED**

Run:

```bash
python -m unittest tests.test_visual_collaboration_capability_contract -v
```

Expected: new token assertions fail on the pre-change policy.

- [ ] **Step 3: Add the minimal policy section**

Add a section that defines:

```text
canonical planning
→ Screen Brief
→ AI planning visualization
→ Screen Interpretation Review
→ Project Visual Flow Workspace
→ prototype when useful
→ user approval
→ implementation pin
→ runtime capture
→ compare board
→ drift classification
```

Keep existing authority and access/fallback sections intact.

- [ ] **Step 4: Run focused test and confirm GREEN**

Run the same unittest command. Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add docs/VISUAL_COLLABORATION_TOOL_POLICY.md tests/test_visual_collaboration_capability_contract.py
git commit -m "docs: define project visual flow workspace"
```

### Task 2: Bind GPT image interpretation to existing Skills

**Files:**
- Modify: `skills/designing-art-prompts-and-technique-cards/SKILL.md`
- Modify: `skills/auditing-and-refining-ui-art/SKILL.md`
- Test: `tests/test_visual_collaboration_capability_contract.py`

**Interfaces:**
- Consumes: `planning-visualization`, `intermediate-visual-checkpoint`, `flow-and-information-architecture`, `runtime-ui-audit`.
- Produces: interpretation classification and prototype/runtime compare review loop.

- [ ] **Step 1: Add failing Skill assertions**

Require the art Skill to contain:

```text
CONFIRMED
DISCOVERED_IDEA
AI_ASSUMPTION
INTERPRETATION_RECORD
```

Require the UX/UI Skill to contain:

```text
PROTOTYPE_FLOW
RUNTIME_CAPTURE
COMPARE_BOARD
MATCHED
INTENDED_DIFFERENCE
IMPLEMENTATION_GAP
PLANNING_CHANGE_REQUIRED
AI_MOCKUP_ERROR
```

- [ ] **Step 2: Run focused test and confirm RED**

```bash
python -m unittest tests.test_visual_collaboration_capability_contract -v
```

- [ ] **Step 3: Add minimal Skill instructions**

Art Skill: after generated screen review, classify each visible addition as current-canon alignment, unapproved discovered idea, or unsupported AI assumption and write/sync an interpretation record.

UX/UI Skill: evaluate prototype navigation separately from runtime evidence, then compare approved visual reference against actual capture and assign exactly one drift classification per finding.

- [ ] **Step 4: Run focused test and confirm GREEN**

Same command; expected PASS.

- [ ] **Step 5: Commit**

```bash
git add skills/designing-art-prompts-and-technique-cards/SKILL.md skills/auditing-and-refining-ui-art/SKILL.md tests/test_visual_collaboration_capability_contract.py
git commit -m "docs: connect visual interpretation and runtime compare"
```

### Task 3: Make the artifact registry and image plan traceable

**Files:**
- Modify: `templates/project-operations/VISUAL_ARTIFACT_REGISTRY.json`
- Modify: `templates/planning/GPT_IMAGE_GENERATION_AND_REVIEW_PLAN.md`
- Test: `tests/test_visual_collaboration_capability_contract.py`

**Interfaces:**
- Consumes: existing visual artifact identity, source commit, snapshot, scope/exclusion fields.
- Produces: screen/flow IDs, interpretation status, runtime comparison traceability.

- [ ] **Step 1: Add failing schema/template assertions**

Registry sample must include:

```json
"screen_id": "",
"flow_id": "",
"interpretation_status": "UNVERIFIED",
"runtime_compare_status": "NOT_RUN"
```

Image review plan must include tokens:

```text
screen_id
flow_id
figma_artifact_id
interpretation_status
runtime_compare_required
runtime_capture_path
drift_status
```

- [ ] **Step 2: Run focused test and confirm RED**

```bash
python -m unittest tests.test_visual_collaboration_capability_contract -v
```

- [ ] **Step 3: Extend the existing sample and template only**

Do not create a second registry. Keep all old fields. Add enum guidance:

```text
interpretation_status = CONFIRMED | DISCOVERED_IDEA | AI_ASSUMPTION | MIXED | UNVERIFIED
runtime_compare_status = NOT_RUN | MATCHED | INTENDED_DIFFERENCE | IMPLEMENTATION_GAP | PLANNING_CHANGE_REQUIRED | AI_MOCKUP_ERROR | VISUAL_CANONICAL_CONFLICT | BLOCKED_UNVERIFIED
```

- [ ] **Step 4: Validate JSON and focused test**

```bash
python -m json.tool templates/project-operations/VISUAL_ARTIFACT_REGISTRY.json > /dev/null
python -m unittest tests.test_visual_collaboration_capability_contract -v
```

Expected: both PASS.

- [ ] **Step 5: Commit**

```bash
git add templates/project-operations/VISUAL_ARTIFACT_REGISTRY.json templates/planning/GPT_IMAGE_GENERATION_AND_REVIEW_PLAN.md tests/test_visual_collaboration_capability_contract.py
git commit -m "docs: trace visual flow interpretation evidence"
```

### Task 4: Strengthen the optional Sheet visual index without duplicating canon

**Files:**
- Modify: `templates/planning/PROJECT_PLANNING_SEQUENCE_AND_SHEET_TABS.md`
- Test: `tests/test_visual_collaboration_capability_contract.py`

**Interfaces:**
- Consumes: optional `06_시각_작업면` index.
- Produces: compact screen/flow/interpretation/runtime compare status routing.

- [ ] **Step 1: Add failing Sheet-template assertion**

Require `06_시각_작업면` documentation to mention `Screen/Flow ID`, interpretation summary, runtime compare status, and the rule that full interpretation text stays in the responsible artifact/canon record rather than being duplicated in Sheets.

- [ ] **Step 2: Run focused test and confirm RED**

```bash
python -m unittest tests.test_visual_collaboration_capability_contract -v
```

- [ ] **Step 3: Extend `06_시각_작업면` minimally**

Add fields or explanatory guidance only; do not require the tab for projects without visual artifacts.

- [ ] **Step 4: Run focused test and confirm GREEN**

Same command; expected PASS.

- [ ] **Step 5: Commit**

```bash
git add templates/planning/PROJECT_PLANNING_SEQUENCE_AND_SHEET_TABS.md tests/test_visual_collaboration_capability_contract.py
git commit -m "docs: index visual flow review state"
```

### Task 5: Regression, adversarial review, and PR handoff

**Files:**
- Review all changed files.

**Interfaces:**
- Consumes: Tasks 1-4.
- Produces: exact-head evidence and merge-ready PR without claiming actual project Figma/Godot validation.

- [ ] **Step 1: Run focused contract and adjacent suites**

```bash
python -m unittest tests.test_visual_collaboration_capability_contract -v
python -m unittest tests.test_project_gdd_google_sheets_contract -v
python -m unittest tests.test_game_ux_ui_system -v
```

- [ ] **Step 2: Run repository validators used by the visual/sheet workflow**

Use the commands referenced by `.github/workflows/validate-bca-visual-sheet-workflow.yml` and run `git diff --check`.

- [ ] **Step 3: Adversarial review**

Attack for:

```text
second canon
new Skill identity
automatic promotion of DISCOVERED_IDEA / AI_ASSUMPTION
prototype treated as runtime proof
full duplicate interpretation text in Sheets
mandatory Figma adoption
live-file-only handoff without source commit/snapshot
```

Classify each finding as `MUST_FIX / SHOULD_FIX / USER_DECISION_REQUIRED / DEFER / REJECTED_CRITIQUE / BLOCKED_UNVERIFIED`.

- [ ] **Step 4: Re-run exact-head tests after any approved fix**

All previously passing focused/adjacent checks must still pass.

- [ ] **Step 5: Open PR**

PR body must state:

```text
No new ACTIVE Skill.
No project Figma file modified.
Actual Figma prototype/runtime usability: NOT_RUN.
Actual Godot runtime comparison: NOT_RUN.
```

- [ ] **Step 6: Inspect PR diff and required workflow runs**

Confirm intended changed files only, unresolved review threads are zero or explicitly reported, and exact head SHA is recorded.

## Plan Self-Review

- Spec coverage: all approved design requirements map to Tasks 1-5.
- Placeholder scan: no TBD/TODO implementation placeholders.
- Type/field consistency: `screen_id`, `flow_id`, `interpretation_status`, `runtime_compare_status`, and drift classifications use the same spelling across policy, Skills, registry, template, and tests.
- Scope: no new Skill identity, project-specific Figma URL, or Godot implementation is included.
