# Base C1 Godot Multi-Project Pilot Evidence Integration Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Re-verify and preserve the exact Program A outcomes from five real Godot projects plus GRIMOIRE preproject readiness, update Base production-adapter readiness truthfully, and decide only whether Program B design work may begin.

**Architecture:** C1 never trusts PR prose or expiring Actions artifacts alone. A dedicated import tool downloads each exact workflow artifact, verifies repository/commit/Base-C0 identity and every physical evidence hash through the C0 verifier, writes one bounded canonical project evidence JSON per repository, and builds a closed aggregate index plus Markdown summary. Tests enforce complete project coverage, result-state consistency, and continued `NOT_READY` status.

**Tech Stack:** Python 3.12, JSON Schema Draft 2020-12, GitHub CLI/API, SHA-256, Base C0 evidence verifier, pytest, Base required GitHub Actions.

## Global Constraints

- Governing design: `docs/superpowers/specs/2026-08-05-godot-multi-project-production-adapter-expansion-design.md`.
- C1 starts only after Base C0 and all six project PRs are either merged with approved outcomes or explicitly recorded as blocked/not applicable.
- All real-project descriptors must pin the same exact Base C0 merge SHA unless a separately approved compatibility migration exists.
- Accepted project result states are exactly `PASS`, `BLOCKED_PREEXISTING`, `NOT_APPLICABLE`, `NOT_RUN`, and `FAIL`.
- Five real Godot projects are required in the index:
  - `alsdmlals4-eng/Switchy-Express-Cargo-Puzzle`
  - `alsdmlals4-eng/Ten-Paces-Hidden-Moves`
  - `alsdmlals4-eng/Blacksmith`
  - `alsdmlals4-eng/omenward`
  - `alsdmlals4-eng/urban-legend`
- `alsdmlals4-eng/GRIMOIRE-` must be `NOT_APPLICABLE` with `project_state: NOT_CREATED`; runtime PASS is forbidden.
- External artifact identity is bound to exact repository, merged commit SHA, workflow run ID, artifact ID, artifact archive SHA-256, and final evidence JSON SHA-256.
- Imported canonical files are bounded final evidence only. Full logs, Godot binaries, archives, project copies, scratch directories, and product files are not committed.
- C1 does not modify any project repository or Google Sheet.
- C1 does not implement Program B transport or Program C debugger.
- Even when all real-project Pilots pass, `production_adapter_ready` remains `NOT_READY` because authenticated transport, runtime debugger, Windows production operation, physical input, and human usability remain open.
- `program_b_design_gate: OPEN` permits brainstorming/design only, not implementation.

---

## File Responsibility Map

### Schemas and tools

- Create: `schemas/godot-multi-project-pilot-evidence-index-v1.schema.json`
  - Closed aggregate index contract.
- Create: `tools/import_godot_project_pilot_evidence.py`
  - Downloads one exact artifact, verifies metadata/bytes through Base C0, and emits one bounded canonical project JSON.
- Create: `tools/verify_godot_multi_project_pilot_index.py`
  - Validates complete coverage, shared Base C0 pin, status semantics, canonical file hashes, and readiness conclusions.

### Canonical evidence

- Create: `docs/knowledge/godot/evidence/multi-project-pilot/INDEX.json`
- Create: `docs/knowledge/godot/evidence/multi-project-pilot/README.md`
- Create one JSON each:
  - `switchy-express-cargo-puzzle.json`
  - `ten-paces-hidden-moves.json`
  - `blacksmith.json`
  - `omenward.json`
  - `urban-legend.json`
  - `grimoire-readiness.json`

### Readiness and tests

- Modify: `docs/knowledge/godot/GODOT_PRODUCTION_ADAPTER_READINESS.md`
- Create: `tests/test_godot_multi_project_pilot_integration.py`
- Create: `tests/test_godot_multi_project_pilot_integration_adversarial.py`
- Modify: `tests/test_local_validation.py`
- Modify: `tests/test_v9_machine_contracts.py`
- Modify: `.github/reference-freshness.json` only when current coupled-change policy requires it.

---

