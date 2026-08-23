# AI Indie Game Reverse-Engineering Radar Design

## Status

- date: 2026-08-24 KST
- change class: bounded Base research/workflow extension
- runtime/gameplay mutation: none
- project canon mutation: none
- Notion mutation: none
- new Skill/Agent: none
- scheduler owner: external to Base
- existing owner preservation: required

## Problem

AI-assisted solo/indie games are now reaching public demos and commercial storefronts quickly enough that one-off research misses useful production and gameplay patterns. The current Base already owns periodic external-source discovery and reverse-engineering reuse, but it does not yet have a focused capture contract for AI-assisted solo games that separates:

1. games built with AI during production,
2. games using generative AI at runtime,
3. hybrid cases,
4. visible AI-generated player-facing assets,
5. ordinary gameplay patterns discovered through AI-assisted projects.

Without that split, the workflow can overgeneralize from novelty, confuse production speed with game quality, or create duplicate AI-specific systems instead of routing useful patterns into existing owners.

## Existing owners

This change must reuse, not replace:

- `docs/knowledge/game-development/PERIODIC_EXTERNAL_SOURCE_WATCHLIST.md`
- `docs/knowledge/game-development/PERIODIC_EXTERNAL_SOURCE_DISCOVERY_SEEDS.md`
- `docs/knowledge/game-development/PERIODIC_SPECIALTY_SOURCE_RADAR.md`
- `docs/knowledge/research/REVERSE_ENGINEERING_REUSE_PIPELINE.md`
- `docs/knowledge/game-development/AI_ASSISTED_GAME_DEVELOPMENT_GUIDE.md`
- `docs/knowledge/game-development/reuse/REUSABLE_MODULE_REGISTRY.md`
- `docs/knowledge/game-development/reuse/GAMEPLAY_AND_CONTENT_MODULES.md`
- `docs/knowledge/game-development/reuse/PRODUCTION_TOOL_WORKFLOW_MODULES.md`
- `docs/knowledge/game-development/reuse/BENCHMARK_SOURCE_NOTES.md`

The new documents are specialty reference/capture surfaces. They do not become a second Watchlist, module registry, AI development authority, project canon, or scheduler.

## Three-option comparison

### Option A — New AI-game framework/Skill

Create a dedicated Skill plus a new AI-game module catalog and scheduler.

**Reject.** It duplicates existing source discovery, reverse-engineering, AI workflow, module registry, and scheduler responsibilities. Maintenance and routing ambiguity exceed the benefit.

### Option B — External weekly search only

Keep the scheduled task but make no Base-side capture contract.

**Reject as insufficient.** It finds new cases but does not guarantee comparable evidence packets, owner routing, regression/failure capture, or cumulative reuse learning.

### Option C — Specialty Radar + evidence-derived Pattern Pack

Add a focused specialty Radar subordinate to the existing Watchlist and a dated reverse-engineering Pattern Pack subordinate to the existing reuse pipeline. Route reusable deltas to existing owners rather than introducing parallel authorities.

**Adopt.** This gives the weekly task a stable capture schema while preserving Base ownership boundaries.

## Design goals

1. Scan AI-assisted solo/indie releases at least weekly through the external scheduler.
2. Capture both success and failure/mixed evidence.
3. Separate popularity signals from evidence authority.
4. Separate production AI from runtime AI.
5. Reverse-engineer gameplay, production workflow, QA, release, and feedback loops.
6. Extract the smallest reusable contract and check existing owners first.
7. Produce project-fit candidates without silently changing project canon.
8. Preserve zero-incremental-cost preference; paid/runtime model dependence requires a later explicit project gate.
9. Record falsification and rollback/discard conditions.
10. Compare new scans with prior scans so repeated lessons can be promoted and stale lessons can be retired.

## AI use lanes

Every case declares one or more lanes:

```text
PRODUCTION_ASSISTED
RUNTIME_GENERATIVE
HYBRID
PLAYER_FACING_GENERATED_ASSET
AI_MARKETING_OR_PROMOTION
```

