# Aseprite Local CLI Bridge Design

```yaml
status: APPROVED_CONTRACT_CONTINUATION
approval_reference: "Current conversation: user approved the recommended Aseprite integration and requested execution plus detailed methods and links."
baseline_repository: alsdmlals4-eng/Base
baseline_main_sha: 580a362db07b4b1a91a87300402969793784acff
work_mode: BUILD
scope: BASE_SHARED_CANDIDATE_TOOLING_ONLY
project_rollout: NOT_INCLUDED
aseprite_runtime_canary: NOT_RUN
```

## 1. Goal

Add a zero-incremental-cost, repository-owned bridge that lets Codex or a local operator inspect and export licensed Aseprite source files through Aseprite's official command-line interface without installing a long-running MCP server, enabling arbitrary Lua, or writing directly to approved runtime asset paths.

## 2. Current state and gap

Base already treats Aseprite as an official pixel-art production reference and already owns the local candidate flow through `.asset-vault/library/` and `assets/_vault_local/`. It does not currently own an executable Aseprite boundary that:

- discovers a user-supplied licensed Aseprite executable;
- constrains readable source files to project-declared roots;
- constrains generated files to one local candidate root;
- refuses replacement unless the operator explicitly requests it;
- exports a sprite sheet and Aseprite JSON metadata;
- writes a reproducibility receipt without leaking absolute local paths;
- verifies output integrity before claiming tool success.

The bridge fills only that gap. It does not become a second Godot authoring authority and does not promote candidate assets into tracked product paths.

## 3. Benchmark preflight and disposition

| Approach | Observed pattern | Fit | Disposition |
|---|---|---|---|
| Full live-editor MCP (`giangdvdotdev/aseprite-mcp`, `bachhoang0606/aseprite-mcp`) | Python/Rust server plus Aseprite Lua extension; rich live editor mutation over localhost WebSocket | Strong visual feedback, but adds a daemon/plugin pair, local control surface, port lifecycle, and broader mutation authority before a Base project has proved repeated need | `ABSORB` fail-loud preflight and visual readback patterns; live adoption remains `DEFERRED` |
| Minimal raw-Lua MCP (`mattt/aseprite-mcp`) | Small stdio server with workspace confinement, but arbitrary Lua retains full Aseprite and filesystem access | Low tool count, but the unrestricted scripting escape hatch exceeds the default Base permission boundary | `ABSORB` workspace-confinement patterns; default adoption is `REJECTED` |
| Bounded official CLI wrapper | One local Python process shells out to the user's licensed Aseprite CLI for declared inspect/export operations | No server, port, plugin, Go/Rust runtime, or third-party Python package; deterministic and easy to remove | `BUILD_NEW`; selected as the minimum scope because existing candidates cannot meet the restricted write/command surface without material modification |

### ADOPT

- Aseprite official CLI as the executable boundary.
- Aseprite's own `--batch`, `--sheet`, `--data`, `--format json-array`, `--list-layer-hierarchy`, `--list-tags`, and `--list-slices` operations.
- The existing Base local Asset Vault candidate and explicit promotion boundaries.
- Workspace confinement, machine-readable receipts, fail-loud diagnostics, exact version capture, and explicit timeout.

### ADAPT

- Community MCP visual-feedback loops become a later optional live trial after the bounded bridge proves value.
- Environment discovery accepts `--aseprite`, then `ASEPRITE_PATH`, then `PATH`, then common install locations.
- Overwrite is not a default capability; it is an explicit reversible operation limited to the candidate root.

### REJECT AS DEFAULT

- arbitrary Lua execution;
- arbitrary CLI argument passthrough;
- unauthenticated or remotely reachable sockets;
- a background server that remains running after the task;
- output outside the declared local candidate root;
- automatic overwrite;
- automatic repository promotion;
- direct mutation of Godot scenes, resources, or project settings;
- recording personal absolute paths in shared receipts.

## 4. Architecture

```text
Codex/local operator
  -> Python stdlib CLI: tools/aseprite_cli_bridge.py
     -> profile: templates/project-operations/ASEPRITE_LOCAL_BRIDGE_PROFILE.json
     -> licensed local Aseprite executable
        -> inspect metadata on allowed source
        -> export PNG sprite sheet + JSON metadata
     -> local Asset Vault authority only
        -> .asset-vault/library/aseprite-generated/<ASSET_ID>/<ASSET_ID>.png
        -> .asset-vault/library/aseprite-generated/<ASSET_ID>/<ASSET_ID>.json
        -> .asset-vault/library/aseprite-generated/<ASSET_ID>/<ASSET_ID>.receipt.json
  -> existing project_asset_vault.py sync
     -> assets/_vault_local/aseprite-generated/<ASSET_ID>/<ASSET_ID>.png
  -> Godot candidate import and human/runtime review
  -> existing Asset Vault `promote` remains the only tracked-asset promotion boundary
```