### Task 1: Freeze the exact Program A evidence ledger

**Files:**
- No repository writes yet.

**Interfaces:**
- Consumes: merged Base C0 and six project PRs.
- Produces: `program-a-evidence-input.json` in a temporary working directory containing exact immutable identifiers.

- [ ] **Step 1: Read current Base C0 and project merged SHAs**

For each repository, fetch the merged adoption/readiness PR rather than assuming current `main` is still the adoption commit. Record:

```json
{
  "repository": "owner/repo",
  "pr_number": 0,
  "merged_commit_sha": "40-hex",
  "base_c0_sha": "40-hex",
  "workflow_run_id": 0,
  "artifact_id": 0,
  "expected_result": "PASS"
}
```

GRIMOIRE uses `workflow_run_id` for the static readiness workflow and `artifact_id: null`.

- [ ] **Step 2: Verify PR changed-file scope**

Use GitHub API to list every merged PR file. Real-project PRs must contain only their four adoption files. GRIMOIRE must contain only its four readiness files. A scope violation blocks C1 until resolved or explicitly classified `FAIL`.

- [ ] **Step 3: Verify a shared Base C0 SHA**

All five real-project descriptor blobs and workflow pins must contain the same exact Base C0 SHA. GRIMOIRE must pin that same Schema/loader SHA. A mismatch is `BASE_C0_COHORT_MISMATCH` and blocks aggregate PASS.

- [ ] **Step 4: Write the temporary input ledger**

Do not commit tokens or API URLs containing credentials. Store only public repository names, numeric IDs, exact SHAs, expected artifact names, and expected status.

---

### Task 2: Add the closed aggregate evidence Schema test-first

**Files:**
- Create: `schemas/godot-multi-project-pilot-evidence-index-v1.schema.json`
- Create: `tests/test_godot_multi_project_pilot_integration.py`

**Interfaces:**
- Consumes: canonical project evidence files.
- Produces: a closed aggregate index accepted by `verify_index()`.

- [ ] **Step 1: Write Schema RED tests**

```python
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas/godot-multi-project-pilot-evidence-index-v1.schema.json"
INDEX = ROOT / "docs/knowledge/godot/evidence/multi-project-pilot/INDEX.json"


def test_multi_project_index_schema_is_closed_and_complete() -> None:
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    assert schema["additionalProperties"] is False
    assert schema["properties"]["program_state"]["enum"] == [
        "PASS",
        "BLOCKED",
        "FAIL",
    ]
    assert schema["properties"]["production_adapter_ready"]["const"] == "NOT_READY"
```

- [ ] **Step 2: Verify RED**

```bash
python -m pytest tests/test_godot_multi_project_pilot_integration.py -q
```

Expected: missing Schema and index failures.

