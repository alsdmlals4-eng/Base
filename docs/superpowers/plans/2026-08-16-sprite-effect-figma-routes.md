# Dedicated Sprite Action / Effect Figma Routes Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add reviewed `Sprite Action Runs` and `Effect Runs` destinations to all eight registered Figma projects, register 24 exact project/tool routes in Base, and enable fail-closed same-SHA Sprite/Effect atlas delivery through the existing localhost Tool Hub bridge.

**Architecture:** Keep the existing project Figma registry, tool-route registry, and hidden project markers as the only mutation authority. Create two sibling Figma destinations per project, then let an authenticated Sprite Studio child request only a route derived from its server-owned run mode. Sprite confirmation sends the verified exported atlas PNG; Tool Hub validates tool, route, project, registry, node, and SHA before using the existing bridge queue/receipt lifecycle.

**Tech Stack:** Python 3.12, FastAPI, Pydantic, pytest/unittest, Base `base-tool-contracts`, Tool Hub/Figma Bridge, Sprite Animation Studio, Figma Plugin API, GitHub Actions on Ubuntu and Windows.

## Global Constraints

- `ZERO_INCREMENTAL_COST_REQUIRED`: no new paid API, API key, metered provider, or mandatory paid dependency.
- Preserve `subscription_handoff_import` + `CHATGPT_INCLUDED`; the normal subscription path keeps `provider_call_made=false`.
- Start implementation from latest completed `main`; do not modify stale/open owner PR branches. Use `BASE_COPY_INTEGRATION_STANDING_AUTHORIZATION_2026_08_16` for approved overlap.
- Keep all existing `Expression Runs` nodes and hidden `Base Tool Hub Route · {project_id}` markers unchanged.
- Never route Sprite/Effect output to generic `Generated Assets` or `Expression Runs` as fallback.
- Do not commit a new Sprite/Effect route as `READY_FOR_DELIVERY` until all 16 Figma frames have been created or safely reused and read back.
- Browser/project input is not Figma route authority. Sprite route identity comes from server-owned `RunRecord.request.mode`.
- `pose_sequence` and `sprite_action` map to `sprite_action_runs`; `effect_stages` maps to `effect_runs`; `expression_variation` remains delivery-blocked in this slice.
- The confirmed Sprite/Effect payload is the exact verified exported atlas PNG.
- Same run + same route + same atlas SHA is idempotent. Same run + changed route or bytes fails closed.
- `PROJECT_ASSET_APPROVED` is not granted.
- Cloud Figma/CI evidence does not prove user-PC execution, real ChatGPT Pro quality, localhost Bridge receipt, or Godot consumption.

## Files

**Create**
- `tools/base-tool-contracts/src/base_tool_contracts/hub_delivery.py`
- `tools/sprite-animation-studio/tests/test_hub_delivery.py`
- `docs/evidence/2026-08-16-sprite-effect-figma-route-readback.md`

**Modify**
- `tools/base-tool-contracts/src/base_tool_contracts/__init__.py`
- `tools/base-tool-contracts/src/base_tool_contracts/figma_tool_routing.py`
- `tools/expression-studio/src/expression_studio/hub_delivery.py`
- `tools/tool-hub/src/tool_hub/figma_delivery.py`
- `tools/tool-hub/src/tool_hub/studio_delivery_api.py`
- `tools/tool-hub/tests/test_figma_exact_tool_route.py`
- `tools/tool-hub/tests/test_studio_delivery_trust.py`
- `tools/sprite-animation-studio/src/sprite_animation_studio/service.py`
- `tools/sprite-animation-studio/src/sprite_animation_studio/app.py`
- `tools/sprite-animation-studio/web/index.html`
- `tools/sprite-animation-studio/web/app.js`
- `tools/sprite-animation-studio/README.md`
- `tools/sprite-animation-studio/tests/test_docs_contract.py`
- `docs/operations/PROJECT_FIGMA_TOOL_ROUTE_REGISTRY.json`
- `tests/test_tool_hub_subscription_production_contract.py`
- `.github/workflows/validate-provisional-figma-integration.yml`

