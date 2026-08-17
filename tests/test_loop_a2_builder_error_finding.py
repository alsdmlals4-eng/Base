from __future__ import annotations

import unittest

from tools.loop_a2_runtime.protocol import RunRequest, WorkerResult
from tools.loop_a2_runtime.runner import A2Runtime


_SHA = "a" * 40
_SENSITIVE_MESSAGE = "private provider detail: C:/Users/example/secret/path"


def _request() -> RunRequest:
    return RunRequest.from_dict(
        {
            "schema_version": 1,
            "contract_role": "LOOP_A2_RUN_REQUEST",
            "project_id": "BLACKSMITH",
            "run_id": "BS_A2_DIAG_20260817_001",
            "package_id": "BS_A2_BURNIN_TEST_ONLY_PKG_001",
            "expected_main_sha": _SHA,
            "capsule_path": "docs/operations/loop/PROJECT_EXECUTION_CAPSULE.json",
            "package_path": "docs/operations/loop/IMPLEMENTATION_PACKAGE.json",
            "allowed_paths": ["docs/operations/loop/burnin/BS_A2_BURNIN_MARKER.txt"],
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


def _blocked_worker() -> WorkerResult:
    return WorkerResult.from_dict(
        {
            "schema_version": 1,
            "contract_role": "LOOP_A2_WORKER_RESULT",
            "project_id": "BLACKSMITH",
            "run_id": "BS_A2_DIAG_20260817_001",
            "package_id": "BS_A2_BURNIN_TEST_ONLY_PKG_001",
            "expected_main_sha": _SHA,
            "role": "BUILDER",
            "status": "BLOCKED",
            "changed_paths": [],
            "summary": "Builder stopped before a candidate was completed.",
            "usage": {"turns": 1},
            "errors": [
                {
                    "code": "BUILDER_PROVIDER_PROTOCOL_INVALID",
                    "message": _SENSITIVE_MESSAGE,
                }
            ],
        }
    )


class BuilderErrorFindingTests(unittest.TestCase):
    def test_blocked_builder_preserves_safe_error_code_before_generic_finding(self) -> None:
        runtime = A2Runtime(builder=object(), critic=object(), provider_mode="REAL")

        outcome = runtime._validate_worker_before_review(
            _request(),
            _blocked_worker(),
            cumulative_turns=1,
        )

        self.assertIsNotNone(outcome)
        assert outcome is not None
        self.assertEqual(outcome.state, "PROVIDER_FAILURE")
        self.assertEqual(
            outcome.finding_codes,
            ("BUILDER_PROVIDER_PROTOCOL_INVALID", "BUILDER_NOT_COMPLETED"),
        )
        self.assertNotIn(_SENSITIVE_MESSAGE, str(outcome.evidence))
        self.assertNotIn("secret/path", str(outcome.evidence))


if __name__ == "__main__":
    unittest.main()