- [ ] **Step 3: Create the exact Schema**

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://github.com/alsdmlals4-eng/Base/schemas/godot-multi-project-pilot-evidence-index-v1.schema.json",
  "title": "Godot Multi-Project Pilot Evidence Index v1",
  "type": "object",
  "additionalProperties": false,
  "required": [
    "schema_version",
    "design_id",
    "base_c0_sha",
    "generated_at",
    "program_state",
    "program_b_design_gate",
    "production_adapter_ready",
    "projects"
  ],
  "properties": {
    "schema_version": {"const": "1"},
    "design_id": {"const": "BASE-GODOT-ADOPT-20260805-MULTIPROJECT-PILOT-01"},
    "base_c0_sha": {"type": "string", "pattern": "^[0-9a-f]{40}$"},
    "generated_at": {"type": "string", "format": "date-time"},
    "program_state": {"enum": ["PASS", "BLOCKED", "FAIL"]},
    "program_b_design_gate": {"enum": ["OPEN", "BLOCKED"]},
    "production_adapter_ready": {"const": "NOT_READY"},
    "projects": {
      "type": "array",
      "minItems": 6,
      "maxItems": 6,
      "items": {"$ref": "#/$defs/projectEvidence"}
    }
  },
  "$defs": {
    "projectEvidence": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "repository",
        "project_id",
        "project_state",
        "result",
        "merged_commit_sha",
        "workflow_run_id",
        "artifact_id",
        "canonical_path",
        "canonical_sha256"
      ],
      "properties": {
        "repository": {"type": "string", "pattern": "^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$"},
        "project_id": {"type": "string", "pattern": "^[a-z0-9][a-z0-9-]{2,63}$"},
        "project_state": {"enum": ["EXISTING_GODOT_PROJECT", "NOT_CREATED"]},
        "result": {"enum": ["PASS", "BLOCKED_PREEXISTING", "NOT_APPLICABLE", "NOT_RUN", "FAIL"]},
        "merged_commit_sha": {"type": "string", "pattern": "^[0-9a-f]{40}$"},
        "workflow_run_id": {"type": "integer", "minimum": 1},
        "artifact_id": {"type": ["integer", "null"], "minimum": 1},
        "canonical_path": {"type": "string", "pattern": "^[a-z0-9-]+\\.json$"},
        "canonical_sha256": {"type": "string", "pattern": "^[0-9a-f]{64}$"}
      }
    }
  }
}
```

- [ ] **Step 4: Commit the Schema and RED test**

```bash
git add schemas/godot-multi-project-pilot-evidence-index-v1.schema.json tests/test_godot_multi_project_pilot_integration.py
git commit -m "test: define Godot multi-project evidence index"
```

---

### Task 3: Implement one-project artifact import and physical verification

**Files:**
- Create: `tools/import_godot_project_pilot_evidence.py`
- Test: `tests/test_godot_multi_project_pilot_integration.py`
- Test: `tests/test_godot_multi_project_pilot_integration_adversarial.py`

**Interfaces:**
- `import_artifact(input_record: InputRecord, download_dir: Path, output_path: Path) -> ImportedEvidence`
- `InputRecord.repository: str`
- `InputRecord.merged_commit_sha: str`
- `InputRecord.workflow_run_id: int`
- `InputRecord.artifact_id: int`
- `ImportedEvidence.canonical_sha256: str`

- [ ] **Step 1: Write import RED tests with a local ZIP fixture**

```python

def test_import_recomputes_archive_and_final_evidence_hashes(tmp_path: Path) -> None:
    archive = build_valid_artifact_zip(tmp_path)
    evidence = import_local_artifact(valid_input_record(), archive, tmp_path / "project.json")
    assert evidence.repository == "alsdmlals4-eng/example"
    assert evidence.archive_sha256 == sha256_file(archive)
    assert evidence.final_evidence_sha256 == sha256_file(extracted_final_evidence(tmp_path))


def test_import_rejects_repository_or_commit_mismatch(tmp_path: Path) -> None:
    archive = build_valid_artifact_zip(tmp_path, repository="alsdmlals4-eng/wrong")
    with pytest.raises(ValueError, match="EVIDENCE_IDENTITY_MISMATCH"):
        import_local_artifact(valid_input_record(), archive, tmp_path / "project.json")
