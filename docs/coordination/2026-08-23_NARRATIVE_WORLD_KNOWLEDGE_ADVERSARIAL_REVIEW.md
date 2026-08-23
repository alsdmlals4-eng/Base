# Narrative & World Knowledge Model · Adversarial Review · 2026-08-23

## Scope

- Base branch: `docs/narrative-world-knowledge-20260823`
- Base method: `docs/knowledge/methods/NARRATIVE_WORLD_KNOWLEDGE_MODEL.md`
- First pilot: COC-Fiction Notion
- Existing PR #620: **read-only / untouched**
- No direct `main` write
- COC unapproved Part 1 prose: **not migrated**

## Benchmark references

Primary/product documentation reviewed during design:

- Notion Help · database views / `Open pages in` — Gallery & Calendar default to Center Peek; each view can choose Side peek / Center peek / Full page.
  - https://www.notion.com/help/views-filters-and-sorts
- Notion Help · databases are collections of pages; the same source can have multiple filtered views.
  - https://www.notion.com/help/intro-to-databases
- articy:draft · Entity objects, template-specific properties and reference connections.
  - https://www.articy.com/help/adx/Entities_Sheet.html
  - https://www.articy.com/help/legacy/Templates_Templates.html
- World Anvil · typed Articles, short introductions, relationships/diplomacy and separate Timelines.
  - https://www.worldanvil.com/learn/beginner-tutorials/get-started-articles
  - https://www.worldanvil.com/learn/article-guides/article-templates
  - https://www.worldanvil.com/learn/beginner-tutorials/get-started-timelines

The benchmark is used for structure, not for copying proprietary UI, prose or content.

## Alternative comparison

### A · five physical DBs

`Entity / Event / Relation / Rule / Evidence`

- Strength: strict semantic separation.
- Failure mode: too many databases/relations for solo and small-team projects; migration and maintenance cost rises quickly.
- Decision: `REJECT_AS_DEFAULT / OPTIONAL_LARGE_PROJECT`.

### B · three physical DBs / five conceptual layers

- `NARRATIVE KNOWLEDGE · Master` = Entity + Relation + Rule
- `NARRATIVE EVENT · Ledger` = Event
- `CANON EVIDENCE · Ledger` = Evidence

- Strength: keeps identity/event/evidence responsibilities distinct without exploding database count.
- Decision: `ADOPT`.

### C · extend ASSET LIBRARY

- Strength: no new database.
- Failure mode: visual references look like narrative canon; repeats the COC pollution incident.
- Decision: `REJECT`.

---

# Full Adversarial Loop 1 / 5 · responsibility / owner conflict

## Attack

Could the new Method duplicate or replace:

- `NARRATIVE_AND_RELATIONSHIP_METHOD.md`
- `CHARACTER_AND_NARRATIVE_ART_METHOD.md`
- `NARRATIVE_WORLD_CHARACTER_SOURCE_RADAR.md`
- `developing-and-revising-serial-fiction`

## Finding

The initial implementation plan proposed directly modifying the serial-fiction Skill. That would make a cross-project Knowledge Model look owned by a serial-fiction-specific execution Skill and create a duplicate routing dependency.

## Fix

- Keep one common Method under `docs/knowledge/methods/`.
- Route it from `docs/knowledge/README.md`.
- Keep the serial-fiction Skill unchanged.
- Existing owners remain:
  - scene/dialogue/relationship execution → Narrative & Relationship Method
  - visual identity → Character & Narrative Art Method
  - external source discovery → Source Radar
  - structured canon extraction/audit → new Knowledge Model

## Re-attack result

`PASS` — no broad Skill added; no existing owner displaced.

---

# Full Adversarial Loop 2 / 5 · canon / candidate contamination

## Attack

Can Candidate, Legacy, generated visuals or old summaries silently appear as current truth?

## Findings

1. COC Event Gallery initially displayed every Canon Status.
2. Existing generated Character/World boards still had `CURRENT` in titles despite known pollution.
3. Asset Library was presented inline inside Character/Story Bible and could be read as narrative authority.

## Fixes

- COC human Event Gallery now filters to `CORE_CONFIRMED / CONFIRMED`.
- Existing polluted visual boards renamed `REVERIFY`.
- Character visual candidates moved under `Visual Assets / Reference · Character`.
- Character/Story Bible explicitly state Asset Library is visual authority only.
- No unapproved COC Part 1 Knowledge rows were created.
- `CANON EVIDENCE · Ledger` separates authority tiers:
  - `A0_USER`
  - `A1_CANON`
  - `A2_APPROVED_PLANNING`
  - `A3_CURRENT_CANDIDATE`
  - `A4_LEGACY`
  - `A5_EXTERNAL`

