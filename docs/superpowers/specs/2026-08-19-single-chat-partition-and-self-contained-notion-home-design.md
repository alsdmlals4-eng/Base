# Single-Chat Partition & Self-Contained Notion Home Design

## Decision

Base remains **ONE BASE** with stable P01..P09 responsibility/learning views, but future full Base optimization runs use **one GPT chat that executes P01 → P09 sequentially**. Partition IDs remain useful for focus, learning, source routing, attribution, and checkpoints; they are no longer hard write barriers between responsibilities inside the same authorized Base maintenance run.

## Why

The previous one-chat-per-Part design reduced collision risk but created handoff overhead and repeatedly converted cross-Part findings into deferred requests even when the current authorized maintenance run could safely fix them. The new model preserves focused Part checkpoints while reducing context loss and deadlocks.

## Operating alternatives considered

1. **Keep nine independent worker chats.** Lowest direct collision risk, but highest handoff cost and repeated cross-Part deadlock. Rejected.
2. **One sequential coordinator chat with stable Part checkpoints and cross-Part repair authority.** Keeps deep domain passes, learning logs, and attribution while allowing discovered overlaps to be fixed in the same run. **Adopted.**
3. **Remove Partitions entirely and audit Base as one undifferentiated scope.** Simplest routing but loses depth tracking, source-learning specialization, and responsibility maps. Rejected.

Revisit the selected model if one chat cannot hold practical context, cross-Part changes become too large to review safely, or concurrent human/agent writers become routine.

## Sequential execution model

```text
latest completed main
→ P01 focus / repair / checkpoint
→ sync latest completed main
→ P02 focus / repair / checkpoint
→ ...
→ P09 focus / repair / checkpoint
→ whole-Base Integration
→ minimum 5 full adversarial improvement loops
→ continue until CLEAN_REVIEW_EXIT
→ merge / post-merge readback
```

A Part defines the **primary responsibility being inspected**, not an absolute prohibition on correcting another responsibility. When a Pxx pass detects a valid cross-Part or CP0 defect, the same authorized coordinator may fix it directly if all of the following hold:

- the target is not owned by an unrelated open/draft/ready workstream;
- the semantic owner and consumers are identified;
- the change is necessary for the current Base goal or regression closure;
- companion tests/references are updated under the real owner;
- changed paths and reasons are attributed in the checkpoint/report;
- exact-head regression and rollback remain possible.

`CROSS_PART_CHANGE_REQUEST` remains useful for unresolved, concurrently-owned, destructive, or separately-authorized changes, but it is no longer the mandatory response to every cross-Part finding.

## Independent workstream protection

The permission above does **not** authorize mutation of unrelated active PRs/branches/worktrees. Open/draft/ready workstreams remain read-only unless the user explicitly transfers or expands ownership. Completed/merged main is the normal integration surface.

## Notion human-facing contract

Base Home and every Project Home must be **self-contained for human understanding**. A user should not need to open child pages just to understand the current project/system.

Base Home directly explains:

- what Base is and how the operating lifecycle works;
- important rules and why/when they activate;
- active Skills/Modes with purpose, trigger, process, output, expected effect, and related module/test;
- module flow with each stage's responsibility, input, output, and failure impact;
- P01..P09 responsibilities, sequence, important Skills, dependencies, and expected effect;
- current status, evidence limits, active risks, and next work.

Project Home directly explains:

- current direction/status and evidence freshness;
- player/user promise and core loop;
- major systems and how they connect;
- UX/UI and visual direction/status;
- implementation/runtime state and evidence ceiling;
- important decisions, risks/blockers, and next work.

Child pages remain deep evidence/data/editing surfaces. They are **not required navigation for basic understanding**.

Unknown/new projects use explicit `UNVERIFIED`, `NOT_DEFINED`, or `IN_PROGRESS` states instead of invented design.

## Adversarial review correction

`FULL_LOOP_COUNT_MINIMUM: 5` means **five complete full-scope improvement lifecycles**, not five review lenses.

Invalid interpretation:

```text
Loop 1 = scope only
Loop 2 = UX only
Loop 3 = consumers only
Loop 4 = alternatives only
Loop 5 = CI only
```

Those five lenses together are at most inputs to a full review; they do not satisfy five full loops.

Every counted loop must re-run the complete lifecycle over the entire approved state:

```text
CURRENT STATE / CANON / SCOPE
→ minimum 3 materially distinct alternatives where a material decision exists
→ ATTACK whole state
→ VALIDATE findings
→ FIX/REFINE approved findings
→ VERIFY / REGRESSION
→ BETTER_ALTERNATIVE_SEARCH
→ LONG_TERM_PLAN_FIT_RECHECK
→ RE-ATTACK resulting whole state
```

A loop may report its most important newly found issue, but the label must not imply that only one lens was reviewed.

Exit requires at least five counted full loops and then zero new valid blockers, zero regressions, acceptance satisfied, canon/reference freshness closed, and evidence ceilings preserved.

## Tetris onboarding

`alsdmlals4-eng/Tetris` is a newly created game repository and is currently in production. Its Notion Project Registry entry and Project Home must be created without inventing missing design/runtime facts. Until repository/project canon appears, the Home should state that core loop, systems, visual direction, runtime evidence, and next implementation details are not yet verified/defined.
