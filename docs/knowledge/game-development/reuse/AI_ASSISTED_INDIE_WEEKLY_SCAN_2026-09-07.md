# AI-Assisted Indie Weekly Scan — 2026-09-07

```yaml
scan_date: 2026-09-07
base_started_from_completed_main: e25695e88e2a10eb32f25e21ce00bf11ddb91dcc
previous_scan: docs/knowledge/game-development/reuse/AI_ASSISTED_INDIE_WEEKLY_SCAN_2026-08-31.md
current_project_adoption_receipt: docs/knowledge/game-development/reuse/AI_ASSISTED_INDIE_PROJECT_ADOPTION_RECEIPT_2026-08-24.md
status: MATERIAL_BASE_FINDING
project_adoption: PROJECT_ADOPTION_NOT_RUN
runtime_mutation: NONE
notion_mutation: NONE
balance_mutation: NONE
paid_dependency_added: false
new_active_skill: false
new_runtime_framework: false
shared_rng_runtime_module_promoted: false
runtime_ai_default: TEST
```

This receipt is a dated evidence snapshot. It does not rewrite the historical 2026-08-24 Pattern Pack or its project-adoption history. Product popularity, review count, wishlist count, AI use, release state, and developer speed claims remain non-causal signals unless independently proven otherwise.

## 1. Sources actually inspected

Base owners read before external research:

- `AGENTS.md`
- `docs/knowledge/game-development/AI_GAME_AND_AI_ASSISTED_INDIE_RADAR.md`
- `docs/knowledge/game-development/reuse/AI_ASSISTED_INDIE_PROJECT_ADOPTION_RECEIPT_2026-08-24.md`
- `docs/knowledge/game-development/reuse/AI_ASSISTED_INDIE_WEEKLY_SCAN_2026-08-31.md`
- `docs/knowledge/game-development/reuse/AI_ASSISTED_INDIE_PATTERN_PACK_2026-08-24.md`
- `docs/knowledge/research/REVERSE_ENGINEERING_REUSE_PIPELINE.md`
- `docs/knowledge/game-development/reuse/REUSABLE_MODULE_REGISTRY.md`
- `docs/knowledge/game-development/PLATFORM_REVIEW_ASSET_RIGHTS_AND_REFERENCE_PRODUCTION_GUIDE.md`
- current open PR inventory; every pre-existing open/draft/ready PR remained read-only

External primary/current product surfaces inspected:

- Slotbound / Slotbound Demo — https://store.steampowered.com/app/4459590/Slotbound/ and https://store.steampowered.com/app/4906570/Slotbound_Demo/
- Vapor World: Over The Mind — https://store.steampowered.com/app/1996090/Vapor_World_Over_The_Mind/ and official Steam Community `Patch 0.5.4: AI Removal Hotfix`
- Matchinko — https://store.steampowered.com/app/4994610/Matchinko/ plus developer workflow post https://www.reddit.com/r/aigamedev/comments/1vs38mh/i_took_an_enginefree_game_from_idea_to_its_first/
- CODEX MORTIS — https://store.steampowered.com/app/4084120/CODEX_MORTIS/
- The Last Admiral / Demo — https://store.steampowered.com/app/4713660/The_Last_Admiral/ and https://store.steampowered.com/app/4958020/The_Last_Admiral_Demo/
- Suck Up! — https://store.steampowered.com/app/2726370/Suck_Up/
- Wanderfolk — https://store.steampowered.com/app/4599270/Wanderfolk/
- Neon Angora: The Cabaret Club — https://store.steampowered.com/app/4447940/Neon_Angora_The_Cabaret_Club/
- Express 404 — https://store.steampowered.com/app/4329710/Express_404/
- Ashen Crown — https://store.steampowered.com/app/4826250/Ashen_Crown/
- FARLUME: Into the Silent Dark — https://store.steampowered.com/app/4604120/FARLUME_Into_the_Silent_Dark/ and https://farlume.com/
- The Black Breath / Demo — https://store.steampowered.com/app/4227530/El_Aliento_Negro/ and https://store.steampowered.com/app/5160770/The_Black_Breath_Demo/ plus developer self-report https://www.reddit.com/r/aigamedev/comments/1w5vpnx/i_released_an_aiassisted_indie_game_demo_on_steam/
- Vonkelveld — https://store.steampowered.com/app/4846840/Vonkelveld/
- Homunculus: The Little One in the Flask — https://store.steampowered.com/app/4958080/Homunculus_The_Little_One_in_the_Flask/
- Black Rope Hell - Ximen Qing — https://store.steampowered.com/app/5013650/

