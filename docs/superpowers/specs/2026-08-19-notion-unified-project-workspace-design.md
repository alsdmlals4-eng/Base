# Unified Notion Project Workspace Design

## Status

`APPROVED_FOR_IMPLEMENTATION` — user approved the single-workspace Notion direction after a live pilot proved image upload, replacement, readback, project-page composition, Mermaid flow maps, and human/AI view separation.

## Goal

Replace the deprecated Figma + local visual-tool operating surface with one Notion workspace that keeps projects strongly separated while preserving reusable planning, asset, provenance, review, and visual-flow principles.

## Chosen architecture

One Notion workspace contains a single project registry and two shared master data sources. Each project is a separate registry page and receives only project-filtered views.

```text
00 · PROJECT HUB
  → PROJECT REGISTRY · Master
      → Project A page
      → Project B page
      → ...

90 · SYSTEM MASTERS
  → Work Master
  → Asset & Knowledge Master
  → Project Registry

project page
  01 · PROJECT CONTROL
    → Work Master filtered by Project relation

  [large visual gap]

  02 · ASSET / LIBRARY / BENCHMARK
    → Asset & Knowledge Master filtered by Project relation

  [large visual gap]

  03 · VISUAL MAP
    → semantic Mermaid flow
    → approved visual gallery filtered by Project relation
```

`Project` relation is mandatory. A record without a project relation is not project canon.

## Project boundary

- One workspace is shared, but each project page is a hard user-facing boundary.
- Work, asset, screen, reference, and benchmark records are never copied between project pages as independent canon.
- Cross-project reuse keeps one source record and records reuse intent explicitly.
- Narrative projects may replace UI-flow semantics with canon/character/clue/scene/continuity relationships.

## Work Master

Minimum visible fields:

- Work
- Status
- Area
- Priority
- Start / End
- Completion Criteria
- Validation / Evidence
- Assignee

System fields may include stable task ID and project relation. Views should expose Board, Table, and Timeline without duplicating records.

## Asset & Knowledge Master

One data source owns these record types:

- `ASSET`
- `COMPONENT`
- `SCREEN`
- `REFERENCE`
- `BENCHMARK`

Human-facing views emphasize preview, name, usage, style, approval, and reuse. AI/system views may retain:

- Asset ID
- Version
- Status
- Category
- Prompt
- AI Note
- Source
- Rights / License
- Hash
- Implementation Path
- Decision

Benchmark decisions use `ADOPT / ADAPT / TEST / REFERENCE_ONLY / AVOID / IGNORE`.

## Visual Map

The Visual Map is a derived human-facing representation, not a second asset authority.

- Human surface: generated or captured visual flow board plus approved visual gallery.
- Machine surface: semantic screen/relationship records and Mermaid graph.
- If the rendered board drifts from current Screen records, regenerate the board instead of editing the image as canon.

## Absorbed principles from deprecated visual tools

Keep the principles, not their Figma/local implementations:

- exact project identity / project boundary
- source provenance and hash where useful
- identity-preserving character edits
- explicit candidate selection and approval
- version and replacement relationships
- reusable-asset classification
- screen IDs and flow IDs
- image output readback before claiming success
- benchmark decision and source-rights fields
- separate human-visible and AI/system metadata views
- runtime validation remains separate from planning visuals

Expression/pose/effect generation remains a workflow capability of the responsible image-generation/review skill; it no longer requires a dedicated localhost Studio.

## Authority

```text
latest user decision
→ project Notion workspace for project planning / asset catalog / visual map
→ repository-native code, config, scenes, resources, tracked implementation assets and tests for runtime truth
→ Base shared rules, templates, skills and benchmark knowledge
→ external references
```

Notion is the project operating workspace; it does not prove Godot runtime behavior. Runtime evidence remains code/test/build/QA evidence.

## Deprecated implementation removal

Remove active implementations and canonical routes whose purpose was the abandoned visual path:

- Figma Bridge
- Figma project/target/tool-route registries and Figma-only schemas
- Expression Studio
- Sprite Animation Studio
- Tool Hub visual-delivery / Studio-launch path
- Figma-specific project-operation templates
- Figma-specific active CI and contract tests
- Figma as an active periodic discovery dependency

Keep QA Evidence Studio because developer-PC QA is independent of Figma/Notion and remains useful after visual assets are placed in the real build.

## Cost boundary

Default project workflow must add no separately metered cost. Active paid-plan assumption is `GPT_PRO` only. Notion Free is used within its file-size and feature limits; no paid Notion AI or paid API provider is required for the default workflow.

## Five full adversarial review loops

### Loop 1 — project mixing

Attack: one workspace could blend records across games.

Improvement: mandatory Project relation + project-filtered linked views + project-boundary banner. No unfiltered master views on normal project pages.

### Loop 2 — duplicate canon

Attack: Visual Map, Asset Gallery and repository files could each look canonical.

Improvement: Asset/Screen records are the planning/catalog source; Visual Map is derived; implementation files/tests remain runtime truth.

### Loop 3 — human clutter

Attack: hashes, prompts, IDs and provenance make the workspace unreadable.

Improvement: human Gallery/Table exposes only useful display fields; AI/System view retains full metadata.

### Loop 4 — losing useful local-tool behavior

Attack: deleting the tools could remove good provenance, approval and reuse practices.

Improvement: preserve those practices as neutral Notion/repository contracts and image-generation review rules before deleting the tool-specific execution layers.

### Loop 5 — over-deleting local validation capability

Attack: treating every localhost utility as deprecated could remove real QA value.

Improvement: removal is goal-based. Figma/visual-delivery Studios and Hub are removed; QA Evidence Studio and unrelated Godot/CI/validation tooling remain.

No blocking finding remains after loop 5.

## Re-review triggers

Reconsider this architecture when any of the following becomes material:

- Project relation filtering repeatedly leaks or confuses records.
- Notion Free limits materially block normal project assets.
- Visual Map cannot express a required interaction or collaboration need.
- Cross-project reusable assets become large enough to justify a separate shared-asset workspace.
- Notion automation requires separately metered features.
- A new tool demonstrably reduces lifecycle cost without reintroducing duplicate authority.