---

### Task 1: Fork latest main and establish TDD RED

**Interfaces:** Produces implementation branch `feat/sprite-effect-figma-routes-20260816`. PR #451 becomes read-only design/plan provenance after handoff.

- [ ] **Step 1: Create the implementation branch from exact latest completed `main`**

Re-read Base `main` and active PR changed paths. Create `feat/sprite-effect-figma-routes-20260816` from that exact SHA and copy the approved spec and plan blobs from #451. Do not push implementation commits to #451.

- [ ] **Step 2: Make the root contract require 24 routes**

In `tests/test_tool_hub_subscription_production_contract.py` replace the old 8-route/absent-Sprite assertions with:

```python
expected_route_names = {
    "character_expression_runs": "Expression Runs",
    "sprite_action_runs": "Sprite Action Runs",
    "effect_runs": "Effect Runs",
}
self.assertEqual(8, len(projects))
self.assertEqual(24, len(routes))
self.assertEqual(
    {(project_id, route_id) for project_id in projects for route_id in expected_route_names},
    {(entry["project_id"], entry["tool_route_id"]) for entry in routes},
)
for route in routes:
    project = projects[route["project_id"]]
    self.assertEqual(project["figma_file_key"], route["figma_file_key"])
    self.assertEqual(project["generation_area_node_id"], route["parent_node_id"])
    self.assertEqual(expected_route_names[route["tool_route_id"]], route["destination_name"])
```

Also assert each project's three destination IDs are mutually distinct and distinct from its parent and marker.

- [ ] **Step 3: Define RED Tool Hub route tests**

Add to `tools/tool-hub/tests/test_figma_exact_tool_route.py`:

```python
def test_sprite_action_delivery_binds_only_sprite_action_destination(tmp_path: Path) -> None:
    service, _ = service_for(tmp_path, "omenward")
    job = service.enqueue(
        "sprite-animation-studio", "omenward", "run-sprite-action",
        png_bytes(), "image/png", tool_route_id="sprite_action_runs",
    )
    assert job.tool_route_id == "sprite_action_runs"
    assert job.target_node_name == "Sprite Action Runs"


def test_effect_delivery_binds_only_effect_destination(tmp_path: Path) -> None:
    service, _ = service_for(tmp_path, "omenward")
    job = service.enqueue(
        "sprite-animation-studio", "omenward", "run-effect",
        png_bytes(), "image/png", tool_route_id="effect_runs",
    )
    assert job.tool_route_id == "effect_runs"
    assert job.target_node_name == "Effect Runs"
```

Add tests that Sprite rejects `character_expression_runs` and an unknown route, and that same run + same bytes + different route raises `DELIVERY_RUN_ROUTE_MISMATCH`.

- [ ] **Step 4: Define RED child-auth route tests**

Add this helper to `test_studio_delivery_trust.py`:

```python
def _authorize_sprite_child(monkeypatch: pytest.MonkeyPatch) -> None:
    def authorize(self: ProcessSupervisor, token: str) -> tuple[str, str]:
        if token != _PRIVATE_TOKEN:
            raise LaunchError("studio delivery credential is invalid")
        return ("sprite-animation-studio", "coc-fiction")
    monkeypatch.setattr(ProcessSupervisor, "authorize_delivery_token", authorize)
```

Assert missing route and Character route both return HTTP 409 `DELIVERY_TOOL_ROUTE_UNAVAILABLE`; valid `sprite_action_runs` and `effect_runs` return the matching route and target name.

- [ ] **Step 5: Define RED Sprite confirmed-atlas tests**

Create `tools/sprite-animation-studio/tests/test_hub_delivery.py` with a complete sender:

