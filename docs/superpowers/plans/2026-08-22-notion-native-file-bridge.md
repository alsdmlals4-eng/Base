# Notion Native File Bridge Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a free local bridge that uses Notion's official `ntn` CLI for binary upload and typed `file_upload` attachment while preserving MCP for normal page/document work.

**Architecture:** The bridge is a zero-runtime-dependency Python CLI that shells out only to the official `ntn` binary. Upload and typed attachment each require independent Notion API readback, and Android rendering remains outside the automated PASS ceiling. A root Base contract test guarantees the bridge remains narrow and is consumed by the existing `core-regression` unittest discovery.

**Tech Stack:** Python 3.12 standard library, Notion official `ntn` CLI, `unittest`, PowerShell onboarding helper.

**Spec:** `docs/superpowers/specs/2026-08-22-notion-native-file-bridge-design.md`

## Global Constraints

- Reuse official `ntn`; do not implement a parallel Notion authentication/multipart stack.
- No paid SaaS and no committed Notion secret.
- `ntn login`/OS keychain is the preferred credential path.
- MCP remains the default owner for Notion text, structure, databases, and semantic layout.
- The bridge owns only binary upload + typed `file_upload` attachment/readback.
- `READBACK_PASS != HUMAN_VISIBLE_PASS`; Android-visible pixels require actual device observation.
- Production implementation may not precede a failing test for the behavior.
- Base current-task branch only; no direct main write or ruleset bypass.

---

### Task 1: Lock the bridge contract with failing tests

**Files:**
- Create: `tools/notion-native-file-bridge/tests/test_ntn.py`
- Create: `tools/notion-native-file-bridge/tests/test_cli.py`
- Create: `tests/test_notion_native_file_bridge_contract.py`

**Interfaces:**
- Consumes: design spec only.
- Produces: expected public types `BridgeError`, `NtnClient`, and CLI commands `preflight`, `upload`, `append-image`, `set-cover`, `set-files-property`.

- [x] **Step 1: Add package behavior tests before implementation**

Write `unittest` cases that import the future package and require:

```python
client.preflight()
client.upload(path)
client.append_image(page_id, upload_id)
client.set_cover(page_id, upload_id)
client.set_files_property(page_id, property_name, upload_id, filename)
```

The fake runner must assert exact typed `ntn` argument construction and upload stdin bytes.

- [x] **Step 2: Add error/identity tests**

Tests require:

- SHA-256 + byte-count upload receipt,
- upload-ID/readback equality,
- destination readback after writes,
- ambiguous non-idempotent append state detection,
- `NOTION_API_TOKEN` redaction from surfaced subprocess errors,
- no `HUMAN_VISIBLE_PASS` emitted by the bridge.

- [x] **Step 3: Add Base integration contract test**

`tests/test_notion_native_file_bridge_contract.py` asserts package/docs paths, consumes the nested package test suite, and confirms `.github/workflows/validate-game-project-operating-system.yml` contains `python -m unittest discover -s tests -v`.

- [x] **Step 4: Run RED verification**

Observed RED before production implementation: package tests failed with `ModuleNotFoundError: notion_native_file_bridge`.

---

### Task 2: Implement the official `ntn` transport adapter

**Files:**
- Create: `tools/notion-native-file-bridge/pyproject.toml`
- Create: `tools/notion-native-file-bridge/src/notion_native_file_bridge/__init__.py`
- Create: `tools/notion-native-file-bridge/src/notion_native_file_bridge/ntn.py`

**Interfaces:**
- Produces:
  - `NOTION_VERSION = "2026-03-11"`
  - `BridgeError(code: str, detail: str = "")`
  - `UploadReceipt`
  - `NtnClient`

- [x] **Step 1: Implement minimal subprocess boundary**

`NtnClient` locates `ntn` with `shutil.which`, runs commands with captured stdout/stderr, and raises fail-closed `BridgeError` codes.

- [x] **Step 2: Implement secret redaction**

Before an error is emitted, replace the current exact value of `NOTION_API_TOKEN` with `<REDACTED>` in captured output.

- [x] **Step 3: Implement preflight**

Run:

```text
ntn --version
ntn api v1/users/me --notion-version 2026-03-11
```

Parse the API probe as JSON and return a machine-readable PASS receipt.

- [x] **Step 4: Implement upload + readback**

For a local file, infer MIME, read bytes, compute SHA-256, run:

```text
ntn files create --plain --filename <name> --content-type <mime>
```

with file bytes on stdin, parse the first tab-separated field as `upload_id`, then run official `ntn files get <id> --json` and require the same ID with `status=uploaded`.

- [x] **Step 5: Transport behavior is covered by the package suite**

The nested package suite is executed by the root `core-regression` contract rather than merely existing as unconsumed tests.

---

### Task 3: Implement typed destination attachment and CLI receipts

**Files:**
- Modify: `tools/notion-native-file-bridge/src/notion_native_file_bridge/ntn.py`
- Create: `tools/notion-native-file-bridge/src/notion_native_file_bridge/cli.py`

**Interfaces:**
- `append_image(page_id, upload_id)` uses typed child image fields.
- `set_cover(page_id, upload_id)` uses typed page-cover fields.
- `set_files_property(page_id, property_name, upload_id, filename)` uses typed Files-property fields.
- CLI prints one JSON object and returns `0` on PASS, `2` on blocked/fail-closed errors.

