# Base Tool Hub Local-to-Figma Production Delivery Design

## Goal

Turn the existing Base Tool Hub from a verified local launcher/import workflow into a production delivery loop where the developer can choose a project and tool, create or import visual outputs, select accepted bytes, save those bytes inside only that project, optionally download the same bytes, and deliver the same bytes to the project's canonical Figma `Generated Assets` target with readback evidence.

GitHub remains the canonical source/config/evidence repository. The normal user surface remains the existing localhost Tool Hub launched from the Windows desktop shortcut.

## Authority and overlap

- Issue: `#375 feat(tool-hub): complete local-to-Figma production delivery loop`.
- Baseline: `main@15fcce9d598b7deb0b4c60d2e330f7404a6a8db1`.
- Reuse merged PR #363 for managed project onboarding and no-terminal Windows launch.
- Reuse merged PR #370 for the eight live-verified Figma files and exact target node IDs.
- Do **not** modify, duplicate, or merge around open draft PR #373. It owns the top-level `Base Tool Hub/` suite root and Character/Expression outfit/scene work until completed.
- Reuse the existing Expression/Sprite/QA project isolation, Asset Vault, anchor, export, and delivery contracts.

## Existing-solution-first decision

### Static HTML only — REJECT

Static HTML remains useful as the visible UI, but cannot safely own project filesystem writes, provider secrets, process identity, delivery queues, or remote Figma mutation.

### Existing localhost web app — REUSE / PRIMARY

Keep `HTML/CSS/JS + FastAPI + pythonw + Base Tool Hub.lnk`. The browser stays a thin UI. The local backend owns all authority-bearing operations.

This avoids a rewrite, preserves current project isolation tests, and keeps a future desktop shell optional.

### Tauri shell — DEFERRED PACKAGING OPTION

Tauri may later wrap the same local frontend/backend experience after the workflow is proven. Do not add Rust, signing, updater, or installer complexity in this slice.

## Figma Bridge architecture

A small Figma development/plugin bridge is the independent local write transport. It is not a second Tool Hub and does not contain generation logic.

The bridge follows current Figma Plugin API contracts:

- Plugin `networkAccess` permits only the reviewed localhost Tool Hub origin.
- Image bytes are fetched from localhost only after explicit pairing.
- Raster bytes are inserted with Figma's image API and placed as image fills below the canonical generation target.
- Pairing data is device-local plugin storage, not project/document authority.
- The bridge cannot choose arbitrary file keys or arbitrary target nodes; those remain Base registry authority.

## Data flow

```text
Tool/Studio accepted output bytes
  -> project-scoped accepted export
  -> DeliveryQueue.create_job()
       binds tool_id + project_id + run_id + content_sha256
       binds canonical Figma file key + target node IDs
       stores only an opaque delivery token in browser-visible state
  -> user opens/runs Base Tool Hub Figma Bridge in the registered Figma file
  -> bridge pairs with localhost Hub using one-time pairing code
  -> bridge claims only a job for its exact current Figma file + project route
  -> bridge downloads exact queued bytes from 127.0.0.1
  -> bridge creates image-filled node under canonical Generated Assets target
  -> bridge calculates/returns receipt metadata
  -> Hub validates project/route/job/hash/node identity
  -> project-local FIGMA_DELIVERY_RECEIPT.json is atomically written
  -> job becomes DELIVERED_VERIFIED
```

## Delivery queue

### Identity

Each job is keyed by:

- `delivery_id`: cryptographically random opaque ID
- `tool_id`
- `project_id`
- `run_id`
- `content_sha256`

The user/browser cannot submit a Figma file key or target node ID. Those are loaded from the canonical `PROJECT_FIGMA_TARGET_REGISTRY.json`.

### State machine

```text
QUEUED
  -> CLAIMED
  -> DELIVERED_VERIFIED

QUEUED -> EXPIRED
CLAIMED -> QUEUED       only through bounded retry release
```

A verified job is immutable and cannot be delivered again.

### Expiry

Default job lifetime: 15 minutes. Pairing codes expire after 5 minutes. Tokens are never written into the Git repository or project source files.

### Byte ceiling

One raster delivery is limited to 10 MiB and PNG/JPEG/GIF/WebP inputs accepted by the local validator. Figma's image dimension ceiling is treated as 4096×4096; oversize images fail before claim.

## Pairing and trust boundary

- Pairing is explicit, per Figma file/project route, and revocable.
- Tool Hub creates a one-time pairing code.
- The Figma Bridge supplies the current file identity and code to localhost.
- The Hub returns a scoped bearer token only for that exact project/file route.
- The token can claim/download/submit receipts only for that project.
- Browser CSRF/session credentials and bridge bearer credentials are separate.
- Bridge endpoints accept loopback Host only and require the bridge bearer token; normal browser mutation CSRF does not authorize bridge operations.
- Project A's token must not read, claim, deliver, or acknowledge Project B's queue.

## Project write contract

The delivery queue never invents an arbitrary project path. It resolves the project through `ProjectLocator`, then writes only to a reviewed project-local Tool Hub delivery area.

Initial durable receipt path:

`<project>/.base-tool-hub/delivery/<delivery_id>/FIGMA_DELIVERY_RECEIPT.json`

The project must already treat `.base-tool-hub/` as ignored/local operational state before production enablement. If the exact ignored path is not proven by the project adapter or Git ignore evidence, queue creation fails closed with `PROJECT_DELIVERY_AREA_UNAVAILABLE`.

Accepted Studio exports remain owned by each Studio's current Asset Vault/export contract; this slice does not relocate or delete them.

## Receipt contract

A verified receipt records:

