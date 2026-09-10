from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from typing import Mapping, Sequence


ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools/run_project_work_gate.py"
OWNER = ROOT / "docs/operations/BASE_CURRENT_PROJECT_WORK_BOOTSTRAP.md"
_GIT = shutil.which("git")
if _GIT is None:
    raise RuntimeError("Git is required for Base-current bootstrap tests")
GIT = Path(_GIT).resolve()
DIRECT_CONSUMERS = (
    ROOT / "AGENTS.md",
    ROOT / "templates/custom-instructions.gpt.md",
    ROOT / "docs/BASE_SHARED_SKILL_ADAPTER_CONTRACT.md",
    ROOT / "skills/managing-project-intake-and-work-contract/SKILL.md",
    ROOT / "skills/managing-project-intake-and-work-contract/references/work-decomposition-and-sequencing.md",
    ROOT / "templates/planning/EXECUTION_SEQUENCE_PLAN.md",
    ROOT / "templates/project-operations/.agents/skills/base-project-router/SKILL.md",
    ROOT / "templates/project-operations/AI_WORKFLOW.md",
    ROOT / "templates/project-operations/PROJECT_START_HERE.md",
    ROOT / "templates/project-operations/WORK_CODEX_MINIMUM_TRANSITION_STARTER_PROMPT.md",
    ROOT / "templates/project-operations/WORK_PROJECT_EXECUTION_CURRENT_ROUTER.md",
    ROOT / "templates/project-operations/WORK_PROJECT_START_CANON_CHECKLIST.md",
)


def _clean_environment(
    overrides: Mapping[str, str] | None = None,
) -> dict[str, str]:
    environment = {
        key: value
        for key, value in os.environ.items()
        if not key.upper().startswith("GIT_")
        and key.upper() not in {"PYTHONPATH", "PYTHONHOME"}
    }
    environment.update(
        {
            "GIT_CONFIG_NOSYSTEM": "1",
            "GIT_CONFIG_GLOBAL": os.devnull,
            "GIT_TERMINAL_PROMPT": "0",
            "GIT_NO_REPLACE_OBJECTS": "1",
            "GIT_NO_LAZY_FETCH": "1",
        }
    )
    if overrides:
        environment.update(overrides)
    return environment


def _run(
    *argv: str,
    cwd: Path | None = None,
    input_text: str | None = None,
    environment: Mapping[str, str] | None = None,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        list(argv),
        cwd=cwd,
        input=input_text,
        text=True,
        capture_output=True,
        check=False,
        timeout=60,
        env=dict(environment) if environment is not None else None,
    )


def _git(root: Path, *args: str, check: bool = True) -> str:
    result = _run(
        str(GIT),
        "--no-replace-objects",
        "-c",
        "maintenance.auto=false",
        "-c",
        "gc.auto=0",
        "-C",
        str(root),
        *args,
        environment=_clean_environment(),
    )
    if check and result.returncode != 0:
        raise AssertionError(result.stdout + result.stderr)
    return result.stdout.strip()


def _commit_blob(root: Path, commit_sha: str, relative: str) -> bytes:
    result = subprocess.run(
        [
            str(GIT),
            "--no-replace-objects",
            "-c",
            "maintenance.auto=false",
            "-c",
            "gc.auto=0",
            "-C",
            str(root),
            "cat-file",
            "blob",
            f"{commit_sha}:{relative}",
        ],
        capture_output=True,
        check=False,
        timeout=30,
        env=_clean_environment(),
    )
    if result.returncode != 0:
        raise AssertionError(result.stdout.decode(errors="replace") + result.stderr.decode(errors="replace"))
    return bytes(result.stdout)


