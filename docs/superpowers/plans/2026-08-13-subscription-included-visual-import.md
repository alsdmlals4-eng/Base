# Subscription-Included Visual Import Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make Expression Studio and Sprite Animation Studio usable without metered API calls by importing user-supplied ChatGPT/Figma/local image outputs into the existing validated review, export, and project-GPT handoff pipeline.

**Architecture:** Each Studio gets one focused import module that validates uploaded image bytes before they enter project-local staging. A new multipart endpoint creates a normal run record with trusted `subscription_handoff_import` provenance, while the existing JSON generation endpoint remains available only when the server was explicitly launched in a generation mode. The service—not the browser—owns cost-route, provenance, validation, export eligibility, and project binding.

**Tech Stack:** Python 3.10+, FastAPI multipart uploads, Pydantic 2, Pillow 10–11, `python-multipart==0.0.32`, existing `base-tool-contracts` no-follow staging primitives, vanilla HTML/CSS/JavaScript, pytest.

## Global Constraints

- Default CLI run mode is `subscription_handoff_import`; it makes no OpenAI, Figma, Weave, or other provider call.
- Existing OpenAI and simulated adapters remain explicit CLI-only modes and preserve their current engine policies.
- Import provenance is `subscription_handoff_import`, `cost_route` is `INCLUDED_OR_LOCAL_HANDOFF`, and `provider_call_made` is always `false` for imported runs.
- Accepted uploads are PNG, JPEG, or WebP, at most 25 MiB each, with both dimensions in `1..4096`; complete Expression and Sprite requests are capped at 202 MiB and 402 MiB respectively before multipart parsing, preserving the documented 8/16-file maxima plus multipart overhead.
- Expression imports accept exactly `candidate_count` files in the inclusive range `1..8`; candidates must be non-empty, visually distinct from the anchor, and pairwise non-duplicate.
- Sprite imports accept exactly `frame_count` files in the existing inclusive range `1..16`; every frame must be non-empty, share dimensions, and be pairwise non-duplicate.
- Browser filenames are never used as filesystem paths. Staging uses deterministic internal names and existing no-follow safe writes.
- `declared_source` is one of `CHATGPT_INCLUDED`, `FIGMA_INCLUDED`, `LOCAL_GENERATOR`, or `OTHER_USER_SUPPLIED`; it is user-declared metadata, not provider attestation.
- A malformed file rejects the whole import before any run becomes export-eligible.
- Expression export still requires explicit candidate selection. Sprite curation still controls frame order/removal before export.
- Figma delivery still requires exact project routing and approved-anchor evidence; preparing a packet does not mutate Figma.
- The implementation must not call a paid provider, change billing settings, or claim live Figma placement.
- `python-multipart` is pinned exactly to `0.0.32` in both Studio packages.

---

### Task 1: Shared import image contracts inside each Studio

**Files:**
- Create: `tools/expression-studio/src/expression_studio/imports.py`
- Create: `tools/sprite-animation-studio/src/sprite_animation_studio/imports.py`
- Create: `tools/expression-studio/tests/test_imports.py`
- Create: `tools/sprite-animation-studio/tests/test_imports.py`
- Modify: `tools/expression-studio/pyproject.toml`
- Modify: `tools/sprite-animation-studio/pyproject.toml`

**Interfaces:**
- Produces `DeclaredSource = Literal["CHATGPT_INCLUDED", "FIGMA_INCLUDED", "LOCAL_GENERATOR", "OTHER_USER_SUPPLIED"]`.
- Produces immutable `ImportedImage(data: bytes, sha256: str, detected_format: str, width: int, height: int, has_alpha: bool, declared_source: DeclaredSource, order: int)`.
- Produces `validate_imported_image(data: bytes, *, declared_source: DeclaredSource, order: int) -> ImportedImage`.
- Produces async `read_upload_limited(upload: UploadFile) -> bytes`, which reads chunks and rejects byte 25 MiB + 1.
- Produces `import_metadata(image: ImportedImage) -> dict[str, object]` for durable lineage/manifest data.

- [ ] **Step 1: Write focused failing tests for accepted PNG/JPEG/WebP metadata, the 25 MiB boundary, unsupported/truncated/decompression-bomb images, zero/over-4096 dimensions, and alpha detection.**

  Every test names the missing validation branch and uses hand-derived expected metadata. The async size test passes a real `UploadFile` backed by `BytesIO`, not a mock.

