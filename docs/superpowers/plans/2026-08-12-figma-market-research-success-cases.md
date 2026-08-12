# Figma Practical Use + Game Market Research / Success Cases Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Extend existing Base Figma and game-concept owners with practical Figma usage, market-research sources, separately qualified 100K+ success evidence, comparison discipline, and project-kick extraction without creating a new Skill.

**Architecture:** Keep Figma operational craft in the existing workspace profile, market/success-case reasoning in the existing benchmark reference, and changing external sites in Discovery Seeds. Regression tests assert both durable method and source-routing boundaries. Figma remains noncanonical and success metrics never mix verified downloads, verified sales, and estimates.

**Tech Stack:** Markdown contracts, Python `unittest`, GitHub Actions / existing Base validation.

## Global Constraints

- Baseline main: `4288871809239a402a2d73ffcedd4d7330bf6136`.
- No new ACTIVE Skill, Registry entry, dependency, workflow authority, Figma project mutation, or project-specific canon.
- `VERIFIED_100K_DOWNLOAD_INSTALL`, `VERIFIED_100K_SALES`, `ESTIMATED_100K_PLUS`, `NOT_100K_VERIFIED` stay distinct.
- Reviews, wishlists, followers, CCU, gross/revenue, installs/downloads, and paid sales are not interchangeable.
- Successful-game features are not causal proof; use success cases together with failure/mixed cases.
- Figma/ FigJam are visual/research workspaces, not game-rule canon or runtime proof.
- Current Figma feature availability comes from official Figma sources and must be rechecked when decisions depend on plan/version state.
- Market estimates retain estimate labeling and source/method context.
- Existing Solution First / consolidation-first; process spec/plan may be removed from final net diff after they have served execution history.

---

### Task 1: Add RED contract tests for Figma practical use and market-success evidence

**Files:**
- Modify: `tests/test_visual_collaboration_capability_contract.py`
- Modify: `tests/test_periodic_external_source_discovery_seeds.py`

**Interfaces:**
- Consumes: existing `FIGMA_WORKSPACE_STRUCTURE_PROFILE.md`, benchmark reference, Discovery Seeds.
- Produces: focused regression methods that fail before production docs are changed and pass after implementation.

- [ ] **Step 1: Add Figma practical-use failing test**

Append a method that reads `templates/project-operations/FIGMA_WORKSPACE_STRUCTURE_PROFILE.md` and requires:

```python
for token in (
    "Auto Layout",
    "Shift+A",
    "Variants",
    "Variables",
    "interactive components",
    "FigJam",
    "Dev Mode",
    "prototype",
    "runtime proof",
    "componentizing one-off decoration",
):
    self.assertIn(token, profile)
```

- [ ] **Step 2: Add market/success/kick failing test**

Extend `tests/test_periodic_external_source_discovery_seeds.py` with a benchmark path constant and a method that requires in seed + benchmark content:

```python
for token in (
    "SteamDB",
    "GameDiscoverCo",
    "Sensor Tower",
    "VERIFIED_100K_DOWNLOAD_INSTALL",
    "VERIFIED_100K_SALES",
    "ESTIMATED_100K_PLUS",
    "Shattered Pixel Dungeon",
    "Mindustry",
    "Slice & Dice",
    "Sledding Game",
    "God Of Weapons",
    "Astrea: Six-Sided Oracles",
    "PLAYER_NOTICEABLE",
    "LOOP_RELEVANT",
    "MARKET_LEGIBLE",
    "PRODUCTION_FIT",
    "NON_DERIVATIVE",
):
    self.assertIn(token, combined)
```

Also require an explicit boundary such as:

```python
self.assertIn("downloads", combined.lower())
self.assertIn("sales", combined.lower())
self.assertIn("estimate", combined.lower())
self.assertIn("causal", combined.lower())
```

- [ ] **Step 3: Run focused RED tests**

Run through the repository's existing Evidence Knowledge / relevant unittest workflow on the branch head.

Expected: existing tests pass; the two newly added methods fail because production docs do not yet contain the required contracts.

- [ ] **Step 4: Record RED exact head in the PR body later**

Do not call the suite GREEN and do not change production docs before RED is observed.

---

### Task 2: Add practical Figma usage and efficiency guidance

**Files:**
- Modify: `templates/project-operations/FIGMA_WORKSPACE_STRUCTURE_PROFILE.md`
- Test: `tests/test_visual_collaboration_capability_contract.py`

**Interfaces:**
- Consumes: existing Figma authority/lifecycle and official Figma Learn sources.
- Produces: project-copyable practical guidance without changing Figma's authority.

- [ ] **Step 1: Add a `실전 사용법·팁·노하우` section**

