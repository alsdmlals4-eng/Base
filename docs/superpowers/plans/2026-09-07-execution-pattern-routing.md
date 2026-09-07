# Execution Pattern Routing Implementation Plan

> **For agentic workers:** Use superpowers:executing-plans for inline execution. Preserve current authority and run superpowers:requesting-code-review before merge.

**Goal:** 기존 비용 Skill에 작업별 실행 방식과 실패별 다음 행동을 연결한다. 실제 모델 전환·유료 도구·새 실행기는 만들지 않는다.

**Architecture:** 기존 `route-model-and-effort` mode와 `model-stack-routing.md`가 판단을 소유한다. Skill Output contract의 조건부 필드와 기존 Skill 실행 보고가 결과를 소비하며, 검증·재개·권한은 기존 owner에 남는다.

**Tech Stack:** Markdown reference, existing Python validators and repository CI, separate-context agent application tests.

**Spec:** 사용자에게 제시한 세 대안 중 기존 Skill 확장 권장안을 2026-09-07 `진행해`로 승인한 현재 계약. 시작 근거: `docs/operations/work-receipts/2026-09-07-execution-pattern-routing.json`.

## Global constraints

- Base baseline: `1072e201900e3aa4a403330d4132c737fc86142a`; existing root checkout and unrelated PRs read-only.
- No model/provider/profile/Registry/config/runner/CI workflow changes; no new paid path, installation, game change or project rollout.
- Fixed safety/quality/authority gates, variable task-specific model choices and limits. Single does not waive review; Critique does not replace the existing full-loop floor.
- Reference retrieval/application evidence is not production efficacy, runtime, cost reduction or Human approval.
- PLAN → BUILD → REVIEW; `REUSED_APPROVAL`, `CONTINUOUS_WORK_ACTIVE`. Blueprint/game design is not applicable to this Base reference-only change.

## Task 1 — complete existing reference and its consumer

**Files:** Modify the cost Skill `SKILL.md`, `references/model-stack-routing.md`, `LEARNING_LOG.md` and existing `templates/project-operations/SKILL_EXECUTION_REPORT.md` consumer link; retain this plan and start receipt as evidence. No new runtime schema or code.

**Interface:** Input is the existing work_package, cost_surface, actual capability and acceptance evidence. Output adds a conditional advisory execution_strategy inside the existing Skill result; map it to existing SKILL_EXECUTION_REPORT fields. Unknown evidence is not a successful route execution.

- [x] Read latest main/current owners, actual report template, adjacent recovery/continuation owners, official HydraFusion source and open PR807/808 paths; no overlapping changed target paths.
- [x] Baseline regression: 41 existing tests PASS. Start receipt validator PASS.
- [x] Baseline reference application by separate-context agent on exact baseline: three cases below; missing pattern/role/failure-record structure and single-model exclusion observed, not an unsafe production execution.
- [x] Extend existing Skill/reference/log and report link to close observed retrieval gaps, retaining Registry non-use boundaries.
- [ ] New separate-context consumer applies same cases with extended Skill; retain counterexamples and actual outputs on this task PR.
- [ ] Existing focused tests, full local validation, canonical freshness and package checks pass.
- [ ] Independent full-scope review loops, exact-head CI, protected merge and postmerge readback.

### Frozen reference application cases and expected boundaries

These are hypothetical tasks used to test documentation consumption, not game execution. Do not expose the expected answers when dispatching application consumers.

| Case | Input | Required observable answer |
|---|---|---|
| A | Approved deterministic Schema conversion, existing converter and validator, no meaning change; one model only | Reuse deterministic tool; if AI needed Single; select pattern/reason and evidence gate without automatic model change or invented cost |
| B | Small approved fix: engine missing; actual assertion defect; essential authority unavailable; external write timeout with unknown effect | Distinguish all four causes; recover environment without quality PASS, bounded defect correction/escalation recommendation, authority blocker, destination readback before any write replay |
| C | Cross-system save contract needs independent review; only same-model separate context, no new paid service | Critique candidate, actual independence/evidence ceiling, current reviewer contract determines acceptability, no paid cross-family demand or review floor waiver |

Variation/negative cases: capability unavailable; unchanged candidate repeatedly fails; cancellation after possible external effect; user offers subscription tokens as proof of 67% monetary saving. Expected: no invented route/capability or threshold, no blind replay/automatic stronger provider, no unsupported savings.

## Verification commands

Run with process-local `PYTHONUTF8=1` and `PYTHONIOENCODING=utf-8`:

```text
python -m unittest tests.test_p08_ai_operations_contract tests.test_skill_package_integrity tests.test_mcp_capability_absorption tests.test_approved_slice_continuous_handoff tests.test_continuous_work_execution_contract tests.test_handoff_resumability_contract -q
python tools/run_local_validation.py --trusted-history-commit 1072e201900e3aa4a403330d4132c737fc86142a
python tools/check_canonical_reference_freshness.py --base 1072e201900e3aa4a403330d4132c737fc86142a --head HEAD
```

No grep-only new test is presented as agent behavior. Existing text contracts remain regression checks; reference consumption is evaluated by the separate-context application results. Scenario-level retrieval coverage is the only improvement being tested; no stochastic robustness or productivity claim.

## Rollback and closeout

Revert only this change's additions to Skill/reference/log/plan/receipt together, preserving preexisting and subsequent work. Recheck routing, package and cost boundaries. Final subject SHA, exact checks, review, merge and cleanup belong to current-task PR; the receipt is an immutable start snapshot, not a second current board. Project local copies adopt only through their own approved synchronization.