- schema version
- delivery ID
- tool/project/run IDs
- content SHA-256
- byte length and media type
- canonical Figma file key
- canonical generation target node ID
- created Figma node ID
- created node name
- bridge version
- verification timestamp
- state `DELIVERED_VERIFIED`

It never stores API keys, pairing codes, bearer tokens, absolute project paths, or provider secrets.

## HTTP surface

### Browser-authorized endpoints

- `POST /api/figma/pairing/{project_id}` -> create a one-time pairing code and registered Figma URL.
- `GET /api/figma/status/{project_id}` -> redacted pairing/bridge/queue state.

Future Studio handoff endpoint is adapter-owned; this slice provides the queue service API so Expression/Sprite can call it without duplicating queue logic.

### Bridge-authorized endpoints

- `POST /bridge/pair` -> exchange pairing code + current Figma file identity for scoped token.
- `GET /bridge/jobs/next` -> claim next compatible job.
- `GET /bridge/jobs/{delivery_id}/content` -> exact bytes with SHA header.
- `POST /bridge/jobs/{delivery_id}/receipt` -> submit created-node evidence and finalize.
- `POST /bridge/jobs/{delivery_id}/release` -> return a claimed job to queue after a bounded local failure.

Bridge endpoints reject cookies as authority and use `Authorization: Bearer ...` only.

## Figma plugin

Create `tools/figma-bridge/` containing:

- `manifest.json`
- plain JavaScript main plugin code
- minimal UI HTML/JS for pair, deliver, status, retry
- README with one-time Figma development-plugin import instructions
- static contract tests that validate manifest network bounds and forbid arbitrary destination input

No Node build step is required for v1; the plugin stays inspectable and dependency-free.

### Plugin behavior

1. Display current Figma file name and Hub connection state.
2. User enters the one-time pairing code shown by Tool Hub.
3. Bridge pairs and stores only the scoped token in `figma.clientStorage`.
4. `Deliver next` claims one job.
5. Verify job file identity and target node ID.
6. Fetch bytes and verify SHA-256 in plugin UI context before mutation.
7. Resolve exact generation target node.
8. Create a rectangle/frame child sized to image dimensions, fill with image, name with project/run/delivery identity.
9. Submit created node receipt.
10. Show `DELIVERED_VERIFIED` only after Hub accepts the receipt.

If any step before receipt confirmation fails, the local accepted output remains intact.

## UX

The long-term primary action is `확정 및 전달`, with explicit destination status:

- `PROJECT_SAVED`
- `FIGMA_DELIVERED_VERIFIED`
- `DOWNLOAD_READY`

The Tool Hub itself shows Figma bridge pairing status and a button/link to the canonical Figma file. It must not claim `Figma delivered` merely because PR #370 verified the route or because a delivery packet exists.

## Multi-project behavior

- Queue directories/state are keyed by exact project ID.
- Pairing tokens are route-scoped.
- Canonical targets come only from Base registry.
- Two projects may have pending jobs simultaneously.
- A bridge paired to one Figma file sees only that project's jobs.
- Cleanup/retry for one project never traverses another project's queue.

## Windows execution boundary

This slice does not weaken the existing fail-closed Windows Studio child gate. Figma Bridge transport can be implemented and unit-tested independently, but full end-to-end production acceptance still requires the separate Windows Job Object/process-tree/staging work to make visual Studio children runnable on the actual developer PC.

## Real image evidence

Fixture copies and transparent Sprite frames remain insufficient.

Final production claims require real, visibly non-identical samples recording:

- provider/model/config identity
- input hash
- output hashes
- image validity
- requested visual change
- anchor/character consistency review
- project save evidence
- exact Figma node/readback evidence

Sprite additionally requires one real `pose_sequence`, one real `effect_stages`, and GIF/atlas/Godot handoff from the accepted frames.

## Validation

### Automated

- Queue state/expiry/idempotency/hash tests.
- Pairing token scope and revocation tests.
- Cross-project denial tests.
- Wrong file/target/hash receipt rejection.
- Atomic receipt write tests.
- Bridge manifest/CSP/static destination tests.
- Browser API redaction and CSRF tests.
- Existing Tool Hub regression suite.
- Windows/Linux CI for portable queue logic.

### Live Figma smoke

After implementation and before `DELIVERED_VERIFIED` production claim:

- pair the development bridge to one registered test project/file
- enqueue a deterministic non-secret sample PNG
- deliver it to the exact registered generation target
- read back the created node/image through the connected Figma path
- confirm content identity/metadata
- delete only the smoke node
- record evidence with claim ceiling

This live smoke proves bridge transport, not AI image quality.

## Implementation Reality Gate

Do not collapse these claims:

- localhost UI displayed != production tool complete
- project registered != Studio executed
- packet prepared != Figma uploaded
- Figma route verified != local Hub direct delivery
- bridge receipt accepted != image visually approved
- fixture export != real provider generation
- provider output != game integration

## Adversarial review targets

Attack at minimum:

1. Browser tries to override Figma file/node destination.
2. Stolen Project A bridge token tries Project B.
3. Delivery file is changed after queueing.
4. Duplicate receipt/delivery is submitted.
5. Target node drifted/deleted between queue and bridge run.
6. Pairing code/token appears in logs or repository files.
7. Figma is unavailable after project save.
8. Two projects deliver concurrently.
9. Malformed or oversized raster bytes reach Figma.
10. Static HTML attempts to become authority for filesystem/provider/Figma mutation.

## Rollback

The bridge and queue are additive. Reverting the implementation PR restores the current packet-based project-GPT Figma handoff. Existing accepted local outputs are not deleted during rollback, and remote delivery failure never rolls back project-local accepted image bytes.
