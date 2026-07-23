---
name: writing-traceable-game-design-rationales
description: Use when turning a game feature, mode, system, content proposal, or design problem into a traceable Why–How–What rationale, implementation-ready specification, necessity review, trade-off decision, or acceptance criteria.
---

# Write Traceable Game Design Rationales

## Responsibility

Make every game-design requirement earn its place. Use this chain:

| Layer | Define | Test |
|---|---|---|
| Why | Player or product issue, desired experience, and behavior to encourage | Would success materially improve the player or project outcome? |
| How | Strategy, mechanism, pacing, and trade-off that can cause the change | Does the method change the player situation in the needed direction? |
| What | Concrete rules, UI, content, tuning, assets, and implementation requirements | Can a teammate build and test it without guessing? |

Trace every `What` upward to one principal `How` and at least one `Why`. Trace every `Why` downward to testable `What` requirements. Delete, defer, or label assumptions that do not complete the chain.

## 1. Frame the decision

Record a continuity snapshot:

- core concept, pointed fun, player fantasy, and core-loop behavior to protect;
- target player, platform, session conditions, production boundary, and non-negotiable constraints;
- existing systems, terminology, and locked decisions;
- decision owner, scope, and what this proposal may not change.

State the issue as a player or product problem, not a preselected feature. Write:

> Because **[observable issue]**, enable **[target player]** to experience **[desired outcome]** and practice **[desired behavior]**, while preserving **[core-direction constraint]**.

Set an observable success condition.

## 2. Develop strategies before features

Generate two or three distinct approaches. For each, state the causal claim:

> If the design provides **[mechanism]** in **[context]**, players can **[behavior]**, leading to **[outcome]** because **[reason]**.

Compare strategies for core-direction fit, player benefit, implementation cost, exploit risk, accessibility, onboarding, live-operation burden, and measurable evidence. Select the smallest set that covers the goal.

## 3. Specify the chosen strategy

Use one row per major requirement.

| Why: issue / goal | How: strategy | What: requirement | Player-facing effect | Rule or dependency | Validation evidence | Non-goal / trade-off |
|---|---|---|---|---|---|---|
|  |  |  |  |  |  |  |

Then define all needed behavior:

1. entry conditions and prerequisites;
2. state transitions, timing, priority, values, and tuning objective;
3. normal, alternate, failure, recovery, and exit flows;
4. UI labels, information hierarchy, feedback, and accessibility needs;
5. content, technical, telemetry, and operation dependencies;
6. acceptance criteria that an implementer and tester can observe.

When rules vary by mode, player state, or difficulty, state precedence explicitly.

## 4. Apply the issue-to-plan pattern

Use the pattern to avoid disconnected method lists.

| Issue | Goal | Strategy | Possible requirement type |
|---|---|---|---|
| New players cannot safely practice varied play patterns | Provide safe, varied practice | Reduce the cost of experimentation and time to meaningful play | access, meaningful start state, recovery, encounter distribution |
| Long sessions cause fatigue | Deliver short, readable sessions | Reduce downtime while preserve consequential moments | traversal, baseline income, objectives, reset protection |
| Existing modes feel monotonous | Offer a distinct form of core expression | Change decisions, not only speed or numbers | objective, spatial pressure, team incentive, progression constraint |

Treat the final column as a design direction. Select only requirements justified by the project’s own core loop and constraints.

## 5. Validate necessity and coherence

For every requirement, check:

1. **Necessity:** What exact goal fails if it is removed?
2. **Causality:** Does it cause the intended behavior or merely make it possible in theory?
3. **Alignment:** Does it intensify or protect the core experience?
4. **Completeness:** Can players enter, understand, choose, succeed, fail, recover, and exit?
5. **Trade-off:** Who benefits, who loses, what scope is added or removed, and what exploit appears?
6. **Falsifiability:** What observation proves the intended behavior did not occur?
7. **Traceability:** Is the Why–How–What link explicit and singular enough to test?

Record each material problem as severity, player scenario, broken link, correction, and new trade-off. Apply corrections only after this review and re-check the affected flow.

## Output contract

Return:

1. decision and continuity snapshot;
2. player issue and design-intent statement;
3. two or three strategy options with recommendation and trade-offs;
4. Why–How–What table;
5. rules, player flow, dependencies, and acceptance criteria;
6. necessity and adversarial findings with revisions;
7. locked decisions, open risks, and the smallest next test or production artifact.

Learning Log: `skills/SKILL_LEARNING_LOG.md`
