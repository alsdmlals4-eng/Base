# Notion System Blueprint Design

## Decision

Adopt a `Notion System Blueprint` as a derived human/implementation view between approved design and repository implementation. It is not a visual-scripting runtime and does not become an independent source of truth.

## Authority

- Project Notion Home remains the human-facing design surface.
- Detailed Blueprint implementation mapping lives in the appropriate project detail/AI-System surface and references repository owners.
- GitHub repository remains canon for structured data, code, scenes, resources, tests, and runtime truth.
- If Blueprint and repository runtime truth diverge, the approved design decision is reconciled first and the derived Blueprint is corrected; the Blueprint cannot silently override runtime canon.

## Blueprint node contract

Every material node uses a stable ID and, when applicable, records:

- `Node ID`
- `Type`: Trigger / Condition / Action / State / Data / Feedback / Output
- `Player Meaning / Intent`
- `Trigger / Input`
- `Condition`
- `State or Data Change`
- `Output / Next Node`
- `Feedback`
- `Owner`
- `Godot Mapping`
- `Validation`

Human-facing Home views may collapse this to the node label + relationship graph. Detailed fields stay in the detailed Blueprint surface.

## Applicability gate

Use System Blueprint when the work contains multi-state or multi-system logic, branching conditions, reusable system interaction, or complex player-facing flow. Typical candidates are Core Loop, combat, progression, economy, AI, stage/state transitions, quest logic, and complex UI/UX flow.

Do not require Blueprint for copy edits, isolated numeric tuning, cosmetic-only adjustments, one-off asset replacement, or repetitive implementation whose contract is already explicit and unchanged.

## Notion presentation

Project Home should expose `핵심 System Blueprint` near Core Loop / Flow / Visual content so a person can understand what the player does, what changes, and why. Detailed node tables, edge cases, Godot mapping, and validation criteria remain below the Home summary or in a linked detail page.

Do not place raw PR/SHA/CI/receipt metadata in the human Home. That evidence remains in AI/System/Handoff or repository surfaces.

## Implementation mapping

The Blueprint maps intent to Godot concepts without creating a visual scripting engine:

- data ownership → Resource / structured project data owner
- state → state machine or explicit state owner
- event → Signal / callback / explicit message path
- behavior → Node / GDScript component
- scene composition → Scene / Node hierarchy
- validation → automated test, deterministic scenario, or explicit manual play evidence

Mappings are descriptive contracts, not permission to invent missing project decisions.

## Lifecycle

1. Approved design establishes or changes a system flow.
2. The human Blueprint is updated in the same approval unit.
3. Detailed mapping identifies repository owners and verification criteria.
4. Codex/implementation changes repository canon.
5. Runtime/play verification compares behavior with the approved Blueprint intent.
6. If behavior or design changes, both the correct canon owner and the derived Blueprint are reconciled.

## Risks and controls

- Third-canon drift → Blueprint is explicitly derived and owner-linked.
- Graph bloat → blueprint only material branching/system nodes; split by bounded system.
- AI over-interpretation → stable node IDs + text fields; diagrams never stand alone as implementation truth.
- Home clutter → summary graph at Home, detail tables below/linked.
- Process overhead → applicability gate exempts trivial work.

## Rollback

Remove the Blueprint-specific Home/detail guidance and any derived node views. Repository canon, approved design records, and runtime data/code remain unchanged, so rollback does not affect game behavior.
