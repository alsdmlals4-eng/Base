# Notion Connector Image Delivery Correction · 2026-08-22

## Authority

This file **supersedes the `Binary media delivery routing` subsection** of `NOTION_GPT_VISUAL_LAYOUT_CONTRACT.md`.

The older 2026-08-22 route proved that Notion can persist an uploaded file and render it on Android, but it used a temporary Google Sheet to obtain an HTTPS transport URL and retained a local `ntn` bridge fallback. Those transport choices are now superseded by the latest project-workspace decision:

```text
NO_SHEETS_NO_LOCAL_BRIDGE_IMAGE_TRANSPORT
Google Sheets: FORBIDDEN_AS_NEW_IMAGE_TRANSPORT
LOCAL_NOTION_FILE_BRIDGE: RETIRED_FROM_ACTIVE_ROUTE
```

Google Sheets remains `MIGRATION_ONLY_UNTIL_REMOVAL`. A local Notion file bridge may remain in Git history or historical source for rollback/audit, but it is not an active/default/fallback project route.

The rest of `NOTION_GPT_VISUAL_LAYOUT_CONTRACT.md` remains active after its matching routing update.

## Current decision

Human-facing Notion images use a direct Notion-owned attachment path only when the current client exposes a supported connector route and a real invocation proves it.

```text
approved image / visual
→ trusted direct HTTPS source or connector-native attachment source
→ Notion create-attachment(source_url) when that callable schema is actually available
→ require upload completion
→ consume returned suggested_markdown / file-upload:// source as-is
→ attach to the exact Project Notion Home / Visual / Asset destination
→ fetch destination
→ require Notion-owned prod-files-secure readback
→ observe target client when rendering matters
```

The ordered transport contract is therefore:

```text
trusted direct HTTPS source or connector-native attachment source
→ Notion create-attachment(source_url)
→ suggested_markdown / file-upload:// source
→ prod-files-secure readback
```

A workspace capability hint is not enough. The current client must expose a callable function with a usable schema and the real invocation must succeed.

If the approved image exists only as local/session bytes and the current client has no supported direct Notion attachment source, use:

```text
BLOCKED_NO_DIRECT_NOTION_BINARY_TRANSPORT
```

Do not substitute Google Sheets or a local bridge. Do not silently introduce another CDN, local server, paid automation service, Figma, HTML workspace, Tool Hub, or QA Studio merely to make the upload succeed.

This fail-closed state blocks only the binary-delivery-dependent step. Planning, visual review, repository work, Notion text/structure updates, and other independent work may continue.

## Historical verified evidence — preserved, not current routing authority

COC-Fiction approved dark project-hub visual previously demonstrated the following historical transport experiment:

- temporary Google Sheets URL transport: `HISTORICAL_PASS`
- Notion `create-attachment(source_url)`: `PASS`
- returned `file-upload://` consumed directly by page update: `PASS`
- Home destination readback as Notion-owned `prod-files-secure...`: `PASS`
- Visual destination readback as Notion-owned `prod-files-secure...`: `PASS`
- temporary Sheet removed: `PASS`
- Android Notion actual dark dashboard pixels: **HUMAN_VISIBLE_PASS** by user screenshot on 2026-08-22

The earlier `Visual Hub Pilot` also demonstrated that Notion can copy a temporary source into a Notion-owned file.

These facts remain useful evidence about Notion persistence and rendering. They do **not** authorize Google Sheets or the local bridge as a current project transport.

```text
HISTORICAL_TRANSPORT_SUCCESS
!= CURRENT_DEFAULT_ROUTE_AUTHORITY
```

## Root-cause findings retained

`create-attachment(source_url)` was not itself the failed architecture.

Known-bad variants remain:

- GitHub raw URL used as the final Notion image source;
- jsDelivr URL used as the final Notion image source;
- a temporary signed URL stored directly as the final page image;
- a completed Notion upload reconstructed as another URL/string instead of consuming the connector-returned `file-upload://` source;
- reusing a page upload ID through a Files-property wrapper that cannot resolve it;
- treating workspace capability discovery as proof of a callable current-client upload surface.

When a supported direct source exists, the useful principle is still:

> Notion copies the source into a Notion-owned attachment, and the page consumes the connector-returned attachment representation directly.

The reusable principle is **Notion-owned copy + exact returned attachment source + destination readback**, not the old transport intermediary.

## Routing order

```text
Notion text / structure / databases / semantic placement
→ Notion MCP

human-facing page image
→ current-client capability check
→ trusted direct HTTPS source or connector-native attachment source available?
  → yes: direct Notion attachment invocation
  → upload completion
  → returned attachment source used as-is
  → destination readback
  → target-client pixel observation when required
  → no: BLOCKED_NO_DIRECT_NOTION_BINARY_TRANSPORT

Asset Library Files/Preview property
→ treat separately from page-image delivery
→ do not infer PASS from Home/Visual success
→ current Files/Gallery capability must be verified independently
```

## Hard rules

1. **Google Sheets: FORBIDDEN_AS_NEW_IMAGE_TRANSPORT.** Migration-only legacy Sheets never become a new binary relay.
2. **LOCAL_NOTION_FILE_BRIDGE: RETIRED_FROM_ACTIVE_ROUTE.** Do not ask the user to run PowerShell/`ntn` to compensate for a connector attachment gap.
3. **Do not substitute Google Sheets or a local bridge** when direct binary transport is unavailable; report `BLOCKED_NO_DIRECT_NOTION_BINARY_TRANSPORT` for that dependent step.
4. **Do not store an external or signed transport URL as the durable Notion image source.**
5. **Do not reconstruct a successful FileUpload into a different URL/string representation.** Use the returned `suggested_markdown` / `file-upload://` source as-is.
6. A separate attachment may be created per durable page destination when reuse semantics are uncertain; correctness is preferred over unsafe reuse.
7. Page/Home/Visual image success does not prove database Files-property or Gallery Preview success.
8. `READBACK_PASS != HUMAN_VISIBLE_PASS`; only actual Android/iOS/browser pixel observation can close a rendering claim.
9. Status text, filenames, empty Gallery cards, placeholders, or server-only signed URLs are not human-visible image evidence.
10. A historical success path may remain in evidence/history without remaining executable in current routing.

## Acceptance for future project images

A future approved image is healthy only when the currently supported direct route can prove:

```text
actual approved image bytes or trusted direct source
→ direct Notion attachment capability actually callable
→ Notion-owned attachment
→ correct Project relation / semantic placement
→ destination readback
→ no Google Sheet / local bridge / retired project-management tool introduced
→ target-client pixel verification when that client matters
```

If direct transport cannot be proven, the correct result is `BLOCKED_NO_DIRECT_NOTION_BINARY_TRANSPORT`, not an invented workaround.

Re-run the Reality Gate when the Notion connector/client attachment schema changes, when Files/Gallery properties gain a newly callable attachment surface, or when a target client changes media-delivery behavior.