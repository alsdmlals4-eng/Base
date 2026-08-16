# Expression Studio ChatGPT Pro Same-Run Handoff Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a server-issued pending ChatGPT Pro handoff run that imports returned `CHATGPT_INCLUDED` PNG candidates into the exact same run before existing review/export/Figma delivery.

**Architecture:** Keep the existing direct `/api/import-runs` path and all downstream review/export/delivery contracts unchanged. Add a bounded in-memory pending handoff registry inside `ExpressionStudioService`, build prompts exclusively through the existing Base subscription handoff renderer, and consume the reserved server run ID only after existing upload/anchor/evidence validation succeeds.

**Tech Stack:** Python 3.12, FastAPI, Pydantic v2, Pillow, Base `base_tool_contracts`, vanilla JS/HTML, pytest, GitHub Actions Ubuntu/Windows.

## Global Constraints

- Canonical production route remains `subscription_handoff_import` + `CHATGPT_INCLUDED`.
- `provider_call_made=false` and `requires_additional_payment=false` are fixed truth fields.
- No OpenAI API/provider generation call is added.
- Browser never creates a free-form handoff run ID.
- Existing approved-anchor, Asset Vault, Figma exact-route, download, pairing, and receipt contracts remain authoritative.
- Existing direct `/api/import-runs` remains compatible.
- No Sprite/Effect handoff UI expansion in this slice.
- No Local Executor #420 changes.
- Owner PR #373/#376/#386 branches remain READ_ONLY.

---

### Task 1: Pending handoff service contract

**Files:**
- Create: `tools/expression-studio/tests/test_subscription_handoff_run.py`
- Modify: `tools/expression-studio/src/expression_studio/service.py`

**Interfaces:**
- Consumes: `ExpressionRequest`, `resolve_expression()`, `generation_instruction(request, resolved)`, `build_subscription_handoff_packet()`, `render_chatgpt_pro_prompt()`.
- Produces: `PendingHandoff`, `ExpressionStudioService.prepare_subscription_handoff(request)`, `ExpressionStudioService.import_subscription_handoff(run_id, candidates)`.

- [ ] **Step 1: Write failing service tests**

Require preparation to return one server-generated run ID and exact subscription truth, and require successful import to preserve that same run ID:

```python
pending = service.prepare_subscription_handoff(request)
assert pending.run_id
assert pending.packet.run_id == pending.run_id
assert pending.packet.import_declared_source == "CHATGPT_INCLUDED"
assert pending.packet.provider_call_made is False
assert pending.packet.requires_additional_payment is False
assert "https://www.figma.com/" not in pending.prompt

record = service.import_subscription_handoff(pending.run_id, imported_candidates)
assert record.run_id == pending.run_id
assert record.run_mode == "subscription_handoff_import"
assert record.provider_call_made is False
```

Add adversarial tests for unknown run ID, second consume, invalid candidate count, anchor mutation between prepare/import, and invalid candidates leaving the pending record retryable.

- [ ] **Step 2: Run service RED**

Run:

```bash
python -m pytest -q tools/expression-studio/tests/test_subscription_handoff_run.py
```

Expected: FAIL because pending handoff types/methods do not exist.

- [ ] **Step 3: Add minimal pending record and shared import implementation**

Add internal state:

```python
@dataclass(frozen=True)
class PendingHandoff:
    run_id: str
    request: ExpressionRequest
    resolved: ResolvedExpression
    anchor_sha256: str
    anchor_evidence: dict[str, str]
    packet: SubscriptionHandoffPacket
    prompt: str

self._pending_handoffs: dict[str, PendingHandoff] = {}
```

`prepare_subscription_handoff()` must fully validate project ID, Figma anchor route, project-owned anchor evidence and current anchor bytes before storing the pending record. Build the packet with a display-only `Path(request.anchor.source_path).name`, `generation_instruction(request, resolved)`, the request candidate count, bounded PNG dimensions, and a fixed review checklist.

Extract current `create_import_run()` body into a private implementation that accepts a server-selected `run_id`:

```python
def _create_import_run(
    self,
    request: ExpressionRequest,
    candidates: tuple[ImportedImage, ...],
    declared_source: DeclaredSource,
    *,
    reserved_run_id: str | None = None,
) -> RunRecord:
    run_id = reserved_run_id or uuid4().hex
    ...
```

Keep public `create_import_run()` delegating with `reserved_run_id=None` so legacy behavior is unchanged.

`import_subscription_handoff()` must:

```python
pending = self._pending_handoffs.get(run_id)
if pending is None:
    raise RunNotFoundError(run_id)
record = self._create_import_run(
    pending.request,
    candidates,
    "CHATGPT_INCLUDED",
    reserved_run_id=run_id,
)
del self._pending_handoffs[run_id]
return record
```

Before delegation re-read/revalidate the exact approved anchor and require its SHA/evidence to still match the pending record. Delete pending state only after successful import.

- [ ] **Step 4: Run focused service GREEN**

```bash
python -m pytest -q tools/expression-studio/tests/test_subscription_handoff_run.py tools/expression-studio/tests/test_service.py
```

Expected: PASS.

- [ ] **Step 5: Commit Task 1**

Commit message:

```text
feat(expression-studio): add pending subscription handoff runs
```

---

### Task 2: Safe same-run handoff API

**Files:**
- Create: `tools/expression-studio/tests/test_subscription_handoff_api.py`
- Modify: `tools/expression-studio/src/expression_studio/app.py`

**Interfaces:**
- Consumes: Task 1 service methods.
- Produces: `POST /api/handoff-runs`, `POST /api/handoff-runs/{run_id}/import`.

- [ ] **Step 1: Write API RED tests**

Preparation test:

```python
response = client.post("/api/handoff-runs", json=request_payload, headers=csrf)
assert response.status_code == 201
payload = response.json()
assert payload["state"] == "GPT_PRO_HANDOFF_READY"
assert payload["generation_surface"] == "CHATGPT_PRO_SUBSCRIPTION"
assert payload["declared_source"] == "CHATGPT_INCLUDED"
assert payload["provider_call_made"] is False
assert payload["requires_additional_payment"] is False
assert payload["run_id"] in payload["prompt"]
```

Import test sends only candidate files to the server-issued URL and asserts the returned run ID is unchanged. Add tests that arbitrary/unknown IDs fail and failed image validation does not consume the pending run.

- [ ] **Step 2: Run API RED**

```bash
python -m pytest -q tools/expression-studio/tests/test_subscription_handoff_api.py
```

Expected: 404 because endpoints are absent.

- [ ] **Step 3: Implement preparation endpoint**

```python
@app.post("/api/handoff-runs", status_code=201)
def prepare_handoff(request: ExpressionRequest) -> dict[str, object]:
    pending = service.prepare_subscription_handoff(request)
    public = pending.packet.public_view()
    return {
        **public,
        "prompt": pending.prompt,
        "declared_source": pending.packet.import_declared_source,
        "run_mode": pending.packet.import_run_mode,
    }
```

Map `RunBlockedError` to 409 and `ValueError`/anchor contract errors to 422 without exposing paths or secrets.

- [ ] **Step 4: Implement same-run import endpoint**

```python
@app.post("/api/handoff-runs/{run_id}/import", status_code=201)
async def import_handoff(run_id: str, candidates: list[UploadFile] = File(...)) -> dict[str, object]:
    imported = []
    for index, upload in enumerate(candidates):
        data = await read_upload_limited(upload)
        imported.append(validate_imported_image(data, declared_source="CHATGPT_INCLUDED", order=index))
    return service.import_subscription_handoff(run_id, tuple(imported)).public_view()
```

Map unknown run to 404, consumed/conflicting state to 409, candidate/request validation to 422. Do not accept `request_json`, `declared_source`, project ID, or user-provided run truth on this endpoint.

- [ ] **Step 5: Run API + existing import GREEN**

```bash
python -m pytest -q \
  tools/expression-studio/tests/test_subscription_handoff_api.py \
  tools/expression-studio/tests/test_character_import_api.py \
  tools/expression-studio/tests/test_confirm_delivery.py
```

Expected: PASS.

- [ ] **Step 6: Commit Task 2**

```text
feat(expression-studio): expose same-run subscription handoff API
```

---

### Task 3: Canonical Character Studio handoff UI

**Files:**
- Modify: `tools/expression-studio/web/index.html`
- Modify: `tools/expression-studio/web/app.js`
- Modify: `tools/expression-studio/tests/test_web_contract.py`

**Interfaces:**
- Consumes: Task 2 endpoints.
- Produces: user flow `프롬프트 준비 -> PNG 선택 -> 같은 Run 가져오기 -> existing review/confirm`.

- [ ] **Step 1: Write UI contract RED**

Require stable DOM IDs and canonical labels:

```python
assert 'id="prepare-handoff-button"' in html
assert 'id="handoff-prompt"' in html
assert 'id="import-handoff-button"' in html
assert "ChatGPT Pro 프롬프트 준비" in html
assert "같은 Run으로 후보 가져오기" in html
assert 'request("/api/handoff-runs"' in javascript
assert '`/api/handoff-runs/${pendingHandoffRunId}/import`' in javascript
```

Also assert normal `확정 및 전달`, PC download, Figma pairing/refresh and legacy direct import contracts remain present.

- [ ] **Step 2: Run UI RED**

```bash
python -m pytest -q tools/expression-studio/tests/test_web_contract.py
```

Expected: FAIL only for missing handoff UI/JS contract.

- [ ] **Step 3: Add handoff preparation surface**

In subscription mode show a canonical handoff section containing:

```html
<button id="prepare-handoff-button" type="button">ChatGPT Pro 프롬프트 준비</button>
<textarea id="handoff-prompt" readonly hidden></textarea>
<p id="handoff-run-info" hidden></p>
<button id="import-handoff-button" type="button" disabled>같은 Run으로 후보 가져오기</button>
```

Preparation handler posts `requestPayload()` to `/api/handoff-runs`, stores only the returned server `run_id`, displays the prompt, and enables same-run import after the exact candidate file count is selected.

- [ ] **Step 4: Add same-run import action**

Build FormData with candidate files only and call:

```javascript
request(`/api/handoff-runs/${pendingHandoffRunId}/import`, { method: "POST", body })
```

On success clear pending handoff UI state and pass the returned run through the same existing candidate rendering path used by direct imports. Do not duplicate review/export/delivery logic.

Keep a secondary legacy import action for Figma/local/other user-supplied candidates; the canonical ChatGPT source path must not ask the user to re-enter a declared source.

- [ ] **Step 5: Run UI GREEN**

```bash
python -m pytest -q \
  tools/expression-studio/tests/test_web_contract.py \
  tools/expression-studio/tests/test_character_surface_contract.py
```

Expected: PASS.

- [ ] **Step 6: Commit Task 3**

```text
feat(expression-studio): connect ChatGPT Pro handoff UI to same run
```

---

### Task 4: Composed regressions and adversarial closeout

**Files:**
- Modify only if a regression exposes a specific defect.
- Reuse all existing workflow/test files unless a new focused gate is required.

**Interfaces:**
- Consumes: Tasks 1-3 complete flow.
- Produces: exact-head evidence for Issue #427 work order item 4.

- [ ] **Step 1: Run focused local/CI-compatible suites**

```bash
python -m pytest -q \
  tools/expression-studio/tests/test_subscription_handoff_run.py \
  tools/expression-studio/tests/test_subscription_handoff_api.py \
  tools/expression-studio/tests/test_character_import_api.py \
  tools/expression-studio/tests/test_confirm_delivery.py \
  tools/expression-studio/tests/test_web_contract.py
```

- [ ] **Step 2: Run existing Ubuntu/Windows workflows on exact head**

Require SUCCESS for:

- Validate Visual Studio Subscription Import Portability
- Validate Tool Hub Subscription Contracts
- Validate Provisional Character Integration
- Validate Provisional Confirm Delivery
- Validate Provisional Figma Integration
- Validate Tool Hub Windows Child Ownership
- Validate Base v9 Operating Contracts
- Dependency Review

- [ ] **Step 3: Re-run real Windows four-child smoke**

Require the existing Windows workflow to launch Expression+Sprite for two isolated projects, import/export the reviewed candidates, and terminate the owned process trees without cross-project files.

- [ ] **Step 4: Adversarial regression checklist**

Confirm with tests/code review:

```text
P0/P1 = 0
browser cannot choose project/run/source truth for same-run handoff
unknown/replayed pending run fails closed
failed import remains retryable without duplicate Asset Vault run
prompt contains no Figma/private routing or credential material
provider_call_made=false
requires_additional_payment=false
existing direct import still works
existing confirm/download/Figma receipt flow unchanged
```

- [ ] **Step 5: Re-read main and owner PR heads**

If main or #373/#376/#386 moved, semantically reconcile before any completion claim. Do not write to owner branches.

- [ ] **Step 6: Update PR #428 description only after exact-head verification**

Replace stale “plan-only” TDD state with actual implemented and verified state, while retaining `DO_NOT_MERGE_PROVISIONAL` and the IRG ceiling.

- [ ] **Step 7: Do not merge**

Stop with PR #428 draft/open unless owner resolution or new explicit user authorization changes the merge boundary.