```python
class RecordingSender:
    def __init__(self) -> None:
        self.calls: list[tuple[str, bytes, str, str | None]] = []
        self.last: dict[str, object] | None = None

    def __call__(self, run_id: str, image_bytes: bytes, media_type: str,
                 tool_route_id: str | None = None) -> dict[str, object]:
        self.calls.append((run_id, image_bytes, media_type, tool_route_id))
        target = {
            "sprite_action_runs": "Sprite Action Runs",
            "effect_runs": "Effect Runs",
        }[str(tool_route_id)]
        self.last = {
            "status": "QUEUED",
            "delivery_id": "1" * 32,
            "tool_id": "sprite-animation-studio",
            "project_id": "coc-fiction",
            "run_id": run_id,
            "content_sha256": hashlib.sha256(image_bytes).hexdigest(),
            "tool_route_id": tool_route_id,
            "target_node_name": target,
            "bridge_state": "BRIDGE_PAIRED",
            "delivery_state": "DELIVERY_PENDING",
            "figma_url": "https://www.figma.com/design/PEa5zDbPHll3eHiNKX0e1k/example",
        }
        return dict(self.last)

    def status(self, delivery_id: str) -> dict[str, object]:
        assert self.last is not None
        assert delivery_id == self.last["delivery_id"]
        verified = dict(self.last)
        verified["status"] = "DELIVERED_VERIFIED"
        verified["bridge_state"] = "BRIDGE_PAIRED"
        verified["delivery_state"] = "FIGMA_DELIVERED_VERIFIED"
        return verified
```

Tests require `pose_sequence` and `sprite_action` to use `sprite_action_runs`, `effect_stages` to use `effect_runs`, `expression_variation` to return 409 without a sender call, payload bytes to equal the exported atlas, payload SHA to equal `record.export_output_sha256["atlas"]`, and atlas tamper to fail before sender invocation.

- [ ] **Step 6: Wire RED into Ubuntu and Windows CI**

Extend `.github/workflows/validate-provisional-figma-integration.yml` paths with `tools/base-tool-contracts/**`, `tools/sprite-animation-studio/**`, and `tests/test_tool_hub_subscription_production_contract.py`. Install:

```bash
python -m pip install -e './tools/base-tool-contracts[dev]' -e './tools/tool-hub[dev]' -e './tools/sprite-animation-studio[dev]'
```

Add `test_studio_delivery_trust.py`, `tools/sprite-animation-studio/tests/test_hub_delivery.py`, and the root production contract to the pytest command on both OSes.

- [ ] **Step 7: Run RED and commit**

```bash
python -m pytest -q \
  tools/tool-hub/tests/test_figma_exact_tool_route.py \
  tools/tool-hub/tests/test_studio_delivery_trust.py \
  tools/sprite-animation-studio/tests/test_hub_delivery.py \
  tests/test_tool_hub_subscription_production_contract.py
```

Expected failures are limited to the 8-entry registry, absent route-aware Tool Hub API, and absent Sprite confirm-delivery lifecycle. Reproduce unrelated failures on current `main` before proceeding.

Commit message:

```text
test: define dedicated sprite and effect delivery routes
```

---

### Task 2: Create or reuse and read back all 16 Figma frames

**Interfaces:** Produces `figma_route_nodes[project_id][route_id] -> actual node_id` for 16 nodes. Task 3 is blocked until all 16 are valid.

- [ ] **Step 1: Load Figma write guidance and preflight exact authority**

Use these exact tuples:

```text
coc-fiction | PEa5zDbPHll3eHiNKX0e1k | parent 12:3 | Expression 15:2 | marker 23:2
ten-paces-hidden-moves | pVQ2e6aK45iL8BLBJWDSw4 | parent 22:3 | Expression 28:2 | marker 38:2
ninja-survival | xNm1xbYPftEaAE2jOENlvt | parent 12:3 | Expression 15:2 | marker 20:2
switchy-express-cargo-puzzle | QMbylbdAi96PGSdHIT3AGa | parent 11:3 | Expression 14:2 | marker 19:2
urban-legend | Z7J3eLeavEytKN20H4HfoP | parent 11:3 | Expression 14:2 | marker 19:2
grimoire-how-to-rewrite-the-world | AdOGNMp61AZSMMvBVxsVBd | parent 8:3 | Expression 11:2 | marker 16:2
blacksmith | xy6W4ga6ldkF3TvP0eRmtN | parent 13:3 | Expression 18:2 | marker 24:2
omenward | IhxUJaS6ik6MpBzdxt6o8D | parent 10:3 | Expression 13:2 | marker 19:2
```

