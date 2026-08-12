# Figma Practical Use + Game Market Research / Success Case Design

- date: 2026-08-12
- baseline main: `4288871809239a402a2d73ffcedd4d7330bf6136`
- approved direction: user approved recommended approach in current task
- work mode: PLAN → BUILD → REVIEW

## 1. Goal

Base가 다음 두 질문에 더 잘 답하도록 한다.

1. **Figma를 실제 게임 개발에서 어떻게 빠르고 안정적으로 쓰는가?**
2. **시장·경쟁작·성공작을 어떻게 조사해 우리 게임만의 뾰족한 킥으로 변환하는가?**

새 `figma-*` Skill이나 새 시장조사 Skill을 만들지 않는다. 기존 Figma visual workspace 계약과 `analyzing-and-refining-game-concepts` benchmark owner를 확장한다.

## 2. Existing Solution First

Current Base already owns:

- Figma authority / lifecycle: `docs/VISUAL_COLLABORATION_TOOL_POLICY.md`
- project Figma Visual Bible: `templates/project-operations/FIGMA_VISUAL_BIBLE_PROFILE.md`
- Figma Team/Project/File/Page structure: `templates/project-operations/FIGMA_WORKSPACE_STRUCTURE_PROFILE.md`
- actual project Figma pointers: `docs/operations/PROJECT_FIGMA_WORKSPACE_REGISTRY.json`
- market / benchmark / player evidence: `skills/analyzing-and-refining-game-concepts/references/benchmark-player-evidence-and-playtests.md`
- recurring external intake: `docs/knowledge/game-development/PERIODIC_EXTERNAL_SOURCE_DISCOVERY_SEEDS.md`

Therefore the disposition is `ABSORB_EXISTING_OWNER`, not `BUILD_NEW`.

## 3. Considered approaches

### A. Create a new Figma + market research Skill

Pros: one obvious entry point.

Reject: duplicates current Figma and game-concept owners, creates a tool-named Skill merely because Figma exists, and mixes visual authoring with product strategy authority.

### B. Add only source URLs to Discovery Seeds

Pros: smallest diff.

Reject: does not answer the user's request for concrete usage tips, practical know-how, success qualification, comparison method, or kick extraction.

### C. Recommended — owner-local practical rules + source seeds

- extend `FIGMA_WORKSPACE_STRUCTURE_PROFILE.md` with practical use patterns;
- extend the existing benchmark reference with market/success-case evidence and kick extraction;
- add Figma + market intelligence source groups to Discovery Seeds;
- add focused regression tests.

This keeps source discovery separate from durable working method and preserves authority boundaries.

## 4. Figma practical-use design

### 4.1 Source authority

Use Figma official Learn / Help as `AUTHORITY_TARGET` only for Figma behavior and availability:

- plans/features: `https://help.figma.com/hc/en-us/articles/360040328273-Figma-plans-and-features`
- Auto Layout: `https://help.figma.com/hc/en-us/articles/360040451373-Guide-to-auto-layout`
- 2026 Auto Layout / CSS Flexbox migration guidance: `https://help.figma.com/hc/en-us/articles/42031586813719-Use-auto-layout-with-CSS-Flexbox-in-mind`
- components / variants: `https://help.figma.com/hc/en-us/articles/39636737843735-Components-collection-Variants-and-component-set-fundamentals`
- interactive components: `https://help.figma.com/hc/en-us/articles/360061175334-Create-interactive-components-with-variants`
- variables: `https://help.figma.com/hc/en-us/articles/15339657135383-Guide-to-variables-in-Figma`
- prototyping: `https://help.figma.com/hc/en-us/articles/360040314193-Guide-to-prototyping-in-Figma`
- Dev Mode: `https://help.figma.com/hc/en-us/articles/15023124644247-Guide-to-Dev-Mode`
- sections: `https://help.figma.com/hc/en-us/articles/9771500257687-Organize-your-canvas-with-sections`
- FigJam: `https://help.figma.com/hc/en-us/articles/1500004362321-Guide-to-FigJam`

### 4.2 Practical operating sequence

```text
question / screen purpose
→ rough FigJam or low-fi frame only when uncertainty is structural
→ frame + Auto Layout
→ repeated UI becomes Component
→ state/size/type becomes Variant or component property
→ repeated design value becomes Variable only when reuse justifies it
→ Prototype for flow/interaction hypothesis
→ approved-reference comparison
→ Ready for dev / annotation / Dev Mode handoff
→ Godot runtime capture
→ compare board / drift classification
```

