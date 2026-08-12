# Base Tool Hub Phase 0 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make Expression Studio and Sprite Animation Studio fail closed before Tool Hub can expose them across projects.

**Architecture:** Each Studio remains an independent localhost FastAPI package. Engines declare immutable provenance and delivery eligibility; services own export/delivery gates, project-bound Figma anchor validation, and verified project-local vault staging. Browser state comes from server config rather than editable project identity.

**Tech Stack:** Python 3.12, FastAPI, Pydantic v2, Pillow, pytest, browser JavaScript.

## Global Constraints

- Work Mode is `BUILD`; approved scope is Phase 0/0.5 only.
- Simulated or unchanged fixture output must never be exportable or Figma-delivery eligible.
- Production generation, paid provider smoke, live Figma placement, and Windows concurrency remain `BLOCKED_UNVERIFIED` until separately evidenced.
- Figma is a `VISUAL_WORKSPACE`, not approval canon or process host.
- Generated candidates live only in verified `.asset-vault/library/generated/<tool-id>/...` staging; browser-controlled output roots are rejected.
- Existing user changes and project registry entries must be preserved.

---

### Task 1: Engine provenance and simulated-delivery gate

**Files:**
- Modify: `tools/expression-studio/src/expression_studio/engine.py`
- Modify: `tools/expression-studio/src/expression_studio/service.py`
- Modify: `tools/expression-studio/tests/test_service.py`
- Modify: `tools/expression-studio/tests/test_api.py`
- Modify: `tools/sprite-animation-studio/src/sprite_animation_studio/engine.py`
- Modify: `tools/sprite-animation-studio/src/sprite_animation_studio/service.py`
- Modify: `tools/sprite-animation-studio/tests/test_api.py`

**Interfaces:**
- Produces: `EngineProvenance = Literal["simulated", "openai", "pinned_sprite_gen"]`.
- Produces: `EngineResult.provenance: str` and `EngineResult.delivery_eligible: bool`.
- Service export and delivery methods reject `delivery_eligible=False`.

- [ ] **Step 1: Write failing tests for both services**

```python
def test_simulated_result_cannot_be_exported_or_delivered(tmp_path: Path) -> None:
    client = client_for(tmp_path)
    run_id = client.post("/api/runs", json=valid_payload()).json()["run_id"]
    response = client.post(f"/api/runs/{run_id}/export", json=selection_payload())
    assert response.status_code == 409
    assert "simulated" in response.json()["detail"]
```

- [ ] **Step 2: Run each focused test and verify RED because fake results currently export**

Run: `cd tools/expression-studio && PYTHONPATH=src ../../.venv/bin/python -m pytest tests/test_api.py -q`

Run: `cd tools/sprite-animation-studio && PYTHONPATH=src ../../.venv/bin/python -m pytest tests/test_api.py -q`

- [ ] **Step 3: Add immutable provenance and gate in service**

```python
@dataclass(frozen=True)
class EngineResult:
    candidates: tuple[Path, ...]
    generation_instruction: str
    provenance: str
    delivery_eligible: bool

def _require_delivery_eligible(record: RunRecord) -> None:
    if record.result is None or not record.result.delivery_eligible:
        raise RunBlockedError("simulated engine output is not eligible for export or Figma delivery")
```

- [ ] **Step 4: Run `tests/test_service.py tests/test_api.py` for Expression and `tests/test_api.py` for Sprite, then each full package suite; require exit 0**

- [ ] **Step 5: Commit only Task 1 files**

```bash
git commit -m "fix: block simulated studio delivery"
```

### Task 2: Canonical project config and bound Figma anchor route

**Files:**
- Modify: `tools/expression-studio/src/expression_studio/models.py`
- Modify: `tools/expression-studio/src/expression_studio/service.py`
- Modify: `tools/expression-studio/src/expression_studio/app.py`
- Modify: `tools/sprite-animation-studio/src/sprite_animation_studio/models.py`
- Modify: `tools/sprite-animation-studio/src/sprite_animation_studio/service.py`
- Modify: `tools/sprite-animation-studio/src/sprite_animation_studio/app.py`
- Test: `tools/expression-studio/tests/test_api.py`
- Test: `tools/expression-studio/tests/test_delivery.py`
- Test: `tools/sprite-animation-studio/tests/test_api.py`
- Test: `tools/sprite-animation-studio/tests/test_delivery.py`
- Modify: `tools/expression-studio/web/app.js`
- Modify: `tools/expression-studio/web/index.html`
- Modify: `tools/sprite-animation-studio/web/app.js`
- Modify: `tools/sprite-animation-studio/web/index.html`

**Interfaces:**
- Produces: `GET /api/config` with immutable `project_id`, engine provenance, delivery eligibility, and routing state.
- Produces: anchor validator that requires `https://www.figma.com/design/<bound-file-key>/...?node-id=<canonical-id>` for approved delivery lineage.

- [ ] **Step 1: Write failing API tests**

```python
def test_config_exposes_bound_project_and_simulated_state(tmp_path: Path) -> None:
    response = client_for(tmp_path, project_id="demo").get("/api/config")
    assert response.json() == {
        "project_id": "demo",
        "engine_provenance": "simulated",
        "delivery_eligible": False,
        "routing_state": "ROUTING_CONFIGURED",
    }
```

```python
def test_anchor_from_another_figma_file_is_rejected(tmp_path: Path) -> None:
    payload = valid_payload()
    payload["anchor"]["figma_node_url"] = "https://www.figma.com/design/WRONG/source?node-id=1-2"
    response = client_for(tmp_path).post("/api/runs", json=payload)
    assert response.status_code == 422
```

