# AI-Assisted Solo/Indie Reverse-Engineering Pattern Pack — 2026-08-24

```yaml
status: RESEARCH_CAPTURE_COMPLETE
checked_at: 2026-08-24_KST
specialty_radar: docs/knowledge/game-development/AI_GAME_AND_AI_ASSISTED_INDIE_RADAR.md
source_policy_owner: docs/knowledge/game-development/PERIODIC_EXTERNAL_SOURCE_WATCHLIST.md
reuse_owner: docs/knowledge/research/REVERSE_ENGINEERING_REUSE_PIPELINE.md
ai_workflow_owner: docs/knowledge/game-development/AI_ASSISTED_GAME_DEVELOPMENT_GUIDE.md
module_registry_owner: docs/knowledge/game-development/reuse/REUSABLE_MODULE_REGISTRY.md
project_adoption: PROJECT_ADOPTION_NOT_RUN
runtime_ai_implementation: NOT_RUN
notion_mutation: NOT_RUN
new_skill: false
new_base_scheduler: false
paid_dependency_added: false
```

## 1. Purpose and evidence boundary

This pack reverse-engineers public AI-assisted solo/small-team game cases into the smallest reusable production or gameplay contracts that could improve player value or solo-development efficiency.

The following are never treated as equivalent:

```text
AI use != cause of success
release != market validation
review count != complete quality measure
wishlist/CCU self-report != independent audit
fast generation != low total production cost
content breadth != player value
AI novelty != better gameplay
PRODUCTION_ASSISTED != RUNTIME_GENERATIVE
```

Evidence classes remain explicit:

```text
OFFICIAL_PRODUCT_FACT
DEVELOPER_SELF_REPORT
PLAYER_REPORT
SECONDARY_REPORT
ANALYST_INFERENCE
```

Popularity is a discovery signal. It cannot independently prove why a game succeeded or failed.

## 2. Current case matrix

| Case | State @ 2026-08-24 KST | AI lane | Evidence ceiling | Reuse disposition |
|---|---|---|---|---|
| Slotbound | DEMO; full release upcoming | PRODUCTION_ASSISTED + PLAYER_FACING_GENERATED_ASSET | official store/update history + developer self-report + public review signal | ADAPT |
| Ashen Crown | RELEASED 2026-07-11 | PRODUCTION_ASSISTED + PLAYER_FACING_GENERATED_ASSET | official product/disclosure; very small review sample | TEST / REFERENCE_ONLY |
| Express 404 | UPCOMING 2026-08-25; demo available | PRODUCTION_ASSISTED | official product + experienced-developer self-report; no launch reception yet | REFERENCE_ONLY / recheck after release |
| Infinite Arcana | RELEASED 2026-07-30 | PRODUCTION_ASSISTED | official product + developer self-report; very small review sample | REFERENCE_ONLY |
| Vapor World: Over the Mind | EARLY_ACCESS 2026-08-18 | PLAYER_FACING_GENERATED_ASSET | official store + secondary launch reporting + public review signal | ADOPT quality gate / REJECT shortcut |
| Grimoire of Hecate: Tower of Starlight | DEMO | PRODUCTION_ASSISTED | developer self-report; no success claim | ADOPT existing context discipline |
| FARLUME: Into the Silent Dark | RELEASED 2026-06-01 | PRODUCTION_ASSISTED + PROCEDURAL_OUTPUT | official product/site; very small review sample | TEST / REFERENCE_ONLY |

Upcoming or weakly reviewed titles are not promoted to shipped-success evidence.

---

# 3. Slotbound — strongest current pilot case

## 3.1 Sources

Official:
- Steam Demo: <https://store.steampowered.com/app/4906570/Slotbound_Demo/>
- Steam Community updates: <https://steamcommunity.com/app/4459590/allnews/>

Developer self-report, verified source URLs:
- first public-playtest/build report: <https://www.reddit.com/r/aigamedev/comments/1ug5f5w/i_cant_code_but_after_8_months_of_building_with/>
- Steam-demo reception/workflow report: <https://www.reddit.com/r/aigamedev/comments/1v6wsy0/i_spent_8_months_making_my_first_ai_assisted_game/>

