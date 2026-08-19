# Notion Visual Asset and Flow Workflow

## Authority

`NOTION_DEFAULT_PROJECT_WORKSPACE` is the default human-facing project workspace. It organizes planning, reusable assets, references, benchmarks and derived visual maps. It does not replace repository runtime truth.

Every project-scoped record must satisfy `PROJECT_RELATION_REQUIRED`. A record without a Project relation is unassigned working material, not project canon.

## GPT-first visual planning

```text
NOTION_VISUAL_CHECKPOINT_BEFORE_POC
UX_UI_REPRESENTATIVE_STATE_REQUIRED
APPROVED_VISUALS_FEED_POC
```

When image, UI, UX or screen composition can materially change the PoC/demo judgment, GPT plans and reviews representative visual states before implementation. The visual checkpoint is part of planning/review, not a post-PoC decoration pass.

The minimum representative set is selected by the current core experience, but normally includes enough of the following to judge the intended experience:

- entry / first-impression state;
- primary play state;
- key decision or interaction state;
- major feedback, reward, fail or transition state;
- HUD, popup or navigation state that is necessary to understand the system.

Do not force complete production UI before PoC. A technical-only spike may skip this gate when visuals cannot affect the result, but record the reason.

Approved visual candidates are PoC inputs. If a candidate was approved because its composition, hierarchy, readability, mood or identity matters, the PoC should use that asset directly or an implementation derivative with the same provenance instead of silently substituting an unrelated placeholder.

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
→ GPT visual + UX review
→ project-scoped review
→ readback-verified preview
→ approval
→ PROJECT_ASSET_APPROVED when promoted as a project asset
→ implementation task when runtime use is required
→ repository PR/merge when implementation-bound
→ runtime consumption evidence
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
→ attach to the intended Project record or page
→ fetch/read back the target
→ verify expected file/preview/version
→ report candidate delivery
```

If readback fails, report the delivery as unverified and do not promote the asset.

If the image is approved as a PoC/runtime input, continue:

```text
approved Notion image
→ stable provenance / version
→ repository implementation asset or derivative
→ branch / PR / exact-head checks
→ merge
→ runtime scene/resource consumption evidence
→ Notion status/readback refresh
```

## Runtime handoff

Notion manages the project operating workspace; runtime integration remains repository-owned.

```text
Notion approved asset / screen / decision
→ explicit implementation task
→ optional Codex sub-executor when actual repository/engine mutation is needed
→ repository asset / scene / resource / config
→ runtime build
→ repository-native QA evidence
→ GPT final planning/UX review
```

A Notion approval, screenshot or Visual Map is not evidence that Godot or another runtime consumed the asset correctly.

## Deprecated implementation boundary

The following old execution surfaces are not required by this workflow:

- dedicated Figma Bridge
- project Figma route registries
- localhost Expression Studio
- localhost Sprite Animation Studio
- visual-delivery Tool Hub routing
- standalone localhost/browser QA Evidence Studio as the default project review surface
- independent HTML project-management dashboards

The reusable concepts from those systems are represented above as project identity, provenance, approval, versioning, reuse classification, bounded edits, readback, explicit runtime handoff and repository-native evidence.

Retired surface cleanup follows `docs/DEPRECATED_PROJECT_SURFACE_RETIREMENT_POLICY.md`; do not restore a retired local/HTML surface merely because historical files or Git history mention it.