### 4.3 Practical tips to encode

- **Auto Layout first, pixel pushing second** for repeated/responsive UI. Use `Shift+A`; use Hug/Fill/fixed intentionally rather than arbitrary coordinates.
- Current 2026 Figma Auto Layout is moving toward closer CSS Flexbox semantics. Existing legacy frames should not be mass-upgraded without comparison; newly created frames may use the current layout behavior.
- **Components are for real reuse**, not every object. Promote after the same UI concept repeats or must stay synchronized.
- **Variants encode predictable dimensions** such as `state`, `size`, `type`; avoid giant Cartesian-product component sets because large variant sets cost navigation/performance.
- **Variables encode reusable tokens/state**, not every numeric value. Recommended game UI collections: color/semantic role, spacing, typography role, platform/density mode, optional prototype state.
- Use **interactive components** to avoid prototype “noodle soup” for button/toggle/input states.
- Use **Sections** as review/handoff boundaries and meaningful navigation anchors, not decorative rectangles.
- Use **FigJam** for market map, affinity grouping, competitor screenshots/notes, journey/system diagrams, and critique. Do not promote FigJam notes to canon without the normal evidence/Decision gate.
- Use **Dev Mode** after an artifact is `IMPLEMENTATION_PINNED`; inspect spacing, variables, assets, component properties, status/annotations, and version differences. Auto-generated code is a translation aid, not production correctness evidence.
- Name layers/components for semantic purpose (`Button/Primary`, `HUD/ResourceChip`) rather than appearance-only labels (`BlueRect`).
- Prefer duplication into WIP before destructive change to approved reference.
- Keep screenshot/reference boards visually close to the comparison table/card, but preserve source URL/date/version in editable text.

### 4.4 Figma anti-patterns

Reject:

- manual absolute positioning for a repeated responsive UI where Auto Layout clearly fits;
- componentizing one-off decoration;
- one giant component with dozens of unrelated variant dimensions;
- variable/token proliferation without reuse;
- prototypes treated as runtime proof;
- Dev Mode snippets pasted into Godot as proof of correctness;
- market/research boards becoming a second game-design canon;
- copying competitor UI/art layout as a shortcut to “best practice”.

## 5. Market research and comparison design

### 5.1 Source roles

#### Primary / official product facts

- Steam store / Steamworks official docs — product facts, reviews, visibility, Playtest behavior.
- Google Play store pages — public install buckets when shown (`100K+`, `1M+`, `5M+`, etc.).
- developer/publisher official announcements / Steam community announcements — exact sales milestone when explicitly stated.

#### Professional / market intelligence

- SteamDB — independent Steam catalog, player charts, price/update history; owner numbers are third-party estimates and must retain that label.
- GameDiscoverCo — PC/console discoverability analysis and market-data practice.
- Sensor Tower Game IQ / VGI — mobile and Steam market intelligence; downloads/revenue/units are estimates unless traced to a first-party release.

These sources are research inputs, never project canon.

### 5.2 Success qualification

The user-approved success threshold is encoded with **separate labels**:

```text
VERIFIED_100K_DOWNLOAD_INSTALL
VERIFIED_100K_SALES
ESTIMATED_100K_PLUS
NOT_100K_VERIFIED
```

Rules:

- `VERIFIED_100K_DOWNLOAD_INSTALL`: official/public store install/download bucket or first-party explicit download statement >= 100,000.
- `VERIFIED_100K_SALES`: developer/publisher/platform first-party statement of paid copies >= 100,000.
- `ESTIMATED_100K_PLUS`: SteamDB/VGI/Sensor Tower/AppMagic-like model estimate >= 100,000; never relabel as verified sales/downloads.
- wishlists, reviews, followers, CCU, rank, revenue, gross, MAU, subscribers are not interchangeable with downloads/sales.

### 5.3 Seed success cases

Use a small verified seed set, not a hall of fame:

- `Shattered Pixel Dungeon` — Google Play `5M+` downloads → `VERIFIED_100K_DOWNLOAD_INSTALL`.
- `Mindustry` — Google Play `5M+` downloads → `VERIFIED_100K_DOWNLOAD_INSTALL`.
- `Slice & Dice` — Google Play `1M+` downloads → `VERIFIED_100K_DOWNLOAD_INSTALL`.
- `Sledding Game` — developer Steam announcement: 100,000 copies in 5 days → `VERIFIED_100K_SALES`.
- `God Of Weapons` — developer/publisher Steam announcement: over 100,000 copies in two weeks → `VERIFIED_100K_SALES`.
- `Astrea: Six-Sided Oracles` — developer Steam announcement: over 100,000 copies within four months → `VERIFIED_100K_SALES`.