Abort a file if parent, Expression node, or marker drifts in ID/name/type/parent.

- [ ] **Step 2: Retry-safely clone the existing Expression frame**

For each file pass its tuple as `cfg` to this Figma Plugin operation:

```javascript
const parent = await figma.getNodeByIdAsync(cfg.parentId);
const expression = await figma.getNodeByIdAsync(cfg.expressionId);
const marker = await figma.getNodeByIdAsync(cfg.markerId);
if (!parent || parent.type !== "FRAME" || parent.name !== "Generated Assets") throw new Error("parent drift");
if (!expression || expression.type !== "FRAME" || expression.parent !== parent || expression.name !== "Expression Runs") throw new Error("expression drift");
if (!marker || marker.type !== "FRAME" || marker.parent !== parent || marker.name !== `Base Tool Hub Route · ${cfg.projectId}`) throw new Error("marker drift");

async function loadTextFonts(text) {
  if (text.characters.length === 0) return;
  for (const font of text.getRangeAllFontNames(0, text.characters.length)) await figma.loadFontAsync(font);
}

async function ensureRoute(name, y, note) {
  const matches = parent.children.filter(node => node.name === name);
  if (matches.length > 1) throw new Error(`duplicate ${name}`);
  const frame = matches.length === 1 ? matches[0] : expression.clone();
  if (frame.type !== "FRAME") throw new Error(`${name} type drift`);
  if (matches.length === 0) parent.appendChild(frame);
  frame.name = name;
  frame.x = 40;
  frame.y = y;
  frame.resize(1360, 148);
  const texts = frame.findAll(node => node.type === "TEXT");
  if (texts.length < 2) throw new Error(`${name} presentation drift`);
  await loadTextFonts(texts[0]);
  await loadTextFonts(texts[1]);
  texts[0].characters = name;
  texts[1].characters = note;
  return frame;
}

const sprite = await ensureRoute("Sprite Action Runs", 408,
  "Base Tool Hub exact destination for reviewed sprite action and pose-sequence atlas deliveries.");
const effect = await ensureRoute("Effect Runs", 576,
  "Base Tool Hub exact destination for reviewed effect-stage atlas deliveries.");
return JSON.stringify({sprite_action_runs: sprite.id, effect_runs: effect.id});
```

- [ ] **Step 3: Read back and record evidence**

Each new node must be `FRAME`, under the exact parent, with exact name. Sprite geometry is `x=40,y=408,w=1360,h=148`; Effect geometry is `x=40,y=576,w=1360,h=148`. Require one canonical sibling of each name and unchanged marker.

Create `docs/evidence/2026-08-16-sprite-effect-figma-route-readback.md` with 8 rows containing project ID, file key, parent, marker, actual Sprite node ID, actual Effect node ID, and `PASS`. Record the preflight Base SHA and `LOCALHOST_BRIDGE_RECEIPT: NOT_RUN`.

- [ ] **Step 4: Gate and commit evidence**

Require 8 rows, 16 non-empty new IDs, and uniqueness across parent/marker/Expression/Sprite/Effect IDs per project. If incomplete, keep the Base registry at 8 entries.

```bash
git add docs/evidence/2026-08-16-sprite-effect-figma-route-readback.md
git commit -m "docs: record reviewed sprite and effect Figma route nodes"
```

---

### Task 3: Expand the canonical registry to 24 routes

- [ ] **Step 1: Add two entries per project using Task 2 IDs**

