# Expression Studio Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a local FACS-inspired character-expression tool that preserves an approved anchor, validates bounded controls, exports an explicitly selected candidate, and prepares an exact-project Figma delivery packet.

**Architecture:** Create an independent `tools/expression-studio` FastAPI/Pydantic/Pillow package patterned after the existing Sprite Animation Studio lifecycle, but with a single selected still image instead of frames or an atlas. A dedicated control catalog resolves product IDs into natural-language image-edit instructions and detects incompatible combinations before the engine runs. The tool reads the existing project Figma registry but never owns credentials or performs a Figma mutation.

**Tech Stack:** Python 3.10+, FastAPI, Pydantic 2, Pillow, pytest, vanilla HTML/CSS/JavaScript.

## Global Constraints

- Use no additional runtime dependency beyond FastAPI, Pydantic, Pillow, and Uvicorn.
- Treat the user-supplied reference grid as a product-control reference, not proof that every label is canonical FACS.
- No image generation provider credential, ZIP artifact, external network call, or direct Figma mutation client.
- Require an approved existing local anchor and a configured matching `--project-id` for project delivery.
- Persist every generated/exported artifact only under the configured project-relative output root.
- Figma delivery packets are `ready_for_project_gpt`, never an upload-success claim.
- Preserve the existing Sprite Animation Studio behaviour and its project registry schema/version.

---

### Task 1: Define and test the expression request contract

**Files:**
- Create: `tools/expression-studio/pyproject.toml`
- Create: `tools/expression-studio/src/expression_studio/__init__.py`
- Create: `tools/expression-studio/src/expression_studio/models.py`
- Create: `tools/expression-studio/tests/test_models.py`

**Interfaces:**
- Produces: `ExpressionRequest`, `ExpressionAnchor`, `FaceControl`, `ExpressionPreset`, `Intensity`, `Gaze`, and `HeadPose`.
- Consumed by: catalog, engine, lineage, service, API, and web UI.

- [ ] **Step 1: Write the failing model tests**

```python
def test_wink_request_accepts_an_approved_character_anchor() -> None:
    request = ExpressionRequest.model_validate(valid_payload(controls=[{"code": "AU46", "intensity": "C"}]))
    assert request.controls[0].code == "AU46"

def test_request_rejects_more_than_four_face_controls() -> None:
    with pytest.raises(ValueError, match="at most 4"):
        ExpressionRequest.model_validate(valid_payload(controls=[{"code": "AU1", "intensity": "A"}] * 5))
```

- [ ] **Step 2: Run the model tests and verify RED**

Run: `cd tools/expression-studio && PYTHONPATH=src ../../.venv/bin/python -m pytest tests/test_models.py -q`

Expected: FAIL because `expression_studio.models` does not exist.

- [ ] **Step 3: Implement the minimal Pydantic models**

```python
class FaceControl(BaseModel):
    model_config = ConfigDict(extra="forbid")
    code: str = Field(pattern=r"^AU[0-9]+$")
    intensity: Literal["A", "B", "C", "D", "E"]
    side: Literal["left", "right"] | None = None

class ExpressionRequest(BaseModel):
    project_id: str = Field(pattern=r"^[A-Za-z0-9_-]+$")
    asset_id: str = Field(pattern=r"^[A-Za-z0-9_-]+$")
    anchor: ExpressionAnchor
    controls: list[FaceControl] = Field(default_factory=list, max_length=4)
    gaze: Gaze = "center"
    head_pose: HeadPose = "neutral"
    preset: ExpressionPreset | None = None
    candidate_count: int = Field(ge=1, le=8)
    output_root: str
```

Include validators for a character-only approved anchor, relative output path, and at least one direct control or preset.

- [ ] **Step 4: Run the model tests and verify GREEN**

Run: `cd tools/expression-studio && PYTHONPATH=src ../../.venv/bin/python -m pytest tests/test_models.py -q`

Expected: PASS.

- [ ] **Step 5: Commit the completed contract task**

```bash
git add tools/expression-studio/pyproject.toml tools/expression-studio/src/expression_studio tools/expression-studio/tests/test_models.py
git commit -m "feat: add expression request contract"
```