def _run_gate(
    *,
    base_root: Path,
    project_root: Path,
    project_source_sha: str,
    receipt: Path | str,
    phase: str = "start",
    verified_head_sha: str | None = None,
    render_markdown: bool = False,
    expected_base_sha: str | None = None,
    entrypoint_commit_sha: str | None = None,
    git_executable: Path = GIT,
    environment: Mapping[str, str] | None = None,
    entrypoint_digest: str | None = None,
) -> subprocess.CompletedProcess[str]:
    streamed_from = entrypoint_commit_sha or _git(base_root, "rev-parse", "HEAD")
    expected = expected_base_sha or streamed_from
    entrypoint = _commit_blob(
        base_root, streamed_from, "tools/run_project_work_gate.py"
    )
    digest = entrypoint_digest or hashlib.sha256(entrypoint).hexdigest()
    argv = [
        sys.executable,
        "-I",
        "-",
        "--entrypoint-source",
        "commit-stream",
        "--entrypoint-sha256",
        digest,
        "--git-executable",
        str(git_executable),
        "--base-root",
        str(base_root),
        "--expected-base-sha",
        expected,
        "--project-root",
        str(project_root),
        "--project-source-sha",
        project_source_sha,
        "--receipt",
        str(receipt),
        "--phase",
        phase,
    ]
    if verified_head_sha is not None:
        argv.extend(("--verified-head-sha", verified_head_sha))
    if render_markdown:
        argv.append("--render-markdown")
    completed = subprocess.run(
        argv,
        input=entrypoint,
        capture_output=True,
        check=False,
        timeout=60,
        env=(
            dict(environment)
            if environment is not None
            else _clean_environment()
        ),
    )
    return subprocess.CompletedProcess(
        completed.args,
        completed.returncode,
        completed.stdout.decode("utf-8", errors="replace"),
        completed.stderr.decode("utf-8", errors="replace"),
    )


def _init_project(root: Path) -> str:
    root.mkdir()
    for args in (
        ("init", "-q"),
        ("config", "user.email", "bootstrap-test@example.invalid"),
        ("config", "user.name", "bootstrap test"),
    ):
        _git(root, *args)
    (root / "AGENTS.md").write_text("# Project authority\n", encoding="utf-8")
    _git(root, "add", "AGENTS.md")
    _git(root, "commit", "-qm", "initial project authority")
    return _git(root, "rev-parse", "HEAD")


def _active_receipt(source_sha: str) -> dict[str, object]:
    return {
        "work_level": "L1",
        "benchmark_preflight_receipt": {
            "state": "PASS",
            "entries": [
                {
                    "source_and_evidence": "exact project source and Base-current bootstrap owner",
                    "observed_pattern": "one repository-owned or ephemeral work receipt drives the visible PM view",
                    "project_fit_and_difference": "reuse the Base workflow without changing project product canon",
                    "disposition": "ADAPT",
                }
            ],
        },
        "context_configuration_hygiene": {
            "scope": "bootstrap test only",
            "inventory": [
                {
                    "path": "AGENTS.md",
                    "classification": "ACTIVE_OWNER",
                    "owner_or_provenance": "temporary project authority",
                    "references_and_consumers": "Base-current project work bootstrap test",
                    "removal_proposed": False,
                }
            ],
        },
        "project_work_kanban": {
            "goal_or_slice_issue_ref": "approved bootstrap test goal",
            "source_main_sha": source_sha,
            "work_item_refs": ["BOOT-01"],
            "active_work_item_ref": "BOOT-01",
            "next_action": "run the approved bootstrap test task",
            "work_items": [
                {
                    "work_item_id": "BOOT-01",
                    "title": "validate Base-current project work entry",
                    "status": "IN_PROGRESS",
                    "canon_owner": "AGENTS.md",
                    "actual_consumers": ["temporary project work session"],
                    "depends_on": [],
                    "acceptance_criteria": ["AC-01"],
                    "required_evidence": ["E2_TEST"],
                    "checklist": [
                        {
                            "id": "AC-01",
                            "text": "Base current can validate a project without preinstalling Base files",
                            "status": "NOT_RUN",
                        }
                    ],
                    "verification": [
                        {
                            "level": "E2_TEST",
                            "status": "NOT_RUN",
                            "evidence": [],
                        }
                    ],
                    "next_action": "run the focused bootstrap behavior test",
                }
            ],
        },
    }