For each project copy file key, parent fields, marker fields, and marker name from its existing Character entry. Add `sprite_action_runs` with the observed Sprite node ID and name `Sprite Action Runs`, and `effect_runs` with the observed Effect node ID and name `Effect Runs`. Mark both `READY_FOR_DELIVERY`. Keep Character entries semantically unchanged.

- [ ] **Step 2: Reject duplicate active destinations within a project**

Add to `ProjectFigmaToolRouteRegistry.__init__`:

```python
project_destinations: dict[str, set[str]] = {}
for entry in document.entries:
    if entry.delivery_status == "ARCHIVED":
        continue
    destinations = project_destinations.setdefault(entry.project_id, set())
    if entry.destination_node_id in destinations:
        raise ValueError("active Figma tool routes for one project must use distinct destinations")
    destinations.add(entry.destination_node_id)
```

- [ ] **Step 3: Test and commit**

```bash
python -m pytest -q tests/test_tool_hub_subscription_production_contract.py \
  tools/tool-hub/tests/test_figma_exact_tool_route.py
```

Commit message:

```text
feat: register dedicated sprite and effect Figma routes
```

---

### Task 4: Enforce authenticated tool-to-route ownership in Tool Hub

**Interface:** `FigmaDeliveryService.enqueue(tool_id, project_id, run_id, image_bytes, media_type, *, tool_route_id: str | None = None) -> DeliveryJob`, with the same optional keyword on `enqueue_idempotent`.

- [ ] **Step 1: Add a fixed allowlist**

```python
_TOOL_ROUTE_IDS = {
    "expression-studio": frozenset({"character_expression_runs"}),
    "sprite-animation-studio": frozenset({"sprite_action_runs", "effect_runs"}),
}


def _requested_route_id(tool_id: str, requested: str | None) -> str:
    allowed = _TOOL_ROUTE_IDS.get(tool_id)
    if allowed is None:
        raise DeliveryError("DELIVERY_TOOL_ROUTE_UNAVAILABLE")
    if requested is None:
        if tool_id == "expression-studio":
            return "character_expression_runs"
        raise DeliveryError("DELIVERY_TOOL_ROUTE_UNAVAILABLE")
    if requested not in allowed:
        raise DeliveryError("DELIVERY_TOOL_ROUTE_UNAVAILABLE")
    return requested
```

Make `_resolve_tool_route` resolve only the resulting route ID.

- [ ] **Step 2: Bind route to idempotency and recovery**

Compare the requested route with every matching stored job before reuse. Raise `DELIVERY_RUN_ROUTE_MISMATCH` if route differs and preserve `DELIVERY_RUN_CONTENT_MISMATCH` for changed bytes. `_assert_current_job_route` and receipt recovery resolve using `job.tool_route_id`. Only legacy Expression jobs may default missing route identity to `character_expression_runs`; a recovered Sprite job without stored route identity is invalid.

- [ ] **Step 3: Add private route header handling to the internal POST**

In `studio_delivery_api.py` import `Header` and add:

```python
_ROUTE_ID = re.compile(r"^[a-z0-9]+(?:_[a-z0-9]+)*$")


def _requested_route(tool_id: str, value: str | None) -> str | None:
    if value is not None and _ROUTE_ID.fullmatch(value) is None:
        raise HTTPException(status_code=409, detail="DELIVERY_TOOL_ROUTE_UNAVAILABLE")
    if tool_id == "expression-studio":
        if value not in {None, "character_expression_runs"}:
            raise HTTPException(status_code=409, detail="DELIVERY_TOOL_ROUTE_UNAVAILABLE")
        return value
    if tool_id == "sprite-animation-studio":
        if value not in {"sprite_action_runs", "effect_runs"}:
            raise HTTPException(status_code=409, detail="DELIVERY_TOOL_ROUTE_UNAVAILABLE")
        return value
    raise HTTPException(status_code=409, detail="DELIVERY_TOOL_ROUTE_UNAVAILABLE")
```