The 50,000-wishlist milestone is developer-announced/self-reported through the official Steam community feed. It is useful as a traction signal, not evidence that AI caused the traction.

## 3.2 One-sentence hook and loop

```text
What if a slot machine built your army?
```

```text
3x3 slot spin
→ unit result
→ keep / protect / absorb / strengthen
→ Items + Cores alter probabilities and build rules
→ battle/wave
→ survive / boss
→ repeat with a more legible run identity
```

The transferable layer is not “slot machine = fun.” It is the conversion of uncertain outcomes into meaningful player control.

```text
RNG produces candidates
→ interpret current board/build
→ preserve valuable result
→ sacrifice expendable result
→ alter future odds
→ commit to next risk
→ learn what this run wants to become
```

## 3.3 Public-feedback rebuild loop

The official Steam update history shows a significant Core-system rebuild rather than only parameter tuning. The developer also added a manual lock so units selected for preservation are not consumed by absorption, plus mid-run save and later performance/balance/stability fixes.

Reusable shape:

```text
real player evidence
→ classify problem
   bug | clarity | balance | weak core choice
→ local defect: hotfix
→ player-promise failure: rebuild the system
→ add agency/clarity affordance
→ regression + performance/stability check
→ collect new player evidence
```

This is strong evidence for `PLAYER_FEEDBACK_REBUILD_LOOP`.

## 3.4 AI-production lesson

Developer self-report separates AI throughput from human judgement: AI coding/visual tools were used to build and iterate, while the human repeatedly handled systems design, build testing, bug fixing, balance rework, idea removal and rebuilding. The public Steam disclosure separately confirms there is no live generative-AI system during gameplay.

```text
ADOPT
- one-sentence playable hook
- human-directed AI build loop
- demo-first evidence loop
- willingness to rebuild a weak core
- RNG agency/control lens
- bad-output recovery/absorption

ADAPT
- content breadth only after core identity is legible
- AI-assisted visuals only behind normal quality/rights gates

REJECT
- generation speed as a quality claim
- traction as proof AI caused success
- stability/performance debt as acceptable payment for breadth
```

---

# 4. Ashen Crown — breadth is capability evidence, not success evidence

Official:
- Steam: <https://store.steampowered.com/app/4826250/Ashen_Crown/>

The product disclosure describes heavy generative-AI use, Claude-assisted coding with a human directing/correcting/testing/deciding, code-drawn visuals, and AI-assisted audio/music. The public product surface is broad, but the review sample is too small to establish market success or long-term quality.

```text
AI strength
solo/small team → breadth becomes feasible

AI risk
breadth
→ more combinations
→ more balance surfaces
→ more QA surfaces
→ more architecture/context surfaces
```

Disposition:

```text
ADOPT
- human owns direction, correction, test and decision

TEST
- AI-assisted breadth after a stable core

REJECT
- content count as player-value evidence
- tiny review sample as AI-production success evidence
```

This case strengthens `BREADTH_AFTER_CORE_IDENTITY_LOCK` and `CONTEXT_SCOPE_AND_ARCHITECTURE_BUDGET`.

---

# 5. Express 404 — experienced developer uses AI as an expansion layer

Official:
- Steam: <https://store.steampowered.com/app/4329710/Express_404/>

Developer self-report:
- <https://www.reddit.com/r/aigamedev/comments/1vqf990/in_9_days_my_experimental_aiassisted_game_will_be/>

As of 2026-08-24 the Steam release is scheduled for 2026-08-25, so this is not a shipped-success example.

The developer reports roughly a decade of game-development experience, an initial human-authored codebase, AI analysis/expansion of that structure, and manual review of each change. The art process also required repeated correction before visual consistency improved.

Gameplay hook:

```text
night train
+ speed/quota management
+ several passengers
+ one mimic
+ lightning-only reveal window
+ wrong accusation costs profit
+ upgrades can transform danger/death into economy
```

Reusable production hypothesis:

```text
human architecture seed
→ AI reads existing structure
→ bounded expansion
→ every changed surface reviewed
→ run/play verification
```

Disposition: `REFERENCE_ONLY` until launch evidence exists; recheck immediately after release and again after early hotfixes.

---

# 6. Infinite Arcana — AI covers adjacent solo-production bottlenecks

Official:
- Steam: <https://store.steampowered.com/app/4754330/Infinite_Arcana/>

Developer self-report:
- <https://www.reddit.com/r/aigamedev/comments/1udqyt2/after_10_years_as_a_programmer_i_finally_built/>

The useful lesson is not that an experienced programmer no longer needs engineering. It is that a solo developer can still be blocked by art, UI, localization, marketing, trailer, content and production surfaces. AI can be useful when deliberately bounded to those missing roles.

Gameplay structure also reinforces an established design pattern:

```text
arcane slot wheel
→ each spin costs mana
→ symbols produce damage / shield / mana
→ enemy spell charge advances
→ continue spinning vs stop/play safe
```

The player decision comes from `resource cost + risk clock + continue/stop control`, not randomness alone.

Disposition:
- `ADAPT`: bounded AI support for solo-production bottlenecks.
- `ADAPT`: RNG with explicit resource/risk control.
- `REFERENCE_ONLY`: market success until evidence grows.

---

# 7. Vapor World: Over the Mind — player-facing AI output failure/mixed evidence

Official:
- Steam: <https://store.steampowered.com/app/1996090/Vapor_World_Over_The_Mind/>

Secondary report:
- GamesRadar, 2026-08-20: <https://www.gamesradar.com/games/action/after-25-percent-positive-steam-reviews-soulslike-dev-realizes-people-hate-ai-slop-and-admits-if-it-looks-like-the-effort-is-not-there-that-is-a-fair-reading-of-what-is-on-screen/>

Current Steam reception is weak. Secondary launch reporting identifies AI-generated cutscenes/voice as one major criticism and reports that the director acknowledged the perceived low-effort presentation and planned replacement/removal. This does **not** establish that AI alone caused the entire review score.

Safe reusable lesson:

```text
player-facing generated output
+ visible inconsistency / weak perceived craft
→ disclosure does not repair perceived value
→ rework/replacement cost can erase generation-speed savings
```

Disposition:
- `ADOPT`: `AI_VISIBLE_OUTPUT_QUALITY_GATE`.
- `REJECT`: generated presentation as a shortcut around normal craft/consistency review.
- Do not claim AI alone caused all negative reception.

---

# 8. Grimoire of Hecate — context drift requires durable checkpoints

Official/demo:
- Steam: <https://store.steampowered.com/app/5078840/Grimoire_of_Hecate__Tower_of_Starlight/>

Developer self-report:
- <https://www.reddit.com/r/ChatGPT/comments/1vu6tjv/three_months_of_building_a_steam_demo_with/>

The developer describes ChatGPT for design-detail work and Codex for project-file code/tests, while the human reviews, runs, plays and revises. As the project grew, AI increasingly lost earlier decisions or changed the wrong area; the mitigation was to write the current state to Markdown after tasks.

This does not require a new Base module. It reinforces existing context/evidence discipline:

```text
ADOPT existing discipline
- canonical current-state checkpoint
- scoped owner/context rehydration
- changed-surface review
- human run/play verification

REJECT
- ever-growing chat history as architecture/canon
```

---

# 9. FARLUME — constraints can turn procedural production into identity

Official:
- site: <https://farlume.com/>
- press kit: <https://farlume.com/press/>
- Steam: <https://store.steampowered.com/app/4604120/FARLUME_Into_the_Silent_Dark/>

The official material describes a solo Godot project built around code/procedural visuals rather than a large hand-authored texture library, with Claude Code used in code/localization production. The current review sample is too small for a success claim.

Transferable pattern candidate:

## CONSTRAINT_DRIVEN_PROCEDURAL_ASSET_PIPELINE

```text
production constraint
→ deliberately narrow visual grammar
→ code/procedural generator
→ deterministic reusable primitives
→ visual identity gate
→ performance/readability/accessibility check
```

