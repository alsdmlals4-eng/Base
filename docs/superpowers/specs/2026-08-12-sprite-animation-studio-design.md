# Sprite Animation Studio Design

**Status:** Approved design for implementation planning
**Date:** 2026-08-12
**Scope owner:** Base shared-tool package
**Approval evidence:** User approved Base-hosted common tool, local browser UI, and the Figma reference-to-derived-sprite-sheet flow in this conversation.

## 1. Direction anchor

Build a local-first production tool that turns an approved character or effect reference into curated, game-ready 2D animation assets while preserving visual identity across poses. Figma presents the visual lineage; project repositories own source art and exported runtime assets; Base owns reusable tool code, contracts, templates, and tests.

## 2. User outcome

A solo game developer can:
1. select an approved reference image;
2. lock a character idle anchor or effect silhouette anchor;
3. request a named action such as `attack`, `jump`, `hit`, or `cast`;
4. generate one candidate row for that action;
5. discard, reorder, align, and preview frames;
6. export accepted frames as PNGs, a GIF preview, an atlas, and a machine-readable animation manifest.

The tool must make visual drift visible and correctable. It must not promise that one image input produces a fully approved animation without human review.

## 3. Existing-solution disposition

| Candidate | Evidence | Decision |
|---|---|---|
| `aldegad/sprite-gen` | Component-row generation, anchor ownership, chroma cleanup, frame extraction, non-destructive curation, atlas and manifest export; Apache-2.0. | **REUSE** as a pinned execution engine. Do not fork or vendor in MVP. |
| Whole-sheet, one-shot image generation | Cannot reliably prevent identity drift, overlapping poses, unstable pivots, or uncurated raw output. | **REJECT** as the production route. |
| New independent generation/extraction engine | Duplicates maintained functionality without a demonstrated blocker. | **REJECT**. |
| New local browser workflow and Base adapter | The upstream engine does not provide this project's Korean workflow, Figma visual-lineage record, project handoff structure, or Base contracts. | **BUILD_NEW**, bounded to the adapter and UI. |

The engine dependency must be pinned by immutable release/version and verified at installation. If future requirements demand source modification, the derivative work must retain Apache-2.0 notices and carry prominent change notices.

## 4. System boundary

### Base owns

- `tools/sprite-animation-studio/`: local server, UI, engine bridge, exporters, installers, and tests;
- a specialist operating skill only if existing Base Skill coverage confirms there is no owned input/output/validation boundary;
- request templates, validation contracts, license notices, and tool documentation;
- no project art, generated raw images, account credentials, API keys, or project-specific Figma files.

### Project owns

- source character/effect images and their rights evidence;
- Figma file/node URLs, approved reference snapshots, and decisions;
- per-action request files;
- run directories, candidate frames, accepted sprite assets, and engine imports;
- the final decision to ship each asset.

## 5. Figma visual lineage

Figma is the visual review surface, not the binary asset store.

For one animation request, the project Figma page is arranged left-to-right:

```text
Source reference
  → approved anchor
  → action-row candidates
  → selected frame sequence
  → final atlas / GIF preview
```

Every Base-tool run writes a portable lineage record containing:
- Figma file URL and node URL when one exists;
- exported reference snapshot filename and SHA-256;
- anchor ID and approval status;
- action name, direction, frame count, FPS, and loop mode;
- generated candidate IDs;
- selected order and non-destructive transforms;
- output filenames and SHA-256 values.

The initial MVP accepts a local uploaded PNG plus optional Figma URLs and exported-snapshot hashes. It does not auto-write to Figma, scrape private Figma content, or treat a changed remote Figma image as the old approved anchor. Automatic Figma upload/import is a later integration only after Figma permissions and a project-specific design-file contract are verified.

## 6. MVP architecture

```text
Local browser UI
  → Studio API
  → request + lineage validation
  → pinned sprite-gen engine bridge
  → candidate run directory
  → curation sidecar
  → deterministic export
  → project asset directory + Figma lineage record
```

### Components

| Component | Responsibility |
|---|---|
| `local_server` | Serves the browser UI only on localhost and provides validated job endpoints. |
| `request_model` | Validates action, direction, frame count, FPS, loop mode, reference source, and project output path. |
| `engine_bridge` | Creates an isolated run, invokes the pinned engine, captures reports, and fails closed on missing provider/output/expected frame count. |
| `curation` | Stores selection, order, transforms, and explicit rejection reasons in a non-destructive sidecar. |
| `exporters` | Produces frame PNGs, GIF preview, atlas, manifest, and a Godot handoff record. |
| `lineage` | Writes Figma/source/anchor/output hashes and approval states without copying source art into Base. |
| `ui` | Korean-first upload, action request, candidate inspection, frame controls, playback, and export summary. |

### Provider boundary

