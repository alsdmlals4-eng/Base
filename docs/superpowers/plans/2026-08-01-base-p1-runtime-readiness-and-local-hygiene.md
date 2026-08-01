# Base P1 Runtime Readiness and Local Hygiene Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make publication readiness executable and shared, and provide one local validation command that cannot leak owned temporary fixtures into the repository.

**Architecture:** A focused `publication_readiness` module resolves existing publication paths, runs bounded real-process probes, and returns one structured readiness result consumed by the preflight CLI and both generation test modules. A separate local validation runner executes the repository's canonical checks inside an owned `.tmp/local-validation-*` environment and removes only that session in `finally`.

**Tech Stack:** Python 3.12 standard library, existing `publication_v3` path helpers, `unittest`, Git, LibreOffice and Poppler subprocess probes.

## Global Constraints

- Baseline is `main@9f69a8e3badc49bcc4f9378551708f63cb54c7cd` on `codex/base-p1-runtime-hygiene`.
- Preserve released v9.0-v9.4 lock files, Registry bytes, generated Base artifacts, v7/v8 compatibility materials, project repositories, Google Sheets, Godot code, and assets.
- Basic publication readiness requires executable LibreOffice conversion, executable Poppler, `font_regular`, and `font_bold`.
- Environment-dependent generation tests must report `SKIPPED`, never `PASSED`, when readiness is false.
- Local cleanup may remove only the exact current `.tmp/local-validation-*` session; never glob or delete arbitrary `tmp*`, `.venv`, caches, or user files.
- `.gitignore` adds `.venv/` and `.tmp/` only; generic `tmp*` remains visible.
- Use TDD: every production behavior is observed RED for its intended missing behavior before implementation.
- Accessibility, performance, Godot runtime, project Google Sheets, and human visual review are not applicable and must not be reported as executed.

---

### Task 1: Shared Executable Publication Readiness

**Files:**
- Create: `tools/publication_readiness.py`
- Create: `tests/test_publication_readiness.py`
- Modify: `tools/check_publication_environment.py`

**Interfaces:**
- Consumes: a repository root and publication paths resolved by `tools/publication_v3.py`.
- Produces: `PublicationTools`, `ReadinessReport`, `resolve_publication_tools(root)`, `probe_publication_readiness(tools, require_mermaid=False)`, and cached `publication_readiness(root, require_mermaid=False)`.
- `ReadinessReport.ready` is true only when every required path exists and every required probe succeeds.
- `ReadinessReport.as_dict()` is JSON-safe and preserves `tools`, `versions`, `probe_failures`, `missing`, `ready`, and `skip_reason`.

- [x] **Step 1: Write real-process readiness fixtures**

Create executable fixture scripts inside `TemporaryDirectory()` and literal font files. The tests name these production breaks:

```python
class PublicationReadinessTests(unittest.TestCase):
    def test_existing_libreoffice_wrapper_without_pdf_is_not_ready(self) -> None:
        tools = self.tools(libreoffice=self.executable("exit 0\n"))
        report = readiness.probe_publication_readiness(tools)
        self.assertFalse(report.ready)
        self.assertIn("libreoffice", report.probe_failures)

    def test_existing_poppler_wrapper_that_fails_is_not_ready(self) -> None:
        tools = self.tools(pdftoppm=self.executable("exit 9\n"))
        report = readiness.probe_publication_readiness(tools)
        self.assertFalse(report.ready)
        self.assertIn("pdftoppm", report.probe_failures)

    def test_missing_regular_or_bold_font_is_not_ready(self) -> None:
        for missing_name in ("font_regular", "font_bold"):
            with self.subTest(missing_name=missing_name):
                tools = replace(self.working_tools(), **{missing_name: None})
                report = readiness.probe_publication_readiness(tools)
                self.assertFalse(report.ready)
                self.assertIn(missing_name, report.missing)

    def test_working_basic_tools_and_both_fonts_are_ready(self) -> None:
        report = readiness.probe_publication_readiness(self.working_tools())
        self.assertTrue(report.ready, report.skip_reason)
        self.assertEqual([], report.missing)
        self.assertEqual({}, report.probe_failures)
```

The working LibreOffice fixture parses `--outdir` and copies a literal minimal `%PDF-` file to `probe.pdf`; the working Poppler fixture exits zero for `-v`. No process behavior is mocked.

- [x] **Step 2: Run RED and confirm the module is missing**

Run:

```bash
/workspace/scratch/3c4c7a52226c/base-p1-env/bin/python -m unittest tests.test_publication_readiness -v
```

Expected: import failure for `tools.publication_readiness`, not a fixture syntax error.

- [x] **Step 3: Implement the minimal readiness module**

Use immutable dataclasses and bounded subprocesses:

```python
@dataclass(frozen=True)
class PublicationTools:
    libreoffice: str | None
    pdftoppm: str | None
    mermaid_cli: str | None
    chrome: str | None
    node: str | None
    pnpm: str | None
    font_regular: str | None
    font_bold: str | None


@dataclass(frozen=True)
class ReadinessReport:
    tools: PublicationTools
    versions: dict[str, str | None]
    probe_failures: dict[str, str]
    missing: tuple[str, ...]

    @property
    def ready(self) -> bool:
        return not self.missing and not self.probe_failures

    @property
    def skip_reason(self) -> str:
        names = sorted(set(self.missing) | set(self.probe_failures))
        return "publication runtime unavailable: " + ", ".join(names)
```

`_libreoffice_smoke` must verify a `%PDF-` output. `_command_version` must treat timeout and non-zero status as failures. `_terminate_process_tree` retains the existing Windows and POSIX behavior. `publication_readiness` uses `@lru_cache(maxsize=None)` keyed by resolved root string and `require_mermaid`.

- [x] **Step 4: Run focused GREEN**

Run the Task 1 test command. Expected: all readiness fixtures pass.

- [x] **Step 5: Convert the preflight CLI to the shared report**

Replace the CLI-local `version`, `libreoffice_smoke`, and process-tree helpers with:

```python
readiness = publication_readiness.publication_readiness(root, require_mermaid=args.require_mermaid)
report = {
    "platform": platform.platform(),
    **readiness.as_dict(),
    "output_path": str(output),
    "output_parent_exists": output.parent.exists(),
    "output_writable": os.access(output if output.exists() else output.parent, os.W_OK),
    "recovery": RECOVERY,
}
return 1 if not readiness.ready or not report["output_writable"] else 0
```

Keep `--output`, `--require-mermaid`, JSON output, and recovery override names compatible.

- [x] **Step 6: Add and run CLI behavior tests**

Add a test that invokes the real CLI with fake paths and verifies `font_bold` appears in `missing` and the exit status is non-zero. Run Task 1 tests and `tools/check_publication_environment.py` in the current environment; current expected status is non-zero with missing regular and bold fonts.

- [x] **Step 7: Commit Task 1**

```bash
git add tools/publication_readiness.py tools/check_publication_environment.py tests/test_publication_readiness.py
git diff --cached --check
git commit -m "fix: share executable publication readiness"
```

### Task 2: Make Generation Tests Consume the Shared Contract

**Files:**
- Modify: `tests/test_design_document_generation.py`
- Modify: `tests/test_project_skill_map_generation.py`

**Interfaces:**
- Consumes: `publication_readiness(REPOSITORY_ROOT)`.
- Produces: one cached basic readiness report and class-level skips with its `skip_reason`.

- [x] **Step 1: Capture the baseline failure as RED evidence**

Run:

```bash
TMPDIR=/tmp TMP=/tmp TEMP=/tmp \
/workspace/scratch/3c4c7a52226c/base-p1-env/bin/python -m unittest \
  tests.test_design_document_generation \
  tests.test_project_skill_map_generation -v
```

Expected baseline: two font-related failures because the old file-only skip gate enters the classes.

- [x] **Step 2: Replace both duplicate availability helpers**

In each module:

```python
from tools.publication_readiness import publication_readiness

PUBLICATION_READINESS = publication_readiness(REPOSITORY_ROOT)

@unittest.skipUnless(
    PUBLICATION_READINESS.ready,
    PUBLICATION_READINESS.skip_reason,
)
class ...
```

Remove imports used only by the deleted helpers. Do not weaken assertions inside provisioned generation tests.

- [x] **Step 3: Run focused GREEN in the current environment**

Run the Task 2 command. Expected: the two classes are explicitly skipped for `font_bold, font_regular`; Mermaid remains independently skipped when unavailable; zero failures.

- [x] **Step 4: Run the readiness fixtures again**

Run Task 1 tests to prove working fake tools still produce `ready=True`, preventing a blanket always-skip implementation.

- [x] **Step 5: Commit Task 2**

```bash
git add tests/test_design_document_generation.py tests/test_project_skill_map_generation.py
git diff --cached --check
git commit -m "test: gate publication generation on executable readiness"
```

