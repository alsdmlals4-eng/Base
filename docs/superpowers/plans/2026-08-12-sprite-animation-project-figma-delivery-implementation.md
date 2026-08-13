# Sprite Animation Project-Figma Delivery Implementation Plan

> **Implementation record:** this plan was executed inline. The target project Figma files were later explicitly authorized for mutation; their verified `Sprite Animation Studio` pages and `Generated Assets` areas are now recorded in the registry.

**Goal:** Extend the shared Sprite Animation Studio so a project GPT can select a purpose-built sprite mode and prepare a fail-closed, project-specific Figma delivery packet for the same project workspace. The Base web app never writes Figma directly; a project GPT with the image bytes and Figma connector performs the later placement.

**Architecture:** Add a small registry/delivery domain module that reads the Base routing JSON, validates a project target and its mutation status, and returns only a serializable placement packet. Add mode compatibility at request validation, expose it through the API/web UI, and test both ready and blocked target paths. Publish a reusable project-GPT prompt and update the existing adoption documentation to make the authority boundary explicit.

**Tech stack:** Python 3.11+, FastAPI, Pydantic v2, pytest, vanilla HTML/CSS/JS, JSON Schema.

## Scope and non-goals

- In scope: `expression_variation`, `pose_sequence`, `effect_stages`, and `sprite_action`; project target resolution; protected-target blocking; handoff packet; project-GPT Figma placement instructions.
- Out of scope: Figma API tokens, direct local-browser uploads, ZIP delivery, mutation of any supplied project Figma file, generated artwork, Godot runtime validation.
- Protected by default: a caller cannot select a fallback target. A project becomes deliverable only after `READY_FOR_DELIVERY` and verified page/area node IDs are present.

## Existing-solution and adversarial checks

- Reuse the existing request, run, export, Figma lineage, curation, and FastAPI abstractions. Do not add an MCP server or duplicate the upstream `sprite-gen` generator.
- Preserve the upstream `sprite-gen` license notices and the current real/fake engine boundary.
- Fail closed for: missing registry, unknown project ID, duplicate project IDs, malformed Figma target, non-ready mutation status, missing approved anchor, missing selected outputs, and incompatible asset kind/mode.
- Keep a Figma URL and file key as routing metadata only. They do not prove edit permission or that a page/area already exists.

## Implementation tasks

### 1. Add request mode validation (test first)

**Files:**
- Modify `tools/sprite-animation-studio/src/sprite_animation_studio/models.py`
- Modify `tools/sprite-animation-studio/tests/test_models.py`
- Modify `templates/sprite-animation/sprite-animation-request.schema.json`

1. Add a typed `SpriteAnimationMode` literal/enum and default `sprite_action` so legacy valid requests remain valid.
2. Validate `expression_variation` and `pose_sequence` only for `character`, and `effect_stages` only for `effect`; allow `sprite_action` for both.
3. Add positive and negative tests before implementation; keep current approval and path validation tests intact.
4. Represent the same optional default and mode enum in JSON Schema so external producers do not drift.

### 2. Build a fail-closed delivery domain (test first)

**Files:**
- Add `tools/sprite-animation-studio/src/sprite_animation_studio/delivery.py`
- Add `tools/sprite-animation-studio/tests/test_delivery.py`

1. Define models for registry entries and the resulting Figma delivery packet.
2. Load a registry from an explicit JSON path; reject malformed files and duplicate project IDs.
3. Resolve only the matching `project_id`. A missing/unknown/non-ready entry produces a specific blocked result/error, never a fallback target.
4. Build packets containing mode, anchor lineage, target file metadata, page/area names, run ID, and project-relative visual deliverables. Do not add bytes, credentials, or a Figma mutation client.
5. Test a `READY_FOR_DELIVERY` fixture and the `REGISTERED_NO_MUTATION`/unknown/malformed cases.

### 3. Wire the packet into service and API (test first)

**Files:**
- Modify `tools/sprite-animation-studio/src/sprite_animation_studio/service.py`
- Modify `tools/sprite-animation-studio/src/sprite_animation_studio/app.py`
- Modify `tools/sprite-animation-studio/tests/test_api.py`

1. Require the run to have an approved anchor and curated selected frames before a packet is prepared.
2. Add `POST /api/runs/{run_id}/figma-delivery` that returns a packet for a ready target and a deterministic conflict response for a protected/unknown target.
3. Inject an optional registry into `create_app` for tests; expose a CLI option for a registry path instead of baking a Figma target into the app.
4. Return no claim that Figma was uploaded. The response is explicitly `ready_for_project_gpt` rather than a send success.

### 4. Expose project mode and guarded handoff in the web tool

**Files:**
- Modify `tools/sprite-animation-studio/web/index.html`
- Modify `tools/sprite-animation-studio/web/app.js`
- Modify `tools/sprite-animation-studio/web/styles.css` only if layout needs it
- Modify `tools/sprite-animation-studio/tests/test_web_contract.py`

1. Add a Korean mode selector with the four stable values.
2. After export, offer `프로젝트 GPT 전송 준비` and render the packet/blocked explanation.
3. State that the final Figma placement runs in the matching project GPT workspace and is unavailable for a protected target; do not imply an automatic cross-chat upload.
4. Verify UI wiring and user-facing guard language using static web contract tests.

### 5. Publish the reusable project-GPT and adoption contracts

**Files:**
- Add `templates/sprite-animation/project-gpt-figma-delivery.md`
- Modify `tools/sprite-animation-studio/README.md`
- Modify `docs/knowledge/game-development/SPRITE_ANIMATION_STUDIO_ADOPTION_GUIDE.md`
- Modify `tools/sprite-animation-studio/tests/test_docs_contract.py`

1. Provide an exact project-GPT action sequence: resolve registry, check status/anchor/selection/image availability, create/resolve the designated page and area only when ready, write a new run section, and return the section URL.
2. Explicitly prohibit handling `REGISTERED_NO_MUTATION` targets, fallback routing, destructive replacement, ZIP/token use, and unsupported delivery claims.
3. Make local app vs. project GPT/Figma connector roles unambiguous in README and adoption guide.

## Verification and review

1. Run focused pytest suite for the package.
2. Run `node --check` for `web/app.js` and `git diff --check`.
3. Run the relevant Base schema/contract test if available; report dependency/pre-existing Base-wide failures separately.
4. Adversarially inspect the diff for accidental Figma mutation, credentials, target fallback, ZIP remnants, default status escalation, and schema/docs/UI drift.
5. Commit only validated changes. Publish the new exact head to the existing draft PR; do not merge or alter any protected Figma file.

## Rollback

Revert the implementation commit(s). The feature adds no Figma content, external credentials, or irreversible project data; registry entries remain protection-marked throughout.