### Task 2: Add a curated control catalog and conflict detection

**Files:**
- Create: `tools/expression-studio/src/expression_studio/catalog.py`
- Create: `tools/expression-studio/tests/test_catalog.py`

**Interfaces:**
- Consumes: `FaceControl`, `ExpressionPreset`, `ExpressionRequest` from `models.py`.
- Produces: `ResolvedExpression` with `controls`, `gaze`, `head_pose`, `preset`, and `movement_phrases`; `resolve_expression(request) -> ResolvedExpression`.
- Consumed by: engine and lineage.

- [ ] **Step 1: Write the failing catalog tests**

```python
def test_au46_resolves_to_a_side_specific_wink_phrase() -> None:
    resolved = resolve_expression(request_with("AU46"))
    assert "wink" in resolved.movement_phrases

def test_closed_eyes_and_upper_lid_raise_are_rejected_before_generation() -> None:
    with pytest.raises(ExpressionConflictError, match="AU43.*AU5"):
        resolve_expression(request_with("AU43", "AU5"))
```

- [ ] **Step 2: Run catalog tests and verify RED**

Run: `cd tools/expression-studio && PYTHONPATH=src ../../.venv/bin/python -m pytest tests/test_catalog.py -q`

Expected: FAIL because `expression_studio.catalog` does not exist.

- [ ] **Step 3: Implement the catalog and minimal conflict matrix**

```python
CONTROL_PHRASES = {"AU46": "wink one eye", "AU43": "close both eyes", "AU5": "raise the upper eyelids"}
CONFLICT_PAIRS = {frozenset({"AU43", "AU5"}), frozenset({"AU45", "AU43"}), frozenset({"AU46", "AU43"})}

def resolve_expression(request: ExpressionRequest) -> ResolvedExpression:
    # Resolve a preset, reject unknown IDs/pairs, then return ordered phrases.
```

Implement every initial control and preset listed in the approved design; keep gaze and head pose out of the face-control map.

- [ ] **Step 4: Run catalog tests and verify GREEN**

Run: `cd tools/expression-studio && PYTHONPATH=src ../../.venv/bin/python -m pytest tests/test_catalog.py -q`

Expected: PASS.

- [ ] **Step 5: Commit the completed catalog task**

```bash
git add tools/expression-studio/src/expression_studio/catalog.py tools/expression-studio/tests/test_catalog.py
git commit -m "feat: validate expression controls"
```

### Task 3: Generate deterministic candidate images and durable lineage

**Files:**
- Create: `tools/expression-studio/src/expression_studio/engine.py`
- Create: `tools/expression-studio/src/expression_studio/lineage.py`
- Create: `tools/expression-studio/tests/test_engine.py`
- Create: `tools/expression-studio/tests/test_lineage.py`

**Interfaces:**
- Consumes: `ExpressionRequest`, `ResolvedExpression`.
- Produces: `ExpressionEngine.generate(request, resolved, run_dir) -> EngineResult`, `FakeExpressionEngine`, `write_lineage(...) -> Path`.
- Consumed by: service.

- [ ] **Step 1: Write failing engine and lineage tests**

```python
def test_fake_engine_creates_requested_number_of_candidate_pngs(tmp_path: Path) -> None:
    result = FakeExpressionEngine().generate(valid_wink_request(), resolve_expression(valid_wink_request()), tmp_path)
    assert [item.name for item in result.candidates] == ["candidate-000.png", "candidate-001.png"]

def test_lineage_records_anchor_hash_and_resolved_phrase(tmp_path: Path) -> None:
    record = json.loads(write_lineage(request, resolved, b"anchor", tmp_path).read_text())
    assert record["resolved_expression"]["movement_phrases"] == ["wink one eye"]
```

- [ ] **Step 2: Run tests and verify RED**

Run: `cd tools/expression-studio && PYTHONPATH=src ../../.venv/bin/python -m pytest tests/test_engine.py tests/test_lineage.py -q`

Expected: FAIL because engine and lineage modules do not exist.

