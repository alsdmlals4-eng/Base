# Base P0 CI Required Gate Consolidation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make `ci-gate` a single, always-created Required Check for every pull request while preserving the focused Base v9 contract and adversarial evidence.

**Architecture:** Add a standard-library topology checker that inspects workflow job and trigger structure, then use it to protect one canonical `ci-gate` owner. The main operating-system workflow runs on every pull request and classifies changes internally; the focused Base v9 workflow keeps its contract and adversarial jobs but no longer publishes a second `ci-gate` context.

**Tech Stack:** GitHub Actions YAML, Python 3.12 standard library, `unittest`, existing Base governance and reference-freshness tooling.

## Global Constraints

- Base branch is `main@0c2936bc375d522472c2b9c06e20786fb58cd2c7`.
- Work on `codex/base-p0-ci-gate-consolidation`; do not modify released v9.0-v9.4 lock files, Registry bytes, v7/v8 compatibility artifacts, project repositories, Google Sheets, Godot code, or assets.
- Preserve `base-v9-contract`, `adversarial-gate`, `classify-changes`, `docs-validation`, `ubuntu-contract`, conditional publication validation, and conditional Windows smoke evidence.
- Exactly one workflow job may expose the check-run name `ci-gate`; its canonical owner is `.github/workflows/validate-game-project-operating-system.yml`.
- The canonical owner must create `ci-gate` for every pull request, so its workflow-level `pull_request` trigger must not use `paths` or `paths-ignore`.
- Focused workflows may retain path filters but must not reuse the Required Check name `ci-gate`.
- Use TDD: each new behavior must be observed failing before its minimal implementation.
- Full verification uses `/workspace/scratch/63e271131098/Base/.venv/bin/python -m unittest discover -s tests -v` with the broken Work Mode LibreOffice/Poppler wrappers excluded from `PATH`.
- Accessibility, performance, Godot runtime, Google Sheets, and live model evaluation are not applicable to this CI topology change and must not be reported as executed.

---

### Task 1: Executable CI Required-Gate Topology Checker

**Files:**
- Create: `tools/check_ci_required_gate_topology.py`
- Create: `tests/test_ci_required_gate_topology.py`

**Interfaces:**
- Consumes: repository root containing `.github/workflows/*.yml` and `.yaml`.
- Produces: `validate_topology(root: Path) -> list[str]` and CLI `python tools/check_ci_required_gate_topology.py [--root PATH]`.
- CLI success: exit `0` and `CI REQUIRED GATE TOPOLOGY: PASS`.
- CLI failure: exit `1`, `CI REQUIRED GATE TOPOLOGY: FAIL`, and one `- <error>` line per violation.

- [ ] **Step 1: Write fixture tests that name the protected failures**

```python
from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "tools/check_ci_required_gate_topology.py"


class CiRequiredGateTopologyTests(unittest.TestCase):
    def _run(self, workflows: dict[str, str]) -> subprocess.CompletedProcess[str]:
        with tempfile.TemporaryDirectory(dir=ROOT) as temporary:
            fixture = Path(temporary)
            workflow_root = fixture / ".github/workflows"
            workflow_root.mkdir(parents=True)
            for name, body in workflows.items():
                (workflow_root / name).write_text(body, encoding="utf-8")
            return subprocess.run(
                [sys.executable, str(CHECKER), "--root", str(fixture)],
                capture_output=True,
                text=True,
                encoding="utf-8",
            )

    def test_single_unfiltered_canonical_gate_passes(self) -> None:
        result = self._run({
            "validate-game-project-operating-system.yml": """name: Canonical\non:\n  pull_request:\njobs:\n  ci-gate:\n    name: ci-gate\n    if: always()\n    runs-on: ubuntu-latest\n    steps:\n      - run: echo ok\n""",
            "focused.yml": """name: Focused\non:\n  pull_request:\n    paths:\n      - docs/**\njobs:\n  focused:\n    name: focused\n    runs-on: ubuntu-latest\n    steps:\n      - run: echo ok\n""",
        })
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn("CI REQUIRED GATE TOPOLOGY: PASS", result.stdout)

    def test_duplicate_ci_gate_names_fail(self) -> None:
        result = self._run({
            "validate-game-project-operating-system.yml": VALID_CANONICAL,
            "focused.yml": VALID_CANONICAL.replace("name: Canonical", "name: Focused"),
        })
        self.assertNotEqual(0, result.returncode)
        self.assertIn("exactly one workflow job must be named ci-gate", result.stdout)

    def test_path_filtered_canonical_pull_request_fails(self) -> None:
        filtered = VALID_CANONICAL.replace("  pull_request:\n", "  pull_request:\n    paths:\n      - docs/**\n")
        result = self._run({"validate-game-project-operating-system.yml": filtered})
        self.assertNotEqual(0, result.returncode)
        self.assertIn("pull_request trigger must not declare paths or paths-ignore", result.stdout)
```

