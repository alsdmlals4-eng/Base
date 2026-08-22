# Notion Visual Asset and Flow Workflow

## Authority

`NOTION_DEFAULT_PROJECT_WORKSPACE` is the default human-facing project workspace. It organizes planning, reusable assets, references, benchmarks and derived visual maps. It does not replace repository runtime truth.

Every project-scoped record must satisfy `PROJECT_RELATION_REQUIRED`. A record without a Project relation is unassigned working material, not project canon.

## Standard project page

Each project page keeps large visual separation between three responsibilities:

```text
01 · PROJECT CONTROL
  → project-filtered Work Master views

[large visual gap]

02 · ASSET / LIBRARY / BENCHMARK
  → project-filtered Asset & Knowledge Master views

[large visual gap]

03 · VISUAL MAP
  → semantic flow
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
Notion approved asset / screen / decision
→ explicit implementation task
→ repository asset / scene / resource / config
→ runtime build
→ QA evidence
```

A Notion approval, screenshot or Visual Map is not evidence that Godot or another runtime consumed the asset correctly.

## Deprecated implementation boundary

The following old execution surfaces are not required by this workflow:

- dedicated Figma Bridge
- project Figma route registries
- localhost Expression Studio
- localhost Sprite Animation Studio
- visual-delivery Tool Hub routing

The reusable concepts from those systems are represented above as project identity, provenance, approval, versioning, reuse classification, bounded edits, readback and explicit runtime handoff.
