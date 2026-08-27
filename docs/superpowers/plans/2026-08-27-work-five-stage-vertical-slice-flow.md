# Work Five-Stage Vertical Slice Flow Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Work 게임 프로젝트 실행을 기획 → 검수 → 이미지·요소 생성 → Codex 구현 → 사용자 검증의 5단계 macro flow로 정렬하고, 사람 검증 전 자동 readiness와 최종 버티컬 슬라이스 완료를 명확히 분리한다.

**Architecture:** 기존 Base owner와 compatibility token을 보존한 채 current Router, minimum-transition profile, GPT↔Codex policy, planning/Grill Me policy, vertical-slice Skill에 같은 5단계 의미를 연결한다. 프로젝트에는 세부 절차를 복제하지 않고 충돌하는 current AGENTS에 얇은 Base macro-flow routing만 추가한다.

**Tech Stack:** Markdown contracts, Python `unittest` contract tests, GitHub Actions, current Base/project canon.

**Spec:** `docs/superpowers/specs/2026-08-27-work-five-stage-vertical-slice-flow-design.md`

## Global Constraints

- current Base owner를 두 번째 정본으로 복제하지 않는다.
- `CODEX_SINGLE_IMPLEMENTATION_WINDOW`와 Work↔Codex 최소 왕복을 유지한다.
- `AUTOMATED_VERTICAL_SLICE_READY != VERTICAL_SLICE_VALIDATED_COMPLETE`를 명시한다.
- Stage 5 actual user play 전 Human/Player PASS를 주장하지 않는다.
- 새/변경 core Slice planning은 material user Decision에 Grill Me + decision-relevant benchmark를 사용한다.
- actual consumer 없는 production image/element를 만들지 않는다.
- Base open PR의 changed path를 takeover하지 않는다.
- 비게임 프로젝트에는 Godot/Codex five-stage flow를 강제하지 않는다.

---

### Task 1: RED contract for the five macro stages

**Files:**
- Create: `tests/test_work_five_stage_vertical_slice_flow_contract.py`

**Interfaces:**
- Consumes: current Router/profile/workflow/planning/vertical-slice owner text.
- Produces: exact token/order/completion regression contract used by later tasks.

- [ ] **Step 1: Write the failing contract test**

Assert five stage tokens in order, collaborative planning markers, Stage 2 clean gate, Stage 3 actual consumer, Stage 4 Work review before Stage 5, and `VERTICAL_SLICE_VALIDATED_COMPLETE` only after actual user validation.

- [ ] **Step 2: Run exact RED in GitHub Actions**

Open a draft PR on the test-only head and confirm the contract fails because current owners still expose the three-stage Work-prep flow and lack the final completion marker.

- [ ] **Step 3: Record the expected RED evidence in the PR body**

Do not reinterpret unrelated failures as the intended RED.

### Task 2: Align Base current Router and minimum-transition profile

**Files:**
- Modify: `templates/project-operations/WORK_PROJECT_EXECUTION_CURRENT_ROUTER.md`
- Modify: `templates/project-operations/WORK_CODEX_MINIMUM_TRANSITION_VERTICAL_SLICE_PROFILE.md`
- Test: `tests/test_work_five_stage_vertical_slice_flow_contract.py`
- Test: `tests/test_work_codex_minimum_transition_automation_contract.py`

**Interfaces:**
- Consumes: five-stage spec, existing compatibility tokens.
- Produces: shared macro routing and single Codex window semantics.

- [ ] **Step 1: Replace the current three-stage macro interpretation with five explicit macro stages**

Keep existing minimum-transition tokens as compatibility vocabulary; explain that minimal transition refers to Work↔Codex round trips, not macro stage count.

- [ ] **Step 2: Put Work final evidence review inside Stage 4 closeout**

Keep it before Stage 5 actual user validation.

- [ ] **Step 3: Add final completion boundary**

Require `READY_FOR_USER_VERTICAL_SLICE_VALIDATION != VERTICAL_SLICE_VALIDATED_COMPLETE` and actual user validation/decision before next Slice.

