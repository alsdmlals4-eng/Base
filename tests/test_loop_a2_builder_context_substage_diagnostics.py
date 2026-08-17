from __future__ import annotations

import tempfile
import unittest
from unittest.mock import patch

import tools.loop_a2_runtime.openai_transport as transport
from tests.test_loop_a2_openai_transport import _Client, _repo_and_request


_SECRET = "private-context-substage-detail"


def _builder():
    return transport.OpenAIWorkspaceBuilder(
        client=_Client(
            {
                "status": "BLOCKED",
                "summary": "unused",
                "writes": [],
                "blocked_reason": "unused",
            }
        ),
        model="builder-model",
    )


def _assert_blocked_code(testcase: unittest.TestCase, result, expected_code: str) -> None:
    testcase.assertEqual(result.status, "BLOCKED")
    testcase.assertEqual(result.errors[0].code, expected_code)
    testcase.assertNotIn(_SECRET, str(result))


class BuilderContextSubstageDiagnosticsTests(unittest.TestCase):
    def test_unexpected_authority_path_resolution_exception_is_localized(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root, request = _repo_and_request(tmp)
            builder = _builder()
            with patch.object(
                transport,
                "_effective_authority_paths",
                side_effect=AttributeError(_SECRET),
            ):
                result = builder.invoke(request, worktree_path=root, repair_cycle=0)
        _assert_blocked_code(
            self,
            result,
            "BUILDER_AUTHORITY_PATH_RESOLUTION_EXCEPTION",
        )

    def test_unexpected_authority_context_binding_exception_is_localized(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root, request = _repo_and_request(tmp)
            builder = _builder()
            with patch.object(
                transport,
                "_redact_prompt_text",
                side_effect=AttributeError(_SECRET),
            ):
                result = builder.invoke(request, worktree_path=root, repair_cycle=0)
        _assert_blocked_code(
            self,
            result,
            "BUILDER_AUTHORITY_CONTEXT_BINDING_EXCEPTION",
        )

    def test_unexpected_tracked_context_inventory_exception_is_localized(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root, request = _repo_and_request(tmp)
            builder = _builder()
            with patch.object(
                transport,
                "_tracked_allowed_context",
                side_effect=AttributeError(_SECRET),
            ):
                result = builder.invoke(request, worktree_path=root, repair_cycle=0)
        _assert_blocked_code(
            self,
            result,
            "BUILDER_TRACKED_CONTEXT_INVENTORY_EXCEPTION",
        )

    def test_unexpected_tracked_context_read_exception_is_localized(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root, request = _repo_and_request(tmp)
            builder = _builder()
            original_read = transport._read_utf8

            def fail_tracked(path, *, label):
                if label == "scripts/feature/existing.gd":
                    raise AttributeError(_SECRET)
                return original_read(path, label=label)

            with patch.object(transport, "_read_utf8", side_effect=fail_tracked):
                result = builder.invoke(request, worktree_path=root, repair_cycle=0)
        _assert_blocked_code(
            self,
            result,
            "BUILDER_TRACKED_CONTEXT_READ_EXCEPTION",
        )

    def test_unexpected_final_immutable_authority_path_exception_is_localized(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root, request = _repo_and_request(tmp)
            builder = _builder()
            original = transport._effective_authority_paths
            calls = 0

            def fail_second(*args, **kwargs):
                nonlocal calls
                calls += 1
                if calls == 2:
                    raise AttributeError(_SECRET)
                return original(*args, **kwargs)

            with patch.object(
                transport,
                "_effective_authority_paths",
                side_effect=fail_second,
            ):
                result = builder.invoke(request, worktree_path=root, repair_cycle=0)
        _assert_blocked_code(
            self,
            result,
            "BUILDER_IMMUTABLE_AUTHORITY_PATHS_EXCEPTION",
        )


if __name__ == "__main__":
    unittest.main()
