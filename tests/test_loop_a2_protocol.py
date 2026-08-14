from __future__ import annotations

import unittest

from tools.loop_a2_runtime.protocol import (
    ProtocolError,
    RunRequest,
    WorkerResult,
    ReviewResult,
)


def valid_request() -> dict[str, object]:
    return {
        "schema_version": 1,
        "contract_role": "LOOP_A2_RUN_REQUEST",
        "project_id": "BLACKSMITH",
        "run_id": "RUN_001",
        "package_id": "PACKAGE_001",
        "expected_main_sha": "0123456789abcdef0123456789abcdef01234567",
        "capsule_path": "docs/operations/loop/PROJECT_EXECUTION_CAPSULE.json",
        "package_path": "docs/operations/loop/IMPLEMENTATION_PACKAGE.json",
        "allowed_paths": ["scripts/feature/**", "tests/**"],
        "forbidden_paths": ["project.godot", ".github/**"],
        "resource_locks": ["SAVE_SCHEMA"],
        "requirement_ids": ["REQ_001"],
        "budgets": {
            "max_turns": 12,
            "max_repair_cycles": 2,
            "timeout_seconds": 600,
        },
        "provider_mode": "FAKE",
    }


class ProtocolTests(unittest.TestCase):
    def test_request_rejects_unknown_authority_field(self) -> None:
        with self.assertRaises(ProtocolError):
            RunRequest.from_dict(valid_request() | {"merge": True})

    def test_request_rejects_cross_platform_parent_paths(self) -> None:
        for unsafe in ("../OTHER/**", "..\\OTHER\\**", "C:\\OTHER\\**", "/tmp/OTHER/**"):
            value = valid_request()
            value["allowed_paths"] = [unsafe]
            with self.subTest(unsafe=unsafe), self.assertRaises(ProtocolError):
                RunRequest.from_dict(value)

    def test_request_is_frozen_and_exact(self) -> None:
        request = RunRequest.from_dict(valid_request())
        self.assertEqual(request.project_id, "BLACKSMITH")
        self.assertEqual(request.budgets.max_turns, 12)

    def test_worker_and_review_reject_hidden_reasoning_fields(self) -> None:
        worker = {
            "schema_version": 1,
            "contract_role": "LOOP_A2_WORKER_RESULT",
            "project_id": "BLACKSMITH",
            "run_id": "RUN_001",
            "package_id": "PACKAGE_001",
            "expected_main_sha": "0123456789abcdef0123456789abcdef01234567",
            "role": "BUILDER",
            "status": "COMPLETED",
            "changed_paths": ["scripts/feature/a.gd"],
            "summary": "Completed; deterministic verification required.",
            "usage": {"turns": 1},
            "errors": [],
        }
        review = {
            "schema_version": 1,
            "contract_role": "LOOP_A2_REVIEW_RESULT",
            "project_id": "BLACKSMITH",
            "run_id": "RUN_001",
            "package_id": "PACKAGE_001",
            "expected_main_sha": "0123456789abcdef0123456789abcdef01234567",
            "role": "CRITIC",
            "verdict": "PASS",
            "findings": [],
            "checked_requirement_ids": ["REQ_001"],
        }
        WorkerResult.from_dict(worker)
        ReviewResult.from_dict(review)
        with self.assertRaises(ProtocolError):
            WorkerResult.from_dict(worker | {"chain_of_thought": "secret"})
        with self.assertRaises(ProtocolError):
            ReviewResult.from_dict(review | {"reasoning": "secret"})

    def test_worker_usage_turns_are_bounded(self) -> None:
        worker = {
            "schema_version": 1,
            "contract_role": "LOOP_A2_WORKER_RESULT",
            "project_id": "BLACKSMITH",
            "run_id": "RUN_001",
            "package_id": "PACKAGE_001",
            "expected_main_sha": "0123456789abcdef0123456789abcdef01234567",
            "role": "BUILDER",
            "status": "COMPLETED",
            "changed_paths": ["scripts/feature/a.gd"],
            "summary": "too many turns",
            "usage": {"turns": 51},
            "errors": [],
        }
        with self.assertRaises(ProtocolError):
            WorkerResult.from_dict(worker)


if __name__ == "__main__":
    unittest.main()
