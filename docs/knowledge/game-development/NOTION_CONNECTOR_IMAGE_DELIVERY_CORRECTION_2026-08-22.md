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
→ treat separately from page-image delivery
→ do not infer PASS from Home/Visual success
→ current wrapper limitation remains an independent gap
```

## Hard rules

1. **Do not require PowerShell/`ntn` when the connector-only path is executable and verified.**
2. **Do not keep the temporary Sheet.** Delete it after Notion destination readback.
3. **Do not store the signed transport URL as the durable Notion image source.**
4. **Do not reconstruct a successful FileUpload into a different URL/string representation.** Use the returned `suggested_markdown` / `file-upload://` source as-is.
5. A separate attachment may be created per durable page destination when reuse semantics are uncertain; correctness is preferred over unsafe reuse.
6. Page/Home/Visual image success does not prove database Files-property or Gallery Preview success.
7. `READBACK_PASS != HUMAN_VISIBLE_PASS`; only actual Android/iOS/browser pixel observation can close a rendering claim.
8. Status text, filenames, empty Gallery cards, placeholders, or server-only signed URLs are not human-visible image evidence.

## Local bridge status

`tools/notion-native-file-bridge` remains valid and maintained as a **fallback capability**, not the ordinary first step for page images.

Use it when:

- the connector cannot produce a usable temporary source URL;
- `create-attachment` is unavailable or fails real invocation;
- typed attachment is required by a surface the current connector cannot express;
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

Once this path has passed for a target client/workspace combination, subsequent images may reuse the same delivery contract. Re-run human-visible verification when the client, workspace, connector implementation, or media delivery behavior materially changes.