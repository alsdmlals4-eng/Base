# Notion Connector Image Delivery Correction · 2026-08-22

## Authority

This file **supersedes the `Binary media delivery routing` subsection** of `NOTION_GPT_VISUAL_LAYOUT_CONTRACT.md` where the older wording made the local `Notion Native File Bridge` the default fallback immediately after a typed-MCP gap.

The rest of `NOTION_GPT_VISUAL_LAYOUT_CONTRACT.md` remains active.

This correction is based on a reproduced COC-Fiction Android acceptance run and the earlier `Visual Hub Pilot` precedent.

## Decision

For human-facing Notion page images, prefer the no-PC-action connector path first.

```text
image bytes available to ChatGPT
→ temporary Google Sheets image_uris transport
→ obtain short-lived signed HTTPS source URL
→ Notion create-attachment(source_url)
→ require status=uploaded
→ consume the returned suggested_markdown / file-upload:// source WITHOUT reconstructing it
→ save that source directly into the target Home / Visual page image block
→ fetch destination
→ require Notion-owned prod-files-secure readback
→ delete temporary Sheet
→ observe target client when rendering matters
```

The temporary Google Sheet is **transport only**, never the durable project workspace or visual authority.

## Verified evidence

COC-Fiction approved dark project-hub visual:

- temporary Sheets transport: PASS
- Notion `create-attachment(source_url)`: PASS
- returned `file-upload://` consumed directly by page update: PASS
- Home destination readback as Notion-owned `prod-files-secure...`: PASS
- Visual destination readback as Notion-owned `prod-files-secure...`: PASS
- temporary transport Sheet removed: PASS
- Android Notion actual dark dashboard pixels: **HUMAN_VISIBLE_PASS** by user screenshot on 2026-08-22

Historical precedent: the earlier `Visual Hub Pilot` used the same temporary-Sheets-to-Notion-copy pattern and persisted as a Notion-owned file.

## Root-cause correction

`create-attachment(source_url)` was not itself the failed architecture.

Known-bad variants were:

- GitHub raw URL used as the final Notion image source;
- jsDelivr URL used as the final Notion image source;
- a temporary signed URL stored directly as the final page image;
- a completed Notion upload reconstructed as a URL/string reference instead of consuming the connector-returned `file-upload://` source;
- reusing a page upload ID through the current Files-property wrapper when that wrapper cannot resolve it.

The working path is different: **Notion copies the temporary source, and the page consumes the connector-returned `file-upload://` attachment source directly.**

## Routing order

```text
Notion text / structure / databases / semantic placement
→ Notion MCP

human-facing page image
→ connector-only temporary Sheets transport
→ Notion create-attachment
→ returned file-upload:// suggested_markdown used directly
→ destination readback
→ client-visible verification when required

if connector-only binary transport is unavailable or actually fails
→ local Notion Native File Bridge (`ntn`) fallback

Asset Library Files/Preview property
→ optional metadata convenience, not visual authority
→ do not block Home / Visual / Asset-page image delivery on Preview
→ use direct Notion-owned image blocks on human-facing pages
```

## Asset Library Preview / Gallery decision

The `Preview` FILES property is **OPTIONAL / NON-AUTHORITY** for the current connector surface.

A clean isolated probe reproduced all of the following:

- historical `Visual Hub Pilot` fetch shows a valid `Preview` as a Notion-internal `file://{source, permissionRecord}` reference;
- SQL readback exposes that stored Preview as an internal file-ID array;
- current `create-attachment` returns a temporary FileUpload ID, not the durable internal file ID expected by the Files-property wrapper;
- `Preview=["file-upload://<id>"]` fails with `File ... not found`;
- `Preview=["<raw-upload-id>"]` fails with `File ... not found`;
- creating a database row while consuming the same upload in page content and Preview still fails;
- reconstructing a `file://{source, permissionRecord}` value from a page image fails with `User cannot access file id`;
- the temporary probe database was trashed after verification.

Therefore the workflow does **not** spend additional complexity on reverse-engineering private Notion file IDs.

Human-facing visual authority is:

```text
Project Home / Visual / approved Asset page
→ direct Notion-owned image block
→ semantic placement
→ destination readback
→ client-visible verification when required
```