## Re-attack result

`PASS` — contamination is visible instead of flattened.

---

# Full Adversarial Loop 3 / 5 · Notion usability / summary-detail overload

## Attack

Does the new structure simply replace one wall of text with several dense databases?

## Findings

1. One-page Character Bible mixed narrative data and a large visual Asset view.
2. Polluted Part 1/Part 2 visual boards were listed directly under Character Bible.
3. Full detail shown on overview would defeat the requested summary-first interaction.

## Fixes

- Common human UX uses Gallery cards with only:
  - Name
  - Summary
  - Core Function
  - Scope
  - Canon Status
  - Text Approval
- Clicking a Gallery card uses Notion's native database page interaction; Gallery defaults to **Center Peek** according to current official Notion documentation.
- COC gets dedicated pages:
  - `CURRENT · 인물 요약 → 상세`
  - `CURRENT · 세계관·세력 요약 → 상세`
- Visual Asset databases are preserved but moved into separate Visual Reference child pages instead of deleted.
- REVERIFY Character visual pages moved into the Character Visual Reference page.

## Re-attack result

`PASS` for structural UX.

Claim ceiling: exact Android/iOS/desktop geometry and scroll balance remain `UI_GEOMETRY_NOT_VERIFIED` until observed on device.

---

# Full Adversarial Loop 4 / 5 · cross-project reuse / schema overfit

## Attack

Is the model secretly hardcoded to COC chapters, Part 1/Part 2 or fiction-only concepts?

## Findings

- A `Part` field would overfit serial fiction.
- A date-only Event ledger would fail quest/scenes/eras without calendar dates.
- A 5-DB physical model would be excessive for projects with light narrative density.

## Fixes

- Generic `Scope` accepts Part / Arc / Region / System / Era as project-specific text.
- Generic `Sequence` accepts Chapter / Scene ID / Quest Step / Era key.
- Knowledge `Type` supports Character, Faction, Location, World Rule, Relationship, Item, Clue, Setting.
- Five conceptual layers remain, but only three physical databases are required.
- Project relation connects all records to `PROJECT REGISTRY · Master`, allowing filtered per-project views without schema duplication.

## Re-attack result

`PASS` — COC is a pilot, not the schema definition.

---

# Full Adversarial Loop 5 / 5 · visual gate bypass / evidence ceiling

## Attack

Can a user/agent mark a draft text as visually ready and recreate the original image-first pollution?

## Findings

1. Separate Text Approval / Visual Gate selects alone do not prevent contradictory states.
2. First Gate formula incorrectly treated legitimate `REPLACED / REPLACED` lifecycle state as invalid.
3. Relationship direction existed conceptually but was not sufficiently structured in the physical schema.

## Fixes

- Added Knowledge fields:
  - `Relation Source`
  - `Relation Target`
  - `Relation Type`
  - `Source → Target`
  - `Target → Source`
  - `Relation State`
  - `Power / Debt / Dependency`
- Added `Gate Check` formula.
- Added `시각 Gate 위반` audit view filtering `Gate Check = INVALID`.
- Corrected Gate formula lifecycle:
  - `DRAFT / REVIEW_REQUIRED` → Visual must stay `BLOCKED_BY_TEXT`
  - `APPROVED` → Visual may remain blocked or advance
  - `REPLACED` → Visual must be `REPLACED`
- COC Composition Board explicitly requires `Text Approval = APPROVED` before `Visual Gate = READY_FOR_VISUAL`.

## Re-attack result

`PASS` — invalid lifecycle combinations are observable and auditable.

---

# Final review result

```text
Loop 1: PASS
Loop 2: PASS after fixes
Loop 3: PASS after fixes
Loop 4: PASS
Loop 5: PASS after fixes

new material conflict: NONE FOUND
open design blocker: NONE
```

## Implementation Reality Gate

Verified:

- Base Method exists on isolated branch.
- Knowledge README routing exists on isolated branch.
- Contract regression test file exists on isolated branch.
- three Notion master databases were created and schema-read back.
- directional relationship fields and Gate Check exist.
- common summary-first views exist.
- COC filtered views exist.
- Asset Library narrative/visual responsibility is separated in COC pages.
- polluted Character visual pages are marked `REVERIFY`.
- no unapproved COC Part 1 narrative records were promoted.

Not yet claimed:

- Base regression test PASS until exact-head GitHub Actions runs.
- PR/ruleset/review gate PASS until the PR is open and checked.
- COC Part 1 text migration; user approval is still required.
- new COC visuals; Text Approval is still intentionally blocking them.
- mobile Center Peek visual geometry.
