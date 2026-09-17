# Aseprite Local CLI Bridge Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a safe, zero-dependency Aseprite CLI bridge that inspects and exports local candidate assets without arbitrary Lua, a background MCP server, or direct repository promotion.

**Architecture:** A Python standard-library command-line wrapper validates repository-relative paths and fixed command arguments before invoking the user's licensed Aseprite executable. It emits PNG/JSON candidate outputs and a redacted hash receipt under `.asset-vault/library/`, after which the existing Asset Vault sync/promotion workflow projects only approved local candidates toward Godot.

**Tech Stack:** Python 3.11+ standard library, `unittest`, Aseprite 1.3+ official CLI, JSON profiles.

**Spec:** `docs/superpowers/specs/2026-09-09-aseprite-local-cli-bridge-design.md`

## Global Constraints

- Baseline Base main SHA is `580a362db07b4b1a91a87300402969793784acff`.
- Additional paid services and separately metered API usage are forbidden.
- No arbitrary Lua or arbitrary CLI passthrough.
- No network listener or background server.
- Source and output targets must resolve inside the declared project roots.
- Default overwrite is forbidden; explicit overwrite remains candidate-root-only.
- Absolute local paths must not enter the shared receipt.
- Candidate export is not repository promotion, runtime proof, or user asset approval.
- Actual user-PC Aseprite and Godot runtime verification remain `NOT_RUN` in this Base-only change.

---

### Task 1: Lock the public path and command safety contract

**Files:**
- Create: `tests/test_aseprite_cli_bridge.py`
- Create: `tools/aseprite_cli_bridge.py`

**Interfaces:**
- Produces: `BridgeError`, `BridgeConfig`, `load_config(project_root, config_path)`, `resolve_source(config, source)`, `resolve_candidate_dir(config, asset_id)`, `validate_asset_id(asset_id)`.
- Consumes: Python `pathlib`, `json`, `dataclasses`, and `unittest` only.

- [x] **Step 1: Write failing tests for safe defaults and path containment**

Create tests that import `tools/aseprite_cli_bridge.py` by file path and assert:

```python
config = bridge.load_config(project_root, None)
self.assertEqual(config.candidate_output_root, (project_root / ".asset-vault/library/aseprite-generated").resolve())
self.assertFalse(config.allow_overwrite)
self.assertEqual(bridge.validate_asset_id("HERO_IDLE_01"), "HERO_IDLE_01")
with self.assertRaises(bridge.BridgeError):
    bridge.validate_asset_id("../hero")
with self.assertRaises(bridge.BridgeError):
    bridge.resolve_source(config, project_root.parent / "outside.aseprite")
```

Also assert a profile whose source or candidate root resolves outside `project_root` fails closed.

- [x] **Step 2: Run the focused tests and verify RED**

Run:

```bash
python -m unittest discover -s tests -p 'test_aseprite_cli_bridge.py' -v
```

Expected: import failure because `tools/aseprite_cli_bridge.py` does not exist.

- [x] **Step 3: Implement the minimal safe configuration and path functions**

Implement:

```python
@dataclass(frozen=True)
class BridgeConfig:
    project_root: Path
    source_roots: tuple[Path, ...]
    candidate_output_root: Path
    allowed_source_extensions: tuple[str, ...]
    allow_overwrite: bool
    timeout_seconds: int
    sheet_type: str
```

Normalize repository-relative paths, reject `..` and existing symlink components, then use `Path.resolve()` and `relative_to()` for containment. Reject unknown profile keys, unsupported extensions, adoption states outside the Base lifecycle vocabulary, non-positive timeout, and sheet types outside `rows`, `columns`, `horizontal`, `vertical`, and `packed`.

- [x] **Step 4: Run the focused tests and verify GREEN**

Run the same `unittest` command. Expected: all Task 1 tests PASS.

- [ ] **Step 5: Commit Task 1**

```bash
git add tests/test_aseprite_cli_bridge.py tools/aseprite_cli_bridge.py
git commit -m "feat: add safe Aseprite bridge path contract"
```

### Task 2: Add executable discovery and read-only inspection

**Files:**
- Modify: `tests/test_aseprite_cli_bridge.py`
- Modify: `tools/aseprite_cli_bridge.py`

