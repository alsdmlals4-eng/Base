# Tool Hub Managed Project Onboarding Design

## Status

`APPROVED_FOR_BUILD` — the user approved automatic clone for missing projects on 2026-08-14.

## Goal

Remove the need for a person to know or type a local Git folder. For each reviewed game project, Tool Hub finds the exact repository in bounded standard locations or clones the exact reviewed GitHub URL into the managed Windows project root, validates the existing project-owned identity, and registers it without altering tracked project content.

## User experience

The project picker shows one primary action per reviewed project:

- `연결됨`: select the already validated machine-local project.
- `PC에서 찾기`: check exact bounded candidate locations and match the Git remote.
- `자동 설치 및 연결`: clone an absent repository and register it.
- `조치 필요`: show a bounded public reason and preserve every existing file.

The current eight projects require no Git folder, GitHub URL, or Figma URL input. Their exact pointers are already reviewed in Base. For a future project, the user supplies its GitHub and Figma URLs to the project GPT once; a normal Base PR adds the reviewed pointer pair before Tool Hub can consume it. The browser never creates canonical identity or writes Base registries.

## Existing-solution disposition

| Candidate | Disposition | Reason |
| --- | --- | --- |
| Current Tool Hub project picker and `ProjectLocator` | `REFACTOR_AND_REUSE` | It already owns machine-local pointers and exact v2 identity validation. |
| Existing canonical `PROJECT_FIGMA_TARGET_REGISTRY.json` loader | `EXTEND` | It is already the single Hub project-name/routing catalog; adding an exact repository pointer avoids a third project catalog/parser. |
| Git CLI clone | `REUSE` | A clone is a connected local copy of the repository. GitHub Desktop uses the same clone concept but normally asks the person to choose a local path. <https://docs.github.com/en/desktop/adding-and-cloning-repositories/cloning-a-repository-from-github-to-github-desktop> |
| GitHub Desktop handoff | `FALLBACK_ONLY` | Useful for authentication or Git LFS remediation, but it does not remove the local-path decision from the primary flow. |
| Whole-disk recursive discovery | `REJECT` | Slow, privacy-invasive, and unnecessary when exact repository names and managed roots are known. |
| Browser-supplied arbitrary clone URL or destination | `REJECT` | It would reopen arbitrary network fetch and filesystem-write authority. |

## Canonical catalog extension

Extend every entry in `docs/operations/PROJECT_FIGMA_TARGET_REGISTRY.json` and its shared schema/loader with a required `repository_url`. The URL is an HTTPS GitHub repository pointer without credentials, query, fragment, or alternate host. The loader binds the exact tuple:

```text
project_id
+ display_name
+ repository_url
+ figma_file_key
+ figma_url
+ delivery_status
```

No separate project-onboarding registry is created. `repository_url` is public metadata, not a credential or execution command.

Reviewed initial mapping:

| project_id | repository_url |
| --- | --- |
| `coc-fiction` | `https://github.com/alsdmlals4-eng/Coc-Fiction.git` |
| `ten-paces-hidden-moves` | `https://github.com/alsdmlals4-eng/Ten-Paces-Hidden-Moves.git` |
| `ninja-survival` | `https://github.com/alsdmlals4-eng/ninja-survival-godot.git` |
| `switchy-express-cargo-puzzle` | `https://github.com/alsdmlals4-eng/Switchy-Express-Cargo-Puzzle.git` |
| `urban-legend` | `https://github.com/alsdmlals4-eng/urban-legend.git` |
| `grimoire-how-to-rewrite-the-world` | `https://github.com/alsdmlals4-eng/GRIMOIRE-.git` |
| `blacksmith` | `https://github.com/alsdmlals4-eng/Blacksmith.git` |
| `omenward` | `https://github.com/alsdmlals4-eng/omenward.git` |

These pointers were matched against the repositories currently accessible through the connected GitHub account. Repository availability at a later run is revalidated; the design does not treat this inventory observation as permanent availability.

## Managed roots and bounded discovery

The Windows default managed root is:

```text
%USERPROFILE%\Documents\GitHub
```

Tool Hub checks only:

1. the already registered exact root;
2. `<managed-root>/<exact-repository-name>`;
3. `<USERPROFILE>/source/repos/<exact-repository-name>`;
4. explicit additional roots stored in Tool Hub's machine-local configuration by a future approved UI, not browser-supplied request paths.

