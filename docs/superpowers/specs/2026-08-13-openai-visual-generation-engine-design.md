# OpenAI Visual Generation Engine Design

## Decision

Keep Figma as the project `VISUAL_WORKSPACE`, review board, pinned handoff view, and approved-result placement surface. GitHub project contracts and confirmed decisions remain the canonical rules and approval authority. Run image generation, frame extraction, curation, GIF/atlas export, and project-local file writes in the Base local HTML tools.

Add explicit OpenAI-backed engines to `Expression Studio` and `Sprite Animation Studio`. The local tools use the OpenAI Image API only when the operator explicitly selects the production engine and `OPENAI_API_KEY` is present. Fake engines remain available for automated tests, but simulated outputs are never eligible for export or Figma delivery.

## Why Figma is not the generator runtime

Figma can contain raster images and its Plugin API exposes `figma.createImage(bytes)`. The connected project GPT can also create or edit Figma nodes when it has a Figma write tool. That makes Figma suitable for visual organization, comparison, annotations, component composition, and keeping approved references.

Figma is not a general local execution host. It does not replace the project filesystem, Python image processing, provider credentials, repeatable CLI tests, Godot handoff generation, or multi-project output isolation. The current Base delivery packet contains project-relative paths rather than image bytes, so the local browser does not upload an image merely by preparing that packet. Actual placement requires the matching project GPT to read the selected visual and use its Figma connector in the exact registered file.

## External-tool versus Figma ownership

| Work | Owner | Reason |
| --- | --- | --- |
| FACS expression generation | Local HTML tool + OpenAI Image API | Needs a source file, credential, provider error handling, and candidate files. |
| Pose/action frame generation | Local HTML tool + OpenAI Image API | Needs ordered frames, identity constraints, extraction, and filesystem output. |
| Effect-stage generation | Local HTML tool + OpenAI Image API | Needs stage prompts, transparency/model rules, frame validation, and export. |
| GIF, atlas, manifest, Godot handoff | Local HTML tool | Deterministic binary/file processing belongs in the project workspace. |
| Candidate comparison and selection | Local HTML first; Figma after approval | Local selection gates export; Figma preserves the approved visual context. |
| UI layout, components, tokens, comments | Figma | These are editable design-authoring and review tasks. |
| Approved visual reference and pinned handoff history | Project Figma file | It is the shared visual workspace for later GPT and human work; the responsible GitHub record remains approval canon. |
| Automatic game implementation | Project repository/Godot tools | Figma nodes are design evidence, not runtime game files. |

Future tools follow the same rule: use an external/local tool for asset generation, data transformation, validation, audio processing, localization pipelines, build/export, and engine integration. Use Figma for UI composition, visual libraries, annotations, approval, and cross-project visual review. A hybrid handoff is preferred when both generation and visual review matter.

## Production engine contract

### Expression Studio

- Use the OpenAI Image API edit endpoint with the run-local approved-anchor copy.
- Default production model: `gpt-image-2`, `input_fidelity=high`, PNG output.
- Generate exactly the requested candidate count and store each response only in the run candidate directory.
- Carry provider/model provenance, the resolved FACS instruction, and the anchor SHA-256 into lineage.
- Reject empty, unreadable, duplicate, out-of-directory, or wrong-count outputs.

### Sprite Animation Studio

- Support `pose_sequence`, `sprite_action`, and `effect_stages` with mode-specific prompts.
- Produce exactly the requested frame count, then reuse the existing curation, GIF, atlas, manifest, and Godot handoff pipeline.
- Character action prompts preserve identity, silhouette, outfit, palette, art style, facing direction, and camera framing while changing only the requested motion phase.
- Effect prompts explicitly name startup, active, impact, and fade ordering. Transparent-background requests use a model/configuration that officially supports transparency; they do not silently claim transparency when the selected model does not support it.
- Independent frame generation is reviewable candidate output, not proof of production-quality temporal coherence. The sample smoke test must report visual drift rather than auto-approve it.

## Simulation boundary

Every engine result declares provenance and delivery eligibility.

