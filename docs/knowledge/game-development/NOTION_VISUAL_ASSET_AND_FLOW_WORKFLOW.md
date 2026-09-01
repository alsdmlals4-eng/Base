# Notion Visual Asset and Flow Workflow

## V3 compatibility / V4 exception authority

`NOTION_DEFAULT_PROJECT_WORKSPACE_RETIRED`: this document preserves V3 layout and migration guidance only. The V4 default is `REPOSITORY_PRIMARY_CANON` plus `HUMAN_GDD_PDF_DERIVED_VIEW` from `docs/operations/PROJECT_WORKSPACE_AUTHORITY_CONTRACT_V4.json`. `V4_NOTION_EXCEPTION_ONLY` / `NO_NEW_NOTION_WRITE_BY_DEFAULT`: Notion may organize a bounded approved exception or legacy material, but is not the default human-facing workspace and never replaces repository runtime truth.

For an approved V4 exception or migration scope, apply `NOTION_GPT_VISUAL_LAYOUT_CONTRACT.md` together with this workflow. Otherwise use repository-native planning/visual owners and derived PDFs.

For complex gameplay/system logic represented as connected nodes, also apply `docs/operations/project-workspace/NOTION_SYSTEM_BLUEPRINT_CONTRACT.md`. A System Blueprint is a derived human/implementation view, not a visual-scripting runtime or a third source of truth.

Every project-scoped record must satisfy `PROJECT_RELATION_REQUIRED`. A record without a Project relation is unassigned working material, not project canon.

## Legacy/exception project page pattern

Each project page keeps large visual separation between three responsibilities:

```text
01 · PROJECT CONTROL
  → project-filtered Work Master views

[large visual gap]

02 · ASSET / LIBRARY / BENCHMARK
  → project-filtered Asset & Knowledge Master views

[large visual gap]

03 · VISUAL MAP / SYSTEM BLUEPRINT
  → semantic flow
  → core-system node graph when applicable
  → approved project visuals
```

Do not copy one project's filtered view, asset record, screen record or benchmark conclusion into another project as independent canon. Cross-project reuse keeps one source record and records the reuse relationship explicitly.

## Asset & Knowledge Master

The shared data source uses `Record Type`:

- `ASSET`
- `COMPONENT`
- `SCREEN`
- `REFERENCE`
- `BENCHMARK`

Human views should normally expose only the fields useful for visual scanning: Preview, Name, Usage, Style, Approved, Reuse and a small number of project-relevant labels.

The `AI / System` view may retain detailed metadata such as:

- Asset ID
- Project
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

Keep these details available to automation without forcing them into the default human view.

## Provenance and approval

Use source provenance when a source image, external reference, generated candidate or transformed asset influences the result. Record enough evidence to distinguish source, candidate and approved replacement.

For durable or implementation-bound assets, record a stable identity and version. Where useful, record a hash. A new version does not silently overwrite the meaning of an approved prior version; replacement state must be explicit.

Suggested status vocabulary:

```text
WIP
APPROVED
REPLACED
ARCHIVED
```

Approval means the user or project authority accepted the candidate for the stated use. It does not prove runtime integration.

### Approved project visual delivery gate

`APPROVED_VISUAL_NOTION_DELIVERY_REQUIRED`

`APPROVAL_WITHOUT_NOTION_DELIVERY_IS_INCOMPLETE`

When an **actual** image, mockup, diagram, screenshot composition or visualization exists and is approved for project use, the approval is incomplete until the visual is durably represented in the project Notion workspace.

```text
actual visual exists
→ project-scoped approval
→ upload/attach to Project Visual Bible or project-scoped Asset record
→ record Approved + intended use + Project
→ fetch/readback destination
→ verify file/preview and approval state
→ PROJECT_ASSET_APPROVED
```

- A text-only art direction, image prompt/package, `READY_TO_GENERATE` state or reference candidate is **not** an actual approved image.
- Do not generate a missing visual merely to satisfy this gate. Image generation still requires the user's explicit image-generation request when the project/user policy requires it.
- Human-facing Visual Bible/Home shows the visual and human-useful approval context. Prompt, AI Note, Hash, Implementation Path and similar processing metadata stay in `AI / System` surfaces.
- If an approved visual is stored ad hoc outside the project Visual Bible/Asset lifecycle, move or link it into the correct project human surface and create/update the project-scoped Approved asset record without duplicating the visual as competing canon.

## Identity-preserving image edits

When the task requests the same character, UI element or asset with a limited edit, treat unchanged identity attributes as hard constraints. Depending on the asset this can include:

- face geometry
- hairstyle
- costume / equipment
- palette
- silhouette
- camera framing
- lighting grammar
- material language
- UI component family

Change only the requested expression, pose, gaze, effect stage, state, text-free content or other scoped property. If a requested change would materially alter identity, surface that as a new variant rather than silently replacing the master.

### Persistent character additive visual layering

`PERSISTENT_CHARACTER_ADDITIVE_VISUAL_LAYER_GATE`