- [ ] **Step 2: Run each new import test module and verify RED.**

  Run:
  ```bash
  cd tools/expression-studio && PYTHONPATH=../base-tool-contracts/src:src ../../.venv/bin/python -m pytest -q tests/test_imports.py
  cd ../sprite-animation-studio && PYTHONPATH=../base-tool-contracts/src:src ../../.venv/bin/python -m pytest -q tests/test_imports.py
  ```
  Expected: collection fails because each Studio's `imports` module does not exist.

- [ ] **Step 3: Implement the minimal validators.**

  Each module uses constants `MAX_IMPORT_BYTES = 25 * 1024 * 1024`, `MAX_IMPORT_DIMENSION = 4096`, and `ALLOWED_IMPORT_FORMATS = {"PNG", "JPEG", "WEBP"}`. It catches `UnidentifiedImageError`, `OSError`, and `Image.DecompressionBombError`; calls `image.verify()` before reopening; checks dimensions before `convert("RGBA").load()`; computes SHA-256 from the original bytes; and never accepts a filename argument.

- [ ] **Step 4: Pin multipart support and install it in the repository venv.**

  Add `"python-multipart==0.0.32"` to both dependency lists, then run:
  ```bash
  .venv/bin/pip install python-multipart==0.0.32
  .venv/bin/pip check
  ```

- [ ] **Step 5: Run both import test modules and both existing suites; verify GREEN.**

- [ ] **Step 6: Commit.**

  ```bash
  git add tools/expression-studio tools/sprite-animation-studio
  git commit -m "feat: add bounded visual import validation"
  ```

### Task 2: Expression Studio import lifecycle and multipart API

**Files:**
- Modify: `tools/expression-studio/src/expression_studio/models.py`
- Modify: `tools/expression-studio/src/expression_studio/app.py`
- Modify: `tools/expression-studio/src/expression_studio/service.py`
- Modify: `tools/expression-studio/src/expression_studio/lineage.py`
- Modify: `tools/expression-studio/src/expression_studio/exporter.py`
- Modify: `tools/expression-studio/tests/test_api.py`
- Modify: `tools/expression-studio/tests/test_service.py`
- Create: `tools/expression-studio/tests/test_import_api.py`

**Interfaces:**
- Adds `run_mode: Literal["subscription_handoff_import", "simulated", "openai"]` to `create_app` and `ExpressionStudioService`.
- Adds `ExpressionImportRequest(request: ExpressionRequest, declared_source: DeclaredSource)` as the parsed metadata envelope.
- Adds `ExpressionStudioService.create_import_run(request: ExpressionRequest, candidates: tuple[ImportedImage, ...], declared_source: DeclaredSource) -> RunRecord`.
- Adds `POST /api/import-runs` with multipart fields `request_json: str`, `declared_source: str`, and repeated `candidates: list[UploadFile]`.
- Adds `RunRecord.run_mode`, `RunRecord.imported_images`, and public `cost` fields.

- [ ] **Step 1: Write RED API tests for a successful two-candidate import and a JSON generation request rejected with `409 MODE_NOT_AVAILABLE` on the default import-mode server.**

  The success test posts real multipart PNGs, asserts HTTP 201, `status == "generated"`, `engine.provenance == "subscription_handoff_import"`, `engine.delivery_eligible is True` only when approved-anchor evidence is configured, `cost.provider_call_made is False`, and retrieves both candidate endpoints.

- [ ] **Step 2: Write RED service/API tests for exact file count, anchor-identical pixels, pairwise duplicate pixels, fully transparent candidates, malformed `request_json`, invalid `declared_source`, and all-or-nothing staging.**

  For the all-or-nothing case, place one valid and one invalid upload and assert no `candidate-*.png` remains under the new run root.

- [ ] **Step 3: Run the new Expression tests and verify each failure is caused by the missing import endpoint/lifecycle.**

- [ ] **Step 4: Implement server-owned run mode and multipart parsing.**

  The endpoint parses `ExpressionRequest.model_validate_json(request_json)`, validates `declared_source` through Pydantic/`TypeAdapter`, reads each upload with `read_upload_limited`, validates every image in memory, and only then calls `create_import_run`. It maps malformed metadata/image errors to 422 and disabled modes to 409 with `detail="MODE_NOT_AVAILABLE"`.

- [ ] **Step 5: Implement `create_import_run` by reusing project ID, Figma anchor-route, approved-anchor evidence, safe source read, expression resolution, vault path, stable tree, lineage, run storage, and export checks.**

  Imported files are written as `candidate-{order:03d}.png` using `safe_staging_write_bytes`. The service converts image pixels to RGBA only for comparison; it rejects an anchor-identical candidate, transparent candidate, or repeated RGBA hash before setting `status="generated"`. Engine policy is constructed by the service with adapter ID `expression.import.v1`; browser metadata cannot set eligibility.

