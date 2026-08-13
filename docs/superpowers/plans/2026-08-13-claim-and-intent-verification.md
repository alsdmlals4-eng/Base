# Claim and Intent Verification Gate — Implementation Plan

> Proposal: `BCP-2026-027-claim-and-intent-verification-gate`
> Owner: `reviewing-and-validating-project-changes`
> Work Mode: `REVIEW`
> Branch: `feat/claim-intent-verification-gate-final`

## Work contract

### Goal

AI·Agent·작업자의 사실·완료 주장과 승인 의도가 실제 저장소·diff·실행·병합 증거에 연결됐는지 fail-closed로 검증하는 Gate를 기존 review owner에 흡수한다.

### In scope

- 전용 Mode와 reference
- material claim, intent fidelity, completion claim 계약
- 좁은 Registry trigger/use_when 보강과 파생본 갱신
- validation template 및 REVIEW 운영 문서 연결
- `SBE-038`, 전용 regression, 중앙 Learning Log
- BCP-2026-027 구현 lifecycle closeout

### Protected

- 30 ACTIVE Skill IDs
- `PLAN / BUILD / REVIEW`
- 기존 review modes와 검증 계약
- PR #312 시각 도구 경로
- PR #316 exact-SHA 교정 경로
- 외부 SaaS 비의무 원칙
- 사용자 변경과 저장소 정본

### Excluded

- 일반 TDD 신규 Skill
- 일반 비엔진 디버깅 신규 Skill
- 출시 준비도 신규 Skill
- CI workflow 구조 변경
- Godot runtime·render 기능 변경

### Rollback

PR #319 squash commit을 revert하고 Registry 파생본을 재생성한다. 신규 파일만 제거한 뒤 기존 owner·template·docs·eval·BCP state additions를 함께 되돌린다.

## Task 1 — Concurrent-change preflight

1. current main, PR #312, PR #316, 동일 목표 branch/PR을 조회한다.
2. changed-path 교집합과 semantic ownership을 확인한다.
3. branch가 main보다 뒤처지면 force 없이 merge history를 reconcile한다.
4. `behind_by=0`, changed-path intersection 0을 기록한다.

**Complete when**

- branch는 current main의 후손이다.
- 다른 열린 작업 경로를 수정하지 않는다.

## Task 2 — RED contract

1. `tests/test_claim_and_intent_verification_contract.py`를 먼저 작성한다.
2. canonical CI가 새 테스트를 실행하는지 확인한다.
3. 실행 목록 누락 시 이미 docs·contract suite가 실행하는 기존 aggregator에 전용 test case를 연결한다.
4. exact RED head에서 기존 계약은 통과하고 새 계약만 실패하는지 확인한다.

**Recorded RED**

- initial test commit: `9a4a6e688e993114466e3f25831555b23fcf5912`
- canonical aggregation commit: `8a161eca8d129584aecb3898e8d5622dcfc89efb`
- Game Project OS run: `31656590653`
- docs-validation job: `94312314139`
- result: 113 tests, exactly 6 new-contract failures; existing listed contracts passed before those failures

**Complete when**

- 실패가 mode/reference/routing/template/eval/design 누락만 가리킨다.

## Task 3 — Reference and design artifacts

Create:

- `skills/reviewing-and-validating-project-changes/references/claim-and-intent-verification.md`
- `docs/superpowers/specs/2026-08-13-claim-and-intent-verification-design.md`
- this plan

The reference must define:

- `MATERIAL_CLAIM_LEDGER`
- `INTENT_IMPLEMENTATION_FIDELITY_MATRIX`
- `COMPLETION_CLAIM_GATE`
- authority/freshness/counterevidence
- deterministic-first evidence
- Evidence ceiling
- exact HEAD and post-merge main readback
- `CLAIM_UNVERIFIED`, `IMPLEMENTATION_UNVERIFIED`, `BLOCKED_UNVERIFIED`

## Task 4 — Existing owner integration

