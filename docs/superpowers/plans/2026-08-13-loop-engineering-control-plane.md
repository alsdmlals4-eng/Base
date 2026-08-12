# Loop Engineering Control Plane Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a Base-owned Loop Engineering control-plane contract that starts only after user-reviewed planning is locked and autonomously executes, verifies, repairs, and integrates only that approved scope.

**Architecture:** Extend the existing `docs/OPERATING_MODEL.md` owner rather than creating a new broad Skill or fourth Work Mode. Add a machine-readable loop-run schema and project adapter templates, while reusing the current PLAN/BUILD/REVIEW, Continuous Work, GPT↔Codex handoff, adversarial review, validation, CI, and Learning/BCP owners.

**Tech Stack:** Markdown operating contracts, JSON Schema draft 2020-12, JSON example contract, Python `unittest`, existing GitHub Actions/Base validation.

## Global Constraints

- `Human-led WHAT/WHY, Agent-led HOW.`
- Loop execution may start only after `PLANNING_COMPLETE_GATE → PLANNING_LOCKED → LOOP_READY`.
- The loop may change technical HOW inside the approved contract but may not silently change approved WHAT/WHY, player experience, product direction, major UX meaning, content meaning, scope, or protected behavior.
- No new ACTIVE Skill, fourth Work Mode, always-on Base daemon, new workflow authority, dependency, secret, repository permission, or branch-protection change in this implementation.
- Default initial autonomy is isolated execution; auto-merge is a narrow project-declared allowlist and never covers protected governance/product surfaces.
- Multi-agent fan-out requires independent tasks and resource locks; same semantic resource must not have concurrent writers.
- Builder is not final reviewer; actual diff/evidence are reviewed independently.
- Learning never becomes Base canon automatically; reusable improvements continue through Learning/BCP/approval.
- External benchmark sources inform the design but never become project/Base authority.
- Runtime scheduler/webhook/24x7 service implementation is explicitly out of scope for this Base contract change.

---

### Task 1: Contract-first regression

**Files:**
- Create: `tests/test_loop_engineering_control_plane_contract.py`

**Interfaces:**
- Consumes: current Base `docs/OPERATING_MODEL.md` and existing routing/validation conventions.
- Produces: a focused regression that fails until the control-plane contract, schema, and project templates exist.

- [ ] **Step 1: Write the failing test**

Create a `unittest` contract that requires:
- `LOOP_ENGINEERING_CONTROL_PLANE`
- `PLANNING_COMPLETE_GATE`, `PLANNING_LOCKED`, `LOOP_READY`
- `Human-led WHAT/WHY, Agent-led HOW`
- A0–A4 autonomy labels and A2 initial default
- `WORK_JUSTIFICATION_GATE`
- `TASK_LEASE`, `RESOURCE_LOCK`, semantic-resource collision prevention
- independent Builder/Verifier/Critic separation
- `DESIGN_DRIFT_GATE`
- retry/budget/`NO_PROGRESS`
- source/main SHA freshness and stale-base handling
- learning→BCP separation
- protected surfaces and user-decision return
- explicit statement that the control plane is neither a fourth Work Mode nor a new broad Skill
- parseable `schemas/loop-run-contract-v1.schema.json`
- project profile and example run contract templates.

- [ ] **Step 2: Run the focused test to verify RED**

Run through the existing PR-triggered Base CI. Expected: focused contract fails because `LOOP_ENGINEERING_CONTROL_PLANE` and the new schema/templates do not yet exist; existing unrelated tests remain unaffected.

- [ ] **Step 3: Preserve RED evidence in the draft PR**

Record the exact branch HEAD, failing test/job, and expected missing-contract reason in the PR description before implementing production contract files.

### Task 2: Operating-model control plane

**Files:**
- Modify: `docs/OPERATING_MODEL.md`

**Interfaces:**
- Consumes: current PLAN/BUILD/REVIEW, `CONTINUOUS_WORK_ACTIVE`, GPT↔Codex handoff, adversarial-review, validation, CI, and Learning/BCP owners.
- Produces: the sole cross-owner lifecycle contract for post-planning autonomous execution.

- [ ] **Step 1: Add the planning lock entry gate**

Define `PLANNING_DRAFT → PLANNING_REVIEW → PLANNING_CONFIRMED → PLANNING_LOCKED → LOOP_READY` and require user-reviewed scope, acceptance criteria, protected behavior, exclusions, and adversarial planning review before `LOOP_READY`.

- [ ] **Step 2: Add the control-plane state machine**

Define `TRIGGER → DISCOVER → TRIAGE → CONTRACT → CONTEXT_SYNC → DECOMPOSE → ROUTE → ISOLATE → EXECUTE → VERIFY → ADVERSARIAL_REVIEW → REPAIR/DEFER/USER_DECISION → INTEGRATION_GATE → PR/MERGE_GATE → MAIN_READBACK → LEARN → NEXT_WORK`.

- [ ] **Step 3: Add autonomy and scope boundaries**

