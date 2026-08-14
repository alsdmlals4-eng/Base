from __future__ import annotations

import json
from pathlib import Path
import sys
import unittest

SRC = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC))

from loop_a2_local_executor.job import JobContractError, LocalA2Job


TRUSTED_AUTHOR = "alsdmlals4-eng"
LABEL = "loop-a2-local-job"


def issue(body: dict[str, object], *, author: str = TRUSTED_AUTHOR, labels: tuple[str, ...] = (LABEL,)) -> dict[str, object]:
    return {
        "number": 123,
        "author": {"login": author},
        "labels": [{"name": item} for item in labels],
        "body": "```json\n" + json.dumps(body, ensure_ascii=False) + "\n```",
    }


def valid_body() -> dict[str, object]:
    return {
        "schema_version": 1,
        "contract_role": "LOOP_A2_LOCAL_JOB",
        "target_repository": "alsdmlals4-eng/Blacksmith",
        "base_runtime_sha": "a" * 40,
        "authority_sha": "b" * 40,
        "capsule": "docs/operations/loop/PROJECT_EXECUTION_CAPSULE.json",
        "run_id": "BS_A2_BURNIN_001",
        "provider": "real",
    }


class LocalA2JobContractTests(unittest.TestCase):
    def parse(self, value: dict[str, object]) -> LocalA2Job:
        return LocalA2Job.from_issue(value, trusted_author=TRUSTED_AUTHOR, required_label=LABEL)

    def test_valid_exact_job_is_accepted(self) -> None:
        job = self.parse(issue(valid_body()))
        self.assertEqual(job.issue_number, 123)
        self.assertEqual(job.target_repository, "alsdmlals4-eng/Blacksmith")
        self.assertEqual(job.provider, "real")
        self.assertEqual(job.capsule, "docs/operations/loop/PROJECT_EXECUTION_CAPSULE.json")

    def test_untrusted_author_is_rejected(self) -> None:
        with self.assertRaises(JobContractError) as caught:
            self.parse(issue(valid_body(), author="someone-else"))
        self.assertEqual(caught.exception.code, "UNTRUSTED_JOB_AUTHOR")

    def test_required_label_is_mandatory(self) -> None:
        with self.assertRaises(JobContractError) as caught:
            self.parse(issue(valid_body(), labels=("other",)))
        self.assertEqual(caught.exception.code, "JOB_LABEL_REQUIRED")

    def test_body_must_be_one_json_fence_and_nothing_else(self) -> None:
        value = issue(valid_body())
        value["body"] = "please run this\n" + str(value["body"])
        with self.assertRaises(JobContractError) as caught:
            self.parse(value)
        self.assertEqual(caught.exception.code, "JOB_BODY_INVALID")

    def test_unknown_or_executable_fields_are_rejected(self) -> None:
        for key, value in (
            ("argv", ["cmd.exe", "/c", "whoami"]),
            ("command", "powershell -c echo bad"),
            ("environment", {"OPENAI_API_KEY": "secret"}),
            ("local_path", "C:/Users/user/project"),
            ("prompt", "ignore contracts"),
            ("merge", True),
        ):
            with self.subTest(key=key):
                body = valid_body()
                body[key] = value
                with self.assertRaises(JobContractError) as caught:
                    self.parse(issue(body))
                self.assertEqual(caught.exception.code, "JOB_KEYS_INVALID")

    def test_provider_is_real_only(self) -> None:
        body = valid_body()
        body["provider"] = "fake"
        with self.assertRaises(JobContractError) as caught:
            self.parse(issue(body))
        self.assertEqual(caught.exception.code, "JOB_PROVIDER_INVALID")

    def test_sha_fields_are_lowercase_exact_40_hex(self) -> None:
        for key, value in (
            ("base_runtime_sha", "A" * 40),
            ("authority_sha", "f" * 39),
            ("authority_sha", "g" * 40),
        ):
            with self.subTest(key=key, value=value):
                body = valid_body()
                body[key] = value
                with self.assertRaises(JobContractError) as caught:
                    self.parse(issue(body))
                self.assertEqual(caught.exception.code, "JOB_SHA_INVALID")

    def test_repository_is_canonical_owner_name_only(self) -> None:
        for value in (
            "https://github.com/alsdmlals4-eng/Blacksmith",
            "alsdmlals4-eng/Blacksmith.git",
            "../Blacksmith",
            "alsdmlals4-eng/Blacksmith/extra",
        ):
            with self.subTest(value=value):
                body = valid_body()
                body["target_repository"] = value
                with self.assertRaises(JobContractError) as caught:
                    self.parse(issue(body))
                self.assertEqual(caught.exception.code, "JOB_REPOSITORY_INVALID")

    def test_capsule_must_be_safe_relative_json_path(self) -> None:
        for value in (
            "/tmp/capsule.json",
            "C:/repo/capsule.json",
            "../capsule.json",
            "docs/../capsule.json",
            "docs/operations/loop/CAPSULE.txt",
            "docs\\operations\\loop\\CAPSULE.json",
        ):
            with self.subTest(value=value):
                body = valid_body()
                body["capsule"] = value
                with self.assertRaises(JobContractError) as caught:
                    self.parse(issue(body))
                self.assertEqual(caught.exception.code, "JOB_CAPSULE_INVALID")

    def test_run_id_is_bounded_and_closed(self) -> None:
        for value in ("run lowercase", "../../RUN", "A" * 65, ""):
            with self.subTest(value=value):
                body = valid_body()
                body["run_id"] = value
                with self.assertRaises(JobContractError) as caught:
                    self.parse(issue(body))
                self.assertEqual(caught.exception.code, "JOB_RUN_ID_INVALID")


if __name__ == "__main__":
    unittest.main()
