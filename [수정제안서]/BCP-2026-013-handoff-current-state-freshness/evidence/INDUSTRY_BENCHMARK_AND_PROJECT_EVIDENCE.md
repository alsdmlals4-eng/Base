# BCP-2026-013 Evidence — Handoff / Current-State Freshness

## 1. Project observation

Source project: `alsdmlals4-eng/Switchy-Express-Cargo-Puzzle`

Observed project baseline before the handoff repair:

- current decision/canon had advanced through `SX-DEC-055`;
- the configured Google Sheet also recorded `SX-DEC-055` as implementation DoR ready;
- `START_HERE.md`, `ACTIVE_CONTEXT.md`, and `ROADMAP.md` still routed a new session through materially older PR/decision/gate state;
- the user explicitly deferred `SX-DEC-055` runtime implementation and requested handoff work instead.

The project repair therefore treated handoff/current-state files as **resume locators, not repository truth**, reread GitHub/Sheet/current canon, and updated the existing current-state owners rather than creating a second handoff authority.

Project repair PR: `alsdmlals4-eng/Switchy-Express-Cargo-Puzzle#137`.

## 2. Existing Base coverage

Current Base already has the right responsibility owners:

- `maintaining-project-context-and-handoff`
- `auditing-canonical-reference-freshness`
- project-operation templates for `PROJECT_START_HERE.md`, `ACTIVE_CONTEXT.md`, and `HANDOFF.md`
- project change validation and cold-start operating-system tests

The missing layer is not a new Handoff Skill. It is a reusable **cross-owner freshness / resume-route consistency** contract.

Verdict: `ABSORB`.

## 3. External benchmark

### 3.1 GitHub — keep a PR in sync with its base

Official GitHub guidance says a pull-request branch can be updated with changes from the base branch to resolve conflicts and catch test failures before merge. GitHub also notes that the base commit associated with an already-open PR does not automatically become a new historical reference simply because the base branch later moves.

Reusable principle:

```text
saved review/context state
≠ automatically current repository state
```

For handoff/resume, this supports rereading current main/PR state instead of trusting a stored SHA or prose snapshot as current truth.

Adopt:
- current repository state before resume decisions;
- explicit stale/compatibility check when the base/current state has moved.

Do not copy:
- GitHub-specific PR metadata schema into every project handoff format.

Sources:
- GitHub Docs, *Keeping your pull request in sync with the base branch*.
- GitHub Docs, *Changing the base branch of a pull request*.

### 3.2 Google Engineering Practices — small, self-contained changes

Google's public code-review guidance recommends small, self-contained changes because they are easier to review thoroughly, reason about, merge, and roll back. It also recommends separating unrelated refactors from behavior changes.

Reusable principle:

```text
repair the existing current-state owner with the smallest coherent delta
instead of creating a second broad status/handoff authority
```

Adopt:
- bounded current-state repair;
- separate active implementation from proposal/governance changes;
- keep one conceptual change per review unit where practical.

Do not copy:
- organization-specific CL approval mechanics or line-count heuristics as hard project rules.

Source:
- Google Engineering Practices, *Small CLs*.

### 3.3 AWS Prescriptive Guidance — preserve decision history and supersession

AWS ADR guidance treats accepted decision records as historical records that should be preserved. When a new decision replaces an old one, the newer record supersedes the old rather than rewriting history; the decision log remains useful to future team members.

Reusable principle:

```text
historical snapshot can remain historical
while active current-state routing must point to the current decision
```

Adopt:
- preserve historical context instead of deleting it;
- distinguish active current-state owner from historical evidence;
- explicit superseded/deferred states.

Do not copy:
- require ADR format for every project or every handoff.

Sources:
- AWS Prescriptive Guidance, *Architectural decision record process*.
- AWS Prescriptive Guidance, *Best practices for using architectural decision records*.

## 4. Generalization boundary

Promote only:

- current repo truth precedes stored handoff prose;
- material checkpoint triggers a freshness check;
- stale continuation state fails closed before task selection;
- approved-but-deferred work retains approval while execution remains deferred;
- existing owner is repaired rather than duplicated.

Do not promote:

- project-specific Decision IDs, PR numbers, Sheet rows, gameplay rules, engine version, or asset counts;
- a requirement that every project have the same exact filenames;
- a timestamp-only stale detector;
- automatic resumption of user-deferred work without the user's resume trigger.

## 5. Counterexamples

- historical/archive handoff intentionally excluded from cold-start routing;
- project has a generated current-state view that is atomically derived from the canonical source;
- stored SHA explicitly means `baseline_observed_at`, not `current_head`;
- roadmap owns only long-term milestones and not the next executable action.

These should not be flagged solely because values are older than current main.

## 6. Adversarial review

### MUST_FIX — resolved in proposal

- BCP ID collision: `BCP-2026-012` was already used and merged by another proposal. This candidate uses `BCP-2026-013`.

### REJECTED_CRITIQUE

- Create a new broad Handoff/Progress Skill: rejected because Base already has a clear owner.
- Treat every old SHA as stale: rejected because historical baselines are legitimate.
- Force Roadmap as an active next-step owner in every project: rejected because project structures differ.

### DEFER

- exact active-file/test implementation design: deferred to a separate follow-up stage because this execution contract allows Base proposal storage only and forbids active Base implementation.

## 7. Evidence ceiling

```yaml
project_failure_mode_reproduced: true
project_handoff_repair_pr: 137
base_existing_owner_identified: true
industry_benchmark_completed: true
second_project_pilot: NOT_RUN
automated_base_behavior_test: NOT_RUN
base_active_implementation: NOT_STARTED_IN_THIS_STAGE
knowledge_state: PATTERN
```