**Interfaces:**
- Consumes: Task 1 `BridgeConfig` and `BridgeError`.
- Produces: `discover_aseprite(explicit, environment) -> ExecutableInfo`, `read_aseprite_version(info, timeout_seconds) -> str`, `inspect_source(config, executable, source) -> dict[str, object]`.

- [x] **Step 1: Write failing tests for discovery precedence and inspect command**

Create temporary executable files and assert explicit path wins over `ASEPRITE_PATH`; environment wins over `PATH`. Patch only `subprocess.run` to return a real `CompletedProcess` and assert the inspect argument list contains the fixed flags:

```python
("-b", "--list-layer-hierarchy", "--list-tags", "--list-slices", "--data=", source)
```

Assert parsed output includes only project-relative `source`, source SHA-256, version, and parsed Aseprite metadata.

- [x] **Step 2: Run the new tests and verify RED**

Expected: failures identify missing `discover_aseprite` and `inspect_source`.

- [x] **Step 3: Implement minimal discovery and inspection**

Discovery order:

1. `--aseprite` explicit path;
2. `ASEPRITE_PATH` environment variable;
3. `shutil.which("aseprite")` and `shutil.which("aseprite.exe")`;
4. deterministic common Windows/macOS/Linux locations.

Invoke Aseprite without `shell=True`, with `capture_output=True`, `text=True`, UTF-8 replacement, and configured timeout. Convert timeout and non-zero return code into `BridgeError`.

- [x] **Step 4: Run focused tests and verify GREEN**

Expected: all discovery and inspection tests PASS.

- [ ] **Step 5: Commit Task 2**

```bash
git add tests/test_aseprite_cli_bridge.py tools/aseprite_cli_bridge.py
git commit -m "feat: inspect Aseprite sources through fixed CLI commands"
```

### Task 3: Export candidates and verify receipts

**Files:**
- Modify: `tests/test_aseprite_cli_bridge.py`
- Modify: `tools/aseprite_cli_bridge.py`

**Interfaces:**
- Consumes: Task 1 path functions and Task 2 executable/version functions.
- Produces: `export_candidate(...) -> dict[str, object]`, `validate_candidate(config, asset_id) -> dict[str, object]`, `sha256_file(path) -> str`.

- [x] **Step 1: Write failing tests for no-overwrite, export, and drift detection**

The fake subprocess side effect must create:

```python
png_path.write_bytes(b"\x89PNG\r\n\x1a\n" + b"test")
json_path.write_text(json.dumps({"frames": [], "meta": {}}), encoding="utf-8")
```

Assert export:

- refuses an existing output unless `overwrite=True`;
- creates PNG, metadata JSON, and receipt in `<candidate_root>/<ASSET_ID>/`;
- records project-relative paths only;
- records source/output SHA-256 and Aseprite version;
- sends fixed `--sheet`, `--data`, `--format json-array`, and `--sheet-type` arguments;
- detects a changed PNG when `validate_candidate` is run later.

- [x] **Step 2: Run tests and verify RED**

Expected: missing export/validate functions.

- [x] **Step 3: Implement fixed export and receipt validation**

Build the command internally; do not accept arbitrary extra arguments. Keep the source before `--sheet`, because Aseprite exports sprites opened earlier in the command. Render into an owned staging directory, validate the PNG signature and JSON object shape, then publish the bundle. On overwrite, move the old bundle into the same staging area and restore it on publication failure. Store receipt paths relative to project root and timestamp in UTC ISO 8601.

- [x] **Step 4: Run focused tests and verify GREEN**

Expected: all Task 3 tests PASS.

- [ ] **Step 5: Commit Task 3**

```bash
git add tests/test_aseprite_cli_bridge.py tools/aseprite_cli_bridge.py
git commit -m "feat: export and verify Aseprite candidate receipts"
```

### Task 4: Add the operator CLI and beginner-facing guide

**Files:**
- Modify: `tests/test_aseprite_cli_bridge.py`
- Modify: `tools/aseprite_cli_bridge.py`
- Create: `templates/project-operations/ASEPRITE_LOCAL_BRIDGE_PROFILE.json`
- Create: `docs/knowledge/game-development/ASEPRITE_LOCAL_CLI_BRIDGE_GUIDE.md`

