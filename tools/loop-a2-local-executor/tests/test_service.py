from __future__ import annotations

import json
from pathlib import Path
import sys
import unittest

SRC = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC))

from loop_a2_local_executor.job import LocalA2Job
from loop_a2_local_executor.runtime import LocalRuntimeError
from loop_a2_local_executor.service import LocalExecutorService


AUTHOR = "alsdmlals4-eng"
LABEL = "loop-a2-local-job"


def valid_issue(number: int = 1) -> dict[str, object]:
    body = {
        "schema_version": 1,
        "contract_role": "LOOP_A2_LOCAL_JOB",
        "target_repository": "alsdmlals4-eng/Blacksmith",
        "base_runtime_sha": "a" * 40,
        "authority_sha": "b" * 40,
        "capsule": "docs/operations/loop/PROJECT_EXECUTION_CAPSULE.json",
        "run_id": f"BS_A2_BURNIN_{number:03d}",
        "provider": "real",
    }
    return {
        "number": number,
        "author": {"login": AUTHOR},
        "labels": [{"name": LABEL}],
        "body": "```json\n" + json.dumps(body) + "\n```",
    }


class FakePlane:
    def __init__(self, issues: list[dict[str, object]]) -> None:
        self.issues = issues
        self.published: list[tuple[int, dict[str, object], bool]] = []
        self.preflights = 0

    def preflight(self) -> None:
        self.preflights += 1

    def list_open_jobs(self):
        return tuple(self.issues)

    def publish_terminal(self, number, receipt, *, close):
        self.published.append((number, dict(receipt), close))


class FakeRuntime:
    def __init__(self, *, error: LocalRuntimeError | None = None) -> None:
        self.error = error
        self.jobs: list[LocalA2Job] = []

    def execute(self, job: LocalA2Job):
        self.jobs.append(job)
        if self.error:
            raise self.error
        return {
            "state": "WAITING_INTEGRATION",
            "provider_mode": "REAL",
            "a3_auto_merge": "DISABLED",
            "scheduler": "NOT_CONFIGURED",
            "receipt_digest": "d" * 64,
        }


class ServiceTests(unittest.TestCase):
    def service(self, plane: FakePlane, runtime: FakeRuntime) -> LocalExecutorService:
        return LocalExecutorService(
            control_plane=plane,
            runtime=runtime,
            trusted_author=AUTHOR,
            required_label=LABEL,
        )

    def test_once_processes_at_most_one_eligible_job(self) -> None:
        plane = FakePlane([valid_issue(1), valid_issue(2)])
        runtime = FakeRuntime()
        result = self.service(plane, runtime).once()
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(len(runtime.jobs), 1)
        self.assertEqual(runtime.jobs[0].issue_number, 1)
        self.assertEqual(len(plane.published), 1)
        self.assertTrue(plane.published[0][2])

    def test_untrusted_or_malformed_jobs_are_skipped_without_execution(self) -> None:
        bad = valid_issue(1)
        bad["author"] = {"login": "attacker"}
        malformed = valid_issue(2)
        malformed["body"] = "not json"
        plane = FakePlane([bad, malformed])
        runtime = FakeRuntime()
        result = self.service(plane, runtime).once()
        self.assertEqual(result["status"], "IDLE")
        self.assertEqual(runtime.jobs, [])
        self.assertEqual(plane.published, [])

    def test_runtime_blocker_is_published_as_sanitized_terminal_code(self) -> None:
        plane = FakePlane([valid_issue(1)])
        runtime = FakeRuntime(error=LocalRuntimeError("CODEX_CHATGPT_AUTH_REQUIRED", "local private detail"))
        result = self.service(plane, runtime).once()
        self.assertEqual(result["status"], "BLOCKED")
        self.assertEqual(plane.published[0][1]["code"], "CODEX_CHATGPT_AUTH_REQUIRED")
        self.assertNotIn("local private detail", json.dumps(plane.published[0][1]))
        self.assertTrue(plane.published[0][2])

    def test_success_receipt_binds_job_and_a2_digest(self) -> None:
        plane = FakePlane([valid_issue(7)])
        runtime = FakeRuntime()
        self.service(plane, runtime).once()
        public = plane.published[0][1]
        self.assertEqual(public["issue_number"], 7)
        self.assertEqual(public["run_id"], "BS_A2_BURNIN_007")
        self.assertEqual(public["a2_state"], "WAITING_INTEGRATION")
        self.assertEqual(public["a2_receipt_digest"], "d" * 64)
        self.assertEqual(public["a3_auto_merge"], "DISABLED")
        self.assertEqual(public["scheduler"], "NOT_CONFIGURED")

    def test_preflight_delegates_without_executing_jobs(self) -> None:
        plane = FakePlane([valid_issue(1)])
        runtime = FakeRuntime()
        result = self.service(plane, runtime).preflight()
        self.assertEqual(result, {"status": "READY", "code": "GH_CONTROL_PLANE_READY"})
        self.assertEqual(plane.preflights, 1)
        self.assertEqual(runtime.jobs, [])


if __name__ == "__main__":
    unittest.main()
