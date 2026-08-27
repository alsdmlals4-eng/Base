# Work 5단계 버티컬 슬라이스 Lifecycle Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Work 프로젝트 실행을 `기획 → 검수 → 이미지·요소 생성 → Codex 구현 → 사용자 검증`의 5단계 Gate로 명확히 분리하고, 사용자 검증 전에는 버티컬 슬라이스 완료나 다음 Slice 진입을 허용하지 않는다.

**Architecture:** 새 `WORK_FIVE_STAGE_VERTICAL_SLICE_LIFECYCLE.md`가 단계명·입출력·재진입·완료 상태만 소유한다. 기존 Startup Checklist, Grill Me, minimum-transition profile, local Visual, evidence identity, Codex, QA, Git/merge owner는 유지하고 Router/Profile/Starter가 새 owner를 progressive-load한다.

**Tech Stack:** Markdown policy/contract, Python `unittest`, GitHub Actions Base contract regression.

**Spec:** `docs/superpowers/specs/2026-08-27-work-five-stage-vertical-slice-lifecycle-design.md`

## Global Constraints

- Base latest completed main과 exact Project canon/actual implementation이 우선한다.
- 새 second canon·새 broad Skill·새 provider·새 dependency·새 비용을 만들지 않는다.
- Coc-Fiction 같은 non-game project에는 게임 product 5단계를 자동 강제하지 않는다.
- Stage 1의 핵심 제품 결정은 standing routine approval로 자동 승인하지 않는다.
- 현재 승인된 결정은 재질문하지 않고, unresolved/material core decision에만 Grill Me를 사용한다.
- Work→Codex 정상 전환은 Stage 3 뒤 한 번이다.
- Human/Player evidence는 실제 사용자 검증 전 `NOT_RUN`이다.
- direct main, force, blind reset/clean/rebase, ruleset/admin bypass 금지.

---

### Task 1: 5단계 계약 RED 테스트

**Files:**
- Create: `tests/test_work_five_stage_vertical_slice_lifecycle_contract.py`

**Interfaces:**
- Consumes: current Router/Profile/Starter/Grill Me/Vertical Slice owners.
- Produces: 신규 lifecycle owner와 routing이 없으면 의도적으로 실패하는 계약 테스트.

- [ ] **Step 1: Write the failing test**