The POST accepts `x_base_tool_route: str | None = Header(default=None, alias="X-Base-Tool-Route")` and passes the validated route to `enqueue_idempotent`. The status endpoint accepts no route header and returns the stored route.

- [ ] **Step 4: Test and commit**

```bash
python -m pytest -q tools/tool-hub/tests/test_figma_exact_tool_route.py \
  tools/tool-hub/tests/test_studio_delivery_trust.py \
  tools/tool-hub/tests/test_figma_delivery.py \
  tools/tool-hub/tests/test_figma_delivery_hardening.py \
  tools/tool-hub/tests/test_figma_delivery_concurrency.py
```

Commit message:

```text
feat(tool-hub): enforce exact sprite and effect delivery routes
```

---

### Task 5: Share the loopback client and add Sprite confirmed-atlas delivery

**Interfaces:** Shared sender signature is `__call__(run_id: str, image_bytes: bytes, media_type: str, tool_route_id: str | None = None) -> dict[str, object]`; `status(delivery_id: str) -> dict[str, object]`. Sprite service exposes `delivery_route_id(run_id: str) -> str`.

- [ ] **Step 1: Promote the Expression Hub client into `base-tool-contracts`**

Preserve loopback-only origin validation, no-proxy opener, child token checks, 5-second timeout, 64-KiB response cap, strict JSON response, and existing environment variables. Define the protocol without an empty body:

```python
class HubDeliverySender(Protocol):
    def __call__(self, run_id: str, image_bytes: bytes, media_type: str,
                 tool_route_id: str | None = None) -> dict[str, object]:
        raise NotImplementedError

    def status(self, delivery_id: str) -> dict[str, object]:
        raise NotImplementedError
```

Concrete client request:

```python
def __call__(self, run_id: str, image_bytes: bytes, media_type: str,
             tool_route_id: str | None = None) -> dict[str, object]:
    if _RUN_ID.fullmatch(run_id) is None:
        raise HubDeliveryError("delivery run identity is invalid")
    if media_type != "image/png" or not isinstance(image_bytes, bytes) or not image_bytes:
        raise HubDeliveryError("delivery content is invalid")
    extra_headers: dict[str, str] = {}
    if tool_route_id is not None:
        if re.fullmatch(r"[a-z0-9]+(?:_[a-z0-9]+)*", tool_route_id) is None:
            raise HubDeliveryError("delivery tool route identity is invalid")
        extra_headers["X-Base-Tool-Route"] = tool_route_id
    return self._json_request(
        f"/internal/studio-delivery/{quote(run_id, safe='')}",
        method="POST",
        data=image_bytes,
        content_type="image/png",
        extra_headers=extra_headers,
    )
```

Add `extra_headers: dict[str, str] | None = None` to `_json_request` and merge only those bounded headers after Authorization/Accept/Content-Type.

- [ ] **Step 2: Preserve Expression compatibility**

Replace `tools/expression-studio/src/expression_studio/hub_delivery.py` with:

```python
from base_tool_contracts.hub_delivery import (
    HubDeliveryError,
    HubDeliverySender,
    LocalHubDeliveryClient,
    sender_from_environment,
)

__all__ = [
    "HubDeliveryError", "HubDeliverySender", "LocalHubDeliveryClient", "sender_from_environment",
]
```

Export the same names from `base_tool_contracts.__init__`. Existing three-argument Expression calls keep the only allowed default `character_expression_runs` route.

- [ ] **Step 3: Add server-owned Sprite mode mapping**

```python
_SPRITE_DELIVERY_ROUTES = {
    "pose_sequence": "sprite_action_runs",
    "sprite_action": "sprite_action_runs",
    "effect_stages": "effect_runs",
}


def delivery_route_id(self, run_id: str) -> str:
    record = self.get_run(run_id)
    try:
        return _SPRITE_DELIVERY_ROUTES[record.request.mode]
    except KeyError as error:
        raise RunBlockedError("DELIVERY_TOOL_ROUTE_UNAVAILABLE") from error
```

No Sprite endpoint accepts route ID in body or query.