### Task 3: Isolated Canonical Local Validation

**Files:**
- Create: `tools/run_local_validation.py`
- Create: `tests/test_local_validation.py`
- Modify: `tests/test_ci_required_gate_topology.py`
- Modify: `.gitignore`
- Modify: `.github/workflows/validate-game-project-operating-system.yml`

**Interfaces:**
- `default_commands(python: str, trusted_history_commit: str) -> tuple[tuple[str, ...], ...]` returns the canonical fixed validation sequence.
- `run_validation(repository_root: Path, commands: Sequence[Sequence[str]], environment: Mapping[str, str] | None = None) -> int` creates and owns one validation session, runs real child commands in order, propagates the first failure, and cleans the session in `finally`.
- CLI: `python tools/run_local_validation.py --trusted-history-commit <commit>`.

- [x] **Step 1: Write runner cleanup and failure-propagation tests**

Use real child Python processes that record their received `TMPDIR`, `TMP`, and `TEMP` to a test-owned evidence file:

```python
def test_success_uses_owned_temp_environment_and_cleans_it(self) -> None:
    status = runner.run_validation(self.root, [self.recording_command(exit_code=0)])
    session = Path(json.loads(self.evidence.read_text())["TMPDIR"])
    self.assertEqual(session.parent, self.root / ".tmp")
    self.assertTrue(session.name.startswith("local-validation-"))
    self.assertFalse(session.exists())

def test_failure_status_is_propagated_and_owned_session_is_cleaned(self) -> None:
    status = runner.run_validation(self.root, [self.recording_command(exit_code=7)])
    session = Path(json.loads(self.evidence.read_text())["TMPDIR"])
    self.assertEqual(7, status)
    self.assertFalse(session.exists())

def test_ignore_contract_hides_only_owned_roots(self) -> None:
    self.assertTrue(git_check_ignore(".venv/probe"))
    self.assertTrue(git_check_ignore(".tmp/probe"))
    self.assertFalse(git_check_ignore("tmp-user-data/probe"))
```

- [x] **Step 2: Run RED**

Run:

```bash
/workspace/scratch/3c4c7a52226c/base-p1-env/bin/python -m unittest tests.test_local_validation -v
```

Expected: import failure for `tools.run_local_validation` and ignore assertions fail before `.gitignore` changes.

- [x] **Step 3: Implement minimal runner and hygiene rules**

The runner must validate cleanup ownership before deletion:

```python
temp_root = repository_root / ".tmp"
temp_root.mkdir(exist_ok=True)
session = Path(tempfile.mkdtemp(prefix="local-validation-", dir=temp_root))
child_environment = dict(os.environ if environment is None else environment)
child_environment.update({name: str(session) for name in ("TMPDIR", "TMP", "TEMP")})
try:
    for command in commands:
        result = subprocess.run(command, cwd=repository_root, env=child_environment, check=False)
        if result.returncode:
            return result.returncode
    return 0
finally:
    _remove_owned_session(repository_root, session)
```

`_remove_owned_session` resolves both paths, requires `session.parent == <repo>/.tmp` and the prefix, then removes that exact tree. It may remove `.tmp` only if empty.

Default commands are full unittest discovery, CI topology, Base v9 artifact `--check`, Base v9 integrity with the supplied trusted commit, Skill coverage, `git diff --check`, and `git fsck --strict`.

Add to `.gitignore`:

```gitignore
.venv/
.tmp/
```

Change the topology fixture from `TemporaryDirectory(dir=ROOT)` to `TemporaryDirectory(prefix="base-ci-topology-")` so it honors the runner's environment.

- [x] **Step 4: Run focused GREEN and topology regression**

```bash
/workspace/scratch/3c4c7a52226c/base-p1-env/bin/python -m unittest \
  tests.test_local_validation tests.test_ci_required_gate_topology -v
git status --short
```

Expected: tests pass and no repository-root `tmp*` fixture appears.

- [x] **Step 5: Wire the new files into CI risk and syntax coverage**

Add `tools/publication_readiness.py`, `tools/run_local_validation.py`, `tests/test_publication_readiness.py`, and `tests/test_local_validation.py` to the publication/high-risk classifier or contract syntax/test lists according to responsibility. The local runner itself is contract tooling; readiness changes require publication and Windows smoke evidence.

- [x] **Step 6: Run topology and CI policy regression**

