# Notion Native File Bridge Design

## Status

- Date: 2026-08-22
- Issue: Base #604
- Decision: **ADOPT official `ntn` CLI as a thin local binary-media bridge**
- Scope: Notion binary file upload + typed `file_upload` attachment only
- Out of scope: replacing Notion MCP for text, databases, page structure, semantic placement, or general automation

## Problem

The existing ChatGPT↔Notion path can reliably read and write text/page/database structure, but COC-Fiction Android tests proved that media claims require a different transport boundary.

Observed failures:

1. `raw.githubusercontent.com` image → Android Notion 422.
2. `cdn.jsdelivr.net` image → Android Notion 422.
3. MCP `create-attachment(source_url)` → upload/readback creates a Notion-hosted object, but the attachment produced through the current ChatGPT Markdown/string surface still renders as `app.notion.com` 422 on Android.
4. Reusing the resulting string/file reference as a Files property produces a broken Gallery card.
5. Server readback therefore does not prove Android-visible pixels.

The official Notion file-upload contract uses a typed `file_upload` object after upload. The current ChatGPT connector surface does not expose the required typed attach payload end to end.

## Goals

1. Upload a local PNG/JPG or other Notion-supported file through Notion's official upload lifecycle.
2. Preserve the returned `file_upload` ID and attach it with typed Notion API fields.
3. Support the three human-facing placements needed by the current workflow:
   - page body image block,
   - page cover,
   - database `FILES` property such as `Preview`.
4. Reuse one upload ID across multiple destinations while the official object remains valid.
5. Emit deterministic JSON receipts with enough identity information to audit what was uploaded and where it was attached.
6. Keep Android/client rendering as a separate `HUMAN_VISIBLE_PASS` gate.
7. Avoid a new paid SaaS and avoid committing secrets.

## Non-goals

- No new broad Skill.
- No replacement for Notion MCP search/fetch/update/database tools.
- No external image CDN as a default human-facing image path.
- No hidden token file in the repository.
- No automatic claim that a successful upload/readback means Android rendering works.
- No bespoke multipart HTTP stack unless the official CLI becomes unavailable or insufficient.

## Alternatives

### A. Keep using Notion MCP only — REJECT

Pros: no local dependency.
Cons: the current surfaced attach representation has already produced Android 422 across inline, cover, and Gallery use. More URL permutations would repeat a disproven architecture.

### B. Thin wrapper over official `ntn` CLI — ADOPT

Pros:

- reuses Notion's official upload lifecycle and API client,
- OAuth login and OS keychain are owned by the official CLI,
- no Python HTTP dependency or custom multipart implementation,
- works as a small local capability beside existing MCP,
- low long-term maintenance and no additional SaaS cost.

Cons:

- local Node.js/`ntn` installation required,
- first login requires user OAuth approval,
- actual Android rendering still requires device observation.

### C. Custom Python Notion REST client — FALLBACK

Pros: complete transport control.
Cons: duplicates official authentication, multipart upload, API-version handling, error normalization, and credential management. Higher maintenance with no current user-value advantage.

## Architecture

```text
ChatGPT / Notion MCP
  ├─ search/fetch/page text/database/layout
  └─ decide semantic placement

Local Notion Native File Bridge
  └─ official `ntn`
      ├─ preflight/auth probe
      ├─ files create < local bytes
      ├─ typed file_upload attach
      └─ API readback

Evidence Gate
  ├─ upload invocation PASS
  ├─ Notion destination readback PASS
  └─ Android/browser actual pixel observation -> HUMAN_VISIBLE_PASS
```

The bridge is intentionally narrow. MCP stays the default owner for page/document work. The bridge is invoked only when a real binary must become a typed Notion `file_upload` attachment.

## Package layout

```text
tools/notion-native-file-bridge/
  pyproject.toml
  README.md
  src/notion_native_file_bridge/
    __init__.py
    cli.py
    ntn.py
  tests/
    test_cli.py
    test_ntn.py
  windows/
    Install_Notion_Native_File_Bridge.ps1

tests/
  test_notion_native_file_bridge_contract.py
```

The root test is a Base integration/contract test consumed by `core-regression`; package tests cover behavior in isolation.

## Interface

Executable: `notion-native-file-bridge`

### `preflight`

Checks:

1. `ntn` exists and returns a version.
2. authenticated Notion API probe succeeds using API version `2026-03-11`.