- [x] **Step 1: Implement typed image append**

Official CLI syntax is fixed to:

```text
children[0][type]=image
children[0][image][type]=file_upload
children[0][image][file_upload][id]=<id>
```

Then read back the created block and require `type=image`. If the write returns a block ID but readback fails, return `AMBIGUOUS_DESTINATION_STATE`; do not invite a blind retry because append is non-idempotent.

- [x] **Step 2: Implement typed cover update**

Use:

```text
cover[type]=file_upload
cover[file_upload][id]=<id>
```

and require a page readback with a Notion-hosted file cover.

- [x] **Step 3: Implement typed Files-property update**

Use bracket args under `properties[<name>][files][0]` with `type=file_upload`, upload ID, and display name. Read the page back and require a non-empty target Files property.

- [x] **Step 4: Implement argparse CLI**

Added `preflight`, `upload`, `append-image`, `set-cover`, `set-files-property`; output stable JSON receipts with no secret values.

- [ ] **Step 5: Exact-head package/core regression GREEN**

Fresh CI remains the authority. Current implementation is still under exact-head validation.

---

### Task 4: Add Windows onboarding and human-facing documentation

**Files:**
- Create: `tools/notion-native-file-bridge/README.md`
- Create: `tools/notion-native-file-bridge/windows/Install_Notion_Native_File_Bridge.ps1`
- Modify: `docs/knowledge/game-development/NOTION_GPT_VISUAL_LAYOUT_CONTRACT.md`

**Interfaces:**
- Installer detects Node/npm/`ntn`, installs official `ntn` via npm when absent, selects a verified Python 3.12+ launcher, installs bridge user-scoped, and optionally starts `ntn login`.
- Documentation routes binary work to the bridge only when typed MCP attachment is unavailable.

- [x] **Step 1: Document beginner setup and exact commands**

Includes Node 22+, npm 10+, `npm install --global ntn`, `ntn login`, bridge preflight, upload-once, typed attachment commands, ambiguous append handling, and Android verification.

- [x] **Step 2: Add fail-closed PowerShell installer**

The script never asks for/stores a token itself, validates Node/npm floors, tries `py -3.12` then `python` fallback, and runs module-based preflight without requiring the Python user Scripts directory to already be on PATH.

- [x] **Step 3: Update Notion visual-layout contract**

Media routing:

```text
MCP typed media attach available + verified -> use MCP
otherwise local official ntn bridge -> typed file_upload
external CDN -> not a substitute when target client has known 422
```

- [ ] **Step 4: Exact-head root integration contract GREEN**

Fresh CI remains the authority.

---

### Task 5: Verify, adversarially review, and integrate

**Files:**
- Modify only files required by verified findings.
- This plan records executed evidence and leaves live Android acceptance separate.

**Interfaces:**
- Produces exact-head CI evidence and merge/postmerge evidence.

- [ ] **Step 1: Fresh exact-head focused + root tests GREEN**

`core-regression` must execute both the root contract and the nested package unit suite.

- [x] **Step 2: Adversarial full loop 1 — secrets/auth**

Findings addressed: official auth owner retained; token never committed; exact `NOTION_API_TOKEN` value redacted from subprocess output; `ntn login` full-member requirement documented.

- [x] **Step 3: Adversarial full loop 2 — typed API semantics/readback**

Official current Notion CLI docs verified bracket syntax for nested/array fields, typed image append, Files-property attach, `ntn files create --plain`, and `ntn files get --json`; page-cover typed `file_upload` was checked against current Update Page/File Upload docs.

- [x] **Step 4: Adversarial full loop 3 — Windows/onboarding**

Finding addressed: `py` existing without Python 3.12 no longer blocks a valid `python` 3.12 fallback; preflight no longer depends on console-script PATH propagation in the current shell.

- [x] **Step 5: Adversarial full loop 4 — reuse/partial failure**

Finding addressed: non-idempotent image append reports `AMBIGUOUS_DESTINATION_STATE` when write returns a block ID but readback fails, requiring destination inspection before retry.

- [x] **Step 6: Adversarial full loop 5 — authority/evidence ceiling**

MCP remains default Notion owner; bridge is binary-only; external-CDN regression is rejected after reproduced Android 422; bridge cannot emit `HUMAN_VISIBLE_PASS`.

- [x] **Step 7: Open current-task PR referencing #604**

Draft PR #606 is open. It does not auto-close #604 because device-visible acceptance is pending.

- [ ] **Step 8: Require fresh exact-head CI**

Confirm `core-regression` actually runs `tests/test_notion_native_file_bridge_contract.py`, required `ci-gate` passes, and no unresolved blocking review/thread remains.

- [ ] **Step 9: Merge using repository-allowed method and exact HEAD**

No force, admin, or ruleset bypass.

- [ ] **Step 10: Post-merge main readback**

Read back bridge code/docs/tests from new main and record merge SHA.

- [ ] **Step 11: Keep live Android acceptance explicit**

Issue #604 remains `LIVE_ACCEPTANCE_PENDING` until the bridge is run with the user's `ntn login`, the approved dark COC dashboard is attached by typed `file_upload`, and an Android screenshot shows the actual pixels.
