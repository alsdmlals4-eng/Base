# Notion Native File Bridge

A narrow local adapter for one capability the current ChatGPT↔Notion surface does not reliably preserve: **official typed `file_upload` attachment for binary media**.

It does **not** replace Notion MCP. Use MCP for search, text, page structure, databases, semantic placement, and readback. Use this bridge only when a local file must be uploaded to Notion and attached as an image block, page cover, or Files property.

## Why this exists

COC-Fiction Android tests reproduced these failures:

- GitHub raw image → 422
- jsDelivr image → 422
- current ChatGPT/MCP attachment representation → server readback exists, but Android `app.notion.com` 422
- Gallery using the same representation → broken preview

Notion's official upload lifecycle is different:

```text
local bytes
→ official File Upload
→ upload status = uploaded
→ typed file_upload attachment
→ destination readback
→ Android/browser human-visible verification
```

The bridge delegates that lifecycle to Notion's official `ntn` CLI rather than implementing a second HTTP/authentication stack.

## Requirements

- Python 3.12+
- Notion official `ntn` CLI
- On Windows, the npm installation route requires Node.js 22+ and npm 10+
- A Notion workspace account that can authenticate with `ntn login`

No paid automation service is required.

## Windows setup

From this directory in PowerShell:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\windows\Install_Notion_Native_File_Bridge.ps1 -Login
```

The installer:

1. verifies Node.js/npm versions;
2. installs official `ntn` with `npm install --global ntn` when needed;
3. installs this Python package for the current user;
4. optionally starts `ntn login`;
5. runs bridge preflight.

`ntn login` opens Notion authorization in the browser and stores the workspace credential through the official CLI's credential mechanism. The bridge never asks for or writes a token itself.

## Manual setup

Install the official Notion CLI:

```powershell
npm install --global ntn
ntn --version
ntn login
```

Install the bridge from the Base checkout:

```powershell
py -3.12 -m pip install --user .\tools\notion-native-file-bridge
notion-native-file-bridge preflight
```

Expected preflight shape:

```json
{"api_version":"2026-03-11","operation":"preflight","status":"PASS","ntn_version":"..."}
```

## Upload once

```powershell
notion-native-file-bridge upload --file "C:\path\COC-Fiction_Approved_Dark_Project_Hub_Android.jpg"
```

The JSON receipt includes:

- `upload_id`
- filename
- content type
- content length
- local SHA-256
- Notion upload status

Save `upload_id`; the same upload can be attached to multiple destinations after it has been made permanent by attachment.

## Append an image block

```powershell
notion-native-file-bridge append-image `
  --page-id "<NOTION_PAGE_ID>" `
  --upload-id "<FILE_UPLOAD_ID>"
```

This uses the official typed fields:

```text
children[0][type]=image
children[0][image][type]=file_upload
children[0][image][file_upload][id]=<FILE_UPLOAD_ID>
```

and independently reads back the created block.

## Set a page cover

```powershell
notion-native-file-bridge set-cover `
  --page-id "<NOTION_PAGE_ID>" `
  --upload-id "<FILE_UPLOAD_ID>"
```

## Set a Files property such as `Preview`

```powershell
notion-native-file-bridge set-files-property `
  --page-id "<DATABASE_PAGE_ID>" `
  --property "Preview" `
  --upload-id "<FILE_UPLOAD_ID>" `
  --filename "COC-Fiction_Approved_Dark_Project_Hub_Android.jpg"
```

Property names with spaces are safe because the bridge passes each CLI field as a separate subprocess argument.

## Evidence ceiling

A PASS receipt means the operation and its Notion API readback passed. It does **not** mean a mobile client displayed the image.

```text
upload/readback PASS
≠ destination readback PASS
≠ HUMAN_VISIBLE_PASS
```

For the COC-Fiction gate, final success requires opening the page in Android Notion and seeing the **actual dark COC project-hub pixels**, not a status callout, filename, empty card, or broken-image placeholder.

## Security

- Preferred auth: `ntn login`.
- Never commit a Notion access token.
- `NOTION_API_TOKEN` may be used by the official CLI for unattended work, but the bridge redacts its current exact value from captured subprocess errors.
- Do not use `ntn --unsafe-verbose` in shared logs or chat.
- The bridge accepts local file paths for upload; it is not a generic URL downloader.

## Failure codes

The CLI exits with code `2` and a JSON `BLOCKED` receipt for fail-closed errors such as:

- `NTN_UNAVAILABLE`
- `NTN_COMMAND_FAILED`
- `AUTH_READBACK_FAILED`
- `INVALID_NTN_JSON`
- `FILE_NOT_FOUND`
- `UNSUPPORTED_CONTENT_TYPE`
- `UPLOAD_ID_MISSING`
- `UPLOAD_READBACK_MISMATCH`
- `DESTINATION_READBACK_FAILED`

## Routing rule

```text
Notion text/structure/layout
→ Notion MCP

Binary file requiring typed file_upload
→ Notion Native File Bridge / official ntn

After write
→ Notion readback

If client rendering matters
→ actual Android/iOS/browser observation
```

If a future ChatGPT Notion connector exposes and verifies typed `file_upload` attachment directly, prefer that native connector path and retire this bridge rather than maintaining duplicate infrastructure.
