# Base Tool Hub Local-to-Figma Production Delivery Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a project-scoped local delivery queue and Figma Bridge that can move exact accepted raster bytes from Base Tool Hub to the canonical project Figma target and record a verified receipt without exposing arbitrary paths, destinations, or secrets.

**Architecture:** Reuse the existing localhost FastAPI Tool Hub and validated `.asset-vault/` project boundary. Add a focused `FigmaDeliveryService` for pairing, queue state, content hashing, project isolation, and receipts; expose separate browser-CSRF and bridge-bearer HTTP surfaces; add a dependency-free Figma development plugin restricted to localhost. Do not touch open PR #373 files/behavior beyond reading compatibility state.

**Tech Stack:** Python 3.12, FastAPI/Pydantic, pytest, plain Figma Plugin API JavaScript/HTML, GitHub Actions on Ubuntu + Windows.

## Global Constraints

- Baseline is `main@15fcce9d598b7deb0b4c60d2e330f7404a6a8db1`.
- Do not modify open draft PR #373 or duplicate Character/Expression outfit/scene implementation.
- Canonical Figma file/node identity comes only from `docs/operations/PROJECT_FIGMA_TARGET_REGISTRY.json`.
- Reuse the already validated project `.asset-vault/`; no new per-project gitignored root.
- Browser input cannot provide project root, Figma file key, target node, local command, interpreter, provider secret, or bridge bearer token.
- One queued raster is at most 10 MiB and at most 4096×4096.
- Pairing code TTL is 5 minutes; delivery job TTL is 15 minutes.
- A verified delivery is immutable/idempotent.
- Failed remote delivery never deletes accepted local output bytes.
- Full Windows Studio execution and real provider image generation remain separate IRG gates.

---

### Task 1: Delivery queue, pairing, and receipt core

**Files:**
- Create: `tools/tool-hub/src/tool_hub/figma_delivery.py`
- Create: `tools/tool-hub/tests/test_figma_delivery.py`

**Interfaces:**
- Consumes: `ProjectLocator.resolve(project_id)`, `ProjectFigmaRegistry.target_for(project_id)` or equivalent exact registry lookup.
- Produces: `FigmaDeliveryService.create_pairing(project_id)`, `pair(project_id, file_key, pairing_code)`, `enqueue(tool_id, project_id, run_id, image_bytes, media_type)`, `claim_next(token)`, `content(token, delivery_id)`, `finalize(token, delivery_id, receipt)`, `release(token, delivery_id)`.

- [ ] **Step 1: Write failing queue and isolation tests**

```python
from hashlib import sha256
from pathlib import Path

import pytest

from tool_hub.figma_delivery import DeliveryError, FigmaDeliveryService
from tool_hub.projects import ProjectLocator
from test_projects import make_project


def test_pairing_and_delivery_are_project_scoped(tmp_path: Path, figma_registry) -> None:
    a = make_project(tmp_path / "a", "coc-fiction")
    b = make_project(tmp_path / "b", "omenward")
    locator = ProjectLocator(tmp_path / "projects.json")
    locator.register(a, "coc-fiction")
    locator.register(b, "omenward")
    service = FigmaDeliveryService(tmp_path / "runtime", locator, figma_registry)

    code = service.create_pairing("coc-fiction").pairing_code
    token = service.pair("coc-fiction", figma_registry.target_for("coc-fiction").figma_file_key, code).token
    job = service.enqueue("expression-studio", "coc-fiction", "run-1", PNG_1X1, "image/png")

    claimed = service.claim_next(token)
    assert claimed.delivery_id == job.delivery_id
    assert claimed.project_id == "coc-fiction"
    assert claimed.content_sha256 == sha256(PNG_1X1).hexdigest()

    other_code = service.create_pairing("omenward").pairing_code
    other = service.pair("omenward", figma_registry.target_for("omenward").figma_file_key, other_code).token
    with pytest.raises(DeliveryError, match="DELIVERY_SCOPE_MISMATCH"):
        service.content(other, job.delivery_id)
```

Add independent tests for: wrong file key, expired pairing, expired job, duplicate finalize, release/reclaim, changed queued bytes, oversize bytes, invalid raster, cross-project content, wrong target/node receipt, token revocation, and secret-free public views.

- [ ] **Step 2: Run RED in canonical CI**

Create only tests plus a narrow workflow first. Expected: failure because `tool_hub.figma_delivery` does not exist.

- [ ] **Step 3: Implement minimal core**

