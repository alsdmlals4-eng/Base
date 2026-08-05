# Base C1 Godot Multi-Project Pilot Evidence Integration Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:test-driven-development` task by task, `superpowers:systematic-debugging` for unexpected evidence failures, and `superpowers:verification-before-completion` before Program A claims.

**Goal:** Reverify and preserve Program A outcomes from five real Godot projects plus GRIMOIRE readiness, update Base readiness truthfully, and decide only whether Program B design may begin.

**Architecture:** Each project workflow runs once on the PR and again on the squash-merged `main` commit. C1 consumes only the post-merge run recorded in the Program A ledger. An import tool verifies repository, merged commit, Base C0 cohort, workflow run, artifact, archive bytes, final evidence bytes, saved scratch Scene bytes, and source-inventory hashes before writing bounded canonical JSON. A closed aggregate index enforces complete coverage and continued `NOT_READY` status.

**Tech Stack:** Python 3.12, JSON Schema Draft 2020-12, GitHub CLI/API, ZIP-safe extraction, SHA-256, Base C0 evidence verifier, pytest, Base required Actions.

## Immutable evidence rules

- Governing design: `docs/superpowers/specs/2026-08-05-godot-multi-project-production-adapter-expansion-design.md`.
- C1 starts only after Base C0 and all six project PRs have approved merged outcomes.
- One immutable `BASE_C0_SHA` comes from the Base C0 merge ledger.
- All six project descriptors/static workflows must pin that same SHA.
- Five real-project inputs use the workflow run triggered by **push to the exact squash-merged project commit**.
- For each real project:

```yaml
validated_pr_head_sha: recorded review identity
merged_commit_sha: exact squash merge
postmerge_workflow_source_sha: must equal merged_commit_sha
postmerge_workflow_run_id: exact run
postmerge_artifact_id: exact artifact
base_c0_sha: exact cohort SHA
```

- PR-run artifacts may support review, but are not canonical C1 inputs.
- GRIMOIRE uses its push-triggered static readiness workflow; `artifact_id` is null and runtime result is `NOT_APPLICABLE`.
- Accepted project results: `PASS`, `BLOCKED_PREEXISTING`, `NOT_APPLICABLE`, `NOT_RUN`, `FAIL`.
- Imported files are bounded final evidence only; no raw full logs, project copies, Godot archives/binaries, temporary paths, tokens, or environment dumps are committed.
- C1 changes no project repository or Google Sheet and implements no Program B/C code.
- `production_adapter_ready` is always `NOT_READY` in Program A.

## Required cohort

```text
alsdmlals4-eng/Switchy-Express-Cargo-Puzzle
alsdmlals4-eng/Ten-Paces-Hidden-Moves
alsdmlals4-eng/Blacksmith
alsdmlals4-eng/omenward
alsdmlals4-eng/urban-legend
alsdmlals4-eng/GRIMOIRE-
```

## File responsibility map

- Create `schemas/godot-multi-project-pilot-evidence-index-v1.schema.json`
- Create `tools/import_godot_project_pilot_evidence.py`
- Create `tools/verify_godot_multi_project_pilot_index.py`
- Create `docs/knowledge/godot/evidence/multi-project-pilot/INDEX.json`
- Create `docs/knowledge/godot/evidence/multi-project-pilot/README.md`
- Create:
  - `switchy-express-cargo-puzzle.json`
  - `ten-paces-hidden-moves.json`
  - `blacksmith.json`
  - `omenward.json`
  - `urban-legend.json`
  - `grimoire-readiness.json`
- Modify `docs/knowledge/godot/GODOT_PRODUCTION_ADAPTER_READINESS.md`
- Create `tests/test_godot_multi_project_pilot_integration.py`
- Create `tests/test_godot_multi_project_pilot_integration_adversarial.py`
- Modify `tests/test_local_validation.py`
- Modify `tests/test_v9_machine_contracts.py`
- Modify `.github/reference-freshness.json` only if current coupling rules require it.

---

### Task 1: Build the exact post-merge input ledger

- [ ] For every project, fetch:
  - adoption/readiness PR metadata;
  - reviewed PR head SHA;
  - squash-merged commit SHA;
  - post-merge push workflow run;
  - workflow source/head SHA;
  - artifact metadata for real projects;
  - descriptor/static workflow blob at merged commit;
  - complete changed-file list.
