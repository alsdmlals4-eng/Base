# Public Video Research & Creative Provider Adapters Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a zero-incremental-cost, fail-closed public-video caption ingest reference implementation and connect provider-neutral creative production plus `HUMAN_EDIT_DELTA` to existing Base reuse owners.

**Architecture:** Keep the public-video Tool narrow: `yt-dlp` discovers metadata/caption URLs, standard-library code selects and normalizes WebVTT, and full transcripts default to ignored `.tmp/` storage. Do not add a new broad Skill/Hub; Visual provider switching and total human-edit cost live as contracts inside existing reuse modules.

**Tech Stack:** Python 3.12 standard library, optional external `yt-dlp` CLI, Markdown/YAML contracts, `unittest`, GitHub Actions.

**Spec:** `docs/superpowers/specs/2026-08-22-public-video-research-and-creative-provider-adapters-design.md`

## Global Constraints

- `ZERO_INCREMENTAL_COST_REQUIRED`: no paid transcript API, proxy, API credit, new subscription, or separately metered service.
- No video/audio download or storage in the Base reference implementation.
- Full third-party transcripts default to `.tmp/public-video-research/` and are not committed.
- Missing transcript evidence must fail closed as `ASR_FALLBACK_REQUIRED`/`BLOCKED_UNVERIFIED`, not become inferred content.
- No new broad Skill/Agent/Hub.
- Project Visual Canon and project asset approval remain project-owned.
- No project repository mutation in this change.

---

### Task 1: Define public-video ingest behavior with failing tests

**Files:**
- Create: `tests/test_public_video_research_ingest.py`
- Create later in Task 2: `tools/public_video_research_ingest.py`

**Interfaces:**
- Consumes: none.
- Produces: expected behavior for `extract_video_id`, `choose_caption_track`, `parse_vtt`, `build_evidence_packet`, and `NoCaptionTrack`.

- [ ] **Step 1: Write the failing test**

Create tests that assert:

```python
self.assertEqual("ItWEhmEm7jA", module.extract_video_id("https://youtu.be/ItWEhmEm7jA?si=x"))
self.assertEqual("ItWEhmEm7jA", module.extract_video_id("https://www.youtube.com/watch?v=ItWEhmEm7jA"))
```

and fixture-based behavior:

```python
track = module.choose_caption_track(metadata, ["ko", "en"])
self.assertEqual("youtube_manual_caption", track["source_kind"])
self.assertEqual("ko", track["language"])
```

```python
segments = module.parse_vtt(VTT_WITH_ROLLING_DUPLICATES)
self.assertEqual(["첫 문장", "두 번째 문장"], [item["text"] for item in segments])
```

```python
with self.assertRaises(module.NoCaptionTrack):
    module.choose_caption_track({"subtitles": {}, "automatic_captions": {}}, ["ko", "en"])
```

- [ ] **Step 2: Run test to verify RED**

Run in a temporary reconstructed workspace:

```bash
python -m unittest tests/test_public_video_research_ingest.py -v
```

Expected: import/file failure because `tools/public_video_research_ingest.py` does not yet exist.

- [ ] **Step 3: Keep RED evidence**

Record the exact failing command/output in the implementation verification notes; do not change the expected behavior to make the test pass.

---

### Task 2: Implement the narrow caption ingest Tool

**Files:**
- Create: `tools/public_video_research_ingest.py`
- Test: `tests/test_public_video_research_ingest.py`

**Interfaces:**
- Consumes: URL string, yt-dlp metadata dictionary, WebVTT text.
- Produces:
  - `extract_video_id(value: str) -> str`
  - `choose_caption_track(metadata: Mapping[str, object], languages: Sequence[str]) -> dict[str, object]`
  - `parse_vtt(text: str) -> list[dict[str, object]]`
  - `build_evidence_packet(...) -> dict[str, object]`
  - CLI JSON output under `.tmp/public-video-research/` by default.

- [ ] **Step 1: Implement URL parsing and fail-closed exceptions**

Support bare 11-character IDs plus `youtu.be`, `/watch?v=`, `/shorts/`, `/embed/`. Raise `ValueError` for unsupported input.

- [ ] **Step 2: Implement caption selection**

Search manual `metadata["subtitles"]` before `metadata["automatic_captions"]`; within each source, obey language priority and prefer `vtt` entries containing a URL. Return `source_kind`, `language`, `is_generated`, `url`, `ext`.

- [ ] **Step 3: Implement deterministic WebVTT normalization**

Parse timestamp cues, HTML-unescape text, remove tags, collapse whitespace, strip VTT positioning suffixes, and remove only consecutive duplicate caption text. Return `{start_sec, end_sec, text}` dictionaries.

- [ ] **Step 4: Implement metadata/retrieval packet**

Use subprocess only for:

```text
yt-dlp --version
yt-dlp --ignore-config --skip-download --no-playlist --dump-single-json <url>
```

Use `urllib.request` only for the selected caption track URL. Do not request video/audio formats. No caption raises `NoCaptionTrack`; CLI serializes that state as `ASR_FALLBACK_REQUIRED` and exits nonzero.

- [ ] **Step 5: Run GREEN tests**