The module may define `VALID_CANONICAL` once with the exact valid YAML shown in `test_single_unfiltered_canonical_gate_passes`; expected values remain literal and independent from checker helpers.

- [ ] **Step 2: Run tests and verify RED**

Run:

```bash
/workspace/scratch/63e271131098/Base/.venv/bin/python -m unittest tests.test_ci_required_gate_topology -v
```

Expected: FAIL because `tools/check_ci_required_gate_topology.py` does not exist.

- [ ] **Step 3: Implement the minimal indentation-aware checker**

```python
#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path


CANONICAL_WORKFLOW = Path(".github/workflows/validate-game-project-operating-system.yml")


def _indented_block(text: str, header: str, indent: int) -> str | None:
    lines = text.splitlines(keepends=True)
    prefix = " " * indent + header + ":"
    for index, line in enumerate(lines):
        if line.rstrip() == prefix:
            body: list[str] = []
            for candidate in lines[index + 1:]:
                stripped = candidate.lstrip(" ")
                current_indent = len(candidate) - len(stripped)
                if stripped.strip() and current_indent <= indent:
                    break
                body.append(candidate)
            return "".join(body)
    return None


def _job_names(path: Path, text: str) -> list[tuple[str, str]]:
    jobs = _indented_block(text, "jobs", 0) or ""
    matches = re.finditer(r"(?m)^  ([A-Za-z0-9_-]+):\n(?P<body>(?:^(?: {4,}.*|\s*)\n?)*)", jobs)
    found: list[tuple[str, str]] = []
    for match in matches:
        name = re.search(r"(?m)^    name:\s*['\"]?([^'\"#\n]+?)['\"]?\s*$", match.group("body"))
        if name:
            found.append((match.group(1), name.group(1).strip()))
    return found


def validate_topology(root: Path) -> list[str]:
    workflow_root = root / ".github/workflows"
    workflows = sorted([*workflow_root.glob("*.yml"), *workflow_root.glob("*.yaml")])
    errors: list[str] = []
    named_gates: list[tuple[str, str]] = []
    for workflow in workflows:
        text = workflow.read_text(encoding="utf-8")
        for job_id, job_name in _job_names(workflow, text):
            if job_name == "ci-gate":
                named_gates.append((workflow.relative_to(root).as_posix(), job_id))
    if len(named_gates) != 1:
        errors.append(f"exactly one workflow job must be named ci-gate; found {named_gates}")
    elif named_gates[0] != (CANONICAL_WORKFLOW.as_posix(), "ci-gate"):
        errors.append(f"ci-gate must be owned by {CANONICAL_WORKFLOW.as_posix()} job ci-gate")

    canonical = root / CANONICAL_WORKFLOW
    if not canonical.is_file():
        errors.append(f"canonical workflow is missing: {CANONICAL_WORKFLOW.as_posix()}")
        return errors
    canonical_text = canonical.read_text(encoding="utf-8")
    on_block = _indented_block(canonical_text, "on", 0)
    pull_request = _indented_block(on_block or "", "pull_request", 2)
    if on_block is None or pull_request is None:
        errors.append("canonical workflow must declare a pull_request trigger")
    elif re.search(r"(?m)^    (paths|paths-ignore):", pull_request):
        errors.append("canonical pull_request trigger must not declare paths or paths-ignore")
    return errors
```

Finish the CLI by resolving `--root`, printing the exact PASS/FAIL markers above, and returning the corresponding exit code. Keep the parser limited to the repository's block-style workflow structure; do not add PyYAML or another dependency.

- [ ] **Step 4: Run fixture tests and verify GREEN**

Run:

```bash
/workspace/scratch/63e271131098/Base/.venv/bin/python -m unittest tests.test_ci_required_gate_topology -v
```

Expected: all fixture tests PASS.

- [ ] **Step 5: Commit Task 1**

