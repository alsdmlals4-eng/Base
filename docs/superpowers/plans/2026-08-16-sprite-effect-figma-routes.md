# Dedicated Sprite Action / Effect Figma Routes Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add reviewed `Sprite Action Runs` and `Effect Runs` destinations to all eight registered Figma projects, register all 24 exact project/tool routes in Base, and enable fail-closed same-SHA Sprite/Effect atlas delivery through the existing localhost Tool Hub bridge.

**Architecture:** Keep Figma node authority in the existing project/route registries and keep the existing hidden project markers. Add two sibling Figma route frames per project, then extend Tool Hub so an authenticated `sprite-animation-studio` child may request only a server-derived `sprite_action_runs` or `effect_runs` route. Sprite Animation Studio confirms only its verified exported atlas PNG; Tool Hub revalidates tool/route/project/registry identity before queueing the existing exact-node bridge job.

**Tech Stack:** Python 3.12, FastAPI, Pydantic, pytest/unittest, existing Base `base-tool-contracts`, Tool Hub/Figma Bridge, Sprite Animation Studio, Figma Plugin API through the connected Figma tool, GitHub Actions on Ubuntu/Windows.

## Global Constraints

- `ZERO_INCREMENTAL_COST_REQUIRED`: no new paid API, API key, metered provider, or mandatory paid dependency.
- Preserve `subscription_handoff_import` + `CHATGPT_INCLUDED`; provider call remains false for the normal ChatGPT Pro handoff path.
- Do not mutate stale/open owner PR branches. Start implementation from latest completed `main`; copy approved spec/plan material as needed under `BASE_COPY_INTEGRATION_STANDING_AUTHORIZATION_2026_08_16`.
- Keep `Expression Runs` and all eight existing hidden `Base Tool Hub Route · <project_id>` markers unchanged.
- Never use generic `Generated Assets` or `Expression Runs` as Sprite/Effect fallback destinations.
- Do not commit any new Sprite/Effect route as `READY_FOR_DELIVERY` until all 16 Figma frames have been created or safely reused and read back.
- Browser/project input is not Figma route authority. Sprite route identity must come from server-owned `RunRecord.request.mode`.
- `pose_sequence` and `sprite_action` map to `sprite_action_runs`; `effect_stages` maps to `effect_runs`; `expression_variation` remains delivery-blocked in this slice.
- The Sprite/Effect payload sent to Tool Hub is the exact verified exported atlas PNG, not a candidate frame, contact sheet, GIF, or browser-selected file.
- Same run + same route + same atlas SHA is idempotent. Same run + changed route or changed bytes fails closed.
- `PROJECT_ASSET_APPROVED` is not granted by this work.
- Cloud Figma node/readback and CI evidence do not prove user-PC Tool Hub execution, real ChatGPT Pro visual quality, localhost Bridge receipt, or Godot consumption.

---

## File Structure

**Create**
- `tools/base-tool-contracts/src/base_tool_contracts/hub_delivery.py` — shared loopback Studio-to-Hub client with optional exact route header.
- `tools/sprite-animation-studio/tests/test_hub_delivery.py` — server-owned mode→route, atlas-byte, status, and idempotency contracts.
- `docs/evidence/2026-08-16-sprite-effect-figma-route-readback.md` — immutable audit table of the 16 real Figma route node IDs observed during implementation.

**Modify**
- `tools/base-tool-contracts/src/base_tool_contracts/__init__.py` — export shared delivery client contracts.
- `tools/expression-studio/src/expression_studio/hub_delivery.py` — compatibility re-export of the shared client so Expression behavior/import paths remain stable.
- `tools/tool-hub/src/tool_hub/figma_delivery.py` — authenticated tool/route allowlist, explicit route resolution, route-bound idempotency/recovery.
- `tools/tool-hub/src/tool_hub/studio_delivery_api.py` — accept/validate the child-only exact route header; preserve expression default compatibility.
- `tools/tool-hub/tests/test_figma_exact_tool_route.py` — dedicated Sprite/Effect route tests.
- `tools/tool-hub/tests/test_studio_delivery_trust.py` — authenticated child route-header trust and route mismatch tests.
- `tools/sprite-animation-studio/src/sprite_animation_studio/service.py` — server-owned run-mode→route helper and confirmed-atlas evidence access.
- `tools/sprite-animation-studio/src/sprite_animation_studio/app.py` — `confirm-delivery`, status refresh, and confirmed-atlas download endpoints using child-only Hub identity.
- `tools/sprite-animation-studio/web/index.html` — expose `확정 및 전달`/delivery status after export.
- `tools/sprite-animation-studio/web/app.js` — call only server run endpoints; never submit route/node/file authority.
- `tools/sprite-animation-studio/README.md` — document dedicated route behavior and live-IRG ceiling.
- `docs/operations/PROJECT_FIGMA_TOOL_ROUTE_REGISTRY.json` — expand 8 Character routes to 24 exact routes after Figma readback.
- `tests/test_tool_hub_subscription_production_contract.py` — require 24 route pairs and canonical names.
- `.github/workflows/validate-provisional-figma-integration.yml` — install Sprite/shared contracts and actually execute the new route/delivery tests on Ubuntu and Windows.
- `docs/superpowers/specs/2026-08-16-sprite-effect-figma-routes-design.md` and this plan — copy unchanged onto the implementation branch for provenance.

