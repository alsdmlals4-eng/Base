from __future__ import annotations

import json
import unittest

from tools.loop_a2_runtime.candidate_verification import VerificationEvidenceMailbox
from tools.loop_a2_runtime.codex_cli_transport import (
    CodexCliTransportError,
    VerificationBoundCodexResponsesClient,
    VerificationBoundCritic,
)
from tools.loop_a2_runtime.protocol import ReviewResult, RunRequest, WorkerResult
from tools.loop_a2_runtime.test_executor import CommandEvidence, TestSuiteResult


def _request(run_id: str = "RUN_CRITIC_TEST_001") -> RunRequest:
    return RunRequest.from_dict(
        {
            "schema_version": 1,
            "contract_role": "LOOP_A2_RUN_REQUEST",
            "project_id": "TEST_GAME",
            "run_id": run_id,
            "package_id": "PACKAGE_001",
            "expected_main_sha": "a" * 40,
            "capsule_path": "docs/operations/loop/PROJECT_EXECUTION_CAPSULE.json",
            "package_path": "docs/operations/loop/IMPLEMENTATION_PACKAGE.json",
            "allowed_paths": ["scripts/feature/a.gd"],
            "forbidden_paths": [".github/**"],
            "resource_locks": ["TEST_DOMAIN"],
            "requirement_ids": ["REQ_001"],
            "budgets": {
                "max_turns": 4,
                "max_repair_cycles": 1,
                "timeout_seconds": 30,
            },
            "provider_mode": "REAL",
        }
    )


def _worker(request: RunRequest) -> WorkerResult:
    return WorkerResult.from_dict(
        {
            "schema_version": 1,
            "contract_role": "LOOP_A2_WORKER_RESULT",
            "project_id": request.project_id,
            "run_id": request.run_id,
            "package_id": request.package_id,
            "expected_main_sha": request.expected_main_sha,
            "role": "BUILDER",
            "status": "COMPLETED",
            "changed_paths": ["scripts/feature/a.gd"],
            "summary": "candidate",
            "usage": {"turns": 1},
            "errors": [],
        }
    )


def _mailbox_with_pass(request: RunRequest) -> VerificationEvidenceMailbox:
    mailbox = VerificationEvidenceMailbox()
    suite = TestSuiteResult(
        project_id=request.project_id,
        expected_main_sha=request.expected_main_sha,
        status="PASS",
        commands=(
            CommandEvidence(
                command_id="UNIT",
                status="PASS",
                exit_code=0,
                error_code=None,
                stdout_sha256="b" * 64,
                stderr_sha256="c" * 64,
                stdout_bytes=7,
                stderr_bytes=0,
                network_policy="DENIED",
                network_boundary_id="TEST_BOUNDARY",
                duration_ms=12,
            ),
        ),
    )
    mailbox.publish_pass(
        request,
        suite,
        authority_snapshot_sha256="d" * 64,
    )
    return mailbox


class _Response:
    output_text = json.dumps(
        {
            "verdict": "PASS",
            "findings": [],
            "checked_requirement_ids": ["REQ_001"],
        }
    )
    usage = None


class _BaseResponsesClient:
    def __init__(self) -> None:
        self.responses = self
        self.calls: list[dict[str, object]] = []

    def create(self, **kwargs):
        self.calls.append(kwargs)
        return _Response()


class _InnerCritic:
    def __init__(self) -> None:
        self.calls: list[tuple[RunRequest, WorkerResult]] = []

    def review(self, request: RunRequest, worker_result: WorkerResult) -> ReviewResult:
        self.calls.append((request, worker_result))
        return ReviewResult.from_dict(
            {
                "schema_version": 1,
                "contract_role": "LOOP_A2_REVIEW_RESULT",
                "project_id": request.project_id,
                "run_id": request.run_id,
                "package_id": request.package_id,
                "expected_main_sha": request.expected_main_sha,
                "role": "CRITIC",
                "verdict": "PASS",
                "findings": [],
                "checked_requirement_ids": ["REQ_001"],
            }
        )


class CriticTestEvidenceTests(unittest.TestCase):
    def test_subscription_critic_client_fails_closed_without_matching_pass_receipt(self) -> None:
        request = _request()
        base = _BaseResponsesClient()
        client = VerificationBoundCodexResponsesClient(
            base_client=base,
            run_request=request,
            verification_mailbox=VerificationEvidenceMailbox(),
        )

        with self.assertRaisesRegex(CodexCliTransportError, "CRITIC_TEST_EVIDENCE_MISSING"):
            client.responses.create(
                model="critic-model",
                instructions="critic",
                input=json.dumps(
                    {
                        "project_id": request.project_id,
                        "package_id": request.package_id,
                        "diff": "bounded",
                    }
                ),
                text={"format": {"type": "json_schema", "name": "review", "strict": True, "schema": {"type": "object"}}},
                store=False,
                max_output_tokens=128,
                timeout=30,
            )
        self.assertEqual(base.calls, [])

    def test_matching_pass_receipt_is_injected_digest_only_into_codex_critic_input(self) -> None:
        request = _request()
        base = _BaseResponsesClient()
        client = VerificationBoundCodexResponsesClient(
            base_client=base,
            run_request=request,
            verification_mailbox=_mailbox_with_pass(request),
        )
        client.responses.create(
            model="critic-model",
            instructions="critic",
            input=json.dumps(
                {
                    "project_id": request.project_id,
                    "package_id": request.package_id,
                    "diff": "bounded",
                }
            ),
            text={"format": {"type": "json_schema", "name": "review", "strict": True, "schema": {"type": "object"}}},
            store=False,
            max_output_tokens=128,
            timeout=30,
        )

        self.assertEqual(len(base.calls), 1)
        payload = json.loads(str(base.calls[0]["input"]))
        evidence = payload["test_evidence"]
        self.assertEqual(evidence["status"], "PASS")
        self.assertEqual(evidence["run_id"], request.run_id)
        self.assertEqual(evidence["expected_main_sha"], request.expected_main_sha)
        command = evidence["test_suite"]["commands"][0]
        self.assertIn("stdout_sha256", command)
        self.assertIn("stderr_sha256", command)
        self.assertNotIn("stdout", command)
        self.assertNotIn("stderr", command)

    def test_bound_critic_rejects_cross_run_reuse_before_inner_critic(self) -> None:
        request = _request()
        inner = _InnerCritic()
        critic = VerificationBoundCritic(inner=inner, run_request=request)
        other = _request("RUN_CRITIC_TEST_002")

        with self.assertRaisesRegex(CodexCliTransportError, "CRITIC_RUN_IDENTITY_MISMATCH"):
            critic.review(other, _worker(other))
        self.assertEqual(inner.calls, [])


if __name__ == "__main__":
    unittest.main()