No claim below is allowed to exceed the strongest source class attached to it.

## 2. Previous-scan comparison

| Case | 2026-08-31 capture | 2026-09-07 current evidence | Evidence class | Change interpretation |
|---|---|---|---|---|
| Slotbound Demo | 506 all-time / 82%; recent 169 / 85% | 538 all-time / 82%; recent rolling window 156 / 87%; full game says November 2026 | `OFFICIAL_PRODUCT_FACT` | all-time count +32 while percentage unchanged; rolling recent-window counts are not directly additive/comparable |
| Vapor World: Over The Mind | 64 / 37%, Mostly Negative | 80 / 45%, Mixed; official hotfix removed every AI-generated cutscene and restored original cutscenes | `OFFICIAL_PRODUCT_FACT` + `DEVELOPER_SELF_REPORT` | +16 reviews, +8 pp snapshot, category moved to Mixed; no causal claim that AI removal caused reception change |
| Matchinko | upcoming/demo, no reviews | still upcoming with demo and no user reviews | `OFFICIAL_PRODUCT_FACT` | release state unchanged |
| CODEX MORTIS | 57 / 80% | 58 / 79% | `OFFICIAL_PRODUCT_FACT` | +1 review, -1 pp; no material trend |
| The Last Admiral Demo | no user-review evidence in previous receipt | 3 user reviews; full game currently lists 2026-12-01 | `OFFICIAL_PRODUCT_FACT` | tiny demo sample now exists; insufficient for quality inference |
| Suck Up! | 203 / 62%, Mixed | 203 / 62%, Mixed | `OFFICIAL_PRODUCT_FACT` | unchanged on inspected current surface |
| Wanderfolk | upcoming EA planned 2026, no reviews | upcoming EA planned 2026, no reviews; Playtest and xAI Grok service disclosure remain | `OFFICIAL_PRODUCT_FACT` + developer EA self-report | unchanged release state; runtime value still unproven |
| Neon Angora | EA, 2 reviews | EA, 2 reviews; local llama.cpp + basic RAG current-state claim remains | `OFFICIAL_PRODUCT_FACT` + developer EA self-report | unchanged market sample; advanced Whisper features remain explicitly in development |
| Express 404 | released 2026-08-25, 4 reviews | released, 4 reviews | `OFFICIAL_PRODUCT_FACT` | unchanged weak sample |
| Ashen Crown | released, 1 review | released, 1 review; current Steam identifies Godot and broad Claude-assisted production | `OFFICIAL_PRODUCT_FACT` + `DEVELOPER_SELF_REPORT` | stronger engine/production evidence, not stronger market evidence |
| FARLUME | released, 2 reviews | released, 2 reviews; developer site identifies solo Godot 4.6 terminal-only production | `OFFICIAL_PRODUCT_FACT` + `DEVELOPER_SELF_REPORT` | stronger production provenance, market sample unchanged |

Popularity signals are snapshots, not causality. Rolling review windows and differing Steam surfaces are not treated as one cumulative metric unless product, window, filter, and observation basis match.

## 3. New or materially changed evidence

### 3.1 Vapor World: visible-AI rollback is now first-party failure evidence

Official Steam Community patch evidence states that every AI-generated cutscene was removed, the original in-game cutscenes were restored, and the director committed to no AI-generated cutscenes going forward.

Evidence ceiling:

- cutscene removal/restoration: `OFFICIAL_PRODUCT_FACT`
- why the team changed course / launch-day judgement: `DEVELOPER_SELF_REPORT`
- Steam discussion reactions: `PLAYER_REPORT`, not a representative player sample
- reception percentage movement: `OFFICIAL_PRODUCT_FACT`, but not proof that the hotfix caused the movement