- `openai`: real provider response; eligible for user review, export, and later Figma placement.
- `pinned_sprite_gen`: real configured upstream provider response; eligible only after immutable repository validation **and** an OS-isolated workspace runner. The current adapter remains blocked because the isolation runner is not implemented.
- `simulated`: deterministic test fixture; visible only as a test result and blocked from export/Figma delivery.

The browser shows the provenance prominently. It must never label an unchanged copied anchor or transparent fixture as a completed expression, action, or effect.

## Project isolation and concurrent use

- A registry-backed server requires one immutable canonical `project_id`; browser requests cannot override it.
- The UI reads the bound project ID from `/api/config` and renders it read-only.
- Each Studio supports an explicit `--port`. The Base Tool Hub is the single multi-project process supervisor and allocates ports atomically; a direct operator may supply one explicit port when launching a Studio without the Hub. A separate eight-project launcher does not own process or port allocation.
- Run directories use UUIDs and all provider outputs remain under `<project-root>/.asset-vault/library/generated/<tool-id>/<run-id>/` or another project adapter-approved local-only staging root.
- Browser requests cannot choose a free-form output root. The Studio verifies vault initialization, gitignore, project containment, protected/tracked paths and symlink safety before generation; tracked assets require the existing explicit promotion contract.
- A delivery packet resolves only the bound READY target whose Figma URL file key and canonical node IDs validate.

## Credential and cost boundary

- Read `OPENAI_API_KEY` from the process environment only. Never accept it in the browser form, request JSON, lineage, manifest, logs, Figma, or Git.
- The local tool fails closed when the key is absent or the API rejects the request.
- ChatGPT subscription and OpenAI API billing are separate. Provider calls can incur cost and must be initiated by an explicit generation action.
- API responses and error text are sanitized so authentication material cannot appear in UI or files.

## Sample-image verification

Use the supplied portrait as a smoke-test anchor only; it is not automatically approved project art.

1. Generate an AU46 character-anatomical left wink and verify the output is readable, non-empty, and pixel-different from the anchor.
2. Generate a four-frame action sequence and verify four readable non-empty PNGs plus GIF, atlas, manifest, and Godot handoff.
3. Generate four effect stages and verify stage order is reviewable plus the same export artifacts.
4. Visually inspect identity/style drift. API success alone does not pass this gate.
5. Confirm every output is inside the verified project-local vault staging root, no protected/tracked/symlink path was used, and no source hash changed.
6. Prepare the exact-project Figma packet only after explicit selection/export.
7. Use the matching project GPT's Figma connector to place selected results; then read back the exact node and visually inspect it before claiming Figma implementation.

Because the current Codex workspace cannot read the operator's Windows process environment, the final paid smoke calls run from the same Windows PowerShell session where `OPENAI_API_KEY=present`. Local mock tests and all non-network validations run in Codex first.

## Error handling

- Missing key, billing/verification failure, rate limit, moderation refusal, timeout, malformed base64, wrong image count, invalid PNG, or identity-source mutation blocks the run.
- A provider failure never falls back to the fake engine.
- Partial sprite output is retained only as blocked diagnostic evidence and cannot be exported or delivered.
- Figma placement remains separate: a ready packet is not an upload-success claim.

## Acceptance criteria

1. Both tools expose an explicit production OpenAI engine and an explicit simulated test engine.
2. Simulated results cannot be exported or prepared for Figma delivery.
3. The configured project ID is read-only in the UI and cross-project requests fail closed.
4. Two or more project instances can run simultaneously on distinct loopback ports without sharing outputs.
5. Expression, action, and effect requests produce validated project-local images when run with a usable key.
6. The attached sample completes all three paid smoke paths, with results reported as PASS, FAIL, or BLOCKED_UNVERIFIED using file and visual evidence.
7. Figma placement is claimed only after the matching connector writes and re-reads the actual nodes.
8. Focused suites, Base local validation, JavaScript syntax checks, diff checks, adversarial review, and PR checks pass before merge.

## Rollback

Revert the production-engine commits and restore the CLI to provider-disabled behavior. Keep existing approved Figma content, project registry entries, and user project assets untouched. Simulated fixtures and paid smoke outputs are project-local/generated artifacts and are never committed to Base.