def _done_receipt(source_sha: str, verified_head_sha: str) -> dict[str, object]:
    value = _active_receipt(source_sha)
    board = value["project_work_kanban"]
    assert isinstance(board, dict)
    board["active_work_item_ref"] = None
    board["next_action"] = "STOP_APPROVED_SCOPE_COMPLETE"
    tasks = board["work_items"]
    assert isinstance(tasks, list)
    task = tasks[0]
    assert isinstance(task, dict)
    task.update(
        status="DONE",
        verified_head_sha=verified_head_sha,
        repository_readback="PASS",
        readback_evidence=["temporary project exact-head readback"],
        rollback="Discard the temporary repository.",
        must_fix_remaining=0,
        blocked_unverified_remaining=0,
        user_decision_required_remaining=0,
        next_action="STOP_APPROVED_SCOPE_COMPLETE",
    )
    task["checklist"][0].update(
        status="PASS", evidence=["focused bootstrap test"]
    )
    task["verification"][0].update(
        status="PASS", evidence=["focused bootstrap test"]
    )
    return value


class BaseCurrentProjectWorkBootstrapTests(unittest.TestCase):
    def test_base_only_entrypoint_and_owner_exist(self) -> None:
        self.assertTrue(TOOL.is_file(), "Base must own the cross-project PM entrypoint")
        self.assertTrue(OWNER.is_file(), "Base must own the current-work bootstrap contract")

    def test_owner_defines_the_noninvasive_authority_boundary(self) -> None:
        text = OWNER.read_text(encoding="utf-8")
        for token in (
            "BASE_CURRENT_OPERATIONAL_BOOTSTRAP",
            "NO_PROJECT_PREINSTALL_REQUIRED",
            "NO_FLEET_PROJECT_MUTATION",
            "EPHEMERAL_RECEIPT_ALLOWED",
            "PROJECT_CANON_PRECEDENCE",
            "ADOPTED_BASE_RELEASE_UNCHANGED",
            "PERSIST_TO_EXISTING_PROJECT_OWNER_ONLY_WHEN_WORK_REQUIRES",
            "BASE_CURRENT_IS_WORKFLOW_OVERLAY_NOT_PRODUCT_ADOPTION",
            "TRUSTED_COMMIT_STREAM_ENTRYPOINT",
            "ABSOLUTE_SYSTEM_GIT_REQUIRED",
            "LOCAL_COMMIT_OBJECTS_ONLY",
        ):
            self.assertIn(token, text)

    def test_active_consumers_route_to_the_base_current_owner(self) -> None:
        for path in DIRECT_CONSUMERS:
            text = path.read_text(encoding="utf-8")
            with self.subTest(path=path.relative_to(ROOT).as_posix()):
                self.assertIn("BASE_CURRENT_OPERATIONAL_BOOTSTRAP", text)
                self.assertIn("PROJECT_WORK_FRESH_BASE_ENTRY", text)
                self.assertIn("BASE_CURRENT_PROJECT_WORK_BOOTSTRAP.md", text)
                self.assertIn("ordinary target-project work", text)
                self.assertNotIn(
                    "when current scope requires **Base-only maintenance**", text
                )

    def test_project_can_start_without_adapter_or_project_receipt_file(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            project = root / "project"
            source = _init_project(project)
            external_receipt = root / "ephemeral-receipt.json"
            external_receipt.write_text(
                json.dumps(_active_receipt(source)), encoding="utf-8"
            )
            before = _git(
                project,
                "status",
                "--porcelain=v1",
                "--untracked-files=all",
            )

            result = _run_gate(
                base_root=ROOT,
                project_root=project,
                project_source_sha=source,
                receipt=external_receipt,
                phase="start",
                render_markdown=True,
            )

            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            self.assertIn("BASE CURRENT PROJECT WORK BOOTSTRAP: PASS", result.stdout)
            self.assertIn("BOOT-01", result.stdout)
            self.assertIn("ACTIVE", result.stdout)
            self.assertFalse((project / "skills/PROJECT_BASE_ADAPTER.json").exists())
            self.assertFalse((project / "docs/operations/receipts").exists())
            self.assertEqual(
                before,
                _git(
                    project,
                    "status",
                    "--porcelain=v1",
                    "--untracked-files=all",
                ),
            )

    def test_stdin_receipt_mode_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory) / "project"
            source = _init_project(project)
            result = _run_gate(
                base_root=ROOT,
                project_root=project,
                project_source_sha=source,
                receipt="-",
            )
            self.assertNotEqual(0, result.returncode)
            self.assertIn("stdin receipt mode is not supported", result.stdout)

    def test_stale_project_source_and_wrong_base_identity_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            project = root / "project"
            source = _init_project(project)
            receipt = root / "receipt.json"
            receipt.write_text(
                json.dumps(_active_receipt("0" * 40)), encoding="utf-8"
            )

            stale = _run_gate(
                base_root=ROOT,
                project_root=project,
                project_source_sha=source,
                receipt=receipt,
            )
            self.assertNotEqual(0, stale.returncode)
            self.assertIn("source_main_sha", stale.stdout)

            receipt.write_text(
                json.dumps(_active_receipt(source)), encoding="utf-8"
            )
            current_head = _git(ROOT, "rev-parse", "HEAD")
            previous_head = _git(ROOT, "rev-parse", "HEAD^")
            wrong_base = _run_gate(
                base_root=ROOT,
                project_root=project,
                project_source_sha=source,
                receipt=receipt,
                entrypoint_commit_sha=current_head,
                expected_base_sha=previous_head,
            )
            self.assertNotEqual(0, wrong_base.returncode)
            self.assertIn("Base checkout HEAD does not match", wrong_base.stdout)

    def test_source_commit_must_exist_in_the_target_project(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            project = root / "project"
            source = _init_project(project)
            receipt = root / "receipt.json"
            receipt.write_text(
                json.dumps(_active_receipt(source)), encoding="utf-8"
            )
            result = _run_gate(
                base_root=ROOT,
                project_root=project,
                project_source_sha="e" * 40,
                receipt=receipt,
            )
            self.assertNotEqual(0, result.returncode)
            self.assertIn("project source commit is unavailable locally", result.stdout)

    def test_closeout_uses_an_independently_supplied_project_head(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            project = root / "project"
            source = _init_project(project)
            receipt = root / "receipt.json"
            receipt.write_text(
                json.dumps(_done_receipt(source, source)), encoding="utf-8"
            )

            passed = _run_gate(
                base_root=ROOT,
                project_root=project,
                project_source_sha=source,
                receipt=receipt,
                phase="closeout",
                verified_head_sha=source,
                render_markdown=True,
            )
            self.assertEqual(0, passed.returncode, passed.stdout + passed.stderr)
            self.assertIn("1 / 1", passed.stdout)

            (project / "next.txt").write_text("later\n", encoding="utf-8")
            _git(project, "add", "next.txt")
            _git(project, "commit", "-qm", "later subject")
            later = _git(project, "rev-parse", "HEAD")
            stale = _run_gate(
                base_root=ROOT,
                project_root=project,
                project_source_sha=source,
                receipt=receipt,
                phase="closeout",
                verified_head_sha=later,
                render_markdown=True,
            )
            self.assertNotEqual(0, stale.returncode)
            self.assertIn(
                "verified_head_sha does not match trusted expected head",
                stale.stdout,
            )
            self.assertNotIn("## PM 작업 체크리스트 — 1 / 1", stale.stdout)


if __name__ == "__main__":
    unittest.main()