Define A0 Observe, A1 Propose, A2 Execute Isolated, A3 Bounded Auto Merge, A4 Human Only; set A2 as initial recommended default and prohibit governance/product-direction surfaces from auto-merge.

- [ ] **Step 4: Add multi-agent safety and stop rules**

Require task DAG, `TASK_LEASE`, `RESOURCE_LOCK`, semantic ownership, independent reviewer context, budget/retry bounds, `NO_PROGRESS`, stale SHA detection, failure classification, and local defer/continue behavior.

- [ ] **Step 5: Add design-drift and learning boundaries**

Define `NO_DRIFT / MINOR_TECHNICAL_DRIFT / PLANNING_CONFLICT`; only the first two may continue automatically. Store discovered product ideas as deferred improvement candidates. Learning must flow through existing Learning/BCP approval before Base canon changes.

- [ ] **Step 6: Route machine/project artifacts**

Reference `schemas/loop-run-contract-v1.schema.json`, `templates/project-operations/LOOP_ENGINEERING_PROFILE.md`, and `templates/project-operations/LOOP_RUN_CONTRACT.example.json` from the operating model.

### Task 3: Machine-readable loop run

**Files:**
- Create: `schemas/loop-run-contract-v1.schema.json`
- Create: `templates/project-operations/LOOP_RUN_CONTRACT.example.json`

**Interfaces:**
- Consumes: the operating-model state/autonomy vocabulary.
- Produces: a durable, validation-friendly per-run checkpoint and queue format.

- [ ] **Step 1: Create schema v1**

Require schema version/role, run/goal/project IDs, planning lock evidence, autonomy tier, source/main SHA, loop state, task queues, leases/locks, budget/retry state, evidence/findings, design-drift status, approval refs, blockers, and next action. Reject unknown top-level fields.

- [ ] **Step 2: Create valid example contract**

Provide an A2 isolated run example with `PLANNING_LOCKED`, exact 40-char SHA, bounded budgets, one ready task, no active lease, and explicit `NOT_RUN` evidence where execution has not occurred.

### Task 4: Project adoption profile

**Files:**
- Create: `templates/project-operations/LOOP_ENGINEERING_PROFILE.md`

**Interfaces:**
- Consumes: Base control-plane invariants.
- Produces: project-owned adapter values without copying Base policy into each project.

- [ ] **Step 1: Define adapter fields**

Include enabled/disabled status, planning-lock source, default autonomy, allowed executors, resource-lock domains, A3 allowlist, A4 protected surfaces, budget/retry limits, required evidence levels, merge policy reference, and scheduler/runtime provider when later adopted.

- [ ] **Step 2: Define safe defaults**

Default to A2 isolated execution, empty A3 allowlist, explicit A4 governance/product surfaces, bounded retries/agents/CI runs, and no scheduler/runtime provider until separately implemented and verified.

- [ ] **Step 3: Define adoption phases**

Document Shadow → Isolated Agent → Multi-Agent → Bounded Autonomous → Continuous Operations → Self-Improvement, with evidence-based promotion between phases and rollback to the prior phase on regressions.

### Task 5: GREEN, adversarial review, and integration

**Files:**
- Test: `tests/test_loop_engineering_control_plane_contract.py`
- Validate all changed production artifacts above.

**Interfaces:**
- Consumes: Tasks 1–4.
- Produces: exact-head evidence and merge-ready bounded Base change.

- [ ] **Step 1: Run focused GREEN validation**

Expected: all focused Loop Engineering contract tests pass.

- [ ] **Step 2: Run existing Base contract validation**

Require applicable Base v9/governance/reference-freshness/docs/publication checks and final `ci-gate`; skipped/non-applicable jobs are not PASS.

- [ ] **Step 3: Run adversarial review**

Attack goal drift, busywork generation, same-resource concurrent writes, self-review, infinite repair loops, cost explosion, stale-main work, memory/canon laundering, self-governance, prompt injection/external-source authority, secret/permission overreach, PR churn, unsafe auto-merge, false completion, flaky-test misclassification, and automation-over-product overengineering.

- [ ] **Step 4: Apply only validated minimal findings**

Any technical MUST_FIX within the approved scope is corrected and regression-tested; product/governance expansion becomes `USER_DECISION_REQUIRED` rather than silent implementation.

- [ ] **Step 5: Remove transient plan if it has no durable consumer**

Delete this implementation-plan file from the final net diff after its execution history is preserved in commits/PR, unless Base validation identifies a durable consumer.

- [ ] **Step 6: Final exact-head gate and merge**

Recheck latest main, same-goal open/recent PRs, changed-file allowlist, exact HEAD, required checks, unresolved threads, and protected-surface state. If unchanged and all required gates pass, use expected-head protected squash merge under the user's approval-inherits-merge-authority contract.

- [ ] **Step 7: Post-merge readback**

Read the new main SHA and the retained artifacts, recheck same-goal PR/canon state, and report implemented, verified, not-run, residual risks, rollback, and future Phase-0/Phase-1 pilot work separately.
