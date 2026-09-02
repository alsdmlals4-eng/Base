# Evidence-Based Work-Loop Operational Projection Design

## Decision and approval

- **Decision:** Adopt the user-provided `READ → PICK → BUILD → CHECK → COMMIT` model as a small, evidence-based operational projection over the existing Base project-work card, Issue/Goal lifecycle, continuous-work queue, and verification gates.
- **Approval:** The user explicitly approved promotion, absorption, and protected merge in this chat on 2026-09-02 after the alternatives and no-second-canon recommendation were presented.
- **Current Base-change locator:** This design and its paired implementation plan are the durable direct-user-approved record for this bounded Base policy change. The normal protected PR, once published, is its integration record; Base Issue #825 remains historical evidence for the earlier PM execution-gate implementation and is not this change's current work authority.
- **Scope:** Base shared workflow and templates only. No game repository, Godot scene, runtime code, asset, workflow permission, paid service, Project board, or external PM product is created or changed.

## Problem

The reference workflow makes the current task, selected work, verification, and handoff easy to see. Base already has the underlying evidence system, but its six-section handoff does not name the small loop or explicitly map the four reference document roles. That leaves room for two unsafe readings:

1. creating four new canonical files (`PROMPT.md`, `DESIGN.md`, `INBOX.md`, `STATUS.md`) for every project; or
2. treating a checkpoint commit, a source checklist, a visual capture, or repeated loops as proof of completion or automatically improving quality.

## Research and alternative comparison

| Alternative | Decision | Evidence and trade-off |
|---|---|---|
| Require four standalone `PROMPT.md` / `DESIGN.md` / `INBOX.md` / `STATUS.md` files | **REJECT** | It duplicates current repository owners and violates the existing derived-card, Active Context, and accepted-decision boundaries. It also adds context loading and stale-copy risk. |
| Add a new dashboard, PM service, scheduler, or global workflow Skill | **REJECT** | The existing receipt validator, markdown renderer, Issue hierarchy, WIP limits, and continuous-work recovery already provide the execution boundary. A new product would add a second state store without solving an evidence gap. |
| Extend the existing work-card handoff and lifecycle policy with a thin projection | **ADOPT** | Preserves one canonical source per fact while making the current loop readable. It fits the existing project receipt, continuous queue, progressive loading, protected PR route, and evidence matrix. |

The user-provided visual reference supplies the desired small-loop ergonomics. The existing Base implementation supplies the stronger safety boundaries. The Scrum Guide supports visible work, inspection, and adaptation rather than a claim that every iteration succeeds; GitHub Issues supports task/idea tracking and optional hierarchy rather than a required duplicate board. GitHub protected branches support requirements such as checks and linear history, so the final `COMMIT` step cannot replace the normal PR gate.

## Ownership model

The five labels are responsibilities, not required files:

| Reference label | Existing owner and required behavior |
|---|---|
| `PROMPT` | The approved work contract / Goal / card scope and acceptance criteria. A short task entry may point to these sources, but it is not a permanent all-context file. |
| `DESIGN` | The existing registered design, decision, blueprint, wireframe, flow-map, or implementation owner. It is loaded only when the selected work requires it. |
| `INBOX` | Untriaged user input recorded through the existing Issue, goal backlog, or current-context route. It is not execution authority: each request is first classified `ADOPT`, `ADAPT`, `REJECT`, `DEFER`, or `USER_DECISION_REQUIRED` and then attached to an approved work item if in scope. |
| `STATUS` | The existing Active Context plus the derived `project_work_kanban` receipt, including exact source/head, WIP, blockers, evidence, and the next safe action. |
| `guide/*` | Existing progressive-load references selected only by the actual owner, consumer, risk, or verification need. They do not override the canonical design or task contract. |

No Base or project installation creates four files by default.

## Operational loop

```text
READ
→ PICK
→ BUILD
→ CHECK
→ COMMIT
→ (correction or next approved work)
```

