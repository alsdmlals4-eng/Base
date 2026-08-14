# Figma Narrative Dialogue Flow Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a reusable, regression-tested Figma rule for scene/background continuity, branching dialogue, location movement, and per-scene/per-dialogue editability.

**Architecture:** Reuse the existing Visual Collaboration authority model. Add one focused project-operation profile for narrative dialogue flow and one focused regression test; avoid touching open Tool Hub/Figma bridge PR files. Figma remains a visual mirror while stable IDs connect the visual structure to project narrative data.

**Tech Stack:** Markdown contracts, Python `unittest`, GitHub PR/CI.

## Global Constraints

- Issue: #381.
- Existing Solution First verdict: `ABSORB` into existing Figma operation rules; no new broad Skill.
- Do not modify files changed by open PR #373 or #376.
- `SCENE_GROUP → DIALOGUE_BEAT → DIALOGUE_LINE → CHOICE` is the selected minimum hierarchy.
- Choices use `STAY_IN_SCENE | MOVE_SCENE | END`.
- Every scene, beat, dialogue line, and choice has a stable ID; array index is not durable identity.
- Figma is not narrative/runtime canon; prototype is not runtime proof.
- The supplied Figma Make edit mode is not implemented by this Base rules PR.

---

### Task 1: Contract test first

**Files:**
- Create: `tests/test_figma_narrative_dialogue_flow_contract.py`

**Interfaces:**
- Consumes: existing project-operation template naming and visual authority vocabulary.
- Produces: required tokens/relationships that the new profile must expose.

- [ ] **Step 1: Write the failing test**

Create a focused `unittest` that opens `templates/project-operations/FIGMA_NARRATIVE_DIALOGUE_FLOW_PROFILE.md` and requires:

```python
for token in (
    "SCENE_GROUP",
    "DIALOGUE_BEAT",
    "DIALOGUE_LINE",
    "CHOICE",
    "scene_id",
    "beat_id",
    "dialogue_id",
    "choice_id",
    "STAY_IN_SCENE",
    "MOVE_SCENE",
    "END",
    "array index",
    "Figma",
    "runtime proof",
):
    self.assertIn(token, text)
```

Also require explicit edit-selection headings for Scene, Beat, Dialogue Line, Choice and a statement that same-scene transitions preserve the scene/background container.

- [ ] **Step 2: Run test to verify RED**

Run:

```bash
python -m unittest tests.test_figma_narrative_dialogue_flow_contract -v
```

Expected: FAIL because `FIGMA_NARRATIVE_DIALOGUE_FLOW_PROFILE.md` does not exist yet.

- [ ] **Step 3: Commit RED test**

Commit only the test (design/plan documents may already exist as planning artifacts). If local execution is unavailable, use PR CI as the observed RED evidence and do not claim a local run.

### Task 2: Add minimum reusable Figma profile

**Files:**
- Create: `templates/project-operations/FIGMA_NARRATIVE_DIALOGUE_FLOW_PROFILE.md`
- Test: `tests/test_figma_narrative_dialogue_flow_contract.py`

**Interfaces:**
- Consumes: `docs/VISUAL_COLLABORATION_TOOL_POLICY.md`, `FIGMA_WORKSPACE_STRUCTURE_PROFILE.md`, `FIGMA_VISUAL_BIBLE_PROFILE.md`.
- Produces: a copy/adapt profile for project `60_GAMEPLAY_FLOWS/NARRATIVE_DIALOGUE` workspaces.

- [ ] **Step 1: Write minimal profile**

Include:

```text
SCENE_GROUP
  DIALOGUE_BEAT
    DIALOGUE_LINE
    CHOICE -> STAY_IN_SCENE | MOVE_SCENE | END
```

Define stable IDs, same-scene/background continuity, cross-scene movement, edit-mode selection scope, authority boundary, Figma naming/layout, handoff fields, and anti-drift rules.

Do not add condition/effect/localization schemas beyond ID hooks; those remain project-specific until needed.

- [ ] **Step 2: Run focused test to verify GREEN**

```bash
python -m unittest tests.test_figma_narrative_dialogue_flow_contract -v
```

Expected: PASS.

- [ ] **Step 3: Run existing visual collaboration regression**

```bash
python -m unittest tests.test_visual_collaboration_capability_contract -v
```

Expected: PASS.

### Task 3: Adversarial review and exact-head PR verification

**Files:**
- Review: all changed files only, plus untouched owners named above.

**Interfaces:**
- Consumes: exact PR diff, required status checks, same-goal open PR list.
- Produces: merge/no-merge decision with Implementation Reality Gate claim ceiling.

- [ ] **Step 1: Attack**

Check for: Figma becoming second canon; `Scene`/Godot scene terminology collision; graph node explosion; hand-authored duplicate edge sources; overbuilt condition/effect model; overlap with #373/#376.

- [ ] **Step 2: Validate critique**

Classify each finding as `MUST_FIX`, `SHOULD_FIX`, `DEFER`, `REJECTED_CRITIQUE`, or `BLOCKED_UNVERIFIED`.

- [ ] **Step 3: Minimal refinement**

Apply only validated in-scope findings.

- [ ] **Step 4: Regression recheck**

Re-read current Figma owners, changed filenames, and same-goal PRs. Confirm prototype/runtime and canon/visual boundaries still hold.

- [ ] **Step 5: Exact-head validation**

Required evidence:

```text
focused narrative dialogue-flow contract = PASS
existing visual collaboration contract = PASS
repository required status check ci-gate = PASS
unresolved review threads = 0
P0/P1 findings = 0
```

If any required item cannot be observed, keep merge blocked and report the exact missing evidence.

- [ ] **Step 6: Merge and post-merge readback**

Squash merge only after exact-head requirements pass. Then re-read merged `main`, same-goal open/recent PRs, and the new profile. Close #381 only when the merged content is present and no material follow-up remains.

## Self-review

- Spec coverage: user-requested scene grouping, choice branch visualization, location movement, per-scene and per-dialogue editing, benchmarking, IRG, adversarial loop, regression and rollback are each covered.
- Placeholder scan: no `TBD`, `TODO`, or unspecified implementation step remains.
- Type consistency: the same four stable IDs and three transition kinds are used throughout.
- Scope protection: no Figma Make source, Tool Hub, Figma bridge, Godot runtime, or external narrative-engine dependency is modified.