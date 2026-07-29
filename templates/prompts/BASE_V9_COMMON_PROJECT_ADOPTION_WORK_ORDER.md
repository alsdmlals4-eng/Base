# Base v9 Common Project Adoption Work Order

## Status: [보류]

This work order is intentionally not an authorization to alter a project. It is
the reusable instruction to use only after the Base RC has been locked and the
user explicitly resumes a named project.

| Project | Status |
| --- | --- |
| Ten Paces: Hidden Moves | [보류] |
| Blacksmith | [보류] |
| OMENWARD | [보류] |
| urban-legend | [보류] |
| GRIMOIRE: 세계를 다시 쓰는 법 | [보류] |

## Resume prerequisites

All prerequisites must be independently confirmed for the chosen project:

1. Base RC lock
2. repository audit
3. Sheet access
4. user approval
5. verification environment

No Sheet write, Sheet creation, repository change, or project-adapter
installation occurs before the five prerequisites are met.

## Approved execution sequence after resumption

1. Read project `AGENTS.md`, current canonical sources, implementation facts,
   and the project-specific Skill Registry.
2. Confirm the actual GDD Sheet URL, permission, tabs, and current state. Treat
   it as `USER_FACING_GDD_WORKSPACE`; classify an unapproved Sheet-only edit as
   `PROPOSED_SHEET_CHANGE`.
3. Audit Base Adapter compatibility and create a deterministic project Skill
   snapshot without copying Base shared Skill bodies.
4. Create a project-scoped PLAN→BUILD→REVIEW contract and validation plan.
5. Apply only the approved project change, test it, and update project canon plus
   Sheet synchronization status.
6. Record project evidence before considering any v9.0.0 final-release decision.
