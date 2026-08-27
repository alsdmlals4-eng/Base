# Visual Concept Exploration and Continuity Lock Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 중요한 Visual Direction을 여러 통제된 후보로 탐색·사용자 선택·정본 잠금한 뒤 후속 이미지와 runtime 화면이 같은 시각 문법을 유지하도록 Base 계약을 연결한다.

**Architecture:** 기존 Art Direction Guide, image policy, conversation approval, candidate review, continuity gate, local Visual delivery를 그대로 상세 owner로 두고 하나의 얇은 composed contract가 `explore → select → lock → scale → runtime consistency` 전이를 소유한다. Project-specific Art Bible/Flow/Asset은 각 프로젝트 정본에 남으며 Base는 필드와 Gate만 제공한다.

**Tech Stack:** Markdown contracts, Python `unittest`, GitHub Actions, current Base partition/governance contracts.

**Spec:** `[수정제안서]/BCP-2026-043-visual-concept-exploration-and-continuity-lock/PROPOSAL.md`

## Global Constraints

- `THIN_CONTRACT_NOT_SECOND_ART_BIBLE`.
- `MINIMUM_VIABLE_CONCEPT_DIRECTIONS: 3`은 실질 대안이 있을 때만 적용하고 허수 후보를 금지한다.
- 비교 board는 한 exploration 결과이며 여러 independent runtime asset 납품을 대체하지 않는다.
- existing `TEXT_BRIEF_STOP_REQUIRED → NEXT_USER_EXPLICIT_APPROVAL → GENERATE_EXACTLY_ONE`을 유지한다.
- current approved Visual Direction이 유효하면 bounded asset마다 exploration을 반복하지 않는다.
- Project-native Art Bible, Flow/Screen, Decision, asset state를 Base에 복제하지 않는다.
- 이미지 생성, 프로젝트 Notion/제품 코드, 엔진·의존성·비용·공개 배포는 이번 범위가 아니다.
- 모든 pre-existing open PR은 read-only다.
- `PROPOSAL_REGISTRY.json`은 PR #678 ownership 때문에 수정하지 않는다.

---

### Task 1: RED contract and partition-topology normalization

**Files:**
- Create: `tests/test_visual_concept_exploration_lock.py`
- Remove historical branch-only path: `tests/test_visual_concept_exploration_and_continuity_lock.py`

**Interfaces:**
- Consumes: current Art Direction/Image/Continuity/Local Visual owner text.
- Produces: exact token/order/state/routing regression contract.

- [x] **Step 1: Write the failing behavior contract**

Require the composed owner, route, controlled concept options, selection/lock packets, comparison-board boundary, existing local packet mapping, state separation and bounded drift reopen.

- [x] **Step 2: Run exact RED in GitHub Actions**

Expected: Base v9 and unrelated validation remain green; whole core regression fails because the composed owner and route do not exist.

- [x] **Step 3: Diagnose partition-manifest overlap**

Observed: the original filename matched both P01 `tests/test_*continuity*.py` and P05 `tests/test_*visual*.py`.

- [x] **Step 4: Normalize the test path to P05**

Use `tests/test_visual_concept_exploration_lock.py`; do not alter the protected partition manifest for a filename-only collision.

---

### Task 2: Add the thin composed Visual contract

**Files:**
- Create: `docs/knowledge/game-development/VISUAL_CONCEPT_EXPLORATION_AND_CONTINUITY_LOCK.md`
- Test: `tests/test_visual_concept_exploration_lock.py`

**Interfaces:**
- Consumes: current Project canon, actual consumer, Art Direction Concept Exploration, Image Conversation Approval Gate, candidate review and local Visual packet.
- Produces: `CONCEPT_DIRECTION_SELECTION`, `APPROVED_VISUAL_DIRECTION_PACKET`, consistency acceptance and drift reopen rules.

- [ ] **Step 1: Define trigger and skip conditions**

Trigger on new/material/unresolved Visual Direction; reuse a current approved lock when scope and assumptions have not changed.

