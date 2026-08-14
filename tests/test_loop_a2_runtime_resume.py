from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from tests.test_loop_a2_runtime_worktree import WorktreeAdapterTests, run_git
from tools.loop_a2_runtime.protocol import RunRequest
from tools.loop_a2_runtime.workspace_registry import (
    WorkspaceOwnershipError,
    WorkspaceOwnershipRegistry,
)
from tests.test_loop_a2_protocol import valid_request


class DurableWorktreeResumeTests(WorktreeAdapterTests):
    def registry(self) -> WorkspaceOwnershipRegistry:
        return WorkspaceOwnershipRegistry(
            repo_root=self.repo,
            runtime_root=self.runtime,
        )

    def test_creation_publishes_integrity_checked_ownership_receipt(self) -> None:
        request = self.request()
        adapter = self.adapter(self.worker_script())
        try:
            result = adapter.invoke(request, repair_cycle=0)
            self.assertEqual(result.status, "COMPLETED")
            receipt = self.registry().read(request.project_id, request.run_id)
            self.assertEqual(receipt["contract_role"], "LOOP_A2_WORKSPACE_OWNERSHIP")
            self.assertEqual(receipt["project_id"], request.project_id)
            self.assertEqual(receipt["run_id"], request.run_id)
            self.assertEqual(receipt["expected_main_sha"], request.expected_main_sha)
            self.assertEqual(receipt["source_repo"], str(self.repo.resolve()))
            self.assertEqual(receipt["workspace"], str(adapter.workspace_path(request).resolve()))
            self.assertRegex(receipt["receipt_digest"], r"^[0-9a-f]{64}$")
        finally:
            adapter.close(request)

    def test_new_adapter_process_can_explicitly_resume_verified_owned_worktree(self) -> None:
        request = self.request()
        first = self.adapter(self.worker_script())
        result = first.invoke(request, repair_cycle=0)
        self.assertEqual(result.status, "COMPLETED")
        workspace = first.workspace_path(request)
        self.assertTrue(workspace.is_dir())

        second = self.adapter(self.worker_script())
        second.resume(request)
        repaired = second.invoke(request, repair_cycle=1)
        self.assertEqual(repaired.status, "COMPLETED")
        second.close(request)

        self.assertFalse(workspace.exists())
        self.assertFalse(self.registry().receipt_path(request.project_id, request.run_id).exists())

    def test_existing_registered_worktree_without_receipt_cannot_be_adopted(self) -> None:
        request = self.request()
        workspace = self.runtime / request.project_id / request.run_id
        workspace.parent.mkdir(parents=True)
        run_git(self.repo, "worktree", "add", "--detach", str(workspace), request.expected_main_sha)

        adapter = self.adapter(self.worker_script())
        with self.assertRaises(WorkspaceOwnershipError):
            adapter.resume(request)
        adapter.close(request)
        self.assertTrue(workspace.exists(), "unowned worktree must remain untouched")

    def test_tampered_ownership_receipt_fails_closed_and_is_not_cleaned(self) -> None:
        request = self.request()
        first = self.adapter(self.worker_script())
        first.invoke(request, repair_cycle=0)
        workspace = first.workspace_path(request)
        receipt_path = self.registry().receipt_path(request.project_id, request.run_id)
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
        receipt["expected_main_sha"] = "f" * 40
        receipt_path.write_text(json.dumps(receipt), encoding="utf-8")

        second = self.adapter(self.worker_script())
        with self.assertRaises(WorkspaceOwnershipError):
            second.resume(request)
        second.close(request)
        self.assertTrue(workspace.exists())
        self.assertTrue(receipt_path.exists())

        # The original in-memory owner may still clean the worktree, but a corrupt
        # ownership receipt must not be silently deleted by a restarted adapter.
        subprocess.run(
            ["git", "worktree", "remove", "--force", str(workspace)],
            cwd=self.repo,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_receipt_bound_to_wrong_source_repository_is_rejected(self) -> None:
        request = self.request()
        first = self.adapter(self.worker_script())
        first.invoke(request, repair_cycle=0)
        receipt_path = self.registry().receipt_path(request.project_id, request.run_id)
        value = json.loads(receipt_path.read_text(encoding="utf-8"))
        value.pop("receipt_digest", None)
        value["source_repo"] = str((self.root / "other-repo").resolve())
        from tools.loop_a2_runtime.evidence import canonical_receipt
        receipt_path.write_text(
            json.dumps(canonical_receipt(value), sort_keys=True, indent=2) + "\n",
            encoding="utf-8",
        )

        restarted = self.adapter(self.worker_script())
        with self.assertRaises(WorkspaceOwnershipError):
            restarted.resume(request)
        self.assertTrue(first.workspace_path(request).exists())
        first.close(request)

    def test_missing_git_registration_blocks_resume_even_with_valid_receipt(self) -> None:
        request = self.request()
        first = self.adapter(self.worker_script())
        first.invoke(request, repair_cycle=0)
        workspace = first.workspace_path(request)
        receipt_path = self.registry().receipt_path(request.project_id, request.run_id)
        self.assertTrue(receipt_path.exists())

        run_git(self.repo, "worktree", "remove", "--force", str(workspace))
        restarted = self.adapter(self.worker_script())
        with self.assertRaises(WorkspaceOwnershipError):
            restarted.resume(request)
        self.assertTrue(receipt_path.exists(), "failed resume must preserve forensic receipt")

    def test_wrong_request_identity_cannot_resume_another_runs_receipt(self) -> None:
        request = self.request()
        first = self.adapter(self.worker_script())
        first.invoke(request, repair_cycle=0)

        value = valid_request()
        value["expected_main_sha"] = request.expected_main_sha
        value["run_id"] = "RUN_999"
        value["allowed_paths"] = ["scripts/feature/a.gd"]
        wrong = RunRequest.from_dict(value)
        restarted = self.adapter(self.worker_script())
        with self.assertRaises(WorkspaceOwnershipError):
            restarted.resume(wrong)
        first.close(request)


if __name__ == "__main__":
    unittest.main()