The bridge is stateless between invocations. The receipt is evidence about one invocation, not a catalog, approval record, or runtime proof.

## 5. Command contract

### `doctor`

- Inputs: project root, optional profile, optional explicit Aseprite path.
- Resolves the executable in this order: explicit CLI path, `ASEPRITE_PATH`, `PATH`, common OS locations.
- Runs `Aseprite --version` with a bounded timeout.
- Returns machine-readable JSON with executable source and version.
- Does not write project files.

### `inspect`

- Requires an existing `.aseprite` or `.ase` source inside an allowed source root.
- Runs Aseprite in batch mode with list flags and `--data=` so metadata is returned through stdout.
- Returns the source's project-relative path, SHA-256, Aseprite version, and parsed metadata.
- Does not write project files.

### `export`

- Requires a strict asset ID matching `[A-Z0-9][A-Z0-9_-]{0,63}`.
- Resolves the output directory as `<candidate_output_root>/<ASSET_ID>/`.
- Refuses any existing output by default.
- Executes only the fixed sprite-sheet/JSON command assembled by the bridge.
- Validates the PNG signature and required JSON shape before writing the receipt.
- The optional `--overwrite` remains confined to the candidate root and is never implied by the profile.

### `validate`

- Re-reads PNG, metadata JSON, and receipt.
- Confirms paths are still within the candidate root.
- Confirms recorded and actual SHA-256 hashes match.
- Confirms the metadata contains `frames` and `meta` objects.
- Returns machine-readable status and fails non-zero on drift.

## 6. Profile contract

The committed profile is a copyable example, not a project adoption claim. It contains only repository-relative paths and safe defaults:

```json
{
  "schema_version": 1,
  "adoption_state": "CANDIDATE",
  "source_roots": [".asset-vault/library", "assets/source/aseprite"],
  "candidate_output_root": ".asset-vault/library/aseprite-generated",
  "allowed_source_extensions": [".aseprite", ".ase"],
  "allow_overwrite": false,
  "timeout_seconds": 60,
  "sheet_type": "rows"
}
```

A project copies this to a project-owned path only after fresh-reading its `AGENTS.md`, asset roots, `.gitignore`, Godot version, and actual consumer. An absolute Aseprite executable path belongs in the local `ASEPRITE_PATH` environment variable, not in the repository profile.

## 7. Safety and error handling

- All project-relative paths are resolved and checked with `Path.resolve()` and `Path.relative_to()`.
- Configured roots and source/candidate paths reject existing symlink components before containment checks, including symlinks that point back inside an allowed root.
- Existing final PNG, JSON, or receipt paths that are symlinks or Windows junctions are rejected even when explicit overwrite is enabled.
- Source and output roots must remain below the project root.
- The bridge never invokes a shell; `subprocess.run()` receives an argument list.
- Standard output and standard error are bounded in time; command failure returns a concise error with no secret/environment dump.
- Receipt paths are repository-relative and use forward slashes.
- A failed export removes only files created by the current attempt; it does not delete pre-existing files.
- No background process is created.

## 8. Testing strategy

Automated tests use a temporary fake Aseprite executable so the suite runs without a licensed Aseprite installation. Tests cover:

- executable precedence and version readback;
- rejection of source and output path escapes;
- strict asset ID validation;
- no-overwrite default;
- deterministic command construction;
- PNG/JSON/receipt generation;
- receipt path redaction and SHA-256 verification;
- drift detection;
- non-zero CLI failure behavior.

The focused test suite proves wrapper behavior only. It does not prove compatibility with an installed Aseprite build, visual quality, Godot import, in-game animation, or human approval.

## 9. Rollout and evidence ceiling

### Base candidate completion

- design, plan, guide, profile, bridge, and focused tests committed on one isolated branch;
- focused tests pass;
- Base CI passes on the exact PR head;
- exactly two whole-scope adversarial review loops close with no blocking finding.

### Project adoption gate

A project remains `CANDIDATE` or `DEFERRED`, not `ADOPTED_ACTIVE`, until a Windows canary records:

1. exact project and exact Base/project revision;
2. licensed Aseprite executable path resolved locally;
3. `doctor`, `inspect`, `export`, and `validate` PASS;
4. PNG and JSON imported/consumed by the actual Godot project path;
5. Godot runtime capture for the intended animation or sprite state;
6. no tracked source delta during candidate-only trial;
7. explicit user approval before promotion.

### Evidence ceiling

This Base change can prove a restricted wrapper and reproducible documentation. It cannot claim `ASEPRITE_CONNECTED_ON_USER_PC`, `PROJECT_ADOPTED`, `GODOT_RUNTIME_VERIFIED`, `USER_APPROVED_ASSET`, or `RELEASE_READY` without the project-local canary.

## 10. Rollback

Revert the Base commit or remove the new bridge, guide, profile, tests, design, and plan. Project files and local Aseprite installations remain untouched because this scope performs no project rollout or global client configuration.
