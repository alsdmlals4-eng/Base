# Human Home + AI/System Separation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make Base/Project Notion Home a rich self-contained human learning surface while keeping operational AI metadata in existing System surfaces, and enforce a two-turn image approval barrier.

**Architecture:** Reuse the existing `HUMAN_HOME_SELF_CONTAINED_POLICY`, Project Workspace authority contract, System Masters, Project Home pages, and current visual/dashboard Skills. Strengthen existing owners instead of adding a broad Skill or a second dashboard. Tests lock the Home content boundary and image-conversation barrier before Notion migration.

**Tech Stack:** Markdown/JSON policy contracts, Python `unittest`, GitHub PR/Actions, Notion MCP bounded page edits/readback.

**Spec:** `docs/superpowers/specs/2026-08-23-human-home-ai-system-separation-design.md`

## Global Constraints

- `OPEN_PR_READ_ONLY_BY_DEFAULT`; do not modify unrelated open/draft/ready PRs.
- Human Home may be information-rich; the exclusion criterion is AI/System operational metadata, not page length.
- Existing System Masters/Registry/Master DBs and project child pages must be preserved.
- No new broad Skill, paid service, Figma/HTML dashboard, or duplicated runtime authority.
- Project-specific data must not be flattened into one universal template.
- Actual approved visuals require Notion durable delivery + readback; missing visuals are not generated implicitly.
- Image work requires `TEXT_BRIEF_STOP_REQUIRED → NEXT_USER_EXPLICIT_APPROVAL → GENERATE_EXACTLY_ONE → STOP_REQUIRED`.
- Notion writes use smallest bounded edit and destination readback.
- Build completion requires minimum five full adversarial improvement loops after implementation, exact-head validation, merge, and postmerge readback.

---

### Task 1: Lock the richer Human Home contract with failing tests

**Files:**
- Modify: `tests/test_human_home_self_contained_contract.py`
- Test: `tests/test_human_home_self_contained_contract.py`

**Interfaces:**
- Consumes: current `HUMAN_HOME_SELF_CONTAINED_POLICY.md`, `NOTION_PROJECT_ISOLATION_AND_CORE_SYSTEM_CONTRACT.md`, `building-project-visual-dashboards/SKILL.md`.
- Produces: regression expectations for rich Home sections, AI interpretation boundary, edit guide, and project-specific data projection.

- [ ] **Step 1: Add failing regression tests**

Add tests equivalent to:

```python
def test_project_home_is_rich_not_minimal_and_exposes_human_core_data(self) -> None:
    text = POLICY.read_text(encoding="utf-8")
    for term in (
        "PROJECT_HOME_INFORMATION_RICHNESS_ALLOWED",
        "PROJECT_SPECIFIC_CORE_DATA",
        "AI_INTERPRETATION_FOR_USER_CORRECTION",
        "HUMAN_EDIT_GUIDE_REQUIRED",
        "FLOW_MAP",
        "CORE_SYSTEMS",
        "VISUAL_ASSET_ANCHORS",
    ):
        self.assertIn(term, text)


def test_ai_interpretation_is_not_operational_metadata(self) -> None:
    text = POLICY.read_text(encoding="utf-8")
    self.assertIn("AI_INTERPRETATION_FOR_USER_CORRECTION", text)
    self.assertIn("AI_SYSTEM_OPERATIONAL_METADATA_EXCLUDED", text)
    for forbidden in (
        "raw PR/commit/CI history",
        "Prompt / AI Note / Asset ID / Hash / Implementation Path",
    ):
        self.assertIn(forbidden, text)
```

- [ ] **Step 2: Run the focused test and confirm RED**

Run through Base required CI or local validation entrypoint:

```bash
python -m unittest tests.test_human_home_self_contained_contract -v
```

Expected: new token assertions fail against the current policy.

- [ ] **Step 3: Commit the RED contract**

Commit message:

```text
test: require rich human home and AI system boundary
```

---

### Task 2: Strengthen existing Human Home and Project Home owners

**Files:**
- Modify: `docs/operations/HUMAN_HOME_SELF_CONTAINED_POLICY.md`
- Modify: `skills/building-project-visual-dashboards/SKILL.md`
- Modify when needed for discovery/freshness: `docs/DOCUMENTATION_MAP.md`
- Test: `tests/test_human_home_self_contained_contract.py`

**Interfaces:**
- Consumes: Task 1 regression.
- Produces: one human-facing contract used by Base Home and all Project Homes without creating a new Skill.

- [ ] **Step 1: Extend `HUMAN_HOME_SELF_CONTAINED_POLICY.md` with explicit invariants**

Add these named contracts and their human-readable definitions:

```text
PROJECT_HOME_INFORMATION_RICHNESS_ALLOWED
PROJECT_SPECIFIC_CORE_DATA
AI_INTERPRETATION_FOR_USER_CORRECTION
AI_SYSTEM_OPERATIONAL_METADATA_EXCLUDED
HUMAN_EDIT_GUIDE_REQUIRED
HUMAN_HOME_PROGRESSIVE_DISCLOSURE
HOME_PROJECTION_IS_NOT_DUPLICATE_CANON
```