- [ ] **Step 2: Verify RED**
- [ ] **Step 3: Implement config response and registry-owned anchor validation**
- [ ] **Step 4: Bootstrap the project ID from `/api/config`; remove editable `demo` defaults**
- [ ] **Step 5: Run API, web-contract, and JS syntax tests**
- [ ] **Step 6: Commit Task 2 files**

### Task 3: Verified vault staging

**Files:**
- Modify: `tools/expression-studio/src/expression_studio/models.py`
- Modify: `tools/expression-studio/src/expression_studio/paths.py`
- Modify: `tools/expression-studio/src/expression_studio/service.py`
- Modify: `tools/sprite-animation-studio/src/sprite_animation_studio/models.py`
- Modify: `tools/sprite-animation-studio/src/sprite_animation_studio/paths.py`
- Modify: `tools/sprite-animation-studio/src/sprite_animation_studio/service.py`
- Test: `tools/expression-studio/tests/test_models.py`
- Test: `tools/expression-studio/tests/test_service.py`
- Test: `tools/sprite-animation-studio/tests/test_models.py`
- Test: `tools/sprite-animation-studio/tests/test_paths.py`
- Modify: `tools/expression-studio/web/index.html`
- Modify: `tools/expression-studio/web/app.js`
- Modify: `tools/sprite-animation-studio/web/index.html`
- Modify: `tools/sprite-animation-studio/web/app.js`

**Interfaces:**
- Produces: fixed relative root `.asset-vault/library/generated/<tool-id>`.
- Consumes: project root with initialized `.asset-vault/library` and `.gitignore` coverage.
- Rejects: symlink roots, `.git`, tracked/protected target roots, and free-form browser `output_root`.

- [ ] **Step 1: Write failing tests for missing vault, symlink escape, and exact output shape**

```python
def test_missing_project_vault_blocks_generation(tmp_path: Path) -> None:
    response = client_for(tmp_path, initialize_vault=False).post("/api/runs", json=valid_payload())
    assert response.status_code == 422
    assert "asset vault" in response.json()["detail"]
```

- [ ] **Step 2: Verify RED**
- [ ] **Step 3: Replace request-selected output root with service-owned vault paths**
- [ ] **Step 4: Update browser payloads and docs**
- [ ] **Step 5: Run full Studio suites**
- [ ] **Step 6: Commit Task 3 files**

### Task 4: Localhost mutation boundary and health identity

**Files:**
- Create: `tools/expression-studio/src/expression_studio/security.py`
- Create: `tools/sprite-animation-studio/src/sprite_animation_studio/security.py`
- Modify: `tools/expression-studio/src/expression_studio/app.py`
- Modify: `tools/sprite-animation-studio/src/sprite_animation_studio/app.py`
- Test: `tools/expression-studio/tests/test_api.py`
- Test: `tools/sprite-animation-studio/tests/test_api.py`
- Modify: `tools/expression-studio/web/app.js`
- Modify: `tools/sprite-animation-studio/web/app.js`

**Interfaces:**
- Produces: `GET /api/status` with tool ID, project ID, engine state, per-launch nonce, and config hash.
- Requires: exact loopback Host, allowed Origin, same-site session cookie, and `X-Studio-CSRF` for mutation endpoints.

- [ ] **Step 1: Write failing tests for hostile Host/Origin and missing CSRF**
- [ ] **Step 2: Verify RED**
- [ ] **Step 3: Add middleware and server-generated CSRF bootstrap**
- [ ] **Step 4: Add authenticated status identity and browser headers**
- [ ] **Step 5: Run API regression tests**
- [ ] **Step 6: Commit Task 4 files**

### Task 5: CLI port and user-facing truthful state

**Files:**
- Modify: `tools/sprite-animation-studio/src/sprite_animation_studio/app.py`
- Modify: `tools/expression-studio/README.md`
- Modify: `tools/expression-studio/web/app.js`
- Modify: `tools/expression-studio/web/index.html`
- Modify: `tools/sprite-animation-studio/README.md`
- Modify: `tools/sprite-animation-studio/web/app.js`
- Modify: `tools/sprite-animation-studio/web/index.html`
- Test: `tools/expression-studio/tests/test_docs_contract.py`
- Test: `tools/expression-studio/tests/test_web_contract.py`
- Test: `tools/expression-studio/tests/test_api.py`
- Test: `tools/sprite-animation-studio/tests/test_docs_contract.py`
- Test: `tools/sprite-animation-studio/tests/test_web_contract.py`
- Test: `tools/sprite-animation-studio/tests/test_api.py`

**Interfaces:**
- Sprite CLI gains `--port` with range `1..65535`.
- UI prominently displays `SIMULATED / DELIVERY_BLOCKED` and disables export/Figma actions.

- [ ] **Step 1: Write failing CLI/parser and web behavior tests**
- [ ] **Step 2: Verify RED**
- [ ] **Step 3: Implement explicit port and truthful UI state**
- [ ] **Step 4: Run both full suites and `node --check`**
- [ ] **Step 5: Commit Task 5 files**

### Task 6: Phase 0 regression and adversarial review

**Files:**
- Modify: only exact Phase 0 files identified by a P0/P1 review finding; add the corresponding package test before production changes.

- [ ] **Step 1: Run Expression suite independently**
- [ ] **Step 2: Run Sprite suite independently**
- [ ] **Step 3: Run Base local validation with exact trusted main SHA**
- [ ] **Step 4: Run adversarial review against fake bypass, cross-project, path escape, and false Figma claims**
- [ ] **Step 5: Fix P0/P1 findings through fresh RED/GREEN cycles**
- [ ] **Step 6: Record unrun production/Windows/Figma evidence as `BLOCKED_UNVERIFIED`**