Output example:

```json
{"status":"PASS","operation":"preflight","ntn_version":"...","api_version":"2026-03-11"}
```

### `upload --file PATH`

- reads local bytes only,
- infers MIME type,
- invokes `ntn files create --plain --filename ... --content-type ...`,
- reads the returned upload ID back through `v1/file_uploads/{id}`,
- emits filename, MIME, byte count, SHA-256, upload ID, and upload status.

The SHA-256 is evidence identity, not a secret.

### `append-image --page-id ID --upload-id ID`

Uses typed API arguments equivalent to:

```json
{
  "children": [{
    "type": "image",
    "image": {
      "type": "file_upload",
      "file_upload": {"id": "<UPLOAD_ID>"}
    }
  }]
}
```

Then reads back the created block and requires `type=image`.

### `set-cover --page-id ID --upload-id ID`

Uses typed `cover[type]=file_upload` and `cover[file_upload][id]=...`, then reads back the page.

### `set-files-property --page-id ID --property NAME --upload-id ID --filename NAME`

Updates a Notion Files property with a typed `file_upload` item and reads the page back to ensure the property is non-empty.

## Authentication and security

Preferred authentication:

```text
ntn login
→ browser OAuth
→ official CLI stores credential in OS keychain
```

Rules:

- never commit a Notion token,
- never print credential values in receipts,
- if `NOTION_API_TOKEN` exists for unattended use, redact that exact value from subprocess stderr/stdout before surfacing errors,
- no arbitrary remote `source_url` input in the bridge; upload source is a local file path,
- fail closed when `ntn` is absent, authentication is missing, the upload readback disagrees, or destination readback is missing.

## Evidence states

The shared connector/MCP Reality Gate remains authoritative.

```text
ntn executable/auth probe         -> CALLABLE_SCHEMA_PRESENT / preflight evidence
file upload + upload readback     -> INVOCATION_PASS + READBACK_PASS
typed destination attach/readback -> EFFECT_VERIFIED / READBACK_PASS
Android actual pixels             -> HUMAN_VISIBLE_PASS
```

A bridge operation never emits `HUMAN_VISIBLE_PASS` itself.

## Windows onboarding

Windows uses the official npm distribution rather than a custom credential implementation:

1. require Node.js 22+ and npm 10+;
2. install `ntn` globally if absent;
3. install this zero-runtime-dependency Python package locally/user-scoped;
4. optionally run `ntn login`;
5. run bridge `preflight`.

The installer does not request or persist tokens itself.

## Failure behavior

CLI returns JSON on stdout and exits non-zero on blockers.

Representative codes:

- `NTN_UNAVAILABLE`
- `NTN_COMMAND_FAILED`
- `INVALID_NTN_JSON`
- `UPLOAD_ID_MISSING`
- `UPLOAD_READBACK_MISMATCH`
- `DESTINATION_READBACK_FAILED`
- `FILE_NOT_FOUND`
- `UNSUPPORTED_CONTENT_TYPE`

Errors redact any current `NOTION_API_TOKEN` value before reporting.

## Test strategy

### Unit tests

Use fake subprocess runners to verify:

- typed command construction,
- local bytes are passed through stdin for upload,
- SHA-256/content-length receipt identity,
- upload readback mismatch fails closed,
- attach readback required,
- token redaction,
- CLI JSON/exit-code behavior.

### Base integration contract

A root `unittest` checks that:

- package files exist,
- official `ntn` is the transport owner,
- no Python HTTP dependency is introduced,
- docs preserve the `HUMAN_VISIBLE_PASS` ceiling,
- the root test is consumed by `core-regression` through test discovery.

### Live verification

CI cannot authenticate to the user's Notion workspace and must not receive their personal token. Live acceptance is therefore:

```text
Windows preflight
→ upload approved COC image once
→ attach to a disposable/target page
→ Notion readback
→ user opens Android Notion
→ actual dark dashboard pixels visible
```

Until the last observation, Base Issue #604 remains open or explicitly marked live-acceptance pending.

## Rollback

The bridge is additive. If the official CLI changes or the ChatGPT Notion connector later exposes typed `file_upload` attachment directly:

1. stop routing binary media through the local bridge,
2. keep the shared Reality Gate and tests for evidence ceilings,
3. deprecate/remove the wrapper in a normal Base change,
4. do not change project Story/Runtime canon.
