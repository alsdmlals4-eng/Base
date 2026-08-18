# Base Long-Horizon Work Governance Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 최신 Base main에서 장기 작업 계약, sparse Skill routing, 게임 기획/밸런스 계약, Figma migration boundary, Loop status freshness를 하나의 검증 가능한 lifecycle로 연결한다.

**Architecture:** 기존 Skill owner를 유지하고 공용 long-horizon policy를 entry rule에서 연결한다. Open PR의 material delta는 latest main에 selective copy하고 stale PR/상태 문서는 superseded 처리한다. 정책 변경은 contract test → expected RED → implementation → exact-head GREEN 순서로 검증한다.

**Tech Stack:** Markdown, JSON, Python unittest, GitHub Actions, GitHub PR/Actions.

**Spec:** `docs/superpowers/specs/2026-08-18-base-long-horizon-work-governance-design.md`

## Global Constraints

- `ZERO_INCREMENTAL_COST_REQUIRED`
- latest completed `main` is the implementation base.
- open PR branches may be inspected/absorbed under the user's current explicit authorization; stale whole-branch merge is forbidden.
- no direct main push, force push, ruleset bypass, or paid API fallback.
- `NOT_RUN` / `BLOCKED_*` may not be promoted to PASS without evidence.
- exactly five adversarial rounds, each with a distinct attack surface.

---

### Task 1: Add RED governance contract

**Files:**
- Create: `tests/test_base_long_horizon_work_contract.py`
- Create: `.github/workflows/validate-base-long-horizon-work-contract.yml`

**Interfaces:**
- Consumes: current `AGENTS.md`, Loop status doc, Tool Registry, existing Sheet/Figma policies.
- Produces: machine-checkable required terms and route wiring.

- [ ] Write tests that require the new policy, entrypoint link, sparse routing guide, five-round contract, Figma/repo-data migration contract, game workflow contract, and Loop current-status pointer.
- [ ] Push tests/workflow without implementation.
- [ ] Observe an exact-head Actions failure caused by missing new contract, not syntax/setup errors.

### Task 2: Implement sparse Skill routing from PR #399

**Files:**
- Create: `docs/knowledge/ai/SKILL_ROUTING_PRECISION_GUIDE.md`
- Create: `tests/test_skill_routing_precision_policy.py`
- Create: `.github/workflows/validate-skill-routing-precision.yml`
- Modify: `skills/README.md`

**Interfaces:**
- Consumes: `skills/SKILL_REGISTRY.json` hard ceilings and #399 material delta.
- Produces: default supporting budget=1, second supporting skill exception-only, body tie-break, reuse/absorb/merge-first rule.

- [ ] Selectively copy #399 guide/test/workflow onto latest main.
- [ ] Wire the current latest-main `skills/README.md` without overwriting newer changes.
- [ ] Run focused Actions and broad contract workflows on the new exact head.

### Task 3: Add long-horizon lifecycle policy and entry wiring

**Files:**
- Create: `docs/LONG_HORIZON_WORK_EXECUTION_POLICY.md`
- Modify: `AGENTS.md`

**Interfaces:**
- Consumes: existing intake/continuous-work/adversarial/game-OS/Tool-Hub/Loop/Figma owners.
- Produces: direction-first workflow, expected-effect/risk/mitigation gate, one initial approval, bounded continuous completion, error recovery, 5 review rounds, postmerge promotion/supersession, scoped required-work=0.

- [ ] Write the policy without creating a new Skill or duplicate authority.
- [ ] Link it from `AGENTS.md` and make Figma + repo-native structured data the new-work default while preserving legacy Sheet migration compatibility.
- [ ] Re-run long-horizon contract.

### Task 4: Repair Loop status freshness

**Files:**
- Modify: `docs/LOOP_ENGINEERING_A2_RUNTIME.md`

**Interfaces:**
- Consumes: `docs/operations/UNIVERSAL_LOOP_CROSS_PROJECT_ACCEPTANCE.json`.
- Produces: clear historical/foundation status and a single current operational authority pointer.

- [ ] Mark the old current-status wording as `SUPERSEDED_STATUS_SNAPSHOT`.
- [ ] Preserve foundation invariants and point current operational claims to the machine checkpoint.
- [ ] Assert that deferred slices already marked merged in the checkpoint are not presented as current deferred work.

### Task 5: Open-PR reconciliation and five-round review

**Files:**
- Create: `docs/evidence/2026-08-18-base-long-horizon-governance-adversarial-review.md`

**Interfaces:**
- Consumes: latest main, integration diff, PR #399/#460/#450/#445/#384/#369/#496 status.
- Produces: `absorbed_owner_deltas`, `residual_owner_deltas`, 5 distinct adversarial rounds and dispositions.

- [ ] Recheck each open PR against latest main.
- [ ] Close only PRs with zero unique material delta and record successor/integration evidence.
- [ ] Preserve unrelated or residual work.
- [ ] Execute rounds: intent/scope; canon/dependency; failure/security/concurrency; benchmark/player-value/cost; regression/evidence/completion.
- [ ] Resolve P0/P1 findings and re-run exact-head checks.

### Task 6: PR gate, merge, postmerge

**Files:**
- No new product file required; update evidence only if exact-head state changes.

**Interfaces:**
- Consumes: final integration head and GitHub Actions.
- Produces: merged main SHA and postmerge readback.

- [ ] Confirm current main movement and reconcile if necessary.
- [ ] Confirm exact-head required workflows, unresolved thread 0, P0/P1 0.
- [ ] Merge using the repository-allowed method.
- [ ] Re-read merged main files and workflow status.
- [ ] Promote reusable incident/lesson and mark superseded PR/material.
- [ ] Report `required work remaining`, `external blockers`, `optional backlog` separately.
