# Sequential Partition, Cross-Part Repair, Notion Full-View, and Full-Scope Adversarial Review Design

## Goal

Keep P01~P09 as stable responsibility/learning lenses, but run them sequentially in one coordinator chat, allow validated cross-Part repairs during the same work when ownership is clear and no independent active workstream is being mutated, make Notion main/project Home pages self-sufficient for human learning, and prohibit treating five adversarial review lenses as five full review loops.

## Approved operating model

- One coordinator chat runs P01 → P09 sequentially.
- Each Part remains a responsibility, learning, source-discovery, and completion-report unit.
- Part boundaries no longer mean "detected issue must not be fixed".
- If a validated issue belongs to another Part or CP0 and the current coordinator has authority, the same work may repair it directly with provenance and regression coverage.
- An independent open/draft/ready PR or foreign active workstream remains protected from mutation. Detection is allowed; direct mutation of that active workstream is not.
- Prefer one Part-sized PR at a time: finish/merge P01, re-pin latest main, continue P02, etc. Integration/cleanup may use a dedicated coordinator PR when several completed-Part findings must be reconciled atomically.

## Cross-Part repair rule

`PART_BOUNDARY_IS_ANALYSIS_AND_ACCOUNTABILITY_NOT_A_FIX_PROHIBITION`

A cross-Part finding may be fixed in the current coordinator work when all are true:

1. the finding is validated and within the approved Base goal;
2. canonical owner and affected consumers/tests are known;
3. no independent open/draft/ready workstream already owns the same semantic change;
4. the repair does not silently change game/project direction requiring user decision;
5. actual changed paths, owner reason, regression tests, and rollback are recorded.

If an independent active workstream already owns the semantic change, record the conflict/dependency and do not mutate that workstream.

## Notion human-facing completeness

`NOTION_MAIN_VIEW_MUST_BE_HUMAN_COMPLETE`

Base and project main/Home pages must allow a human to understand the operating/project state without opening child pages for essential context. Child pages remain detailed evidence/data/log surfaces, not required reading for the basic mental model.

Base main must directly explain:

- what Base is and its authority split;
- end-to-end module flow and why each step exists;
- every active Skill or grouped active Skill family with purpose, trigger, process, outputs, expected effect, major dependencies/tests;
- P01~P09 responsibilities, inputs, outputs, representative Skills/Modules, interactions, and failure risks;
- adversarial review contract;
- current work state, verification/evidence ceilings, learning/source loop, and legacy policy.

Project Home must directly expose, when applicable:

- project identity and current direction;
- player/user promise and core loop;
- major systems and how they interact;
- UX/UI and visual direction;
- current implementation/runtime state;
- validation/evidence state and NOT_RUN boundaries;
- current decisions, blockers/risks, and next work;
- authority/source locations.

Links to detailed pages may remain, but the essential explanation must be duplicated as a human-facing summary rather than hidden behind navigation.

## Adversarial review correction

`FULL_LOOP_IS_NOT_A_REVIEW_LENS`

A full adversarial loop is the complete lifecycle over the whole approved scope:

`CURRENT_STATE → ≥3 REAL ALTERNATIVES → ATTACK WHOLE STATE → VALIDATE FINDINGS → FIX/REFINE → VERIFY/REGRESSION → BETTER_ALTERNATIVE_SEARCH → LONG_TERM_FIT_RECHECK → RE-ATTACK WHOLE RESULT`

The following does **not** satisfy five full loops:

- Loop 1 = scope only
- Loop 2 = UX only
- Loop 3 = consumers only
- Loop 4 = CI only
- Loop 5 = rollback only

Those are review lenses inside a loop. Every counted loop must cover the whole scope. A completion report may mention the dominant finding in each loop but must state that the full lifecycle and whole-scope review were repeated.

Minimum is five complete loops; after loop 5 continue until new valid errors/conflicts/omissions/blockers are zero, regressions are zero, acceptance/canon/evidence conditions are satisfied.

## Current integration boundary

Merged completed work may be integrated from main. Current open/draft/ready PRs such as P03/P08 remain independent active workstreams and are not rewritten, rebased, merged, closed, or absorbed by this policy-refactor branch unless separately authorized after their own completion state changes.

## Long-term fit

This design keeps stable Part vocabulary and learning/source routing while removing multi-chat handoff overhead and cross-Part deadlocks. Revisit if one-chat P01~P09 runs exceed practical context, cross-Part fixes repeatedly create attribution ambiguity, or independent concurrent workers become common enough that strict write partitions again reduce more conflict than they create.
