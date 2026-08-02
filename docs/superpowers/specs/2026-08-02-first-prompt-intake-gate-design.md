# First-Prompt Intake Gate Design

## Goal

Extend the existing prompt-contract owner so every L1+ instruction-writing workflow starts with a direction-setting sentence, becomes an executable prompt contract, passes a Grill Me alignment gate, and only then proceeds to execution.

## Existing ownership

- `managing-project-intake-and-work-contract` remains the single owner for request routing, clarification, prompt conversion, work contracts, and approval state.
- `AI_INSTRUCTION_AND_CONTEXT_DESIGN_METHOD.md` remains the reusable method for instruction authority, Interface-first prompts, context curation, fixtures, and artifact claim limits.
- `simplifying-skill-bodies` continues to own progressive disclosure and fixture preservation.
- No new broad Skill or Registry entry is added.

The legacy name `transforming-requests-into-prompts` and user-facing names such as `[좋은 프롬프트]`, `퍼스트 프롬프트`, and `first prompt` route to the existing intake Skill.

## Core concept: direction anchor

A generated instruction begins with a short **direction anchor**: the smallest sentence or pair of sentences that states the primary task, intended outcome, and dominant decision criterion.

The anchor is placed at the front of the user-authored prompt so the remaining context is interpreted through the correct task frame. Placement increases salience but does not change authority. It cannot override system instructions, repository rules, approved canon, safety boundaries, or a later explicit hard constraint.

Example shape:

```text
[Direction anchor]
Create an implementation-ready plan that preserves the approved project core and closes the verified planning gaps before any code change.

[Task and success]
...
[Context and sources]
...
[Constraints and protected scope]
...
[Output contract and validation]
...
```

## First-prompt structure

The `first-prompt` mode composes the prompt in this order:

1. `DIRECTION_ANCHOR`: primary action, intended outcome, dominant criterion.
2. `TASK_AND_SUCCESS`: concrete task, audience or player value, completion condition.
3. `CONTEXT_AND_SOURCES`: current facts, canonical sources, actual files, freshness and conflicts.
4. `CONSTRAINTS_AND_PROTECTED_SCOPE`: hard constraints, exclusions, invariants, permissions and rollback boundary.
5. `OUTPUT_AND_VALIDATION`: required artifact, status vocabulary, tests, evidence and unverified reporting.
6. `OPTIONAL_RESPONSE_DIVERSIFICATION`: when a decision benefits from exploration, request a conventional option, a bold option, and an integrated option, then compare them under one criterion set and recommend one.

The structure absorbs three useful prompt practices:

- explicit instructions and clear instruction/context separation;
- Task, Context, Source, Constraints, Output and Validation coverage;
- deliberate first-answer diversification for design or decision work instead of accepting one predictable draft.

Diversification is conditional. Mechanical edits, fixed-format transformations, and already-approved implementation steps do not generate artificial alternatives.

## Mandatory workflow

```text
request
→ managing-project-intake-and-work-contract: route
→ repository and decision inspection
→ first-prompt
→ contract
→ Grill Me alignment gate
→ CONFIRMED
→ BUILD or delegated execution
→ REVIEW and execution report
```

Every L1+ instruction-writing request passes through the intake Skill. The Grill Me alignment gate always runs, but its visible interaction depends on existing evidence:

- material intent, planning, scope, priority, or canon uncertainty: ask one high-leverage Grill Me question at a time;
- complete but not yet approved contract: present the direction anchor and contract summary for one explicit confirmation;
- exact contract already approved in the current work item: reuse the approval reference and do not repeat the question;
- L0 typo, obvious formatting correction, or identical validation rerun: no interview is required.

Execution remains blocked as `AWAITING_USER_CONFIRMATION` when the generated instruction could materially change planning or implementation and no valid approval reference exists.

## Conflict and quality controls

The first-prompt pass must check:

- the anchor matches the full contract rather than narrowing or exaggerating it;
- later constraints do not contradict the anchor;
- priority words such as “always”, “only”, “must”, and “never” have the correct authority;
- context and examples do not silently replace canonical sources;
- the anchor does not hide exclusions, uncertainty, or user decisions;
- alternatives use the same evaluation criteria and preserve counterevidence;
- the prompt states what was not verified.

A front-loaded sentence is not a substitute for Interface-first completeness. A prompt fails if it has a strong opening but lacks source authority, protected scope, output contract, failure conditions, or validation.

## Files and propagation

Modify:

- `AGENTS.md`
- `skills/managing-project-intake-and-work-contract/SKILL.md`
- `skills/managing-project-intake-and-work-contract/references/first-prompt-direction-anchoring.md`
- `docs/knowledge/game-development/AI_INSTRUCTION_AND_CONTEXT_DESIGN_METHOD.md`
- `skills/LEGACY_SKILL_ALIASES.md`
- `tests/test_first_prompt_intake_contract.py`

Record the design and implementation plan under `docs/superpowers/`.

Do not modify:

- `skills/SKILL_REGISTRY.json`
- released locks or frozen/generated release artifacts
- project repositories or Google Sheets
- open prompt PR files unrelated to this owner

## Verification

Focused tests must prove:

- the existing intake Skill owns `first-prompt`;
- the direction anchor is front-loaded but authority-safe;
- Task/Context/Source/Constraints/Output/Validation and optional three-way exploration are present;
- every L1+ instruction workflow reaches the Grill Me alignment gate before execution;
- approved exact contracts do not trigger duplicate questioning;
- L0 and identical rerun exceptions remain intact;
- legacy names route to the existing Skill instead of creating a new Skill.

Repository CI and canonical-reference checks remain the final executable evidence. Actual cross-model prompt-quality improvement and human comprehension remain `NOT_RUN` until separately evaluated.