**External Figma mutations**
- Eight existing Figma design files listed in the approved spec; create/reuse exactly 16 frames under their exact `Generated Assets` parents.

---

### Task 1: Create latest-main implementation branch and establish TDD RED

**Files:**
- Modify: `tests/test_tool_hub_subscription_production_contract.py`
- Modify: `tools/tool-hub/tests/test_figma_exact_tool_route.py`
- Modify: `tools/tool-hub/tests/test_studio_delivery_trust.py`
- Create: `tools/sprite-animation-studio/tests/test_hub_delivery.py`
- Modify: `.github/workflows/validate-provisional-figma-integration.yml`
- Copy unchanged: `docs/superpowers/specs/2026-08-16-sprite-effect-figma-routes-design.md`
- Copy unchanged: `docs/superpowers/plans/2026-08-16-sprite-effect-figma-routes.md`

**Interfaces:**
- Consumes: approved spec head from PR #451 plus latest completed Base `main`.
- Produces: a separate implementation branch with failing contracts that require 24 registry routes, route-aware authenticated Sprite delivery, and Sprite confirmed-atlas delivery.

- [ ] **Step 1: Re-read latest `main` and active PR overlap, then create a separate implementation branch**

Create `feat/sprite-effect-figma-routes-20260816` from the exact latest completed `main` SHA. Copy the approved spec and this plan from PR #451 by blob/content; do not rebase, push to, or convert #451 into an implementation branch. Re-read open PR changed paths and use copy-integration if another PR has since touched a planned path.

Expected branch invariant:

```text
implementation base == latest completed Base main
PR #451 branch == read-only design/plan source after handoff
source owner branches == unmodified
```

- [ ] **Step 2: Change the root subscription production contract to the desired 24-route state**

Replace the old “8 Character routes only / Sprite routes absent” assertions with:

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

Also group each project's three entries and assert all three destination node IDs are distinct from each other, their parent, and their marker.

- [ ] **Step 3: Replace the old Sprite-unavailable Tool Hub route test with desired route-aware RED tests**

In `tools/tool-hub/tests/test_figma_exact_tool_route.py`, define the expected contract:

```python
def test_sprite_action_delivery_binds_only_sprite_action_destination(tmp_path: Path) -> None:
    service, _ = service_for(tmp_path, "omenward")
    job = service.enqueue(
        "sprite-animation-studio",
        "omenward",
        "run-sprite-action",
        png_bytes(),
        "image/png",
        tool_route_id="sprite_action_runs",
    )
    assert job.tool_route_id == "sprite_action_runs"
    assert job.target_node_name == "Sprite Action Runs"


def test_effect_delivery_binds_only_effect_destination(tmp_path: Path) -> None:
    service, _ = service_for(tmp_path, "omenward")
    job = service.enqueue(
        "sprite-animation-studio",
        "omenward",
        "run-effect",
        png_bytes(),
        "image/png",
        tool_route_id="effect_runs",
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

Add a same-run/same-bytes/different-route assertion expecting `DELIVERY_RUN_ROUTE_MISMATCH`.

- [ ] **Step 4: Add authenticated Studio API RED tests**

Extend `tools/tool-hub/tests/test_studio_delivery_trust.py` with a Sprite child authorization helper and tests using the private route header:

```python
def _authorize_sprite_child(monkeypatch: pytest.MonkeyPatch) -> None:
    def authorize(self: ProcessSupervisor, token: str) -> tuple[str, str]:
        if token != _PRIVATE_TOKEN:
            raise LaunchError("studio delivery credential is invalid")
        return ("sprite-animation-studio", "coc-fiction")
    monkeypatch.setattr(ProcessSupervisor, "authorize_delivery_token", authorize)


