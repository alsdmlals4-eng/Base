# Release-Near Vertical Slice First — Implementation Plan

- Baseline: `c8de06cdd63ddcb9121d8321bf135eaea9e14f06`
- Approved scope: current user pre-approved all approvals needed in this chat.
- Design: `docs/superpowers/specs/2026-08-20-release-near-vertical-slice-first-design.md`

## Task 1 — RED contract

Modify existing permanent regression suites before production policy changes.

Primary test owner: `tests/test_vertical_slice_v6_contract.py`.

Assert that current active contracts eventually require:

- `RELEASE_NEAR_VERTICAL_SLICE_FIRST`
- `GAMEPLAY_VALIDATION_REQUIRES_SHIPPING_INTENT_SLICE`
- `SYSTEM_ONLY_POC_NOT_PLAYER_EXPERIENCE_EVIDENCE`
- `TECHNICAL_SPIKE_INTERNAL_ONLY`
- `SHIPPING_INTENT_UI_IMAGE_AUDIO_VFX_SYSTEM_REQUIRED`
- `EXISTING_SOLUTION_FIRST_ADAPT_TO_PROJECT`
- `PLAYER_APPEAL_QUALITY_GATE`
- no active `VISUAL_NOT_MATERIAL_TO_THIS_POC` gameplay-validation escape
- no separate `CORE_POC` product stage.

Add a separate Long-Horizon/adversarial regression for the already-approved clean-exit contract: no fixed loop minimum/quota; repeat full review until zero new valid findings and regression.

Run the existing permanent Vertical Slice and Long-Horizon CI to observe expected RED before production changes.

## Task 2 — Global lifecycle

Update `docs/LONG_HORIZON_WORK_EXECUTION_POLICY.md`:

- replace visual-PoC-first compatibility language with release-near Vertical Slice-first gameplay validation;
- preserve narrow technical spikes;
- make UI/image/audio/VFX/system integration explicit;
- keep human playtest evidence ceiling;
- remove stale fixed-five adversarial quota and restore pure `ADVERSARIAL_REVIEW_UNTIL_CLEAN`.

## Task 3 — Vertical Slice authority

Update:

- `skills/designing-vertical-slices/SKILL.md`
- `docs/knowledge/vertical-slice/INTEGRATED_DEMO_STAGE_GATES.md`
- `templates/planning/VERTICAL_SLICE_PLAN.md`

Requirements:

- first gameplay validation product is short and near-release quality;
- included segment uses shipping-intent UI/art/image/audio/VFX/system/content;
- temporary/grey-box system proof cannot validate player experience;
- technical spike remains internal and bounded;
- full-game content volume is not required.

## Task 4 — Concept / originality / DDD quality gate

Update existing `analyzing-and-refining-game-concepts` owner and relevant reference only; do not create a new Skill.

Add Player Appeal Quality Gate covering:

- originality / reason to choose this game;
- DDD first meaningful reward, feedback latency, reward density/clarity, Micro→Session→Meta, fatigue/inflation;
- visual/audio/system/world/fantasy consistency;
- avoidable complexity / simultaneous cognitive burden;
- difficulty approachability / fairness / recovery;
- unique identity signals / memorable moments.

Human playtest remains required for actual fun/immersion PASS.

## Task 5 — Existing solution / completed-game adaptation

Route complete-game references, mature UX patterns, licensed/owned assets, audio/VFX libraries, Godot capabilities/plugins through existing benchmark/rights/Existing Solution First owners.

Default disposition is `ADAPT`; copying identifiable expression is forbidden. A different faster path is allowed when the trade study shows better total time, quality, rights, maintainability, fit, and rollback.

## Task 6 — Registry / learning / generated consumers

If Skill description/triggers/use_when change:

- update `skills/SKILL_REGISTRY.json` only for affected existing owners;
- update appropriate Learning Logs;
- rebuild generated skill publication with the existing generator;
- keep one-to-one package/Registry integrity.

## Task 7 — Verification

Run:

- integrated Vertical Slice workflow;
- Base Long-Horizon contract workflow;
- Skill Routing / Game UX UI / Game Project OS / Base v9 workflows as triggered;
- canonical reference freshness;
- unresolved review threads;
- exact-head mergeability;
- whole resulting-state adversarial review until clean.

Do not count skipped/not-run runtime work as PASS.

## Task 8 — Merge + project synchronization

After Base merge/readback:

- synchronize Tetris active repo planning away from system-PoC-first language to release-near short Vertical Slice-first;
- preserve old POC ruleset only as initial tuning/history if still useful;
- update Tetris Project Home and Project Registry;
- Godot Port stays `NOT_ASSIGNED_YET` and Godot Project Address stays `NOT_PRESENT_YET` until actual project/runtime evidence exists;
- set Notion Sync State back to `SYNCED` only after GitHub + Notion readback agree.

## Task 9 — Remaining Base backlog

Re-evaluate and selectively absorb current-valid P03 #537 and P08 #535 semantics onto latest main; do not merge stale branches wholesale. Close superseded backlog after equivalent current-main changes are verified.

Finish with whole-Base / Notion consistency review and `REQUIRED_WORK_REMAINING = 0` only when supported by evidence.
