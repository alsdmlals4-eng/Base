# Narrative & World Knowledge Model Design

## Status

- Date: 2026-08-23
- Scope: Base common narrative/world research and canon organization
- First pilot: COC-Fiction
- Existing open PRs: read-only; PR #620 is not modified or absorbed
- New broad skill: NO
- New dashboard: NO

## Problem

Projects currently have good individual methods for narrative/relationship design, character art, canon freshness, and external source research, but they lack one common layer for turning raw project sources into a stable human-readable knowledge system.

Without that layer, the same failure repeats:

- a generated image or Visual Index is mistaken for canon,
- a legacy manuscript phrase is treated as the current fact,
- character biography, event history, relationship changes, world rules, and evidence are mixed into one long page,
- one huge Character Bible becomes difficult to audit,
- candidate material and confirmed canon are shown at the same visual weight,
- character/world images are produced before the text facts are approved,
- summary pages become too dense to read.

The new model fills only this missing layer. Existing owners remain authoritative:

- `NARRATIVE_AND_RELATIONSHIP_METHOD.md`: scene/dialogue/relationship execution
- `CHARACTER_AND_NARRATIVE_ART_METHOD.md`: visual identity and asset design
- `NARRATIVE_WORLD_CHARACTER_SOURCE_RADAR.md`: external research sources
- `auditing-canonical-reference-freshness`: stale/canon drift audit
- project canon/AGENTS/current source: project-specific truth

## Benchmark Findings

### articy:draft

articy separates stable Entities from Flow events and uses References to connect entities, locations, dialogue and story objects. Project-specific templates add only the properties required for the object type. The useful principle is separation of identity from event flow, with explicit references between them.

### World Anvil

World Anvil uses short article introductions as primers, then type-specific detailed articles. Characters, organizations and other world objects have structured relations, while plot/timeline content is separate. The useful principle is summary-first navigation plus linked typed detail.

### Notion

Notion databases are collections of pages. Gallery cards can expose only a small set of properties, while opening a card reveals the full page. Gallery views open database pages in `Center peek` by default, providing the desired summary-first → popup-detail interaction without duplicating content. Custom layouts and a collapsible details panel can keep high-density metadata out of the main reading area.

## Alternatives

### A. Five independent databases

`Entity / Event / Relation / Rule / Evidence` each as its own database.

Pros:
- strongest semantic separation
- simple type-specific schemas

Cons:
- too many databases and relations for small/medium solo projects
- higher maintenance and migration cost
- hard to reuse cleanly across projects with different narrative density

Decision: REJECT as default; reserve for very large narrative teams.

### B. Three physical databases with five conceptual layers

1. `NARRATIVE KNOWLEDGE · Master`
   - Entity: Character, Faction, Location, Item, Clue, Setting
   - Relation
   - Rule
2. `NARRATIVE EVENT · Ledger`
   - Event, choice, reveal, battle, relationship change, historical event
3. `CANON EVIDENCE · Ledger`
   - claim evidence, source authority, conflicts, supersession

Conceptual layers remain `Entity → Event → Relation → Rule → Evidence`, but Notion implementation is only three databases.

Pros:
- clear responsibility boundaries
- manageable database count
- supports articy-like Entity/Flow separation
- supports World-Anvil-like typed article views
- supports project-wide reuse and filtering
- supports evidence-backed conflict audits

Cons:
- `NARRATIVE KNOWLEDGE` needs type-aware page templates
- relationship objects share the master with stable entities

Decision: ADOPT.

### C. Extend ASSET LIBRARY into narrative canon

Pros:
- no new database
- existing Project relation and views

Cons:
- mixes visual assets with narrative truth
- repeats the current failure where Character Bible points at Asset Library
- weak evidence/conflict modeling
- makes images look authoritative before text is approved

Decision: REJECT.

## Common Conceptual Model

### 1. Entity

Stable identity: who/what it is.

Examples:
- Character
- Faction
- Location
- Item
- Clue
- Setting

Entity pages do not own long chronological activity logs.

### 2. Event

What actually happened and what changed.

Minimum shape:

```yaml
starting_state:
pressure_or_goal:
choice_or_action:
outcome:
cost_or_consequence:
state_change:
relationship_change:
```

### 3. Relation

