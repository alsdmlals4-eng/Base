# Planning-First Grill Me Batch Governance Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Enforce planning-first execution, GPT-recommended reversible numeric defaults, Grill Me approval for planning conflicts, and maximum-ten-decision PR checkpoints with exact-head adversarial validation.

**Architecture:** Keep `managing-project-intake-and-work-contract` as the single intake owner. Extend its Grill Me reference, the confirmed-decision sync policy, the GitHub work-item lifecycle, and the decision-record template with one shared batch state machine. Add one focused contract test and connect the existing deep-interview and neutral-adversarial regressions without changing Registry or release-lock bytes.

**Tech Stack:** Markdown contracts, Python `unittest`, GitHub Actions existing Base contract workflow.

## Global Constraints

- L1 이상 작업은 `PLAN → approved contract → BUILD → REVIEW` 순서를 기본으로 한다.
- 상세 데이터·초기 수치는 가역적이고 프로젝트 방향을 바꾸지 않을 때만 `RECOMMENDED_DEFAULT`다.
- 기획 충돌은 `USER_DECISION_REQUIRED`이며 Grill Me 한 질문·한 승인으로 처리한다.
- 승인 Decision은 즉시 활성 배치 Branch 정본과 추적 surface에 기록한다.
- 한 배치의 승인 Decision 상한은 10건이다. 고위험·정본 충돌·세션 종료·구현 차단 시 조기 체크포인트를 허용한다.
- 10번째 승인 후 배치 병합·재동기화 전 11번째 질문을 금지한다.
- 병합은 exact-head checks, 적대적 검토, unresolved thread 0, P0/P1 0 후 수행한다.
- Registry, released lock, frozen release artifacts는 변경하지 않는다.

---

### Task 1: Add the failing governance contract test

**Files:**
- Create: `tests/test_planning_first_grillme_batch_governance.py`

**Interfaces:**
- Consumes: canonical Markdown contracts and the Grill Me decision template.
- Produces: one focused executable contract that fails until every required surface is synchronized.

- [ ] **Step 1: Write the failing test**

Create tests that require:

- `기획 우선 원칙` and PLAN-before-BUILD language in `AGENTS.md`, `docs/OPERATING_MODEL.md`, and `docs/WORK_MODE_AND_SKILL_ROUTING.md`;
- `RECOMMENDED_DEFAULT` for reversible detailed numeric defaults and `USER_DECISION_REQUIRED` for planning conflicts;
- `MAX_APPROVED_DECISIONS_PER_BATCH: 10`, early checkpoint reasons, and an explicit ban on an eleventh question before merge;
- branch-first immediate recording, `APPROVED_PENDING_MERGE`, batch PR exact-head checks, adversarial review, and `SYNCED_TO_MAIN` after merge;
- batch fields in `templates/project-operations/GRILL_ME_DECISION_RECORD.md`;
- unchanged Registry and v9.4.1 release-lock identity.

- [ ] **Step 2: Run the focused test and verify RED**

Run:

```bash
python -m unittest tests.test_planning_first_grillme_batch_governance -v
```

Expected: FAIL because the new planning-first and batch-state terms are absent.

- [ ] **Step 3: Commit the RED test**

```bash
git add tests/test_planning_first_grillme_batch_governance.py
git commit -m "test: define planning-first Grill Me batch governance"
```

### Task 2: Add planning-first and decision-classification authority

**Files:**
- Modify: `AGENTS.md`
- Modify: `docs/OPERATING_MODEL.md`
- Modify: `docs/WORK_MODE_AND_SKILL_ROUTING.md`
- Modify: `skills/managing-project-intake-and-work-contract/SKILL.md`

**Interfaces:**
- Consumes: existing PLAN / BUILD / REVIEW and neutral recommendation gate.
- Produces: a single authority rule for planning-first execution and the numeric-default/planning-conflict boundary.

- [ ] **Step 1: Add the minimum contract language**

Add:

```text
기획 우선 원칙
→ L1 이상은 PLAN에서 정본·대안·충돌·완료 기준·검증·롤백을 닫는다.
→ 사용자 승인 또는 기존 승인 계약 없이 BUILD에 진입하지 않는다.
→ 가역적 상세 수치·초기 데이터는 RECOMMENDED_DEFAULT로 기록한다.
→ 프로젝트 방향을 바꾸는 수치·분야 정본 충돌은 USER_DECISION_REQUIRED로 Grill Me 승인 후 확정한다.
```

Preserve L0 mechanical exceptions and existing neutral/adversarial gates.

- [ ] **Step 2: Run the focused test**

Expected: remaining failures only for batch lifecycle and template fields.

- [ ] **Step 3: Commit**

```bash
git add AGENTS.md docs/OPERATING_MODEL.md docs/WORK_MODE_AND_SKILL_ROUTING.md skills/managing-project-intake-and-work-contract/SKILL.md
git commit -m "docs: enforce planning-first decision boundaries"
```

### Task 3: Implement the maximum-ten-decision Grill Me batch lifecycle

**Files:**
- Modify: `skills/managing-project-intake-and-work-contract/references/grill-me-protocol.md`
- Modify: `docs/CONFIRMED_DECISION_SYNC_POLICY.md`
- Modify: `docs/GITHUB_WORK_ITEM_LIFECYCLE_POLICY.md`
- Modify: `templates/project-operations/GRILL_ME_DECISION_RECORD.md`

