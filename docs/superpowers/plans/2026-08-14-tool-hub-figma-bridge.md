# Tool Hub Figma Bridge Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add an authenticated localhost Figma Bridge so a Base Tool Hub export can be delivered as the exact same bytes to the registered project Figma target and closed with a verified receipt.

**Architecture:** Keep `tools/tool-hub` as local delivery authority and add a bounded `tools/figma-bridge` plugin. Tool Hub creates route-bound delivery jobs and short-lived capability tokens; the Figma plugin claims one job, verifies bytes, writes to the registered Generated Assets node, and submits a receipt. The protocol remains browser-shell agnostic for a future Tauri wrapper.

**Tech Stack:** Python 3.12, FastAPI/Pydantic, existing Base Tool Hub project/Figma registry contracts, JavaScript Figma Plugin API, pytest, GitHub Actions.

## Global Constraints

- Do not modify or duplicate open draft PR #373.
- Reuse `docs/operations/PROJECT_FIGMA_TARGET_REGISTRY.json`; browser/plugin input cannot override Figma file/node routes.
- Keep existing executable owners under `tools/*`.
- Do not add Tauri in this slice.
- Bind bridge APIs to the existing loopback Hub only.
- No provider API keys or secrets enter the Figma plugin.
- Figma delivery failure must preserve project-local exports.
- `delivery packet ready` is not a Figma-upload success claim.
- Exact-head CI and adversarial P0/P1=0 are required before merge.

---

### Task 1: Delivery job and pairing domain model

**Files:**
- Create: `tools/tool-hub/src/tool_hub/figma_bridge.py`
- Test: `tools/tool-hub/tests/test_figma_bridge.py`

**Interfaces:**
- Produces: `FigmaBridgeStore`, `DeliveryJob`, `PairingSession`, `DeliveryReceipt`, `BridgeError`.
- Consumes: canonical project/Figma target values passed by Tool Hub service code; no browser-controlled routes.

- [ ] **Step 1: Write failing model/store tests**

Test these behaviors with real temporary files and no mocks:

```python

def test_job_binds_exact_export_hash_and_route(tmp_path): ...

def test_pairing_code_is_one_time_and_project_scoped(tmp_path): ...

def test_expired_pairing_is_rejected(tmp_path): ...

def test_wrong_project_token_cannot_claim_job(tmp_path): ...

def test_served_artifact_rehash_detects_tampering(tmp_path): ...

def test_identical_receipt_is_idempotent_but_conflict_is_rejected(tmp_path): ...
```

The production change that makes these tests pass must be the new `FigmaBridgeStore`; tests must not pass by asserting helper mocks.

- [ ] **Step 2: Run focused RED**

Run in CI/available workspace:

```bash
python -m pytest -q tools/tool-hub/tests/test_figma_bridge.py
```

Expected: collection/import failure because `tool_hub.figma_bridge` does not exist.

- [ ] **Step 3: Implement minimal domain model**

Implement immutable Pydantic/dataclass records with:

```python
class BridgeError(RuntimeError): ...

class FigmaBridgeStore:
    def create_pairing(self, *, project_id: str, target: ProjectFigmaTarget, ttl_seconds: int = 300) -> PairingSession: ...
    def exchange_pairing(self, *, code: str, current_file_key: str) -> PairingSession: ...
    def enqueue(self, *, tool_id: str, project_id: str, run_id: str, export_path: Path, target: ProjectFigmaTarget, media_type: str, ttl_seconds: int = 900) -> DeliveryJob: ...
    def claim_next(self, *, capability_token: str, current_file_key: str) -> DeliveryJob | None: ...
    def artifact_bytes(self, *, capability_token: str, delivery_id: str) -> bytes: ...
    def accept_receipt(self, *, capability_token: str, receipt: DeliveryReceipt) -> DeliveryReceipt: ...
    def revoke(self, *, capability_token: str) -> None: ...
```

Rules:
- secrets from `secrets.token_urlsafe` / `secrets.compare_digest`;
- pairing code single-use;
- capability exact project/file route;
- store absolute paths only in memory/local private state, never public payloads;
- hash export at enqueue and immediately before serve;
- accepted receipt must match delivery id, project id, file key, generation area node id, artifact SHA-256 and byte length;
- identical receipt is idempotent; conflicting receipt fails closed.