A relationship is a first-class knowledge object, not only a tag.

Minimum shape:

```yaml
source:
target:
relationship_type:
source_view_of_target:
target_view_of_source:
power_debt_dependency:
current_state:
change_events:
```

Direction matters. `A → B` and `B → A` may differ.

### 4. Rule

A world rule records possibility, limit, cost and exceptions.

Minimum shape:

```yaml
rule_domain:
allows:
forbids:
cost:
exception:
knowledge_holders:
first_observed:
first_confirmed:
```

A character claim is not automatically a world rule.

### 5. Evidence

Evidence answers why a claim is allowed to appear as fact.

Source authority order defaults to:

```text
latest user decision
→ project current canon
→ approved planning
→ current candidate
→ legacy material
→ external reference
```

Projects may override the exact authority chain in `AGENTS.md`.

## Notion Physical Model

### NARRATIVE KNOWLEDGE · Master

Required properties:

- `Name` — title
- `Project` — relation to PROJECT REGISTRY
- `Type` — Character / Faction / Location / World Rule / Relationship / Item / Clue / Setting
- `Scope` — part/arc/region/system scope
- `Summary` — human-facing primer, short enough for card view
- `Core Function` — why this exists in the work
- `Aliases` — names/disguises/old spellings; must not silently redefine identity
- `Current State`
- `Canon Status` — CORE_CONFIRMED / CONFIRMED / CURRENT_CANDIDATE / INFERRED / UNKNOWN / CONFLICT / DEPRECATED
- `Text Approval` — DRAFT / REVIEW_REQUIRED / APPROVED / REPLACED
- `Visual Gate` — BLOCKED_BY_TEXT / READY_FOR_VISUAL / VISUAL_CANDIDATE / VISUAL_APPROVED / REPLACED
- `Related Knowledge` — self relation
- `Relation Source` — self relation, used only for Relationship rows
- `Relation Target` — self relation, used only for Relationship rows

### NARRATIVE EVENT · Ledger

Required properties:

- `Name`
- `Project`
- `Scope`
- `Sequence`
- `Event Type`
- `Summary`
- `Participants` — relation to Knowledge Master
- `Canon Status`
- `Starting State`
- `Choice / Action`
- `Outcome`
- `Cost / Consequence`
- `State Change`
- `Relationship Change`

### CANON EVIDENCE · Ledger

Required properties:

- `Name`
- `Project`
- `Claim`
- `Knowledge Targets`
- `Event Targets`
- `Source Type` — USER_DECISION / GITHUB_CANON / GITHUB_MANUSCRIPT / NOTION_DECISION / RUNTIME_EVIDENCE / EXTERNAL_SOURCE
- `Source Locator`
- `Authority Tier` — A0_USER / A1_CANON / A2_APPROVED_PLANNING / A3_CURRENT_CANDIDATE / A4_LEGACY / A5_EXTERNAL
- `Verdict` — SUPPORTS / CONFLICTS / UNVERIFIED / SUPERSEDED
- `Checked At`
- `Notes`

## Summary → Popup Detail UX

Primary human-facing navigation is a Gallery view.

Each card shows only:

- Name
- Summary
- Core Function
- Scope
- Canon Status
- Text Approval

The page body is not rendered on the overview.

Interaction:

```text
summary gallery card
→ click card / “상세 보기” affordance
→ Center peek modal
→ short primer remains at top
→ toggles/sections reveal detailed content
```

For connector-built workspaces, the card itself is the canonical `상세 보기` control. Do not duplicate a second full page just to simulate a popup button.

Recommended detail page structure for Characters:

```text
Primer
→ Character Engine
→ Major Events
→ Relationships
→ Current State
→ Visual Contract
→ Distortion Guards
→ Evidence / Conflict Notes
```

Recommended detail page structure for world/faction/rule records:

```text
Primer
→ Function in the world
→ Observable rules / constraints
→ Major events
→ Relations
→ Unknowns / conflicts
→ Visual contract if needed
→ Evidence
```

Long sections should use toggles when they are not required for first-read comprehension.

## Text-first Visual Gate

No character/world/faction image is created from an unapproved description.

```text
source authority check
→ structured extraction
→ contradiction audit
→ human summary
→ user approval
→ Text Approval = APPROVED
→ Visual Gate = READY_FOR_VISUAL
→ visual contract
→ image generation
→ visual review
→ placement
```

