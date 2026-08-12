# Sprite Animation Studio Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a Base-hosted local browser tool that turns approved character/effect anchors into curated sprite-animation exports while recording Figma visual lineage and preserving project ownership of binary assets.

**Architecture:** A Python 3.10+ package serves a Korean-first localhost UI and owns request validation, run workspaces, Figma/source lineage, curation, and deterministic exports. It invokes a pinned external `sprite-gen` adapter behind an interface; all tests use a fake adapter so provider credentials and image generation are never needed for verification.

**Tech Stack:** Python 3.10+, FastAPI, Uvicorn, Pydantic, Pillow, pytest, vanilla HTML/CSS/JavaScript; external `sprite-gen` pinned to commit `88f2ea17cac2ef066536beee7e3f40b2f8d29c87`.

## Global Constraints

- Base contains tool code, templates, tests, documentation, and third-party notices only; it never contains project art, generated runs, Figma exports, tokens, or API keys.
- Project-local binary inputs and outputs are passed by explicit paths and remain outside Base.
- The user-facing source-of-truth flow is `Figma source → approved anchor → candidate row → selected sequence → final atlas/GIF`.
- The external engine is reused through a pinned adapter; do not copy, fork, or modify its source in MVP.
- A generation/provider/extraction failure is a blocked result, never a fallback success.
- Production code follows test-first red → green → refactor for each behavior.
- The MVP does not update the Base Skill Registry or released plugin snapshot; a new Skill registration is deferred until the tool's independent trigger boundary is proven by real use.
- The tool binds only to `127.0.0.1` and accepts no remote request origin.
- `project_root` is a required server launch configuration (`--project-root`), not a browser-request field; every user-supplied asset/output path is resolved beneath it. Path traversal and Base-root output are rejected.
- The MVP stores and calls no OpenAI API key. Its only generation bridge is the explicitly configured local `sprite-gen` executable (which may use the developer's existing Codex authentication outside Base). Direct API integration is deferred.

---

## File Structure

| Path | Responsibility |
|---|---|
| `tools/sprite-animation-studio/pyproject.toml` | Isolated Python package metadata and development dependencies. |
| `tools/sprite-animation-studio/README.md` | Local installation, launch, and project-adoption instructions. |
| `tools/sprite-animation-studio/THIRD_PARTY_NOTICES.md` | Pinned `sprite-gen` origin, commit, license, and upgrade procedure. |
| `tools/sprite-animation-studio/src/sprite_animation_studio/models.py` | Validated request, anchor, action, run-status, and manifest data models. |
| `tools/sprite-animation-studio/src/sprite_animation_studio/paths.py` | Safe project-root path resolution and run-directory creation. |
| `tools/sprite-animation-studio/src/sprite_animation_studio/lineage.py` | Figma/source hashes and accepted-anchor lineage record creation. |
| `tools/sprite-animation-studio/src/sprite_animation_studio/engine.py` | Engine protocol, fake fixture adapter, and pinned `sprite-gen` subprocess adapter. |
| `tools/sprite-animation-studio/src/sprite_animation_studio/curation.py` | Non-destructive selection, ordering, transform, and explicit rejection persistence. |
| `tools/sprite-animation-studio/src/sprite_animation_studio/exporter.py` | Deterministic PNG copy, contact sheet, GIF, atlas manifest, and Godot handoff export. |
| `tools/sprite-animation-studio/src/sprite_animation_studio/service.py` | Application use cases and fail-closed run state transitions. |
| `tools/sprite-animation-studio/src/sprite_animation_studio/app.py` | Localhost FastAPI routes and static-file serving. |
| `tools/sprite-animation-studio/web/index.html` | Korean-first workspace layout and accessible controls. |
| `tools/sprite-animation-studio/web/app.js` | Browser-side request submission, frame selection, ordering, and preview state. |
| `tools/sprite-animation-studio/web/styles.css` | Local tool visual styles including candidate/accepted/blocked states. |
| `tools/sprite-animation-studio/tests/` | Unit, API, export, and browser-static contract tests. |
| `templates/sprite-animation/sprite-animation-request.schema.json` | Portable request JSON Schema for project adoption. |
| `templates/sprite-animation/figma-sprite-lineage.example.json` | Example of the Figma source-to-export audit record. |
| `docs/knowledge/game-development/SPRITE_ANIMATION_STUDIO_ADOPTION_GUIDE.md` | Common adoption, rights, Figma, Godot, validation, and rollback contract. |

## Task 1: Isolated package and safe file boundary

**Files:**
- Create: `tools/sprite-animation-studio/pyproject.toml`
- Create: `tools/sprite-animation-studio/src/sprite_animation_studio/__init__.py`
- Create: `tools/sprite-animation-studio/src/sprite_animation_studio/paths.py`
- Create: `tools/sprite-animation-studio/tests/test_paths.py`

**Interfaces:**
- Produces: `resolve_project_path(project_root: Path, candidate: str) -> Path`
- Produces: `create_run_paths(project_root: Path, asset_id: str, action_name: str, run_id: str) -> RunPaths`

- [ ] **Step 1: Write the failing path-boundary tests**

```python
def test_resolve_project_path_rejects_parent_escape(tmp_path: Path) -> None:
    with pytest.raises(PathViolation):
        resolve_project_path(tmp_path, "../Base/secret.txt")

def test_create_run_paths_stays_under_project_root(tmp_path: Path) -> None:
    paths = create_run_paths(tmp_path, "knight", "attack_heavy", "run-001")
    assert paths.run_dir == tmp_path / "art" / "animation-runs" / "knight" / "run-001"
    assert paths.run_dir.is_relative_to(tmp_path)
```

- [ ] **Step 2: Run the tests to verify red**

Run: `cd tools/sprite-animation-studio && pytest tests/test_paths.py -v`
Expected: FAIL because `sprite_animation_studio.paths` does not exist.

- [ ] **Step 3: Add the minimal package configuration and implementation**

```python
class PathViolation(ValueError):
    pass

def resolve_project_path(project_root: Path, candidate: str) -> Path:
    root = project_root.resolve()
    target = (root / candidate).resolve()
    if target != root and root not in target.parents:
        raise PathViolation(f"path escapes project root: {candidate}")
    return target
```

Use `pyproject.toml` with Python `>=3.10`, runtime dependencies `fastapi`, `uvicorn`, `pydantic`, and `Pillow`; dev dependency `pytest`.

- [ ] **Step 4: Run the path tests to verify green**

Run: `cd tools/sprite-animation-studio && pytest tests/test_paths.py -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add tools/sprite-animation-studio/pyproject.toml tools/sprite-animation-studio/src tools/sprite-animation-studio/tests/test_paths.py
git commit -m "feat: add sprite studio package boundary"
```

## Task 2: Request and Figma lineage contracts

**Files:**
- Create: `tools/sprite-animation-studio/src/sprite_animation_studio/models.py`
- Create: `tools/sprite-animation-studio/src/sprite_animation_studio/lineage.py`
- Create: `tools/sprite-animation-studio/tests/test_models.py`
- Create: `tools/sprite-animation-studio/tests/test_lineage.py`
- Create: `templates/sprite-animation/sprite-animation-request.schema.json`
- Create: `templates/sprite-animation/figma-sprite-lineage.example.json`

**Interfaces:**
- Produces: `SpriteAnimationRequest` with `project_id`, `asset_id`, `asset_kind`, `anchor`, `action`, and project-root-relative `output_root`.
- Produces: `write_lineage(request: SpriteAnimationRequest, anchor_bytes: bytes, output_dir: Path) -> Path`.

- [ ] **Step 1: Write failing request and lineage tests**

```python
def test_request_requires_approved_anchor() -> None:
    with pytest.raises(ValidationError):
        SpriteAnimationRequest.model_validate({
            "project_id": "demo", "asset_id": "knight", "asset_kind": "character",
            "anchor": {"source_path": "art/source/idle.png", "approval_status": "draft"},
            "action": {"name": "attack", "direction": "left", "frame_count": 4, "fps": 8, "loop_mode": "none", "prompt": "strike"},
            "output_root": "art/animation-runs/knight"
        })

def test_lineage_records_figma_url_and_anchor_sha256(tmp_path: Path) -> None:
    record = write_lineage(valid_request(figma_node_url="https://www.figma.com/design/x?node-id=1-2"), b"anchor", tmp_path)
    data = json.loads(record.read_text())
    assert data["anchor"]["sha256"] == hashlib.sha256(b"anchor").hexdigest()
    assert data["anchor"]["figma_node_url"].endswith("node-id=1-2")
```

- [ ] **Step 2: Run the tests to verify red**

Run: `cd tools/sprite-animation-studio && pytest tests/test_models.py tests/test_lineage.py -v`
Expected: FAIL because request and lineage models do not exist.

- [ ] **Step 3: Implement strict schemas**

Require `approval_status == "approved"`; allow only `character` or `effect`; require `1 <= frame_count <= 16`, `1 <= fps <= 60`, and loop modes `none|linear|pingpong`. Write stable sorted JSON and a SHA-256 of the exact anchor bytes. The JSON Schema must match the Pydantic fields and reject additional properties.

- [ ] **Step 4: Run tests and JSON-schema validation**

Run: `cd tools/sprite-animation-studio && pytest tests/test_models.py tests/test_lineage.py -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add tools/sprite-animation-studio/src/sprite_animation_studio/models.py tools/sprite-animation-studio/src/sprite_animation_studio/lineage.py tools/sprite-animation-studio/tests templates/sprite-animation
git commit -m "feat: add sprite request and lineage contracts"
```

## Task 3: Engine bridge with fake-first verification

**Files:**
- Create: `tools/sprite-animation-studio/src/sprite_animation_studio/engine.py`
- Create: `tools/sprite-animation-studio/tests/test_engine.py`
- Create: `tools/sprite-animation-studio/THIRD_PARTY_NOTICES.md`

**Interfaces:**
- Produces: `SpriteEngine.generate(request: SpriteAnimationRequest, run_dir: Path) -> EngineResult`.
- Produces: `FakeSpriteEngine(frame_count: int)` for deterministic tests.
- Produces: `PinnedSpriteGenEngine(sprite_gen_executable: Path)` for local use.

- [ ] **Step 1: Write failing engine tests**

```python
def test_fake_engine_creates_exact_requested_frame_count(tmp_path: Path) -> None:
    result = FakeSpriteEngine().generate(valid_request(frame_count=3), tmp_path)
    assert [frame.name for frame in result.frames] == ["frame-000.png", "frame-001.png", "frame-002.png"]

def test_engine_result_rejects_wrong_frame_count(tmp_path: Path) -> None:
    with pytest.raises(EngineContractError, match="expected 4 frames"):
        FakeSpriteEngine(frame_count=3).generate(valid_request(frame_count=4), tmp_path)
```

- [ ] **Step 2: Run the tests to verify red**

Run: `cd tools/sprite-animation-studio && pytest tests/test_engine.py -v`
Expected: FAIL because `engine.py` does not exist.

- [ ] **Step 3: Implement the engine protocol and fake**

The fake writes small transparent PNG fixtures through Pillow. The pinned adapter runs only the installed executable explicitly configured by the user, verifies exit code, verified PNG output, and exact count before returning `EngineResult`. It must surface stdout/stderr in a blocked result and never select another provider automatically.

Document `sprite-gen` source URL, exact commit `88f2ea17cac2ef066536beee7e3f40b2f8d29c87`, Apache-2.0 license, and manual upgrade/revert process in `THIRD_PARTY_NOTICES.md`.

- [ ] **Step 4: Run tests to verify green**

Run: `cd tools/sprite-animation-studio && pytest tests/test_engine.py -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add tools/sprite-animation-studio/src/sprite_animation_studio/engine.py tools/sprite-animation-studio/tests/test_engine.py tools/sprite-animation-studio/THIRD_PARTY_NOTICES.md
git commit -m "feat: add pinned sprite engine bridge"
```

## Task 4: Non-destructive curation and deterministic export

**Files:**
- Create: `tools/sprite-animation-studio/src/sprite_animation_studio/curation.py`
- Create: `tools/sprite-animation-studio/src/sprite_animation_studio/exporter.py`
- Create: `tools/sprite-animation-studio/tests/test_curation.py`
- Create: `tools/sprite-animation-studio/tests/test_exporter.py`

**Interfaces:**
- Produces: `CurationState(selected: list[int], transforms: dict[int, FrameTransform])`.
- Produces: `export_run(run_dir: Path, request: SpriteAnimationRequest, curation: CurationState) -> ExportResult`.

- [ ] **Step 1: Write failing curation/export tests**

```python
def test_curation_never_rewrites_source_frame(tmp_path: Path) -> None:
    source = write_fixture_frame(tmp_path / "frames" / "frame-000.png")
    before = source.read_bytes()
    save_curation(tmp_path, CurationState(selected=[0], transforms={0: FrameTransform(dx=3)}))
    assert source.read_bytes() == before

def test_export_manifest_preserves_selected_order_fps_and_loop(tmp_path: Path) -> None:
    result = export_run(run_with_four_frames(tmp_path), valid_request(fps=8, loop_mode="none"), CurationState(selected=[2, 0, 3, 1]))
    manifest = json.loads(result.manifest.read_text())
    assert manifest["animation"]["rows"]["attack"]["fps"] == 8
    assert manifest["animation"]["rows"]["attack"]["loop"] is False
    assert [frame["source_index"] for frame in manifest["selected_frames"]] == [2, 0, 3, 1]
```

- [ ] **Step 2: Run tests to verify red**

Run: `cd tools/sprite-animation-studio && pytest tests/test_curation.py tests/test_exporter.py -v`
Expected: FAIL because curation and exporter modules do not exist.

- [ ] **Step 3: Implement sidecar and exports**

Store `curation.json` separately from `frames/`. Export selected PNGs to `exports/frames/<action>/`, create a GIF preview with requested FPS, compose a uniformly sized atlas, and emit `manifest.json` with absolute frame rectangles, frame order, `fps`, and `loop`. Emit `godot/<action>.spriteframes.json` as an unambiguous handoff only.

- [ ] **Step 4: Run tests to verify green**

Run: `cd tools/sprite-animation-studio && pytest tests/test_curation.py tests/test_exporter.py -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add tools/sprite-animation-studio/src/sprite_animation_studio/curation.py tools/sprite-animation-studio/src/sprite_animation_studio/exporter.py tools/sprite-animation-studio/tests
git commit -m "feat: add curation and animation exports"
```

## Task 5: Service API and fail-closed run lifecycle

**Files:**
- Create: `tools/sprite-animation-studio/src/sprite_animation_studio/service.py`
- Create: `tools/sprite-animation-studio/src/sprite_animation_studio/app.py`
- Create: `tools/sprite-animation-studio/tests/test_api.py`

**Interfaces:**
- Produces: `POST /api/runs` → creates a blocked or generated run.
- Produces: `POST /api/runs/{run_id}/curation` → persists selection/transforms.
- Produces: `POST /api/runs/{run_id}/export` → rejects incomplete selection or exports deterministic files.
- Produces: `GET /api/runs/{run_id}` → returns status, warnings, and lineage metadata only.

- [ ] **Step 1: Write failing API tests**

```python
def test_create_run_returns_blocked_without_approved_anchor(client: TestClient) -> None:
    response = client.post("/api/runs", json=request_with_anchor_status("draft"))
    assert response.status_code == 422

def test_export_rejects_incomplete_selection(client: TestClient) -> None:
    run_id = create_fake_run(client, frame_count=4)
    response = client.post(f"/api/runs/{run_id}/export", json={"selected": [0, 1, 2]})
    assert response.status_code == 409
    assert response.json()["status"] == "blocked"
```

- [ ] **Step 2: Run tests to verify red**

Run: `cd tools/sprite-animation-studio && pytest tests/test_api.py -v`
Expected: FAIL because the FastAPI app does not exist.

- [ ] **Step 3: Implement localhost-only API**

Use dependency injection so tests pass `FakeSpriteEngine`. Require `--project-root` when the server starts; reject requests whose output resolves outside that configured root or whose anchor is not approved. Include `blocked`, `generated`, `curated`, and `exported` statuses; no route may write to Base paths.

- [ ] **Step 4: Run tests to verify green**

Run: `cd tools/sprite-animation-studio && pytest tests/test_api.py -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add tools/sprite-animation-studio/src/sprite_animation_studio/service.py tools/sprite-animation-studio/src/sprite_animation_studio/app.py tools/sprite-animation-studio/tests/test_api.py
git commit -m "feat: add sprite studio local API"
```

## Task 6: Korean-first browser workspace

**Files:**
- Create: `tools/sprite-animation-studio/web/index.html`
- Create: `tools/sprite-animation-studio/web/app.js`
- Create: `tools/sprite-animation-studio/web/styles.css`
- Create: `tools/sprite-animation-studio/tests/test_web_contract.py`

**Interfaces:**
- Consumes: `POST /api/runs`, `GET /api/runs/{run_id}`, curation, and export endpoints.
- Produces: a visible five-stage lineage ribbon and accessible candidate/selected frame controls.

- [ ] **Step 1: Write failing static UI contract tests**

```python
def test_workspace_names_the_five_visual_lineage_stages() -> None:
    html = (WEB / "index.html").read_text(encoding="utf-8")
    for label in ["원본 이미지", "승인 앵커", "동작 후보", "채택 프레임", "최종 시트"]:
        assert label in html

def test_controls_have_labels_for_destructive_actions() -> None:
    html = (WEB / "index.html").read_text(encoding="utf-8")
    assert 'aria-label="선택 프레임에서 제거"' in html
    assert 'aria-label="프레임 순서 앞으로"' in html
```

- [ ] **Step 2: Run tests to verify red**

Run: `cd tools/sprite-animation-studio && pytest tests/test_web_contract.py -v`
Expected: FAIL because web files do not exist.

- [ ] **Step 3: Implement the workspace**

Lay out: request panel, visual-lineage ribbon, source/anchor card, candidate frame grid, accepted-play sequence, preview player, warning panel, and export summary. Bind the UI only to localhost API paths. Require explicit confirmation before removing a selected frame, and show the Figma node URL and anchor SHA-256 in the lineage panel.

- [ ] **Step 4: Run tests to verify green**

Run: `cd tools/sprite-animation-studio && pytest tests/test_web_contract.py -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add tools/sprite-animation-studio/web tools/sprite-animation-studio/tests/test_web_contract.py
git commit -m "feat: add sprite studio browser workspace"
```

## Task 7: Adoption guide, verification, and review evidence

**Files:**
- Create: `tools/sprite-animation-studio/README.md`
- Create: `docs/knowledge/game-development/SPRITE_ANIMATION_STUDIO_ADOPTION_GUIDE.md`
- Create: `tools/sprite-animation-studio/tests/test_docs_contract.py`
- Modify: `docs/superpowers/specs/2026-08-12-sprite-animation-studio-design.md` only if implementation discoveries require a narrowly approved correction.

**Interfaces:**
- Consumes: implemented API, templates, test command, and third-party notice.
- Produces: reproducible local launch instructions and an explicit project-adoption checklist.

- [ ] **Step 1: Write failing documentation contract tests**

```python
def test_readme_states_that_credentials_and_generated_art_are_not_committed() -> None:
    text = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "API 키" in text
    assert "커밋하지 않습니다" in text

def test_adoption_guide_requires_figma_lineage_and_project_runtime_check() -> None:
    text = ADOPTION_GUIDE.read_text(encoding="utf-8")
    assert "Figma 노드 URL" in text
    assert "Godot 런타임 검증" in text
```

- [ ] **Step 2: Run tests to verify red**

Run: `cd tools/sprite-animation-studio && pytest tests/test_docs_contract.py -v`
Expected: FAIL because user documentation does not exist.

- [ ] **Step 3: Write adoption and rollback documentation**

Document setup, `python -m sprite_animation_studio.app --project-root <absolute-project-path>` launch, Figma flow, source-art rights, generated-output handling, explicit engine installation requirement, provider failure recovery, Godot handoff versus runtime verification, and a PR-revert rollback. State that the MVP has no direct API-key configuration; do not include credentials or unverified installation claims.

- [ ] **Step 4: Run focused tests and all package tests**

Run: `cd tools/sprite-animation-studio && pytest -v`
Expected: PASS with no provider credential required.

- [ ] **Step 5: Run Base validation and visual review**

Run: `python tools/run_local_validation.py --trusted-history-commit <verified-main-40-char-sha>`
Expected: Base checks pass or any environment-specific skipped/blocked checks are reported without being relabeled as pass.

Launch the local server with the fake engine fixture and perform one manual browser path: source → approved anchor → action row → curation → export. Record actual screenshot/output evidence in the PR; if the server cannot be launched in the validation environment, record `BLOCKED_UNVERIFIED` rather than claiming visual verification.

- [ ] **Step 6: Perform adversarial regression review**

Check these attacks against implementation evidence:
1. path escape outside `project_root`;
2. unapproved anchor export;
3. wrong engine frame count;
4. raw frame rewrite by curation;
5. Figma URL/hash omission;
6. credential/generated-art inclusion in Base;
7. Godot handoff mislabeled as verified runtime import.

Apply only approved in-scope fixes, re-run the affected tests, then record residual risks.

- [ ] **Step 7: Commit**

```bash
git add tools/sprite-animation-studio/README.md tools/sprite-animation-studio/tests/test_docs_contract.py docs/knowledge/game-development/SPRITE_ANIMATION_STUDIO_ADOPTION_GUIDE.md
git commit -m "docs: add sprite studio adoption guide"
```

## Plan self-review

- Spec coverage: Tasks 1–7 cover request validation, visual lineage, engine reuse, curation, exports, UI, project ownership, Figma records, Godot handoff, documentation, and rollback.
- Completion detail: every task contains named files, interfaces, concrete tests, commands, and expected outcomes.
- Type consistency: `SpriteAnimationRequest`, `EngineResult`, `CurationState`, `ExportResult`, and `RunPaths` are introduced before their consumers.
- Scope control: direct Figma write, project-repository publishing, direct Godot scene edits, and provider credential setup remain explicitly excluded from MVP.
