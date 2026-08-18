# Base Long-Horizon Governance — Five-Round Adversarial Review

Date: 2026-08-18

Scope: PR #516 (`feat/base-lifecycle-governance-refresh-20260818`) and the user-authorized reconciliation of the remaining Base owner PR backlog.

This record is evidence for the requested **exactly five distinct adversarial rounds**. It is not runtime/gameplay/Figma-user-PC proof. `NOT_RUN` and external/live evidence ceilings remain distinct from repository contract PASS.

## Baseline and benchmark synthesis

Current integration direction is grounded in repository evidence plus external practice; none of these external sources becomes Base authority by itself.

| Source | Principle extracted | Disposition |
|---|---|---|
| Google Engineering Practices — Small CLs (`https://google.github.io/eng-practices/review/developer/small-cls.html`) | small, self-contained changes are easier to review, correct, merge and roll back | `ADAPT`: repo-wide discovery, bounded independently testable implementation slices |
| DORA — Working in small batches (`https://dora.dev/capabilities/working-in-small-batches/`) | small batches counter delivery instability, including AI-assisted work | `ADOPT`: avoid one giant opaque Base rewrite |
| ACL 2026 ToolScope (`https://aclanthology.org/2026.acl-long.1573/`) | overlapping/redundant tool descriptions increase selection ambiguity; merging/filtering improves routing | `ADAPT`: sparse Skill routing, REUSE/ABSORB/MERGE before new Skill |
| Godot Resources (`https://docs.godotengine.org/en/stable/tutorials/scripting/resources.html`) | Resources are serializable repo-native data containers | `ADAPT`: Figma for visual collaboration, repo-native structured data for runtime/balance/config authority |

## Round 1 — Intent / scope / planning distortion

**Attack hypothesis:** The request can be misread as “add more rules and Skills everywhere,” producing bureaucracy instead of preserving the user’s intended long-horizon game-development workflow.

**Evidence inspected:** user-approved design/plan; current `AGENTS.md`; Skill Registry routing model; `docs/LONG_HORIZON_WORK_EXECUTION_POLICY.md`; open/closed PR inventory.

**Findings:**

1. A new broad Skill would duplicate intake/review/Git/archive/change-proposal owners. Severity: `P1` before disposition.
2. “Remaining work = 0” could become an unbounded mandate to finish unrelated future backlog. Severity: `P1` before disposition.
3. “Use Figma instead of Sheets” could be distorted into moving runtime/balance/schema truth into a visual canvas. Severity: `P1` before disposition.

**Disposition / fix:**

- Implement one policy composition layer, not a new active Skill.
- Define `REQUIRED_WORK_REMAINING: 0` only against the approved acceptance criteria; external blockers and optional backlog are separate axes.
- Define Figma as the default visual workspace while preserving GitHub canon and repo-native structured data for rules/balance/economy/schema/runtime configuration.
- Keep destructive Sheet deletion outside the default migration path; preserve legacy/proposal source until verified migration/readback.

**Recheck:** focused long-horizon contract and Base-v9 broad contract passed on exact integration heads after implementation.

**Round status:** `PASS`; unresolved P0/P1: `0`.

## Round 2 — Canonical ownership / structure / dependency drift

**Attack hypothesis:** New policy text can create a second authority, stale status documents can contradict implementation, and old owner PRs can leave duplicate active routes.

**Evidence inspected:** `AGENTS.md`; `docs/LOOP_ENGINEERING_A2_RUNTIME.md`; `docs/operations/UNIVERSAL_LOOP_CROSS_PROJECT_ACCEPTANCE.json`; Skill routing guide; #399/#369/#384/#445/#450/#460 and their merged successors.

**Findings:**

1. Loop A2 foundation documentation carried historical/current-state ambiguity. Severity: `P1`.
2. #399 contained a useful sparse-routing delta not yet on completed main. Severity: `P1`.
3. #369/#384/#445/#450/#460 remained open after stronger or canonical successor implementations existed. Severity: `P1` as duplicate/stale authority risk.

**Disposition / fix:**

- `docs/LOOP_ENGINEERING_A2_RUNTIME.md` now declares itself a foundation/historical invariant document and delegates mutable current operational status to `docs/operations/UNIVERSAL_LOOP_CROSS_PROJECT_ACCEPTANCE.json`.
- #399 was selectively absorbed into #516 and its focused routing contract revalidated; #399 was then closed as superseded.
- #369 was reconciled against merged #374 (`DOCKER_NONE_DENIED_V1`), #384 against the reconciled Tool Hub/Figma delivery mainline (#428 and successors), #445 against #446, #450 against #452, and #460 against #468; each stale owner PR was closed unmerged with a supersession comment.
- Whole stale branches were not merged onto current main.

**Recheck:** repository open-PR query after reconciliation returned only #516 as the active PR in this scope.

**Round status:** `PASS`; unresolved P0/P1: `0`.

## Round 3 — Failure / security / concurrency / recovery

**Attack hypothesis:** A long automated work sequence may overwrite concurrent updates, broaden privileges/cost, retry blindly, or convert blocked evidence into PASS.

**Evidence inspected:** current GitHub connector capability; branch write conflict behavior; `ZERO_INCREMENTAL_COST_REQUIRED`; Loop provider policy; Learning Log; exact-head workflow behavior.

**Findings:**