- [ ] **Step 4: Run focused contracts and fix only observed regressions**

### Task 3: Align planning collaboration and GPT↔Codex boundaries

**Files:**
- Modify: `docs/PLANNING_FIRST_GRILL_ME_BATCH_POLICY.md`
- Modify: `docs/GPT_CODEX_WORKFLOW_POLICY.md`
- Modify: `templates/project-operations/WORK_PROJECT_START_CANON_CHECKLIST.md`
- Test: `tests/test_work_five_stage_vertical_slice_flow_contract.py`

**Interfaces:**
- Consumes: existing Grill Me mode/policy, Existing Solution First, project direction receipt.
- Produces: Stage 1 user collaboration and Stage state receipt fields.

- [ ] **Step 1: Add core Slice planning collaboration trigger**

Use Grill Me for still-unapproved material player-promise/choice/reward/emotion/sales-point/Slice-acceptance decisions; never re-ask known facts or implementation details.

- [ ] **Step 2: Require decision-relevant three-approach benchmark for core choices**

Use current project/reuse first and classify `ADOPT / ADAPT / REJECT`.

- [ ] **Step 3: Split GPT pre-handoff flow into Stages 1–3 and Stage 4 closeout**

Preserve Codex technical autonomy and no-extra-round-trip intent.

- [ ] **Step 4: Add `macro_stage` / `stage_gate_state` to startup receipt without duplicating project mutable truth**

### Task 4: Align vertical-slice completion semantics

**Files:**
- Modify: `skills/designing-vertical-slices/SKILL.md`
- Test: `tests/test_work_five_stage_vertical_slice_flow_contract.py`

**Interfaces:**
- Consumes: existing Definition of Done and playtest decision gate.
- Produces: unambiguous pre-human readiness vs validated completion vocabulary.

- [ ] **Step 1: Define Stage 4 automated readiness as a candidate state, not completed Vertical Slice**

- [ ] **Step 2: Define `VERTICAL_SLICE_VALIDATED_COMPLETE` after actual Stage 5 play evidence and decision gate**

- [ ] **Step 3: Preserve existing shipping-intent quality, rights, accessibility, performance and playtest requirements**

### Task 5: Project thin-routing reconciliation

**Files:**
- Modify only current game-project AGENTS/adapter files whose macro workflow conflicts or is ambiguous.
- Do not modify `Coc-Fiction` game-runtime flow because it is explicitly non-game.

**Interfaces:**
- Consumes: merged/current Base five-stage owner.
- Produces: thin project routing with project-specific current stage still resolved locally.

- [ ] **Step 1: Re-read every active game project main/open PR before each project write**

- [ ] **Step 2: Add thin macro-flow routing instead of copying Base details**

Use:

```text
PROJECT_WORK_MACRO_FLOW = CURRENT_BASE_FIVE_STAGE_VERTICAL_SLICE_FLOW
PROJECT_SPECIFIC_STAGE_STATE = RESOLVE_FROM_CURRENT_PROJECT_CANON
```

- [ ] **Step 3: Reconcile explicit `PLAN / BUILD / REVIEW` wording as Work Mode, not macro stage**

- [ ] **Step 4: Avoid paths owned by pre-existing open PRs**

### Task 6: GREEN verification, adversarial review, merge/readback

**Files:**
- All files changed by Tasks 1–5.

**Interfaces:**
- Consumes: exact current-task PR heads.
- Produces: verified merged owner state and evidence ceiling.

- [ ] **Step 1: Run focused Base contracts and required CI at exact PR head**

- [ ] **Step 2: Compare current-task diff against latest main and recheck open-PR path overlap**

- [ ] **Step 3: Perform at least five full-scope adversarial loops**

Attack phase collapse, Grill Me over-questioning, asset-before-review leakage, Codex extra round trips, human-evidence overclaim, non-game over-application and project drift.

- [ ] **Step 4: Squash merge only with exact-head required checks and zero blockers**

- [ ] **Step 5: Read back new Base main and each changed project main/Notion destination**

- [ ] **Step 6: Report `BEFORE → AFTER → expected effect → remaining/unverified`**
