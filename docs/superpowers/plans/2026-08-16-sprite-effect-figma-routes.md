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
- Never route Sprite/Effect output to generic `Generated Assets` or `Expression Runs` as a fallback.
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

**Files:** root contract, Tool Hub route/trust tests, new Sprite delivery test, Figma integration workflow, approved spec/plan copies.

**Interfaces:** Produces a separate `feat/sprite-effect-figma-routes-20260816` implementation branch. PR #451 becomes read-only design/plan provenance after handoff.

- [ ] **Step 1: Create the implementation branch from exact latest completed `main`**

Re-read `main` and open PR changed paths. Create `feat/sprite-effect-figma-routes-20260816` from that SHA and copy the approved spec and plan blobs from #451. Do not push implementation commits to #451.

- [ ] **Step 2: Make the root route contract require the final 24-route shape**

In `tests/test_tool_hub_subscription_production_contract.py` use:

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

Group each project's three entries and assert the three destination IDs are mutually distinct and distinct from parent/marker.

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


@pytest.mark.parametrize("route_id", ["character_expression_runs", "bogus_route"])
def test_sprite_delivery_rejects_unowned_route(tmp_path: Path, route_id: str) -> None:
    service, _ = service_for(tmp_path, "omenward")
    with pytest.raises(DeliveryError, match="DELIVERY_TOOL_ROUTE_UNAVAILABLE"):
        service.enqueue(
            "sprite-animation-studio", "omenward", "run-wrong-route",
            png_bytes(), "image/png", tool_route_id=route_id,
        )
```

Add a same-run/same-bytes/different-route test expecting `DELIVERY_RUN_ROUTE_MISMATCH`.

- [ ] **Step 4: Define RED authenticated child-route tests**

Add a Sprite authorization helper to `test_studio_delivery_trust.py`:

```python
def _authorize_sprite_child(monkeypatch: pytest.MonkeyPatch) -> None:
    def authorize(self: ProcessSupervisor, token: str) -> tuple[str, str]:
        if token != _PRIVATE_TOKEN:
            raise LaunchError("studio delivery credential is invalid")
        return ("sprite-animation-studio", "coc-fiction")
    monkeypatch.setattr(ProcessSupervisor, "authorize_delivery_token", authorize)
