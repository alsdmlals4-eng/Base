# Notion Approved Original-First Gate

## Purpose

This gate fixes the default delivery rule for **approved project visuals** in Notion.

It is a narrow addendum to:

- `docs/knowledge/game-development/NOTION_GPT_VISUAL_LAYOUT_CONTRACT.md`
- `docs/knowledge/methods/NOTION_OFFICIAL_PRODUCT_OPERATING_REFERENCE.md`
- `docs/knowledge/game-development/NOTION_VISUAL_ASSET_AND_FLOW_WORKFLOW.md`

Those documents continue to own general Notion behavior, layout, fallback transport, client-visible evidence, and visual continuity. **For an already approved canonical visual, this gate has priority over any wording that could be read as making a reduced preview the normal delivery artifact.**

## Decision

`NOTION_APPROVED_ORIGINAL_FIRST_GATE`

For an approved visual, the default human-facing Notion delivery is the **canonical approved original itself**, stored as a Notion-owned image/file attachment when the active tool path can do so reliably.

A reduced preview is a fallback/display derivative, not the default source of truth.

```text
approved visual
→ resolve canonical source/version
→ record pixel dimensions + file size + hash when available
→ compare transport candidate with canonical evidence
→ if chat/intermediate transport re-encoded the file, reacquire canonical source bytes
→ upload canonical original bytes to Notion
→ attach returned file-upload result without reconstructing its private identifier
→ destination fetch/readback confirms Notion-owned persistence
→ human Notion “Original” / equivalent client observation when that claim is required
```

## Byte fidelity vs pixel fidelity

`BYTE_ORIGINAL != PIXEL_EQUIVALENT`

- `BYTE_ORIGINAL`: bytes/hash match the canonical approved source.
- `PIXEL_EQUIVALENT`: dimensions and rendered pixels may match, but encoding, alpha/channel layout, metadata, compression, file size, or hash differs.

When a canonical Hash exists, a chat upload or temporary transport artifact that is only `PIXEL_EQUIVALENT` must not silently replace the byte-original authority.

```text
canonical Hash exists
+ transport candidate Hash differs
→ do not label candidate ORIGINAL
→ reacquire canonical source
→ upload canonical source bytes
```

## Preview exception

`DISPLAY_PREVIEW_ONLY`

A smaller preview may be added when:

- a specific Notion client cannot reliably render the original inline;
- an intentionally cropped Gallery/Home thumbnail improves navigation;
- an API/client upload ceiling blocks the original inline representation;
- the original is preserved as a Notion-owned file but a smaller inline rendering is operationally safer.

The preview must remain explicitly derivative.

```text
DISPLAY_PREVIEW
→ optimized derivative
→ may be resized/compressed/cropped for the stated display purpose
→ never replaces original authority

CANONICAL ORIGINAL
→ approved source bytes/version
→ Notion-owned image/file attachment by default
→ provenance + dimensions + size + hash retained when available
```

External Drive/GitHub/storage may remain provenance or source backup, but **external-only storage is not the normal completion state when the current Notion path can attach the canonical original directly**.

## Delivery evidence states

Do not collapse server persistence, post-storage byte verification, and human client rendering into one PASS.

- `HIGH_RES_NOTION_SERVER_PASS`
  - canonical original was selected using pre-upload dimensions/size/hash evidence;
  - upload completed;
  - the returned upload object/source was attached;
  - destination readback resolves to a Notion-owned file/image.
- `POST_STORAGE_HASH_READBACK_NOT_AVAILABLE`
  - current connector cannot re-download the stored Notion file and recompute its hash;
  - do not fabricate byte-level post-storage proof.
- `HUMAN_ORIGINAL_VIEW_NOT_RUN`
  - no human/browser/mobile observation of Notion’s Original/equivalent view was performed.
- `HIGH_RES_NOTION_PASS`
  - use only when the task’s required original-resolution claim has also been closed by an available equivalent readback or human observation.

`HIGH_RES_NOTION_SERVER_PASS != HIGH_RES_NOTION_PASS`

## Failure classifications

- `LEGACY_PREVIEW_NEEDS_ORIGINAL`: historical low-resolution preview exists but canonical original has not yet been promoted to the new route.
- `UPLOAD_TRANSPORT_BLOCKED`: current tool cannot deliver canonical bytes without an unsupported step. Do not resize/recompress merely to report success.
- `APPROVED_VISUAL_NOT_DELIVERED`: only an external link/status/filename exists; no required Notion-owned delivery evidence exists.
- `DISPLAY_PREVIEW_ONLY`: derivative preview is intentionally retained alongside the original.

## Project/Home behavior

- Project Home shows the approved visual at a useful display width; changing block display width does **not** require lowering the stored source resolution.
- Visual Bible / approved Asset page keeps the canonical original accessible and preserves provenance/version evidence.
- Asset database `Preview`/Gallery fields are presentation helpers, not a replacement for the canonical original page/file authority.
- Existing low-resolution previews may remain as history/reference; do not rename them as originals or delete them merely to hide migration history.

## Completion checklist

- [ ] Approved canonical source/version resolved.
- [ ] Pixel dimensions and file format recorded.
- [ ] File size recorded.
- [ ] Hash recorded/compared when available.
- [ ] Chat/intermediate re-encoding was detected rather than assumed away.
- [ ] Canonical source bytes were used when byte fidelity matters.
- [ ] Original was attached as a Notion-owned image/file.
- [ ] Destination readback confirms Notion-owned persistence.
- [ ] Any preview is labeled `DISPLAY_PREVIEW_ONLY` / legacy reference.
- [ ] Post-storage hash limitations are reported explicitly.
- [ ] Human Original/client-visible validation is reported separately from server readback.

## Implementation Reality Gate

An upload call, external link, signed URL, filename, or low-resolution preview alone is not proof that the approved original was delivered.

The minimum server-side claim requires:

```text
canonical pre-upload evidence
→ upload status
→ attach
→ destination readback
```

The minimum human-visible original-resolution claim additionally requires the client-visible/original-view evidence that the current tool cannot otherwise prove.
