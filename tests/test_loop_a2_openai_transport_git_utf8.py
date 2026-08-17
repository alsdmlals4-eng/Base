from __future__ import annotations

from pathlib import Path
import subprocess
import unittest
from unittest.mock import patch

import tools.loop_a2_runtime.openai_transport as transport
from tools.loop_a2_runtime.protocol import RunRequest


_SHA = "a" * 40
_KOREAN_PATH = "기획서/프로젝트_허브/ACTIVE_CONTEXT.md"


def _request() -> RunRequest:
    return RunRequest.from_dict(
        {
            "schema_version": 1,
            "contract_role": "LOOP_A2_RUN_REQUEST",
            "project_id": "BLACKSMITH",
            "run_id": "BS_A2_GIT_UTF8_TEST_001",
            "package_id": "BS_A2_BURNIN_TEST_ONLY_PKG_001",
            "expected_main_sha": _SHA,
            "capsule_path": "docs/operations/loop/PROJECT_EXECUTION_CAPSULE.json",
            "package_path": "docs/operations/loop/IMPLEMENTATION_PACKAGE.json",
            "allowed_paths": [_KOREAN_PATH],
            "forbidden_paths": ["data/"],
            "resource_locks": ["UNIVERSAL_LOOP_OPERATIONS"],
            "requirement_ids": ["BS_A2_BURNIN_TEST_ONLY_001"],
            "budgets": {
                "max_turns": 4,
                "max_repair_cycles": 2,
                "timeout_seconds": 600,
            },
            "provider_mode": "REAL",
        }
    )


class OpenAITransportGitUtf8Tests(unittest.TestCase):
    def test_tracked_context_inventory_uses_explicit_strict_utf8_git_capture(self) -> None:
        observed: dict[str, object] = {}

        def windows_locale_sensitive_run(argv, **kwargs):
            observed.update(kwargs)
            if kwargs.get("encoding") != "utf-8":
                raise UnicodeDecodeError(
                    "cp949",
                    _KOREAN_PATH.encode("utf-8"),
                    0,
                    1,
                    "simulated Korean Windows locale decode failure",
                )
            if kwargs.get("errors") != "strict":
                raise AssertionError("Git path capture must fail closed on invalid UTF-8")
            return subprocess.CompletedProcess(
                list(argv),
                0,
                stdout=_KOREAN_PATH + "\0",
                stderr="",
            )

        with patch.object(transport.subprocess, "run", side_effect=windows_locale_sensitive_run):
            selected = transport._tracked_allowed_context(Path("."), _request())

        self.assertEqual(selected, (_KOREAN_PATH,))
        self.assertTrue(observed.get("text"))
        self.assertTrue(observed.get("capture_output"))
        self.assertFalse(observed.get("shell", False))
        self.assertFalse(observed.get("check"))


if __name__ == "__main__":
    unittest.main()
