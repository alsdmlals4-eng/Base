---
name: designing-game-core-loops
description: Use when defining, repairing, or testing a game's core loop, repeated player actions, rewards, choices, progression, resource economy, session structure, return trigger, or repeat-play motivation.
---

# Design Game Core Loops

## Responsibility

Define the smallest repeatable exchange that creates the next meaningful action:

`action → resolution → feedback / reward or consequence → decision → changed possibility or pressure`.

A genre, feature list, tutorial sequence, or number increase is not a core loop until the recurring player action, consequence, and next decision are explicit. Use `developing-game-concepts-and-pocs` first when the sharp fun is uncertain.

## Establish the promise and scales

State the one-sentence core-loop promise: why this player chooses the next action.

Define each applicable scale independently.

| Scale | Duration | Trigger | Goal | Repeat boundary | Exit / reinvestment |
|---|---:|---|---|---|---|
| Moment loop | seconds to a minute |  |  |  |  |
| Session loop | minutes to an hour |  |  |  |  |
| Meta loop | multiple sessions |  |  |  |  |

Do not merge loops with different cadence or decisions simply to make one large diagram.

## Build the action–reward–decision chain

Use observable verbs and state changes.

| Step | Player action | Input / cost / risk | Resolution and feedback | Reward or consequence | Next decision | Progress effect |
|---|---|---|---|---|---|---|
|  |  |  |  |  |  |  |

Confirm each link:

1. The player has a legible reason to act now.
2. The action contains timing, strategy, execution, or information use.
3. The result is quickly readable and attributable to player choice.
4. The reward changes capability, information, access, status, or strategic position.
5. That change creates a desirable next choice, challenge, or goal.

If a step does not alter the next decision, classify it as presentation, friction, or a different loop rather than core progression.

## Specify the anchors

For every repeated loop, define:

- **Action:** verb, target, cadence, mastery, alternatives, and failure mode.
- **Feedback:** immediate sensory or informational result and its attribution.
- **Reward / consequence:** source, amount, certainty, variability, loss condition, cadence, and player value.
- **Progress:** what expands—options, competence, access, knowledge, social standing, or leverage—not merely numbers.
- **Return trigger:** unfinished goal, unlocked possibility, challenge, evolving world, collection, social commitment, or another honest reason to return.

## Connect economy and challenge

Trace each meaningful resource.

| Resource or reward | Earned by | Spent or risked on | Decision changed | Source cadence | Sink cadence | Hoarding / inflation / dominant-strategy risk |
|---|---|---|---|---|---|---|
|  |  |  |  |  |  |  |

For random, idle, gacha, crafting, or live-service systems, specify guaranteed progress, randomness boundaries, duplicate handling, protection rules, and an agency-preserving response to bad outcomes.

## Design variation without identity loss

For each variation, define the invariant—the action and feeling that must remain recognizable.

| Variation source | New decision or pressure | Core invariant protected | Cut condition |
|---|---|---|---|
| Enemy, map, objective, input context, build, route, stakes, or information |  |  |  |

Use variation to deepen the same promise, not to replace it every few minutes.

## Test before scaling

Build one full moment loop and enough session context to test reinvestment.

| Hypothesis | Observable behavior | Player question | Success threshold | Failure interpretation | Next change |
|---|---|---|---|---|---|
|  |  |  |  |  |  |

Observe voluntary repeats, build or route changes, ability to explain the next goal, response to failure, reward-spending choices, and willingness to continue after novelty fades.

## Adversarial review

Test for:

- **Grind:** no evolving decision, skill, or consequence.
- **Reward fog:** players cannot explain cause, reward, or value.
- **Dead reward:** reward does not change a meaningful next choice.
- **Dominant strategy:** one action, build, or spend path erases alternatives.
- **Progress trap:** larger numbers remove challenges or decisions.
- **Disconnection:** combat, economy, story, and meta systems reward incompatible behavior.
- **Novelty collapse:** nothing deepens after the first five minutes.
- **Punishing exit:** returning relies on avoidable loss rather than desire.

Record scenario, severity, correction, and trade-off for every material issue; rerun the affected chain after correction.

## Output contract

Return:

1. core-loop promise;
2. moment, session, and meta-loop definitions;
3. action–reward–decision–progress table;
4. resource and challenge links;
5. variation rules and non-goals;
6. prototype test plan;
7. validated assumptions, risks, and next required specification.

Learning Log: `skills/SKILL_LEARNING_LOG.md`