**Interfaces:**
- Consumes: approved Decision IDs, active Goal/Issue, canonical documents, project Sheet configuration.
- Produces: `GM-BATCH-*` lifecycle with branch commits, PR checks, adversarial review, merge SHA, and Sheet finalization.

- [ ] **Step 1: Define the batch identity and states**

Use:

```yaml
grill_me_batch_id: GM-BATCH-YYYY-MM-DD-NN
max_approved_decisions_per_batch: 10
approved_decision_count: 0
checkpoint_reason: TEN_APPROVALS | HIGH_IMPACT | CANON_CONFLICT | IMPLEMENTATION_BLOCKED | SESSION_END | USER_REQUEST | DIFF_SIZE
status: COLLECTING | CHECKPOINT_REQUIRED | PR_OPEN | CHECKS_RUNNING | REVIEW_REQUIRED | MERGED | SYNCED_TO_MAIN | BLOCKED
```

- [ ] **Step 2: Reconcile immediate sync with PR batching**

After each approval:

1. record the answer and Decision ID on the active GitHub tracking surface;
2. update canonical documents on the active batch branch;
3. create one logical Decision commit;
4. update the Sheet row as `APPROVED_PENDING_MERGE` when configured;
5. do not claim main synchronization.

At checkpoint:

1. open or update the one active Goal batch PR;
2. run required checks on the latest exact HEAD;
3. run `attack → validate-critique → regression-recheck → decision-report`;
4. require unresolved thread 0 and P0/P1 0;
5. squash merge;
6. re-read merged main and update Sheet rows to `SYNCED_TO_MAIN` with the merge SHA.

- [ ] **Step 3: Add stop rules**

- Stop before the eleventh question until the ten-decision batch is merged and synchronized.
- Close a partial batch at interview/session end.
- Trigger an early checkpoint for any listed high-impact condition.
- Do not store approvals only in chat memory.

- [ ] **Step 4: Update the decision-record template**

Add batch ID, approved count, checkpoint reason, PR number/HEAD, required-check result, adversarial result, merge SHA, and Sheet status fields.

- [ ] **Step 5: Run the focused test**

Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add skills/managing-project-intake-and-work-contract/references/grill-me-protocol.md docs/CONFIRMED_DECISION_SYNC_POLICY.md docs/GITHUB_WORK_ITEM_LIFECYCLE_POLICY.md templates/project-operations/GRILL_ME_DECISION_RECORD.md
git commit -m "docs: add Grill Me decision batch checkpoints"
```

### Task 4: Synchronize learning evidence and regressions

**Files:**
- Modify: `skills/SKILL_LEARNING_LOG.md`
- Modify: `tests/test_deep_interview_contract.py`
- Modify: `tests/test_neutral_adversarial_feature_lifecycle.py`

**Interfaces:**
- Consumes: new governance contract.
- Produces: focused learning record and protection against future contract drift.

- [ ] **Step 1: Add a Learning Log entry**

Record:

- problem: per-decision direct-main sync conflicts with PR-gated ten-decision checkpoints;
- resolution: immediate branch canonicalization plus max-ten batch PR and merged-main Sheet finalization;
- rejected alternative: waiting for exactly ten decisions before any durable record;
- evidence limit: real multi-project Grill Me batch execution remains `NOT_RUN` until piloted.

- [ ] **Step 2: Extend existing regressions**

Require the deep-interview test to discover the maximum-ten batch and planning-conflict boundary. Require the neutral-adversarial test to confirm exact-head adversarial review before batch merge.

- [ ] **Step 3: Run focused regressions**

```bash
python -m unittest \
  tests.test_planning_first_grillme_batch_governance \
  tests.test_deep_interview_contract \
  tests.test_neutral_adversarial_feature_lifecycle \
  -v
```

Expected: PASS.

- [ ] **Step 4: Commit**

```bash
git add skills/SKILL_LEARNING_LOG.md tests/test_deep_interview_contract.py tests/test_neutral_adversarial_feature_lifecycle.py
git commit -m "test: preserve planning-first Grill Me batch contract"
```

### Task 5: Run full verification and adversarial review

**Files:**
- Verify all changed files.

**Interfaces:**
- Consumes: complete branch.
- Produces: exact-head evidence and merge recommendation.

- [ ] **Step 1: Run local validation**

```bash
python tools/run_local_validation.py --trusted-history-commit 79cae496b89eb519d93b1430ceb0caa13ac77d8b
```

- [ ] **Step 2: Run reference freshness**

```bash
python tools/check_canonical_reference_freshness.py \
  --config .github/reference-freshness.json \
  --base 79cae496b89eb519d93b1430ceb0caa13ac77d8b \
  --head HEAD
```

- [ ] **Step 3: Perform adversarial review**

Attack:

- planning-first becoming waterfall or blocking harmless L0 work;
- GPT defaults silently changing project direction;
- ten-decision batches becoming large unreviewable PRs;
- approvals being lost before merge;
- Sheet claiming main sync before merge;
- eleventh question proceeding after a blocked batch;
- same Goal creating multiple active decision PRs.

- [ ] **Step 4: Verify exact-head GitHub Actions**

Require the canonical `ci-gate` and all checks selected by the change classifier to succeed on the final PR HEAD.

- [ ] **Step 5: Record evidence and keep limitations explicit**

Real project batch execution, external-model behavior, and human process usability remain `NOT_RUN` unless separately piloted.
