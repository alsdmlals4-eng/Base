# Tool Hub Figma Bridge Design

## Goal

Complete the local production delivery slice for Base Tool Hub without depending on ChatGPT as a hidden runtime hop:

`local Tool Hub -> exact project output -> paired Figma Bridge -> registered Generated Assets node -> readback receipt`.

Issue: #375.

## Boundaries

- Do not modify or duplicate open draft PR #373. Character expression/outfit/scene behavior remains owned there until it is completed and merged.
- Reuse merged PR #363 for Windows no-terminal launch and managed project onboarding.
- Reuse merged PR #370 and `docs/operations/PROJECT_FIGMA_TARGET_REGISTRY.json` for exact Figma file/node routing.
- Keep existing executable owners under `tools/*`; `Base Tool Hub/` is suite/navigation authority, not a duplicated source tree.
- Do not add Tauri now. Keep the localhost browser contract shell-agnostic so Tauri can wrap the same frontend later.
- Do not claim real provider image quality, Windows Studio child execution, or game integration from this slice.

## Existing-solution-first decision

| Option | Verdict | Reason |
|---|---|---|
| Static HTML only | REJECT | Cannot safely own project writes, secret-bearing provider calls, process ownership, or authenticated Figma mutation. |
| Existing localhost HTML/JS + Python backend | REUSE | Already implemented, project-scoped, testable, and compatible with current Windows launcher. |
| Tauri 2 shell now | DEFER | Tauri can wrap an existing web frontend later, but Rust/build/signing/update complexity does not help prove the missing delivery loop today. |
| ChatGPT/Figma connector as runtime dependency | REJECT | Useful for verification and assisted workflows, but the local tool must not require a chat session to deliver an image. |
| Figma Plugin API bridge | BUILD_NEW (bounded) | Figma Plugin API provides actual file write access and image creation; network access can be restricted to localhost. |

## Architecture

### 1. Local delivery authority

`tools/tool-hub` owns a small delivery queue. A delivery job is created only from an already-exported project-scoped artifact. The browser cannot provide arbitrary filesystem paths, Figma file keys, node ids, commands, or URLs.

A job is keyed by:

- `tool_id`
- `project_id`
- `run_id`
- `delivery_id`

and binds:

- exact output relative path
- output SHA-256
- media type
- byte length
- canonical Figma file key
- canonical delivery page node id
- canonical generation area node id
- creation and expiry timestamps
- single-use state

### 2. Pairing

The Hub creates a short-lived one-time pairing code for one exact registered project route. The Figma plugin UI asks the user for this code while opened in the matching Figma file. Successful pairing returns a random capability token stored only in plugin session memory and Hub local state.

The token:

- is scoped to one `project_id` and one exact Figma route,
- expires,
- is revocable,
- is never returned by catalog APIs,
- is required for job claim, artifact bytes, and receipt submission.

### 3. Figma Bridge plugin

Create `tools/figma-bridge/` as a support component, not a fourth image-generation Studio.

The plugin:

1. pairs to `http://127.0.0.1:8764`,
2. asks the Hub for the next job for its paired route,
3. downloads exact PNG/JPEG/GIF/WebP bytes from the Hub,
4. verifies SHA-256 before mutation,
5. resolves the registered target node inside the current Figma file,
6. creates an image through the Figma Plugin API,
7. creates one frame under the registered Generated Assets target and applies the image fill,
8. returns created node id, dimensions, content hash, and route identity,
9. marks nothing successful locally until the Hub validates the receipt.

The manifest network allowlist is localhost-only. Production/public plugin packaging must not broaden that domain list.

### 4. Receipt and idempotency

A valid receipt must match the queued job exactly. The Hub rejects wrong project, route, token, hash, media metadata, expired job, unknown node, and duplicate divergent receipts.

After acceptance, the Hub writes an immutable project-local receipt beside the exported delivery metadata. A second identical submission returns the existing verified result; a conflicting second submission fails closed.

Figma failure never deletes or rolls back the project-local image export.

### 5. UX

Primary action is `확정 및 전달`, not ambiguous `다운로드`.

Destination state is independent:

- `PROJECT_SAVED`
- `DOWNLOAD_READY`
- `FIGMA_BRIDGE_REQUIRED`
- `FIGMA_DELIVERY_PENDING`
- `FIGMA_DELIVERED_VERIFIED`
- `FIGMA_DELIVERY_FAILED`

A local browser download is optional and never acts as proof of project save or Figma delivery.

## Security constraints

- Bind only to loopback.
- Browser cannot choose route ids or paths.
- Capability tokens use cryptographically secure randomness and constant-time comparison.
- Pairing and delivery are bounded by expiry and exact project route.
- Artifact bytes are re-hashed immediately before serving.
- Receipt acceptance never trusts plugin-supplied project routing over the queued job.
- No API keys or provider secrets enter the plugin.
- No Git mutation is performed by Figma delivery.
- Failed remote delivery preserves the local export.

## Multi-project behavior

Two projects may have simultaneous pending jobs. A paired plugin instance sees only jobs for its exact project route. A receipt from one route cannot complete another project's job.

## Tauri migration seam

The browser frontend must call the same localhost APIs that a future Tauri webview would call. No Figma Bridge protocol may depend on browser-specific download behavior. When packaging becomes useful, Tauri can wrap the existing web frontend while the Python/local service and plugin protocol remain stable.

## Verification / Implementation Reality Gate

This slice can be marked `IMPLEMENTED_AND_VERIFIED` only when evidence proves:

1. queue/pairing contracts reject cross-project, expired, tampered, and duplicate-divergent inputs;
2. exact image bytes served by Hub match the project export hash;
3. Figma plugin code is constrained to localhost networking and exact target placement;
4. a live Figma smoke creates a temporary real image node under a registered Generated Assets target and readback correlates with the receipt;
5. exact-head CI passes;
6. P0/P1 adversarial findings are zero before merge.

Claim ceilings:

- `delivery packet ready` != Figma uploaded
- `plugin unit tests pass` != live Figma mutation
- `Figma route smoke pass` != local Hub direct bridge pass
- `fixture image delivered` != real AI generation quality
- `Figma delivered` != Godot/game integration

## Rollback

Revert the implementation PR. Existing packet-based project-GPT handoff remains the fallback. Do not delete exported project images or previously verified Figma nodes automatically during rollback.

## External basis

- Figma Plugin API supports read/write access and `figma.createImage(Uint8Array)` for image creation.
- Figma plugin manifests support `networkAccess` restrictions and localhost development/connection domains.
- Tauri 2 supports adding a shell to an existing web frontend, so deferring packaging does not strand the current HTML/JS UI.