If image and approved text conflict, approved text wins.

Existing images may be retained as `VISUAL_CANDIDATE` or `REPLACED`, but cannot backfill missing canon by inference.

## Research Pipeline

### Phase 0 — Authority Map

List current sources and authority order before extracting facts.

### Phase 1 — Object Extraction

Extract only existence and identity first:

- characters
- factions
- locations
- rules
- items/clues

Do not write polished descriptions yet.

### Phase 2 — Event Extraction

For each scene/chapter/quest, record who acted, what they wanted, what they chose and what changed.

### Phase 3 — Relationship / Rule Extraction

Derive relationships and world rules only from supported events/claims. Preserve directional relationship states and `UNKNOWN` where evidence is incomplete.

### Phase 4 — Evidence Link

Every high-risk identity, death/survival, faction membership, ability, timeline boundary, disguise/alias, or reveal timing must have at least one evidence record.

### Phase 5 — Contradiction Audit

Check at minimum:

- name / alias drift
- sex/gender/presentation drift where relevant to identity
- part/arc/scope drift
- alive/dead/unknown drift
- faction membership drift
- ability/reveal timing drift
- relationship state drift
- event order drift
- candidate promoted as canon
- image or AI summary promoted as canon

### Phase 6 — Human Primer

Only after the conflict pass, write the short `Summary` and `Core Function` shown on overview cards.

### Phase 7 — User Approval

Approval changes `Text Approval` from `REVIEW_REQUIRED` to `APPROVED`.

### Phase 8 — Visual

Only approved text can become a visual contract.

## Character Research Contract

A character is organized around what makes them usable in scenes, not biography volume.

Detail sections:

- identity / public role / hidden presentation if canonically relevant
- core desire / need / fear / contradiction
- attention filter / decision rule / moral boundary
- competence / limitation / cost of strength
- voice / body language / social mask
- major events and state changes from Event Ledger
- directional relationships
- current status
- visual identity and reveal variants
- distortion guards

`Major Events` are references to Event Ledger; the full chronology is not duplicated in the character page.

## World Research Contract

Worldbuilding is organized by lived consequence.

A setting/rule/faction/location page must answer at least one:

- what choice does this create or remove?
- what everyday behavior does it change?
- what resource/institution/risk flow does it create?
- what scene/system makes it observable?

Unused encyclopedia volume is not promoted merely because it is interesting.

## COC-Fiction Pilot

COC is the first migration target because it already exposed the failure modes this model is intended to stop.

Pilot order:

1. build the three common databases without migrating unapproved character prose,
2. replace Character Bible's current Asset-Library-as-character-index role with a filtered Knowledge gallery,
3. keep Asset Library only as visual asset authority,
4. mark existing generated boards as non-canon visual candidates until text is approved,
5. rebuild Part 1 character text with source/evidence rows,
6. user approves text,
7. only then add final Character records and reopen visual production.

Known COC pilot guards:

- `밀리 코사` actual identity and university presentation must be separate fields/claims,
- `하템` default visual presentation and unmasked/reveal variants must be separate,
- Part 1 / Bridge / Part 2 / Rift Accord must not be merged by image inference,
- manuscript migration boundaries must remain visible instead of being flattened into one certainty level.

## Implementation Reality Gate

Claim ceiling:

- Method file present ≠ project migration complete
- Database created ≠ knowledge extracted
- Knowledge extracted ≠ canon approved
- Text approved ≠ visual approved
- Visual approved ≠ runtime/reader validation
- Center-peek design documented ≠ every client/platform pixel layout verified

Notion Gallery default Center Peek behavior is platform capability; exact mobile geometry remains `UI_GEOMETRY_NOT_VERIFIED` until observed.

## Success Criteria

- no project needs a separate bespoke character/world database schema to begin
- overview pages show short primers, not wall-of-text biographies
- detailed pages can be opened from summary cards without duplicating content
- events are not copied into character biographies as the only source of chronology
- candidate/legacy evidence cannot silently become confirmed canon
- visual generation is blocked until text approval
- COC Character Bible no longer uses Asset Library as its narrative knowledge index
- existing narrative/relationship/art/source-radar owners remain intact
