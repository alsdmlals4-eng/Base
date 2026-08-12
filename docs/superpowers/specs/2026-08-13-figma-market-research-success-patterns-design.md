# Figma Practical Workflow + Game Market Research Success Patterns Design

- Date: 2026-08-13
- Baseline: `4288871809239a402a2d73ffcedd4d7330bf6136`
- Scope: Base guidance/source expansion only; no project Figma canvas mutation, no new ACTIVE Skill, no product-direction decision

## Goal

Extend Base so Figma is usable as a practical game-design/research workspace, while game market research can compare successful cases without laundering popularity, estimates, or correlation into causal design rules.

## Existing Solution First

Reuse current owners instead of creating a `figma-*` or `market-research-*` Skill.

- Figma authority/workspace: `docs/VISUAL_COLLABORATION_TOOL_POLICY.md`, `templates/project-operations/FIGMA_VISUAL_BIBLE_PROFILE.md`, `templates/project-operations/FIGMA_WORKSPACE_STRUCTURE_PROFILE.md`
- Game benchmark/player evidence: `skills/analyzing-and-refining-game-concepts` and `references/benchmark-player-evidence-and-playtests.md`
- Periodic source intake: `docs/knowledge/game-development/PERIODIC_EXTERNAL_SOURCE_DISCOVERY_SEEDS.md`

Disposition: `ABSORB_EXISTING_OWNER` + `LOW_RISK_BOUNDED_UPDATE`.

## Figma practical workflow

Add official Figma sources and practical guidance for:

1. Auto Layout for responsive content, reusable spacing/padding and long/localized text.
2. Components, variants and component properties for state/size/type families.
3. Variables for tokens, modes and stateful prototypes, without turning prototype state into game-rule canon.
4. Prototype flows for user journeys and interaction hypotheses.
5. Dev Mode for inspect/version comparison, annotations and code/document links when plan/seat permits.
6. FigJam for market research clustering, competitor maps, player-problem notes, hypothesis/counterexample boards and decision workshops.
7. Community files as discovery/reference only; popularity/duplicates do not prove quality, fit, originality or usage rights.

Recommended working rule: `structure first → component/state reuse → prototype only the risky flow → handoff only pinned/approved frames → runtime compare after implementation`.

## Market research and successful-case classification

The user-approved threshold is split into two non-interchangeable labels:

- `VERIFIED_100K_DOWNLOAD_INSTALL`: an official store/developer source visibly establishes at least 100,000 downloads/installs. Google Play public download bands qualify, but the band is a lower bound rather than an exact lifetime count.
- `VERIFIED_100K_SALES`: a developer/publisher/platform primary statement establishes at least 100,000 paid units sold.

Additional labels:

- `ESTIMATE_ONLY`: third-party estimated owner/sales/download/revenue data.
- `POPULARITY_SIGNAL_ONLY`: reviews, followers, wishlists, CCU, chart rank, social reach or Community duplication without direct sales/download proof.
- `BLOCKED_UNVERIFIED`: success threshold cannot be verified from an allowed source.

Downloads, sales, revenue, wishlists, CCU and review count must never be converted into each other.

## Market sources

Primary/official first:

- Google Play product pages for public download bands and current mobile product facts.
- Steam store pages and Steamworks official docs for current product/review/platform facts; public Steam pages do not supply a universal exact download count.
- Developer/publisher primary milestone posts, press releases and postmortems for sales milestones when available.

Professional/estimate/discovery sources:

- SteamDB: store/release/history/discovery signals; not Valve authority and not sales truth.
- Video Game Insights / Sensor Tower VGI: estimated Steam units/revenue; methodology must be preserved as estimate evidence.
- GameDiscoverCo: professional discovery/market analysis and case-study hypotheses.
- AppMagic/Sensor Tower when available: mobile market estimates, kept separate from official store download bands.

## Successful examples used as calibration, not templates

Examples should be refreshed when used. Current verified mobile calibration examples include:

- `Slice & Dice`: Google Play public page currently shows `1M+ Downloads`.
- `Mindustry`: Google Play public page currently shows `5M+ Downloads`.
- `Shattered Pixel Dungeon`: Google Play public page currently shows `5M+ Downloads`.

They qualify for `VERIFIED_100K_DOWNLOAD_INSTALL`; the number alone does not prove why the game succeeded.

PC/console sales examples may be included only when a primary developer/publisher/platform milestone supports `VERIFIED_100K_SALES`; news or estimate sources can lead discovery but should be backtraced before durable classification.

## Kick / individuality extraction

Do not copy a feature list. For each comparison case, extract:

```text
observable success signal
→ target player/context
→ repeated player action
→ expectation/promise
→ distinctive constraint or combination
→ feedback/reward/readability
→ production/marketing advantage
→ player praise and complaints
→ counterexample/failure condition
→ transferable design principle
→ project-specific twist candidate
→ cheapest falsifiable test
```

A `KICK_CANDIDATE` must be expressible as a player-observable difference and should combine at least two dimensions such as mechanic + presentation, constraint + reward, input + pacing, or theme + system. A cosmetic novelty with no effect on expectation, decision, feedback or recall stays `SURFACE_NOVELTY`.

Kick dispositions:

- `KEEP_PROJECT_IDENTITY`
- `ADAPT_PRINCIPLE`
- `TEST_KICK`
- `AVOID_COPY`
- `REJECT_NON_CAUSAL`
- `BLOCKED_UNVERIFIED`

## Figma research-board use

When useful, FigJam/Figma may visualize research using sections such as:

```text
00_RESEARCH_QUESTION
10_DIRECT_COMPETITORS
20_ADJACENT_GAMES
30_100K_PLUS_VERIFIED
40_PLAYER_PRAISE
50_PLAYER_PAIN
60_FAILURE_MIXED_CASES
70_KICK_CANDIDATES
80_COUNTEREXAMPLES
90_DECISION_AND_TEST
```

Each card carries source/date/platform/evidence label and links back to the responsible GitHub research record. The visual board is not a second canon.

## Claim ceilings

Reject these shortcuts:

- `100K+ == good design`
- `downloads == sales`
- `sales == profit`
- `reviews/wishlists/CCU == downloads`
- `third-party estimate == verified milestone`
- `successful feature == causal reason for success`
- `Figma Community popularity == professional quality or usage rights`
- `prototype == Godot runtime proof`
- `novel visual == durable game kick`

## Validation

TDD should fail before production guidance exists, then pass after minimum owner/source updates. Final validation uses existing Base contract tests, exact-head GitHub Actions, adversarial review and same-goal PR checks.