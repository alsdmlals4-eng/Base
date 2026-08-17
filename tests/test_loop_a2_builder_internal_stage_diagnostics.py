from __future__ import annotations

import tempfile
import unittest
from unittest.mock import patch

import tools.loop_a2_runtime.openai_transport as transport
from tests.test_loop_a2_openai_transport import _Client, _repo_and_request


_SECRET = "secret-builder-internal-detail"


class _RaisingMailbox:
    def read(self, request, *, repair_cycle):
        raise AttributeError(_SECRET)


class _BadPath:
    def __fspath__(self):
        raise AttributeError(_SECRET)


def _assert_blocked_code(
    testcase: unittest.TestCase,
    result,
    expected_code: str,
) -> None:
    testcase.assertEqual(result.status, "BLOCKED")
    testcase.assertEqual(result.errors[0].code, expected_code)
    testcase.assertNotIn(_SECRET, str(result))


class BuilderInternalStageDiagnosticsTests(unittest.TestCase):
    def test_unexpected_worktree_resolution_exception_becomes_bounded_worker_code(self) -> None:
        builder = transport.OpenAIWorkspaceBuilder(
            client=_Client({"status": "BLOCKED", "summary": "unused", "writes": [], "blocked_reason": "unused"}),
            model="builder-model",
        )
        with tempfile.TemporaryDirectory() as tmp:
            _, request = _repo_and_request(tmp)
            result = builder.invoke(request, worktree_path=_BadPath(), repair_cycle=0)
        _assert_blocked_code(self, result, "BUILDER_WORKTREE_PREPARATION_EXCEPTION")

    def test_unexpected_context_preparation_exception_becomes_bounded_worker_code(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root, request = _repo_and_request(tmp)
            client = _Client({"status": "BLOCKED", "summary": "unused", "writes": [], "blocked_reason": "unused"})
            builder = transport.OpenAIWorkspaceBuilder(client=client, model="builder-model")
            with patch.object(transport, "_collect_context", side_effect=AttributeError(_SECRET)):
                result = builder.invoke(request, worktree_path=root, repair_cycle=0)
        _assert_blocked_code(self, result, "BUILDER_CONTEXT_PREPARATION_EXCEPTION")
        self.assertEqual(client.responses.calls, [])

    def test_unexpected_repair_feedback_exception_becomes_bounded_worker_code(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root, request = _repo_and_request(tmp)
            client = _Client({"status": "BLOCKED", "summary": "unused", "writes": [], "blocked_reason": "unused"})
            builder = transport.OpenAIWorkspaceBuilder(
                client=client,
                model="builder-model",
                repair_mailbox=_RaisingMailbox(),
            )
            result = builder.invoke(request, worktree_path=root, repair_cycle=1)
        _assert_blocked_code(self, result, "BUILDER_REPAIR_FEEDBACK_EXCEPTION")
        self.assertEqual(client.responses.calls, [])

    def test_unexpected_write_plan_validation_exception_becomes_bounded_worker_code(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root, request = _repo_and_request(tmp)
            client = _Client(
                {
                    "status": "COMPLETED",
                    "summary": "candidate",
                    "writes": [{"path": "scripts/feature/new.gd", "content": "extends Node\n"}],
                    "blocked_reason": "",
                }
            )
            builder = transport.OpenAIWorkspaceBuilder(client=client, model="builder-model")
            with patch.object(builder, "_validate_write_plan", side_effect=AttributeError(_SECRET)):
                result = builder.invoke(request, worktree_path=root, repair_cycle=0)
        _assert_blocked_code(self, result, "BUILDER_WRITE_PLAN_VALIDATION_EXCEPTION")

    def test_unexpected_final_worker_result_construction_becomes_bounded_worker_code(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root, request = _repo_and_request(tmp)
            client = _Client(
                {
                    "status": "COMPLETED",
                    "summary": "candidate",
                    "writes": [{"path": "scripts/feature/new.gd", "content": "extends Node\n"}],
                    "blocked_reason": "",
                }
            )
            builder = transport.OpenAIWorkspaceBuilder(client=client, model="builder-model")
            original = transport.WorkerResult.from_dict

            def fail_only_completed(value):
                if isinstance(value, dict) and value.get("status") == "COMPLETED":
                    raise AttributeError(_SECRET)
                return original(value)

            with patch.object(transport.WorkerResult, "from_dict", side_effect=fail_only_completed):
                result = builder.invoke(request, worktree_path=root, repair_cycle=0)
        _assert_blocked_code(self, result, "BUILDER_RESULT_CONSTRUCTION_EXCEPTION")


if __name__ == "__main__":
    unittest.main()
