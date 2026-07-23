---
name: developing-game-concepts-and-pocs
description: Use when discovering or revising a game's core concept, constraints, pointed fun, feature alignment, proof of concept, post-test recalibration, or production-readiness decision.
---

# Develop Game Concepts and POCs

## Responsibility

Turn an early game idea into a testable direction with a clear reason for repeat play. Own the sequence:

`concept → constraints → pointed-fun hypothesis → element alignment → PoC → recalibration → production decision`.

Do not replace market-positioning analysis, detailed core-loop design, or feature-level Why–How–What specification. Route those to `analyzing-game-positioning-with-swot-vrio`, `designing-game-core-loops`, and `writing-traceable-game-design-rationales` once the relevant decision is ready.

## Required frame

Record the following before selecting a direction:

| Field | Required decision |
|---|---|
| Target player and play context | Who plays, on what platform, for how long, and in what situation |
| Player fantasy | Repeated role, feeling, or mastery the player seeks |
| Signature action | What the player repeatedly does that expresses the fantasy |
| Constraints | Experience, platform, team, budget, schedule, technical, content, and prohibited directions |
| Production boundary | What can be tested now versus what cannot be assumed |
| Decision target | The specific choice this work must make |

State facts, assumptions, hypotheses, and locked decisions separately.

## Workflow

### 1. Form the concept

Write one testable sentence:

> For **[target player]**, this game repeatedly delivers **[distinct feeling or mastery]** by having them **[signature action]** under **[meaningful pressure or limitation]**.

A genre, setting, art style, or list of features is not a core concept unless it changes repeated player action and feeling.

### 2. Turn constraints into tests

Translate every adjective or condition into player-facing evidence.

| Constraint | Observable evidence | Design implication | Failure signal |
|---|---|---|---|
|  |  |  |  |

Resolve conflicts explicitly. For example, a heavy action game may preserve commitment and readable impact over maximum cancellation freedom; an audio-led game must make sound change a real decision, not only atmosphere.

### 3. Select pointed fun

Generate at least three hypotheses:

> The player returns to **[repeatable situation]** because they can **[unusual agency or mastery]**, creating **[felt payoff]**.

Score each for repeatability, distinctiveness, constraint fit, decision density, communicability, and PoC feasibility. Choose one primary hypothesis, one supporting appeal, and record rejected alternatives with their trade-off.

### 4. Align the game

Classify every proposed element as `AMPLIFY`, `SUPPORT`, `NEUTRAL`, `CONFLICT`, or `UNPROVEN`.

| Element | Contribution to pointed fun | Classification | Keep / change / cut / defer |
|---|---|---|---|
| Player verbs |  |  |  |
| Encounters and content |  |  |  |
| Progression and rewards |  |  |  |
| Narrative, art, and sound |  |  |  |
| UI and controls |  |  |  |

Keep an element only when it intensifies, varies, teaches, or protects the selected appeal, or solves a proven production requirement.

### 5. Contract the PoC

Build the smallest interactive slice that can falsify the riskiest assumption.

| Field | Define |
|---|---|
| Hypothesis | Expected player feeling, behavior, or choice |
| Test scene | Smallest repeatable situation that exposes it |
| Included variables | Player action, obstacle, feedback, and one meaningful variation |
| Excluded variables | Content breadth, polish, progression, or narrative that could hide the result |
| Participants and task | Target player, prior exposure, task, and facilitator boundary |
| Evidence | Observable behavior, qualitative questions, and instrumentation if applicable |
| Success threshold | Evidence required to advance |
| Falsification rule | Evidence that requires refine, pivot, or stop |
| Decision owner and date | Who decides and when |

Freeze success criteria before testing. Do not let novelty, presentation, or facilitator explanation substitute for the intended interaction.

### 6. Recalibrate and gate production

Compare observed evidence with the predeclared hypothesis, then choose exactly one:

- `ADVANCE`: preserve the validated premise and hand off the selected core loop and production pillars.
- `REFINE`: change the smallest uncertain variable and run a focused PoC.
- `PIVOT`: replace the pointed-fun hypothesis.
- `STOP`: do not scale an unvalidated or infeasible appeal.

Record the evidence, changed assumption, scope consequence, and next smallest artifact. Enter production only when the core experience is evidenced; a complete document is not evidence.

## Adversarial review

Try to disprove the direction:

- Remove setting and marketing language: is the repeated play still distinct?
- Remove one proposed feature: does the pointed fun disappear, or was the feature arbitrary?
- Ask what changes after the first five minutes; identify the new decision, mastery, or pressure.
- Check whether a constraint became decoration instead of a rule that shapes play.
- Identify the most expensive unvalidated assumption and ensure the PoC tests it first.
- Check whether production scope exceeds the evidence gained.

For every material finding, record severity, player scenario, correction, and new trade-off.

## Output contract

Return:

1. concept and target-player sentence;
2. constraint-to-test table;
3. ranked pointed-fun hypotheses and chosen direction;
4. feature-alignment decisions;
5. PoC contract with falsification rule;
6. post-PoC decision and production gate;
7. validated assumptions, unproven risks, and next owner.

Learning Log: `skills/SKILL_LEARNING_LOG.md`