Required meaning:

```text
30-second overview
→ 5-minute core Flow/System/Data understanding
→ drilldown for full tables/evidence/history
```

Project Home must surface project-relevant examples such as budget/economy, monster/opponent, item/skill, roster, growth, route/map only when they are actually core to that project.

- [ ] **Step 2: Add a Base Home rule**

Base Home must teach lifecycle, Skill purpose/input/process/output, user correction path, active-vs-retired surfaces, and readable PASS/NOT_RUN state. Raw PR/SHA/CI/receipt histories move to AI/System drilldown by default.

- [ ] **Step 3: Update `building-project-visual-dashboards`**

Strengthen `frame-project-home` / `build-project-home` / quality gate so Home construction explicitly includes:

```text
project-specific core data inventory
→ core Flow
→ core systems
→ human-useful visual anchors
→ AI interpretation for user correction
→ edit guide
→ current human-readable state
```

Reject fixed universal sections that force irrelevant monster/economy/etc. into every project.

- [ ] **Step 4: Run focused regression**

```bash
python -m unittest tests.test_human_home_self_contained_contract -v
```

Expected: PASS.

- [ ] **Step 5: Commit**

```text
docs: make human homes rich and self-contained
```

---

### Task 3: Enforce the two-turn image conversation barrier

**Files:**
- Create: `docs/knowledge/game-development/IMAGE_CONVERSATION_APPROVAL_GATE.md`
- Modify: `docs/knowledge/game-development/NOTION_GPT_VISUAL_LAYOUT_CONTRACT.md`
- Modify: `skills/building-project-visual-dashboards/SKILL.md`
- Modify: `tests/test_visual_requirement_gate.py`
- Test: `tests/test_visual_requirement_gate.py`

**Interfaces:**
- Consumes: existing Visual Requirement Gate, approved-visual Notion delivery workflow.
- Produces: a reusable hard conversation gate that prevents immediate image generation chains.

- [ ] **Step 1: Add RED tests**

Add a test equivalent to:

```python
def test_image_conversation_requires_two_turn_barrier(self) -> None:
    gate = read("docs/knowledge/game-development/IMAGE_CONVERSATION_APPROVAL_GATE.md")
    for token in (
        "PROJECT_REVIEW_COMPLETE",
        "TEXT_BRIEF_STOP_REQUIRED",
        "NEXT_USER_EXPLICIT_APPROVAL",
        "GENERATE_EXACTLY_ONE",
        "STOP_REQUIRED_AFTER_GENERATION",
        "NO_AUTOMATIC_IMAGE_CHAIN",
    ):
        self.assertIn(token, gate)
```

Also assert `NOTION_GPT_VISUAL_LAYOUT_CONTRACT.md` and `building-project-visual-dashboards/SKILL.md` reference `IMAGE_CONVERSATION_APPROVAL_GATE.md`.

- [ ] **Step 2: Confirm RED**

```bash
python -m unittest tests.test_visual_requirement_gate -v
```

Expected: missing gate file/reference assertions fail.

- [ ] **Step 3: Create the gate**

The new file must define exactly:

```text
project/current visual canon review
→ Visual Need
→ text brief
→ TEXT_BRIEF_STOP_REQUIRED

next user message
→ NEXT_USER_EXPLICIT_APPROVAL
→ generate/edit exactly one requested image
→ STOP_REQUIRED_AFTER_GENERATION
```

It must state that generation success never auto-approves or auto-continues to the next image.

- [ ] **Step 4: Reference the gate from current visual owners**

Do not create a new Skill. Existing Home/visual work routes to this contract only when image generation/editing is actually requested.

- [ ] **Step 5: Run focused regression and commit**

```bash
python -m unittest tests.test_visual_requirement_gate -v
```

Expected: PASS.

Commit:

```text
docs: enforce two-turn image approval gate
```

---

### Task 4: Lock the pre-work / approval / post-work lifecycle into existing routing

**Files:**
- Modify: `skills/managing-project-intake-and-work-contract/SKILL.md`
- Modify: `skills/managing-design-documents/SKILL.md`
- Modify only if current wording is insufficient: `docs/PLANNING_SEQUENCE_AND_EVIDENCE_POLICY.md`
- Test: existing routing/governance tests plus a focused new test if no existing test owns the behavior.

**Interfaces:**
- Consumes: current Deep Work gate, >=3 alternatives, adversarial-review-until-clean, confirmed decision sync.
- Produces: an explicit user-facing pre-build report contract and mandatory GitHub+Notion synchronization during approved project work.

- [ ] **Step 1: Add/extend regression for the lifecycle**

Required tokens:

```text
FULL_CURRENT_STATE_AUDIT_BEFORE_PLAN
PRE_BUILD_BEFORE_AFTER_EXPECTED_EFFECT_REPORT
USER_APPROVAL_BEFORE_BUILD
APPROVED_DECISION_GITHUB_NOTION_SYNC_DURING_WORK
POST_BUILD_FULL_ADVERSARIAL_REVIEW_AND_PR_RECHECK
```

- [ ] **Step 2: Confirm RED**

Run the focused routing/governance test selected by the existing test suite.

- [ ] **Step 3: Strengthen existing owners, not `AGENTS.md` duplication**

The implementation must preserve:

```text
current state + canon + PR + Skill + Notion audit
→ benchmark/professional practice
→ >=3 alternatives
→ IRG
→ before/after/effects/risks/rollback report
→ user approval
→ build
→ approved decision GitHub+Notion sync during work
→ post-build full adversarial review + PR recheck
```

Do not duplicate already-strong Long Horizon/AGENTS invariants unless a required consumer test proves a propagation gap.

- [ ] **Step 4: Run focused and routing regressions**

Expected: PASS.

- [ ] **Step 5: Commit**

```text
docs: harden prebuild approval and sync lifecycle
```

---

### Task 5: Migrate Notion human surfaces without deleting System data

**Files / Surfaces:**
- Update: `Base · 작업 시스템 & Skill 지도`
- Update: `00 · 프로젝트 허브`
- Preserve: `90 · SYSTEM MASTERS`
- Update: 10 current Human Project Home pages
- Reuse: project Visual Bible / Flow / Asset / project-specific confirmed tables and existing Master DBs

**Interfaces:**
- Consumes: merged/verified Base contract candidate and current Notion content.
- Produces: rich Human Homes plus preserved AI/System masters.

- [ ] **Step 1: Read every destination immediately before write**

For each Home fetch current page and relevant drilldowns. Do not use stale snapshots.

- [ ] **Step 2: Update Base Home**

Move/condense operational closure history out of the default learning flow. Keep durable human lessons, but make lifecycle, Skill map, user correction path, active/retired surfaces, and readable current state primary.

- [ ] **Step 3: Update `00 · 프로젝트 허브`**

Keep it a human navigation surface. Make Base Home and Project Homes primary; System Masters remain an explicitly separate AI/operations entry.

- [ ] **Step 4: Update each Project Home using its actual project identity**

For each project:

```text
read Home
→ read core Flow/System/Visual/data drilldowns
→ identify project-specific core data
→ update Home with rich human explanations/anchors
→ add AI interpretation for user correction
→ add user edit guide
→ keep raw operational metadata out
→ destination readback
```

Do not copy the Ten Paces section names to every game.

- [ ] **Step 5: Preserve visuals correctly**

Existing approved visuals remain. Missing visuals stay missing. No image generation in this migration task.

- [ ] **Step 6: Destination readback**

Fetch Base Home, Hub, all Project Homes, and System Masters. Verify no Human Home became a Registry row or raw AI metadata dump.

---

### Task 6: Full verification, adversarial loops, PR, merge, postmerge readback

**Files:**
- All changed Base files/tests from Tasks 1–4
- Notion surfaces from Task 5

**Interfaces:**
- Consumes: candidate branch + Notion migrated state.
- Produces: exact-head evidence, clean adversarial result, merge, and final GitHub/Notion readback.

- [ ] **Step 1: Run focused tests**

```bash
python -m unittest tests.test_human_home_self_contained_contract -v
python -m unittest tests.test_visual_requirement_gate -v
```

- [ ] **Step 2: Run applicable Base required validation**

Use repository-native required workflows/CI for docs/Skill/contract changes. Do not claim local/runtime/device evidence that is not executed.

- [ ] **Step 3: Perform full adversarial improvement loops**

Each counted loop rechecks the complete approved scope:

```text
user intent + Base authority + Notion + Skill + PR + tests + visuals + image barrier + project-specific data + cost + rollback + evidence ceiling
→ validate findings
→ refine verified findings
→ regression recheck
→ better alternative search
→ long-term fit recheck
→ re-attack full result
```

Minimum 5 loops; continue beyond 5 if any new valid MUST_FIX/blocker appears.

- [ ] **Step 4: Reconcile latest main and open PRs**

Do not absorb unrelated open PR material. If main advanced, rebase/reconstruct only on current completed main while preserving the approved semantic diff.

- [ ] **Step 5: Open current-task PR and wait for exact-head required checks**

PR body records before/after, selected/rejected alternatives, IRG ceiling, Notion migration/readback, adversarial loop evidence, and rollback.

- [ ] **Step 6: Merge only after required checks and clean review**

Use repository-approved squash merge path; no bypass.

- [ ] **Step 7: Postmerge readback**

Fetch exact new Base main, re-read Base/Project Homes and System Masters, recheck same-goal PR state, and confirm `REQUIRED_WORK_REMAINING = 0` or explicitly list a real external blocker.
