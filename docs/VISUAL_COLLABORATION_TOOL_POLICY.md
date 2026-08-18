# Visual Collaboration Tool Policy

## Current authority

The default project operating surface is `NOTION_DEFAULT_PROJECT_WORKSPACE`.

```text
Notion project workspace
→ project planning, Asset/Knowledge catalog, references, benchmarks, approved visual previews and derived Visual Map

repository-native code/data/scenes/resources/tests
→ REPOSITORY_RUNTIME_TRUTH

legacy Google Sheets
→ COMPATIBILITY_ONLY when an existing migration source still contains unique material
```

No visual collaboration tool becomes a second runtime or implementation canon.

## Supported collaboration contexts

The same project-boundary rules apply whether the immediate work context is `GDD`, `EXTERNAL_COLLABORATION`, or `BOTH`. These labels describe where a visual decision is being consumed; they do not create another authority.

## Project boundary

`PROJECT_RELATION_REQUIRED` is mandatory for project-scoped Work, Asset, Component, Screen, Reference and Benchmark records.

One workspace may contain many projects, but a normal project page exposes only Project-filtered views. Unfiltered Master views belong under the system-master area and are not the default human work surface.

Cross-project reuse keeps one source record and records reuse intent; do not clone records into multiple projects as separate current authorities.

## Standard project surface

```text
01 · PROJECT CONTROL
→ WORK_MASTER filtered to the selected Project

[large visual separation]

02 · ASSET / LIBRARY / BENCHMARK
→ ASSET_KNOWLEDGE_MASTER filtered to the selected Project

[large visual separation]

03 · VISUAL MAP
→ VISUAL_MAP_DERIVED
→ approved project visuals
```

The large separation is intentional: it reduces accidental mixing between planning, reusable knowledge/assets and visual-flow interpretation.

## Intermediate visual checkpoint

`Intermediate visual checkpoint` is a project-scoped decision gate, not a tool/page-specific location.

- `MISSING_CANON`: there is not enough approved visual direction to judge continuity safely.
- `DRAFT_VISUAL`: the artifact is an exploratory checkpoint and is not an approved project asset.
- `PROJECT_ASSET_APPROVED`: the project authority accepted the asset for a stated role.
- `APPLIED_AND_RUNTIME_VERIFIED`: repository/runtime integration has separate evidence.

A checkpoint may use a screenshot, generated image, component preview, semantic flow or Visual Map. It must retain the correct Project relation and must not imply runtime success merely because the draft looks correct.

## Asset and knowledge model

The shared Asset/Knowledge Master uses `Record Type` values such as:

```text
ASSET
COMPONENT
SCREEN
REFERENCE
BENCHMARK
```

Human-facing Gallery/Table views should emphasize Preview, Name, Usage, Style, Approved and Reuse.

The `AI / System` view may retain Asset ID, Project, version, Status, Category, Prompt, AI Note, source provenance, Rights / License, Hash, Implementation Path and Decision without forcing those fields into the normal human view.

Benchmark decisions use:

```text
ADOPT / ADAPT / TEST / REFERENCE_ONLY / AVOID / IGNORE
```

External references are evidence and inspiration, not project canon. Record why a source matters and what is transferable; do not copy identifiable expression merely because the source is cataloged.

## Image and visual candidate lifecycle

```text
need / brief
→ generate or edit candidate
→ bounded visual review
→ attach candidate to the correct Project record
→ readback
→ explicit approval or rejection
→ version / replacement relationship
→ implementation task when needed
→ runtime evidence separately
```

For identity-preserving edits, unchanged identity attributes are hard constraints. Change only the requested expression, pose, gaze, effect stage, UI state or other scoped property.

A successful generation is not approval. A successful upload is not delivery until readback confirms the expected file/preview/version at the intended Project target.

## Reuse promotion

Reusable visual harvest and reuse promotion happen in `ASSET_KNOWLEDGE_MASTER`, not in a tool-specific profile. A source candidate may be classified as `REUSE_AS_IS`, `VARIANT_SEED`, `STRUCTURE_PATTERN`, `STYLE_DNA`, `REBUILD_FOR_REUSE`, `ONE_OFF_KEEP`, or `REJECT_REUSE` before any project approval. Reuse classification does not itself grant approval or rights.

## Visual Map

`VISUAL_MAP_DERIVED` is a human-facing representation derived from current Screen/relationship records and approved previews.

Game projects may visualize screen IDs, thumbnails, entry points, primary/secondary/conditional routes and key systems. Narrative projects may visualize canon, character, clue, scene and continuity relationships.

The semantic graph and project records own the meaning. If the rendered map disagrees with current records, regenerate or correct the map rather than treating the picture as a competing canon.

## Human and AI views

The same records support two display layers:

- `human` view: sparse visual information for scanning and decision making.
- `AI / System` view: provenance, IDs, version, status, hash, prompt, rights and implementation metadata.

Hiding system metadata is a presentation decision, not deletion. Automation may still read it when needed.

## Repository handoff and runtime evidence

Notion approval means the project accepted the planning or asset candidate for its stated use. It does not prove runtime implementation.

```text
Notion approved record
→ repository implementation task
→ code / asset / scene / resource / config
→ build or runtime
→ QA evidence
```

QA Evidence Studio or equivalent runtime evidence remains independent of the project planning workspace.

## Legacy and deprecated visual execution paths

Dedicated Figma routing, a Figma Bridge, localhost Expression/Sprite Studios and visual-delivery Tool Hub routing are not active authorities or required project surfaces. Their reusable ideas—project identity, provenance, bounded edits, approval, versioning, reuse classification, readback and explicit handoff—are absorbed into `docs/knowledge/game-development/NOTION_VISUAL_ASSET_AND_FLOW_WORKFLOW.md`.

Do not restore a deprecated execution surface merely because historical docs, Git history or archived evidence mention it. Reintroduction requires a new Existing Solution First comparison, lifecycle-cost justification and user approval.

## Cost boundary

The default path must satisfy `ZERO_INCREMENTAL_COST_REQUIRED`. Notion Free may be used within its current feature/file-size limits; paid Notion AI, separately metered storage, paid automation, or external provider calls are not part of the default workflow.

## Adversarial rejection criteria

Reject or revise a change if it:

- exposes unfiltered cross-project records on a normal project page;
- creates a second asset or runtime canon in the Visual Map;
- duplicates one approved asset into multiple independent project authorities;
- hides provenance by deleting metadata instead of hiding it from the human view;
- reports upload success without readback;
- promotes a Reference/Benchmark to approved asset without a project decision;
- treats planning screenshots as runtime proof;
- reintroduces a deprecated visual tool without evidence that it lowers total lifecycle cost.