- [ ] **Step 2: Define controlled option generation**

Require valid real directions, controlled comparison axes, same consumer conditions where possible, candidate IDs and explicit trade-offs.

- [ ] **Step 3: Define explicit comparison-board semantics**

One explicitly briefed board may be one exploration result under the existing generation gate. State that it is not multiple runtime deliverables, product approval or runtime evidence.

- [ ] **Step 4: Define selection and direction-lock packets**

Record selected/adopted/rejected elements, mood/style/palette/light/camera, confirmed Flow/Screen anchors, Keep/Avoid/Do Not Drift and allowed variation.

- [ ] **Step 5: Map the lock to existing local Visual delivery fields**

Specify how the lock populates `approved_reference_or_style_anchor`, `notion_reference_surface`, `objective_acceptance` and `runtime_validation` without changing that packet schema.

- [ ] **Step 6: Define runtime consistency and bounded drift reopen**

Validate target-size/runtime integration, preserve deliberate variation, and reopen the earliest affected visual scope rather than the whole project.

---

### Task 3: Route project visual continuity through the composed contract

**Files:**
- Modify: `skills/designing-art-prompts-and-technique-cards/references/notion-project-visual-continuity-gate.md`
- Test: `tests/test_visual_concept_exploration_lock.py`

**Interfaces:**
- Consumes: material Visual Direction state from Project canon.
- Produces: conditional route to the new contract and approved direction packet before ordinary Keep/Avoid/Do Not Drift production.

- [ ] **Step 1: Add a conditional exploration route**

Load the composed contract only when direction is new, missing, conflicting or materially changed.

- [ ] **Step 2: Preserve valid approved anchors**

State that bounded follow-up asset work reuses the current lock without re-running concept exploration.

- [ ] **Step 3: Preserve existing conversation and candidate lifecycle gates**

Do not weaken text-brief approval, one-result generation, candidate selection, Notion readback or product/runtime promotion boundaries.

---

### Task 4: Record the project-neutral problem/lesson case

**Files:**
- Create: `docs/knowledge/cases/VISUAL_CONCEPT_EXPLORATION_AND_CONTINUITY_LOCK_CASE.md`

**Interfaces:**
- Consumes: user-provided comparison-board examples and current Base owner audit.
- Produces: reusable rationale, anti-patterns and evidence ceiling without storing project-specific image bytes.

- [ ] **Step 1: Describe the two supported comparison patterns**

Record same-surface environment/mood comparison and pixel-style-family comparison as process evidence.

- [ ] **Step 2: Capture the main anti-patterns**

Include final-first production, fake alternatives, confounded comparisons, board-as-runtime compression, rigid sameness and stale lock propagation.

- [ ] **Step 3: Record why the selected architecture reuses current owners**

Explain why a thin transition contract is safer than duplicating the Art Bible/image policy.

---

### Task 5: GREEN verification and safe closeout

**Files:**
- All current-task changed paths.

**Interfaces:**
- Consumes: exact current-task PR head.
- Produces: verified merged Base main or an explicit blocker receipt.

- [ ] **Step 1: Run focused/core/Base required workflows at exact head**

Required: Base v9 PASS; docs PASS; Ubuntu contract PASS; publication PASS; whole core regression PASS; final `ci-gate` PASS.

- [ ] **Step 2: Reconcile latest main and open PR paths**

Confirm branch not behind current main and exact path overlap 0 with pre-existing PRs, especially #713, #748 and #678.

- [ ] **Step 3: Perform five full-scope adversarial loops**

Attack fake/confounded options, runtime-deliverable compression, approval/evidence conflation, rigid sameness versus uncontrolled drift, stale Flow/direction and project-wide restart.

- [ ] **Step 4: Verify review and merge gates**

Require mergeable state, unresolved thread 0, blocker 0 and exact-head checks.

- [ ] **Step 5: Squash merge with expected head and post-merge readback**

Read back new main, new contract, continuity route, case and regression test. Do not claim project/runtime/Human PASS.