```python
class DeliveryError(RuntimeError):
    pass

@dataclass(frozen=True)
class DeliveryJob:
    delivery_id: str
    tool_id: str
    project_id: str
    run_id: str
    content_sha256: str
    byte_length: int
    media_type: str
    figma_file_key: str
    generation_area_node_id: str
    state: str

class FigmaDeliveryService:
    def __init__(self, runtime_root: Path, locator: ProjectLocator, registry: ProjectFigmaRegistry, *, clock=time.time): ...
    def create_pairing(self, project_id: str) -> PairingView: ...
    def pair(self, project_id: str, file_key: str, pairing_code: str) -> BridgeSession: ...
    def enqueue(self, tool_id: str, project_id: str, run_id: str, image_bytes: bytes, media_type: str) -> DeliveryJob: ...
    def claim_next(self, token: str) -> DeliveryJob | None: ...
    def content(self, token: str, delivery_id: str) -> bytes: ...
    def finalize(self, token: str, delivery_id: str, receipt: BridgeReceipt) -> DeliveryReceipt: ...
    def release(self, token: str, delivery_id: str) -> DeliveryJob: ...
```

Implementation requirements:
- resolve project before every authority-bearing operation;
- derive target from canonical registry only;
- store queue under `<project>/.asset-vault/tool-hub-delivery/<delivery_id>/`;
- use atomic temp-file + `os.replace` writes;
- re-hash bytes before claim/content/finalize;
- token and pairing code stay only in machine runtime memory/state, never project files;
- validate PNG/JPEG/GIF/WebP and dimensions without adding a new imaging dependency to Tool Hub; use deterministic header parsing for supported formats or reuse an already transitive reviewed validator if available without expanding dependency surface.

- [ ] **Step 4: Run GREEN plus existing Tool Hub tests**

Run in workflow:

```bash
python -m pytest -q tools/tool-hub/tests/test_figma_delivery.py
python -m pytest -q tools/tool-hub/tests
```

Expected: all pass on Ubuntu and Windows.

- [ ] **Step 5: Commit Task 1**

Commit message: `feat(tool-hub): add project-scoped Figma delivery queue`

---

### Task 2: Separate browser and bridge HTTP authority

**Files:**
- Modify: `tools/tool-hub/src/tool_hub/app.py`
- Modify: `tools/tool-hub/src/tool_hub/security.py`
- Modify: `tools/tool-hub/tests/test_api.py`
- Create: `tools/tool-hub/tests/test_figma_bridge_api.py`

**Interfaces:**
- Consumes: Task 1 `FigmaDeliveryService`.
- Produces browser endpoints `/api/figma/pairing/{project_id}`, `/api/figma/status/{project_id}` and bridge endpoints `/bridge/pair`, `/bridge/jobs/next`, `/bridge/jobs/{id}/content`, `/bridge/jobs/{id}/receipt`, `/bridge/jobs/{id}/release`.

- [ ] **Step 1: Write failing authority tests**

```python
def test_browser_cannot_supply_figma_destination(tmp_path: Path) -> None:
    client = client_for(tmp_path)
    response = client.post(
        "/api/figma/pairing/coc-fiction",
        json={"figma_file_key": "attacker", "node_id": "999:999"},
    )
    assert response.status_code == 422


def test_bridge_endpoint_rejects_browser_csrf_as_authority(tmp_path: Path) -> None:
    client = client_for(tmp_path)
    response = client.get("/bridge/jobs/next")
    assert response.status_code == 401


def test_bridge_token_cannot_cross_project(tmp_path: Path) -> None:
    # pair Project A, queue A and B, then prove A token can claim only A.
    ...
```

Also test no absolute path, pairing token, bearer token, or file key leaks from `/api/catalog` and `/api/figma/status`.

- [ ] **Step 2: Run RED workflow**

Expected: 404/missing endpoints and missing bridge auth path.

- [ ] **Step 3: Implement endpoints and bridge auth**

Add request models with `extra="forbid"` and no arbitrary destination fields.

```python
class BridgePairPayload(BaseModel):
    model_config = ConfigDict(extra="forbid")
    project_id: str
    figma_file_key: str
    pairing_code: str
    bridge_version: str

class BridgeReceiptPayload(BaseModel):
    model_config = ConfigDict(extra="forbid")
    created_node_id: str
    created_node_name: str
    target_node_id: str
    content_sha256: str
    bridge_version: str
```

Bridge bearer parsing must use a dedicated helper and must not reuse browser cookies/CSRF.