```bash
python -m py_compile tools/public_video_research_ingest.py tests/test_public_video_research_ingest.py
python -m unittest tests/test_public_video_research_ingest.py -v
```

Expected: all tests PASS.

---

### Task 3: Register the Tool and provider-neutral Visual contract

**Files:**
- Modify: `docs/knowledge/game-development/reuse/PRODUCTION_TOOL_WORKFLOW_MODULES.md`
- Modify: `docs/knowledge/game-development/reuse/VISUAL_ASSET_MATERIAL_MODULES.md`
- Modify: `docs/knowledge/game-development/reuse/REUSABLE_MODULE_REGISTRY.md`
- Modify: `templates/research/PROJECT_REUSE_OPPORTUNITY_SCAN.md`

**Interfaces:**
- Consumes: Tool API from Task 2 and existing reuse owner rules.
- Produces: `RM-TOOL-005 PUBLIC_VIDEO_RESEARCH_INGEST_ADAPTER`, `RM-VIS-006 VISUAL_CREATIVE_PROVIDER_ADAPTER`, and `HUMAN_EDIT_DELTA` fields under existing `RM-WORK-002`.

- [ ] **Step 1: Add RM-TOOL-005 contract**

Document source ladder, local-only transcript storage, zero-paid-fallback rule, fail-closed states, reference implementation path, and evidence ceiling.

- [ ] **Step 2: Extend RM-WORK-002 with HUMAN_EDIT_DELTA**

Add exact fields from the spec without creating a new workflow module.

- [ ] **Step 3: Add RM-VIS-006 contract**

Document provider routes `AI_SERVICE | LOCAL_MODEL | MANUAL | OUTSOURCE`, project-canon authority, rights/provenance link, zero-metered-cost rule, and no-auto-approval boundary.

- [ ] **Step 4: Update registry and project scan handoff**

Register both IDs and add public-video evidence provenance fields to the scan template. Do not add project adoption claims.

---

### Task 4: Add regression contracts and relevant CI execution

**Files:**
- Modify: `tests/test_p04_reverse_engineering_reuse_pipeline.py`
- Modify: `.github/workflows/validate-evidence-knowledge.yml`

**Interfaces:**
- Consumes: new module contracts and Tool path.
- Produces: regression checks that fail if the Tool/provider/HUMAN_EDIT_DELTA contracts disappear.

- [ ] **Step 1: Extend P04 static contract tests**

Require:

```text
RM-TOOL-005
PUBLIC_VIDEO_RESEARCH_INGEST_ADAPTER
RM-VIS-006
VISUAL_CREATIVE_PROVIDER_ADAPTER
HUMAN_EDIT_DELTA
tools/public_video_research_ingest.py
```

- [ ] **Step 2: Add Tool/test to evidence-knowledge workflow path and commands**

Add `tools/public_video_research_ingest.py` and `tests/test_public_video_research_ingest.py` to path triggers, `py_compile`, `unittest`, and uploaded evidence file list.

- [ ] **Step 3: Run reconstructed branch regression tests**

```bash
python -m unittest tests/test_public_video_research_ingest.py tests/test_p04_reverse_engineering_reuse_pipeline.py -v
```

Expected: PASS.

---

### Task 5: Five-loop adversarial review, branch readback, and PR

**Files:**
- Review all changed paths.
- No new file unless a validated finding requires a bounded correction before PR creation.

**Interfaces:**
- Consumes: complete feature branch.
- Produces: clean reviewed branch and one PR targeting `main`.

- [ ] **Step 1: Loop 1 — authority/duplication attack**

Attack whether any new broad owner duplicates periodic-source, Skill, Visual, or Asset authority. Fix validated overlap, rerun tests, re-read full scope.

- [ ] **Step 2: Loop 2 — cost/dependency/recovery attack**

Attack paid/proxy/cloud fallback, hidden install assumptions, yt-dlp absence, no-caption path, rollback. Fix, rerun, re-read full scope.

- [ ] **Step 3: Loop 3 — copyright/provenance/storage attack**

Attack transcript retention, generated-caption labeling, timestamp provenance, rights escalation. Fix, rerun, re-read full scope.

- [ ] **Step 4: Loop 4 — parser/runtime correctness attack**

Attack URL parsing, language priority, manual-vs-auto selection, empty/rolling VTT, subprocess errors, deterministic tests. Fix, rerun, re-read full scope.

- [ ] **Step 5: Loop 5 — regression/CI/document consistency attack**

Attack registry IDs, owner links, test coverage, workflow execution, stale status claims, and scope creep. Fix, rerun, re-read full scope. Exit only with `CLEAN_REVIEW_EXIT`.

- [ ] **Step 6: Read branch back from GitHub**

Fetch each changed path from `feat/video-research-ingest-adapter` and verify exact content exists on remote.

- [ ] **Step 7: Open PR**

Open one PR from `feat/video-research-ingest-adapter` to `main`. After this point, do not mutate/merge/close the PR unless the user explicitly names that PR number and allowed action.

- [ ] **Step 8: Inspect exact-head CI**

Fetch PR head commit workflow runs/status. Report PASS/FAIL truthfully. If CI fails, stop with the exact blocker; do not mutate the open PR without explicit authorization.