def test_sprite_child_must_supply_an_owned_exact_route(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    client = _registered_hub(tmp_path)
    _authorize_sprite_child(monkeypatch)
    base = _studio_headers()

    missing = client.post("/internal/studio-delivery/run-sprite", content=png_bytes(2, 1), headers=base)
    assert missing.status_code == 409
    assert missing.json()["detail"] == "DELIVERY_TOOL_ROUTE_UNAVAILABLE"

    wrong = client.post(
        "/internal/studio-delivery/run-sprite",
        content=png_bytes(2, 1),
        headers={**base, "X-Base-Tool-Route": "character_expression_runs"},
    )
    assert wrong.status_code == 409
    assert wrong.json()["detail"] == "DELIVERY_TOOL_ROUTE_UNAVAILABLE"
```

A valid `sprite_action_runs` request must return that route and `Sprite Action Runs`; a valid `effect_runs` request must return `Effect Runs`.

- [ ] **Step 5: Add Sprite Studio confirmed-atlas RED tests**

Create `tools/sprite-animation-studio/tests/test_hub_delivery.py` around a recording sender:

```python
class RecordingSender:
    def __init__(self) -> None:
        self.calls: list[tuple[str, bytes, str, str | None]] = []

    def __call__(
        self,
        run_id: str,
        image_bytes: bytes,
        media_type: str,
        tool_route_id: str | None = None,
    ) -> dict[str, object]:
        self.calls.append((run_id, image_bytes, media_type, tool_route_id))
        target = {
            "sprite_action_runs": "Sprite Action Runs",
            "effect_runs": "Effect Runs",
        }[str(tool_route_id)]
        return {
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

    def status(self, delivery_id: str) -> dict[str, object]:
        ...
```

Implement the test fixture's `status()` fully in the test file by storing the last response and returning the same identity with `status="DELIVERED_VERIFIED"` and `delivery_state="FIGMA_DELIVERED_VERIFIED"`; do not leave an ellipsis in committed code.

Tests must prove:

```python
assert sender.calls[0][3] == "sprite_action_runs"  # pose_sequence or sprite_action
assert sender.calls[0][1] == exported_atlas.read_bytes()
assert hashlib.sha256(sender.calls[0][1]).hexdigest() == record.export_output_sha256["atlas"]
```

For `effect_stages`, expect `effect_runs`. For `expression_variation`, expect HTTP 409 `DELIVERY_TOOL_ROUTE_UNAVAILABLE` and zero sender calls. Tampering the atlas after export must return 409 before any sender call.

- [ ] **Step 6: Wire the RED tests into the existing cross-platform Figma workflow before production changes**

Update `.github/workflows/validate-provisional-figma-integration.yml` path filters to include:

```yaml
- "tools/base-tool-contracts/**"
- "tools/sprite-animation-studio/**"
- "tests/test_tool_hub_subscription_production_contract.py"
```

Install:

```bash
python -m pip install -e './tools/base-tool-contracts[dev]' -e './tools/tool-hub[dev]' -e './tools/sprite-animation-studio[dev]'
```

and Windows equivalents. Extend the pytest invocation with:

```text
tools/tool-hub/tests/test_studio_delivery_trust.py
tools/sprite-animation-studio/tests/test_hub_delivery.py
tests/test_tool_hub_subscription_production_contract.py
```

- [ ] **Step 7: Run RED and record why it fails**

Run:

```bash
python -m pytest -q \
  tools/tool-hub/tests/test_figma_exact_tool_route.py \
  tools/tool-hub/tests/test_studio_delivery_trust.py \
  tools/sprite-animation-studio/tests/test_hub_delivery.py \
  tests/test_tool_hub_subscription_production_contract.py
```

Expected failures must be limited to the intended missing capabilities: registry still has 8 routes, Tool Hub has no Sprite route parameter/header support, and Sprite Studio has no Hub confirm-delivery path. If unrelated baseline failures appear, separate them before implementation.

- [ ] **Step 8: Commit the RED contract slice**

```bash
git add \
  docs/superpowers/specs/2026-08-16-sprite-effect-figma-routes-design.md \
  docs/superpowers/plans/2026-08-16-sprite-effect-figma-routes.md \
  tests/test_tool_hub_subscription_production_contract.py \
  tools/tool-hub/tests/test_figma_exact_tool_route.py \
  tools/tool-hub/tests/test_studio_delivery_trust.py \
  tools/sprite-animation-studio/tests/test_hub_delivery.py \
  .github/workflows/validate-provisional-figma-integration.yml
git commit -m "test: define dedicated sprite and effect delivery routes"
```

---

### Task 2: Create/reuse and read back all 16 Figma route frames

**Files:**
- Create: `docs/evidence/2026-08-16-sprite-effect-figma-route-readback.md`
- External: mutate eight existing Figma design files only under their exact registered `Generated Assets` parents.

**Interfaces:**
- Consumes: the eight `(file_key, parent_node_id, expression_node_id, marker_node_id)` tuples from the approved spec.
- Produces: `figma_route_nodes[project_id] = {"sprite_action_runs": node_id, "effect_runs": node_id}` for all 8 projects, plus cloud readback evidence. Task 3 must not begin registry mutation unless this map has 16 valid unique node IDs.

- [ ] **Step 1: Load Figma write guidance and re-read all eight parents before mutation**

Attempt to load the available `figma-use` guidance before `use_figma`. Re-read each exact parent with metadata. Abort mutation for that file if any of these drift from the approved spec:

```text
parent type/name != FRAME / Generated Assets
Expression Runs id/name/type mismatch
project marker id/name/type mismatch
parent no longer contains the Expression route and marker
```

Also search only direct children of the exact parent for `Sprite Action Runs` and `Effect Runs` so retries reuse valid siblings rather than creating duplicates.

- [ ] **Step 2: For each Figma file, clone the existing Expression frame into the two exact sibling routes**

Use the existing `Expression Runs` frame as the style source rather than reconstructing visual styling. The per-file Figma Plugin API operation follows this shape, with the approved file-specific constants substituted from the spec:

```javascript
const parent = await figma.getNodeByIdAsync(PARENT_ID);
const expression = await figma.getNodeByIdAsync(EXPRESSION_ID);
const marker = await figma.getNodeByIdAsync(MARKER_ID);
if (!parent || parent.type !== "FRAME" || parent.name !== "Generated Assets") throw new Error("parent drift");
if (!expression || expression.type !== "FRAME" || expression.parent !== parent || expression.name !== "Expression Runs") throw new Error("expression drift");
if (!marker || marker.type !== "FRAME" || marker.parent !== parent || marker.name !== `Base Tool Hub Route · ${PROJECT_ID}`) throw new Error("marker drift");

async function loadTextFonts(text) {
  if (text.characters.length === 0) return;
  for (const font of text.getRangeAllFontNames(0, text.characters.length)) {
    await figma.loadFontAsync(font);
  }
}

async function ensureRoute(name, y, titleText, noteText) {
  const matches = parent.children.filter(node => node.name === name);
  if (matches.length > 1) throw new Error(`duplicate ${name}`);
  let frame;
  if (matches.length === 1) {
    frame = matches[0];
    if (frame.type !== "FRAME") throw new Error(`${name} type drift`);
  } else {
    frame = expression.clone();
    parent.appendChild(frame);
  }
  frame.name = name;
  frame.x = 40;
  frame.y = y;
  frame.resize(1360, 148);
  const texts = frame.findAll(node => node.type === "TEXT");
  if (texts.length < 2) throw new Error(`${name} presentation drift`);
  await loadTextFonts(texts[0]);
  await loadTextFonts(texts[1]);
  texts[0].characters = titleText;
  texts[1].characters = noteText;
  return frame;
}

const sprite = await ensureRoute(
  "Sprite Action Runs", 408, "Sprite Action Runs",
  "Base Tool Hub exact destination for reviewed sprite action / pose-sequence atlas deliveries."
);
const effect = await ensureRoute(
  "Effect Runs", 576, "Effect Runs",
  "Base Tool Hub exact destination for reviewed effect-stage atlas deliveries."
);
return JSON.stringify({sprite_action_runs: sprite.id, effect_runs: effect.id});
```

Do not rename or reposition `Expression Runs` or the hidden project marker.

- [ ] **Step 3: Read back every new node after each write**

For each of 16 nodes, confirm through Figma metadata:

```text
node.type == FRAME
node.name == canonical name
node.parent == exact Generated Assets parent
Sprite Action geometry == x40/y408/1360x148
Effect geometry == x40/y576/1360x148
exact sibling name count == 1
existing marker still present and unchanged
```

- [ ] **Step 4: Record exact observed IDs in the evidence document**

Write one row per project:

```markdown
| project_id | file_key | parent | marker | Sprite Action Runs | Effect Runs | readback |
| ... | ... | ... | ... | <real node id> | <real node id> | PASS |
```

The document also records the Base main SHA used for preflight and states `LOCALHOST_BRIDGE_RECEIPT: NOT_RUN`.

- [ ] **Step 5: Gate the next task on complete evidence**

Count exactly 8 rows, 16 non-empty route IDs, and ensure within each project the parent, marker, Expression destination, Sprite destination, and Effect destination IDs are all distinct. If any Figma file failed, stop with the Base route registry still at 8 entries.

- [ ] **Step 6: Commit only the readback evidence**

```bash
git add docs/evidence/2026-08-16-sprite-effect-figma-route-readback.md
git commit -m "docs: record reviewed sprite and effect Figma route nodes"
```

---

### Task 3: Expand the canonical registry to 24 exact routes

**Files:**
- Modify: `docs/operations/PROJECT_FIGMA_TOOL_ROUTE_REGISTRY.json`
- Modify: `tests/test_tool_hub_subscription_production_contract.py`
- Test: `tools/tool-hub/tests/test_figma_exact_tool_route.py`

**Interfaces:**
- Consumes: complete `figma_route_nodes` evidence from Task 2.
- Produces: 24 `READY_FOR_DELIVERY` project/tool route pairs; existing 8 Character entries remain byte-equivalent in semantic fields.

- [ ] **Step 1: Append two entries per project using only Task 2 observed node IDs**

Each `sprite_action_runs` entry has:

```json
{
  "project_id": "<same project as existing entry>",
  "tool_route_id": "sprite_action_runs",
  "figma_file_key": "<same existing file key>",
  "parent_node_id": "<same existing Generated Assets parent>",
  "parent_node_type": "FRAME",
  "destination_node_id": "<Task 2 Sprite Action Runs id>",
  "destination_node_type": "FRAME",
  "destination_name": "Sprite Action Runs",
  "project_marker_node_id": "<same existing marker>",
  "project_marker_node_type": "FRAME",
  "project_marker_name": "Base Tool Hub Route · <project_id>",
  "delivery_status": "READY_FOR_DELIVERY"
}
```

The `effect_runs` entry is identical except route ID, Task 2 Effect node ID, and `destination_name: "Effect Runs"`.

- [ ] **Step 2: Strengthen registry collision validation for sibling destinations**

In `ProjectFigmaToolRouteRegistry.__init__`, add a per-project destination uniqueness check so two active route IDs for the same project cannot point at the same destination node:

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

- [ ] **Step 3: Run the registry-focused tests**

Run:

```bash
python -m pytest -q \
  tests/test_tool_hub_subscription_production_contract.py \
  tools/tool-hub/tests/test_figma_exact_tool_route.py
```

Expected state after this task: 24-route registry assertions pass; Sprite Tool Hub delivery tests may still fail because explicit route selection is not implemented yet.

- [ ] **Step 4: Commit the complete registry atomically**

```bash
git add \
  docs/operations/PROJECT_FIGMA_TOOL_ROUTE_REGISTRY.json \
  tools/base-tool-contracts/src/base_tool_contracts/figma_tool_routing.py \
  tests/test_tool_hub_subscription_production_contract.py
git commit -m "feat: register dedicated sprite and effect Figma routes"
```

---

### Task 4: Make Tool Hub route-aware without trusting browser route authority

**Files:**
- Modify: `tools/tool-hub/src/tool_hub/figma_delivery.py`
- Modify: `tools/tool-hub/src/tool_hub/studio_delivery_api.py`
- Modify: `tools/tool-hub/tests/test_figma_exact_tool_route.py`
- Modify: `tools/tool-hub/tests/test_studio_delivery_trust.py`

**Interfaces:**
- Consumes: `tool_route_id` supplied only by the authenticated Studio server client; canonical route registry from Task 3.
- Produces: `FigmaDeliveryService.enqueue(..., *, tool_route_id: str | None = None)` with a fixed authenticated-tool allowlist and route-bound idempotency.

- [ ] **Step 1: Replace the one-to-one tool map with an explicit allowlist**

In `figma_delivery.py`:

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

Change `_resolve_tool_route` to accept `requested_route_id` and resolve only that allowed route.

- [ ] **Step 2: Thread the exact route through enqueue/idempotency**

Use keyword-only route identity:

```python
def enqueue(
    self,
    tool_id: str,
    project_id: str,
    run_id: str,
    image_bytes: bytes,
    media_type: str,
    *,
    tool_route_id: str | None = None,
) -> DeliveryJob:
    route = self._resolve_tool_route(tool_id, project_id, tool_route_id)
    ...
```

and the same keyword in `enqueue_idempotent`.

Before reusing matching jobs:

```python
requested = _requested_route_id(tool_id, tool_route_id)
if any(job.tool_route_id != requested for job in matching if isinstance(job, DeliveryJob)):
    raise DeliveryError("DELIVERY_RUN_ROUTE_MISMATCH")
```

Then preserve the existing different-content check and same-run/same-SHA reuse.

- [ ] **Step 3: Revalidate stored route identity during claim/finalize/recovery**

`_assert_current_job_route` resolves using `job.tool_route_id`. For recovered jobs, read `tool_route_id` from `JOB.json`; only legacy Expression jobs may default missing route identity to `character_expression_runs`. A Sprite job without a stored route ID is invalid and must be dropped from recovery rather than guessed.

Use the same explicit job route in `_valid_recovered_receipt`.

- [ ] **Step 4: Accept one bounded private route header in the Studio delivery API**

In `studio_delivery_api.py`:

```python
_ROUTE_ID = re.compile(r"^[a-z0-9]+(?:_[a-z0-9]+)*$")


def requested_route(tool_id: str, value: str | None) -> str | None:
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

Add `x_base_tool_route: str | None = Header(default=None, alias="X-Base-Tool-Route")` to the POST endpoint and pass the validated value to `enqueue_idempotent(..., tool_route_id=route_id)`.

Do not add this header to the public browser Tool Hub API. The endpoint remains protected by the existing live-child bearer token.

- [ ] **Step 5: Keep status route-bound without accepting a second route assertion**

The status endpoint authorizes the child token, loads the stored job, and checks `job.tool_id == authenticated tool_id`; it does not accept a route header. Return the already stored `tool_route_id`/target identity.

- [ ] **Step 6: Run focused Tool Hub tests**

```bash
python -m pytest -q \
  tools/tool-hub/tests/test_figma_exact_tool_route.py \
  tools/tool-hub/tests/test_studio_delivery_trust.py \
  tools/tool-hub/tests/test_figma_delivery.py \
  tools/tool-hub/tests/test_figma_delivery_hardening.py \
  tools/tool-hub/tests/test_figma_delivery_concurrency.py
```

Expected: Expression tests remain green; valid Sprite Action/Effect routes green; missing/wrong route and route drift fail closed as asserted.

- [ ] **Step 7: Commit Tool Hub route enforcement**

```bash
git add \
  tools/tool-hub/src/tool_hub/figma_delivery.py \
  tools/tool-hub/src/tool_hub/studio_delivery_api.py \
  tools/tool-hub/tests/test_figma_exact_tool_route.py \
  tools/tool-hub/tests/test_studio_delivery_trust.py
git commit -m "feat(tool-hub): enforce exact sprite and effect delivery routes"
```

---

### Task 5: Share the loopback Hub client and add Sprite confirmed-atlas delivery

**Files:**
- Create: `tools/base-tool-contracts/src/base_tool_contracts/hub_delivery.py`
- Modify: `tools/base-tool-contracts/src/base_tool_contracts/__init__.py`
- Modify: `tools/expression-studio/src/expression_studio/hub_delivery.py`
- Modify: `tools/sprite-animation-studio/src/sprite_animation_studio/service.py`
- Modify: `tools/sprite-animation-studio/src/sprite_animation_studio/app.py`
- Test: `tools/sprite-animation-studio/tests/test_hub_delivery.py`
- Regression: Expression Studio Hub-delivery tests already present in its test suite.

**Interfaces:**
- Produces shared `LocalHubDeliveryClient.__call__(run_id, image_bytes, media_type, tool_route_id=None)` and `status(delivery_id)`.
- Produces `SpriteAnimationService.delivery_route_id(run_id) -> str` and Sprite API endpoints that bind one exported atlas SHA to one route/delivery identity.

- [ ] **Step 1: Promote the existing Expression loopback client into base-tool-contracts without changing its security behavior**

Move/copy the existing implementation semantics from `expression_studio/hub_delivery.py` into `base_tool_contracts/hub_delivery.py`. Preserve:

```text
http://127.0.0.1:<port> only
no proxy use
child-only bearer token length check
5 second timeout
64 KiB response cap
strict JSON object response
BASE_TOOL_HUB_DELIVERY_ORIGIN + BASE_TOOL_HUB_DELIVERY_TOKEN environment pair
```

Extend only the call signature and optional header:

```python
class HubDeliverySender(Protocol):
    def __call__(
        self,
        run_id: str,
        image_bytes: bytes,
        media_type: str,
        tool_route_id: str | None = None,
    ) -> dict[str, object]: ...


def __call__(self, run_id, image_bytes, media_type, tool_route_id=None):
    headers = {}
    if tool_route_id is not None:
        if re.fullmatch(r"[a-z0-9]+(?:_[a-z0-9]+)*", tool_route_id) is None:
            raise HubDeliveryError("delivery tool route identity is invalid")
        headers["X-Base-Tool-Route"] = tool_route_id
    return self._json_request(..., extra_headers=headers)
```

Implement `_json_request(..., extra_headers: dict[str, str] | None = None)` by merging only the caller-provided bounded internal headers after constructing Authorization/Accept/Content-Type.

- [ ] **Step 2: Preserve Expression import compatibility**

Replace `tools/expression-studio/src/expression_studio/hub_delivery.py` with a compatibility re-export:

```python
from base_tool_contracts.hub_delivery import (
    HubDeliveryError,
    HubDeliverySender,
    LocalHubDeliveryClient,
    sender_from_environment,
)

__all__ = [
    "HubDeliveryError",
    "HubDeliverySender",
    "LocalHubDeliveryClient",
    "sender_from_environment",
]
```

Export the same names from `base_tool_contracts.__init__`. Expression app continues calling the sender with three arguments, so Tool Hub applies the only valid legacy default: `character_expression_runs`.

- [ ] **Step 3: Add server-owned Sprite run-mode→route resolution**

In `SpriteAnimationService`:

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

Do not accept a route ID as an endpoint body/query parameter.

- [ ] **Step 4: Add Sprite confirmed delivery state to `create_app`**

Add `hub_delivery_sender: HubDeliverySender | None = None`, resolve `sender_from_environment()` when omitted, and maintain a lock-protected `confirmed_deliveries: dict[str, dict[str, object]]` analogous to Expression Studio.

Add a private normalization helper that requires:

```python
expected_target = {
    "sprite_action_runs": "Sprite Action Runs",
    "effect_runs": "Effect Runs",
}[route_id]
```

and verifies Tool Hub response fields equal:

```text
tool_id = sprite-animation-studio
project_id = record.request.project_id
run_id = exact run
content_sha256 = exported atlas SHA
tool_route_id = derived route_id
target_node_name = expected_target
delivery_id stable
bridge/delivery states internally consistent
figma_url = https://www.figma.com/design/...
```

- [ ] **Step 5: Add `POST /api/runs/{run_id}/confirm-delivery` with no route/body authority**

Require an already exported run. The endpoint does not re-curate or choose a file. Core flow:

```python
record = service.get_run(run_id)
if record.status != "exported" or record.export is None:
    raise RunBlockedError("an exported run is required before confirmation")
service.prepare_figma_delivery(run_id)  # revalidates export + anchor evidence
route_id = service.delivery_route_id(run_id)
expected_sha256 = record.export_output_sha256.get("atlas")
if expected_sha256 is None:
    raise RunBlockedError("confirmed atlas hash evidence is unavailable")
atlas_bytes = _read_staged_file(
    project_root,
    record.export.atlas,
    expected_sha256=expected_sha256,
)
if sender is None:
    raise HubDeliveryError("Tool Hub confirmed delivery is unavailable")
delivery = sender(run_id, atlas_bytes, "image/png", route_id)
```

Normalize and cache only after exact identity verification. Retry returns the same cached identity; the Tool Hub itself remains the final same-run/same-route/same-SHA idempotency authority.

- [ ] **Step 6: Add status refresh and confirmed atlas download**

Add:

```text
GET /api/runs/{run_id}/delivery-status
GET /api/runs/{run_id}/confirmed-download
```

Status refresh re-reads the atlas with the cached SHA before calling `sender.status(delivery_id)`, and rejects route/target/delivery/SHA changes. Download returns only the same atlas bytes with `X-Content-SHA256` and a filename such as `atlas-<first12run>.png`.

- [ ] **Step 7: Run shared-client, Sprite, and Expression regressions**

```bash
python -m pytest -q \
  tools/sprite-animation-studio/tests/test_hub_delivery.py \
  tools/sprite-animation-studio/tests/test_api.py \
  tools/sprite-animation-studio/tests/test_delivery.py \
  tools/expression-studio/tests \
  tools/tool-hub/tests/test_studio_delivery_trust.py
```

Expected: new Sprite confirmed-atlas tests pass; Expression delivery/import behavior remains unchanged.

- [ ] **Step 8: Commit shared client and Sprite delivery lifecycle**

```bash
git add \
  tools/base-tool-contracts/src/base_tool_contracts/hub_delivery.py \
  tools/base-tool-contracts/src/base_tool_contracts/__init__.py \
  tools/expression-studio/src/expression_studio/hub_delivery.py \
  tools/sprite-animation-studio/src/sprite_animation_studio/service.py \
  tools/sprite-animation-studio/src/sprite_animation_studio/app.py \
  tools/sprite-animation-studio/tests/test_hub_delivery.py
git commit -m "feat(sprite-studio): confirm exact atlas delivery through Tool Hub"
```

---

### Task 6: Expose the safe Sprite confirmation UX and update operator docs

**Files:**
- Modify: `tools/sprite-animation-studio/web/index.html`
- Modify: `tools/sprite-animation-studio/web/app.js`
- Modify: `tools/sprite-animation-studio/README.md`
- Modify: `tools/sprite-animation-studio/tests/test_docs_contract.py`
- Modify: `tests/test_tool_hub_subscription_production_contract.py`

**Interfaces:**
- Consumes: server endpoints from Task 5.
- Produces: user-facing `확정 및 전달`, delivery status refresh, pairing guidance, and confirmed-atlas download without browser route authority.

- [ ] **Step 1: Add UX contract assertions before changing the web files**

Tests must require the Sprite web source to contain endpoint usage for:

```text
/api/runs/${runId}/confirm-delivery
/api/runs/${runId}/delivery-status
confirmed-download
확정 및 전달
Sprite Action Runs
Effect Runs
```

and must reject browser-side strings/fields that attempt to send:

```text
figma_file_key
target_node_id
generation_area_node_id
project_marker_node_id
X-Base-Tool-Route
```

The private header belongs only in the Python shared Hub client, never browser JavaScript.

- [ ] **Step 2: Replace the old project-GPT delivery action with the confirmed Hub path**

After a successful export, enable `확정 및 전달`. Its request body is empty:

```javascript
const confirmation = await api(`/api/runs/${encodeURIComponent(runId)}/confirm-delivery`, {
  method: "POST"
});
```

Render server-returned state only: target name, bridge state, pairing code if present, verified/pending state, and download URL. Do not derive a route from the browser's mode control.

- [ ] **Step 3: Add status refresh without route selection**

```javascript
const status = await api(`/api/runs/${encodeURIComponent(runId)}/delivery-status`);
```

When `figma_delivery === "VERIFIED"`, show the canonical target name returned by the server. Pairing instructions may show the Figma URL/code returned by Tool Hub but never expose file keys or node IDs.

- [ ] **Step 4: Update Sprite README truthfully**

Document:

```text
pose_sequence/sprite_action -> Sprite Action Runs
effect_stages -> Effect Runs
expression_variation -> delivery unavailable in this slice
confirmed Figma payload -> exported atlas PNG
real ChatGPT Pro visual-quality / user-PC / live Bridge receipt -> still NOT_RUN until observed
```

Remove historical prose that says all dedicated Sprite/Effect routes are unavailable after the new registry is merged.

- [ ] **Step 5: Run web/docs contracts**

```bash
python -m pytest -q \
  tools/sprite-animation-studio/tests/test_docs_contract.py \
  tools/sprite-animation-studio/tests/test_hub_delivery.py \
  tests/test_tool_hub_subscription_production_contract.py
```

- [ ] **Step 6: Commit the UX/docs slice**

```bash
git add \
  tools/sprite-animation-studio/web/index.html \
  tools/sprite-animation-studio/web/app.js \
  tools/sprite-animation-studio/README.md \
  tools/sprite-animation-studio/tests/test_docs_contract.py \
  tests/test_tool_hub_subscription_production_contract.py
git commit -m "feat(sprite-studio): expose confirmed dedicated Figma delivery"
```

---

### Task 7: Cross-platform GREEN, adversarial review, and latest-main reconciliation

**Files:**
- Modify if needed: `.github/workflows/validate-provisional-figma-integration.yml`
- No new product scope.

**Interfaces:**
- Consumes: Tasks 1–6 complete implementation.
- Produces: exact-head GREEN implementation PR with current-main reconciliation and no unresolved P0/P1 findings.

- [ ] **Step 1: Run the entire focused local suite**

```bash
python -m pytest -q \
  tools/tool-hub/tests/test_figma_delivery.py \
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

No failing test may be dismissed as unrelated without reproducing it on current `main` and recording that baseline separately.

- [ ] **Step 2: Verify the dedicated workflow actually runs the new tests on both OSes**

Push the implementation branch and inspect `Validate Provisional Figma Integration`. Confirm Ubuntu and Windows both execute the named Sprite/Tool Hub/root contract files, not just that the workflow itself exists.

Also require the normal Base operating gates triggered by the diff, including Base v9 and Game Project Operating System/`ci-gate` where applicable.

- [ ] **Step 3: Run adversarial reconciliation checks**

Attack at least these cases in tests/review:

```text
sprite child requests character route
expression child requests effect route
sprite child omits route
same run + same bytes + changed route
same run + changed bytes
atlas changed after export
registry node renamed/reparented
marker drift
generic Generated Assets fallback
browser injects route/node/file fields
recovered sprite job lacks route identity
```

Decision target: P0/P1 = 0; any unresolved fail-open behavior blocks merge.

- [ ] **Step 4: Re-read latest Base main and open PR changed paths**

If `main` moved, reconcile by non-force merge/copy integration onto the implementation branch, keeping source owner branches untouched. If another open PR now owns a changed path, compare material deltas; absorb approved compatible material onto the integration branch rather than waiting for the owner PR to merge.

- [ ] **Step 5: Re-run exact-head workflows after every reconciliation movement**

The head used for merge must be the head for which all required workflows are green. Record exact head SHA and the 16 Figma route IDs in the PR body.

- [ ] **Step 6: Create/refresh the implementation PR and make it ready only after GREEN**

PR body must state:

```text
24/24 registered routes
16/16 new Figma node readbacks PASS
Expression route behavior preserved
Sprite server-owned mode→route mapping implemented
confirmed payload = exported atlas SHA
user-PC/live ChatGPT/live Bridge/Godot evidence still NOT_RUN
source owner PR branches untouched
```

- [ ] **Step 7: Commit any final CI-only correction**

If the workflow needed a path/test-list correction discovered during RED/GREEN, commit only that bounded correction and rerun exact-head CI.

---

### Task 8: Merge, post-merge verification, and tracking cleanup

**Files:**
- No product changes after exact-head GREEN unless post-merge exposes a new regression.
- Update tracking: Base Issue #393 and design PR #451 disposition.

**Interfaces:**
- Consumes: exact-head GREEN implementation PR.
- Produces: new Base `main` with 24-route authority and post-merge cloud/readback evidence; live PC IRG remains separately pending.

- [ ] **Step 1: Final pre-merge re-read**

Immediately before merge verify:

```text
Base main SHA unchanged since final reconciliation
implementation head SHA unchanged
24 registry pairs present on head
16 Figma new nodes still exact name/type/parent
unresolved review threads = 0
required workflows = success
```

- [ ] **Step 2: Merge with expected-head protection**

Use squash merge with the exact verified head SHA. Do not use admin/ruleset bypass.

- [ ] **Step 3: Read back new main authority**

From the new Base `main`, re-read:

```text
docs/operations/PROJECT_FIGMA_TOOL_ROUTE_REGISTRY.json
tools/tool-hub/src/tool_hub/figma_delivery.py
tools/tool-hub/src/tool_hub/studio_delivery_api.py
tools/sprite-animation-studio/src/sprite_animation_studio/app.py
```

Confirm registry count = 24 and exact route names = three canonical classes.

- [ ] **Step 4: Re-read all 24 Figma destinations**

For all eight files verify the existing Expression route plus the two new routes and existing marker. Any post-merge cloud drift is reported as a route-blocking issue rather than silently patched.

- [ ] **Step 5: Verify post-merge push workflows**

Wait for all workflows triggered on the merge SHA that cover the changed paths. Confirm no in-progress/failure conclusion remains before calling the repository layer complete.

- [ ] **Step 6: Update Issue #393 with bounded evidence**

Record:

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

- [ ] **Step 7: Close/supersede #451 only after its spec/plan blobs are present on new main**

Compare the design and plan blobs in new main with #451. If the implementation PR absorbed them byte-identically, comment that #451 was superseded by the merged implementation and close it. If not, keep #451 open until documentation provenance is reconciled; do not silently lose the approved design record.

- [ ] **Step 8: Hand off to the live PC IRG**

The next action after repository/Figma route completion is the real user-PC path:

```text
Base Tool Hub.lnk
→ urban-legend
→ real ChatGPT Pro Character/Expression same-run confirmation/receipt
→ Sprite pose_sequence real sample
→ Sprite effect_stages real sample
→ exact Figma Bridge same-SHA receipts
→ Godot/project consumption
```

Do not convert cloud Figma creation or CI into those live PASS claims.
