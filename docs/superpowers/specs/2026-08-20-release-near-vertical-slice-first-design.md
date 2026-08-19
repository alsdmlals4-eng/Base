# Release-Near Vertical Slice First — Design

- Status: **APPROVED_BY_CURRENT_USER_SCOPE**
- Date: 2026-08-20
- Baseline main: `c8de06cdd63ddcb9121d8321bf135eaea9e14f06`
- Goal: gameplay/player-experience validation must use a short, shipping-intent Vertical Slice rather than a system-only PoC.

## 1. Problem

Base already owns `DEMO_FIRST_VERTICAL_SLICE` and rejects a separate `CORE_POC` product stage, but active higher-level policies still expose `VISUALIZED_POC_BEFORE_DEMO_TEST`, `VISUAL_NOT_MATERIAL_TO_THIS_POC`, `POC_BUILD_AND_TEST`, and minimum-PoC language. A project can therefore still drift into system-first grey-box gameplay validation even though the desired production target is a short near-release-quality slice.

The user explicitly rejects that workflow because a system-only PoC does not provide enough immersion to judge the game as a product.

## 2. Alternatives

### A. Strengthen only `VISUALIZED_POC_BEFORE_DEMO_TEST`

Keep PoC as the normal gameplay validation stage and require more visuals.

- Advantage: smallest edit.
- Failure: still legitimizes system-first gameplay validation and leaves audio/VFX/product quality optional.
- Decision: REJECT.

### B. Rename PoC to Vertical Slice

Replace terminology but keep the existing optional quality gates.

- Advantage: low migration cost.
- Failure: semantic rename does not ensure shipping-intent UI, image/art, audio, VFX, systems, integration, or player-appeal evidence.
- Decision: REJECT.

### C. `RELEASE_NEAR_VERTICAL_SLICE_FIRST`

Use a short, representative, shipping-intent Vertical Slice as the first gameplay/player-experience validation product. Narrow technical spikes remain permitted only for isolated feasibility questions and cannot validate fun, immersion, readability, pacing, identity, or overall player experience.

- Advantage: aligns evaluation with the actual game experience and existing Demo-First authority.
- Cost: more front-loaded art/audio/UI/VFX work before the first player-experience test.
- Mitigation: keep the slice short; reuse/adapt existing proven assets and patterns; use technical spikes only when a blocking technical uncertainty would otherwise waste the integrated slice.
- Decision: **SELECTED**.

## 3. Canonical contracts

```text
RELEASE_NEAR_VERTICAL_SLICE_FIRST
GAMEPLAY_VALIDATION_REQUIRES_SHIPPING_INTENT_SLICE
SYSTEM_ONLY_POC_NOT_PLAYER_EXPERIENCE_EVIDENCE
TECHNICAL_SPIKE_INTERNAL_ONLY
SHIPPING_INTENT_UI_IMAGE_AUDIO_VFX_SYSTEM_REQUIRED
EXISTING_SOLUTION_FIRST_ADAPT_TO_PROJECT
PLAYER_APPEAL_QUALITY_GATE
```

### `RELEASE_NEAR_VERTICAL_SLICE_FIRST`

Normal game production direction is:

```text
concept / project core
→ current-state + complete-game / asset / UX / audio / VFX benchmarks
→ >= 3 alternatives + ADOPT / ADAPT / REJECT
→ originality / DDD / coherence / complexity / approachability gate
→ short Vertical Slice contract
→ shipping-intent UI / image-art / audio / VFX / systems / representative content
→ integrated implementation
→ runtime QA
→ human playtest
→ recalibration / production decision
```

It is **not**:

```text
system-only PoC
→ gameplay validation claim
→ gradually add UI / art / sound / effects later
```

### `GAMEPLAY_VALIDATION_REQUIRES_SHIPPING_INTENT_SLICE`

A build used to judge fun, immersion, readability, pacing, emotional response, distinctive identity, or overall player experience must include the actual intended experience for the selected short segment:

- production-intent UI and UX flow;
- production-intent images/art/background/characters needed by the segment;
- representative animation and VFX;
- representative music and SFX plus required alternative feedback channels;
- real core systems and data interactions;
- representative onboarding/feedback/recovery states;
- enough content to complete the short slice from entry to outcome.