Reusable lesson: `AI_VISIBLE_OUTPUT_QUALITY_GATE` must budget rework/replacement; disclosure alone is not a quality or distribution waiver.

Disposition: **ADOPT existing gate; refine its preflight, not a new Skill/module.**

### 3.2 The Black Breath: new solo Unity production case and channel-risk self-report

Official demo evidence:

- demo released 2026-09-01 with 2 reviews at inspection time
- solo developer disclosure says some assets used AI selectively, were manually reviewed/adapted, and no generative AI runs during gameplay
- core player promise is caravan survival: scarce resources, route choice with gathered information, tactical grid combat, fatigue/sickness/morale/permadeath pressure

Developer Reddit self-report:

- project began in late 2023; developer reports prior Unity/programming experience
- AI asset assistance came after a solid gameplay base existed
- developer reports some community posts removed as low effort, some festival rejection because of GenAI, some streamers refusing coverage, and nearly 1,000 wishlists
- developer reports subsequently hiring an artist for capsules, splash screens, UI, and a lore video

Evidence ceiling:

- demo/release/product loop/Steam AI disclosure: `OFFICIAL_PRODUCT_FACT`
- Unity experience, exact workflow timing, festival/streamer/community rejection, wishlist count, hiring rationale: `DEVELOPER_SELF_REPORT`
- no official festival or streamer policy was independently established by this scan

Reusable production lesson: use AI asset breadth only after a playable core is stable, and treat high-visibility AI assets as replaceable production routes rather than irreplaceable canon.

Reusable distribution lesson: when a project plans to depend on festivals/showcases/creator outreach/community discovery, check those channel-specific current constraints separately from store disclosure/compliance.

Disposition: **ADAPT production workflow; ADOPT bounded `AI_VISIBLE_OUTPUT_QUALITY_GATE` refinement; market success remains `REFERENCE_ONLY`.**

### 3.3 Vonkelveld: deterministic causal explanation without runtime AI

Official Steam evidence:

- Early Access released 2026-07-02; 4 user reviews, too small for reception inference
- simulation is described as deterministic from seed + player choices
- `Chronicle` and `Ask Why-Here` expose actual causal chains from the simulation
- same-seed challenges and score spreads are developer-described feedback inputs
- narration uses deterministic templates; English template library was hand-crafted, then mass-localized with an LLM and human-curated; zero runtime AI

Reverse-engineered reusable contract:

```text
project-owned deterministic event/state history
→ causality trace
→ explainable result packet
→ same-seed comparison / bug report
```

Existing Solution First:

- `RM-SYS-004 EXPLAINABLE_RESULT_PACKET`
- `RM-TOOL-002 DETERMINISTIC_SEED_REPLAY_CAPTURE`
- `RM-TOOL-003 BALANCE_SCENARIO_BATCH_SIMULATOR`

Disposition: **ADAPT / TEST.** Do not create an AI narration framework; the useful property is deterministic causal traceability.

### 3.4 Homunculus: runtime-AI agency is interesting but authority remains unresolved

Current Steam surface contains conflicting state text: metadata shows 2026-08-27 as release date and no reviews, while cached page copy still says the game is not yet available and plans to unlock on that date. Therefore current release availability is **UNKNOWN / STALE_SOURCE_CONFLICT**, not promoted to a confirmed released-success case.

Official product promise/disclosure describes:

- limited player `Oracle` interventions that the simulated character may accept, adapt, or refuse
- persistent profiles/memories/objectives
- third-party Tencent Cloud MaaS / DeepSeek live generation
- generated dialogue, diaries, journey events, NPC conversation, and outcomes of player-directed interactions
- broadband/Steam authentication required; same setup can produce different outcomes

Evidence ceiling: product promise and disclosure are `OFFICIAL_PRODUCT_FACT`; actual deterministic authority, state validation, moderation, replay/debug, cost, and failure behavior are not public runtime proof.

Smallest reusable idea independent of LLM:

```text
limited intervention
→ character rule / identity constraint
→ accept | adapt | refuse
→ relationship / loyalty consequence
```

