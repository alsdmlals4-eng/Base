# Human Home / AI Surface Hardening Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Base와 프로젝트 Notion의 첫 화면을 풍부한 사용자 학습면으로 강화하고 AI/System 운영 메타데이터를 분리하며, 이미지 two-turn hard barrier와 작업 전후 검증 Gate를 테스트로 고정한다.

**Architecture:** 기존 `HUMAN_HOME_SELF_CONTAINED_POLICY`, `PROJECT_WORKSPACE_AUTHORITY_CONTRACT`, `NOTION_PROJECT_ISOLATION_AND_CORE_SYSTEM_CONTRACT`, Visual workflow와 기존 Skill들을 유지한다. 새 광역 Skill이나 dashboard를 만들지 않고 책임 원본·Skill·회귀 테스트만 최소 확장한 뒤 GitHub merge 후 Notion Home들을 bounded edit/readback으로 동기화한다.

**Tech Stack:** Markdown/JSON policy, Python unittest contracts, GitHub PR/Actions, Notion MCP.

**Spec:** `docs/superpowers/specs/2026-08-23-human-home-ai-surface-hardening-design.md`

## Global Constraints

- `DOMAIN_SPLIT_CANON` 유지: Notion human-facing canon과 repository structured/runtime truth를 합치지 않는다.
- Human Home은 정보량을 줄이는 것이 아니라 사람에게 필요한 핵심 정보를 풍부하게 보여준다.
- PR/SHA/CI/Prompt/Hash/Implementation Path 등 AI/System metadata는 Human Home 기본 본문에서 제외한다.
- Project Home은 프로젝트별 핵심 데이터/Visual을 선택하며 모든 게임에 동일 카테고리를 강제하지 않는다.
- 새 광역 Skill, 유료 자동화, 제2 dashboard를 만들지 않는다.
- open/draft/ready PR은 read-only. Base #618 및 GRIMOIRE #151을 수정·흡수하지 않는다.
- 이미지 생성은 `TEXT_BRIEF_COMPLETE → STOP_REQUIRED → next user message → EXPLICIT_IMAGE_APPROVAL → GENERATE_EXACTLY_ONE → STOP_REQUIRED`를 지킨다.
- 승인된 결과는 GitHub/Notion에 동기화하고 write 뒤 destination readback한다.
- 최소 5회의 full adversarial improvement loop 후 clean exit를 요구한다.

---

### Task 1: Add RED contracts for richer Human Home and image hard barrier

**Files:**
- Modify: `tests/test_human_home_self_contained_contract.py`
- Modify: `tests/test_visual_requirement_gate.py`

**Interfaces:**
- Consumes: current policy text files.
- Produces: failing assertions that define the new contract before production docs change.

- [ ] **Step 1: Add Human Home failing assertions**

Require policy/Skill text to include:

```python
for term in (
    "PROJECT_SPECIFIC_CORE_DATA_INVENTORY",
    "AI_DESIGN_INTERPRETATION_FOR_HUMAN_REVIEW",
    "HOW_TO_CORRECT_AI_UNDERSTANDING",
    "HUMAN_HOME_INFORMATION_RICHNESS_IS_ALLOWED",
    "DO_NOT_FORCE_UNIVERSAL_DATA_CATEGORIES",
):
    self.assertIn(term, text)
```

- [ ] **Step 2: Add image hard-barrier failing assertions**

Require policy text to include:

```python
for term in (
    "IMAGE_TWO_TURN_HARD_BARRIER",
    "TEXT_BRIEF_COMPLETE",
    "STOP_REQUIRED",
    "EXPLICIT_IMAGE_APPROVAL",
    "GENERATE_EXACTLY_ONE",
):
    self.assertIn(term, policy)
```

- [ ] **Step 3: Run remote required checks and verify RED**

Create/update the task branch and draft PR so GitHub Actions evaluates the exact head. Expected: focused contract tests fail because production owners do not yet contain the new tokens.

- [ ] **Step 4: Record RED evidence in PR body/comment**

Record exact head and the expected missing-contract failures. Do not claim implementation complete.

---

### Task 2: Harden Human Home policy and Project Home Skill

**Files:**
- Modify: `docs/operations/HUMAN_HOME_SELF_CONTAINED_POLICY.md`
- Modify: `skills/building-project-visual-dashboards/SKILL.md`
- Modify: `docs/DOCUMENTATION_MAP.md`

**Interfaces:**
- Consumes: Task 1 contract tokens.
- Produces: authoritative Human Home behavior for Base and Project Homes.

- [ ] **Step 1: Extend Human Home policy minimally**

Add explicit contracts:

```text
HUMAN_HOME_INFORMATION_RICHNESS_IS_ALLOWED
PROJECT_SPECIFIC_CORE_DATA_INVENTORY
AI_DESIGN_INTERPRETATION_FOR_HUMAN_REVIEW
HOW_TO_CORRECT_AI_UNDERSTANDING
DO_NOT_FORCE_UNIVERSAL_DATA_CATEGORIES
```

Define that Project Home may directly show representative budget/economy/roster/enemy/item/growth/route/map/system data when that data is core to the project, while detailed raw tables remain drilldown owners.

- [ ] **Step 2: Extend visual dashboard Skill**

Require `frame-project-home` to recover the project-specific core data/visual inventory and `build-project-home` to include human-readable AI design interpretation + correction instructions without operational metadata.

- [ ] **Step 3: Align Documentation Map**

Update the Project Home standard so `PROJECT HOME` explicitly includes core systems + project-specific representative data/visual anchors + AI interpretation/correction guide, not only quick links.

- [ ] **Step 4: Verify focused Human Home tests GREEN**

Run required CI or equivalent exact-head test execution. Expected: Human Home contract test passes.

---

### Task 3: Harden project-work preflight and design-document routing

**Files:**
- Modify: `docs/PLANNING_SEQUENCE_AND_EVIDENCE_POLICY.md`
- Modify: `skills/managing-project-intake-and-work-contract/SKILL.md`
- Modify: `skills/managing-design-documents/SKILL.md`

**Interfaces:**
- Consumes: existing deep-work, >=3 alternatives, IRG, adversarial loop contracts.
- Produces: one discoverable route that Project Home/Notion work cannot skip.

- [ ] **Step 1: Add a Human Home/Notion preflight sequence**

Document:

```text
Base/project current state + Notion + PR + Skill + actual implementation/assets/tests
→ benchmark/professional practice
→ >=3 viable alternatives
→ Implementation Reality Gate
→ BEFORE/AFTER/EFFECT/risk/rollback approval bundle
→ >=5 full adversarial loops
→ user approval
```

Reference existing owners instead of duplicating their full rules.

- [ ] **Step 2: Extend intake Skill trigger behavior**

For `project-home` / `notion-project-workspace`, require the above preflight evidence before implementation and preserve small reversible recommended defaults.

- [ ] **Step 3: Extend design-document Skill**

Require approved Human Home changes to synchronize representative human information without leaking operational metadata and to keep detail owners authoritative.

- [ ] **Step 4: Re-run contract and routing tests**

Expected: existing Skill routing/governance tests remain green.

---

### Task 4: Implement the image two-turn hard barrier

**Files:**
- Modify: `docs/GPT_IMAGE_GENERATION_AND_REVIEW_POLICY.md`
- Modify: `docs/knowledge/game-development/NOTION_VISUAL_ASSET_AND_FLOW_WORKFLOW.md`
- Modify: `docs/knowledge/game-development/NOTION_GPT_VISUAL_LAYOUT_CONTRACT.md`

**Interfaces:**
- Consumes: Task 1 image contract tokens.
- Produces: explicit conversational state machine that forbids brief→generation in one assistant turn and forbids automatic sequential generation.

- [ ] **Step 1: Add policy state machine**

Add:

```text
IMAGE_TWO_TURN_HARD_BARRIER
PROJECT_REVIEW_COMPLETE
→ VISUAL_NEED_DEFINED
→ TEXT_BRIEF_COMPLETE
→ STOP_REQUIRED
[next user message]
→ EXPLICIT_IMAGE_APPROVAL
→ GENERATE_EXACTLY_ONE
→ STOP_REQUIRED
```

- [ ] **Step 2: Propagate to Notion visual workflow**

Clarify that actual approved visuals are still delivered to Notion only after approval; the barrier does not fabricate images or turn text directions into assets.

- [ ] **Step 3: Propagate to GPT layout contract**

Prevent placement automation from triggering image generation merely because a Home needs a visual slot.

- [ ] **Step 4: Verify image tests GREEN**

Expected: `tests/test_visual_requirement_gate.py` passes and no existing approval/readback semantics regress.

---

### Task 5: Whole-branch verification and adversarial refinement

**Files:**
- Review all changed files from Tasks 1-4.

**Interfaces:**
- Produces: exact-head evidence and clean review state.

- [ ] **Step 1: Run required Base checks on exact head**

Use GitHub Actions required checks. Do not substitute reasoning for execution evidence.

- [ ] **Step 2: Perform full adversarial loop 1**