Disposition: `TEST / REFERENCE_ONLY`. Do not promote a universal art module until multiple project pilots prove a reusable interface.

---

# 10. Reusable production contracts

## HUMAN_DIRECTED_AI_BUILD_LOOP

Evidence: Slotbound, Ashen Crown, Express 404, Grimoire of Hecate.

```text
human intent + acceptance criteria
→ bounded AI change
→ changed-surface audit
→ test/build/run
→ player-value judgement
→ accept | revise | revert
→ evidence/context refresh
```

Existing owners:
- `AI_ASSISTED_GAME_DEVELOPMENT_GUIDE.md`
- `RM-WORK-002 SKILL_WORKFLOW_PATTERN_EVAL`
- repository/project verification contracts

Disposition: **ADOPT as a reusable lens, not a new Skill.**

## SILENT_OMISSION_GATE

After every material AI-assisted change, attack the result with:

```text
What requested behavior is still missing?
What was simplified or silently skipped?
Which consumers were not updated?
Which failure paths were not tested?
Did the change add hidden architecture debt?
```

Disposition: **ADOPT through existing verification/adversarial owners.**

## CONTEXT_SCOPE_AND_ARCHITECTURE_BUDGET

AI throughput is not permission to create a monolith.

Each material change identifies:

```text
canonical owner
mutable state owner
resolver
presenter
persistence
validation/tests
rollback
```

If the model repeatedly loses the relevant contract, do not only increase prompting. Split responsibility or refresh durable current-state checkpoints.

Disposition: **ADOPT by strengthening existing owners.**

## BREADTH_AFTER_CORE_IDENTITY_LOCK

```text
small playable core
→ core player promise verified
→ state/schema ownership stabilized
→ visual/UX identity bar stabilized
→ cheap rejection criteria exist
→ only then multiply variants/content with AI
```

Disposition: **ADOPT as production gate.**

## PLAYER_FEEDBACK_REBUILD_LOOP

```text
public demo / real-player evidence
→ classify bug | clarity | balance | weak core choice
→ local defect: hotfix
→ player-promise failure: rebuild system
→ regression / performance / save check
→ new player evidence
```

Disposition: **ADOPT.** Slotbound is the strongest current public example in this wave.

## AI_VISIBLE_OUTPUT_QUALITY_GATE

```text
generated player-facing output
→ art-direction consistency
→ readability / UX
→ animation/audio continuity
→ copyright/license/provenance
→ platform disclosure/compliance
→ human quality review
→ in-game context test
→ accept | rework | replace
```

```text
disclosure != quality waiver
generation speed != rework cost saved
```

Disposition: **ADOPT.**

---

# 11. Reusable gameplay contract candidate

## RNG_AGENCY_AND_RECOVERY

Primary evidence: Slotbound. Supporting structural evidence: Infinite Arcana.

```text
unpredictable outcome
→ meaningful player control surface
   reroll | lock | weight shift | banish | convert | absorb | sell | bank | combine
→ control has cost/tradeoff
→ bad outcome still creates a decision, information, or future resource
→ build/run identity becomes legible
```

The design question is not “how much RNG exists?” but:

```text
accept?
reroll?
protect?
sacrifice?
convert?
change future probability?
commit to this run identity?
```

### Existing Solution First

Do **not** create a new `RM-SYS-*` yet. Pilot this lens through existing owners first:

- `RM-SYS-003 CANDIDATE_DRAFT_WEIGHT_ENGINE`
- `RM-SYS-018 ROULETTE_TOKEN_SOURCE_ENGINE`
- `RM-SYS-019 PUSH_YOUR_LUCK_ENHANCEMENT_ENGINE`
- `RM-TOOL-002 DETERMINISTIC_SEED_REPLAY_CAPTURE`
- `RM-TOOL-003 BALANCE_SCENARIO_BATCH_SIMULATOR`

Promotion requires:

```text
>= 2 materially distinct project pilots
+ existing modules cannot express the shared interface cleanly
+ deterministic replay/balance evidence
+ no duplicated state authority
```

Current disposition: **ADAPT / TEST, no new module.**