- [ ] **Step 4: Add Sprite `confirm-delivery`**

`create_app` gains `hub_delivery_sender: HubDeliverySender | None = None`, resolves `sender_from_environment()` when absent, and keeps lock-protected confirmation state. The endpoint has no body and requires an exported run:

```python
record = service.get_run(run_id)
if record.status != "exported" or record.export is None:
    raise RunBlockedError("an exported run is required before confirmation")
service.prepare_figma_delivery(run_id)
route_id = service.delivery_route_id(run_id)
expected_sha256 = record.export_output_sha256.get("atlas")
if expected_sha256 is None:
    raise RunBlockedError("confirmed atlas hash evidence is unavailable")
atlas_bytes = _read_staged_file(project_root, record.export.atlas, expected_sha256=expected_sha256)
if sender is None:
    raise HubDeliveryError("Tool Hub confirmed delivery is unavailable")
delivery = sender(run_id, atlas_bytes, "image/png", route_id)
```

Normalize only when returned tool/project/run/SHA/route/target match the confirmed run. Require target `Sprite Action Runs` for `sprite_action_runs`, target `Effect Runs` for `effect_runs`, stable delivery ID, consistent bridge/delivery states, and an HTTPS Figma design URL.

- [ ] **Step 5: Add status refresh and confirmed atlas download**

Implement `GET /api/runs/{run_id}/delivery-status` and `GET /api/runs/{run_id}/confirmed-download`. Status re-reads the atlas at cached SHA before calling `sender.status(delivery_id)` and rejects identity drift. Download returns exactly the same atlas with `X-Content-SHA256`.

- [ ] **Step 6: Test and commit**

```bash
python -m pytest -q tools/sprite-animation-studio/tests/test_hub_delivery.py \
  tools/sprite-animation-studio/tests/test_api.py \
  tools/sprite-animation-studio/tests/test_delivery.py \
  tools/expression-studio/tests \
  tools/tool-hub/tests/test_studio_delivery_trust.py
```

Commit message:

```text
feat(sprite-studio): confirm exact atlas delivery through Tool Hub
```

---

### Task 6: Expose safe confirmation UX and update docs

- [ ] **Step 1: Add UX contract assertions**

Require `confirm-delivery`, `delivery-status`, `confirmed-download`, `확정 및 전달`, `Sprite Action Runs`, and `Effect Runs`. Assert browser JavaScript does not submit `figma_file_key`, `target_node_id`, `generation_area_node_id`, `project_marker_node_id`, or `X-Base-Tool-Route`.

- [ ] **Step 2: Add browser calls that carry no route authority**

```javascript
const confirmation = await api(`/api/runs/${encodeURIComponent(runId)}/confirm-delivery`, {
  method: "POST"
});
const status = await api(`/api/runs/${encodeURIComponent(runId)}/delivery-status`);
```

Render server-returned target name, bridge state, pairing code when present, delivery state, and download URL. Do not derive a route from browser mode state.

- [ ] **Step 3: Update README and test**

Document `pose_sequence/sprite_action -> Sprite Action Runs`, `effect_stages -> Effect Runs`, `expression_variation -> delivery unavailable`, confirmed payload=`exported atlas PNG`, and live ChatGPT/user-PC/Bridge/Godot evidence=`NOT_RUN` until observed.

```bash
python -m pytest -q tools/sprite-animation-studio/tests/test_docs_contract.py \
  tools/sprite-animation-studio/tests/test_hub_delivery.py \
  tests/test_tool_hub_subscription_production_contract.py
```

Commit message:

```text
feat(sprite-studio): expose confirmed dedicated Figma delivery
```

---

### Task 7: Cross-platform GREEN and adversarial reconciliation

- [ ] **Step 1: Run full focused regression**