Review entire approved scope: authority, Home/AI boundary, data richness, drift, project specificity, image barrier, PR isolation, cost, rollback, evidence ceiling.

- [ ] **Step 3: Perform loops 2-5 on resulting whole state**

Each counted loop repeats the full scope. If any valid MUST_FIX changes the state, apply it, verify, and continue until at least five clean full loops after the final material correction.

- [ ] **Step 4: Confirm no path overlap with Base PR #618**

Compare changed paths; #618 remains read-only.

- [ ] **Step 5: Mark PR ready only after exact-head checks and clean review**

---

### Task 6: Merge Base and postmerge readback

**Files:**
- No new files unless a postmerge correction is required.

**Interfaces:**
- Consumes: ready current-task PR.
- Produces: merged main SHA and postmerge evidence.

- [ ] **Step 1: Reconcile branch with latest main if main advanced**

Do not absorb unrelated open PR material. Resolve only merged-main facts.

- [ ] **Step 2: Re-run exact-head required checks**

- [ ] **Step 3: Squash merge current-task PR**

Follow repository governance; no force/admin bypass.

- [ ] **Step 4: Fetch new main SHA and perform postmerge full-scope review**

If a valid postmerge finding exists, create a new correction branch/PR rather than editing the merged PR.

---

### Task 7: Update Notion Base Home and Hub after GitHub evidence

**Files/Surfaces:**
- Notion `Base · 작업 시스템 & Skill 지도`
- Notion `00 · 프로젝트 허브`
- Existing `90 · SYSTEM MASTERS` remains the AI/System owner.

**Interfaces:**
- Consumes: merged Base policy and new main SHA.
- Produces: user-facing Base Home that teaches the workflow without raw operational clutter.

- [ ] **Step 1: Fetch current Base Home/Hub/System pages**

- [ ] **Step 2: Remove or demote raw PR/SHA/CI/connector closure blocks from the Base Home default learning narrative**

Preserve relevant history in AI/System/drilldown; do not delete System Master data.

- [ ] **Step 3: Add human learning sections**

Include lifecycle flow, why each phase exists, AI interpretation, correction instructions, Home vs AI/System explanation, and image two-turn rule.

- [ ] **Step 4: Keep Hub as the single human navigation entry**

Base Home + Project Homes stay prominent; System Masters remain separate.

- [ ] **Step 5: Destination readback**

Verify expected sections and absence of raw operational metadata in the default Base Home narrative.

---

### Task 8: Enrich Project Homes without duplicating canon

**Files/Surfaces:**
- Ten current Project Homes in Notion.
- Existing project-specific Flow/System/Data/Visual drilldowns.

**Interfaces:**
- Consumes: each project Home plus project-specific drilldowns and current GitHub/PR state.
- Produces: richer project-specific Human Homes.

- [ ] **Step 1: Use TEN_PACES/십보강호 as first internal migration sample**

Pull representative summaries/visual anchors from existing Flow, core system, budget, opponents/Route pages while leaving detailed owners in place.

- [ ] **Step 2: Add `AI가 이해한 설계 의도` and `수정하는 방법`**

Keep them human-readable and exclude operational metadata.

- [ ] **Step 3: Read back TEN_PACES Home and verify no duplicate canon or AI metadata leakage**

- [ ] **Step 4: Apply the same contract project-by-project**

Do not copy TEN_PACES sections blindly. Re-read each project and select its real core data/visual categories.

- [ ] **Step 5: Respect active project PRs**

GRIMOIRE PR #151 remains branch-only/draft and must not be promoted into Home as current confirmed implementation.

- [ ] **Step 6: Read back every updated Home**

Verify project identity, core loop, systems, representative data/visual status, AI interpretation/correction guide, status/NOT_RUN, and no raw AI/System metadata.

---

### Task 9: Final post-change adversarial review and completion report

**Files/Surfaces:**
- Merged Base main
- Updated Notion Base Home/Hub/Project Homes/System boundary

**Interfaces:**
- Produces: final clean state or bounded correction tasks.

- [ ] **Step 1: Full-loop review 1-5+ over merged GitHub + Notion state**

Each loop rechecks the complete approved scope. Continue beyond five if new valid findings remain.

- [ ] **Step 2: Re-check open PRs and untouched consumers**

Ensure #618 and project PRs were not mutated/absorbed.

- [ ] **Step 3: Recalculate Implementation Reality Gate**

Separate policy/Notion readback PASS from runtime/player/device claims that remain NOT_RUN.

- [ ] **Step 4: Report BEFORE → AFTER → actual use example → expected effect → still-unimproved/NOT_RUN**

Include exact merged PR/main evidence and Notion readback status.
