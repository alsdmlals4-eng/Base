# Visual Collaboration Tool Policy

## Current authority

The default project operating surface is `NOTION_DEFAULT_PROJECT_WORKSPACE`.

Authority is split by domain instead of forcing one tool to own every representation.

```text
Notion project workspace
→ NOTION_HUMAN_FACING_CANON
→ project overview / visual direction / visual asset catalog
→ budget tables / tier tables / human-editable Flow Map / Storyboard
→ the primary surface a person reads, compares, and edits

repository-native Markdown / JSON / game data / code / scenes / resources / tests
→ REPOSITORY_STRUCTURED_CANON
→ REPOSITORY_RUNTIME_TRUTH for implemented/runtime facts

legacy Google Sheets
→ RETIRED_MIGRATION_ONLY
→ one-time unique-material migration, then active reference removal
```

`DOMAIN_SPLIT_CANON` means neither side is a disposable copy. Notion has priority for the human-facing visual/table/overview domains above; the repository has priority for structured specifications, data and implementation/runtime domains. When a Notion edit implies a Markdown/data/code/scene/resource/test change, synchronize that structured change to the repository before implementation or runtime claims (`SYNC_BEFORE_IMPLEMENTATION`).

No visual collaboration tool becomes a second runtime or implementation canon.

## Supported collaboration contexts

The same project-boundary rules apply whether the immediate work context is `GDD`, `EXTERNAL_COLLABORATION`, or `BOTH`. These labels describe where a visual decision is being consumed; they do not create another authority.

## Project boundary

`PROJECT_RELATION_REQUIRED` is mandatory for project-scoped Work, Asset, Component, Screen, Reference and Benchmark records.

One workspace may contain many projects, but a normal project page exposes only Project-filtered views. Unfiltered Master views belong under the system-master area and are not the default human work surface.

Cross-project reuse keeps one source record and records reuse intent; do not clone records into multiple projects as separate current authorities.

## Standard project surface

```text
PROJECT HOME
→ current direction / core fun / core loop / blockers / quick links

01 · PROJECT CONTROL
→ WORK_MASTER filtered to the selected Project

02 · VISUAL BIBLE
→ approved visual direction / human-readable north star

03 · FLOW MAP / STORYBOARD
→ human-editable visual relationship surface
→ VISUAL_MAP_DERIVED from structured records when appropriate

04 · ASSET LIBRARY
→ ASSET_KNOWLEDGE_MASTER filtered to the selected Project

05 · REFERENCE / BENCHMARK
→ evidence and adoption decisions

06 · PRODUCTION / HANDOFF
→ approved planning → repository implementation → runtime QA

07+ · PROJECT-SPECIFIC CONFIRMED TABLES
→ budget / tier / roster / economy / progression / other human-learning tables when useful
```

Project-specific confirmed tables are encouraged when they materially improve human understanding. They summarize approved facts with source Decision IDs/paths and must visibly separate confirmed, provisional, deferred and rejected values.

## Intermediate visual checkpoint

`Intermediate visual checkpoint` is a project-scoped decision gate, not a tool/page-specific location.

```text
NOTION_VISUAL_CHECKPOINT_BEFORE_POC
UX_UI_REPRESENTATIVE_STATE_REQUIRED
APPROVED_VISUALS_FEED_POC
```

When visual composition, UI hierarchy, readability, mood, feedback or identity can materially change the PoC/demo judgment, representative visual states are planned and reviewed in GPT, attached to the exact Project in Notion, read back, and approved **before** the PoC uses them.

The checkpoint does not require every production screen. It requires enough representative states to judge the intended core experience: entry/first impression, primary play, key decision, major feedback/reward/fail/transition, and any HUD/popup/navigation state that is necessary to understand the system. A technical-only spike may skip the gate when visuals cannot affect the result, with the reason recorded.

Checkpoint states:

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

## Confirmed planning tables

Budget, tier, roster, economy and progression tables that are primarily for human comparison belong in Notion as `NOTION_HUMAN_FACING_CANON`.

Each confirmed table must preserve enough traceability to cross-check the repository:

```text
Project
→ table purpose
→ Decision ID or canonical repository path
→ confirmed / provisional / deferred / rejected state
→ repository main SHA or equivalent freshness locator when practical
→ last Notion sync date
```

Do not turn a human table into an undocumented second data model. Machine-consumed JSON/game data stays in the repository. Conversely, do not force the user to inspect raw Markdown/JSON when a visual table is the clearer primary human representation.

## Image and visual candidate lifecycle

```text
need / brief
→ generate or edit candidate
→ GPT bounded visual + UX review
→ attach candidate to the correct Project record
→ readback
→ explicit approval or rejection
→ version / replacement relationship
→ repository implementation task when needed
→ branch / PR / exact-head checks for implementation-bound assets
→ runtime evidence separately
```

For identity-preserving edits, unchanged identity attributes are hard constraints. Change only the requested expression, pose, gaze, effect stage, UI state or other scoped property.