Include this sequence:

```text
question / screen purpose
→ FigJam or low-fi only when structural uncertainty is high
→ frame + Auto Layout
→ repeated UI → Component
→ predictable state/size/type → Variants / component properties
→ repeated design value/state → Variables when reuse justifies it
→ Prototype for flow hypothesis
→ approved-reference comparison
→ Ready for dev / annotation / Dev Mode
→ Godot runtime capture
→ compare board / drift classification
```

- [ ] **Step 2: Add practical rules**

Include:

- `Shift+A` Auto Layout use and intentional Hug/Fill/fixed behavior.
- 2026 Auto Layout / Flexbox migration freshness note; no mass upgrade without visual comparison.
- component promotion only after real reuse/synchronization need.
- predictable `state/size/type` variant axes; avoid giant Cartesian-product sets.
- variables for reusable token/state collections, not every raw number.
- interactive components for button/toggle/input state reuse.
- Sections for review/handoff navigation.
- FigJam for market map, affinity grouping, diagrams, critique and research organization.
- Dev Mode only after handoff readiness; snippets are aids, not production proof.
- semantic component/layer naming.

- [ ] **Step 3: Add Figma anti-patterns**

Require explicit rejection of:

```text
manual responsive pixel-pushing when Auto Layout clearly fits
componentizing one-off decoration
giant unrelated variant matrices
variable/token proliferation
prototype == runtime proof
Dev Mode code snippet == production correctness
FigJam research board == game canon
competitor UI/art copying
```

- [ ] **Step 4: Run Figma focused test**

Expected: new Figma practical-use method PASS; prior visual-collaboration tests remain PASS.

---

### Task 3: Add market research, 100K qualification, success cards, and kick extraction

**Files:**
- Modify: `skills/analyzing-and-refining-game-concepts/references/benchmark-player-evidence-and-playtests.md`
- Test: `tests/test_periodic_external_source_discovery_seeds.py`

**Interfaces:**
- Consumes: existing benchmark Evidence Pack and comparison methodology.
- Produces: reusable success-evidence labels, card schema, market-source roles, and differentiation extraction.

- [ ] **Step 1: Add market source hierarchy**

Encode:

```text
first-party store / platform / developer statement
→ VERIFIED fact where metric is explicit
professional market intelligence
→ estimate / discovery evidence only
community / article interpretation
→ hypothesis / context only
```

Market sites:

- SteamDB: catalog, CCU, prices, update history; owner numbers are third-party estimates.
- GameDiscoverCo: PC/console discovery and market analysis.
- Sensor Tower Game IQ / VGI: mobile/Steam market intelligence; estimated downloads/revenue/units retain estimate status.

- [ ] **Step 2: Add success qualification labels**

```text
VERIFIED_100K_DOWNLOAD_INSTALL
VERIFIED_100K_SALES
ESTIMATED_100K_PLUS
NOT_100K_VERIFIED
```

Explicitly state that downloads, paid sales, revenue/gross, wishlists, reviews, followers and CCU are separate metrics.

- [ ] **Step 3: Add compact verified seed examples**

Record threshold evidence only:

```text
Shattered Pixel Dungeon — Google Play 5M+ downloads
Mindustry — Google Play 5M+ downloads
Slice & Dice — Google Play 1M+ downloads
Sledding Game — Steam developer announcement, 100,000 copies in 5 days
God Of Weapons — Steam developer announcement, over 100,000 copies in 2 weeks
Astrea: Six-Sided Oracles — Steam developer announcement, over 100,000 copies within 4 months
```

Add `checked_at: 2026-08-12` and source type. Do not claim causal success reasons from the milestone.

- [ ] **Step 4: Add success/comparison card schema**

Use:

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

- [ ] **Step 5: Add kick ladder and quality dimensions**

```text
market table-stakes
→ repeated player action
→ expectation / tension / fantasy
→ one observable twist
→ one sentence / GIF / screenshot legibility
→ production-feasible expression
→ prototype or store-page comprehension test
```

Require at least three of:

`PLAYER_NOTICEABLE`, `LOOP_RELEVANT`, `MARKET_LEGIBLE`, `PRODUCTION_FIT`, `NON_DERIVATIVE`.

- [ ] **Step 6: Add survivor-bias and causality guard**

Every meaningful research pack must preserve the existing direct competitors + adjacent mechanic references + failure/mixed cases composition. Success milestone membership cannot be used as proof that a specific mechanic caused success.

---

### Task 4: Register Figma and market-intelligence discovery sources

**Files:**
- Modify: `docs/knowledge/game-development/PERIODIC_EXTERNAL_SOURCE_DISCOVERY_SEEDS.md`
- Test: `tests/test_periodic_external_source_discovery_seeds.py`

