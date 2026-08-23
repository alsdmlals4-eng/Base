# Narrative & World Knowledge Model Implementation Plan

> Execution mode: `superpowers:executing-plans` · current-task isolated remote branch `docs/narrative-world-knowledge-20260823`.

**Goal:** Add a reusable narrative/world research and canon-organization layer that separates knowledge, events and evidence, supports summary-first → Center Peek detail in Notion, and blocks visual production before text approval.

**Architecture:** Base owns one common Method and one knowledge-routing entry. Notion implements five conceptual layers using three physical databases. COC-Fiction is the bounded pilot; infrastructure is connected now, but unapproved Part 1 prose is intentionally not migrated.

**Spec:** `docs/superpowers/specs/2026-08-23-narrative-world-knowledge-model-design.md`

## Review amendment · 2026-08-23

Initial plan proposed editing `skills/developing-and-revising-serial-fiction/SKILL.md`. Adversarial review rejected that coupling:

- the new model is shared by games, novels, TRPG adaptations and worldbuilding projects, not only serial fiction;
- `developing-and-revising-serial-fiction` already owns scene/voice/continuity execution;
- assigning the common Knowledge Model to that Skill would create duplicate ownership and a serial-fiction-only routing dependency.

**Final decision:** route through `docs/knowledge/README.md` and keep the serial-fiction Skill unchanged. The Method may be selectively read by that Skill through normal Base knowledge routing when the task is canon/character/world extraction.

## Constraints

- PR #620 stays read-only and is not modified, merged or copied from.
- No direct `main` write.
- No new broad Skill or dashboard.
- Asset Library remains visual-asset authority, not narrative-canon authority.
- Candidate/legacy data cannot silently become confirmed canon.
- No COC character/world image generation before approved text.
- Center Peek capability is used for detail navigation; exact mobile geometry remains unclaimed until observed.

## Task 1 · Base Method + routing

- [x] Create `docs/knowledge/methods/NARRATIVE_WORLD_KNOWLEDGE_MODEL.md`.
- [x] Define `AUTHORITY_MAP → ENTITY_EXTRACTION → EVENT_EXTRACTION → RELATION_RULE_EXTRACTION → EVIDENCE_LINK → CONTRADICTION_AUDIT → HUMAN_PRIMER → USER_APPROVAL → VISUAL_GATE`.
- [x] Define the three physical Notion stores and status/gate enums.
- [x] Route `서사·세계관 정본 조사·구조화` from `docs/knowledge/README.md`.
- [x] Keep existing narrative/relationship/art/source-radar owners intact.

## Task 2 · Contract regression test

- [x] Create `tests/test_narrative_world_knowledge_model.py`.
- [x] Guard required workflow tokens, DB names, status values, Visual Gate and Center Peek wording.
- [x] Guard the Knowledge README routing entry.
- [ ] Execute focused test on exact PR head through repository CI. Local clone/runtime is unavailable because the session container cannot resolve GitHub DNS.

## Task 3 · Common Notion storage

- [x] Create `NARRATIVE KNOWLEDGE · Master` under `90 · SYSTEM MASTERS`.
- [x] Create `NARRATIVE EVENT · Ledger`.
- [x] Create `CANON EVIDENCE · Ledger`.
- [x] Link all three to `PROJECT REGISTRY · Master`.
- [x] Link Event Participants to Knowledge Master.
- [x] Link Evidence to Knowledge and Event targets.
- [x] Add directional Relationship fields: `Relation Source`, `Relation Target`, `Relation Type`, `Source → Target`, `Target → Source`, `Relation State`, `Power / Debt / Dependency`.
- [x] Add `Gate Check` formula to flag invalid Text Approval / Visual Gate combinations.
- [x] Read back schemas after creation.

## Task 4 · Summary-first human UX

- [x] Create P09 page `Narrative & World Knowledge Model · 요약 → 상세`.
- [x] Explain `요약 Gallery → 카드 클릭 → Center Peek 상세 → 필요 섹션 펼치기`.
- [x] Create common Gallery views for Character, Faction, World/Rule and Location.
- [x] Create Event Gallery.
- [x] Create `정본 충돌 / 미검증` Evidence view.
- [x] Create `시각 Gate 위반` audit view.
- [x] Keep overview cards limited to Name / Summary / Core Function / Scope / Canon Status / Text Approval.

## Task 5 · COC bounded pilot

- [x] Create `CURRENT · 인물 요약 → 상세` under Character Bible.
- [x] Filter COC Character Gallery to `Project=Coc소설`, `Type=Character`, `Text Approval=APPROVED`.
- [x] Create `CURRENT · 세계관·세력 요약 → 상세` under Story Bible.
- [x] Add approved Faction / World Rule+Setting / Location / Relationship galleries.
- [x] Add confirmed-only COC Event Gallery.
- [x] Move Character Asset Library view to `Visual Assets / Reference · Character` instead of deleting it.
- [x] Move World Asset Library view to `Visual Assets / Reference · World`.
- [x] Mark polluted character visual pages `REVERIFY` and move them under Character Visual Reference.
- [x] Mark polluted world/faction boards `REVERIFY`.
- [x] Update COC Composition Board: `Text Approval=APPROVED` is required before `Visual Gate=READY_FOR_VISUAL`.
- [x] Do **not** create COC character/world records from unapproved Part 1 prose.

## Task 6 · Adversarial review + verification

Full review targets:

1. duplicate responsibility / owner conflict
2. canon/candidate contamination
3. Notion usability / summary-detail overload
4. cross-project reuse / schema overfit
5. visual gate bypass / evidence ceiling

Verified findings already fixed during loops include:

- serial-fiction Skill over-coupling rejected;
- COC Event view restricted to confirmed statuses;
- relationship direction made structured;
- Visual Gate invalid state formula/audit added;
- Asset Library inline clutter moved to separate visual pages;
- polluted visual pages relabeled `REVERIFY`.

- [ ] Record five full-loop review result on the branch.
- [ ] Open current-task PR.
- [ ] Run exact-head GitHub Actions/checks.
- [ ] Confirm unresolved thread/review/ruleset gates.

## Task 7 · Completion / merge

- [ ] Merge only if current-task continuation authorization and repository gates allow it.
- [ ] No admin bypass, force push or direct main push.
- [ ] Post-merge GitHub readback of Method/routing/test.
- [ ] Post-merge Notion readback of P09 / COC summary / visual separation.

## Implementation Reality Gate

Claims must remain separate:

- Method exists ≠ every project migrated.
- DB exists ≠ project knowledge extracted.
- Entity/Event extracted ≠ canon approved.
- Text approved ≠ visual approved.
- Visual approved ≠ runtime/reader validation.
- Center Peek capability ≠ mobile layout verified.
- COC infrastructure is ready, but COC Part 1 character/world content migration remains blocked until the user approves the text package.
