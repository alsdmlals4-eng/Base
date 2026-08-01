# Base P1 Runtime Readiness and Local Hygiene Design

## Status and authority

- Status: approved recommended implementation, resumed after P0 PR #124.
- Baseline: `main@9f69a8e3badc49bcc4f9378551708f63cb54c7cd`.
- Work branch: `codex/base-p1-runtime-hygiene`.
- Work Mode sequence: `PLAN → BUILD → REVIEW`.
- Base itself has no project Google Sheets requirement; project repositories remain out of scope.

## Problem

The publication preflight executes LibreOffice conversion and Poppler, but two generation test modules use a separate file-existence-only skip condition. A path can therefore look available while the command is broken or a required Korean font is absent. On the current baseline, the two test classes run because the Work Mode wrappers exist, then two of 396 tests fail when diagram generation cannot resolve a regular or bold Korean font.

Local verification also has no canonical entrypoint. Tests can select the repository as a temporary root, and interrupted or failed runs can leave untracked `tmp*` fixture directories. Local `.venv/` and the intended `.tmp/` validation root are not explicitly ignored.

## Approaches considered

### A. Shared executable readiness contract and isolated runner — selected

Create one standard-library readiness module consumed by the preflight CLI and both generation-test skip gates. Resolve the actual publication tools once, execute bounded LibreOffice and Poppler probes, require both regular and bold font paths, and return structured failure evidence. Add a Python local-validation runner that owns a repository-local `.tmp/` session directory, points `TMPDIR`, `TMP`, and `TEMP` at it, runs the canonical suite, and removes the session in `finally`.

This removes semantic duplication, gives the tests the same answer as the preflight, and makes cleanup ownership explicit.

### B. Patch the two test skip functions only

Call the preflight CLI from each test module and add a font check. This is smaller initially, but it duplicates subprocess/report parsing, runs the same probes multiple times, and allows the CLI and tests to drift again.

### C. Keep local behavior and rely on CI

Run publication generation only on provisioned Actions runners. This avoids local failures but preserves false local readiness and gives contributors no clean full-suite entrypoint.

## Architecture

### `tools/publication_readiness.py`

This module owns runtime readiness, not publication generation.

- `resolve_publication_tools(repository_root: Path) -> PublicationTools` resolves LibreOffice, Poppler, Mermaid, Chrome, Node, pnpm, and both fonts through the existing `publication_v3` path rules.
- `probe_publication_readiness(tools: PublicationTools, *, require_mermaid: bool = False) -> ReadinessReport` executes bounded probes and records every missing or failed prerequisite.
- `publication_readiness(repository_root: Path, *, require_mermaid: bool = False) -> ReadinessReport` combines resolution and probing and caches equivalent calls inside one Python process.
- A basic publication run requires executable LibreOffice conversion, executable Poppler, `font_regular`, and `font_bold`.
- Mermaid readiness additionally requires executable Mermaid CLI, Chrome, Node, and pnpm.
- A failed environment override, timeout, non-zero process, missing output, or missing font is not silently accepted.
- The report exposes JSON-safe `tools`, `versions`, `probe_failures`, `missing`, `ready`, and a concise `skip_reason`.

The module uses temporary probe directories outside publication outputs and terminates timed-out process groups. It does not install dependencies or mutate generated artifacts.

### `tools/check_publication_environment.py`

The existing CLI becomes a thin adapter over the shared readiness report. It adds platform, output-path writability, and recovery instructions, then exits non-zero when readiness or output writability fails. Existing command-line options and JSON field meanings remain compatible; `font_bold` becomes a required basic prerequisite instead of a displayed-but-unenforced value.

### Generation test consumers

`tests/test_design_document_generation.py` and `tests/test_project_skill_map_generation.py` import the shared readiness function. Their class-level skip condition uses the same basic report and includes its concise reason. A missing font or a broken wrapper therefore produces an explicit environment-dependent skip, while a fully provisioned environment still executes the real generation tests.

### `tools/run_local_validation.py`

The repository-local validation entrypoint:

1. resolves the repository root from its own path;
2. creates `.tmp/local-validation-*`;
3. sets child `TMPDIR`, `TMP`, and `TEMP` to that session;
4. runs the full unittest discovery and the existing Base topology, artifact, integrity, Skill coverage, whitespace, and Git object checks in a fixed fail-fast sequence;
5. forwards each command's output and exits with its first non-zero status;
6. removes the owned session directory in `finally` on success, test failure, or interruption;
7. removes the parent `.tmp/` only when it is empty and owned by this repository.

The runner accepts `--trusted-history-commit` so integrity checks do not invent a trust baseline. It does not delete arbitrary `tmp*`, user files, `.venv`, caches, or another run's session.

### Repository hygiene

`.gitignore` adds only `.venv/` and `.tmp/`. Broad `tmp*` patterns are deliberately excluded because they could hide user files or real fixtures. The topology test stops forcing `TemporaryDirectory(dir=ROOT)` and uses the active temporary sandbox instead.

## Data flow

```text
publication_v3 path resolution
        ↓
publication_readiness executable/font probes
        ├── check_publication_environment JSON + exit status
        ├── design-document generation skip gate
        └── project-skill-map generation skip gate

run_local_validation
        ↓ sets TMPDIR/TMP/TEMP
isolated child checks
        ↓
result propagation + owned-session cleanup
```

## Error and safety behavior

- Readiness is fail-closed: a path alone never proves the publication runtime.
- Every probe has a timeout and reports a stable first-line failure without masking the failing prerequisite.
- Environment-dependent publication tests are `SKIPPED`, not `PASSED`, when readiness is false.
- The local runner never retries or downgrades a failed validation command.
- Cleanup targets only the exact session path created by the current run after confirming it is beneath `<repo>/.tmp` and has the `local-validation-` prefix.
- Released v9.0-v9.4 locks, Registry bytes, generated Base artifacts, project repositories, Google Sheets, Godot code, and assets are protected.

## Test strategy

TDD fixtures use real temporary executable scripts and real subprocesses rather than mocks.

- A file-existing LibreOffice wrapper that exits zero without creating a PDF must be rejected.
- A file-existing Poppler wrapper that exits non-zero must be rejected.
- Missing regular or bold font paths must make basic readiness false.
- Fully working fake probes plus both font files must make basic readiness true.
- The preflight CLI and both generation skip consumers must use the shared result.
- The local runner must confine a child-created temporary file to its session, propagate child failure, and remove its owned session after both success and failure.
- A repository-root `tmp*` fixture must no longer be produced by the topology tests.
- Full regression remains 396 existing tests plus the new P1 tests, with environment-dependent publication tests explicitly skipped when prerequisites are absent.

## Completion criteria

- One readiness implementation owns executable and font truth for preflight and both generation test gates.
- The baseline two font-related failures become explicit skips in this environment without hiding failures in a provisioned environment.
- The canonical local runner leaves no untracked validation fixture after success or controlled failure.
- `.venv/` and `.tmp/` are ignored; arbitrary `tmp*` paths remain visible.
- Focused RED/GREEN evidence, full regression, topology, artifact, integrity, Skill coverage, whitespace, Git object, reference-freshness, exact-head Actions, and adversarial review are recorded.
- Accessibility, performance, Godot runtime, project Google Sheets, and human visual review remain `NOT_APPLICABLE` or `NOT_RUN` for this tooling-only change.

## Rollback

Revert the P1 commit. The prior preflight, test-local skip helpers, and direct validation commands remain available. No schema, lock, generated artifact, or project data migration is involved.