```python
from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LIFECYCLE = ROOT / "templates/project-operations/WORK_FIVE_STAGE_VERTICAL_SLICE_LIFECYCLE.md"
ROUTER = ROOT / "templates/project-operations/WORK_PROJECT_EXECUTION_CURRENT_ROUTER.md"
PROFILE = ROOT / "templates/project-operations/WORK_CODEX_MINIMUM_TRANSITION_VERTICAL_SLICE_PROFILE.md"
STARTER = ROOT / "templates/project-operations/WORK_CODEX_MINIMUM_TRANSITION_LOCAL_VISUAL_STARTER_PROMPT.md"
GRILL = ROOT / "docs/PLANNING_FIRST_GRILL_ME_BATCH_POLICY.md"


class WorkFiveStageVerticalSliceLifecycleContractTests(unittest.TestCase):
    @staticmethod
    def _read(path: Path) -> str:
        if not path.exists():
            raise AssertionError(f"required contract file missing: {path}")
        return path.read_text(encoding="utf-8")

    def test_five_stages_are_explicit_and_ordered(self) -> None:
        text = self._read(LIFECYCLE)
        stages = (
            "STAGE_1_PLANNING_WITH_USER",
            "STAGE_2_PREPRODUCTION_REVIEW",
            "STAGE_3_GAME_INPUT_PRODUCTION",
            "STAGE_4_CODEX_IMPLEMENTATION_AND_MACHINE_CLOSEOUT",
            "STAGE_5_USER_VERTICAL_SLICE_VALIDATION",
        )
        positions = [text.index(stage) for stage in stages]
        self.assertEqual(positions, sorted(positions))

    def test_stage_one_requires_user_grill_me_and_benchmark_for_core_decisions(self) -> None:
        text = self._read(LIFECYCLE) + "\n" + self._read(GRILL)
        for token in (
            "CORE_PRODUCT_DECISIONS_REQUIRE_GRILL_ME_WHEN_UNRESOLVED",
            "ROUTINE_APPROVAL_DOES_NOT_AUTO_APPROVE_CORE_PLANNING",
            "BENCHMARK_BEFORE_MATERIAL_GRILL_ME",
            "player_promise",
            "pointed_fun",
            "meaningful_choice_and_tradeoff",
            "differentiation_and_sales_points",
            "MINIMUM_VIABLE_ALTERNATIVES: 3",
        ):
            self.assertIn(token, text)

    def test_review_is_separate_from_asset_production_and_codex(self) -> None:
        text = self._read(LIFECYCLE)
        for token in (
            "REVIEW_IS_NOT_ASSET_PRODUCTION",
            "REVIEW_IS_NOT_CODEX_IMPLEMENTATION",
            "STAGE_2_PREPRODUCTION_REVIEW_PACKET",
            "p0_blockers",
            "p1_blockers",
            "REOPEN_STAGE_1",
        ):
            self.assertIn(token, text)

    def test_stage_three_closes_all_work_owned_inputs_before_codex(self) -> None:
        text = self._read(LIFECYCLE)
        for token in (
            "WORK_PRODUCTION_INPUT_PACKET",
            "READY_FOR_SINGLE_CODEX_WINDOW",
            "blocking_missing_inputs",
            "actual_consumers",
            "provenance_rights_manifest",
        ):
            self.assertIn(token, text)

    def test_automated_ready_is_not_vertical_slice_complete(self) -> None:
        text = self._read(LIFECYCLE)
        self.assertIn("AUTOMATED_VERTICAL_SLICE_READY != VERTICAL_SLICE_COMPLETE", text)
        self.assertIn("VERTICAL_SLICE_COMPLETE_REQUIRES_USER_VALIDATION", text)
        self.assertIn("USER_VALIDATED_VERTICAL_SLICE", text)
        self.assertIn("NO_NEXT_SLICE_BEFORE_USER_DECISION_GATE", text)

    def test_stage_four_contains_codex_machine_qa_work_review_build_and_merge(self) -> None:
        text = self._read(LIFECYCLE)
        for token in (
            "CODEX_SINGLE_IMPLEMENTATION_WINDOW",
            "WORK_FINAL_EVIDENCE_REVIEW_INSIDE_STAGE_4",
            "runtime_and_screen_evidence",
            "build_export_package_evidence",
            "exact_ci_and_merge",
            "downloadable_build_locator",
        ):
            self.assertIn(token, text)

    def test_stage_five_routes_findings_back_to_the_correct_stage(self) -> None:
        text = self._read(LIFECYCLE)
        for token in (
            "fun/core/choice failure → Stage 1",
            "comprehension/spec failure → Stage 2",
            "Visual/Audio/input failure → Stage 3",
            "implementation defect → Stage 4",
        ):
            self.assertIn(token, text)

    def test_current_entrypoints_route_the_five_stage_owner(self) -> None:
        for path in (ROUTER, PROFILE, STARTER):
            self.assertIn("WORK_FIVE_STAGE_VERTICAL_SLICE_LIFECYCLE.md", self._read(path))

    def test_non_game_exception_and_evidence_ceiling_are_preserved(self) -> None:
        text = self._read(LIFECYCLE)
        for token in (
            "GAME_PRODUCT_FIVE_STAGE_LIFECYCLE_ONLY",
            "NON_GAME_PROJECT_REQUIRES_PROJECT_SPECIFIC_ADAPTER",
            "HUMAN_USABILITY_EVIDENCE: NOT_RUN",
            "PLAYER_EXPERIENCE_EVIDENCE: NOT_RUN",
        ):
            self.assertIn(token, text)
```

- [ ] **Step 2: Run the test to verify RED**

Run:

```bash
python -m unittest tests.test_work_five_stage_vertical_slice_lifecycle_contract -v
```

Expected: FAIL because `WORK_FIVE_STAGE_VERTICAL_SLICE_LIFECYCLE.md` and routing do not exist.

- [ ] **Step 3: Record RED evidence**

Record exact branch head and failing assertions in the PR body. Unrelated Base checks must not be reported as failures caused by the new behavior unless logs prove it.

- [ ] **Step 4: Commit**

```bash
git add tests/test_work_five_stage_vertical_slice_lifecycle_contract.py
git commit -m "test: require five-stage Work vertical slice lifecycle"
```

---

### Task 2: Add the five-stage lifecycle owner