---

# 12. Runtime generative AI remains TEST-only

The cases above mostly demonstrate production-assisted development, not runtime generative gameplay. They cannot justify runtime AI adoption by themselves.

A useful minimum candidate from the broader AI-game benchmark is:

```text
freeform player input
→ AI semantic interpretation/proposal
→ project-owned deterministic validator
→ authoritative GameState mutation by game rules only
→ result presentation
→ bounded memory update
```

Potential subfeatures:
- semantic action interpretation
- layered memory/canon retrieval
- capability contract preventing impossible promises/actions
- semantic combination with cache
- discovery/codex reward
- emotion/relationship interpretation with deterministic numeric resolution

Any project pilot must prove all of:

```text
PLAYER_VALUE_UNIQUE_TO_AI
CAPABILITY_CONTRACT
DETERMINISTIC_STATE_VALIDATION
MEMORY_CANON_BOUNDARY
LATENCY_OFFLINE_FALLBACK
PRIVACY_MODERATION_SECURITY
COST_SURFACE_APPROVED
PLATFORM_STORE_COMPLIANCE
REPLAY_DEBUG_EVIDENCE
```

Current disposition: **TEST only. runtime implementation NOT_RUN.**

---

# 13. Project-fit hypotheses

These are Base-level routing hypotheses only. Each project remains `PROJECT_ADOPTION_NOT_RUN` until its current canon and implementation reality are read independently.

| Project | Candidate | Initial disposition | Boundary |
|---|---|---|---|
| OMENWARD | RNG agency/control over roulette + explainable odds/build identity | ADAPT — high | existing roulette/token/push-your-luck owners first |
| NINJA_SURVIVAL | poor reward/drop recovery through combine/workbench/convert | ADAPT — high | bad drops should become future decisions rather than dead time |
| BLACKSMITH | push-your-luck + outcome recovery + visible consequence feedback | ADAPT — high | fit must be checked against current enhancement/durability canon |
| GRIMOIRE | semantic combination + deterministic validation + discovery reward | TEST — medium-high | authoritative spell rules remain deterministic |
| URBAN_LEGEND | layered memory/canon-aware interpretation | TEST — medium | only if investigation choices improve; no free-chat default |
| MY_LITTLE_BOAT | relationship memory + capability contract | TEST — medium-low | only if conversation becomes a validated core need |
| TETRIS | AI production workflow | ADOPT workflow / REJECT runtime | no unique runtime-AI player value currently established |
| SWITCHY | production workflow; RNG lens only if random logistics appears | REFERENCE_ONLY gameplay | do not disturb current core without evidence |
| TEN_PACES | production workflow only | ADOPT workflow / REJECT runtime | hidden-plan/deterministic integrity takes priority |
| COC_FICTION | canon-review/production workflow | ADOPT workflow / REJECT runtime game AI | narrative support and runtime AI game system are separate |

---

# 14. Base absorption options

## Option A — New AI-game Skill/framework

**REJECT.** It would duplicate Watchlist, reverse-engineering reuse, AI development, module registry and scheduler responsibilities.

## Option B — External weekly search only

**REJECT as insufficient.** Discovery would recur, but comparable evidence, failure learning and owner routing would not accumulate reliably.

## Option C — Existing Watchlist + specialty Radar + dated Pattern Pack

**ADOPT.** Source policy remains with the existing Watchlist, scheduling remains outside Base, evidence accumulates in dated packs, and reusable candidates route through existing owners before promotion.

---

# 15. Implementation Reality Gate

## VERIFIED / claimable after this Base change is merged

- A focused weekly AI-game/AI-assisted-indie research contract exists.
- Production-assisted and runtime-generative AI are separated.
- Success, weak-evidence, upcoming and failure/mixed cases are all represented.
- Candidate contracts route to existing Base owners first.
- Project fit is explicitly hypothesis-only.
- No new Skill, Base scheduler, paid dependency or runtime AI implementation is introduced.

## UNVERIFIED / forbidden claims

