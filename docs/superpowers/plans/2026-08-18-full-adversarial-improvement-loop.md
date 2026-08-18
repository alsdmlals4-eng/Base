# Full Adversarial Improvement Loop Implementation Plan

> **For agentic workers:** implement this plan in bounded test-first slices; do not bypass exact-head validation or user decision gates.

**Goal:** Correct Base so L1+ material work compares at least three viable alternatives, searches for a better option, evaluates long-term plan fit, and performs five complete adversarial review→improvement cycles rather than five segmented attack lenses.

**Architecture:** Preserve the existing authority chain instead of adding a new broad Skill. `AGENTS.md` owns the top-level invariant, `docs/LONG_HORIZON_WORK_EXECUTION_POLICY.md` owns the detailed long-horizon execution contract, `running-adversarial-review-and-refinement` owns the repeated full review/refinement semantics, and focused regression tests prevent reintroduction of the old five-distinct-round interpretation.

**Tech Stack:** Markdown policy/Skill contracts, Python unittest contract tests, GitHub Actions.

**Spec:** user-approved conversation contract on 2026-08-18.

## Global Constraints

- `MINIMUM_VIABLE_ALTERNATIVES: 3` for L1+ material design/implementation decisions; alternatives must be materially distinct and plausible, not filler.
- Use current-state evidence and benchmark/industry/success/failure evidence before recommendation.
- Search for a better alternative before initial selection and after new findings change the evidence.
- `FIVE_FULL_ADVERSARIAL_IMPROVEMENT_LOOPS` means full scope review → finding validation → approved refinement → verification → re-attack, repeated at least five times.
- Each loop rechecks the whole approved scope, including previous fixes; the five loops are not five different lenses.
- If loop 5 still exposes a blocking finding or a failed long-term-fit criterion, continue additional full loops until the blocking condition is closed or correctly blocked/user-decision-required.
- `LONG_TERM_PLAN_FIT_REQUIRED`: compare lifecycle cost, maintainability, reversibility, reuse/modularity, future Base evolution, user/player value, evidence strength, and current cost constraints.
- Preserve `CURRENT_PAID_PLANS: GPT_PRO, FIGMA_PRO` and `PAID_PLAN_COUNT: 2`.
- Do not add a new broad Skill or Work Mode unless existing owners cannot express the contract.

## Alternatives considered

1. **Keep five distinct attack lenses.** Low implementation cost, but contradicts the clarified user intent and allows five reports without iterative repair. **REJECT.**
2. **Repeat the same review five times without an improvement/search gate.** Matches the count but can become ceremony and does not require new evidence to change the solution. **REJECT.**
3. **Five full closed-loop review/refinement cycles with better-option search and long-term-fit recheck.** Preserves iterative learning, makes each repair input to the next attack, and keeps existing Skill ownership. **ADOPT.**
4. **Create a new orchestration Skill just for the five-cycle behavior.** Explicit but duplicates intake/adversarial/validation owners and increases routing load. **REJECT.**

## Benchmark synthesis already verified in Base evidence

- NASA Decision Analysis / Analysis of Alternatives: define alternatives and criteria, compare performance/cost/risk, then recommend; rigor scales with decision complexity.
- DORA working in small batches: bounded independently testable changes improve feedback and reduce instability.
- Google Engineering Practices small CLs: self-contained changes improve review depth, reasoning, merge and rollback.
- OpenAI agent-loop model previously reviewed for Base: later iterations are grounded by tool/results from prior iterations, supporting evidence-fed re-evaluation rather than disconnected repeated prose.

Live web refresh was attempted on 2026-08-18 and returned HTTP 503; this plan therefore reuses the official-source evidence already captured in `docs/evidence/2026-08-18-base-postmerge-trade-study-and-adversarial-followup.md` and does not claim a fresh fetch succeeded.

## Tasks

### Task 1: RED contract tests

- Update `tests/test_base_long_horizon_work_contract.py`.
- Update `tests/test_neutral_adversarial_feature_lifecycle.py`.
- Require the new minimum-three-alternative, better-option-search, long-term-fit, and five-full-loop contracts.
- Explicitly reject active `FIVE_DISTINCT_ADVERSARIAL_ROUNDS` / segmented round tokens.
- Observe RED on the test-only PR head before production policy changes.

### Task 2: Top-level and long-horizon contracts

- Modify `AGENTS.md` so the invariant is visible at Base entry.
- Modify `docs/LONG_HORIZON_WORK_EXECUTION_POLICY.md` so the execution order is current state → >=3 viable alternatives → benchmark → provisional selection → five full improvement loops → long-term-fit closure.
- Preserve all unrelated cost, Figma, Tool Hub, Loop Engineering, Git, archive and completion rules.

### Task 3: Adversarial owner semantics

- Modify `skills/running-adversarial-review-and-refinement/SKILL.md`.
- Replace the segmented five-round invariant with a complete-loop invariant.
- Each loop must attack the full approved scope, validate findings, refine approved findings, verify/regression-check, search for a better option when evidence changes, and re-attack the resulting state.
- Record `loop_index`, input state/evidence delta, findings, changes, verification, better alternative result, long-term fit, and unresolved items.

### Task 4: Five real improvement cycles on this change

- Cycle 1: full intent/canon/implementation/test/operations/cost/concurrency/completion attack; fix findings; verify.
- Cycle 2: re-run the same full scope on the improved state; fix; verify.
- Cycle 3: repeat; fix; verify.
- Cycle 4: repeat; fix; verify.
- Cycle 5: repeat; fix; verify; if blocking findings remain, continue additional full cycles.
- Do not relabel five lenses as five loops.

### Task 5: Exact-head PR and postmerge

- Recheck latest main and same-goal PRs.
- Require relevant exact-head Actions success and unresolved review threads 0.
- Merge by normal repository path only.
- Read back merged main, active contract tokens, and stale old-token search.
- Classify any historical evidence containing the old design as historical/superseded rather than deleting provenance.
