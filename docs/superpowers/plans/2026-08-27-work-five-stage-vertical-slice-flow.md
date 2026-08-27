# Work Five-Stage Vertical Slice Flow Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Work 게임 프로젝트 실행을 `기획 → 검수 → 이미지·요소 생성 → Codex 구현 → 사용자 검증` 5단계 macro flow로 정렬하고, 사람 검증 전 자동 readiness와 최종 버티컬 슬라이스 완료를 분리한다.

**Architecture:** 5단계 macro 의미는 current Router + minimum-transition profile이 소유한다. Planning/Grill Me, startup checklist, vertical-slice skill, image policy 등 기존 전문 owner는 **수정·복제하지 않고 조합**한다. 프로젝트별 `PLAN / BUILD / REVIEW`는 Work Mode로 해석하고, 현재 stage·Core·Decision·asset/implementation 상태는 Project canon이 계속 소유한다.

**Tech Stack:** Markdown contracts, Python `unittest` contract tests, GitHub Actions, current Base/project/Notion canon.

**Spec:** `docs/superpowers/specs/2026-08-27-work-five-stage-vertical-slice-flow-design.md`

## Global Constraints

- current Base owner를 두 번째 정본으로 복제하지 않는다.
- `CODEX_SINGLE_IMPLEMENTATION_WINDOW`와 Work↔Codex 최소 왕복을 유지한다.
- `AUTOMATED_VERTICAL_SLICE_READY != VERTICAL_SLICE_VALIDATED_COMPLETE`를 명시한다.
- Stage 5 actual user play 전 Human/Player PASS를 주장하지 않는다.
- 새/변경 core Slice planning은 material user Decision에 Grill Me + decision-relevant benchmark를 사용한다.
- actual consumer 없는 production image/element를 만들지 않는다.
- Base/open Project PR의 changed path를 takeover하지 않는다.
- 비게임 프로젝트에는 Godot/Codex five-stage flow를 강제하지 않는다.

---

### Task 1: RED contract for the five macro stages

**Files:**
- Create: `tests/test_work_five_stage_vertical_slice_flow_contract.py`
- Modify: `tests/test_work_codex_minimum_transition_automation_contract.py`

- [x] **Step 1: Write the failing contract tests**

Five stage order, collaborative planning routing, Stage 2 clean gate, Stage 3 actual consumer, Stage 4 Work review before Stage 5, and validated completion boundary를 테스트한다.

- [x] **Step 2: Run exact RED in GitHub Actions**

Exact test-only/contract head에서 Game Project Operating System core-regression 실패를 확인한다.

- [x] **Step 3: Verify RED is caused by missing five-stage owner behavior**

Diagnostics artifact에서 12 failures가 five-stage/validated-completion 요구에 집중됨을 확인한다.

### Task 2: Align Base current Router and minimum-transition profile

**Files:**
- Modify: `templates/project-operations/WORK_PROJECT_EXECUTION_CURRENT_ROUTER.md`
- Modify: `templates/project-operations/WORK_CODEX_MINIMUM_TRANSITION_VERTICAL_SLICE_PROFILE.md`
- Test: `tests/test_work_five_stage_vertical_slice_flow_contract.py`
- Test: `tests/test_work_codex_minimum_transition_automation_contract.py`

- [x] **Step 1: Replace the three-stage macro interpretation with five explicit macro stages**

Compatibility vocabulary는 유지하고 minimum-transition은 Work↔Codex round-trip 최소화이지 macro stage 수 축소가 아니라고 명시한다.

- [x] **Step 2: Put Work final evidence review inside Stage 4 closeout**

Codex product implementation 뒤, Stage 5 actual user validation 전에 둔다.

- [x] **Step 3: Add validated completion boundary**

`AUTOMATED_VERTICAL_SLICE_READY != VERTICAL_SLICE_VALIDATED_COMPLETE`, `ACTUAL_USER_PLAY_REQUIRED`, `NEXT_SLICE_REQUIRES_STAGE5_DECISION`을 고정한다.

- [x] **Step 4: Preserve thin-router architecture**

Router에 5단계 요약만 남기고 상세 Gate는 profile로 위임한다. Existing contract의 `<180 lines`를 유지하도록 한다.

### Task 3: Compose existing specialist owners instead of duplicating them