- [ ] **Step 4: Run GREEN**

```bash
python -m pytest -q tools/tool-hub/tests/test_figma_bridge_api.py tools/tool-hub/tests/test_api.py
python -m pytest -q tools/tool-hub/tests
```

- [ ] **Step 5: Commit Task 2**

Commit message: `feat(tool-hub): expose scoped Figma bridge API`

---

### Task 3: Dependency-free Figma Bridge plugin

**Files:**
- Create: `tools/figma-bridge/manifest.json`
- Create: `tools/figma-bridge/code.js`
- Create: `tools/figma-bridge/ui.html`
- Create: `tools/figma-bridge/README.md`
- Create: `tools/tool-hub/tests/test_figma_plugin_contract.py`

**Interfaces:**
- Consumes: Task 2 bridge HTTP API.
- Produces a Figma development plugin that pairs to localhost, claims one exact project job, writes image bytes below the server-provided canonical target, and submits receipt evidence.

- [ ] **Step 1: Write failing static plugin contract tests**

```python
def test_figma_bridge_manifest_allows_only_local_tool_hub() -> None:
    manifest = json.loads((BASE_ROOT / "tools/figma-bridge/manifest.json").read_text())
    access = manifest["networkAccess"]
    assert access["allowedDomains"] == ["http://127.0.0.1:8764"]
    assert "*" not in json.dumps(access)


def test_plugin_has_no_arbitrary_destination_controls() -> None:
    ui = (BASE_ROOT / "tools/figma-bridge/ui.html").read_text()
    code = (BASE_ROOT / "tools/figma-bridge/code.js").read_text()
    for forbidden in ("figma-file-key-input", "node-id-input", "project-root-input"):
        assert forbidden not in ui + code
```

Also assert manifest points only at repository-local code/UI, plugin uses `figma.clientStorage`, canonical target comes from job data, and no API/provider key vocabulary is present.

- [ ] **Step 2: Run RED**

Expected: plugin files missing.

- [ ] **Step 3: Implement minimal plugin**

`manifest.json`:

```json
{
  "name": "Base Tool Hub Figma Bridge",
  "id": "base-tool-hub-figma-bridge-dev",
  "api": "1.0.0",
  "main": "code.js",
  "ui": "ui.html",
  "editorType": ["figma"],
  "documentAccess": "dynamic-page",
  "networkAccess": {
    "allowedDomains": ["http://127.0.0.1:8764"],
    "reasoning": "Connect only to the developer's local Base Tool Hub for explicitly paired project asset delivery."
  }
}
```

`code.js` owns Figma mutation only; `ui.html` owns fetch/crypto/UI and sends validated bytes to main code via `postMessage`.

Core write shape:

```javascript
const target = await figma.getNodeByIdAsync(job.generation_area_node_id);
if (!target || !("appendChild" in target)) throw new Error("FIGMA_TARGET_UNAVAILABLE");
const image = figma.createImage(new Uint8Array(bytes));
const node = figma.createRectangle();
node.name = job.node_name;
node.resize(job.width, job.height);
node.fills = [{ type: "IMAGE", scaleMode: "FIT", imageHash: image.hash }];
target.appendChild(node);
```

The UI computes SHA-256 over fetched bytes with Web Crypto and refuses mismatch before sending bytes to `code.js`.

- [ ] **Step 4: Run GREEN static tests**

```bash
python -m pytest -q tools/tool-hub/tests/test_figma_plugin_contract.py
```

- [ ] **Step 5: Commit Task 3**

Commit message: `feat(figma): add localhost-only Tool Hub bridge plugin`

---

### Task 4: Tool Hub pairing UX and evidence ceiling

**Files:**
- Modify: `tools/tool-hub/web/index.html`
- Modify: `tools/tool-hub/web/app.js`
- Modify: `tools/tool-hub/web/styles.css`
- Modify: `tools/tool-hub/tests/test_web_contract.py`
- Modify: `tools/tool-hub/README.md`

**Interfaces:**
- Consumes: Task 2 browser pairing/status endpoints.
- Produces user-visible project-specific Figma Bridge setup/status without exposing destination authority.

- [ ] **Step 1: Write failing UI contract tests**

Assert UI contains:
- `Figma Bridge 연결` section;
- `연결 코드 만들기` action;
- registered Figma link rendered from server response only;
- status vocabulary `PAIRING_REQUIRED`, `BRIDGE_PAIRED`, `DELIVERY_PENDING`, `FIGMA_DELIVERED_VERIFIED`;
- no free-form Figma URL/node/path fields;
- evidence text still distinguishes route verified from local bridge delivered.