```bash
git add -- tools/check_ci_required_gate_topology.py tests/test_ci_required_gate_topology.py
git commit -m "test: add required CI gate topology checker"
```

### Task 2: Consolidate the Required Check and Remove the Pending Path-Filter Failure

**Files:**
- Modify: `tests/test_ci_required_gate_topology.py`
- Modify: `.github/workflows/validate-game-project-operating-system.yml`
- Modify: `.github/workflows/validate-base-v9-rc.yml`

**Interfaces:**
- Consumes: Task 1 `validate_topology(root)` and CLI.
- Produces: one repository-wide `ci-gate` context, emitted by the canonical workflow on every pull request.
- Preserves: focused `base-v9-contract` and `adversarial-gate` results.

- [ ] **Step 1: Add the repository integration test**

```python
    def test_current_repository_topology_passes(self) -> None:
        result = subprocess.run(
            [sys.executable, str(CHECKER), "--root", str(ROOT)],
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
```

- [ ] **Step 2: Run the integration test and verify RED**

Run:

```bash
/workspace/scratch/63e271131098/Base/.venv/bin/python -m unittest tests.test_ci_required_gate_topology.CiRequiredGateTopologyTests.test_current_repository_topology_passes -v
```

Expected: FAIL reporting two `ci-gate` job names and the canonical `pull_request.paths` filter.

- [ ] **Step 3: Make the canonical workflow run for every pull request**

Replace the canonical trigger prefix with:

```yaml
on:
  pull_request:
  push:
    branches:
      - main
    paths:
```

Remove only the existing `pull_request.paths` list. Retain the existing `push`, `schedule`, `workflow_dispatch`, classifier, conditional jobs, concurrency, and `ci-gate` body.

- [ ] **Step 4: Remove the duplicate focused gate without deleting focused evidence**

Delete the `ci-gate` job from `.github/workflows/validate-base-v9-rc.yml`. Change `adversarial-gate` to:

```yaml
  adversarial-gate:
    name: adversarial-gate
    needs: base-v9-contract
    if: always()
    runs-on: ubuntu-latest
    steps:
      - name: Require contract evidence before adversarial review
        env:
          CONTRACT_RESULT: ${{ needs.base-v9-contract.result }}
        run: |
          test "$CONTRACT_RESULT" = "success"
          echo "Adversarial gate is ready for evidence-backed review"
```

- [ ] **Step 5: Run the topology checker and tests and verify GREEN**

Run:

```bash
/workspace/scratch/63e271131098/Base/.venv/bin/python tools/check_ci_required_gate_topology.py
/workspace/scratch/63e271131098/Base/.venv/bin/python -m unittest tests.test_ci_required_gate_topology tests.test_ci_workflow_cost_policy tests.test_v9_governance_documents -v
```

Expected: checker PASS; all listed tests PASS.

- [ ] **Step 6: Commit Task 2**

```bash
git add -- .github/workflows/validate-game-project-operating-system.yml .github/workflows/validate-base-v9-rc.yml tests/test_ci_required_gate_topology.py
git commit -m "fix: consolidate the required CI gate"
```

### Task 3: Wire the Checker into CI and Synchronize Operating Contracts

**Files:**
- Modify: `.github/workflows/validate-game-project-operating-system.yml`
- Modify: `docs/CI_EXECUTION_COST_POLICY.md`
- Modify: `docs/GITHUB_PRO_OPERATING_POLICY.md`
- Modify: `docs/CHANGELOG.md`
- Modify: `skills/SKILL_LEARNING_LOG.md`
- Test: `tests/test_ci_required_gate_topology.py`

**Interfaces:**
- Consumes: Task 1 checker and Task 2 canonical topology.
- Produces: every canonical CI run self-validates Required Check ownership before integration.

- [ ] **Step 1: Add a fixture test proving the checker is executed by canonical CI**

```python
    def test_canonical_workflow_must_execute_topology_checker(self) -> None:
        result = self._run({
            "validate-game-project-operating-system.yml": VALID_CANONICAL.replace(
                "      - run: python tools/check_ci_required_gate_topology.py\n",
                "      - run: echo unchecked\n",
            )
        })
        self.assertNotEqual(0, result.returncode)
        self.assertIn("canonical workflow must execute the Required Check topology checker", result.stdout)
```

Update `VALID_CANONICAL` so its gate-independent validation job contains the literal command `python tools/check_ci_required_gate_topology.py`. This fixture protects the consuming CI boundary: replacing the executable check with a no-op makes the checker fail.