`PRODUCTION_ASSISTED != RUNTIME_GENERATIVE`.

A production workflow lesson cannot be used as evidence that runtime AI improves gameplay. A runtime-AI novelty cannot be used as evidence that AI-assisted production is efficient.

## Weekly candidate packet

```yaml
case_id:
checked_at:
release_state: RELEASED | DEMO | EARLY_ACCESS | UPCOMING | UNKNOWN
team_context:
engine_or_stack_when_verified:
ai_use_lanes: []
primary_sources: []
supporting_sources: []
popularity_signals:
  review_count:
  review_sentiment:
  wishlist_or_ccu_when_verified:
  signal_date:
core_player_promise:
core_loop:
player_agency:
production_loop:
feedback_and_update_loop:
observed_strengths: []
observed_failures: []
source_ceiling:
reusable_candidates: []
existing_owner_overlap:
project_fit_candidates: []
disposition: ADOPT | ADAPT | TEST | REJECT | REFERENCE_ONLY
falsification:
rollback_or_discard:
```

## Mandatory source ladder

Prefer:

1. official store/release/update pages for shipped state and product behavior,
2. developer postmortem/blog/repository for production claims,
3. developer-authored community posts for self-reported workflow,
4. user reviews/community reports for player-perceived strengths/failures,
5. secondary reporting only when it adds independently checked context.

Popularity is a discovery signal, not evidence authority. Review count, positivity, wishlists, CCU, rankings, and social votes must retain their observation date and source.

## Current reverse-engineering wave

The first Pattern Pack covers:

- Slotbound — successful public demo signal, solo AI-assisted production, strong one-sentence hook, luck-to-strategy conversion, player-feedback-driven Core rebuild, and notable stability debt.
- Ashen Crown — transparent AI-heavy Godot experiment showing extreme breadth and fast production, but very weak market validation and architecture/context-risk warning signals.
- Express 404 — pre-release case where an experienced developer built the initial codebase and then used AI to analyze/expand it with manual review of every change.
- Infinite Arcana — demo case where an experienced programmer used AI to cover solo-production bottlenecks outside core engineering; useful workflow evidence, weak popularity evidence.
- Vapor World: Over the Mind — failure/mixed evidence for visible AI-generated player-facing presentation and the reputational cost of low-perceived-effort output.

Upcoming games are `MONITOR`, not shipped-success evidence.

## Reusable production contracts

The Pattern Pack may recommend the following as Base promotion candidates, but the existing AI development Guide and workflow owners remain authoritative:

### HUMAN_DIRECTED_AI_BUILD_LOOP

```text
human intent / acceptance criteria
→ bounded AI change
→ changed-surface audit
→ test/build/run
→ player-value judgement
→ accept | revise | revert
→ evidence/context refresh
```

### SILENT_OMISSION_GATE

After AI-assisted change, explicitly ask:

- What requested behavior is still missing?
- What was simplified or silently skipped?
- Which consumers were not updated?
- Which failure paths were not tested?
- Did the change add hidden architecture debt?

### CONTEXT_SCOPE_AND_ARCHITECTURE_BUDGET

AI throughput is not permission to create a monolith. Each change identifies canonical owner, mutable state owner, resolver, presenter, persistence, tests, and rollback. If the model cannot hold the relevant contract in context without repeated drift, split the responsibility before adding breadth.

### BREADTH_AFTER_CORE_IDENTITY_LOCK

Use AI to multiply variants/content only after a small playable core, schema, quality bar, and visual/UX identity are stable enough to reject bad variants cheaply.

### PLAYER_FEEDBACK_REBUILD_LOOP

```text
public/demo evidence
→ classify bug / clarity / balance / core-choice weakness
→ hotfix if local
→ rebuild if the system fails its player promise
→ regression + player evidence
```

### AI_VISIBLE_OUTPUT_QUALITY_GATE

Player-facing AI output must pass the same quality/consistency/rights/usability bar as manually produced output. Disclosure does not compensate for visibly weak craft, and generated presentation is not a sales point by default.

