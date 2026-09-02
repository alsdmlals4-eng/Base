from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools/run_project_work_gate.py"
OWNER = ROOT / "docs/operations/BASE_CURRENT_PROJECT_WORK_BOOTSTRAP.md"
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


def _run(*argv: str, cwd: Path | None = None, input_text: str | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        list(argv),
        cwd=cwd,
        input=input_text,
        text=True,
        capture_output=True,
        check=False,
        timeout=60,
    )


def _git(root: Path, *args: str, check: bool = True) -> str:
    result = _run("git", "-C", str(root), *args)
    if check and result.returncode != 0:
        raise AssertionError(result.stdout + result.stderr)
    return result.stdout.strip()


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


def _active_receipt(source_sha: str) -> dict:
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
                        {"level": "E2_TEST", "status": "NOT_RUN", "evidence": []}
                    ],
                    "next_action": "run the focused bootstrap behavior test",
                }
            ],
        },
    }


def _done_receipt(source_sha: str, verified_head_sha: str) -> dict:
    value = _active_receipt(source_sha)
    board = value["project_work_kanban"]
    board["active_work_item_ref"] = None
    board["next_action"] = "STOP_APPROVED_SCOPE_COMPLETE"
    task = board["work_items"][0]
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
    task["checklist"][0].update(status="PASS", evidence=["focused bootstrap test"])
    task["verification"][0].update(status="PASS", evidence=["focused bootstrap test"])
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
        ):
            self.assertIn(token, text)

    def test_active_consumers_route_to_the_base_current_owner(self) -> None:
        for path in DIRECT_CONSUMERS:
            text = path.read_text(encoding="utf-8")
            with self.subTest(path=path.relative_to(ROOT).as_posix()):
                self.assertIn("BASE_CURRENT_OPERATIONAL_BOOTSTRAP", text)
                self.assertIn("BASE_CURRENT_PROJECT_WORK_BOOTSTRAP.md", text)

    def test_project_can_start_without_adapter_or_project_receipt_file(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            project = root / "project"
            source = _init_project(project)
            external_receipt = root / "ephemeral-receipt.json"
            external_receipt.write_text(json.dumps(_active_receipt(source)), encoding="utf-8")
            before = _git(project, "status", "--porcelain=v1", "--untracked-files=all")
            base_head = _git(ROOT, "rev-parse", "HEAD")

            result = _run(
                sys.executable,
                "-P",
                str(TOOL),
                "--expected-base-sha",
                base_head,
                "--project-root",
                str(project),
                "--project-source-sha",
                source,
                "--receipt",
                str(external_receipt),
                "--phase",
                "start",
                "--render-markdown",
            )

            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            self.assertIn("BASE CURRENT PROJECT WORK BOOTSTRAP: PASS", result.stdout)
            self.assertIn("BOOT-01", result.stdout)
            self.assertIn("ACTIVE", result.stdout)
            self.assertFalse((project / "skills/PROJECT_BASE_ADAPTER.json").exists())
            self.assertFalse((project / "docs/operations/receipts").exists())
            self.assertEqual(before, _git(project, "status", "--porcelain=v1", "--untracked-files=all"))

    def test_ephemeral_receipt_can_be_read_from_stdin(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory) / "project"
            source = _init_project(project)
            result = _run(
                sys.executable,
                "-P",
                str(TOOL),
                "--expected-base-sha",
                _git(ROOT, "rev-parse", "HEAD"),
                "--project-root",
                str(project),
                "--project-source-sha",
                source,
                "--receipt",
                "-",
                "--phase",
                "start",
                "--render-markdown",
                input_text=json.dumps(_active_receipt(source)),
            )
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            self.assertIn("receipt_source=stdin", result.stdout)

    def test_stale_project_source_and_wrong_base_identity_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            project = root / "project"
            source = _init_project(project)
            receipt = root / "receipt.json"
            receipt.write_text(json.dumps(_active_receipt("0" * 40)), encoding="utf-8")
            common = (
                sys.executable,
                "-P",
                str(TOOL),
                "--project-root",
                str(project),
                "--project-source-sha",
                source,
                "--receipt",
                str(receipt),
            )

            stale = _run(*common, "--expected-base-sha", _git(ROOT, "rev-parse", "HEAD"))
            self.assertNotEqual(0, stale.returncode)
            self.assertIn("source_main_sha", stale.stdout)

            wrong_base = _run(*common, "--expected-base-sha", "f" * 40)
            self.assertNotEqual(0, wrong_base.returncode)
            self.assertIn("Base checkout HEAD does not match", wrong_base.stdout)

    def test_source_commit_must_exist_in_the_target_project(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            project = root / "project"
            source = _init_project(project)
            receipt = root / "receipt.json"
            receipt.write_text(json.dumps(_active_receipt(source)), encoding="utf-8")
            result = _run(
                sys.executable,
                "-P",
                str(TOOL),
                "--expected-base-sha",
                _git(ROOT, "rev-parse", "HEAD"),
                "--project-root",
                str(project),
                "--project-source-sha",
                "e" * 40,
                "--receipt",
                str(receipt),
            )
            self.assertNotEqual(0, result.returncode)
            self.assertIn("project source commit is unavailable", result.stdout)

    def test_closeout_uses_an_independently_supplied_project_head(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            project = root / "project"
            source = _init_project(project)
            receipt = root / "receipt.json"
            receipt.write_text(json.dumps(_done_receipt(source, source)), encoding="utf-8")
            common = (
                sys.executable,
                "-P",
                str(TOOL),
                "--expected-base-sha",
                _git(ROOT, "rev-parse", "HEAD"),
                "--project-root",
                str(project),
                "--project-source-sha",
                source,
                "--receipt",
                str(receipt),
                "--phase",
                "closeout",
                "--render-markdown",
            )

            passed = _run(*common, "--verified-head-sha", source)
            self.assertEqual(0, passed.returncode, passed.stdout + passed.stderr)
            self.assertIn("1 / 1", passed.stdout)

            (project / "next.txt").write_text("later\n", encoding="utf-8")
            _git(project, "add", "next.txt")
            _git(project, "commit", "-qm", "later subject")
            later = _git(project, "rev-parse", "HEAD")
            stale = _run(*common, "--verified-head-sha", later)
            self.assertNotEqual(0, stale.returncode)
            self.assertIn("verified_head_sha does not match trusted expected head", stale.stdout)
            self.assertNotIn("## PM 작업 체크리스트 — 1 / 1", stale.stdout)


if __name__ == "__main__":
    unittest.main()