- [ ] **Step 2: Run the new consumer test and verify RED**

Run:

```bash
/workspace/scratch/63e271131098/Base/.venv/bin/python -m unittest tests.test_ci_required_gate_topology.CiRequiredGateTopologyTests.test_canonical_workflow_must_execute_topology_checker -v
```

Expected: FAIL because `validate_topology()` does not enforce checker execution yet.

- [ ] **Step 3: Enforce self-consumption, then execute and compile the checker in canonical CI**

Extend `validate_topology()` with:

```python
    if "python tools/check_ci_required_gate_topology.py" not in canonical_text:
        errors.append("canonical workflow must execute the Required Check topology checker")
```

Add `tools/check_ci_required_gate_topology.py` and `tests/test_ci_required_gate_topology.py` to the existing `python -m py_compile` list. Add this command before the lightweight contract tests in `docs-validation`:

```yaml
      - name: Validate Required Check topology
        run: python tools/check_ci_required_gate_topology.py
```

Add `tests/test_ci_required_gate_topology.py` to both the lightweight and `ubuntu-contract` regression test lists.

- [ ] **Step 4: Synchronize the two policy sources**

Add the following invariant to `docs/CI_EXECUTION_COST_POLICY.md` near the stable-gate rules:

```text
저장소 전체에서 `name: ci-gate`를 노출하는 Job은 하나뿐이어야 한다. 그 Job을 소유한 Workflow의 `pull_request` 이벤트에는 Workflow-level `paths`·`paths-ignore`를 두지 않고 내부 분류 Job에서 비용 계층을 선택한다. 집중 Workflow는 path filter를 사용할 수 있지만 `ci-gate` 이름을 재사용하지 않는다.
```

Add the Base-specific ownership statement to `docs/GITHUB_PRO_OPERATING_POLICY.md`:

```text
Base의 Required Check `ci-gate` 소유자는 `.github/workflows/validate-game-project-operating-system.yml` 하나다. 다른 Workflow는 고유한 Job 이름을 사용하며, Repository Ruleset에서 선택된 `ci-gate`가 이 소유자의 check run인지 실제 PR로 확인한다.
```

- [ ] **Step 5: Record the completed operating change and reusable lesson**

Under the current Unreleased v9.5 section in `docs/CHANGELOG.md`, record that the Required Check now has one owner, the canonical PR trigger is unfiltered, and focused Base v9 evidence remains separate.

Append a dated entry to `skills/SKILL_LEARNING_LOG.md` containing these exact facts:

```text
- 상태: `OBSERVATION`
- 문제: 서로 다른 Workflow가 같은 `ci-gate` check name을 만들고, Required Check 소유 Workflow의 path filter가 일부 PR에서 check를 생성하지 않을 수 있었다.
- 결정: Required Check 이름은 저장소 전체에서 단일 소유하고, 소유 Workflow는 모든 PR에서 시작한 뒤 내부 classifier로 비용을 제어한다.
- 검증: 실행형 topology checker, fixture RED→GREEN, 전체 Python 회귀, 실제 PR Actions.
- 다음 검토 트리거: Required Check Pending 재발, Workflow 추가·이름 변경, Ruleset context 변경.
```

- [ ] **Step 6: Run focused verification and commit Task 3**

Run:

```bash
/workspace/scratch/63e271131098/Base/.venv/bin/python tools/check_ci_required_gate_topology.py
/workspace/scratch/63e271131098/Base/.venv/bin/python -m unittest tests.test_ci_required_gate_topology tests.test_ci_workflow_cost_policy tests.test_gpt_codex_workflow_contract tests.test_v9_governance_documents -v
git diff --check
```

Expected: checker PASS, all focused tests PASS, and no whitespace errors.

Commit:

```bash
git add -- .github/workflows/validate-game-project-operating-system.yml docs/CI_EXECUTION_COST_POLICY.md docs/GITHUB_PRO_OPERATING_POLICY.md docs/CHANGELOG.md skills/SKILL_LEARNING_LOG.md tests/test_ci_required_gate_topology.py
git commit -m "docs: bind the canonical required CI gate"
```

### Task 4: Full Verification, Adversarial Review, and GitHub Evidence

**Files:**
- Verify: all changed files from Tasks 1-3
- Report: PR body using `.github/pull_request_template.md`