1. **READ** — Fresh-read the current repository authority, active Context, approved Goal, actual consumer, exact source revision, related PRs, required benchmark/hygiene receipt, and only the relevant design or guide owner. A missing required source or failed receipt is `BLOCKED_UNVERIFIED`, not a prompt to guess.
2. **PICK** — Triage any new inbox input before execution. Reconcile remaining work, dependency, blocker, WIP, and scope; then select exactly one existing or newly necessary approved work item as `IN_PROGRESS` or `VERIFY_REVIEW`. A request cannot leap from inbox to implementation solely because it is recent.
3. **BUILD** — Make the smallest real change within the approved work item. Load a design guide only when its registered owner is needed. Preserve project-local variable owners and fixed compatibility/security boundaries; do not generalize a project-specific UI, world, menu, or benchmark conclusion.
4. **CHECK** — First run applicable contract/static/automatic checks. Then perform required runtime, visual capture, and machine/agent screen inspection at the actual consumer. A capture is evidence for a runtime or visual level only; it is not Human/Player approval. `E6_HUMAN_PLAYTEST` is performed only when the user explicitly asks or declares that review.
5. **COMMIT** — A checkpoint commit is allowed only after it carries verified partial work and records the remaining evidence. It remains `IN_PROGRESS` or `VERIFY_REVIEW`. A final completion commit still requires exact-head PR checks, independent review, unresolved-thread zero, normal protected merge, merged-main readback, and closeout when those are in the approved denominator.

The loop outcome is never assumed to increase quality. It must be recorded as `PASS`, `PARTIAL`, `FAIL`, `BLOCKED_UNVERIFIED`, or an existing work-item status with evidence. If the same verification produces no new evidence or the acceptance gap persists, the next action is diagnosis, a bounded correction, local defer, or a user decision—not unbounded repetition.

## Required contract changes

1. Add the projection vocabulary and the role mapping to `PROJECT_WORK_ITEM_CHECKLIST.md` section 11, which already owns the fresh-session handoff and checkpoint boundary.
2. Add a concise lifecycle-policy pointer in `GITHUB_WORK_ITEM_LIFECYCLE_POLICY.md` section 14 so project work cards are known to use the projection without duplicating its full procedure.
3. Extend the existing work-card contract test to prove the policy routes to the card and the card preserves all loop, evidence, no-second-canon, and Human-review boundaries.
4. Do not change receipt JSON shape, the renderer, a project adapter, GitHub Project configuration, CI workflow topology, or any open PR.

## Acceptance criteria

- `READ`, `PICK`, `BUILD`, `CHECK`, and `COMMIT` are defined as evidence-bearing responsibilities on the existing card.
- The mapping for `PROMPT`, `DESIGN`, `INBOX`, `STATUS`, and `guide/*` identifies existing owners and says that new default canonical files are not created.
- Inbox triage precedes execution; WIP and approved-scope selection remain intact.
- Functional/static/automated checks, runtime/visual capture, and explicit Human/Player review remain separate evidence levels.
- Checkpoint and final protected-merge completion are distinct.
- The contract explicitly forbids an automatic “quality goes up each loop” conclusion and unbounded repetition.
- The focused contract regression and full local validation succeed after implementation; normal protected-branch PR checks, review, and post-merge readback remain mandatory for merge completion.

## Non-goals and rollback

- No universal menu, button, genre, world, art direction, soft-coded value set, or wireframe is prescribed. Those remain project-specific outputs of fresh-read and benchmark work.
- No existing project receives an empty card, Issue, board, or new context files as a fleet rollout.
- No new Skill, package, service, scheduler, dashboard, or paid tool is introduced.
- Rollback is a single revert of the shared-policy/template/test change. Existing project owners, receipts, and the retained open PRs remain untouched.

## Evidence ceiling

This Base change can prove the shared routing and regression contract only. It does not prove any project has adopted it, that a Godot game runs, that a captured screen is aesthetically accepted, or that Human/Player, device, accessibility, performance, rights, or release gates have passed.
