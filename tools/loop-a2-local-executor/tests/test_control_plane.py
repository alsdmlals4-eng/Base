from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys
import unittest

SRC = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC))

from loop_a2_local_executor.control_plane import (
    ControlPlaneError,
    GhControlPlane,
    sanitize_public_receipt,
)


class FakeRunner:
    def __init__(self, responses: list[subprocess.CompletedProcess[str]]) -> None:
        self.responses = list(responses)
        self.calls: list[dict[str, object]] = []

    def __call__(self, argv, **kwargs):
        self.calls.append({"argv": tuple(argv), **kwargs})
        return self.responses.pop(0)


class ControlPlaneTests(unittest.TestCase):
    def plane(self, runner: FakeRunner) -> GhControlPlane:
        return GhControlPlane(
            control_repository="alsdmlals4-eng/Base",
            required_label="loop-a2-local-job",
            gh_executable="/trusted/gh",
            runner=runner,
        )

    def test_preflight_authenticates_then_idempotently_ensures_queue_label(self) -> None:
        runner = FakeRunner([
            subprocess.CompletedProcess([], 0, stdout="ok", stderr=""),
            subprocess.CompletedProcess([], 0, stdout="", stderr=""),
        ])
        self.plane(runner).preflight()
        self.assertEqual(runner.calls[0]["argv"], ("/trusted/gh", "auth", "status", "--hostname", "github.com"))
        self.assertEqual(
            runner.calls[1]["argv"],
            (
                "/trusted/gh", "label", "create", "loop-a2-local-job", "--repo", "alsdmlals4-eng/Base",
                "--color", "5319E7", "--description", "Bounded unattended Loop A2 local execution job",
                "--force",
            ),
        )

    def test_list_jobs_uses_closed_argv_and_secret_free_environment(self) -> None:
        payload = [{"number": 10, "author": {"login": "alsdmlals4-eng"}, "labels": [{"name": "loop-a2-local-job"}], "body": "x"}]
        runner = FakeRunner([
            subprocess.CompletedProcess([], 0, stdout="ok", stderr=""),
            subprocess.CompletedProcess([], 0, stdout="", stderr=""),
            subprocess.CompletedProcess([], 0, stdout=json.dumps(payload), stderr=""),
        ])
        old = {key: os.environ.get(key) for key in ("GH_TOKEN", "GITHUB_TOKEN", "OPENAI_API_KEY")}
        try:
            os.environ["GH_TOKEN"] = "secret-gh"
            os.environ["GITHUB_TOKEN"] = "secret-github"
            os.environ["OPENAI_API_KEY"] = "secret-openai"
            plane = self.plane(runner)
            plane.preflight()
            jobs = plane.list_open_jobs()
        finally:
            for key, value in old.items():
                if value is None:
                    os.environ.pop(key, None)
                else:
                    os.environ[key] = value
        self.assertEqual(len(jobs), 1)
        listing = runner.calls[2]
        self.assertEqual(
            listing["argv"],
            (
                "/trusted/gh", "issue", "list", "--repo", "alsdmlals4-eng/Base",
                "--state", "open", "--label", "loop-a2-local-job", "--limit", "100",
                "--json", "number,author,labels,body",
            ),
        )
        for call in runner.calls:
            self.assertIs(call["shell"], False)
            env = call["env"]
            self.assertNotIn("GH_TOKEN", env)
            self.assertNotIn("GITHUB_TOKEN", env)
            self.assertNotIn("OPENAI_API_KEY", env)

    def test_nonzero_or_oversized_job_listing_fails_closed(self) -> None:
        for completed, code in (
            (subprocess.CompletedProcess([], 1, stdout="", stderr="bad"), "GH_ISSUE_LIST_FAILED"),
            (subprocess.CompletedProcess([], 0, stdout="x" * 5000, stderr=""), "GH_OUTPUT_LIMIT"),
        ):
            runner = FakeRunner([completed])
            plane = GhControlPlane(
                control_repository="alsdmlals4-eng/Base",
                required_label="loop-a2-local-job",
                gh_executable="/trusted/gh",
                runner=runner,
                output_limit_bytes=1024,
            )
            with self.assertRaises(ControlPlaneError) as caught:
                plane.list_open_jobs()
            self.assertEqual(caught.exception.code, code)

    def test_publish_terminal_comments_before_close(self) -> None:
        runner = FakeRunner([
            subprocess.CompletedProcess([], 0, stdout="", stderr=""),
            subprocess.CompletedProcess([], 0, stdout="", stderr=""),
        ])
        plane = self.plane(runner)
        plane.publish_terminal(44, {"status": "PASS", "code": "A2_WAITING_INTEGRATION"}, close=True)
        self.assertEqual(runner.calls[0]["argv"][:5], ("/trusted/gh", "issue", "comment", "44", "--repo"))
        self.assertIn("--body", runner.calls[0]["argv"])
        self.assertEqual(
            runner.calls[1]["argv"],
            ("/trusted/gh", "issue", "close", "44", "--repo", "alsdmlals4-eng/Base", "--reason", "completed"),
        )

    def test_comment_failure_prevents_close(self) -> None:
        runner = FakeRunner([subprocess.CompletedProcess([], 1, stdout="", stderr="bad")])
        plane = self.plane(runner)
        with self.assertRaises(ControlPlaneError) as caught:
            plane.publish_terminal(44, {"status": "PASS"}, close=True)
        self.assertEqual(caught.exception.code, "GH_RECEIPT_PUBLISH_FAILED")
        self.assertEqual(len(runner.calls), 1)

    def test_public_receipt_is_allowlisted_and_drops_sensitive_material(self) -> None:
        value = sanitize_public_receipt(
            {
                "status": "PASS",
                "code": "A2_WAITING_INTEGRATION",
                "issue_number": 12,
                "target_repository": "alsdmlals4-eng/Blacksmith",
                "base_runtime_sha": "a" * 40,
                "authority_sha": "b" * 40,
                "run_id": "BS_A2_BURNIN_001",
                "a2_state": "WAITING_INTEGRATION",
                "a2_receipt_digest": "c" * 64,
                "provider_mode": "REAL",
                "a3_auto_merge": "DISABLED",
                "scheduler": "NOT_CONFIGURED",
                "stdout": "secret",
                "stderr": "secret",
                "local_path": "C:/Users/user/private",
                "token": "ghp_secret",
                "reasoning": "hidden",
                "changed_paths": ["private.txt"],
            }
        )
        self.assertEqual(value["contract_role"], "LOOP_A2_LOCAL_JOB_RECEIPT")
        rendered = json.dumps(value, sort_keys=True)
        for forbidden in ("stdout", "stderr", "C:/Users", "ghp_", "reasoning", "private.txt"):
            self.assertNotIn(forbidden, rendered)
        self.assertEqual(value["a3_auto_merge"], "DISABLED")
        self.assertEqual(value["scheduler"], "NOT_CONFIGURED")


if __name__ == "__main__":
    unittest.main()