**Interfaces:**
- Consumes: complete branch diff from `main@0c2936bc375d522472c2b9c06e20786fb58cd2c7`.
- Produces: local evidence, independent review verdict, Draft PR, exact-head Actions evidence, and merge/post-merge verdict.

- [ ] **Step 1: Run full local verification**

```bash
PATH=/workspace/scratch/63e271131098/Base/.venv/bin:/usr/bin:/bin \
PYTHONDONTWRITEBYTECODE=1 \
/workspace/scratch/63e271131098/Base/.venv/bin/python -m unittest discover -s tests -v
/workspace/scratch/63e271131098/Base/.venv/bin/python tools/check_ci_required_gate_topology.py
/workspace/scratch/63e271131098/Base/.venv/bin/python tools/build_base_v9_artifacts.py --check
/workspace/scratch/63e271131098/Base/.venv/bin/python tools/check_base_v9_integrity.py --trusted-history-commit 0c2936bc375d522472c2b9c06e20786fb58cd2c7
git diff --check 0c2936bc375d522472c2b9c06e20786fb58cd2c7...HEAD
git fsck --strict
```

Expected: 0 failures; environment-dependent publication tests may remain explicitly skipped; topology, generation, integrity, whitespace, and object checks PASS.

- [ ] **Step 2: Run contract-preservation and adversarial review**

Review the complete diff with these failure assumptions:

```text
- a docs-only or unknown-path PR never creates ci-gate
- a focused workflow reintroduces the same check name
- a required conditional job is skipped but ci-gate passes
- Base v9 contract or adversarial evidence was deleted
- main/nightly/full validation was weakened
- released lock or Registry bytes changed
```

Classify every finding as `MUST_FIX / SHOULD_FIX / DEFER / REJECTED_CRITIQUE / BLOCKED_UNVERIFIED`; resolve all `MUST_FIX` and approved `SHOULD_FIX`, then rerun focused and full verification.

#### Final-review design correction: fail-closed YAML boundary and executable gate evaluator

The final adversarial review proved that a regex/token checker cannot safely attest either full YAML semantics or inline Bash execution semantics. Before Step 3, replace that design with this bounded contract:

- Add `tools/evaluate_ci_required_gate.py`. It consumes the eight existing result/required environment values and exits nonzero unless `classify-changes` and `docs-validation` succeeded and every classifier-required conditional job succeeded. Invalid required flags fail closed.
- Add direct unit tests for success, always-required failure, each conditional required failure or skipped result, optional skipped jobs, and invalid/missing inputs.
- Replace the inline `ci-gate` Bash program with one unconditional `python tools/evaluate_ci_required_gate.py` step. Preserve the five `needs` entries and eight exact environment mappings. Do not add step/job `continue-on-error`, a conditional step, or a custom shell.
- Make the topology checker normalize only simple YAML mapping keys/scalars needed by this contract. Quoted/spaced/commented simple forms are decoded consistently. Folded scalars, aliases, anchors, tags, merge keys, or another ambiguous form in protected job-name/trigger fields fail closed instead of being treated as safe.
- Make the topology checker require the canonical gate job ID, `if: always()`, the five required dependencies, the eight exact environment mappings, and the exact evaluator command.
- Add RED→GREEN fixtures for the final-review counterexamples: folded/aliased/tagged gate names, escaped protected keys, merge injection, missing dependency/environment mapping, gate/step guards, failure masking, and command replacement.
- Wire the evaluator and its tests into compile, lightweight, and Ubuntu contract validation, then rerun the full branch verification and one fresh whole-branch review.

- [ ] **Step 3: Publish one Draft PR and inspect exact-head Actions**

```text
head: codex/base-p0-ci-gate-consolidation
base: main
title: fix: consolidate Base required CI gate
draft: true
```

The PR body must state the old duplicate contexts, the new single owner, preserved focused evidence, local commands/results, skipped environment tests, rollback, and that Repository Ruleset settings are independently verified or `UNVERIFIED_REPOSITORY_SETTING`.

- [ ] **Step 4: Complete the branch through the repository merge policy**

After all exact-head required checks succeed, review threads are resolved, the independent review has no P0/P1 finding, and the HEAD is unchanged, mark the PR ready and squash merge. Then fetch new `main`, verify the merged tree and closed PR, confirm the feature branch cleanup state, and run `running-adversarial-review-and-refinement: post-merge-review`.