**Files:**
- Create: `templates/project-operations/WORK_FIVE_STAGE_VERTICAL_SLICE_LIFECYCLE.md`
- Test: `tests/test_work_five_stage_vertical_slice_lifecycle_contract.py`

**Interfaces:**
- Consumes: Startup Checklist, Grill Me, minimum-transition, local Visual, evidence identity, vertical-slice Skill.
- Produces: exact five-stage state machine, packets, exit/reentry rules, two-level completion state.

- [ ] **Step 1: Implement the minimum owner**

Implement exactly the spec sections:

```text
STAGE_0_PREFLIGHT
STAGE_1_PLANNING_WITH_USER
STAGE_2_PREPRODUCTION_REVIEW
STAGE_3_GAME_INPUT_PRODUCTION
STAGE_4_CODEX_IMPLEMENTATION_AND_MACHINE_CLOSEOUT
STAGE_5_USER_VERTICAL_SLICE_VALIDATION
```

Include the exact packet schemas, stage exit conditions, reentry matrix, game-only applicability, and evidence ceiling from the spec.

- [ ] **Step 2: Run focused tests**

```bash
python -m unittest tests.test_work_five_stage_vertical_slice_lifecycle_contract -v
```

Expected: routing tests remain FAIL; lifecycle-content tests PASS.

- [ ] **Step 3: Commit**

```bash
git add templates/project-operations/WORK_FIVE_STAGE_VERTICAL_SLICE_LIFECYCLE.md
git commit -m "feat: add five-stage Work vertical slice lifecycle"
```

---

### Task 3: Route current owners and bind Grill Me

**Files:**
- Modify: `templates/project-operations/WORK_PROJECT_EXECUTION_CURRENT_ROUTER.md`
- Modify: `templates/project-operations/WORK_CODEX_MINIMUM_TRANSITION_VERTICAL_SLICE_PROFILE.md`
- Modify: `templates/project-operations/WORK_CODEX_MINIMUM_TRANSITION_LOCAL_VISUAL_STARTER_PROMPT.md`
- Modify: `docs/PLANNING_FIRST_GRILL_ME_BATCH_POLICY.md`
- Test: `tests/test_work_five_stage_vertical_slice_lifecycle_contract.py`

**Interfaces:**
- Consumes: lifecycle owner from Task 2.
- Produces: all current Work entrypoints load the same 5-stage owner; Stage 1 core decisions are exempt from routine auto-approval.

- [ ] **Step 1: Update the current router**

Add `WORK_FIVE_STAGE_VERTICAL_SLICE_LIFECYCLE.md` before detailed Stage owners and state:

```text
FIVE_STAGE_LIFECYCLE_IS_PUBLIC_WORK_SEQUENCE
EXISTING_WORK_MODES_AND_PROFILES_ARE_INTERNAL_OWNER_MAPPING
```

- [ ] **Step 2: Update the minimum-transition profile**

Keep current detailed procedures. Add the compatibility mapping:

```text
legacy Stage A = public Stage 1 + 2 + 3
legacy Stage B = public Stage 4 Codex execution
legacy Stage C = public Stage 4 Work closeout + Stage 5 entry
```

State that the new five-stage owner controls public stage identity and gate transitions.

- [ ] **Step 3: Update the copy-paste Starter**

Show the exact user-facing sequence:

```text
1 기획 · 사용자 공동설계
2 검수 · Preproduction Review
3 이미지·요소 생성
4 구현(Codex) + Machine Closeout
5 사용자 검증
```

Explicitly say:

```text
routine auto approval does not cover unresolved core planning
AUTOMATED_VERTICAL_SLICE_READY is not VERTICAL_SLICE_COMPLETE
```

- [ ] **Step 4: Bind Grill Me policy to Stage 1**

Add a section that routes unresolved core player promise/fun/system/meaningful choice/reward/failure/first impression/differentiation/sales-point/major UX/economy/story/Art Direction/scope decisions through benchmark-informed Grill Me before Stage 1 closes.

- [ ] **Step 5: Run focused tests**

```bash
python -m unittest tests.test_work_five_stage_vertical_slice_lifecycle_contract -v
```

Expected: PASS.

- [ ] **Step 6: Run existing related contract tests**