Existing Solution First: `RM-SYS-005 EVENT_CONDITION_CHOICE_OUTCOME_ENGINE`, `RM-NAR-001`, and existing runtime AI gates.

Disposition: **TEST / REFERENCE_ONLY** for runtime AI; **ADAPT candidate** only for the limited-intervention agency lens if a project later needs it.

### 3.5 Black Rope Hell - Ximen Qing: bounded local generation is a monitored runtime pattern

Official Steam disclosure says optional local AI may generate short in-character NPC text, shadow-play/song drafts, and synthesized voice from developer-authored prompts, game state, and an allowlisted lore database. It says live AI does not generate images/video/3D/executable code and does not contact a third-party AI service during gameplay.

Source ceiling: `OFFICIAL_PRODUCT_FACT` describes intended product boundaries, not measured latency, device performance, lore safety, player value, or replay quality. Game is Coming Soon and has no reviews.

Existing Solution First: `RM-SYS-005`, `RM-NAR-002`, `RUNTIME_AI_DEPLOYMENT_MODE_BUDGET`, `DETERMINISTIC_STATE_VALIDATION`, `MEMORY_CANON_BOUNDARY`.

Disposition: **TEST / REFERENCE_ONLY**. No runtime framework promotion.

## 4. Rechecked production-assisted cases and reverse-engineering

### Slotbound

Core promise: turn a slot-machine roll into tactical preparation rather than surrendering all control to luck.

Loop/agency:

```text
spin
→ receive units / random traits
→ protect, absorb, evolve, item/core manipulation
→ fight judgement wave
→ learn result
→ reconfigure next preparation
```

Smallest reusable contract:

```text
uncertain result
→ protect / consume / convert decision
→ explicit commit
→ explain resulting power/state change
```

Existing owner overlap: `RM-SYS-002`, `RM-SYS-003`, `RM-SYS-004`, `RM-SYS-018`, `RM-SYS-019`; recovery/economy meaning remains project-specific.

Difficulty/cost/solo fit: low-to-medium when existing inventory/economy owners already exist; high design cost if recovery erases risk or creates a dominant recycling strategy. No paid dependency implied.

Disposition: **ADAPT**. `RNG_AGENCY_AND_RECOVERY` remains project-specific/adaptation-first.

### Matchinko

Core promise: the match-3 board you deliberately construct becomes the same board that later resolves pachinko scoring.

Developer self-report describes a 16-day path from initial design to first Steam upload, a JavaScript prototype followed by a Rust native implementation, headless logic, seeded randomness, custom physics/rendering, and release safeguards. That speed is `DEVELOPER_SELF_REPORT`, not proof of lower total cost or market success.

Smallest reusable contract:

```text
preparation state
→ bounded player edit
→ committed state snapshot
→ resolution using that same state
→ causal result explanation
```

Existing owner overlap: `RM-SYS-002`, `RM-SYS-014`, `RM-SYS-004`, `RM-TOOL-002`, `RM-TOOL-003`.

Disposition: **ADAPT** the cross-phase state causality; **TEST** physical determinism and project fit. Do not introduce a second state truth or new engine-independent framework.

### CODEX MORTIS

Core promise: mix five schools of dark magic, spell synergies, and undead armies in a bullet-hell progression loop.

Production loop: developer states AI enables fast iteration and that Discord/beta-player feedback drives changes. This is `DEVELOPER_SELF_REPORT` and not proof that AI caused current review score.

Smallest reusable contract:

```text
trigger + target + cost + effect + tags
→ compatibility / resolver ordering
→ state mutation
→ recursion / duplicate guard
→ explain result
```

Existing owner overlap: `RM-SYS-011`, `RM-SYS-007`, `RM-SYS-012`, `RM-SYS-004`.

Disposition: **ADAPT / TEST**. No general spell framework promotion from one game.

### The Last Admiral

Demo promise: a real opening slice of a run rather than a detached showcase; build a fleet, mine/salvage during battle, conquer/hold territory, then reach a scripted last stand.

Production-assisted disclosure: some 2D art and sounds were AI-assisted, then hand-edited/composited/finalized; no runtime generation.

Smallest reusable production contract:

```text
actual core loop
→ bounded content scope
→ complete decision-result-next-decision chain
→ demo feedback
```

Gameplay test candidate: mid-battle extraction/salvage as an explicit risk-reward action that competes with immediate combat safety.

Existing owner overlap: `RM-SYS-002`, `RM-SYS-007`, `RM-SYS-004`.

Disposition: **ADAPT** demo-slice principle; **TEST / REFERENCE_ONLY** for project-specific fleet/salvage design.

### Ashen Crown

Current Steam identifies a Godot release and developer disclosure that Claude assisted code, graphics/audio/balancing while the developer directed, corrected, tested, and decided. Market evidence remains one review.

Core design: the battle resolves automatically; player expression is build assembly across weapons/classes/subspecs/skills/fusions.

Existing owner overlap: `RM-SYS-003`, `RM-SYS-011`, `RM-SYS-012`.

Disposition: **TEST / REFERENCE_ONLY**. It is a verified current Godot AI-assisted release, not a verified success case.

### FARLUME

Current Steam has 2 reviews. Developer site says solo developer, Godot 4.6, terminal-only workflow, procedural visuals, and code-generated audio with Claude assistance. These production statements are `DEVELOPER_SELF_REPORT`.

Core design: auto-fire survivor loop with weapon evolution, passives, hidden synergies, boss/anomaly cadence, reroll/banish, and corruption/Breach risk-reward.

Existing owner overlap: `RM-SYS-003`, `RM-SYS-007`, `RM-SYS-011`, `RM-SYS-012`, existing production/release verification owners.

Disposition: **TEST / REFERENCE_ONLY**. Production breadth is interesting; market evidence is negligible.

## 5. Runtime-generative lane status

| Case | Current lane/evidence | Main unresolved proof | Disposition |
|---|---|---|---|
| Suck Up! | released; third-party AI NPC dialogue; 203 / 62% Mixed | provider reliability, repetitive/quality failure attribution, deterministic state authority, offline/fallback | `TEST / REFERENCE_ONLY` |
| Wanderfolk | upcoming EA; xAI Grok; Playtest; developer claims core loop complete/tested by hundreds | actual release-player evidence, state authority, provider/cost/privacy/fallback | `TEST` |
| Neon Angora | EA; 2 reviews; local llama.cpp, basic RAG | hardware/runtime measurement, memory/canon safety, advanced feature reality vs roadmap | `TEST` |
| Homunculus | release surface conflict; live DeepSeek/Tencent generation | actual availability, authoritative outcome/state validation, provider failure, replay/debug | `TEST / REFERENCE_ONLY` |
| Black Rope Hell | Coming Soon; bounded local AI + allowlisted lore | real device/runtime evidence, player value, latency, canon boundary | `TEST / REFERENCE_ONLY` |

No runtime-generative case is promoted to `ADOPT`. Deterministic project authority remains above model output.

## 6. Material Base finding

```text
MATERIAL_BASE_FINDING
owner: AI_GAME_AND_AI_ASSISTED_INDIE_RADAR.md / existing AI_VISIBLE_OUTPUT_QUALITY_GATE
change: bounded refinement only
new_skill: false
new_module: false
new_runtime_framework: false
```

Evidence chain:

1. Vapor World has first-party evidence of a launch-adjacent rollback that removed all AI-generated cutscenes and restored original cutscenes.
2. The Black Breath developer self-reports that disclosed GenAI assets produced rejection/friction in some communities, festivals, and streamer outreach, then reports hiring a human artist for high-visibility surfaces.
3. Existing Base already owns store/platform AI disclosure and rights in the release compliance Guide, and the existing `AI_VISIBLE_OUTPUT_QUALITY_GATE` owns player-facing AI output quality.
4. Search of current Base found no explicit current contract for **planned festival/showcase/creator/community distribution-channel compatibility** of visible AI outputs.

Smallest correction:

```text
AI_VISIBLE_OUTPUT_QUALITY_GATE
→ TARGET_DISTRIBUTION_CHANNEL_PREFLIGHT
→ VISIBLE_AI_REPLACEMENT_ROUTE
```

Guardrails:

```text
CHANNEL_REJECTION_IS_NOT_UNIVERSAL_POLICY
STORE_APPROVAL_IS_NOT_CHANNEL_ACCEPTANCE
SELF_REPORT_IS_NOT_CHANNEL_POLICY
```

The refinement does not say AI assets should always be replaced. It requires projects that actually depend on specific channels to check current channel constraints and know the replacement cost/route for high-visibility AI assets. Formal store compliance stays with the existing release owner.

## 7. Alternatives and adversarial review

Alternatives compared:

1. **NO_CHANGE** — reject. Existing quality/store gates do not explicitly cover non-store discovery-channel dependency, and current evidence shows that omission can matter for a solo launch plan.
2. **Create a new AI marketing/distribution Skill/module** — reject. No shared runtime/code consumer and the finding fits the existing visible-output gate plus existing release owners.
3. **Refine existing `AI_VISIBLE_OUTPUT_QUALITY_GATE` only** — adopt. Smallest owner-aligned delta; preserves current release-policy ownership and evidence ceilings.

Adversarial review 5/5:

- causality attack: review/wishlist movement is not attributed to AI usage or removal
- universality attack: one developer self-report is not treated as universal festival/streamer policy
- owner attack: formal store compliance remains in existing release Guide; no second release owner created
- overengineering attack: no new Skill/module/framework; only a bounded gate refinement and weekly successor receipt
- project-authority attack: no game project, Notion, gameplay/runtime code, balance, or paid dependency is changed

## 8. Project-fit hypotheses only

These are hypotheses, not project adoption:

- RNG/roulette/build projects may test Slotbound-style protection/consumption and recovery only through existing project economy owners.
- preparation→automatic-resolution projects may test Matchinko-style cross-phase state causality and explanation.
- build-composition projects may test CODEX MORTIS-style effect grammar through existing action/effect owners.
- strategy/demo work may test The Last Admiral-style complete decision-result-next-decision slice and explicit extraction risk.
- simulation-heavy projects may test Vonkelveld-style causal trace packets before considering generated narration.
- narrative/social projects may test limited-intervention agency or bounded local expressive generation only after deterministic state/canon authority is explicit.

No project received an automatic canon or implementation change from this scan.

## 9. Implementation Reality Gate

```yaml
web_primary_source_refresh: RUN
previous_scan_comparison: RUN
base_owner_fresh_read: RUN
open_pr_conflict_scan: RUN
existing_solution_first: RUN
reverse_engineering_contract_extraction: RUN
project_canon_fresh_read_for_adoption: NOT_RUN
project_runtime_mutation: NOT_RUN
runtime_ai_device_measurement: NOT_RUN
human_playtest_or_ux_validation: NOT_RUN
paid_dependency_added: false
causal_success_claim: NOT_PROVEN
```

Repository implementation/merge evidence is intentionally kept outside this evidence receipt until exact-head CI and merge/readback are actually known. This file does not turn unrun repository gates into PASS.

## 10. Next recheck conditions

- Slotbound: full release in November 2026; preserve demo/full-product metric separation and recheck post-release player evidence.
- Vapor World: recheck whether AI-removal policy persists and whether later updates/review samples reveal product-quality evidence independent of AI discourse.
- Matchinko: recheck release date and post-demo/release feedback; verify current production disclosure against developer workflow claims.
- CODEX MORTIS: recheck Early Access content/update cadence and larger sample before any production-efficiency promotion.
- The Last Admiral: recheck full release on/around 2026-12-01 and demo feedback growth.
- The Black Breath: recheck demo feedback and any official festival/showcase policy evidence; do not generalize developer self-report.
- Vonkelveld: recheck whether same-seed/Chronicle claims produce observable bug/balance evidence beyond developer description.
- Homunculus: resolve conflicting Steam availability state before treating it as released.
- Neon Angora / Wanderfolk / Suck Up! / Black Rope Hell: seek actual latency, provider/local-hardware, memory/canon, moderation, replay/debug, and player-value evidence.
- Godot/Unity lane: continue discovering current solo/small-team releases, but require official product + developer workflow evidence before promoting them beyond `REFERENCE_ONLY / TEST`.