**Interfaces:**
- Consumes: all bridge functions from Tasks 1-3.
- Produces: command-line subcommands `doctor`, `inspect`, `export`, and `validate` with JSON stdout and non-zero failure status.

- [x] **Step 1: Write failing CLI tests**

Call `main([...])` with patched functions and captured stdout/stderr. Assert:

- `doctor` prints one JSON object and returns 0;
- bridge errors print `ASEPRITE_BRIDGE_ERROR: <message>` to stderr and return 2;
- no stack trace is printed in normal mode;
- `export --overwrite` is explicit and not inherited from the example profile.

- [x] **Step 2: Run tests and verify RED**

Expected: missing parser/main behavior.

- [x] **Step 3: Implement the CLI and documentation**

Use `argparse`. Every subcommand accepts `--project-root`, optional `--config`, and optional `--aseprite`. Add exact PowerShell blocks for:

1. discovering the executable through Steam or `ASEPRITE_PATH`;
2. copying the profile into a project-owned config;
3. running `doctor`, `inspect`, `export`, and `validate`;
4. checking Godot import and keeping candidate outputs untracked;
5. uninstalling/rolling back;
6. optional MCP phase-two evaluation, clearly marked not installed by this change.

Include official and candidate repository links, license/security cautions, expected outputs, and troubleshooting.

- [x] **Step 4: Run focused tests and verify GREEN**

Expected: all focused tests PASS with no warnings.

- [ ] **Step 5: Commit Task 4**

```bash
git add tests/test_aseprite_cli_bridge.py tools/aseprite_cli_bridge.py templates/project-operations/ASEPRITE_LOCAL_BRIDGE_PROFILE.json docs/knowledge/game-development/ASEPRITE_LOCAL_CLI_BRIDGE_GUIDE.md
git commit -m "docs: add Aseprite bridge setup and operator workflow"
```

### Task 5: Validate the Base candidate and close review gates

**Files:**
- Create: `docs/superpowers/specs/2026-09-09-aseprite-local-cli-bridge-design.md`
- Create: `docs/superpowers/plans/2026-09-09-aseprite-local-cli-bridge.md`
- Review: every file changed by Tasks 1-4

**Interfaces:**
- Consumes: the complete candidate branch and trusted main SHA.
- Produces: focused test evidence, Base validation evidence, two adversarial review receipts, PR exact-head evidence, and an explicit runtime evidence ceiling.

- [x] **Step 1: Run syntax and focused tests**

```bash
python -m py_compile tools/aseprite_cli_bridge.py
python -m unittest discover -s tests -p 'test_aseprite_cli_bridge.py' -v
```

Expected: PASS.

- [ ] **Step 2: Run Base local validation — `NOT_RUN` because this session has no complete Base checkout**

```bash
python tools/run_local_validation.py --trusted-history-commit 580a362db07b4b1a91a87300402969793784acff
```

Expected: PASS. Missing local dependencies or unavailable repository checkout must be reported as `NOT_RUN`, not PASS; exact-head GitHub Actions then becomes required evidence.

- [x] **Step 3: Run whole-scope adversarial review loop 1**

Attack path escapes, symlinks, overwrite behavior, command injection, secret/path leakage, cleanup ownership, Aseprite CLI argument correctness, candidate-vs-approved state confusion, and Godot authority overlap. Add a failing regression test for every valid implementation finding before correcting it.

- [x] **Step 4: Run whole-scope adversarial review loop 2**

Re-read the complete candidate after loop 1. Attack installation instructions, beginner error recovery, exact-version claims, licensing, rollback, Base discovery, and evidence overclaim. Correct only with focused regression coverage where behavior changes.

- [ ] **Step 5: Open an isolated PR and inspect exact-head checks**

Create a branch from current completed main, upload the complete candidate, open a PR, and verify changed files, exact head, checks, and unresolved review threads. Do not modify unrelated open/draft/ready PRs.

- [x] **Step 6: Record the evidence ceiling**

State explicitly:

```text
DOCUMENT/STATIC/FOCUSED_TEST: PASS when evidenced
BASE CI: PASS only on exact PR head
REAL ASEPRITE WINDOWS CANARY: NOT_RUN
GODOT IMPORT/RUNTIME: NOT_RUN
USER ASSET APPROVAL: NOT_RUN
PROJECT ADOPTION: NOT_RUN
```
