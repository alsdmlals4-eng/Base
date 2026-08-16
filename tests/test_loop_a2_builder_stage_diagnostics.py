from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from tools.loop_a2_runtime.protocol import RunRequest
from tools.loop_a2_runtime.worktree_adapter import GitWorktreeBuilderAdapter
from tests.test_loop_a2_protocol import valid_request


def _request() -> RunRequest:
    value = valid_request()
    value["provider_mode"] = "REAL"
    return RunRequest.from_dict(value)


def _assert_stage(testcase: unittest.TestCase, expected: str, callback) -> None:
    with testcase.assertRaises(Exception) as caught:
        callback()
    testcase.assertEqual(type(caught.exception).__name__, expected)
    testcase.assertNotIn("secret-stage-detail", str(caught.exception))


class _RaisingWorker:
    def invoke(self, request, *, worktree_path, repair_cycle):
        raise AttributeError("secret-stage-detail")


class _ReturningWorker:
    def __init__(self, value) -> None:
        self.value = value

    def invoke(self, request, *, worktree_path, repair_cycle):
        return self.value


class BuilderStageDiagnosticsTests(unittest.TestCase):
    def test_unexpected_workspace_preparation_exception_is_stage_tagged(self) -> None:
        adapter = object.__new__(GitWorktreeBuilderAdapter)
        adapter.worker = _ReturningWorker(object())
        with patch.object(
            adapter,
            "_ensure_workspace",
            side_effect=AttributeError("secret-stage-detail"),
        ):
            _assert_stage(
                self,
                "BuilderWorkspacePreparationError",
                lambda: adapter.invoke(_request(), repair_cycle=0),
            )

    def test_unexpected_worker_invocation_exception_is_stage_tagged(self) -> None:
        adapter = object.__new__(GitWorktreeBuilderAdapter)
        adapter.worker = _RaisingWorker()
        with (
            patch.object(adapter, "_ensure_workspace", return_value=None),
            patch.object(adapter, "workspace_path", return_value=Path(".")),
        ):
            _assert_stage(
                self,
                "BuilderWorkerInvocationError",
                lambda: adapter.invoke(_request(), repair_cycle=0),
            )

    def test_unexpected_diff_collection_exception_is_stage_tagged(self) -> None:
        adapter = object.__new__(GitWorktreeBuilderAdapter)
        adapter.worker = _ReturningWorker(SimpleNamespace(status="BLOCKED", changed_paths=()))
        with (
            patch.object(adapter, "_ensure_workspace", return_value=None),
            patch.object(adapter, "workspace_path", return_value=Path(".")),
            patch.object(
                adapter,
                "_actual_changed_paths",
                side_effect=AttributeError("secret-stage-detail"),
            ),
        ):
            _assert_stage(
                self,
                "BuilderDiffCollectionError",
                lambda: adapter.invoke(_request(), repair_cycle=0),
            )

    def test_unexpected_result_binding_exception_is_stage_tagged(self) -> None:
        adapter = object.__new__(GitWorktreeBuilderAdapter)
        adapter.worker = _ReturningWorker(object())
        with (
            patch.object(adapter, "_ensure_workspace", return_value=None),
            patch.object(adapter, "workspace_path", return_value=Path(".")),
            patch.object(adapter, "_actual_changed_paths", return_value=()),
        ):
            _assert_stage(
                self,
                "BuilderResultBindingError",
                lambda: adapter.invoke(_request(), repair_cycle=0),
            )


if __name__ == "__main__":
    unittest.main()