```

- [ ] **Step 2: Verify RED**

```bash
python -m pytest tests/test_godot_multi_project_pilot_integration.py -k import -q
python -m pytest tests/test_godot_multi_project_pilot_integration_adversarial.py -k import -q
```

- [ ] **Step 3: Implement bounded ZIP extraction**

Reject:

```text
absolute member paths
.. traversal
symlink members
more than 64 files
archive larger than 20 MiB
uncompressed total larger than 50 MiB
single file larger than 10 MiB
duplicate member names
unexpected executable files
```

Extract only to a new temporary directory. Hash the archive before extraction.

- [ ] **Step 4: Reuse the Base C0 verifier**

Import `verify_runtime_evidence` and validate the final evidence plus every referenced physical file. Then compare:

```text
repository
source_commit == merged project commit
base_pilot_commit == expected Base C0
workflow run/artifact IDs from input ledger
project result and project_state
```

- [ ] **Step 5: Emit bounded canonical JSON**

The canonical JSON includes identifiers, final states, archive/final-evidence/saved-scene hashes, source-before/source-after hashes, selected engine version, and limitations. It excludes raw logs, absolute local paths, temporary directories, access tokens, and environment variables.

- [ ] **Step 6: Run tests and commit**

```bash
python -m pytest tests/test_godot_multi_project_pilot_integration.py -k import -q
python -m pytest tests/test_godot_multi_project_pilot_integration_adversarial.py -k import -q
git add tools/import_godot_project_pilot_evidence.py tests/test_godot_multi_project_pilot_integration.py tests/test_godot_multi_project_pilot_integration_adversarial.py
git commit -m "feat: import verified Godot project Pilot evidence"
```

---

### Task 4: Import the five real-project artifacts and GRIMOIRE readiness

**Files:**
- Create six canonical JSON files under `docs/knowledge/godot/evidence/multi-project-pilot/`.

**Interfaces:**
- Consumes: temporary Program A evidence ledger.
- Produces: six deterministic bounded canonical files.

- [ ] **Step 1: Download exact artifacts**

For each real project:

```bash
gh api "repos/OWNER/REPO/actions/artifacts/ARTIFACT_ID/zip" > project-artifact.zip
```

Use authenticated redirect handling from `gh`; verify artifact metadata first belongs to the recorded workflow run and is not expired.

- [ ] **Step 2: Run the importer**

```bash
python tools/import_godot_project_pilot_evidence.py \
  --input-record /tmp/program-a-evidence-input.json \
  --project-id switchy-express-cargo-puzzle \
  --artifact project-artifact.zip \
  --output docs/knowledge/godot/evidence/multi-project-pilot/switchy-express-cargo-puzzle.json