“Shipping-intent” means intended to survive into the product unless later evidence changes it. It does not require the whole game's total content volume or every final polish item.

### `SYSTEM_ONLY_POC_NOT_PLAYER_EXPERIENCE_EVIDENCE`

A grey-box, logic harness, rule simulator, unit test, dummy scene, or system-only PoC may prove technical/rule feasibility only. It cannot be cited as evidence that the game is fun, immersive, readable, appropriately difficult, visually coherent, distinctive, or satisfying.

### `TECHNICAL_SPIKE_INTERNAL_ONLY`

A narrow technical spike is allowed when one technical uncertainty would otherwise make integrated Slice production wasteful. It must have one question, bounded output, stop condition, evidence ceiling, and explicit integration/rejection path. It is not a product stage and is never the first player-experience acceptance gate.

## 4. Existing-solution-first production acceleration

Use complete shipped games, mature UI/UX patterns, licensed/owned asset packs, existing project assets, audio/VFX libraries, Godot capabilities/plugins, and other proven references to establish a fast baseline before custom-building everything.

```text
reference / existing solution
→ provenance / rights / version / platform fit
→ transferable principle
→ ADOPT / ADAPT / REFERENCE_ONLY / AVOID / REJECT
→ project-specific transformation
→ originality / coherence / rights review
→ integrated Slice
```

Default is `ADAPT`, not copy. A faster alternative may replace this route when it has better total time, quality, rights, maintainability, project fit, and rollback characteristics.

## 5. Player Appeal Quality Gate

Before the integrated Slice is treated as ready for human playtest, evaluate:

```yaml
originality:
  distinctive_player_reason:
  complete_game_comparisons: []
  similarity_or_derivative_risk:
ddd:
  first_meaningful_reward_time:
  action_feedback_latency:
  reward_clarity_and_density:
  micro_session_meta_ladder:
  fatigue_and_inflation_risk:
consistency:
  visual_audio_system_world_fantasy_alignment:
complexity:
  rules_to_learn:
  simultaneous_attention_burden:
  avoidable_complexity:
difficulty_and_approachability:
  novice_comprehension:
  response_window_and_fairness:
  failure_recovery:
personality:
  unique_identity_signals: []
  memorable_moments: []
decision: PASS | REWORK | HOLD | BLOCKED_UNVERIFIED
```

Base `DDD` continues to mean Digital Dopamine Design. Fast reward/feedback is not permission for indiscriminate stimulus spam, reward inflation, manipulative dark patterns, or removal of meaningful choice.

Static analysis may judge contract coverage but cannot PASS actual fun or immersion. Human playtest remains required for experiential claims.

## 6. Ownership

- lifecycle / global execution: `docs/LONG_HORIZON_WORK_EXECUTION_POLICY.md`
- product stage / Slice quality / playtest: `skills/designing-vertical-slices` + vertical-slice knowledge
- concept / originality / DDD / complexity / difficulty: `skills/analyzing-and-refining-game-concepts`
- visual/art/UI workflow: `docs/VISUAL_COLLABORATION_TOOL_POLICY.md` + existing art/UI Skills
- asset/plugin Existing Solution First: existing evaluation and asset-rights owners
- runtime evidence: existing validation owner; Notion approval is not runtime proof.

No new broad Skill is introduced.

## 7. Notion Project Home / Project Registry

Human-facing project metadata should expose, when applicable:

- repository;
- exact repo main SHA;
- Godot Port;
- Godot Project Address;
- implementation/runtime state.

Unknown values are written as `NOT_ASSIGNED_YET`, `NOT_PRESENT_YET`, or equivalent explicit unverified states, never invented.

## 8. Long-term fit and revisit conditions

This front-loads representative production quality but limits cost by keeping the first Slice short and reusing/adapting proven solutions. Revisit only if evidence shows the approach causes disproportionate asset waste before core uncertainty can be resolved. In that case permit additional narrow technical spikes, but do not reclassify them as player-experience validation.

Revisit if:
- integrated Slice cost repeatedly prevents any meaningful iteration;
- a specific project has a blocking technical unknown that cannot be cheaply isolated otherwise;
- target platform constraints require a different representative fidelity strategy;
- human playtests show that a lower-fidelity representation predicts final player response as reliably as the shipping-intent slice for a clearly defined question.
