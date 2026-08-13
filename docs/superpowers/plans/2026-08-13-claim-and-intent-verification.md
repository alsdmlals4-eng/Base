# Claim and Intent Verification Gate — Implementation Plan

> Proposal: `BCP-2026-027-claim-and-intent-verification-gate`  
> Owner: `reviewing-and-validating-project-changes`  
> Work Mode: `REVIEW`  
> Integration: `ABSORB_BY_PROGRESSIVE_DISCLOSURE`  
> Branch: `feat/claim-intent-verification-gate-20260813`

## Work contract

### Goal

AI·Agent·작업자의 사실·완료 주장과 승인 의도가 실제 저장소·diff·실행·병합 증거에 연결됐는지 fail-closed로 검증하는 Gate를 기존 review owner에 흡수한다.

### In scope

- 전용 reference
- material claim, intent fidelity, completion claim 계약
- 기존 Registry route 재사용
- existing validation Template의 progressive disclosure 연결
- per-skill `SBE-038`, executable regression, owner Learning Log
- BCP-2026-027 lifecycle closeout

### Protected

- 30 ACTIVE Skill IDs
- `PLAN / BUILD / REVIEW`
- 기존 Registry entry와 generated derivative
- 기존 25KB review Skill 본문의 세부 계약
- PR #312 시각 도구 경로
- PR #316 exact-SHA 교정 경로
- 외부 SaaS 비의무 원칙

### Excluded

- 일반 TDD 신규 Skill
- 일반 비엔진 디버깅 신규 Skill
- 출시 준비도 신규 Skill
- CI workflow 구조 변경
- Godot runtime·render 기능 변경

### Rollback

PR #317 squash commit을 revert한다. 신규 reference·eval·design·plan·test를 제거하고 validation Template·owner Learning Log·BCP lifecycle additions를 복구한다.

## Task 1 — Concurrent-change preflight

1. current main, 열린 PR, 동일 목표 branch/PR을 조회한다.
2. changed-path 교집합과 semantic ownership을 확인한다.
3. branch가 main보다 뒤처지면 force 없이 history를 reconcile한다.
4. `behind_by=0`을 재확인한다.

**Observed**

- PR #316 병합 뒤 main은 `e2c1d0c4b6fd0a7ce7874d200176d267a7d614d5`로 이동했다.
- PR #317은 force 없이 merge history를 reconcile해 main의 후손이 됐다.
- PR #312·#316 변경 경로와 구현 경로의 교집합은 0이었다.

## Task 2 — RED contract

1. 전용 contract test를 먼저 작성한다.
2. canonical CI가 새 파일을 실행하는지 확인한다.
3. 실행 목록 누락 시 이미 docs·contract suite가 실행하는 기존 aggregator에 전용 test case를 연결한다.
4. exact RED head에서 기존 계약은 통과하고 새 계약만 실패하는지 확인한다.

**Recorded RED**

- initial test commit: `9a4a6e688e993114466e3f25831555b23fcf5912`
- canonical aggregation commit: `8a161eca8d129584aecb3898e8d5622dcfc89efb`
- run: `31656590653`
- docs-validation job: `94312314139`
- result: 113 tests; exactly six new-contract failures after existing listed contracts passed

## Task 3 — Existing-solution-first disposition

Compare candidate integrations.

- new ACTIVE Skill: reject as duplicate owner
- new Work Mode: reject
- duplicate Registry triggers: defer until repeated model-run routing failure
- large SKILL.md insertion: reject as body bloat and repeated detail
- Template → reference progressive disclosure: approve

Existing route reused:

```text
external-ai-result + contract-check + evidence-report
→ REVIEW
→ reviewing-and-validating-project-changes
→ PROJECT_CHANGE_VALIDATION.md
→ claim-and-intent-verification.md
```

## Task 4 — Reference and validation artifact

Create:

- `skills/reviewing-and-validating-project-changes/references/claim-and-intent-verification.md`
- `docs/superpowers/specs/2026-08-13-claim-and-intent-verification-design.md`
- this plan

Update:

- `templates/quality/PROJECT_CHANGE_VALIDATION.md`

The reference and Template must expose:

- `MATERIAL_CLAIM_LEDGER`
- `INTENT_IMPLEMENTATION_FIDELITY_MATRIX`
- `COMPLETION_CLAIM_GATE`
- authority/freshness/counterevidence
- deterministic-first evidence
- Evidence ceiling
- exact HEAD and post-merge main readback
- `CLAIM_UNVERIFIED`, `IMPLEMENTATION_UNVERIFIED`, `BLOCKED_UNVERIFIED`

## Task 5 — Per-skill evaluation and learning

Create:

- `skills/reviewing-and-validating-project-changes/evals/claim-and-intent-verification.json`

`SBE-038` must:

- select `REVIEW`
- select `reviewing-and-validating-project-changes`
- reuse existing Registry triggers
- require exact-ref readback, actual diff, exact-head execution evidence, explicit unverified states, and main readback for merge claims
- reject search snippet or producer narrative as sole evidence

Update:

- `skills/reviewing-and-validating-project-changes/LEARNING_LOG.md`

Record:

- PR #316 exact-SHA correction
- search-result overpromotion regression
- initial false GREEN caused by CI test-discovery gap
- progressive-disclosure decision

## Task 6 — GREEN verification

On one exact head:

1. check current main ancestry and changed paths
2. run both repository workflows
3. confirm the six dedicated tests execute
4. confirm active Skill count remains 30
5. confirm Registry and generated derivative are unchanged
6. record pass/fail/skip counts
7. run independent adversarial review

Do not reuse a PASS after head or main changes.

## Task 7 — BCP lifecycle and PR closeout

Before merge:

- update BCP-2026-027 implementation record to PR #317
- preserve approval and proposal history
- document the approved design refinement from duplicate triggers/body insertion to existing-route progressive disclosure

Update PR body with:

- RED and GREEN exact heads/runs
- concurrent-path preflight
- changed paths
- protected scope
- verification boundary and rollback

Remove draft only after blocker-free exact-head review.

## Task 8 — Merge and post-merge readback

1. re-read current main and exact PR head
2. verify `behind_by=0`, mergeable state, zero unresolved threads, required workflows PASS
3. squash merge with `expected_head_sha`
4. record merge SHA
5. read new main and changed canonical files at merge SHA
6. verify post-merge workflows
7. report unexecuted local/Godot/render checks explicitly

## Definition of Done

- Existing Registry route selects the existing review owner.
- Validation Template links the dedicated reference.
- Three fail-closed contracts are usable.
- Active Skill count remains 30; Work Modes remain three.
- `SBE-038` and regression execute in canonical CI.
- BCP lifecycle points to PR #317.
- Exact-head workflows and independent review pass.
- Expected-head squash merge succeeds.
- Merge SHA and new main readback are recorded.
- PR #312/#316 paths and protected scope are unchanged.
