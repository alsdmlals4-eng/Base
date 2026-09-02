from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
import stat
import tempfile
import unittest

from tools.run_project_work_gate import REQUIRED_BASE_CLOSURE
from tests.test_base_current_project_work_bootstrap import (
    GIT,
    ROOT,
    _active_receipt,
    _done_receipt,
    _git,
    _init_project,
    _run_gate,
)


class BaseCurrentProjectWorkBootstrapSecurityTests(unittest.TestCase):
    def _init_base_snapshot(self, root: Path) -> str:
        root.mkdir()
        for relative in REQUIRED_BASE_CLOSURE:
            source = ROOT / relative
            destination = root / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)
        for args in (
            ("init", "-q"),
            ("config", "user.email", "bootstrap-security@example.invalid"),
            ("config", "user.name", "bootstrap security"),
            ("add", "."),
            ("commit", "-qm", "trusted Base operational closure"),
        ):
            _git(root, *args)
        return _git(root, "rev-parse", "HEAD")

    def test_receipt_path_must_be_a_regular_file(self) -> None:
        if not hasattr(os, "mkfifo"):
            self.skipTest("named pipes are unavailable on this platform")

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            project = root / "project"
            source = _init_project(project)
            fifo = root / "receipt.pipe"
            os.mkfifo(fifo)

            result = _run_gate(
                base_root=ROOT,
                project_root=project,
                project_source_sha=source,
                receipt=fifo,
            )

            self.assertNotEqual(0, result.returncode, result.stdout + result.stderr)
            self.assertIn("regular file", result.stdout)

    def test_git_replace_cannot_substitute_the_trusted_base_commit(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            base = root / "base"
            project = root / "project"
            trusted = self._init_base_snapshot(base)

            _git(base, "checkout", "-qb", "replacement")
            replacement_tool = base / "tools/run_project_work_gate.py"
            replacement_tool.write_text(
                replacement_tool.read_text(encoding="utf-8")
                + "\n# replacement-object attack fixture\n",
                encoding="utf-8",
            )
            _git(base, "add", "tools/run_project_work_gate.py")
            _git(base, "commit", "-qm", "replacement snapshot")
            replacement = _git(base, "rev-parse", "HEAD")
            replacement_bytes = bytes.fromhex("") if False else None
            replacement_bytes = (
                __import__(
                    "tests.test_base_current_project_work_bootstrap",
                    fromlist=["_commit_blob"],
                )._commit_blob(
                    base, replacement, "tools/run_project_work_gate.py"
                )
            )

            _git(base, "checkout", "-q", "--detach", trusted)
            _git(base, "replace", trusted, replacement)
            replacement_tool.write_bytes(replacement_bytes)

            source = _init_project(project)
            receipt = root / "receipt.json"
            receipt.write_text(
                json.dumps(_active_receipt(source)), encoding="utf-8"
            )
            result = _run_gate(
                base_root=base,
                project_root=project,
                project_source_sha=source,
                receipt=receipt,
                expected_base_sha=trusted,
                entrypoint_commit_sha=trusted,
            )

            self.assertNotEqual(0, result.returncode, result.stdout + result.stderr)
            self.assertIn(
                "Base operational authority bytes differ", result.stdout
            )

    def test_target_project_path_cannot_hijack_git(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            project = root / "project"
            source = _init_project(project)
            receipt = root / "receipt.json"
            receipt.write_text(
                json.dumps(_active_receipt(source)), encoding="utf-8"
            )
            fake_bin = project / "hostile-bin"
            fake_bin.mkdir()
            marker = root / "fake-git-ran"
            if os.name == "nt":
                fake_git = fake_bin / "git.cmd"
                fake_git.write_text(
                    f"@echo off\r\necho used>{marker}\r\nexit /b 91\r\n",
                    encoding="utf-8",
                )
            else:
                fake_git = fake_bin / "git"
                fake_git.write_text(
                    f"#!/bin/sh\necho used > {str(marker)!r}\nexit 91\n",
                    encoding="utf-8",
                )
                fake_git.chmod(
                    fake_git.stat().st_mode
                    | stat.S_IXUSR
                    | stat.S_IXGRP
                    | stat.S_IXOTH
                )
            environment = dict(os.environ)
            environment["PATH"] = os.pathsep.join(
                (str(fake_bin), environment.get("PATH", ""))
            )

            result = _run_gate(
                base_root=ROOT,
                project_root=project,
                project_source_sha=source,
                receipt=receipt,
                environment=environment,
            )

            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            self.assertFalse(marker.exists())

    def test_every_operational_authority_file_is_bound_to_expected_base_commit(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            base = root / "base"
            project = root / "project"
            trusted = self._init_base_snapshot(base)
            (base / "AGENTS.md").write_text(
                "# modified authority\n", encoding="utf-8"
            )
            source = _init_project(project)
            receipt = root / "receipt.json"
            receipt.write_text(
                json.dumps(_active_receipt(source)), encoding="utf-8"
            )

            result = _run_gate(
                base_root=base,
                project_root=project,
                project_source_sha=source,
                receipt=receipt,
                expected_base_sha=trusted,
                entrypoint_commit_sha=trusted,
            )

            self.assertNotEqual(0, result.returncode)
            self.assertIn("AGENTS.md", result.stdout)
            self.assertIn(
                "operational authority bytes differ", result.stdout
            )

    def test_project_identity_object_itself_must_be_a_commit(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            project = root / "project"
            source = _init_project(project)
            _git(project, "tag", "-a", "subject-tag", "-m", "annotated tag")
            tag_object = _git(project, "rev-parse", "subject-tag^{tag}")
            receipt = root / "receipt.json"
            receipt.write_text(
                json.dumps(_active_receipt(tag_object)), encoding="utf-8"
            )

            result = _run_gate(
                base_root=ROOT,
                project_root=project,
                project_source_sha=tag_object,
                receipt=receipt,
            )

            self.assertNotEqual(0, result.returncode)
            self.assertIn("object type must be commit", result.stdout)
            self.assertIn("not tag", result.stdout)
            self.assertNotEqual(source, tag_object)

    def test_closeout_subject_must_descend_from_the_work_source(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            project = root / "project"
            source = _init_project(project)
            tree = _git(project, "write-tree")
            orphan = _git(project, "commit-tree", tree, "-m", "orphan subject")
            receipt = root / "receipt.json"
            receipt.write_text(
                json.dumps(_done_receipt(source, orphan)), encoding="utf-8"
            )

            result = _run_gate(
                base_root=ROOT,
                project_root=project,
                project_source_sha=source,
                receipt=receipt,
                phase="closeout",
                verified_head_sha=orphan,
            )

            self.assertNotEqual(0, result.returncode)
            self.assertIn("must be an ancestor", result.stdout)

    def test_strict_json_rejects_nonfinite_constants_and_duplicate_keys(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            project = root / "project"
            source = _init_project(project)
            receipt = root / "receipt.json"

            receipt.write_text('{"value":NaN}\n', encoding="utf-8")
            nonfinite = _run_gate(
                base_root=ROOT,
                project_root=project,
                project_source_sha=source,
                receipt=receipt,
            )
            self.assertNotEqual(0, nonfinite.returncode)
            self.assertIn("unsupported constant: NaN", nonfinite.stdout)

            receipt.write_text('{"value":1,"value":2}\n', encoding="utf-8")
            duplicate = _run_gate(
                base_root=ROOT,
                project_root=project,
                project_source_sha=source,
                receipt=receipt,
            )
            self.assertNotEqual(0, duplicate.returncode)
            self.assertIn("duplicate key: value", duplicate.stdout)

    def test_receipt_identity_output_escapes_control_characters(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            project = root / "project"
            source = _init_project(project)
            receipt = root / "receipt\nINJECTED=PASS.json"
            receipt.write_text(
                json.dumps(_active_receipt("0" * 40)), encoding="utf-8"
            )

            result = _run_gate(
                base_root=ROOT,
                project_root=project,
                project_source_sha=source,
                receipt=receipt,
            )

            self.assertNotEqual(0, result.returncode)
            self.assertNotIn("\nINJECTED=PASS", result.stdout)
            self.assertIn("\\nINJECTED=PASS", result.stdout)

    def test_entrypoint_digest_must_match_expected_commit_bytes(self) -> None:
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
                project_source_sha=source,
                receipt=receipt,
                entrypoint_digest="0" * 64,
            )

            self.assertNotEqual(0, result.returncode)
            self.assertIn("trusted entrypoint hash", result.stdout)


if __name__ == "__main__":
    unittest.main()