- [ ] **Step 4: Run GREEN**

```bash
python -m pytest -q tools/tool-hub/tests/test_figma_bridge.py
```

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add tools/tool-hub/src/tool_hub/figma_bridge.py tools/tool-hub/tests/test_figma_bridge.py
git commit -m "feat(tool-hub): add Figma bridge delivery store"
```

### Task 2: Authenticated Tool Hub bridge API

**Files:**
- Modify: `tools/tool-hub/src/tool_hub/app.py`
- Test: `tools/tool-hub/tests/test_api.py`
- Test: `tools/tool-hub/tests/test_figma_bridge.py`

**Interfaces:**
- Consumes: `FigmaBridgeStore` from Task 1.
- Produces localhost endpoints under `/api/figma-bridge/*`.

- [ ] **Step 1: Write failing API tests**

Add tests for:

```text
POST /api/figma-bridge/pairings
POST /api/figma-bridge/pairings/exchange
GET  /api/figma-bridge/jobs/next
GET  /api/figma-bridge/jobs/{delivery_id}/artifact
POST /api/figma-bridge/jobs/{delivery_id}/receipt
DELETE /api/figma-bridge/pairings/current
```

Assertions:
- browser-side pairing creation accepts only an existing registered `project_id` and never an arbitrary route;
- exchange requires pairing code + exact current Figma file key;
- capability token is returned only by exchange and required as `Authorization: Bearer` thereafter;
- no local filesystem path is returned;
- wrong/missing token receives 401/409 and cannot learn another project's job;
- artifact `Content-Type`, byte length and `ETag`/hash metadata match job values.

- [ ] **Step 2: Run RED**

```bash
python -m pytest -q tools/tool-hub/tests/test_api.py -k figma_bridge
```

Expected: 404 for missing routes.

- [ ] **Step 3: Implement minimal API**

Wire `FigmaBridgeStore` into `create_app`. Reuse the existing project catalog and canonical Figma registry already loaded by Tool Hub. Route creation must resolve targets server-side.

Do not expose arbitrary upload/write endpoints. The API serves only bytes from a server-created delivery job.

- [ ] **Step 4: Run GREEN + existing API regression**

```bash
python -m pytest -q tools/tool-hub/tests/test_api.py tools/tool-hub/tests/test_figma_bridge.py
```

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add tools/tool-hub/src/tool_hub/app.py tools/tool-hub/tests/test_api.py tools/tool-hub/tests/test_figma_bridge.py
git commit -m "feat(tool-hub): expose authenticated Figma bridge API"
```

### Task 3: Figma Bridge plugin contract

**Files:**
- Create: `tools/figma-bridge/README.md`
- Create: `tools/figma-bridge/manifest.json`
- Create: `tools/figma-bridge/code.js`
- Create: `tools/figma-bridge/ui.html`
- Create: `tools/figma-bridge/tests/test_contract.py`

**Interfaces:**
- Consumes: Task 2 localhost endpoints.
- Produces: a development-importable Figma plugin with one pairing UI and one delivery action.

- [ ] **Step 1: Write failing static/behavior contract tests**

Tests must assert:
- manifest editor type includes `figma`;
- network allowlist includes only the exact localhost Hub origin required by the bridge and no wildcard/external domain;
- plugin has no API key strings/provider endpoints;
- code verifies SHA-256 before calling `figma.createImage`;
- code resolves the exact target node id from the job and verifies it is inside the current document;
- code creates a child frame under the registered generation area and applies an IMAGE fill;
- code submits created node id, dimensions, artifact hash/length and route ids as receipt;
- failure closes without submitting success.

- [ ] **Step 2: Run RED**

```bash
python -m pytest -q tools/figma-bridge/tests/test_contract.py
```

Expected: FAIL because plugin files do not exist.

- [ ] **Step 3: Implement plugin**

`manifest.json`:

```json
{
  "name": "Base Tool Hub Figma Bridge",
  "api": "1.0.0",
  "main": "code.js",
  "ui": "ui.html",
  "editorType": ["figma"],
  "documentAccess": "dynamic-page",
  "networkAccess": {
    "allowedDomains": ["http://127.0.0.1:8764"],
    "reasoning": "Connect only to the developer-owned Base Tool Hub running on localhost."
  }
}
```

`ui.html` owns network fetch and pairing token in memory. `code.js` owns Figma document mutation. Communicate only through `figma.ui.postMessage` / `figma.ui.onmessage`.

Delivery mutation sequence:

```javascript
const bytes = new Uint8Array(message.bytes);
const digest = await sha256Hex(bytes); // UI can compute before passing if Web Crypto is unavailable in main
if (digest !== job.artifact_sha256) throw new Error("artifact hash mismatch");
const target = await figma.getNodeByIdAsync(job.generation_area_node_id);
if (!target || target.type !== "FRAME") throw new Error("registered target unavailable");
const image = figma.createImage(bytes);
const frame = figma.createFrame();
frame.name = `Base Tool Hub ${job.run_id}`;
frame.resize(job.width, job.height);
frame.fills = [{ type: "IMAGE", scaleMode: "FIT", imageHash: image.hash }];
target.appendChild(frame);
```

Use actual image dimensions supplied/validated by Hub; never invent dimensions from browser input.

- [ ] **Step 4: Run GREEN**

```bash
python -m pytest -q tools/figma-bridge/tests/test_contract.py
```

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add tools/figma-bridge
git commit -m "feat(figma): add localhost Tool Hub bridge plugin"
```

### Task 4: Export-to-delivery handoff and immutable receipt

**Files:**
- Modify: `tools/tool-hub/src/tool_hub/figma_bridge.py`
- Modify: `tools/tool-hub/src/tool_hub/app.py`
- Test: `tools/tool-hub/tests/test_figma_bridge.py`
- Test: `tools/tool-hub/tests/test_api.py`

**Interfaces:**
- Consumes: project-scoped exported artifact paths from existing Studio handoff contracts.
- Produces: project-local `FIGMA_DELIVERY_RECEIPT.json` written only after receipt verification.

- [ ] **Step 1: Add failing end-to-end contract test with fixture PNG**

Construct two temporary project roots and two registered Figma targets. Enqueue one non-empty PNG per project. Pair two capabilities. Verify:

- each plugin session claims only its own job;
- served bytes match the exact PNG hash;
- project A receipt cannot close project B;
- accepted receipt writes only inside project A's reviewed delivery metadata directory;
- Figma failure leaves the source PNG intact;
- repeat identical receipt returns same verified record without duplicate local receipt mutation.

- [ ] **Step 2: Run RED**

```bash
python -m pytest -q tools/tool-hub/tests/test_figma_bridge.py -k receipt
```

Expected: failure because receipt persistence is absent.

- [ ] **Step 3: Implement receipt persistence**

Use Base safe-staging helpers and atomic replace semantics already used by the Studios. Persist only public evidence fields; never capability tokens or absolute paths.

Receipt status must be exactly `FIGMA_DELIVERED_VERIFIED` after validation.

- [ ] **Step 4: Run GREEN + cross-project regression**

```bash
python -m pytest -q tools/tool-hub/tests/test_figma_bridge.py tools/tool-hub/tests/test_api.py
```

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add tools/tool-hub/src/tool_hub/figma_bridge.py tools/tool-hub/src/tool_hub/app.py tools/tool-hub/tests
git commit -m "feat(tool-hub): persist verified Figma delivery receipts"
```

### Task 5: Hub UX and explicit destination states

**Files:**
- Modify: `tools/tool-hub/web/index.html`
- Modify: `tools/tool-hub/web/app.js`
- Test: `tools/tool-hub/tests/test_web_contract.py`

**Interfaces:**
- Consumes: bridge API from Task 2 and existing project/tool catalog.
- Produces: project-first `확정 및 전달` flow and independent destination status display.

- [ ] **Step 1: Write failing web contract tests**

Require UI strings/state keys:

```text
확정 및 전달
PROJECT_SAVED
DOWNLOAD_READY
FIGMA_BRIDGE_REQUIRED
FIGMA_DELIVERY_PENDING
FIGMA_DELIVERED_VERIFIED
FIGMA_DELIVERY_FAILED
```

Assert the browser does not expose controls for arbitrary filesystem path, arbitrary Figma URL, file key, or node id.

- [ ] **Step 2: Run RED**

```bash
python -m pytest -q tools/tool-hub/tests/test_web_contract.py
```

Expected: missing primary action/status contract.

- [ ] **Step 3: Implement minimal UI**

Keep project selector first, tool selector second. Display Figma pairing instructions/status only for registered projects. `내 PC에도 다운로드` remains optional and cannot drive Figma state.

- [ ] **Step 4: Run GREEN**

```bash
python -m pytest -q tools/tool-hub/tests/test_web_contract.py tools/tool-hub/tests/test_api.py
```

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add tools/tool-hub/web tools/tool-hub/tests/test_web_contract.py
git commit -m "feat(tool-hub): add explicit save and Figma delivery UX"
```

### Task 6: Focused CI, live Figma smoke evidence, and adversarial review

**Files:**
- Create: `.github/workflows/validate-tool-hub-figma-bridge.yml`
- Create: `docs/reviews/2026-08-14-tool-hub-figma-bridge-adversarial-review.md`
- Create after live smoke: `docs/evidence/2026-08-14-tool-hub-figma-bridge-live-smoke.json`
- Modify only if required by canonical docs: `tools/tool-hub/README.md`, `docs/CHANGELOG.md`

**Interfaces:**
- Consumes: all previous tasks.
- Produces: exact-head automated evidence plus a bounded live-smoke record.

- [ ] **Step 1: Add focused GitHub Actions workflow**

Windows + Ubuntu jobs run:

```bash
python -m pytest -q tools/tool-hub/tests/test_figma_bridge.py tools/tool-hub/tests/test_api.py tools/tool-hub/tests/test_web_contract.py tools/figma-bridge/tests/test_contract.py
```

Do not add paid provider calls.

- [ ] **Step 2: Open draft PR and observe exact RED/GREEN history as applicable**

Record workflow run ids and head SHA. Do not interpret unrelated open PR checks as this branch's evidence.

- [ ] **Step 3: Live Figma smoke**

Using one registered non-production smoke-safe Generated Assets target and a deterministic sample PNG:

1. start/verify local Hub bridge on actual Windows path;
2. import the development Figma Bridge plugin;
3. pair exact project;
4. enqueue exported sample PNG;
5. claim and deliver through plugin;
6. verify resulting node exists under registered target;
7. read back the image/node through the connected Figma inspection path;
8. compare project hash, served hash, receipt hash and readback identity;
9. delete only the temporary smoke node if it is explicitly marked smoke/test;
10. record exact node id and cleanup result in evidence JSON.

If actual Windows/plugin execution cannot be performed in the current environment, record `NOT_RUN_PLATFORM` and do not promote the IRG verdict.

- [ ] **Step 4: Adversarial review**

Attack at minimum:

- route spoofing
- project cross-talk
- path traversal
- token theft/replay
- expired pairing/job
- artifact mutation after enqueue
- duplicate/divergent receipt
- wrong Figma file open
- wrong target node type
- plugin external-network expansion
- hidden remote mutation behind download
- rollback deleting local outputs
- false `DELIVERED` claims before receipt

Document `attack -> validate critique -> minimal correction -> regression recheck`. P0/P1 must be zero.

- [ ] **Step 5: Run full relevant regressions and PR checks**

At minimum:

```bash
python -m pytest -q tools/tool-hub/tests tools/figma-bridge/tests tests/test_tool_registry_contract.py
```

Plus required repository checks on exact PR head.

- [ ] **Step 6: Ready/merge only after evidence ceiling is met**

Merge conditions:

- exact-head required checks PASS;
- unresolved review threads = 0;
- P0/P1 = 0;
- no overlap/mutation of open PR #373;
- live bridge smoke = PASS for any claim of actual direct local-to-Figma delivery.

If live smoke remains `NOT_RUN_PLATFORM`, keep the PR unmerged or merge only with an explicitly narrower non-production claim approved by the user; do not call direct delivery verified.

- [ ] **Step 7: Post-merge IRG**

Re-read merged `main` and report:

- actual changed files;
- exact merged SHA;
- CI evidence;
- live Figma evidence;
- verified vs unverified claims;
- rollback commit/PR path;
- next independent gate: Windows Studio child execution and real provider sample generation.