- [ ] **Step 6: Persist provenance and import metadata in lineage, export manifest, public view, and delivery packet evidence.**

  Durable records include run mode, cost route, provider-call flag, declared source, input order, original SHA-256, detected format, dimensions, alpha, and trusted engine config hash. Existing generated-run records retain their current fields.

- [ ] **Step 7: Run Expression focused tests, then the full Expression suite; refactor only while green.**

- [ ] **Step 8: Commit.**

  ```bash
  git add tools/expression-studio
  git commit -m "feat: import expression candidates without provider calls"
  ```

### Task 3: Expression Studio import-first browser workflow

**Files:**
- Modify: `tools/expression-studio/web/index.html`
- Modify: `tools/expression-studio/web/app.js`
- Modify: `tools/expression-studio/web/styles.css`
- Create: `tools/expression-studio/tests/test_web_contract.py`

**Interfaces:**
- Consumes `/api/config.run_mode`, `/api/import-runs`, and the existing candidate/export/delivery endpoints.
- Produces a multipart import form with repeated `candidates`, a declared-source selector, and an explicit `추가 비용 없는 가져오기` banner.

- [ ] **Step 1: Write a RED web-contract test that loads the real HTML and asserts accessible import controls, multiple-file acceptance, the four declared-source options, and no automatic submit/export.**

- [ ] **Step 2: Run the web-contract test and verify RED because the controls are absent.**

- [ ] **Step 3: Implement the import-first UI.**

  Preserve FACS controls because they describe the intended output. In import mode, submit `request_json`, `declared_source`, and selected files via `FormData`; do not set `Content-Type` manually. Show file count before submit, explain that the user first creates images in their included ChatGPT/Figma/local workflow, and never claim provider generation or Figma upload.

- [ ] **Step 4: Add blocked-state reset and cost/provenance rendering.**

  A failed import clears the old run ID, candidates, selection, export state, and delivery packet. The result banner reads the server-owned `cost` and `engine` values.

- [ ] **Step 5: Run the web-contract test, `node --check web/app.js`, and the full Expression suite.**

- [ ] **Step 6: Commit.**

  ```bash
  git add tools/expression-studio/web tools/expression-studio/tests/test_web_contract.py
  git commit -m "feat: make expression imports the default workflow"
  ```

### Task 4: Sprite Animation Studio import lifecycle and multipart API

**Files:**
- Modify: `tools/sprite-animation-studio/src/sprite_animation_studio/models.py`
- Modify: `tools/sprite-animation-studio/src/sprite_animation_studio/app.py`
- Modify: `tools/sprite-animation-studio/src/sprite_animation_studio/service.py`
- Modify: `tools/sprite-animation-studio/src/sprite_animation_studio/lineage.py`
- Modify: `tools/sprite-animation-studio/src/sprite_animation_studio/exporter.py`
- Modify: `tools/sprite-animation-studio/tests/test_api.py`
- Modify: `tools/sprite-animation-studio/tests/test_service.py`
- Create: `tools/sprite-animation-studio/tests/test_import_api.py`

**Interfaces:**
- Adds the same immutable `run_mode` choices to Sprite app/service.
- Adds `SpriteAnimationService.create_import_run(request: SpriteAnimationRequest, frames: tuple[ImportedImage, ...], declared_source: DeclaredSource) -> RunRecord`.
- Adds `POST /api/import-runs` with `request_json`, `declared_source`, and ordered repeated `frames`.
- Uses trusted adapter ID `sprite.import.v1` and preserves existing `CurationState`, `export_run`, Godot handoff, and Figma packet interfaces.

- [ ] **Step 1: Write RED API tests for a four-frame import that preserves multipart order and for default import mode rejecting JSON generation with `409 MODE_NOT_AVAILABLE`.**

- [ ] **Step 2: Write RED tests for wrong count, dimension mismatch, transparent frame at any index, pairwise duplicate pixels, malformed metadata, and no partial eligible run.**

- [ ] **Step 3: Run the new Sprite tests and verify RED for the missing endpoint/lifecycle.**

- [ ] **Step 4: Implement bounded multipart parsing and `create_import_run`.**

  Validate all bytes before staging. Reuse immutable project ID, anchor route/evidence, no-follow source read, vault/stable-tree paths, lineage, run record, curation, and export gates. Write `frame-{order:03d}.png` in upload order. Require the same `(width, height)` and unique RGBA hashes for all frames. For `effect_stages`, lack of alpha adds a warning but does not block.

- [ ] **Step 5: Persist trusted provenance/import metadata and ensure export/packet hashes cover imported frames and all existing visual deliverables.**

