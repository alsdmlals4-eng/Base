# Planning-First Grill Me Batch Governance Implementation Plan

> **For agentic workers:** Use `superpowers:executing-plans` or `superpowers:subagent-driven-development` and verify every checked step with current evidence.

**Goal:** Enforce planning-first execution, GPT-recommended reversible numeric defaults, Grill Me approval for planning conflicts, and maximum-ten-decision PR checkpoints with exact-head adversarial validation.

**Architecture:** Keep `AGENTS.md` as the always-on authority and add one detailed canonical policy, `docs/PLANNING_FIRST_GRILL_ME_BATCH_POLICY.md`. Avoid copying the whole state machine into every operating document. Provide one execution Template and two regressions: an existing CI-discovered Deep Interview test and a focused complete-policy test. Preserve Registry and v9.4.1 release-lock bytes.

**Tech Stack:** Markdown contracts, Python `unittest`, existing Base GitHub Actions.

## Global Constraints

- `L1` 이상 작업은 `PLAN → approved contract → BUILD → REVIEW` 순서를 기본으로 한다.
- 상세 데이터·초기 수치는 가역적이고 프로젝트 방향을 바꾸지 않을 때만 `DETAILED_NUMERIC_DEFAULT` / `RECOMMENDED_DEFAULT`다.
- 기획 충돌은 `PLANNING_CONFLICT` / `USER_DECISION_REQUIRED` / `GRILL_ME_REQUIRED`로 처리한다.
- 승인 Decision은 즉시 활성 배치 Branch 정본과 GitHub 추적 surface에 기록한다.
- 한 배치의 승인 Decision 상한은 10건이다. 고위험·정본 충돌·세션 종료·구현 차단 시 조기 체크포인트를 허용한다.
- 10번째 승인 후 배치 병합·재동기화 전 11번째 질문을 금지한다.
- 병합은 latest exact-head checks, 적대적 검토, unresolved thread 0, P0/P1 0 후 수행한다.
- Registry, released lock, frozen release artifacts는 변경하지 않는다.

---

### Task 1: Establish RED coverage

**Files:**
- Create: `tests/test_planning_first_grillme_batch_governance.py`
- Modify: `tests/test_deep_interview_contract.py`

- [x] Add a focused contract test for planning-first authority, decision classification, max-ten batching, early checkpoints, immediate Branch recording, exact-head review, and merged-main Sheet finalization.
- [x] Connect the same minimum contract to the existing Deep Interview suite executed by Base contract CI.
- [x] Verify RED on PR #142: all existing contract tests passed except the new planning-first batch assertion.

### Task 2: Add always-on authority and one detailed policy

**Files:**
- Modify: `AGENTS.md`
- Create: `docs/PLANNING_FIRST_GRILL_ME_BATCH_POLICY.md`

- [x] Add `기획 우선 원칙` before BUILD authority in `AGENTS.md`.
- [x] Route detailed mechanics to one canonical policy instead of duplicating them across long operating documents.
- [x] Define `DETAILED_NUMERIC_DEFAULT` / `RECOMMENDED_DEFAULT` and `PLANNING_CONFLICT` / `GRILL_ME_REQUIRED` boundaries.
- [x] Reconcile immediate approval recording with PR-gated main synchronization.
- [x] Define `MAX_APPROVED_DECISIONS_PER_BATCH: 10` as a maximum, not a minimum.
- [x] Define early checkpoints and the eleventh-question stop rule.
- [x] Define exact-head checks and `attack → validate-critique → regression-recheck → decision-report` before merge.

### Task 3: Add the execution checkpoint Template

**Files:**
- Create: `templates/project-operations/GRILL_ME_BATCH_CHECKPOINT.md`

- [x] Add batch identity, approval count, checkpoint reason, PR exact HEAD, required-check result, adversarial result, unresolved/P0-P1 counts, merge SHA, and Sheet states.
- [x] Add planning-first, numeric-default, immediate-recording, adversarial-review, merge, and post-merge readback checklists.
- [x] Keep actual project batch execution, external-model behavior, and human usability evidence separate and defaulted to `NOT_RUN`.

### Task 4: Align design and executable regressions

**Files:**
- Modify: `docs/superpowers/specs/2026-08-02-planning-first-grillme-batch-governance-design.md`
- Modify: `docs/superpowers/plans/2026-08-02-planning-first-grillme-batch-governance.md`
- Modify: `tests/test_planning_first_grillme_batch_governance.py`
- Modify: `tests/test_deep_interview_contract.py`

- [x] Align the design with the single-policy authority model.
- [x] Update the focused test to inspect `AGENTS.md`, the canonical policy, and the checkpoint Template.
- [x] Update the existing CI regression to discover and validate the same surfaces.
- [ ] Run exact-head CI and repair only evidence-backed failures.

### Task 5: Adversarial review and completion

- [ ] Confirm no temporary Workflow remains in the final diff.
- [ ] Confirm Registry and v9.4.1 lock bytes remain unchanged.
- [ ] Attack waterfall risk, hidden planning conflicts, oversized batches, lost approvals, premature Sheet sync, duplicate active PRs, manufactured opposition, and stale exact-head evidence.
- [ ] Verify PR changed files and unresolved review threads.
- [ ] Require the canonical `ci-gate` and all selected checks to succeed on the final PR HEAD.
- [ ] Record real multi-project Grill Me batch execution and human usability as `NOT_RUN` until a project Pilot.