- [ ] **Step 3: Implement a fake edit engine and lineage writer**

```python
IDENTITY_PREFIX = "Preserve the exact same character: face geometry, hairstyle, costume, palette, framing, lighting, and art style. Edit only the requested facial expression, gaze, and head pose."

class FakeExpressionEngine:
    def generate(self, request: ExpressionRequest, resolved: ResolvedExpression, run_dir: Path) -> EngineResult:
        # Copy/annotate transparent-safe PNG candidates for local review only.
```

The fake engine must create valid PNG candidates without changing the source anchor; `generation_instruction` must include `IDENTITY_PREFIX` and resolved phrases. Write JSON lineage with a SHA-256 of anchor bytes and the complete resolved request.

- [ ] **Step 4: Run tests and verify GREEN**

Run: `cd tools/expression-studio && PYTHONPATH=src ../../.venv/bin/python -m pytest tests/test_engine.py tests/test_lineage.py -q`

Expected: PASS.

- [ ] **Step 5: Commit the completed engine/lineage task**

```bash
git add tools/expression-studio/src/expression_studio/engine.py tools/expression-studio/src/expression_studio/lineage.py tools/expression-studio/tests/test_engine.py tools/expression-studio/tests/test_lineage.py
git commit -m "feat: add expression candidate engine"
```

### Task 4: Add curation, still-image export, and guarded Figma delivery

**Files:**
- Create: `tools/expression-studio/src/expression_studio/paths.py`
- Create: `tools/expression-studio/src/expression_studio/exporter.py`
- Create: `tools/expression-studio/src/expression_studio/delivery.py`
- Create: `tools/expression-studio/src/expression_studio/service.py`
- Create: `tools/expression-studio/tests/test_service.py`
- Create: `tools/expression-studio/tests/test_delivery.py`

**Interfaces:**
- Consumes: run request/resolution, candidate PNGs, and the existing registry JSON document.
- Produces: `ExpressionStudioService`, a contact sheet, selected PNG, manifest, and `FigmaDeliveryPacket.public_view()`.
- Consumed by: FastAPI entrypoint and project GPT.

- [ ] **Step 1: Write failing lifecycle and routing tests**

```python
def test_delivery_is_blocked_until_a_candidate_is_explicitly_selected(tmp_path: Path) -> None:
    service, run = generated_service_run(tmp_path)
    with pytest.raises(RunBlockedError, match="selected candidate"):
        service.prepare_figma_delivery(run.run_id)

def test_delivery_packet_targets_only_the_bound_ready_project_area(tmp_path: Path) -> None:
    service, run = exported_service_run(tmp_path, project_id="demo")
    packet = service.prepare_figma_delivery(run.run_id).public_view()
    assert packet["target"]["generation_area_node_id"] == "10:3"
```

- [ ] **Step 2: Run lifecycle tests and verify RED**

Run: `cd tools/expression-studio && PYTHONPATH=src ../../.venv/bin/python -m pytest tests/test_service.py tests/test_delivery.py -q`

Expected: FAIL because `expression_studio.service` does not exist.

- [ ] **Step 3: Implement the minimal guarded lifecycle**

```python
class ExpressionStudioService:
    def export(self, run_id: str, selected_candidate: int) -> RunRecord:
        # Require generated state and an existing candidate; create contact_sheet.png, selected.png, manifest.json.

    def prepare_figma_delivery(self, run_id: str) -> FigmaDeliveryPacket:
        # Require exported state, use only configured project_id, and return paths—not bytes.
```

Copy the small validated Figma registry parser from Sprite Animation Studio rather than importing an uninstalled sibling package. Keep the parser behavior identical: exact URL/file-key check, ready-only status, exact node IDs, no fallback.

- [ ] **Step 4: Run lifecycle tests and verify GREEN**

Run: `cd tools/expression-studio && PYTHONPATH=src ../../.venv/bin/python -m pytest tests/test_service.py tests/test_delivery.py -q`

Expected: PASS.

- [ ] **Step 5: Commit the completed lifecycle task**