```bash
python -m unittest \
  tests.test_work_project_start_canon_checklist_contract \
  tests.test_work_codex_minimum_transition_automation_contract \
  tests.test_work_local_visual_asset_delivery_contract \
  tests.test_work_instruction_superset_reconciliation_contract \
  tests.test_work_final_starter_router_contract -v
```

Expected: PASS without weakening existing contracts.

- [ ] **Step 7: Commit**

```bash
git add \
  templates/project-operations/WORK_PROJECT_EXECUTION_CURRENT_ROUTER.md \
  templates/project-operations/WORK_CODEX_MINIMUM_TRANSITION_VERTICAL_SLICE_PROFILE.md \
  templates/project-operations/WORK_CODEX_MINIMUM_TRANSITION_LOCAL_VISUAL_STARTER_PROMPT.md \
  docs/PLANNING_FIRST_GRILL_ME_BATCH_POLICY.md
git commit -m "fix: route Work through five explicit vertical slice stages"
```

---

### Task 4: Project/Notion compatibility and non-regression audit

**Files:**
- Modify only if a validated current-owner omission is found.
- Record evidence in PR body; do not mass-edit project repositories or Notion.

**Interfaces:**
- Consumes: all active project root AGENTS and representative Notion Home/Production/Vertical Slice pages.
- Produces: proof that the generic owner does not overwrite project-specific stage names, evidence gates, or non-game lifecycle.

- [ ] **Step 1: Re-read active project authority**

Inspect root/current authority for:

```text
GRIMOIRE, MylittleBoat, Switchy Express, Omenward, Tetris,
Ninja Survival, Ten Paces Hidden Moves, Blacksmith, urban-legend, Coc-Fiction
```

- [ ] **Step 2: Re-read representative Notion surfaces**

Inspect Home/Production/Vertical Slice pages that show planning completion, Visual/UX review, implementation and Human validation boundaries.

- [ ] **Step 3: Verify compatibility**

Confirm:

- current Project canon still wins;
- already-approved core decisions are not reopened;
- project-specific tester counts/platform gates remain stronger when present;
- non-game projects are not forced into Godot/Codex lifecycle;
- Notion remains human-facing summary, not a new duplicated stage canon.

- [ ] **Step 4: Record benchmark disposition**

Record external findings:

- vertical slice is a functioning representative portion of the larger game;
- milestone quality must be agreed before production;
- over-polished vertical slice must not consume planning capacity;
- usability testing is a separate evidence activity, not inferred from implementation;
- a playable Godot export includes executable + project data; PCK/ZIP alone is not a runnable build.

---

### Task 5: Exact-head verification, adversarial review and closeout

**Files:**
- Update PR body only.
- Generate final user artifact after merge.

**Interfaces:**
- Consumes: final branch state.
- Produces: merged Base owner, post-merge readback, one downloadable Work instruction.

- [ ] **Step 1: Run full Base validation**

Observe the repository's current required workflows on exact head. At minimum confirm docs, syntax/governance, core regression, publication validation and final required gate.

- [ ] **Step 2: Perform five complete adversarial loops**

Each loop must recheck the entire state:

1. authority, user intent, historical non-regression, project compatibility;
2. Stage 1 Grill Me/benchmark and auto-approval boundary;
3. Stage 2/3 separation, Visual/Audio consumer, rights and Work→Codex transition;
4. Stage 4 implementation/QA/build/merge and `AUTOMATED_READY` evidence ceiling;
5. Stage 5 actual user validation, reentry routing, non-game exception and next-Slice prohibition.

Fix validated findings and restart whole-state review lineage when required.

- [ ] **Step 3: Verify PR gates**

```text
latest main reconciliation
→ exact reviewed HEAD
→ required checks PASS
→ unresolved thread 0
→ conflict 0
→ protected-scope drift 0
→ squash merge
```

- [ ] **Step 4: Post-merge readback**

Verify new main SHA, lifecycle owner, Router/Profile/Starter routing and post-merge workflows.

- [ ] **Step 5: Generate one final artifact**

Create:

```text
/mnt/data/WORK_PROJECT_FIVE_STAGE_VERTICAL_SLICE_FINAL_INSTRUCTION.md
```

The file must be the single copy-paste Work instruction and must match merged Base current owner. Include `[프로젝트명]` replacement guidance, five stage names, Stage 1 Grill Me boundary, Stage 4/5 completion distinction and local Visual path.
