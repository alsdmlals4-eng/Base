# Subscription-Included Visual Import Design

**Date:** 2026-08-13

**Status:** `APPROVED / IMPLEMENTED_AWAITING_FINAL_VERIFICATION`

**Owner:** Base shared visual tools

**Applies to:** `Expression Studio`, `Sprite Animation Studio`, later `Base Tool Hub`

## 1. Goal

Make the normal art-tool workflow usable without purchasing OpenAI API credit. ChatGPT or Figma uses the image-generation allowance already included in the user's subscription, then the Studios import, validate, review, arrange, export, and prepare exact-project Figma handoff records. The existing OpenAI API adapter remains an explicit optional metered route and is never selected automatically.

## 2. Evidence and existing-solution disposition

| Candidate | Evidence | Decision |
| --- | --- | --- |
| ChatGPT included image generation | ChatGPT image generation consumes included usage limits; API-key use is billed at standard API rates. [Official pricing](https://learn.chatgpt.com/docs/pricing) | `REUSE_PRIMARY_SOURCE` |
| Figma included AI credits | Professional Full seats include a monthly allocation; image make/edit consumes fixed credits and pay-as-you-go can be disabled. [Credit management](https://help.figma.com/hc/en-us/articles/35865276858647-Manage-AI-credits), [feature rates](https://help.figma.com/hc/en-us/articles/33459875669015-How-AI-credits-work) | `REUSE_SECONDARY_SOURCE` |
| Figma agent / write-to-canvas MCP | Figma's agent can use Make image; write-to-canvas places external content and is not the same generation authority. [Official distinction](https://help.figma.com/hc/en-us/articles/37998629035799-Work-with-the-Figma-agent-in-design-files) | `REUSE_WITH_ROLE_SPLIT` |
| Figma Weave | Free during open beta and accepts reference images, prompts, options, and multiple runs; future general availability will use AI credits. [Official beta terms](https://help.figma.com/hc/en-us/articles/40779260614935-Use-Weave-tools-in-Figma) | `PILOT_OPTIONAL`, never a permanent free dependency |
| ComfyUI local | No provider call is required; Windows desktop supports local execution and recommends a dedicated GPU. [Official requirements](https://docs.comfy.org/installation/desktop/windows) | `DEFER_HARDWARE_DEPENDENT` |
| Existing OpenAI API adapter | Automated and tested, but requires separately funded API billing. | `PRESERVE_EXPLICIT_METERED_OPTION` |

No new image model, cloud backend, ZIP handoff, second Hub, or automatic paid-credit purchase is introduced.

## 3. Product decision

### 3.1 Default mode

Both Studios start in `subscription_handoff_import` mode. This mode performs no OpenAI, Figma AI, Weave, or other generation call. It accepts image files that the operator already generated in ChatGPT, Figma, or a local generator.

The UI must show:

- `추가 API 과금 없음 — 이미 생성한 이미지 가져오기`
- the configured immutable project ID;
- the selected source declaration: `CHATGPT_INCLUDED`, `FIGMA_INCLUDED`, `LOCAL_GENERATOR`, or `OTHER_USER_SUPPLIED`;
- a warning that this declaration records workflow provenance but does not prove the external provider or subscription tier;
- upload limits and whether the result is eligible for local export or exact-project Figma delivery.

### 3.2 Metered mode

`openai` remains CLI-only opt-in. It requires all existing key, official endpoint, exact model, project-owned approved-anchor, provenance, and delivery gates. The browser cannot change an import-mode server into a metered server. No automatic fallback crosses between import, simulated, and OpenAI modes.

`simulated` remains test/development-only and cannot export or prepare Figma delivery.

### 3.3 Spending guard

The repository never enables Figma pay-as-you-go, purchases credits, funds an OpenAI API project, or changes an account billing setting. Documentation tells the operator to disable Figma pay-as-you-go if zero surprise spend is required. A local import run records `cost_route: INCLUDED_OR_LOCAL_HANDOFF` and `provider_call_made: false` in status, lineage, export manifest, and delivery packet.

## 4. Architecture

### 4.1 Shared import boundary

Create one focused import module in each Studio, following the existing package boundary rather than adding a new cross-package generation authority.

It must:

1. receive bounded multipart image uploads through the existing loopback, session, origin, and CSRF protections;
2. ignore browser filenames for storage identity;
3. reject directory information, links, non-images, malformed images, and unsupported formats;
4. allow PNG, JPEG, and WebP input, with a maximum of 25 MiB and 4096 pixels on either edge per file; cap complete Expression requests at 202 MiB and complete Sprite requests at 402 MiB before multipart parsing so every documented maximum-count request remains representable with multipart overhead;
5. decode dimensions before full pixel loading and fail closed on decompression-bomb signals;
6. publish SHA-named or index-named fresh files through the existing no-follow staging writer;
7. persist SHA-256, detected format, width, height, alpha presence, declared source, and import order;
8. never retain a partial run as export-eligible when any required upload fails.

The implementation adds the exact `python-multipart==0.0.32` dependency, the current Apache-2.0 release verified from [PyPI](https://pypi.org/project/python-multipart/), because binary file upload is the bounded HTTP contract. Base64-in-JSON and browser-controlled filesystem paths are rejected.

### 4.2 Expression Studio

The import request retains the current project, approved anchor, FACS controls/preset, gaze, head pose, and candidate count. It additionally supplies 1–8 candidate image files in one request.

Acceptance rules:

- upload count exactly equals `candidate_count`;
- each candidate is readable and non-empty;
- no candidate is pixel-identical to the approved anchor;
- no two candidates are pixel-identical;
- imported candidates are not described as OpenAI-generated unless independently proven;
- selection remains explicit;
- export eligibility requires verified project-owned anchor evidence but does not require an API provider claim;
- Figma delivery additionally requires the exact ready target and current packet/hash checks.

The existing contact-sheet, selected-image export, lineage, manifest, and delivery packet paths are reused.

### 4.3 Sprite Animation Studio

The import request retains the current project, approved anchor, asset kind, mode, action, frame count, FPS, grid, and Godot handoff fields. It supplies 1–16 ordered frame files, preserving the current request contract.

The UI supports upload order review, drag reorder, and removal before submission. The server treats submitted multipart order as canonical and assigns `frame-000.png` through `frame-NNN.png` itself.

Acceptance rules:

- upload count exactly equals `frame_count`;
- every frame is readable and visually non-empty;
- every frame has the same dimensions;
- all duplicate frames are rejected because imported order must represent distinct reviewable animation states;
- pose/action and effect-stage modes both use the same trusted import boundary;
- effect-stage frames report alpha presence and opaque bounds. Lack of alpha is a warning, not an automatic failure, because background isolation may happen in Figma afterward;
- explicit curation is still required before export;
- existing GIF, atlas, contact sheet, manifest, Godot logical paths, lineage, and Figma packet generation are reused.

## 5. API and state contract

Add separate endpoints rather than overloading the existing JSON generation endpoint:

- `POST /api/import-runs` in Expression Studio: multipart `request_json` plus repeated `candidates` parts.
- `POST /api/import-runs` in Sprite Animation Studio: multipart `request_json` plus ordered repeated `frames` parts.

The existing `POST /api/runs` keeps simulated/OpenAI generation semantics. On an import-mode server it returns `409 MODE_NOT_AVAILABLE` and cannot trigger a provider call.

Successful import returns the existing public run view plus:

```json
{
  "run_mode": "subscription_handoff_import",
  "cost_route": "INCLUDED_OR_LOCAL_HANDOFF",
  "provider_call_made": false,
  "declared_source": "CHATGPT_INCLUDED",
  "imported_files": [
    {
      "index": 0,
      "sha256": "<64 lowercase hex>",
      "format": "PNG",
      "width": 1024,
      "height": 1024,
      "has_alpha": true
    }
  ]
}
```

The server owns `run_mode`, `cost_route`, and `provider_call_made`. A browser field cannot promote an imported, simulated, or unknown run to OpenAI provenance.

## 6. User flow

### Expression

1. Select or upload the approved anchor in ChatGPT/Figma and generate expression candidates using included allowance.
2. Open the project-bound Expression Studio from the later Tool Hub or direct loopback command.
3. Choose the declared source, enter the existing FACS/preset controls, and upload candidates.
4. Compare anchor and candidates; select one explicitly.
5. Export locally, then prepare the exact-project Figma packet if routing is verified.
6. Project GPT places and reads back the exact Figma node before any placement-success claim.

### Sprite

1. Generate ordered pose/action frames or effect stages in ChatGPT/Figma/local generation.
2. Upload frames, review/reorder them, and submit the canonical order.
3. Preview playback and inspect warnings, dimensions, alpha, duplicates, and continuity.
4. Confirm curation and export GIF, atlas, contact sheet, frames, manifest, and Godot paths.
5. Prepare exact-project Figma delivery only when all current gates pass.

Cloud GPT cannot directly access a user's localhost page. Until a separately approved remote/app bridge exists, the upload action is performed by the user or local Codex process. The Figma MCP write-to-canvas step remains an external-content placement step, not an invocation of Figma's AI generator.

## 7. Concurrent projects

Import mode preserves the existing immutable `project_id`, project root, launch nonce, adapter hash, registry hash, loopback origin, and distinct-port requirements. Every run remains under that project's verified `.asset-vault/library/generated/<tool>/...` root. No project selector in the browser can retarget another project.

The later Tool Hub may launch one import-mode Studio instance per `(tool_id, project_id)`; this design does not implement that supervisor.

## 8. Error handling

- Any malformed request part, count mismatch, unsupported image, oversized input, decompression-bomb signal, dimension mismatch, duplicate rule failure, staging violation, anchor mutation, or policy drift returns a bounded blocked result with no export eligibility.
- Provider/network/billing errors cannot occur in import mode because it makes no provider call.
- Browser state clears prior success, selection, preview, export, and Figma-ready panels after a blocked import.
- Error responses never echo file bytes, local absolute paths, provider secrets, browser filenames, or raw exception text.

## 9. Tests and evidence

### Automated

- multipart happy paths for Expression and both Sprite mode families;
- missing, extra, zero-byte, non-image, unsupported, oversized, high-dimension, decompression-bomb, mismatched-size, transparent, opaque, adjacent-duplicate, and non-adjacent-duplicate fixtures;
- final-entry link/hard-link and directory swap attempts at every imported candidate/frame boundary;
- import run never calls the configured generation engine;
- simulated and OpenAI endpoints remain separated;
- server-owned provenance/cost fields cannot be forged;
- export/manifest/lineage/packet hashes bind exact imported bytes;
- project A cannot import/export/deliver through project B;
- UI order, removal, blocked-state reset, cost banner, and no-paid-default contract tests;
- existing Expression, Sprite, shared-contract, Base validation, JavaScript syntax, diff, and dependency checks.

### Runtime

- supplied portrait plus real ChatGPT/Figma-created candidates: `NOT_RUN` until the user supplies or generates the files;
- live Figma placement/readback: `NOT_RUN`;
- Windows import/export and two-or-more concurrent project instances: `BLOCKED_UNVERIFIED` until executed on Windows.

No automated test, imported fixture, or Figma routing record proves visual quality, subscription entitlement, live generation, or Figma placement.

## 10. Scope exclusions

- purchasing or configuring paid credits;
- automatically invoking ChatGPT subscription generation from a local server;
- automatically invoking Figma's agent, Make image, or Weave from the Studio;
- remote hosting, ChatGPT App publishing, account sign-in, or credential brokerage;
- local ComfyUI installation or model/license selection;
- character-consistency scoring by an unverified vision model;
- changing any of the eight project Figma files before exact connector authorization and readback;
- implementing the Tool Hub supervisor in this phase.

## 11. Completion criteria

The implementation phase is accepted only when:

1. both Studios default to import mode and make zero provider calls in that mode;
2. Expression imports and exports a reviewed selected candidate;
3. Sprite imports and exports both pose/action and effect-stage sequences;
4. all imported bytes are bounded, safely staged, hashed, and durably represented in lineage/manifests/packets;
5. paid OpenAI mode remains explicit, separated, and unchanged in its safety gates;
6. all focused and Base validations are green;
7. independent adversarial review reports P0/P1 zero;
8. PR checks are green;
9. unexecuted paid generation, Windows concurrency, and Figma placement remain explicitly unverified.

## 12. Rollback

Revert the import-mode commits and restore the Studios' current simulated defaults. Keep the approved-anchor, staging, provenance, export, and Figma routing hardening. Never delete user-generated images or project vault runs during rollback. The optional OpenAI adapter and ignored local key file remain untouched unless the user separately requests their removal.
