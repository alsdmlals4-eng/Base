---
name: analyzing-and-refining-game-concepts
description: Use when a game-design decision crosses concept, positioning, core-loop, feature-rationale, PoC, recalibration, and production stages and needs one coherent sequence with explicit specialist handoffs.
---

# Coordinate Game-Design Lifecycle

## Responsibility

Coordinate a multi-stage game-design decision without duplicating the detailed work owned by focused Skills. Keep one shared fact set, sequence the necessary specialist work, and ensure each result changes the next decision.

Use this Skill only when the request crosses two or more stages. For a single-stage request, route directly:

| Need | Primary Skill |
|---|---|
| Concept, constraints, pointed fun, PoC, recalibration | `developing-game-concepts-and-pocs` |
| Target segment, SWOT, VRIO, positioning | `analyzing-game-positioning-with-swot-vrio` |
| Repeated actions, rewards, decisions, progression | `designing-game-core-loops` |
| Feature or mode rationale and implementable requirements | `writing-traceable-game-design-rationales` |

Use `governing-game-user-research-coverage` for research-governance coverage, `managing-design-documents` for responsibility documents, and `designing-vertical-slices` for representative production proof.

## Lifecycle

`frame → concept → positioning (when strategic choice changes) → core loop → feature rationale → PoC / test → recalibration → production gate`

1. Establish shared facts: target player, player fantasy, production constraints, locked decisions, evidence status, and the decision to make.
2. Run only the specialist stages that can change that decision; retain their stated assumptions, thresholds, and non-goals.
3. Resolve conflicts explicitly: concept promise takes precedence over locally attractive features; evidence takes precedence over sunk effort.
4. Build the smallest PoC or player test that addresses the most expensive unvalidated assumption.
5. Choose `ADVANCE`, `REFINE`, `PIVOT`, or `STOP`; record the production consequence.

## Output contract

Return the ordered specialist outputs, then a short integration decision:

- shared locked facts and assumptions;
- handoffs performed and why;
- contradictions resolved or deferred;
- evidence, threshold, and next smallest test;
- production gate, remaining risk, and owner.

Learning Log: `skills/SKILL_LEARNING_LOG.md`