```

Repeat for Ten Paces, Blacksmith, OMENWARD, and urban-legend.

- [ ] **Step 3: Create GRIMOIRE readiness evidence from merged source**

Read the merged descriptor, readiness workflow run, changed-file list, and test result. Emit:

```json
{
  "schema_version": "1",
  "repository": "alsdmlals4-eng/GRIMOIRE-",
  "project_id": "grimoire",
  "project_state": "NOT_CREATED",
  "result": "NOT_APPLICABLE",
  "runtime_pilot": "NOT_APPLICABLE",
  "adapter_installation": "FORBIDDEN_UNTIL_PRODUCT_PROJECT_APPROVAL",
  "base_pilot_commit": "40-hex",
  "merged_commit_sha": "40-hex",
  "workflow_run_id": 1,
  "artifact_id": null,
  "source_scope_verified": true,
  "production_adapter_ready": "NOT_READY"
}
```

- [ ] **Step 4: Re-read and hash all six files**

Use canonical JSON serialization for aggregate hashes. Do not manually copy hash strings from PR comments.

- [ ] **Step 5: Commit imported evidence separately**

```bash
git add docs/knowledge/godot/evidence/multi-project-pilot/*.json
git commit -m "docs: preserve verified Godot project Pilot evidence"
```

---

### Task 5: Implement aggregate index validation

**Files:**
- Create: `tools/verify_godot_multi_project_pilot_index.py`
- Create: `docs/knowledge/godot/evidence/multi-project-pilot/INDEX.json`
- Test: `tests/test_godot_multi_project_pilot_integration.py`
- Test: `tests/test_godot_multi_project_pilot_integration_adversarial.py`

**Interfaces:**
- `verify_index(index_path: Path, evidence_root: Path) -> tuple[str, ...]`
- CLI exits `0` on valid index and `1` with stable error codes otherwise.

- [ ] **Step 1: Write index RED tests**

```python
REQUIRED_REPOSITORIES = {
    "alsdmlals4-eng/Switchy-Express-Cargo-Puzzle",
    "alsdmlals4-eng/Ten-Paces-Hidden-Moves",
    "alsdmlals4-eng/Blacksmith",
    "alsdmlals4-eng/omenward",
    "alsdmlals4-eng/urban-legend",
    "alsdmlals4-eng/GRIMOIRE-",
}


def test_index_covers_exact_program_a_repositories() -> None:
    document = json.loads(INDEX.read_text(encoding="utf-8"))
    assert {item["repository"] for item in document["projects"]} == REQUIRED_REPOSITORIES
    assert document["production_adapter_ready"] == "NOT_READY"
```

Adversarial tests remove a project, duplicate a repository, alter a canonical file after hashing, set GRIMOIRE to PASS, mix Base C0 SHAs, or set `program_b_design_gate: OPEN` while a project is `FAIL`.

- [ ] **Step 2: Verify RED**

```bash
python -m pytest tests/test_godot_multi_project_pilot_integration.py -k index -q
python -m pytest tests/test_godot_multi_project_pilot_integration_adversarial.py -k index -q
```

- [ ] **Step 3: Implement semantic rules**

```text
exact six unique repositories
exact one shared Base C0 SHA
canonical path basename only and within evidence root
canonical file SHA-256 matches physical bytes
GRIMOIRE result NOT_APPLICABLE and project_state NOT_CREATED
real project PASS requires all required runtime fields PASS and source unchanged
BLOCKED_PREEXISTING requires bounded blocker evidence and no product mutation
program_state PASS only when all five real projects PASS and GRIMOIRE NOT_APPLICABLE
program_state BLOCKED when no FAIL exists but at least one real project is BLOCKED_PREEXISTING or NOT_RUN
program_state FAIL when any project FAILs or identity/hash validation fails
program_b_design_gate OPEN only when program_state PASS
production_adapter_ready always NOT_READY
```

- [ ] **Step 4: Generate `INDEX.json` deterministically**

Sort projects by repository. Use a UTC RFC3339 timestamp and canonical file hashes computed from physical bytes.

- [ ] **Step 5: Run tests and commit**

```bash
python tools/verify_godot_multi_project_pilot_index.py \
  --index docs/knowledge/godot/evidence/multi-project-pilot/INDEX.json \
  --evidence-root docs/knowledge/godot/evidence/multi-project-pilot
python -m pytest tests/test_godot_multi_project_pilot_integration.py -q
python -m pytest tests/test_godot_multi_project_pilot_integration_adversarial.py -q
git add tools/verify_godot_multi_project_pilot_index.py docs/knowledge/godot/evidence/multi-project-pilot/INDEX.json tests/test_godot_multi_project_pilot_integration.py tests/test_godot_multi_project_pilot_integration_adversarial.py
git commit -m "feat: verify Godot multi-project Pilot evidence index"
```

---

### Task 6: Write the human-readable evidence summary and readiness update

**Files:**
- Create: `docs/knowledge/godot/evidence/multi-project-pilot/README.md`
- Modify: `docs/knowledge/godot/GODOT_PRODUCTION_ADAPTER_READINESS.md`

**Interfaces:**
- Consumes: verified `INDEX.json`.
- Produces: accurate human summary and next-design gate.

- [ ] **Step 1: Generate the summary from the index**

The Markdown table includes repository, merged SHA, result, project load, main Scene inspect, scratch transaction, source integrity, legacy state, workflow run ID, artifact ID, and canonical evidence path.

- [ ] **Step 2: State limitations verbatim**

```yaml
program_a_multi_project_pilots: value from verified index
production_transport: NOT_IMPLEMENTED
mcp_profile: NOT_IMPLEMENTED
runtime_debugger: NOT_IMPLEMENTED
windows_production_operation: NOT_RUN
physical_input: NOT_RUN
human_editor_usability: HUMAN_NOT_RUN
production_adapter_ready: NOT_READY
program_b_design_gate: value from verified index
```

- [ ] **Step 3: Prevent Program B implementation overclaim**

The document must say that `program_b_design_gate: OPEN` authorizes a new brainstorming/spec/approval cycle only. No transport code, endpoint, session token, or MCP capability is approved by C1.

- [ ] **Step 4: Commit**

```bash
git add docs/knowledge/godot/evidence/multi-project-pilot/README.md docs/knowledge/godot/GODOT_PRODUCTION_ADAPTER_READINESS.md
git commit -m "docs: integrate Godot multi-project Pilot readiness"
```

---

### Task 7: Connect required suites and coupled references

**Files:**
- Modify: `tests/test_local_validation.py`
- Modify: `tests/test_v9_machine_contracts.py`
- Modify: `.github/reference-freshness.json` only if required.

**Interfaces:**
- Produces: mandatory CI discovery for C1 evidence/index validation.

- [ ] **Step 1: Import both integration test modules into required suites**

Follow the existing Base aggregation convention. Do not leave standalone tests uncalled by required workflows.

- [ ] **Step 2: Add freshness coupling**

If the current reference-freshness policy tracks readiness/evidence consumers, connect:

```text
INDEX.json
README.md
GODOT_PRODUCTION_ADAPTER_READINESS.md
Schema
verifier
integration tests
```

- [ ] **Step 3: Run focused and aggregate validation**

```bash
python tools/verify_godot_multi_project_pilot_index.py \
  --index docs/knowledge/godot/evidence/multi-project-pilot/INDEX.json \
  --evidence-root docs/knowledge/godot/evidence/multi-project-pilot
python -m pytest tests/test_godot_multi_project_pilot_integration.py -q
python -m pytest tests/test_godot_multi_project_pilot_integration_adversarial.py -q
python -m pytest tests/test_godot_multi_project_pilot.py -q
python -m pytest tests/test_godot_multi_project_pilot_adversarial.py -q
python -m pytest tests/test_local_validation.py tests/test_v9_machine_contracts.py -q
```

- [ ] **Step 4: Commit**

```bash
git add tests/test_local_validation.py tests/test_v9_machine_contracts.py .github/reference-freshness.json
git commit -m "test: require multi-project Godot Pilot evidence"
```

---

### Task 8: Perform final adversarial review and exact-head PR validation

**Files:**
- No new production files.

**Interfaces:**
- Produces: reviewed Base C1 Draft PR and final Program A status.

- [ ] **Step 1: Attack evidence identity and scope**

Attempt each failure:

```text
artifact from wrong repository
artifact from wrong workflow run
source commit not equal merged adoption commit
floating or mixed Base C0 pin
archive traversal or symlink
final JSON hash mismatch
saved scratch Scene byte mismatch
source before/after mismatch hidden by prose
missing project
GRIMOIRE marked runtime PASS
blocked project treated as PASS
Program B OPEN while program state blocked/fail
production adapter marked READY
project or Google Sheet mutation in C1
```

- [ ] **Step 2: Run complete tests**

```bash
python tools/verify_godot_multi_project_pilot_index.py \
  --index docs/knowledge/godot/evidence/multi-project-pilot/INDEX.json \
  --evidence-root docs/knowledge/godot/evidence/multi-project-pilot
python -m pytest tests/test_godot_multi_project_pilot_integration.py -q
python -m pytest tests/test_godot_multi_project_pilot_integration_adversarial.py -q
python -m pytest tests/test_godot_multi_project_pilot.py -q
python -m pytest tests/test_godot_multi_project_pilot_adversarial.py -q
python -m pytest tests/test_godot_editor_transaction_adapter.py -q
python -m pytest tests/test_godot_editor_transaction_adapter_runtime.py -q
python -m pytest tests/test_local_validation.py tests/test_v9_machine_contracts.py -q
python -m unittest discover -s tests -p 'test_*.py'
git diff --check
```

- [ ] **Step 3: Verify protected boundaries**

No changes to Skill Registry, released locks, v1 Schemas/evidence, project repositories, Google Sheets, transport, MCP, debugger, binaries, or archives.

- [ ] **Step 4: Open a Draft PR**

The PR body lists all six exact project merged SHAs, run/artifact IDs, canonical hashes, program state, Program B design gate, and remaining NOT_READY items.

- [ ] **Step 5: Require exact-head GitHub Actions and zero unresolved threads**

Required:

```text
Validate Base v9 Operating Contracts: SUCCESS
Validate Game Project Operating System: SUCCESS
multi-project integration focused tests: SUCCESS
adversarial evidence tests: SUCCESS
branch behind main: 0
unresolved review threads: 0
```

- [ ] **Step 6: Merge only after explicit approval**

Squash merge with expected head SHA. After merge, verify Base `main` and push CI. Program A may then be called complete according to the verified index state; Program B remains a separate design request.