```bash
/workspace/scratch/3c4c7a52226c/base-p1-env/bin/python -m unittest \
  tests.test_ci_workflow_cost_policy tests.test_ci_required_gate_topology -v
/workspace/scratch/3c4c7a52226c/base-p1-env/bin/python tools/check_ci_required_gate_topology.py
```

- [x] **Step 7: Commit Task 3**

```bash
git add .gitignore .github/workflows/validate-game-project-operating-system.yml \
  tools/run_local_validation.py tests/test_local_validation.py \
  tests/test_ci_required_gate_topology.py
git diff --cached --check
git commit -m "feat: isolate canonical local validation"
```

### Task 4: Documentation, Learning Evidence, and Full Review

**Files:**
- Modify: `README.md`
- Modify: `docs/CHANGELOG.md`
- Modify: `docs/DOCUMENTATION_MAP.md` only if the new local entrypoint is a mapped operating tool under current map rules.
- Modify: `skills/SKILL_LEARNING_LOG.md`
- Modify: this plan to mark completed checkboxes.

**Interfaces:**
- Documents one canonical local command, readiness semantics, actual observation status, and rollback.

- [x] **Step 1: Document the canonical command and readiness boundary**

Add the exact command:

```bash
python tools/run_local_validation.py --trusted-history-commit origin/main
```

State that generation tests skip with a named reason when executable tools or either required font are unavailable; they do not pass publication validation.

- [x] **Step 2: Record the observation without over-promoting it**

Learning Log evidence:

- old existence-only gates ran two generation classes and produced two font failures in a 396-test baseline;
- shared executable/font readiness is the implemented hypothesis;
- current-environment generation is `SKIPPED`, not publication `PASSED`;
- one successful repository does not establish a universal external project mandate.

- [x] **Step 3: Run focused and full local validation through the new entrypoint**

```bash
/workspace/scratch/3c4c7a52226c/base-p1-env/bin/python \
  tools/run_local_validation.py \
  --trusted-history-commit 9f69a8e3badc49bcc4f9378551708f63cb54c7cd
```

Expected: zero failures; environment-dependent publication generation is explicitly skipped; `.tmp/` has no remaining owned session.

- [x] **Step 4: Run reference freshness for the working diff**

Commit the documentation/task changes, then run:

```bash
/workspace/scratch/3c4c7a52226c/base-p1-env/bin/python \
  tools/check_canonical_reference_freshness.py \
  --config .github/reference-freshness.json \
  --base 9f69a8e3badc49bcc4f9378551708f63cb54c7cd \
  --head HEAD
```

Expected: all changed files classified and no active stale or untouched consumer finding.

- [x] **Step 5: Execute adversarial review and minimal refinement**

Attack:

- wrappers that exist but return success without output;
- one of two fonts missing;
- timeouts and non-zero exits;
- skip reason masking a provisioned failure;
- cleanup path escape, symlink/parent mismatch, foreign session deletion, and child failure masking;
- CI classifier or syntax list omitting new tooling;
- broad ignore patterns hiding user data;
- released lock, Registry, or generated artifact drift.

Classify findings as `MUST_FIX / SHOULD_FIX / DEFER / REJECTED_CRITIQUE / BLOCKED_UNVERIFIED`, fix only validated in-scope findings, and rerun focused plus full validation.

- [x] **Step 6: Commit Task 4**

```bash
git add README.md docs/CHANGELOG.md docs/DOCUMENTATION_MAP.md \
  skills/SKILL_LEARNING_LOG.md \
  docs/superpowers/plans/2026-08-01-base-p1-runtime-readiness-and-local-hygiene.md
git diff --cached --check
git commit -m "docs: record P1 runtime validation contract"
```

- [ ] **Step 7: Publish and exact-head verify**

Use the repository PR lifecycle: compare local/remote heads, push the verified branch, create a Draft PR, verify every workflow on the exact head including conditional publication and Windows smoke, resolve review findings, mark ready only after checks pass, then exact-head squash merge. Re-fetch `main`, compare the merged tree, confirm branch cleanup, and run `post-merge-review` before moving to P2.

## Self-review

- Spec coverage: all readiness, consumer, cleanup, ignore, CI, documentation, adversarial, and exact-head requirements map to Tasks 1-4.
- Placeholder scan: no unresolved marker or unspecified code step remains.
- Type consistency: `PublicationTools`, `ReadinessReport`, `publication_readiness`, `default_commands`, and `run_validation` names are stable across tasks.
- Scope: no P2 compact-entrypoint work or P3 repository-community/security files are included.