The Asset database remains the structured metadata index. `Preview` may be populated when the connector exposes a supported durable Files-property attach path, but an empty `Preview` is not a defect when the approved visual is present on the owning human-facing page.

The legacy Gallery view that depends on `Preview` must be labeled as paused/limited rather than presented as the primary human visual surface.

Revisit this decision only when one of the following becomes true:

- the connector exposes a stable typed Files-property file-upload action;
- the connector returns a durable internal file ID suitable for the FILES property;
- Notion adds a supported gallery card-preview mode backed by page content through the current view DSL.

## Hard rules

1. **Do not require PowerShell/`ntn` when the connector-only path is executable and verified.**
2. **Do not keep the temporary Sheet.** Delete it after Notion destination readback.
3. **Do not store the signed transport URL as the durable Notion image source.**
4. **Do not reconstruct a successful FileUpload into a different URL/string representation.** Use the returned `suggested_markdown` / `file-upload://` source as-is.
5. A separate attachment may be created per durable page destination when reuse semantics are uncertain; correctness is preferred over unsafe reuse.
6. **Do not make Asset Library `Preview` a completion gate for human-facing image delivery.**
7. `READBACK_PASS != HUMAN_VISIBLE_PASS`; only actual Android/iOS/browser pixel observation can close a rendering claim.
8. Status text, filenames, empty Gallery cards, placeholders, or server-only signed URLs are not human-visible image evidence.

## Inline SVG raster preview fallback

`NOTION_INLINE_SVG_RASTER_PREVIEW_FALLBACK`

This is a **preview-only** secondary route for a narrow connector gap. Use **typed binary / verified primary transport first**. Do not choose this route merely because it avoids the stronger delivery path.

Use only when all of the following are true:

- the current connector accepts small UTF-8 attachment `content` but does not expose a usable local-binary parameter,
- a direct public HTTPS transport is unavailable, inappropriate or unnecessary,
- a low-resolution durable preview is sufficient for the exact human-facing purpose,
- the self-contained SVG stays inside the connector's text attachment size limit without destroying meaningful visual information.

Bounded route:

```text
approved local raster
→ downscale/compress raster to the minimum useful preview
→ embed the raster as a data URI inside UTF-8 SVG
→ create-attachment(content=<svg...>)
→ require status=uploaded
→ consume returned file-upload:// source directly
→ attach to the exact human-facing page
→ fetch destination
→ require Notion-owned prod-files-secure readback
→ record HIGH_RES_PIXEL_EQUIVALENT: NOT_PROVEN
→ observe target client only when rendering acceptance requires it
```

The fallback does not turn a preview into a production asset. Keep these evidence limits explicit:

```text
SERVER_ATTACHMENT: PASS only after upload result
DESTINATION_READBACK: PASS only after target fetch
HIGH_RES_PIXEL_EQUIVALENT: NOT_PROVEN
READBACK_PASS != HUMAN_VISIBLE_PASS
```

Reject this fallback when:

- production-quality or high-resolution source bytes themselves must live in Notion,
- the target client/workspace rejects or misrenders SVG/data-URI media,
- a stronger typed binary or already-verified transport route is available and fits the task,
- meeting the inline size ceiling requires unacceptable loss of visual meaning.

This route is additive. It does not supersede the verified connector transport above or the local `ntn` bridge fallback below.

## Local bridge status

`tools/notion-native-file-bridge` remains valid and maintained as a **fallback capability**, not the ordinary first step for page images.

Use it when:

- the connector cannot produce a usable temporary source URL;
- `create-attachment` is unavailable or fails real invocation;
- typed attachment is required by a surface the current connector cannot express **and that surface is actually required**;
- a connector regression is reproduced by the Reality Gate.

Do not delete the bridge solely because the connector path works today; retain it as a bounded fallback until the connector directly exposes stable typed binary upload/attachment for all required surfaces.

## Acceptance for future project images

A future approved image is healthy when:

```text
actual approved image bytes
→ connector transport
→ Notion-owned attachment
→ correct human-facing semantic placement
→ destination readback
→ no temporary Sheet left behind
→ target-client pixel verification when that client matters
```

`Preview`/Gallery decoration is optional and does not block this acceptance.

Once this path has passed for a target client/workspace combination, subsequent images may reuse the same delivery contract. Re-run human-visible verification when the client, workspace, connector implementation, or media delivery behavior materially changes.