## Reusable gameplay contract candidate

### RNG_AGENCY_AND_RECOVERY

Slotbound is evidence for a reusable design lens, not a new universal runtime module:

```text
unpredictable outcome
→ meaningful player control surface
   reroll | lock | weight shift | convert | absorb | sell | bank | combine
→ cost/tradeoff remains
→ bad outcome still creates a decision or future resource
→ run identity becomes legible
```

This should first be tested as a cross-cutting contract over existing owners such as `RM-SYS-003 CANDIDATE_DRAFT_WEIGHT_ENGINE`, `RM-SYS-018 ROULETTE_TOKEN_SOURCE_ENGINE`, `RM-SYS-019 PUSH_YOUR_LUCK_ENHANCEMENT_ENGINE`, and project-specific reward/crafting systems. Do not create a duplicate module until multiple project adapters prove an interface that existing owners cannot express.

## Runtime generative AI boundary

The earlier AI-game benchmark produced a separate runtime candidate: freeform player input can be interpreted by AI, but authoritative state mutation remains deterministic/project-owned. This design does not promote a runtime implementation in this change.

Any runtime-generative Pilot must separately prove:

- player value that cannot be delivered more cheaply with authored rules/content,
- capability contract preventing impossible promises/actions,
- deterministic validation before authoritative mutation,
- memory/canon boundaries,
- latency/offline/failure fallback,
- moderation/privacy/security needs,
- provider/cost surface,
- platform/store compliance,
- replay/debug evidence.

## Project-fit routing

Initial hypothesis only; project canon remains authoritative:

| Project | Candidate | Initial disposition |
|---|---|---|
| OMENWARD | RNG agency/control over roulette + explainable odds/build identity | ADAPT, high |
| NINJA_SURVIVAL | poor reward/drop recovery through combine/workbench/convert outlets | ADAPT, high |
| BLACKSMITH | push-your-luck + outcome recovery + visible consequence feedback | ADAPT, high |
| GRIMOIRE | semantic combination/runtime-AI candidate only behind deterministic rule validation; discovery rewards | TEST, medium-high |
| URBAN_LEGEND | layered memory/canon-aware AI only if it improves investigation choices; no free-chat default | TEST, medium |
| MY_LITTLE_BOAT | relationship memory/capability contract only if conversation becomes a validated core need | TEST, medium-low |
| TETRIS | production workflow lessons only; generative runtime is not justified by current core | REJECT runtime / ADOPT workflow |
| SWITCHY | production workflow lessons; RNG-to-agency only if a future random logistics layer exists | REFERENCE_ONLY gameplay |
| TEN_PACES | deterministic hidden-plan integrity takes precedence; freeform runtime AI is high risk | REJECT runtime / ADOPT workflow |
| COC_FICTION | production/canon-review workflow only; runtime AI game system is out of current product scope | ADOPT workflow / REJECT runtime |

## Implementation Reality Gate

This change can truthfully claim:

- research cases were captured from public sources,
- a weekly specialty scan contract exists,
- reusable candidate contracts and project-fit hypotheses are documented,
- external scheduling is already available independently of Base.

It cannot claim:

- any project has adopted the candidate,
- any runtime AI module exists,
- any candidate improves player retention/sales,
- AI-assisted development is universally faster after human correction/QA cost,
- upcoming games are commercially successful,
- popularity signals prove causality.

## Adversarial review requirements

Five review passes are required before merge:

1. **Duplication attack** — could existing owners express this without a new file/contract?
2. **Causality attack** — are success signals being misread as proof that AI or one mechanic caused success?
3. **Solo-dev reality attack** — does generated breadth hide QA, architecture, art, localization, or support debt?
4. **Player-value attack** — does a proposed AI feature create a better decision/emotion, or merely demonstrate AI?
5. **Maintenance/rights/cost attack** — can this survive provider change, store policy, rights review, and zero-incremental-cost constraints?

Any new conflict returns the design to pass 1.
