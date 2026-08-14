from __future__ import annotations

import json
from pathlib import Path
import unittest

from jsonschema import Draft202012Validator

from tools.loop_a2_runtime.evidence import canonical_receipt, redact_sensitive
from tools.loop_a2_runtime.protocol import ProtocolError, ReviewResult, RunRequest
from tools.loop_a2_runtime.providers import FakeBuilder, FakeCritic
from tools.loop_a2_runtime.runner import A2Runtime
from tests.test_loop_a2_protocol import valid_request

ROOT = Path(__file__).resolve().parents[1]


class FailureBoundaryTests(unittest.TestCase):
    def request(self) -> RunRequest:
        return RunRequest.from_dict(valid_request())

    def test_builder_exception_becomes_redacted_provider_failure(self) -> None:
        class ExplodingBuilder:
            def invoke(self, request: RunRequest, *, repair_cycle: int):
                raise RuntimeError("OPENAI_API_KEY=sk-do-not-record")

        outcome = A2Runtime(
            builder=ExplodingBuilder(),
            critic=FakeCritic(verdict="PASS", checked_requirement_ids=("REQ_001",)),
        ).run(self.request(), observed_main_sha=self.request().expected_main_sha)
        self.assertEqual(outcome.state, "PROVIDER_FAILURE")
        self.assertIn("BUILDER_PROVIDER_EXCEPTION", outcome.finding_codes)
        self.assertNotIn("sk-do-not-record", json.dumps(outcome.evidence))

    def test_critic_exception_becomes_redacted_provider_failure(self) -> None:
        class ExplodingCritic:
            def review(self, request: RunRequest, worker_result):
                raise RuntimeError("authorization=Bearer do-not-record")

        outcome = A2Runtime(
            builder=FakeBuilder(changed_paths=("scripts/feature/a.gd",)),
            critic=ExplodingCritic(),
        ).run(self.request(), observed_main_sha=self.request().expected_main_sha)
        self.assertEqual(outcome.state, "PROVIDER_FAILURE")
        self.assertIn("CRITIC_PROVIDER_EXCEPTION", outcome.finding_codes)
        self.assertNotIn("do-not-record", json.dumps(outcome.evidence))

    def test_review_protocol_requires_coherent_verdict_evidence(self) -> None:
        base = {
            "schema_version": 1,
            "contract_role": "LOOP_A2_REVIEW_RESULT",
            "project_id": "BLACKSMITH",
            "run_id": "RUN_001",
            "package_id": "PACKAGE_001",
            "expected_main_sha": "a" * 40,
            "role": "CRITIC",
            "checked_requirement_ids": ["REQ_001"],
        }
        finding = {
            "code": "MUST_FIX_ITEM",
            "severity": "P1",
            "message": "Bounded finding.",
            "paths": ["scripts/feature/a.gd"],
            "requirement_ids": ["REQ_001"],
        }
        with self.assertRaises(ProtocolError):
            ReviewResult.from_dict(base | {"verdict": "PASS", "findings": [finding]})
        with self.assertRaises(ProtocolError):
            ReviewResult.from_dict(base | {"verdict": "MUST_FIX", "findings": []})

    def test_review_schema_matches_protocol_consistency(self) -> None:
        schema = json.loads(
            (ROOT / "schemas/loop-a2-review-result-v1.schema.json").read_text(encoding="utf-8")
        )
        validator = Draft202012Validator(schema)
        base = {
            "schema_version": 1,
            "contract_role": "LOOP_A2_REVIEW_RESULT",
            "project_id": "BLACKSMITH",
            "run_id": "RUN_001",
            "package_id": "PACKAGE_001",
            "expected_main_sha": "a" * 40,
            "role": "CRITIC",
            "checked_requirement_ids": ["REQ_001"],
        }
        finding = {
            "code": "MUST_FIX_ITEM",
            "severity": "P1",
            "message": "Bounded finding.",
            "paths": ["scripts/feature/a.gd"],
            "requirement_ids": ["REQ_001"],
        }
        self.assertTrue(list(validator.iter_errors(base | {"verdict": "PASS", "findings": [finding]})))
        self.assertTrue(list(validator.iter_errors(base | {"verdict": "MUST_FIX", "findings": []})))

    def test_fake_receipt_is_never_integration_eligible(self) -> None:
        outcome = A2Runtime(
            builder=FakeBuilder(changed_paths=("scripts/feature/a.gd",)),
            critic=FakeCritic(verdict="PASS", checked_requirement_ids=("REQ_001",)),
        ).run(self.request(), observed_main_sha=self.request().expected_main_sha)
        self.assertFalse(outcome.evidence["integration_eligible"])

    def test_burnin_counts_all_scope_violations(self) -> None:
        runtime = A2Runtime(
            builder=FakeBuilder(changed_paths=(".github/workflows/unsafe.yml",)),
            critic=FakeCritic(verdict="PASS", checked_requirement_ids=("REQ_001",)),
        )
        report = runtime.burn_in(
            self.request(), observed_main_sha=self.request().expected_main_sha, runs=3
        )
        self.assertEqual(report["status"], "FAKE_PROVIDER_BURNIN_FAILED")
        self.assertEqual(report["out_of_scope_writes"], 3)

    def test_camel_and_prefixed_secret_keys_are_redacted(self) -> None:
        value = {
            "apiKey": "a",
            "x-api-key": "b",
            "clientSecret": "c",
            "sessionToken": "d",
        }
        self.assertEqual(set(redact_sensitive(value).values()), {"[REDACTED]"})
        self.assertFalse(canonical_receipt(value)["integration_eligible"] if "integration_eligible" in canonical_receipt(value) else False)


if __name__ == "__main__":
    unittest.main()