- [ ] Require `postmerge_workflow_source_sha == merged_commit_sha`.
- [ ] Require the workflow was triggered by `push` on `main`, completed successfully for PASS claims, and was not rerun against a later commit.
- [ ] Real project PR changed-file set must equal its four adoption files. GRIMOIRE must equal its four readiness files.
- [ ] Extract `base_pilot_commit` from every merged descriptor and workflow; require exact cohort equality.
- [ ] Write a temporary input ledger outside the repository containing only public IDs and hashes:

```json
{
  "base_c0_sha": "40-hex",
  "projects": [
    {
      "repository": "owner/repo",
      "validated_pr_head_sha": "40-hex",
      "merged_commit_sha": "40-hex",
      "postmerge_workflow_run_id": 1,
      "postmerge_workflow_source_sha": "40-hex",
      "postmerge_artifact_id": 1,
      "expected_result": "PASS"
    }
  ]
}
```

GRIMOIRE uses `postmerge_artifact_id: null` and `expected_result: NOT_APPLICABLE`.

---

### Task 2: Define the closed aggregate index Schema first

**Create:**
- `schemas/godot-multi-project-pilot-evidence-index-v1.schema.json`
- `tests/test_godot_multi_project_pilot_integration.py`

- [ ] RED tests require:
  - root and project objects closed;
  - exact design ID;
  - one 40-hex Base C0 SHA;
  - `program_state: PASS | BLOCKED | FAIL`;
  - `program_b_design_gate: OPEN | BLOCKED`;
  - `production_adapter_ready: NOT_READY` constant;
  - exactly six project entries;
  - each entry contains repository, project ID/state, result, reviewed head, merged commit, post-merge run/source SHA, artifact ID, canonical path/hash;
  - real projects require integer artifact ID;
  - `NOT_CREATED` permits null artifact only with `NOT_APPLICABLE`.
- [ ] Verify RED:

```bash
python -m pytest tests/test_godot_multi_project_pilot_integration.py -q
```

- [ ] Implement Draft 2020-12 Schema with `additionalProperties: false` throughout.
- [ ] Commit Schema plus RED test.

---

### Task 3: Implement safe artifact import and physical verification

**Create:**
- `tools/import_godot_project_pilot_evidence.py`
- `tests/test_godot_multi_project_pilot_integration_adversarial.py`

**Interfaces:**

```python
@dataclass(frozen=True)
class EvidenceInput:
    repository: str
    validated_pr_head_sha: str
    merged_commit_sha: str
    postmerge_workflow_run_id: int
    postmerge_workflow_source_sha: str
    postmerge_artifact_id: int
    base_c0_sha: str

@dataclass(frozen=True)
class ImportedEvidence:
    repository: str
    merged_commit_sha: str
    archive_sha256: str
    final_evidence_sha256: str
    canonical_sha256: str

def import_local_artifact(record: EvidenceInput, archive: Path, output_path: Path) -> ImportedEvidence: ...
```

- [ ] RED tests cover valid local ZIP, wrong repository, wrong merged commit, wrong C0 SHA, wrong run/artifact IDs, wrong final evidence hash, and wrong saved scratch Scene bytes.
- [ ] Safe ZIP limits:

```text
no absolute or .. paths
no symlink members
no duplicate names
max 64 files
max archive 20 MiB
max expanded total 50 MiB
max individual file 10 MiB
```

- [ ] Hash archive before extraction.
- [ ] Reuse Base C0 `verify_runtime_evidence` for every referenced physical file.
- [ ] Require final evidence:
  - repository matches;
  - `source_commit == merged_commit_sha`;
  - `base_pilot_commit == base_c0_sha`;
  - workflow source SHA from ledger equals merged commit;
  - source-before/source-after inventories match for PASS;
  - required runtime fields match expected result.
- [ ] Emit canonical JSON without raw logs, local absolute paths, credentials, or environment variables.
- [ ] Run focused/adversarial tests and commit.

---

### Task 4: Download and import the five real-project artifacts

- [ ] Fetch artifact metadata first and prove each artifact belongs to the exact post-merge workflow run in the input ledger.
- [ ] Download through authenticated GitHub redirect handling.
- [ ] Run the importer once per project and write:

```text
docs/knowledge/godot/evidence/multi-project-pilot/switchy-express-cargo-puzzle.json
docs/knowledge/godot/evidence/multi-project-pilot/ten-paces-hidden-moves.json
docs/knowledge/godot/evidence/multi-project-pilot/blacksmith.json
docs/knowledge/godot/evidence/multi-project-pilot/omenward.json
docs/knowledge/godot/evidence/multi-project-pilot/urban-legend.json
```

- [ ] Canonical real-project JSON must include:

```text
repository and project_id
validated_pr_head_sha
merged_commit_sha
postmerge_workflow_run_id/source_sha/artifact_id
base_c0_sha
result and runtime states
engine version
archive and final evidence SHA-256
saved scratch Scene SHA-256
source inventory before/after SHA-256
legacy state and preserved Autoload evidence when applicable
limitations
```

- [ ] Re-read and independently hash each generated canonical file.
- [ ] Commit bounded project evidence only.

---

### Task 5: Import GRIMOIRE static readiness

- [ ] Read the merged descriptor, readiness document, changed-file list, and push-triggered static workflow run.
- [ ] Require workflow source SHA equals the merged GRIMOIRE commit and Base checkout ref equals cohort C0 SHA.
- [ ] Write `grimoire-readiness.json` containing:

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
  "validated_pr_head_sha": "40-hex",
  "merged_commit_sha": "40-hex",
  "postmerge_workflow_run_id": 1,
  "postmerge_workflow_source_sha": "40-hex",
  "postmerge_artifact_id": null,
  "source_scope_verified": true,
  "production_adapter_ready": "NOT_READY"
}
```

- [ ] Reject any Godot runtime result, scratch Scene, ledger, or runtime artifact for GRIMOIRE.
- [ ] Commit static readiness evidence.

---

### Task 6: Implement aggregate index validation

**Create:**
- `tools/verify_godot_multi_project_pilot_index.py`
- `docs/knowledge/godot/evidence/multi-project-pilot/INDEX.json`

**Interface:**

```python
def verify_index(index_path: Path, evidence_root: Path) -> tuple[str, ...]: ...
```

- [ ] RED/adversarial tests remove a project, duplicate a repository, alter canonical bytes, mix C0 SHAs, mismatch post-merge source and merged SHA, set GRIMOIRE PASS, treat a blocked project as PASS, open Program B while blocked, or mark production READY.
- [ ] Semantic rules:

```text
exact six unique repositories
one exact Base C0 cohort
physical canonical file hash equality
real PASS requires postmerge source == merged commit
real PASS requires all runtime fields PASS, unchanged source, no Base listener
BLOCKED_PREEXISTING requires bounded blocker evidence and no product mutation
GRIMOIRE is NOT_CREATED + NOT_APPLICABLE + null artifact
program PASS only when five real projects PASS and GRIMOIRE NOT_APPLICABLE
program BLOCKED when no FAIL exists and at least one real project blocked/not-run
program FAIL on any FAIL or identity/hash violation
Program B OPEN only when program PASS
production adapter always NOT_READY
```

- [ ] Generate `INDEX.json` deterministically, sorted by repository.
- [ ] Run verifier plus focused/adversarial tests and commit.

---

### Task 7: Write evidence summary and readiness state

**Create/modify:**
- `docs/knowledge/godot/evidence/multi-project-pilot/README.md`
- `docs/knowledge/godot/GODOT_PRODUCTION_ADAPTER_READINESS.md`

- [ ] Generate a table from the verified index: repository, merged SHA, post-merge run/artifact, result, main Scene inspect, scratch transaction, source integrity, legacy/Autoload state, canonical evidence path.
- [ ] Preserve exact limitations:

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

- [ ] State that Program B `OPEN` permits brainstorming/spec/approval only, never transport implementation.
- [ ] Commit docs.

---

### Task 8: Wire required CI and perform adversarial closure

- [ ] Import both C1 test modules into `tests/test_local_validation.py` and `tests/test_v9_machine_contracts.py`.
- [ ] Add reference-freshness coupling when required.
- [ ] Attack:

```text
wrong repository/run/artifact
PR artifact substituted for post-merge artifact
workflow source SHA differs from merged commit
mixed/floating C0 pin
archive traversal/symlink
physical hash mismatch
source mutation hidden by prose
missing project
GRIMOIRE runtime PASS
blocked treated as PASS
Program B or production readiness overclaim
project/Sheet mutation from C1
```

- [ ] Run:

```bash
python tools/verify_godot_multi_project_pilot_index.py --index docs/knowledge/godot/evidence/multi-project-pilot/INDEX.json --evidence-root docs/knowledge/godot/evidence/multi-project-pilot
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

- [ ] Confirm no Registry, lock, v1 evidence, project, Sheet, transport, MCP, debugger, binary, or archive changes.
- [ ] Open a Draft PR listing all immutable project identifiers and canonical hashes.
- [ ] Require exact-head Base workflows, branch behind main 0, and unresolved threads 0.
- [ ] Merge only after explicit user approval.
- [ ] After merge, verify Base push CI. Program A completion state is exactly the verified index state; Program B remains a separate design request.