**Files:**
- Read/compose: `docs/PLANNING_FIRST_GRILL_ME_BATCH_POLICY.md`
- Read/compose: `skills/managing-project-intake-and-work-contract/references/grill-me-protocol.md`
- Read/compose: `templates/project-operations/WORK_PROJECT_START_CANON_CHECKLIST.md`
- Read/compose: `skills/designing-vertical-slices/SKILL.md`
- Modify only Router/Profile links and contract tests.

- [x] **Step 1: Route Stage 1 collaborative core planning to current Grill Me owners**

Still-unapproved material player-promise/choice/reward/emotion/sales-point/Slice-acceptance decisions만 사용자와 닫고, known facts/implementation details를 다시 묻지 않는다.

- [x] **Step 2: Require decision-relevant three-approach benchmark in the macro owner**

Current project/reuse first + `ADOPT / ADAPT / REJECT`를 적용한다.

- [x] **Step 3: Reuse startup receipt current stage and active Slice fields**

새 `macro_stage` 정본을 중복 저장하지 않고 `PROJECT_SPECIFIC_STAGE_STATE = RESOLVE_FROM_CURRENT_PROJECT_CANON`으로 해석한다.

- [x] **Step 4: Reuse vertical-slice skill as human play/decision evidence owner**

Existing shipping-intent quality, playtest, rights, accessibility, performance, `EXPAND / REWORK / REPEAT_SLICE / HOLD / STOP` semantics를 복제하지 않는다.

### Task 4: Project/Notion canon reconciliation

**Inputs:** active game Project AGENTS/current main/open PR + Project Notion Home/Production/Handoff.

- [x] **Step 1: Fresh-read representative/current project authorities**

MylittleBoat, urban-legend, ninja-survival, omenward, Ten-Paces, Blacksmith, GRIMOIRE, Switchy, Tetris와 non-game Coc-Fiction을 대조한다.

- [x] **Step 2: Classify project-local wording**

`PLAN / BUILD / REVIEW`는 Work Mode/inner execution으로 분류하고 공용 5단계 macro flow와 분리한다. `Coc-Fiction`은 `NON_GAME_PROJECT_NOT_APPLICABLE`이다.

- [x] **Step 3: Preserve project-local current state**

GRIMOIRE/Tetris/기타 current Notion의 automated/machine readiness와 Human/Player `NOT_RUN` 같은 state는 Project canon이 계속 소유한다.

- [x] **Step 4: Avoid unnecessary project writes**

Shared workflow를 Project AGENTS/Notion에 복제하지 않는다. 특히 open PR이 AGENTS를 소유하는 urban/Ten-Paces 등은 read-only로 유지한다. Shared correction은 Base current owner에만 둔다.

### Task 5: GREEN verification and collision review

- [x] **Step 1: Run initial GREEN candidate full core regression**

5단계 관련 failures는 제거됐고, Router 205 lines가 기존 thin-router `<180` 계약을 위반하는 단일 failure로 축소됨을 diagnostics에서 확인한다.

- [x] **Step 2: Correct only the observed thin-router regression**

상세 설명을 profile로 이동하고 Router를 다시 축약한다.

- [x] **Step 3: Recheck Base open PR changed paths**

Current-task changed paths가 pre-existing Base open PR changed paths와 겹치지 않는지 확인한다.

- [ ] **Step 4: Run fresh exact-head full verification**

Base v9 contracts + Game Project Operating System full core regression/publication/docs checks를 exact final head에서 확인한다.

### Task 6: adversarial review, merge, post-merge readback

- [ ] **Step 1: Perform at least five full-scope adversarial loops**

Attack:
1. planning/review phase collapse
2. Grill Me over-questioning or user bypass
3. asset-before-review / consumerless asset leakage
4. Codex extra round trips or Work product mutation leakage
5. automated-ready/human-evidence overclaim
6. non-game over-application / project state duplication
7. open-PR takeover / owner drift

- [ ] **Step 2: Reconcile final head against latest Base main**

Behind/diverged/new overlapping owner change가 있으면 re-evaluate before merge.

- [ ] **Step 3: Squash merge only with exact-head required checks and zero blockers**

- [ ] **Step 4: Read back new Base main**

Router/Profile/final tests가 merged main에 존재하는지 확인한다.

- [ ] **Step 5: Report `BEFORE → AFTER → expected effect → remaining/unverified`**
