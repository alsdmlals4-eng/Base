from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from tests.test_loop_a2_runtime_resume import DurableWorktreeResumeTests
from tools.loop_a2_runtime.workspace_registry import (
    WorkspaceOwnershipError,
    WorkspaceOwnershipRegistry,
)


class DurableWorktreeResumeAdversarialTests(DurableWorktreeResumeTests):
    def test_project_namespace_symlink_cannot_escape_runtime_root_before_git_mutation(self) -> None:
        request = self.request()
        outside = self.root / "outside-workspaces"
        outside.mkdir()
        self.runtime.mkdir()
        namespace = self.runtime / request.project_id
        try:
            namespace.symlink_to(outside, target_is_directory=True)
        except (OSError, NotImplementedError):
            self.skipTest("directory symlinks are unavailable")

        adapter = self.adapter(self.worker_script())
        result = adapter.invoke(request, repair_cycle=0)

        self.assertEqual(result.status, "BLOCKED")
        self.assertEqual(result.errors[0].code, "WORKSPACE_PATH_UNSAFE")
        self.assertFalse((outside / request.run_id).exists())
        self.assertFalse(self.registry().receipt_path(request.project_id, request.run_id).exists())

    def test_symlinked_ownership_registry_blocks_before_worktree_creation(self) -> None:
        request = self.request()
        outside = self.root / "outside-receipts"
        outside.mkdir()
        self.runtime.mkdir()
        link = self.runtime / ".loop-ownership"
        try:
            link.symlink_to(outside, target_is_directory=True)
        except (OSError, NotImplementedError):
            self.skipTest("directory symlinks are unavailable")

        adapter = self.adapter(self.worker_script())
        result = adapter.invoke(request, repair_cycle=0)

        self.assertEqual(result.status, "BLOCKED")
        self.assertEqual(result.errors[0].code, "WORKSPACE_OWNERSHIP_FAILED")
        self.assertFalse(adapter.workspace_path(request).exists())
        self.assertEqual(list(outside.iterdir()), [])

    def test_stale_ownership_receipt_blocks_before_recreating_missing_worktree(self) -> None:
        request = self.request()
        registry = self.registry()
        workspace = self.runtime / request.project_id / request.run_id
        registry.claim(
            project_id=request.project_id,
            run_id=request.run_id,
            expected_main_sha=request.expected_main_sha,
            workspace=workspace,
        )
        self.assertFalse(workspace.exists())

        adapter = self.adapter(self.worker_script())
        result = adapter.invoke(request, repair_cycle=0)

        self.assertEqual(result.status, "BLOCKED")
        self.assertEqual(result.errors[0].code, "WORKSPACE_OWNERSHIP_FAILED")
        self.assertFalse(workspace.exists())
        self.assertTrue(registry.receipt_path(request.project_id, request.run_id).exists())

    def test_unknown_ownership_receipt_fields_are_rejected(self) -> None:
        request = self.request()
        first = self.adapter(self.worker_script())
        first.invoke(request, repair_cycle=0)
        receipt_path = self.registry().receipt_path(request.project_id, request.run_id)
        value = json.loads(receipt_path.read_text(encoding="utf-8"))
        value.pop("receipt_digest")
        value["unexpected"] = "authority-expansion"
        from tools.loop_a2_runtime.evidence import canonical_receipt
        receipt_path.write_text(
            json.dumps(canonical_receipt(value), sort_keys=True, indent=2) + "\n",
            encoding="utf-8",
        )

        restarted = self.adapter(self.worker_script())
        with self.assertRaises(WorkspaceOwnershipError):
            restarted.resume(request)
        self.assertTrue(first.workspace_path(request).exists())


if __name__ == "__main__":
    unittest.main()