```bash
git add tools/expression-studio/src/expression_studio/{paths,exporter,delivery,service}.py tools/expression-studio/tests/test_service.py tools/expression-studio/tests/test_delivery.py
git commit -m "feat: export reviewed expressions safely"
```

### Task 5: Expose the local web UI and API

**Files:**
- Create: `tools/expression-studio/src/expression_studio/app.py`
- Create: `tools/expression-studio/web/index.html`
- Create: `tools/expression-studio/web/app.js`
- Create: `tools/expression-studio/web/styles.css`
- Create: `tools/expression-studio/tests/test_api.py`
- Create: `tools/expression-studio/tests/test_web_contract.py`

**Interfaces:**
- Consumes: `ExpressionStudioService` lifecycle and public run/delivery JSON.
- Produces: localhost FastAPI endpoints and Korean control/review UI.

- [ ] **Step 1: Write failing API and static web contract tests**

```python
def test_api_returns_conflict_details_before_generation(tmp_path: Path) -> None:
    response = client.post("/api/runs", json=payload_with("AU43", "AU5"))
    assert response.status_code == 422
    assert "AU43" in response.json()["detail"]

def test_web_exposes_separate_face_gaze_and_head_pose_controls() -> None:
    html = (WEB_ROOT / "index.html").read_text(encoding="utf-8")
    assert "얼굴 제어" in html and "시선" in html and "머리 방향" in html
```

- [ ] **Step 2: Run API/web tests and verify RED**

Run: `cd tools/expression-studio && PYTHONPATH=src ../../.venv/bin/python -m pytest tests/test_api.py tests/test_web_contract.py -q`

Expected: FAIL because the API and web files do not exist.

- [ ] **Step 3: Implement localhost API and a minimal Korean review UI**

```python
@app.post("/api/runs", status_code=201)
def create_run(request: ExpressionRequest) -> dict[str, object]:
    return service.create_run(request).public_view()

@app.post("/api/runs/{run_id}/export")
def export(run_id: str, payload: SelectionPayload) -> dict[str, object]:
    return service.export(run_id, payload.selected_candidate).public_view()
```

Render four face-control slots, intensity selectors, separate gaze/head-pose inputs, preset buttons, the resolved prompt, candidate selection, and `프로젝트 GPT 전송 준비`. The UI must explain that actual Figma placement is performed only by the matching project GPT workspace.

- [ ] **Step 4: Run API/web tests and verify GREEN**

Run: `cd tools/expression-studio && PYTHONPATH=src ../../.venv/bin/python -m pytest tests/test_api.py tests/test_web_contract.py -q && node --check web/app.js`

Expected: PASS.

- [ ] **Step 5: Commit the completed API/UI task**

```bash
git add tools/expression-studio/src/expression_studio/app.py tools/expression-studio/web tools/expression-studio/tests/test_api.py tools/expression-studio/tests/test_web_contract.py
git commit -m "feat: add expression studio local ui"
```

### Task 6: Document use and extend existing project Figma boards

**Files:**
- Create: `tools/expression-studio/README.md`
- Create: `templates/expression-studio/project-gpt-figma-delivery.md`
- Modify: `docs/operations/PROJECT_FIGMA_TARGET_REGISTRY.json` only if a verified Figma node ID changes
- Modify: the eight project Figma files via the Figma connector by adding an `Expression Runs` section inside each exact existing generation area
- Create: `tools/expression-studio/tests/test_docs_contract.py`

**Interfaces:**
- Consumes: Figma packet target page/area IDs and exported project-relative files.
- Produces: exact project-GPT delivery instructions and Figma review sections.

- [ ] **Step 1: Write failing documentation contract tests**

```python
def test_project_gpt_template_requires_matching_workspace_and_exact_area() -> None:
    text = TEMPLATE.read_text(encoding="utf-8")
    assert "matching project GPT workspace" in text
    assert "generation_area_node_id" in text
    assert "do not replace" in text
```

- [ ] **Step 2: Run the documentation test and verify RED**

Run: `cd tools/expression-studio && PYTHONPATH=src ../../.venv/bin/python -m pytest tests/test_docs_contract.py -q`