MVP default is the upstream engine's local Codex-backed generation path. A future direct OpenAI API provider is optional and must read credentials only from the user's local environment; no key is written to request files, Base, or Figma.

A provider failure is displayed as blocked with the exact failed precondition. It never silently falls back to a different provider or emits a static reference image as a successful animation.

## 7. Asset contracts

### Required request fields

```json
{
  "schema_version": 1,
  "kind": "sprite-animation-request",
  "project_id": "example-project",
  "asset_id": "knight",
  "asset_kind": "character",
  "anchor": {
    "source_path": "art/source/knight-idle.png",
    "approval_status": "approved",
    "figma_node_url": "optional"
  },
  "action": {
    "name": "attack_heavy",
    "direction": "left",
    "frame_count": 4,
    "fps": 8,
    "loop_mode": "none",
    "prompt": "heavy overhead sword strike"
  },
  "output_root": "art/animation-runs/knight"
}
```

### Required export fields

```text
frames/<action>/frame-*.png
preview/<action>.gif
atlas/sprite-sheet-alpha.png
atlas/manifest.json
lineage/<action>.json
godot/<action>.spriteframes.json
```

The Godot handoff records animation name, ordered frame file paths or atlas rectangles, FPS, and loop mode. It does not claim that a `.tres` resource has been imported or tested in a game unless a project adapter performs and verifies that separate step.

## 8. UX requirements

- Korean-first labels, with action name, frame count, FPS, loop mode, and provider status visible before generation.
- An anchor badge must name the approved reference that the next row inherits.
- Candidate frames support select/reject, drag reorder, delete from play sequence, x/y nudging, scale, flip, and optional grid/ground guide.
- Playback supports pause, step, FPS preview, and loop/non-loop behavior.
- Export is disabled until the expected number of selected frames is present and the anchor is approved.
- Every destructive control asks for confirmation and only affects the current local run; source references are immutable.
- The UI exposes raw-generation provenance and warnings rather than hiding them.

## 9. Acceptance criteria

1. A valid approved anchor plus `attack` request creates a named local run with an auditable lineage record.
2. The next action uses the accepted anchor, not the original broad character sheet, as its identity reference.
3. Missing provider, missing reference, malformed request, incomplete candidate row, or mismatched frame count produces a blocked state with no final export.
4. Reordering and transforming frames updates only the curation sidecar; original extracted frame files remain unchanged.
5. Exported manifest contains exact frame order, FPS, loop mode, and atlas rectangles.
6. A Figma node URL and image hash are preserved from source reference through final export.
7. No API key, OAuth token, raw generated image, or project asset is added to Base by tests or documentation.
8. All deterministic functions have automated tests; provider generation uses a fake bridge fixture in tests.

## 10. Adversarial review

| Attack | Risk | Required mitigation |
|---|---|---|
| Prompt-only identity preservation | Face, armor, palette, or proportions drift between actions. | Approved anchor ownership; broad source references stop being row inputs after anchor approval. |
| One-shot atlas generation | Poses overlap or frame boundaries cannot be trusted. | Generate and validate one action row at a time, then curate. |
| Transparent output assumption | Provider output may lack usable alpha or contain background fringe. | Chroma/alpha pipeline and explicit extraction QA; no silent export. |
| Figma drift | A remote image changes after approval. | Record URL + local exported snapshot hash; do not overwrite an accepted run's anchor. |
| Base contamination | Source art, tokens, or large generated files enter common repo history. | Ignore run/output paths; Base contains code/templates/tests only. |
| Dependency drift | Upstream changes break output semantics. | Immutable pin, installation check, compatibility smoke fixture, and explicit upgrade PR. |
| False Godot completion claim | A JSON handoff is mistaken for working in-game animation. | Separate export success from project import and runtime verification. |

## 11. Exclusions for MVP

- Automatic Figma writing or asset upload;
- automated publication of generated sprites to any project repository;
- direct editing of Godot scenes/resources;
- whole-atlas one-shot generation;
- unreviewed bulk generation of every animation state;
- background removal for arbitrary complex photographs;
- account, credential, or billing setup automation.

## 12. Validation and rollback

Validation has four layers:
1. schema and path validation;
2. deterministic unit tests for request, lineage, curation, and export manifest;
3. fixture-based engine-bridge integration tests;
4. manual localhost visual review of upload → anchor → candidate curation → GIF/atlas export.

Rollback is a single PR revert. Project runs remain outside Base and are never altered by reverting the tool package. An engine-pin upgrade is separately revertible by restoring the prior pin.

## 13. Implementation sequence

1. Add the request/lineage schemas and validator tests.
2. Build the local run directory and fake engine bridge.
3. Add curation persistence and deterministic exporters.
4. Build the localhost UI against the tested API.
5. Integrate the pinned upstream engine only after the fake path passes.
6. Add Figma lineage intake and documentation.
7. Run static, test, visual, and adversarial review gates; then prepare project-adoption guidance.