Update `skills/reviewing-and-validating-project-changes/SKILL.md` without deleting existing modes.

- add `claim-and-intent-verification` under Modes
- add required claim/intent inputs
- place Gate before final evidence report and merge claim
- link `references/claim-and-intent-verification.md`
- add completion-claim failure conditions and Definition of Done items

**Complete when**

- no new Skill ID exists.
- existing review contracts remain byte-semantically preserved except approved additions.

## Task 5 — Routing and generated derivative

Update `skills/SKILL_REGISTRY.json` for the existing owner only.

Add trigger tags:

- `completion-claim`
- `claim-evidence`
- `intent-conformance`
- `hallucination-audit`

Extend `use_when` so 완료 주장, 승인 의도, 실제 diff, exact HEAD are explicit.

Run or rely on CI to verify generator output after updating:

- `docs/generated/BASE_ACTIVE_SKILLS.md`

**Complete when**

- active Skill count remains 30.
- generated derivative matches the Registry.

## Task 6 — Template and operating workflow

Update:

- `templates/quality/PROJECT_CHANGE_VALIDATION.md`
- `docs/WORK_MODE_AND_SKILL_ROUTING.md`
- `docs/OPERATING_MODEL.md`

Expose `CLAIM_AND_INTENT_VERIFICATION_GATE` in REVIEW with:

1. Material Claim Ledger
2. Intent–Implementation Fidelity Matrix
3. Completion Claim Gate
4. `BLOCKED_UNVERIFIED` behavior

Do not duplicate the full reference; link to it.

## Task 7 — Behavior eval and learning

Add `SBE-038` to `skills/SKILL_BEHAVIOR_EVALS.json`.

Expected behavior:

- Work Mode `REVIEW`
- primary owner `reviewing-and-validating-project-changes`
- mode `claim-and-intent-verification`
- requires exact-ref readback, actual diff, exact-head execution evidence, explicit unverified states, and main readback for merge claims
- rejects search snippet or producer narrative as sole evidence

Append to `skills/SKILL_LEARNING_LOG.md`:

- BCP-2026-027
- real search-result overpromotion regression
- exact-SHA readback correction
- initial CI test-discovery gap and canonical aggregation fix

## Task 8 — GREEN verification

On one exact head:

1. check PR changed paths and current main ancestry
2. run both repository workflows
3. confirm proposal validation and reference freshness
4. confirm contract tests include the six new tests
5. record pass/fail/skip counts
6. inspect generated artifact drift
7. run independent adversarial review

Do not reuse a PASS after head or main changes.

## Task 9 — BCP lifecycle and PR closeout

Before implementation merge:

- update BCP-2026-027 proposal/Registry to the lifecycle state accepted by repository governance
- set implementation PR to `https://github.com/alsdmlals4-eng/Base/pull/319` when marking `IMPLEMENTED`
- preserve proposal history and approval evidence

Update PR body with:

- RED and GREEN exact heads/runs
- concurrent-path preflight
- changed paths
- protected scope
- verification boundary and rollback

Remove draft only after blocker-free exact-head review.

## Task 10 — Merge and post-merge readback

1. re-read current main and exact PR head
2. verify `behind_by=0`, mergeable state, zero unresolved threads, required workflows PASS
3. squash merge with `expected_head_sha`
4. record merge SHA
5. read new main and changed canonical files at merge SHA
6. verify post-merge workflows
7. report unexecuted local/Godot/render checks explicitly

## Definition of Done

- Existing owner contains and links the Gate.
- Three contracts are usable from the validation template.
- Registry routing is explicit and active count remains 30.
- Operating docs route material completion claims through REVIEW.
- `SBE-038` and regression run in canonical CI.
- BCP lifecycle points to PR #319.
- Exact-head workflows and independent review pass.
- Expected-head squash merge succeeds.
- Merge SHA and new main readback are recorded.
- No PR #312/#316 path or protected scope is modified.