**Interfaces:**
- Consumes: official Figma, platform/store, professional market sources.
- Produces: recurring discovery inputs routed to existing owners; does not automatically promote them to durable Watchlist authority.

- [ ] **Step 1: Add `Figma practical design workflow` seed group**

Source role: Figma official URLs as `AUTHORITY_TARGET` for Figma behavior only.

Scan surfaces:

```text
Auto Layout + 2026 layout-version changes
Components / Variants / component properties
Variables / modes
Interactive components
Prototype flows
Sections
FigJam research/diagramming
Dev Mode / ready-for-dev / annotations / version compare
plan/seat availability when decision-relevant
```

Route to existing visual collaboration policy/workspace profile and existing UI/art/handoff owners.

- [ ] **Step 2: Add `Game market intelligence + verified success cases` seed group**

Sources:

```text
Steam / Steamworks official
Google Play public store pages
first-party developer/publisher announcements
SteamDB
GameDiscoverCo
Sensor Tower Game IQ / VGI
```

Scan surfaces:

```text
release/price/review/CCU/wishlist or discovery context where available
mobile install/download buckets
first-party sales milestones
estimate methodology and confidence
platform/region/date/version
competitor table-stakes
observable differentiators / kick candidates
failure and mixed cases
```

- [ ] **Step 3: Add common claim ceilings**

```text
100K downloads != 100K paid sales
estimated owners != verified sales
revenue != unit sales
wishlists/reviews/followers/CCU != downloads or sales
success milestone != causal proof of a mechanic
popular UI/art != permission or design authority
Figma feature availability != mandatory workflow
```

- [ ] **Step 4: Run focused market/source tests**

Expected: new source/market method PASS.

---

### Task 5: Refactor process-only files if they add no durable consumer value

**Files:**
- Candidate remove: `docs/superpowers/specs/2026-08-12-figma-market-research-success-cases-design.md`
- Candidate remove: `docs/superpowers/plans/2026-08-12-figma-market-research-success-cases.md`

**Interfaces:**
- Consumes: Existing Solution First / anti-churn review.
- Produces: smaller final repository diff while PR history preserves process evidence.

- [ ] **Step 1: Review final consumer graph**

If no runtime/template/router/test consumes the spec/plan, remove them from final net diff before final validation. Keep their commit/PR history as execution evidence.

- [ ] **Step 2: Confirm final diff contains only durable owner/source/test changes**

Expected durable files: Figma workspace profile, benchmark reference, Discovery Seeds, focused tests.

---

### Task 6: Full verification, adversarial review, PR gate, merge, and post-change monitor

**Files:**
- No new production file expected beyond Tasks 2–4.

**Interfaces:**
- Consumes: final exact branch head and current main.
- Produces: evidence-backed merge or explicit blocker.

- [ ] **Step 1: Run focused tests on final head**

Run all affected test modules freshly after any refactor/removal.

- [ ] **Step 2: Run current Base required validation suites**

Use current repository workflows. Minimum target is the same Evidence Knowledge / Base v9 / Game Project OS `ci-gate` topology required on current main. Do not count skipped/non-applicable jobs as PASS.

- [ ] **Step 3: Run adversarial review**

Attack:

```text
metric laundering
survivor bias
post-hoc causality
popularity as authority
competitor copying
Figma-as-canon
Figma feature overengineering
new-Skill inflation
stale success metrics
same-goal duplicate PR/work
untouched consumer or test omissions
```

- [ ] **Step 4: Recheck current main and same-goal PRs**

If main advanced, revalidate strict-up-to-date compatibility. Do not force/rebase around Ruleset constraints.

- [ ] **Step 5: Open/update PR with RED/GREEN and evidence limits**

Record:

- baseline and exact head;
- source research checked on 2026-08-12;
- verified vs estimated metric labels;
- success cases as threshold evidence only;
- focused/full CI results;
- unresolved review threads;
- rejected overgeneralizations.

- [ ] **Step 6: Merge only if all current gates pass**

Use squash and expected-head protection when available.

- [ ] **Step 7: Post-merge readback and POST_CHANGE_MONITOR_LOOP**

Verify:

```text
merged main contains Figma practical guidance
merged main contains success metric labels and kick method
Discovery Seeds contains both new source groups
same-goal open PR = 0
untouched Figma/game-concept owners remain nonconflicting
no automation prompt update is needed if current automation already consumes all ACTIVE_DISCOVERY_SEED entries
```

Final verdict must be one of `NO_MATERIAL_FOLLOWUP`, `OMISSION`, `CONFLICT`, `COMPLEMENT_GAP`, or `DUPLICATE_WORK`.