```

Assert missing route and `character_expression_runs` both return HTTP 409 `DELIVERY_TOOL_ROUTE_UNAVAILABLE`; assert valid `sprite_action_runs` and `effect_runs` return the matching route/name.

- [ ] **Step 5: Define RED Sprite confirmed-atlas tests with a complete recording sender**

Create `tools/sprite-animation-studio/tests/test_hub_delivery.py` with this sender shape:

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

Tests assert `pose_sequence`/`sprite_action` use `sprite_action_runs`, `effect_stages` uses `effect_runs`, `expression_variation` sends nothing and returns 409, and `sender.calls[0][1]` equals the exported atlas bytes whose SHA equals `record.export_output_sha256["atlas"]`. Atlas tampering must fail before sender invocation.

- [ ] **Step 6: Wire all RED tests into Ubuntu/Windows CI**

Extend `.github/workflows/validate-provisional-figma-integration.yml` path filters with `tools/base-tool-contracts/**`, `tools/sprite-animation-studio/**`, and `tests/test_tool_hub_subscription_production_contract.py`. Install all three editable packages:

```bash
python -m pip install -e './tools/base-tool-contracts[dev]' -e './tools/tool-hub[dev]' -e './tools/sprite-animation-studio[dev]'
```

Run the existing Figma tests plus `test_studio_delivery_trust.py`, `tools/sprite-animation-studio/tests/test_hub_delivery.py`, and the root subscription production contract.

- [ ] **Step 7: Run RED**

```bash
python -m pytest -q \
  tools/tool-hub/tests/test_figma_exact_tool_route.py \
  tools/tool-hub/tests/test_studio_delivery_trust.py \
  tools/sprite-animation-studio/tests/test_hub_delivery.py \
  tests/test_tool_hub_subscription_production_contract.py
```

Expected failures are only: registry has 8 routes, Tool Hub lacks explicit Sprite route support, and Sprite Studio lacks confirmed Hub delivery. Reproduce any unrelated failure on current `main` before proceeding.

- [ ] **Step 8: Commit RED**

```bash
git add docs/superpowers/specs/2026-08-16-sprite-effect-figma-routes-design.md \
  docs/superpowers/plans/2026-08-16-sprite-effect-figma-routes.md \
  tests/test_tool_hub_subscription_production_contract.py \
  tools/tool-hub/tests/test_figma_exact_tool_route.py \
  tools/tool-hub/tests/test_studio_delivery_trust.py \
  tools/sprite-animation-studio/tests/test_hub_delivery.py \
  .github/workflows/validate-provisional-figma-integration.yml
git commit -m "test: define dedicated sprite and effect delivery routes"
```

---

### Task 2: Create/reuse and read back all 16 Figma frames

**Files:** Create `docs/evidence/2026-08-16-sprite-effect-figma-route-readback.md`; mutate only the eight approved Figma files.

**Interfaces:** Produces a complete map `figma_route_nodes[project_id][route_id] -> real node_id`. Task 3 starts only if this contains 16 valid new IDs.

- [ ] **Step 1: Load Figma write guidance and re-read the exact parents**

Use these immutable preflight tuples:

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

Abort mutation for a file if parent, Expression route, or marker name/type/parent has drifted.

- [ ] **Step 2: Retry-safely clone the existing Expression frame twice**

For each file, pass an exact `cfg` object containing that row's IDs to this Figma operation:

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

- [ ] **Step 3: Read back each created/reused node**

Confirm exact type/name/parent, `Sprite Action Runs` geometry `40,408,1360,148`, `Effect Runs` geometry `40,576,1360,148`, one sibling per canonical name, and unchanged marker.

- [ ] **Step 4: Record real IDs**

Create a Markdown table with 8 project rows and columns: project ID, file key, parent, marker, actual Sprite node ID, actual Effect node ID, readback `PASS`. Record the Base main SHA used for preflight and `LOCALHOST_BRIDGE_RECEIPT: NOT_RUN`.

- [ ] **Step 5: Gate and commit evidence**

Require 8 rows, 16 non-empty route IDs, and per-project uniqueness across parent/marker/Expression/Sprite/Effect IDs. If incomplete, leave the Base registry unchanged.

```bash
git add docs/evidence/2026-08-16-sprite-effect-figma-route-readback.md
git commit -m "docs: record reviewed sprite and effect Figma route nodes"
```

---

### Task 3: Expand the canonical registry to 24 routes

**Files:** `PROJECT_FIGMA_TOOL_ROUTE_REGISTRY.json`, `figma_tool_routing.py`, root contract.

**Interfaces:** Consumes the 16 exact IDs from Task 2. Produces 24 `READY_FOR_DELIVERY` route pairs.

- [ ] **Step 1: Add `sprite_action_runs` and `effect_runs` per project**

Copy `figma_file_key`, parent fields, marker fields, and marker name from that project's existing Character entry. Use only Task 2's observed destination ID. Use exact names `Sprite Action Runs` and `Effect Runs`. Keep all eight Character entries semantically unchanged.

- [ ] **Step 2: Reject duplicate active destinations within one project**

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

- [ ] **Step 3: Run registry tests**

```bash
python -m pytest -q tests/test_tool_hub_subscription_production_contract.py \
  tools/tool-hub/tests/test_figma_exact_tool_route.py
```

The 24-route assertions must pass. Route-aware Tool Hub tests may remain RED until Task 4.

- [ ] **Step 4: Commit**

```bash
git add docs/operations/PROJECT_FIGMA_TOOL_ROUTE_REGISTRY.json \
  tools/base-tool-contracts/src/base_tool_contracts/figma_tool_routing.py \
  tests/test_tool_hub_subscription_production_contract.py
git commit -m "feat: register dedicated sprite and effect Figma routes"
```

---

### Task 4: Enforce authenticated tool-to-route ownership in Tool Hub

**Files:** `figma_delivery.py`, `studio_delivery_api.py`, Tool Hub route/trust tests.

**Interfaces:** Produces `enqueue(..., *, tool_route_id: str | None = None)` and fixed route allowlists.

- [ ] **Step 1: Replace the one-route map with an allowlist**

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

Make `_resolve_tool_route` accept the requested route and resolve only that canonical entry.

- [ ] **Step 2: Bind route to enqueue/idempotency/recovery**

Add keyword-only `tool_route_id` to `enqueue` and `enqueue_idempotent`. Before reusing a matching run, compare stored `job.tool_route_id` with `_requested_route_id(tool_id, tool_route_id)` and raise `DELIVERY_RUN_ROUTE_MISMATCH` on mismatch. Preserve existing `DELIVERY_RUN_CONTENT_MISMATCH` for changed bytes.

`_assert_current_job_route` and receipt recovery must resolve using the stored job route. Only a legacy Expression job may default a missing route to `character_expression_runs`; a recovered Sprite job with no stored route is invalid.

- [ ] **Step 3: Add the private route header to the internal Studio POST only**

In `studio_delivery_api.py` import `Header` and validate:

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

The POST endpoint accepts `x_base_tool_route: str | None = Header(default=None, alias="X-Base-Tool-Route")` and passes `_requested_route(tool_id, x_base_tool_route)` to `enqueue_idempotent`. The status endpoint accepts no route header and returns the stored route identity.

- [ ] **Step 4: Run focused tests**

```bash
python -m pytest -q tools/tool-hub/tests/test_figma_exact_tool_route.py \
  tools/tool-hub/tests/test_studio_delivery_trust.py \
  tools/tool-hub/tests/test_figma_delivery.py \
  tools/tool-hub/tests/test_figma_delivery_hardening.py \
  tools/tool-hub/tests/test_figma_delivery_concurrency.py
```

- [ ] **Step 5: Commit**

```bash
git add tools/tool-hub/src/tool_hub/figma_delivery.py \
  tools/tool-hub/src/tool_hub/studio_delivery_api.py \
  tools/tool-hub/tests/test_figma_exact_tool_route.py \
  tools/tool-hub/tests/test_studio_delivery_trust.py
git commit -m "feat(tool-hub): enforce exact sprite and effect delivery routes"
```

---

### Task 5: Share the loopback client and add Sprite confirmed-atlas delivery

**Files:** new shared `hub_delivery.py`, base exports, Expression compatibility wrapper, Sprite service/app/test.

**Interfaces:** Shared sender signature is `__call__(run_id, image_bytes, media_type, tool_route_id=None)` plus `status(delivery_id)`. Sprite service produces `delivery_route_id(run_id) -> str`.

- [ ] **Step 1: Promote the Expression Hub client into `base-tool-contracts`**

Preserve loopback-only origin validation, no-proxy opener, child token, 5-second timeout, 64-KiB response cap, strict JSON object response, and the two existing environment variables. Extend only the optional header path:

```python
class HubDeliverySender(Protocol):
    def __call__(self, run_id: str, image_bytes: bytes, media_type: str,
                 tool_route_id: str | None = None) -> dict[str, object]: ...
    def status(self, delivery_id: str) -> dict[str, object]: ...
```

The protocol method bodies use Python protocol ellipsis syntax intentionally; production methods below are concrete.

Concrete request code:

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

Add `extra_headers: dict[str, str] | None = None` to `_json_request` and merge those bounded headers after Authorization/Accept/Content-Type.

- [ ] **Step 2: Preserve Expression compatibility**

Replace `expression_studio/hub_delivery.py` with:

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

Export the same names from `base_tool_contracts.__init__`. Existing Expression calls remain three-argument calls and therefore use the sole allowed Expression default route.

- [ ] **Step 3: Add server-owned Sprite route mapping**

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

No endpoint accepts route ID as body/query input.

- [ ] **Step 4: Add Sprite `confirm-delivery`**

`create_app` gains `hub_delivery_sender: HubDeliverySender | None = None`, resolves `sender_from_environment()` when absent, and holds a lock-protected confirmation map. The endpoint has no request body and requires an already exported run:

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

Normalize the response only if tool=`sprite-animation-studio`, project/run/SHA match, route equals the derived route, target name equals `Sprite Action Runs` or `Effect Runs`, the delivery ID is valid, states are internally consistent, and Figma URL is `https://www.figma.com/design/`.

- [ ] **Step 5: Add route-bound status and atlas download**

Implement `GET /api/runs/{run_id}/delivery-status` and `GET /api/runs/{run_id}/confirmed-download`. Status re-reads the atlas with cached SHA before `sender.status(delivery_id)` and rejects identity drift. Download returns the same atlas bytes with `X-Content-SHA256`.

- [ ] **Step 6: Run shared/Sprite/Expression regressions**

```bash
python -m pytest -q tools/sprite-animation-studio/tests/test_hub_delivery.py \
  tools/sprite-animation-studio/tests/test_api.py \
  tools/sprite-animation-studio/tests/test_delivery.py \
  tools/expression-studio/tests \
  tools/tool-hub/tests/test_studio_delivery_trust.py
```

- [ ] **Step 7: Commit**

```bash
git add tools/base-tool-contracts/src/base_tool_contracts/hub_delivery.py \
  tools/base-tool-contracts/src/base_tool_contracts/__init__.py \
  tools/expression-studio/src/expression_studio/hub_delivery.py \
  tools/sprite-animation-studio/src/sprite_animation_studio/service.py \
  tools/sprite-animation-studio/src/sprite_animation_studio/app.py \
  tools/sprite-animation-studio/tests/test_hub_delivery.py
git commit -m "feat(sprite-studio): confirm exact atlas delivery through Tool Hub"
```

---

### Task 6: Expose safe confirmation UX and update docs

**Files:** Sprite web HTML/JS, README, docs contract, root production contract.

- [ ] **Step 1: Add UX tests before web changes**

Require `confirm-delivery`, `delivery-status`, `confirmed-download`, `확정 및 전달`, `Sprite Action Runs`, and `Effect Runs`. Assert browser JavaScript does not submit `figma_file_key`, `target_node_id`, `generation_area_node_id`, `project_marker_node_id`, or `X-Base-Tool-Route`.

- [ ] **Step 2: Add confirmation and status calls**

After export:

```javascript
const confirmation = await api(`/api/runs/${encodeURIComponent(runId)}/confirm-delivery`, {
  method: "POST"
});
```

Refresh with:

```javascript
const status = await api(`/api/runs/${encodeURIComponent(runId)}/delivery-status`);
```

Render only server-returned route target name, bridge state, pairing code when present, delivery state, and download URL. Never derive a Figma route from browser mode state.

- [ ] **Step 3: Update README truth**

Document `pose_sequence/sprite_action -> Sprite Action Runs`, `effect_stages -> Effect Runs`, `expression_variation -> delivery unavailable`, confirmed payload=`exported atlas PNG`, and live ChatGPT/user-PC/Bridge/Godot evidence remains `NOT_RUN` until observed.

- [ ] **Step 4: Test and commit**

```bash
python -m pytest -q tools/sprite-animation-studio/tests/test_docs_contract.py \
  tools/sprite-animation-studio/tests/test_hub_delivery.py \
  tests/test_tool_hub_subscription_production_contract.py

git add tools/sprite-animation-studio/web/index.html \
  tools/sprite-animation-studio/web/app.js \
  tools/sprite-animation-studio/README.md \
  tools/sprite-animation-studio/tests/test_docs_contract.py \
  tests/test_tool_hub_subscription_production_contract.py
git commit -m "feat(sprite-studio): expose confirmed dedicated Figma delivery"
```

---

### Task 7: Cross-platform GREEN and adversarial reconciliation

**Files:** implementation files above; CI workflow only if a bounded wiring correction is required.

- [ ] **Step 1: Run the full focused suite**

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

No failure is dismissed without reproducing it on current `main`.

- [ ] **Step 2: Push and verify actual Ubuntu/Windows execution**

Confirm `Validate Provisional Figma Integration` actually executes the new Sprite/Tool Hub/root test files on both operating systems. Require other Base gates triggered by the diff, including Base v9 and Game Project Operating System/`ci-gate` where applicable.

- [ ] **Step 3: Adversarially attack the trust boundary**

Tests/review must cover: Sprite child requesting Character route, Expression child requesting Effect route, Sprite route omission, same run + changed route, same run + changed bytes, atlas tamper, route node rename/reparent, marker drift, generic-parent fallback, browser route/node/file injection, and recovered Sprite job missing route identity. Merge target is P0/P1 findings = 0.

- [ ] **Step 4: Reconcile latest `main` and overlapping PRs without waiting**

Re-read `main` and open PR paths. If main moved, non-force reconcile onto the implementation branch. If approved open work overlaps, compare material deltas and copy compatible material onto this integration branch while leaving source branches read-only.

- [ ] **Step 5: Re-run exact-head CI and open/refresh the implementation PR**

PR body records exact head SHA, 24/24 registry routes, 16/16 Figma readbacks, preserved Expression behavior, server-owned Sprite mode routing, atlas SHA binding, and live IRG items still `NOT_RUN`.

---

### Task 8: Merge, post-merge readback, and tracking cleanup

- [ ] **Step 1: Final pre-merge gate**

Re-read Base main, implementation head, 24 registry pairs, all 16 new Figma nodes, unresolved review threads, and required workflow conclusions. Any movement reopens reconciliation.

- [ ] **Step 2: Squash merge with expected-head protection**

Do not use admin/ruleset bypass.

- [ ] **Step 3: Read back new main**

Verify the canonical route registry has 24 entries and re-read `figma_delivery.py`, `studio_delivery_api.py`, and Sprite `app.py` from the merge SHA.

- [ ] **Step 4: Re-read all 24 Figma destinations**

For each of 8 files verify Expression + Sprite Action + Effect + existing marker. Report drift as a blocking issue rather than silently changing authority.

- [ ] **Step 5: Verify post-merge push CI**

Wait until all workflows covering the changed paths on the merge SHA are complete and successful before calling repository/Figma routing complete.

- [ ] **Step 6: Update Base Issue #393 with bounded evidence**

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

- [ ] **Step 7: Reconcile design PR #451**

If the merged implementation contains the approved spec and plan byte-identically, comment that #451 was superseded by the merged implementation and close #451. Otherwise keep it open until documentation provenance is reconciled.

- [ ] **Step 8: Hand off to live PC IRG**

Next sequence: `Base Tool Hub.lnk -> urban-legend -> real Character/Expression same-run receipt -> real pose_sequence -> real effect_stages -> exact localhost Figma same-SHA receipts -> Godot/project consumption`. Do not promote cloud/CI evidence to those live PASS claims.
