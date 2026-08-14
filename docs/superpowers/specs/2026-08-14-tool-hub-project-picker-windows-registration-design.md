# Tool Hub Project Picker and Windows Registration Design

## Status

`APPROVED_FOR_BUILD` — the user approved a human-readable project list and continuation of the next Windows Tool Hub task on 2026-08-14.

## Goal

Make the localhost Tool Hub easier to use by listing the eight reviewed game projects by name, while enabling those projects to be registered from a real Windows PC without weakening project identity checks or implying that child Studio execution is already supported.

## Scope

- Show two separate project surfaces:
  - `등록 가능한 프로젝트`: the eight canonical entries from Base's committed Figma routing registry.
  - `내 프로젝트`: machine-local projects whose Git roots already passed identity validation.
- Selecting a known project fills a required expected `project_id`; the user supplies its local Git root once.
- The registration API compares the selected `project_id` with the committed v2 `skills/PROJECT_BASE_ADAPTER.json`. A mismatch is rejected and never stored.
- The public catalog exposes display name, project ID, registration state, and routing state only. It never exposes local absolute paths or Figma credentials.
- Add a Windows portable identity-validation path for project registration. It validates a real Git worktree root, committed v2 adapter, project ID, canonical Base pin, protected baseline, and gitignored Asset Vault. It rejects reparse-point path components and rechecks the selected root and adapter after validation.
- Keep all child tools `BLOCKED_PLATFORM` on Windows. Job Object ownership, Windows-safe Studio staging, and four-child smoke are the next independent build gate.

## Authority and data flow

`PROJECT_FIGMA_TARGET_REGISTRY.json` remains the single project-name/routing catalog. It is only a discovery source; it does not authorize a local root or Figma mutation.

```text
Base committed routing registry
  -> public known-project name/id list
  -> user selects expected project + local root
  -> server validates Windows/POSIX project identity
  -> exact adapter project_id match
  -> machine-local locator stores root + fingerprint
  -> public "내 프로젝트" list exposes no path
```

The machine-local locator remains a pointer, not project identity authority. Every resolve revalidates the project.

## Windows validation boundary

The portable Windows validator uses reviewed Git and Base files only, disables Git hooks/fsmonitor/filter execution, rejects symlink/reparse components, bounds file reads, and compares semantic JSON with committed blobs so clean CRLF checkouts are accepted. It rechecks file identity and bytes after the canonical operating-contract check.

The same Windows account and device administrator remain trusted, matching the existing `HARDENED_RUNTIME_DEFERRED` boundary. The Tool Hub must state that Base/Studio/project contract files must not be edited during validation or execution. This design does not claim protection against a malicious process running under the same Windows account.

Microsoft's documented primitives guide the later child-runtime phase: `FILE_FLAG_OPEN_REPARSE_POINT` prevents normal reparse traversal, and Job Objects with `JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE` own descendant termination. Those runtime primitives are not claimed complete in this registration phase.

## UI behavior

- A labeled select contains the eight canonical display names and project IDs.
- A separate local-root input is required only for registration.
- Registration feedback distinguishes invalid path, project-ID mismatch, unsupported identity runtime, and successful registration using bounded public reason codes.
- Registered project buttons remain the only active project selection authority for tool cards.
- On Windows, successful project registration changes cards from `PROJECT_SELECTION_REQUIRED` to `BLOCKED_PLATFORM`; it does not enable `시작 및 열기`.

## Error handling

- Unknown catalog ID: `PROJECT_CATALOG_ENTRY_REQUIRED`.
- Selected ID and adapter mismatch: `PROJECT_IDENTITY_MISMATCH`.
- Windows reparse/link, non-root Git directory, changed snapshot, dirty/uncommitted adapter, invalid Base pin, or missing ignored vault: existing bounded identity reason code.
- No absolute path, raw Git stderr, token, or local configuration contents enter public API responses.

## Verification

- TDD contract tests for the known-project catalog and expected-ID registration.
- POSIX regression suite for existing project identity.
- Windows-specific unit tests for CRLF, ID mismatch, reparse rejection, non-root rejection, adapter drift, and path redaction.
- Real `windows-latest` smoke: start Hub, register two fixture projects whose paths include spaces, verify both appear separately, verify all child tools remain `BLOCKED_PLATFORM`, then terminate Hub.
- `node --check`, package suites, Base contract tests, `git diff --check`, adversarial review, and exact-head PR checks.

## Excluded and next gate

- Windows Job Object child launch and Studio staging.
- Paid provider calls or OpenAI API generation.
- Figma mutation or live node placement.
- Actual game image/UX quality judgment.
- Android.

After this phase, the next build is Windows Job Object supervision plus Windows-safe Studio staging and a two-project/four-child smoke. Only that evidence can change Windows tools from `BLOCKED_PLATFORM` to `RUNNABLE`.

## Rollback

Remove the known-project API/UI projection and the Windows portable registration path. Existing machine-local project configuration schema and POSIX behavior remain compatible; no project repository or Figma file is mutated by this feature.
