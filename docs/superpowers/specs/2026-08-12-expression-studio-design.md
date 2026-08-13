# Expression Studio Design

## Decision

Create `tools/expression-studio` as a separate local, fail-closed tool. It owns a single approved character anchor, structured face controls, prompt resolution, candidate review, and a project-GPT Figma delivery packet. It does not create animation atlases, GIFs, ZIP files, Figma credentials, or a Figma mutation client.

The existing `tools/sprite-animation-studio` remains the owner of multi-frame pose/action/effect generation and atlas export. Both tools may read the same project Figma registry, but no shared package is extracted until at least two stable consumers demonstrate the same interface.

## User outcome

A project GPT can take an approved original character image, request a bounded facial change such as a left wink, review several identity-preserving candidates, select the usable result, and receive a packet that lets the matching project GPT place that result only in that project's existing Figma generation area.

## Input contract

- `project_id`, `asset_id`, and `output_root` are project-relative, validated identifiers/paths.
- The anchor must name an existing local image, its approved Figma node URL, and `approval_status: approved`.
- The request supports up to four face controls, one gaze value, and one head-pose value.
- Face controls use stable product IDs, e.g. `AU46`, plus intensity `A` through `E`; `AU46` additionally requires an explicit `left` or `right` eye side. Sides are the character's anatomical left/right, not the viewer's.
- Intensity resolves into natural-language edit scope: `A` very subtle, `B` subtle, `C` moderate, `D` strong, and `E` maximum readable. It is not a provider-specific numeric guarantee.
- `AU46` resolves to a natural-language instruction such as `left-eye wink`; its code alone is never treated as a model-guaranteed command.
- A preset resolves into the same explicit controls and is recorded in lineage; the user can inspect the resolved controls before generation.

## Control taxonomy

`face` contains only curated facial-action controls. `gaze` and `head_pose` are separate fields, even where the supplied reference chart presents them with AU-like labels. This avoids falsely claiming that every label in a reference grid is a canonical FACS action unit.

Initial controls:

- brow: `AU1`, `AU2`, `AU4`
- eyelid/eye: `AU5`, `AU6`, `AU7`, `AU41`, `AU42`, `AU43`, `AU44`, `AU45`, `AU46`
- nose: `AU9`, `AU10`
- mouth/jaw: `AU12`, `AU14`, `AU15`, `AU16`, `AU17`, `AU18`, `AU20`, `AU23`, `AU24`, `AU25`, `AU26`, `AU27`, `AU28`
- gaze: `left`, `right`, `up`, `down`, `center`
- head pose: `turn_left`, `turn_right`, `up`, `down`, `tilt_left`, `tilt_right`, `forward`, `back`, `neutral`

Initial presets: `idle_neutral`, `alert`, `determined`, `hurt`, `surprised`, `joy`, `anger`, `fear`, `blink`, `wink`.

## Conflict and safety rules

- Reject more than four face controls.
- Reject incompatible pairs: `AU43` with `AU5` or `AU42`; `AU45` with `AU43`; `AU46` with `AU43`; `AU25` with `AU24`; `AU26` with `AU27`; `AU18` with `AU20`.
- Reject two `AU46` controls: bilateral winking is semantically both eyes closed and must be expressed with `AU43`.
- Do not silently remove a requested control. Return the conflicting IDs before generation.
- Always resolve an identity-preservation prefix: retain face geometry, hairstyle, costume, palette, framing, lighting, and art style; edit only the selected facial expression, gaze, and head pose.
- Maximum candidate count is eight. No automatic approval or delivery follows generation.

## Generation boundary

The first implementation exposes a local engine protocol and a deterministic fake engine for tests/demo. It produces a stable natural-language image-edit instruction and an engine request that includes a run-local copy of the approved anchor, never the source path. The source hash is checked again after generation; any attempted source mutation is restored and blocks the run. A production provider adapter is deliberately not added until its configured runtime, pricing, data handling, model version, and image-edit capability are verified in the project workspace.

This is not a claim that any particular model natively recognizes every FACS code. OpenAI's documented image-edit API can use source images and text instructions; the tool turns structured controls into those explicit instructions. See [OpenAI image generation guide](https://developers.openai.com/api/docs/guides/image-generation).

## Review, export, and delivery

- The run stores `lineage.json` with anchor SHA-256, source Figma URL, requested controls, preset, resolved instruction, rejection/conflict outcome, selected candidate, and tool version.
- Only the exact requested number of readable PNG candidates inside the run's candidate directory may be reviewed; a contact sheet plus selected PNG is then created under the configured project-relative output root.
- `POST /api/runs/{id}/figma-delivery` is enabled only after one candidate is explicitly selected and exported.
- The packet resolves only the configured, ready project target from `PROJECT_FIGMA_TARGET_REGISTRY.json`; it includes the target page and generation-area node IDs, not bytes, tokens, ZIP files, or fallback targets.
- The matching project GPT, which has the Figma connector and the same local image bytes, performs the actual placement. The local tool only prepares the packet.

## Project Figma board

Do not create an additional top-level page. The existing `Sprite Animation Studio` page stays the asset-review board. Add an `Expression Runs` section inside its already verified `Generated Assets` area for each active project, preserving earlier sprite-action results and avoiding page sprawl.

## Acceptance criteria

1. Invalid/unknown controls, over-limit controls, and conflicts are rejected before engine invocation.
2. A valid wink request produces an identity-preserving resolved prompt that explicitly says `left-eye wink` or `right-eye wink`.
3. Presets resolve to visible controls and are serialized in lineage.
4. Candidate selection is explicit; exporting/delivery is blocked before selection.
5. Figma routing remains exact-project, ready-status-only, file-key-validated, and node-ID-targeted.
6. The web UI distinguishes face, gaze/head-pose, and preset controls, reports conflicts, shows resolved prompt/lineage, and never claims Figma upload succeeded.
7. Tests cover normal, invalid, conflict, delivery, web-contract, and regression cases.

## Out of scope and rollback

- No direct Figma image upload, token storage, ZIP handoff, bulk expression generation, automatic asset replacement, animation blending, or provider credentials.
- No modification of an approved source image.
- Rollback is a revert of the Expression Studio commits and removal of only the new `Expression Runs` Figma sections. Existing `Generated Assets` content and registry IDs remain intact.

## Adversarial findings incorporated before build

| Finding | Decision |
| --- | --- |
| The supplied AU-style chart mixes face, gaze, head movement, and nonstandard labels. | Separate taxonomy and do not advertise every label as canonical FACS. |
| A bare AU code is ambiguous to an image model. | Resolve each control to natural language plus an identity-preservation contract. |
| Static expression review and multi-frame sprite export have different completeness rules. | Separate tool package; share only registry data until a proven shared interface exists. |
| Multiple project Figma targets permit accidental cross-project delivery. | Reuse bound `project_id`, ready status, Figma file-key validation, and exact node IDs. |
| A candidate contact sheet can invite accidental acceptance. | Require an explicit selected candidate before export/delivery. |