1. An `AGENTS.md` update attempt returned HTTP 409 because the file advanced after the read. A blind retry with stale bytes would have overwritten newer work. Severity: `P0` if mishandled.
2. Local container clone failed because GitHub DNS/network access was unavailable. Treating that as a global blocker would violate the approved recovery policy. Severity: `P1`.
3. No paid API/API-key fallback is needed; enabling one would violate the approved cost boundary. Severity: `P0` if introduced.

**Disposition / fix:**

- On 409, stop the write, re-read the exact current blob, preserve newer content, and apply only missing material delta. In this case the required `AGENTS.md` wiring was already present, so no overwrite was performed.
- Switch repository read/write/test evidence from unavailable container GitHub networking to the authenticated GitHub connector plus GitHub Actions; do not claim local validation that did not run.
- Preserve `paid_openai_api: FORBIDDEN`, ChatGPT-authenticated subscription route, A3 disabled, scheduler not configured, and `NOT_RUN/BLOCKED_* != PASS`.
- Promote the 409/stale-owner/focused-vs-broad-CI lesson into `skills/synchronizing-local-and-github-state/LEARNING_LOG.md`.

**Recheck:** no force push/direct-main/ruleset bypass or paid provider call was used by this integration.

**Round status:** `PASS`; unresolved P0/P1: `0`.

## Round 4 — Player value / benchmark / cost / maintainability

**Attack hypothesis:** Governance can become internally elegant but harmful to actual game production by increasing ceremony, hiding player-value work, or forcing the wrong tool for data.

**Evidence inspected:** external benchmark synthesis above; ToolScope sparse-routing finding; user requirements for core loop, dummy balance, story fit, modular reuse, Figma visualization, and zero incremental cost.

**Findings:**

1. Five identical review repetitions would add ritual without new signal. Severity: `P1`.
2. “Use every important Skill/tool” could recreate the tool-overlap problem and context bloat. Severity: `P1`.
3. Figma-only data ownership would make simulation/balance/runtime regression harder. Severity: `P1`.
4. Game documentation could be “complete” before the player-facing core loop is buildable/testable. Severity: `P1`.

**Disposition / fix:**

- Require exactly five **different attack surfaces**, not five copies of the same self-review.
- Preserve sparse Skill routing: one primary discipline; supporting Skills are need-driven, not a quota.
- Require benchmark `ADOPT / ADAPT / REJECT` reasoning rather than copying one successful game/tool.
- Game workflow is `PLAYER PROMISE → CORE LOOP → CORE SYSTEMS → WORLD/STORYLINE FIT → REUSABLE MODULE BOUNDARIES → DUMMY BALANCE BUDGET → PLAYABLE BUILD → TEST → EVIDENCE-BASED TUNING`.
- Use configurable budget/parameter data instead of scattered magic numbers; no example numeric value is promoted to a project fact without evidence.
- Tool Hub and Loop Engineering are required **when relevant** and must be proven by their actual runtime/evidence boundaries, not by their names.

**Recheck:** long-horizon contract tests cover these stable policy markers; no new broad Skill ID or paid runtime dependency was added.

**Round status:** `PASS`; unresolved P0/P1: `0`.

## Round 5 — Regression / evidence / completion / postmerge readiness

**Attack hypothesis:** Focused tests may pass while Base-wide contracts fail; stale PR text may misreport RED after GREEN; merged status can be claimed before exact-head checks and postmerge readback.

**Evidence inspected:** TDD RED run for the long-horizon contract; exact-head focused workflows; Base-v9 broad workflow; GPO workflow; PR changed paths/body; action pin policy.

**Findings:**

1. Initial TDD RED correctly failed for the missing policy/entry wiring and stale Loop status. Expected and resolved.
2. A later Base-v9 broad run found one real compatibility failure: a newly added workflow referenced a floating `actions/checkout@v4` instead of Base’s required exact 40-character pin, while focused governance tests were green. Severity: `P1`.
3. #516 PR body still described the initial RED phase after production policy had been implemented. Severity: `P2` freshness issue.
4. Merge/postmerge claims remain invalid until final exact-head checks, review threads, merge result and main readback are all observed. Severity: `P0` if bypassed.

**Disposition / fix:**

- Pin new workflows to the repository’s exact reviewed action SHAs (`actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1`, `actions/setup-python@5fda3b95a4ea91299a34e894583c3862153e4b97`).
- Re-run Base-v9: the broad contract returned GREEN on the corrected exact head.
- Update #516 body from RED-phase narrative to the final implementation/reconciliation/evidence state before merge.
- Require final GPO completion, exact-head workflow re-read after this evidence/learning-log commit, unresolved thread count 0, then mark Ready and merge through normal repository rules with expected-head SHA.
- After merge, re-read `main` files and the merge SHA; only then report `REQUIRED_WORK_REMAINING: 0` for this approved contract.

**Recheck state at review-writing time:** final evidence commit itself still requires a fresh exact-head CI cycle; therefore this document does **not** self-assert final merge completion.

**Round status:** `PASS_WITH_FINAL_GATE_PENDING`; unresolved design/code P0/P1: `0`; pending procedural gate: exact-head CI/readback.

## Review summary

```text
Round 1 Intent / Scope                PASS
Round 2 Canon / Structure             PASS
Round 3 Failure / Security            PASS
Round 4 Player Value / Benchmark      PASS
Round 5 Regression / Evidence         PASS_WITH_FINAL_GATE_PENDING

P0 findings remaining: 0
P1 findings remaining: 0
P2 findings remaining: 1 (PR body freshness; update before merge)
Required procedural gate: fresh exact-head CI + threads + merge + postmerge readback
```