Each candidate must be a real directory reached without symlink/reparse traversal, an exact Git worktree root, and have an `origin` URL semantically equal to the reviewed `repository_url`. Discovery does not recursively enumerate the user profile or drives.

## Clone transaction

`POST /api/projects/{project_id}/onboard` accepts a catalog `project_id` only. It cannot accept a URL, command, branch, destination, environment, or Git option.

For an absent project:

1. Resolve the reviewed Git executable using the existing fixed Git policy.
2. Revalidate the canonical catalog immediately before starting.
3. Require the managed root to be a real, user-owned, non-reparse directory.
4. Require the final destination not to exist. Existing paths are never overwritten, merged, cleaned, reset, or deleted.
5. Create a random sibling staging directory owned by the current user.
6. Execute a fixed argv with `shell=False` and a minimal environment:

   ```text
   git clone --origin origin -- <reviewed-repository-url> <random-staging-path>
   ```

7. Verify the resulting origin URL and exact Git root.
8. Create only the ignored local `.asset-vault/library` directory when the committed `.gitignore` already makes `.asset-vault/` effectively ignored. Never edit `.gitignore` or any tracked project file.
9. Run the existing exact project identity validator against the selected `project_id` and current Base pin.
10. Atomically rename the validated staging directory to the final managed destination.
11. Revalidate the final root and store the existing machine-local locator record.

If any step fails, no locator record is written. A staging directory created by this transaction contains no pre-existing user data and may be removed after handles close; cleanup failure is quarantined with a bounded name and reported without exposing the absolute path through the public API.

Existing repositories are never automatically fetched, pulled, reset, cleaned, checked out, or migrated. If an existing checkout is stale or lacks the required v2 adapter, Tool Hub returns an actionable blocked state and offers GitHub Desktop as a manual fallback. It does not silently create project identity.

## Figma boundary

The reviewed `figma_url` is validated as the exact `https://www.figma.com/design/<figma_file_key>/...` pointer already required by the shared loader. It supports discovery and handoff only. Onboarding does not call Figma, verify live nodes, upload images, authorize mutation, or change `REGISTERED_NO_MUTATION`.

## Public states and errors

Public catalog rows add a bounded `local_state`:

- `REGISTERED`
- `FOUND_UNREGISTERED`
- `CLONE_AVAILABLE`
- `ONBOARDING`
- `PROJECT_SETUP_REQUIRED`
- `PATH_OCCUPIED`
- `AUTHENTICATION_REQUIRED`
- `CLONE_FAILED`
- `IDENTITY_MISMATCH`

Public responses never include absolute roots, raw Git output, command lines, environment variables, credentials, adapter contents, or staging names. Detailed local diagnostics are bounded and written only to `%LOCALAPPDATA%\BaseToolHub\logs`.

## Concurrency and recovery

- One transactional lock exists per `project_id`; duplicate clicks return the same in-progress state.
- The final destination uses exclusive publication; another process winning the path race causes `PATH_OCCUPIED` and validation of the winning path, not overwrite.
- Hub restart treats abandoned staging paths as quarantined. It never promotes them without repeating the full validation.
- Registration is idempotent for the same exact repository identity.

## Verification

- Schema and shared-loader tests for all eight exact project/repository/Figma tuples.
- TDD service/API tests for found, absent, successful clone, duplicate click, occupied path, wrong remote, wrong adapter ID, missing adapter, missing effective Asset Vault ignore, clone failure, and redacted errors.
- Symlink/reparse, path swap, executable/PATH substitution, malicious repository filename, Git config execution, credentials-in-URL, and staging publication adversarial tests.
- Real `windows-latest` smoke with paths containing spaces: discover one fixture and clone a second fixture, then register both independently.
- Live user-PC smoke with one existing public project and one absent public project after exact-head CI passes.

## Exclusions

- No automatic pull, commit, push, branch switch, migration, or tracked project edit.
- No arbitrary URL onboarding directly from the browser.
- No private-repository token collection. Existing Git Credential Manager/GitHub Desktop is fallback evidence only.
- No Figma mutation or live placement.
- No Windows Studio child enablement; `BLOCKED_PLATFORM` remains until its separate Job Object gate passes.

## Rollback

Revert the catalog `repository_url` extension and onboarding service/API/UI. Existing project locator records and manual-root registration remain readable. No tracked project repository bytes or Figma files are changed by rollback.