The cases prove threshold membership only. They do **not** prove why each game succeeded.

## 6. Kick extraction method

A “kick” is not an unusual feature list. It is a compact, player-legible differentiation that changes expectation or repeated decision.

For every comparable game, extract:

```yaml
success_evidence_label:
threshold_evidence:
target_player:
core_action:
standard_genre_promise:
observable_twist:
why_player_notices_it_in_30_seconds:
repeated_decision_changed:
store_capsule_or_trailer_legibility:
production_cost:
copy_risk:
our_transferable_principle:
do_not_copy:
project_kick_candidate:
validation:
```

### Kick ladder

```text
market table-stakes
→ repeated player action
→ expectation/tension/power fantasy
→ one observable twist
→ one sentence / one GIF / one screenshot legibility
→ production-feasible expression
→ prototype or store-page comprehension test
```

A strong candidate should satisfy at least three dimensions:

1. `PLAYER_NOTICEABLE` — players can notice it quickly without design explanation.
2. `LOOP_RELEVANT` — it changes repeated play, not only lore or cosmetic theme.
3. `MARKET_LEGIBLE` — capsule/trailer/demo can communicate it.
4. `PRODUCTION_FIT` — feasible for the project/team.
5. `NON_DERIVATIVE` — principle is adapted without copying identifiable execution.

## 7. Comparison board / FigJam use

When visual comparison helps, FigJam/Figma may hold a board with:

```text
DIRECT_COMPETITORS
ADJACENT_MECHANIC_REFERENCES
FAILURE_OR_MIXED_CASES
VERIFIED_100K_CASES
TABLE_STAKES
KICK_CANDIDATES
DO_NOT_COPY
TEST_NEXT
```

Each card keeps source/date/platform/evidence label. The board is a visualization of the benchmark reference, not a second canonical decision store.

## 8. Files and responsibility

Expected final durable changes:

1. `templates/project-operations/FIGMA_WORKSPACE_STRUCTURE_PROFILE.md`
   - add practical use / productivity / anti-pattern section.
2. `skills/analyzing-and-refining-game-concepts/references/benchmark-player-evidence-and-playtests.md`
   - add market-source roles, 100K evidence labels, success-case card, kick extraction.
3. `docs/knowledge/game-development/PERIODIC_EXTERNAL_SOURCE_DISCOVERY_SEEDS.md`
   - add `Figma practical design workflow` and `Game market intelligence + verified success cases` discovery groups.
4. focused tests in existing test owners.

Design/plan files are process evidence. Existing Solution First review may remove them from final net diff if no durable consumer requires them.

## 9. Test-first acceptance

RED should fail on absence of at least:

- Figma practical tokens: `Auto Layout`, `Variants`, `Variables`, `FigJam`, `Dev Mode` plus prototype/runtime ceiling.
- market evidence labels: `VERIFIED_100K_DOWNLOAD_INSTALL`, `VERIFIED_100K_SALES`, `ESTIMATED_100K_PLUS`.
- market sources: `SteamDB`, `GameDiscoverCo`, `Sensor Tower`.
- kick route: `PLAYER_NOTICEABLE`, `LOOP_RELEVANT`, `MARKET_LEGIBLE`, `PRODUCTION_FIT`, `NON_DERIVATIVE`.
- verified case names including mobile install and Steam sales examples.

GREEN must preserve existing authority rules and pass the same relevant full Base suites / required `ci-gate` used by current main.

## 10. Adversarial review targets

Explicitly attack:

- `100K` metric laundering across downloads / sales / estimates / revenue / wishlists / reviews / CCU;
- survivor bias: success cases without failure/mixed comparison;
- post-hoc causality: successful game feature → claimed cause of success;
- popularity → design quality authority;
- copying signature UI/art/mechanic expression;
- Figma feature availability → mandatory process;
- complex design-system theater for a solo project;
- FigJam/Figma becoming canon;
- transient source counts treated as permanent facts without `checked_at`.

Expected final disposition: `LOW_RISK_BOUNDED_UPDATE` if no authority/security/policy boundary changes are introduced.