```bash
python -m pytest -q tools/tool-hub/tests/test_figma_delivery.py \
  tools/tool-hub/tests/test_figma_delivery_hardening.py \
  tools/tool-hub/tests/test_figma_delivery_concurrency.py \
  tools/tool-hub/tests/test_figma_bridge_api.py \
  tools/tool-hub/tests/test_figma_plugin_contract.py \
  tools/tool-hub/tests/test_figma_exact_tool_route.py \
  tools/tool-hub/tests/test_studio_delivery_trust.py \
  tools/sprite-animation-studio/tests \
  tools/expression-studio/tests \
  tests/test_tool_hub_subscription_production_contract.py
```

No failure is dismissed without reproduction on current `main`.

- [ ] **Step 2: Verify actual CI execution on both OSes**

Push and confirm `Validate Provisional Figma Integration` runs the new Sprite/Tool Hub/root tests on Ubuntu and Windows. Require other triggered Base gates, including Base v9 and Game Project Operating System/`ci-gate` when present.

- [ ] **Step 3: Adversarially attack trust boundaries**

Verify tests cover Sprite→Character route misuse, Expression→Effect misuse, missing Sprite route, same-run route change, same-run byte change, atlas tamper, route rename/reparent, marker drift, generic-parent fallback, browser route/node/file injection, and recovered Sprite job missing route identity. Merge target is P0/P1=0.

- [ ] **Step 4: Reconcile latest main and overlapping PRs without waiting**

Re-read latest `main` and open PR changed paths. If main moved, non-force reconcile. If approved open work overlaps, compare material deltas and copy compatible material onto the integration branch while leaving source branches read-only.

- [ ] **Step 5: Re-run exact-head CI and prepare implementation PR**

PR body records exact head SHA, `24/24` routes, `16/16` Figma readbacks, preserved Expression behavior, server-owned Sprite mode routing, atlas SHA binding, and live IRG items still `NOT_RUN`.

---

### Task 8: Merge, post-merge readback, and tracking cleanup

- [ ] **Step 1: Final pre-merge gate**

Re-read Base main, implementation head, 24 registry pairs, all 16 new Figma nodes, unresolved review threads, and required workflow conclusions. Any movement reopens reconciliation.

- [ ] **Step 2: Squash merge with expected-head protection**

Do not use admin/ruleset bypass.

- [ ] **Step 3: Read back new main and Figma**

Verify the route registry has 24 entries. Re-read `figma_delivery.py`, `studio_delivery_api.py`, Sprite `app.py`, and all 24 Figma destinations. Any drift becomes a blocking issue rather than silent authority mutation.

- [ ] **Step 4: Verify post-merge push CI**

Wait until all workflows covering changed paths on the merge SHA are complete and successful before calling repository/Figma routing complete.

- [ ] **Step 5: Update Base Issue #393**

Record exactly:

```text
DEDICATED_SPRITE_EFFECT_ROUTE_CLOUD_PREFLIGHT = PASS_8_OF_8
BASE_TOOL_ROUTE_REGISTRY = READY_24_OF_24
SPRITE_MODE_ROUTE_TRUST = VERIFIED_BY_TESTS
SPRITE_CONFIRMED_ATLAS_SHA_BINDING = VERIFIED_BY_TESTS
USER_PC_TOOL_HUB = NOT_RUN
REAL_CHATGPT_PRO_POSE_SEQUENCE = NOT_RUN
REAL_CHATGPT_PRO_EFFECT_STAGES = NOT_RUN
LOCALHOST_FIGMA_BRIDGE_RECEIPT = NOT_RUN
GODOT_CONSUMPTION = NOT_RUN
```

- [ ] **Step 6: Reconcile design PR #451**

If merged main contains the approved spec and plan byte-identically, comment that #451 was superseded by the merged implementation and close it. Otherwise retain #451 until documentation provenance is reconciled.

- [ ] **Step 7: Hand off to live PC IRG**

Next sequence is `Base Tool Hub.lnk -> urban-legend -> real Character/Expression same-run receipt -> real pose_sequence -> real effect_stages -> exact localhost Figma same-SHA receipts -> Godot/project consumption`. Do not promote cloud/CI evidence to those live PASS claims.