Expected: FAIL because the template and test do not exist.

- [ ] **Step 3: Write project-GPT delivery instructions and create Figma sections**

The template must instruct the project GPT to: verify matching project ID, Figma key, `READY_FOR_DELIVERY`, Figma page node ID, generation-area node ID, and local selected PNG; create a new run subsection in `Expression Runs`; add source/controls/lineage metadata; and return the section URL. It must prohibit fallback routing, replacing prior assets, claiming a local tool upload, tokens, and ZIPs.

Create one `Expression Runs` section inside each existing `Generated Assets` area. Preserve all pre-existing board content. Record the resulting Figma section node IDs in an additive registry field only after re-reading each Figma file.

- [ ] **Step 4: Run documentation contract tests and re-read Figma results**

Run: `cd tools/expression-studio && PYTHONPATH=src ../../.venv/bin/python -m pytest tests/test_docs_contract.py -q`

Expected: PASS. Then inspect each Figma file's target page/area and record successful/blocked mutations separately.

- [ ] **Step 5: Commit validated documentation and registry updates**

```bash
git add tools/expression-studio/README.md templates/expression-studio/project-gpt-figma-delivery.md tools/expression-studio/tests/test_docs_contract.py docs/operations/PROJECT_FIGMA_TARGET_REGISTRY.json
git commit -m "docs: add expression studio figma handoff"
```

### Task 7: Run package, Base, and adversarial verification

**Files:**
- Modify only if a verified `MUST_FIX` finding requires the smallest safe change.

**Interfaces:**
- Consumes: all prior work and the approved design.
- Produces: evidence-backed review result, with no claim that Figma images were uploaded.

- [ ] **Step 1: Run focused and full local checks**

```bash
cd tools/expression-studio && PYTHONPATH=src ../../.venv/bin/python -m pytest -q
node --check web/app.js
cd ../..
git diff --check
python tools/run_local_validation.py --trusted-history-commit <verified-40-character-main-sha>
```

Record unavailable dependencies or unrelated pre-existing failures separately; do not call them a pass.

- [ ] **Step 2: Perform adversarial review**

Attack: unrecognized control IDs, conflicts skipped through presets, output paths escaping the project root, source-anchor mutation, candidate auto-selection, cross-project target selection, mismatched Figma URL/file key, missing node IDs, direct Figma client imports, credential/ZIP artifacts, and stale README/UI/schema wording.

- [ ] **Step 3: Apply only validated MUST_FIX findings and rerun affected tests**

```bash
cd tools/expression-studio && PYTHONPATH=src ../../.venv/bin/python -m pytest -q
node --check web/app.js
cd ../..
git diff --check
```

- [ ] **Step 4: Commit verified review fixes, if any**

```bash
git add <only-verified-files>
git commit -m "fix: harden expression studio review findings"
```

- [ ] **Step 5: Report local/remote state accurately**

Report exact local commit, test evidence, Figma section verification, unexecuted checks, remote branch divergence, and a rollback command using the new commit SHA. Do not claim a push, PR update, or merge without fresh remote evidence.

## Plan self-review

- Spec coverage: Tasks 1–2 implement bounded controls, taxonomic separation, presets, and conflicts; Task 3 handles identity-preserving instruction and provenance; Task 4 requires selection and exact-project packet; Task 5 covers UI/API; Task 6 documents the project-GPT/Figma board workflow; Task 7 performs package/Base/adversarial checks.
- Placeholder scan: all tasks name concrete files, expected behaviors, commands, and interfaces. The one runtime-specific trusted-main SHA remains intentionally runtime-discovered rather than invented.
- Type consistency: `ExpressionRequest` flows through catalog → engine/lineage → service → API; `ResolvedExpression` is the single resolved-control type; `FigmaDeliveryPacket` remains a read-only project-GPT handoff payload.

## Execution handoff

Implement inline in this session, using this plan task-by-task with TDD and review checkpoints. A separate agent may perform a read-only adversarial review after the implementation because the user explicitly requested an adversarial review loop.