- [ ] **Step 6: Run Sprite focused tests, then the full Sprite suite; refactor only while green.**

- [ ] **Step 7: Commit.**

  ```bash
  git add tools/sprite-animation-studio
  git commit -m "feat: import ordered sprite frames without provider calls"
  ```

### Task 5: Sprite import-first browser workflow

**Files:**
- Modify: `tools/sprite-animation-studio/web/index.html`
- Modify: `tools/sprite-animation-studio/web/app.js`
- Modify: `tools/sprite-animation-studio/web/styles.css`
- Create: `tools/sprite-animation-studio/tests/test_web_contract.py`

**Interfaces:**
- Consumes `/api/config.run_mode`, `/api/import-runs`, existing frame/curation/export/delivery endpoints.
- Produces local pre-submit upload ordering/removal and preserves post-import curation ordering/removal/transforms.

- [ ] **Step 1: Write RED web-contract tests for ordered multi-file input, source selector, local reorder/remove controls, and the no-extra-cost explanation.**

- [ ] **Step 2: Verify RED, then implement an import queue keyed by an internal browser ID rather than filename.**

  The queue shows thumbnails, supports move previous/next and remove, and appends `frames` to `FormData` in visible order. It requires the visible count to equal `frame_count` before submit.

- [ ] **Step 3: Preserve the existing post-import sequence editor and blocked-state reset.**

  Imported runs initialize `state.selected` in server-returned order; subsequent transforms and export use the existing curation endpoint. No UI action calls a provider or Figma generation API.

- [ ] **Step 4: Run the web tests, `node --check web/app.js`, and full Sprite suite.**

- [ ] **Step 5: Commit.**

  ```bash
  git add tools/sprite-animation-studio/web tools/sprite-animation-studio/tests/test_web_contract.py
  git commit -m "feat: make sprite frame imports the default workflow"
  ```

### Task 6: Operator docs, cost guardrails, and full verification

**Files:**
- Modify: `tools/expression-studio/README.md`
- Modify: `tools/sprite-animation-studio/README.md`
- Modify: `docs/superpowers/specs/2026-08-13-subscription-included-visual-import-design.md`
- Modify: `docs/START_HERE.md`
- Modify: `README.md`

**Interfaces:**
- Documents direct localhost launch per project, the cloud-GPT/localhost boundary, included-subscription handoff steps, explicit metered API opt-in, and Figma placement as a separate project-GPT connector action.

- [ ] **Step 1: Update launch examples so the default server starts in import mode and every metered example requires `--run-mode openai`.**

- [ ] **Step 2: Document the exact operator flow.**

  1. Generate/edit images using the user's included ChatGPT/Figma credits or a local generator.
  2. Open the project-bound localhost Studio.
  3. Import, validate, review, curate, and export.
  4. Prepare a project-GPT packet only when exact project routing and approved anchor evidence exist.
  5. Let that project's GPT place assets with the Figma connector; the Studio itself does not upload.

- [ ] **Step 3: Run focused verification.**

  ```bash
  PYTHONPATH=tools/base-tool-contracts/src .venv/bin/python -m pytest -q tools/base-tool-contracts/tests
  cd tools/expression-studio && PYTHONPATH=../base-tool-contracts/src:src ../../.venv/bin/python -m pytest -q && node --check web/app.js
  cd ../sprite-animation-studio && PYTHONPATH=../base-tool-contracts/src:src ../../.venv/bin/python -m pytest -q && node --check web/app.js
  ../../.venv/bin/pip check
  git diff --check
  ```

- [ ] **Step 4: Run the repository-wide Base validation commands required by `AGENTS.md` against the exact fetched main SHA and record environment-dependent skips separately from failures.**

- [ ] **Step 5: Perform adversarial review.**

  Pressure-test cost-route self-attestation, upload size bypass, decompression bombs, source/filename path traversal, partial staging, duplicate visual pixels, anchor-evidence bypass, cross-project requests, stale run UI, symlink/hard-link races, export/packet hash drift, provider calls in import mode, and false Figma-upload claims. Fix every P0/P1 with a new failing regression test first.

- [ ] **Step 6: Commit documentation and final fixes.**

  ```bash
  git add README.md docs tools
  git commit -m "docs: document subscription-included visual workflow"
  ```

- [ ] **Step 7: Reconcile with latest main, rerun exact-HEAD checks, publish the branch, update the PR evidence, and merge only if the approved continuous-work gate has unresolved review threads `0`, exact-head required checks green, independent review P0/P1 `0`, and no broader-scope blocker.**