A successful generation is not approval. A successful upload is not delivery until readback confirms the expected file/preview/version at the intended Project target.

If an approved visual is a PoC input, use the approved image itself or a provenance-preserving implementation derivative instead of silently substituting an unrelated placeholder.

## Reuse promotion

Reusable visual harvest and reuse promotion happen in `ASSET_KNOWLEDGE_MASTER`, not in a tool-specific profile. A source candidate may be classified as `REUSE_AS_IS`, `VARIANT_SEED`, `STRUCTURE_PATTERN`, `STYLE_DNA`, `REBUILD_FOR_REUSE`, `ONE_OFF_KEEP`, or `REJECT_REUSE` before any project approval. Reuse classification does not itself grant approval or rights.

## Visual Map

`VISUAL_MAP_DERIVED` means the map may be generated from current Screen/relationship records and approved previews; it does **not** mean the human must treat the map as disposable. Once approved in Notion, that Notion view is the primary human-facing representation for visual planning and review.

Game projects may visualize screen IDs, thumbnails, entry points, primary/secondary/conditional routes and key systems. Narrative projects may visualize canon, character, faction, clue, scene and continuity relationships.

If a visual edit changes structured semantics, reconcile the semantic records/repository before implementation. If repository runtime facts change, refresh the Notion map so the person-facing view does not drift.

## Human and AI views

The same records support two display layers:

- `human` view: sparse visual information for scanning, learning, comparison and direct planning edits.
- `AI / System` view: provenance, IDs, version, status, hash, prompt, rights and implementation metadata.

Hiding system metadata is a presentation decision, not deletion. Automation may still read it when needed.

## Repository handoff and runtime evidence

Notion approval means the project accepted the human-facing planning, table, visual direction or asset candidate for its stated use. It does not prove runtime implementation.

```text
Notion approved human-facing record
→ synchronize any required Markdown / JSON / game data contract
→ repository implementation task
→ optional Codex sub-executor when actual repository/engine mutation is needed
→ code / asset / scene / resource / config
→ build or runtime
→ REPOSITORY_NATIVE_QA_EVIDENCE
→ GPT final planning/UX review
→ Notion readback/status refresh
```

`REPOSITORY_NATIVE_QA_EVIDENCE` uses exact commit/PR head, `PASS / FAIL / BLOCKED / NOT_RUN`, screenshot/video/log, GitHub Actions artifacts or PR evidence packets instead of requiring a standalone localhost QA application. Android not yet connected remains a separate `DEFERRED_NOT_CONNECTED` state rather than being inferred from PC results.

## Legacy and deprecated visual execution paths

Dedicated Figma routing, a Figma Bridge, localhost Expression/Sprite Studios, visual-delivery Tool Hub routing, standalone localhost/browser QA Evidence Studio, independent HTML project-management dashboards, and Google Sheets as an active GDD surface are not active authorities or required project surfaces.

Their reusable ideas—project identity, provenance, bounded edits, approval, versioning, reuse classification, readback, explicit handoff, fail-closed evidence states—are absorbed into `docs/knowledge/game-development/NOTION_VISUAL_ASSET_AND_FLOW_WORKFLOW.md` and `docs/DEPRECATED_PROJECT_SURFACE_RETIREMENT_POLICY.md`.

Do not restore a deprecated execution surface merely because historical docs, Git history or archived evidence mention it. Reintroduction requires a new Existing Solution First comparison, lifecycle-cost justification and user approval.

## Cost boundary

The default path must satisfy `ZERO_INCREMENTAL_COST_REQUIRED`.

```text
CURRENT_PAID_PLANS: GPT_PRO
PAID_PLAN_COUNT: 1
NOTION_PAID_ON_REQUEST_ONLY
```

Notion is used within its free/currently available feature and file-size limits by default. If a paid Notion feature would materially remove a repeated bottleneck, document `COST_BENEFIT_EVIDENCE_BEFORE_NOTION_UPGRADE` and ask for explicit user approval. Paid Notion AI, Business/Enterprise-only features, separately metered storage/automation, or external provider calls are not assumed before that approval.

## Adversarial rejection criteria

Reject or revise a change if it:

- exposes unfiltered cross-project records on a normal project page;
- treats Notion human-facing tables/visuals as runtime proof;
- creates a competing structured data model in a visual table instead of synchronizing machine data to the repository;
- duplicates one approved asset into multiple independent project authorities;
- hides provenance by deleting metadata instead of hiding it from the human view;
- reports upload success without readback;
- promotes a Reference/Benchmark to approved asset without a project decision;
- leaves an approved Notion visual/table materially inconsistent with the repository domain it is meant to summarize;
- runs a visually material PoC with unrelated placeholder art after the project approved a specific visual checkpoint;
- reintroduces a deprecated local/HTML/Sheet surface without evidence that it lowers total lifecycle cost.