- [ ] **Step 2: Run RED**

Expected: missing bridge UI contract.

- [ ] **Step 3: Implement minimal project-first UX**

When a registered project is selected, show:

```text
Figma Bridge
상태: PAIRING_REQUIRED
[연결 코드 만들기] [등록된 Figma 열기]
```

Pairing code is shown only after explicit click and is never stored in localStorage.

Do not add the final `확정 및 전달` Studio button yet; that belongs to the later adapter integration after #373 and Windows child gates are available.

- [ ] **Step 4: Run GREEN plus web regression**

```bash
python -m pytest -q tools/tool-hub/tests/test_web_contract.py tools/tool-hub/tests/test_api.py
```

- [ ] **Step 5: Commit Task 4**

Commit message: `feat(tool-hub): add Figma bridge pairing UX`

---

### Task 5: CI, adversarial review, live-smoke contract, and integration boundary

**Files:**
- Create: `.github/workflows/validate-tool-hub-figma-bridge.yml`
- Create: `docs/reviews/2026-08-14-tool-hub-local-figma-delivery-adversarial-review.md`
- Create: `docs/evidence/2026-08-14-tool-hub-local-figma-delivery.md`
- Modify only if required by existing validation contracts: central documentation/registry references.

**Interfaces:**
- Consumes all prior tasks.
- Produces exact-head Windows/Linux CI evidence and explicit IRG claim ceiling.

- [ ] **Step 1: Add focused CI workflow**

Use Ubuntu + Windows Python 3.12. Install only reviewed Tool Hub/base-tool-contract dependencies. Run:

```bash
python -m pytest -q tools/tool-hub/tests/test_figma_delivery.py
python -m pytest -q tools/tool-hub/tests/test_figma_bridge_api.py
python -m pytest -q tools/tool-hub/tests/test_figma_plugin_contract.py
python -m pytest -q tools/tool-hub/tests/test_web_contract.py
```

Then run the complete `tools/tool-hub/tests` suite on at least Ubuntu; preserve existing wider Base required checks through PR.

- [ ] **Step 2: Execute adversarial attack matrix**

Record actual test/evidence result for:
1. arbitrary destination injection;
2. cross-project token;
3. queued-byte tamper;
4. duplicate finalize;
5. missing/drifted target;
6. token/code leakage scan;
7. Figma unavailable while local output remains;
8. two-project concurrency;
9. malformed/oversized raster;
10. browser/static HTML authority escalation.

P0/P1 must be zero before ready-for-review.

- [ ] **Step 3: Open PR linked to #375 and inspect exact-head Actions**

PR body must state:
- dependency on #373 for Character Studio integration;
- no claim of real AI image generation;
- no claim of actual Windows Studio child execution;
- no claim of live bridge delivery until Figma smoke is run.

- [ ] **Step 4: Run live Figma transport smoke if a runnable local bridge instance exists**

Use one deterministic non-secret sample PNG. Prove write/readback/cleanup against one exact registered project target. If local bridge runtime is unavailable in the current environment, record `NOT_RUN` and keep claim at `BRIDGE_IMPLEMENTED_CI_VERIFIED`, not `FIGMA_DELIVERED_VERIFIED`.

- [ ] **Step 5: Regression and merge gate**

Apply `reviewing-and-validating-project-changes`:

```text
contract-check
-> multi-lens-review
-> static-validation
-> runtime-validation where available
-> regression
-> claim-and-intent-verification
-> evidence-report
```

Merge only when:
- exact-head required checks pass;
- unresolved review threads = 0;
- P0/P1 = 0;
- #373 is not modified or overwritten;
- current `main` has not introduced conflicting Tool Hub/Figma delivery authority.

After merge, re-read merged main and update Issue #375 with what is implemented vs still gated.

---

## Post-plan self-review

- Spec coverage: queue, pairing, auth split, plugin, multi-project isolation, UX, CI, adversarial review, IRG, rollback are mapped to Tasks 1–5.
- Scope: Character edit generation and Windows Studio Job Object work are intentionally excluded because they have separate active/dependent work.
- Type consistency: `FigmaDeliveryService` is the single authority consumed by API tasks; Figma destinations are registry-derived everywhere.
- No new project-local runtime root is introduced; `.asset-vault/` is reused.
- No production-code task starts before a failing test/CI RED.