- Any project adopted these gameplay candidates.
- Any candidate improves retention, wishlists or sales.
- Slotbound traction was caused by AI use.
- AI-assisted production is always faster or cheaper after correction/QA cost.
- Ashen Crown, Infinite Arcana or FARLUME are market-success cases.
- Express 404 will succeed after release.
- AI alone caused Vapor World's overall reception.
- Runtime semantic AI is required by any current project.

Promotion path:

```text
research pattern
→ read current project canon
→ define player-value hypothesis
→ design adapter against existing owner
→ deterministic POC where possible
→ QA/replay/balance evidence
→ human playtest
→ adversarial review
→ ADOPT | ADAPT | REJECT
```

---

# 16. Adversarial review 5/5

**Result: PASSED_WITH_RESOLVED_FINDINGS**

## Loop 1/5 — duplication attack

Finding: registering `RNG_AGENCY_AND_RECOVERY` as a new universal module would duplicate existing draft/roulette/push-your-luck owners.

Resolution: no new `RM-SYS-*`; pilot as an adapter/lens over `RM-SYS-003`, `RM-SYS-018`, and `RM-SYS-019` first.

## Loop 2/5 — causality attack

Finding: Slotbound review/wishlist signals could be misread as “AI caused success.”

Resolution: production method and traction remain separate evidence fields. Wishlist/ranking self-reports remain self-report. Popularity has no causal authority.

## Loop 3/5 — solo-dev reality attack

Finding: AI breadth can conceal QA, performance, save, balance, architecture and context debt.

Resolution: require `HUMAN_DIRECTED_AI_BUILD_LOOP`, `SILENT_OMISSION_GATE`, `CONTEXT_SCOPE_AND_ARCHITECTURE_BUDGET`, `BREADTH_AFTER_CORE_IDENTITY_LOCK`, and normal run/build evidence.

## Loop 4/5 — player-value attack

Finding: runtime AI can become a technology demo rather than a better choice/emotion/reward system.

Resolution: runtime AI stays `TEST`; `PLAYER_VALUE_UNIQUE_TO_AI` is the first gate; authoritative state remains project-owned and deterministic.

## Loop 5/5 — maintenance, rights and cost attack

Finding: provider/API cost, rights, disclosure, visual inconsistency, model drift, offline failure and rework can exceed the initial generation benefit.

Resolution: no paid/runtime dependency in this absorption; add `AI_VISIBLE_OUTPUT_QUALITY_GATE`; future runtime pilots require cost/platform/privacy/replay/debug gates.

### Final source-integrity correction

The final adversarial pass rejected inferred/uncertain Slotbound Reddit paths. The pack now uses the verified June public-playtest/build post and the verified July Steam-demo reception/workflow post, while the Core-system rebuild itself is grounded in the official Steam update history.

### Clean exit

```text
new unresolved authority conflict: none found
new duplicate module: none created
project canon mutation: none
runtime AI implementation: none
paid dependency: none
upcoming title described as shipped success: no
popularity used as causal proof: no
known invalid source URL left in pack: no
```

---

# 17. Next weekly comparison

```yaml
previous_scan: 2026-08-24
priority_recheck:
  Slotbound:
    - review delta
    - hotfixes/performance
    - full release state
    - Core/balance changes
  Express_404:
    - launch state after 2026-08-25
    - early reviews
    - launch hotfixes
    - AI-art reception
  Vapor_World:
    - AI-cutscene replacement
    - review delta
    - patch response
  Ashen_Crown:
    - review growth
    - postmortem
    - architecture/QA updates
  Infinite_Arcana:
    - review growth
    - developer postmortem
  Grimoire_of_Hecate:
    - demo feedback
    - context-process updates
  FARLUME:
    - review growth
    - production postmortem
    - performance/readability evidence
new_case_queries:
  - solo AI-assisted Steam demo
  - AI-assisted Godot indie release
  - AI-assisted Unity indie release
  - AI-generated game postmortem
  - generative AI game Steam recent reviews
  - solo developer Claude Code Codex game
  - AI game player backlash removal replacement
```

Each weekly run compares against this baseline, including candidate promotion, demotion and rejection—not just new discoveries.