Use this gate when one **persistent character identity** accumulates several class, faction, tradition, stance or affinity states over time and those states must remain recognizable together.

Separate the visual contract into two owners before generating variants:

```text
persistent character identity
→ face / hair / body proportion / core outfit / core silhouette invariants

additive visual layers
→ equipment accents / aura / energy / companion / shadow / state effects
```

The faction or class brief must not silently replace the persistent identity merely to make each variant easier to distinguish. Instead, define bounded layer ownership, priority, scale and spatial zones so the result still reads as one character.

Before approval, include a **final composite** acceptance check when multiple layers can coexist:

- the face and core silhouette remain readable,
- accumulated layers do not become unrelated costume clutter,
- dominant and supporting states have an explicit hierarchy when simultaneous maxima would conflict,
- important gameplay information is not hidden,
- the result still reads at the **small gameplay scale** actually used by the project.

Key art, lore art and gameplay may use different rendering density. They may still belong to one visual system when **identity / motif / palette / hierarchy** invariants remain stable across surfaces.

Do not apply this gate mechanically when the product promise is a set of genuinely different playable characters or a **true transformation** whose intended fantasy is full body/identity replacement. In those cases, replacement or transformation continuity is the correct contract.

## Candidate, promotion and reuse model

Generated or edited output starts as a candidate. Do not promote a candidate merely because generation succeeded.

Promotion is explicit:

```text
candidate
→ project-scoped review
→ readback-verified preview
→ approval
→ PROJECT_ASSET_APPROVED when promoted as a project asset
→ implementation task when runtime use is required
```

Reusable classifications may include:

- `REUSE_AS_IS`
- `VARIANT_SEED`
- `STRUCTURE_PATTERN`
- `STYLE_DNA`
- `REBUILD_FOR_REUSE`
- `ONE_OFF_KEEP`
- `REJECT_REUSE`

These classifications describe reuse intent; they do not grant rights or approval.

## References and benchmarking

References and benchmarks live in the same Asset & Knowledge Master but use distinct `Record Type` values. External material never becomes project canon merely because it is visually useful.

Benchmark decision vocabulary:

```text
ADOPT / ADAPT / TEST / REFERENCE_ONLY / AVOID / IGNORE
```

Record the reason, source and rights/license boundary when the material may affect production decisions. Transfer general principles instead of copying identifiable expression.

## Visual Map

`VISUAL_MAP_DERIVED` means the human-facing visual flow is a generated or composed representation of current project records.

For game projects it may show:

- screen IDs
- thumbnails
- entry points
- primary / secondary / conditional navigation
- important systems
- approved visual anchors

For narrative projects it may instead show:

- canon
- character
- clue
- scene
- continuity relationships

Keep a semantic graph or structured Screen records behind the rendered map. When the map disagrees with current records, regenerate or correct the map; do not treat the picture as a competing source of truth.

## System Blueprint node view

`NOTION_SYSTEM_BLUEPRINT` extends the Visual Map concept for **complex system logic**. It is required only when the applicability gate in `docs/operations/project-workspace/NOTION_SYSTEM_BLUEPRINT_CONTRACT.md` passes.

A Home-facing graph should emphasize player-readable meaning:

```text
[Player Action / Trigger]
→ [Condition / Choice]
→ [State or Data Change]
→ [Feedback / Reward / Failure]
→ [Next System or State]
```

The detailed Blueprint surface keeps stable `Node ID` values and, when relevant, Trigger/Input, Condition, State/Data Change, Output/Next, Feedback, Owner, Godot Mapping and Validation. The Home may collapse those fields into a readable diagram, but the graph must not stand alone when implementation interpretation would otherwise be ambiguous.

Place the most important System Blueprint near Core Loop / Full Flow / Visual GDD content on the Project Home. Do not force a universal ordering when another project-specific explanation communicates the game faster.

Do not blueprint trivial work. Text-only changes, isolated numeric tuning, cosmetic edits and already-explicit repetitive implementation stay on the lighter existing workflow.

## Image/file delivery and readback

A generated image or uploaded file is not considered delivered merely because an upload call returned success.

```text
generate / edit
→ keep under workspace file-size boundary
→ upload to Notion
→ attach to the intended project record or page
→ fetch/read back the target
→ verify expected file/preview/version
→ report success
```

If readback fails, report the delivery as unverified and do not promote the asset.

## Runtime handoff

Notion manages the project operating workspace; runtime integration remains repository-owned.

```text
Notion approved asset / screen / System Blueprint / decision
→ explicit implementation task
→ repository asset / scene / resource / config / code
→ runtime build
→ QA evidence
```

A Notion approval, screenshot, Visual Map or System Blueprint is not evidence that Godot or another runtime consumed or implemented it correctly.

## Deprecated implementation boundary

The following old execution surfaces are not required by this workflow:

- dedicated Figma Bridge
- project Figma route registries
- localhost Expression Studio
- localhost Sprite Animation Studio
- visual-delivery Tool Hub routing

The reusable concepts from those systems are represented above as project identity, provenance, approval, versioning, reuse classification, bounded edits, readback and explicit runtime handoff.
