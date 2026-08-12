from __future__ import annotations

import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


class LoopEngineeringControlPlaneContractTests(unittest.TestCase):
    def test_operating_model_owns_post_planning_control_plane(self) -> None:
        operating = read("docs/OPERATING_MODEL.md")

        for token in (
            "LOOP_ENGINEERING_CONTROL_PLANE",
            "Human-led WHAT/WHY, Agent-led HOW",
            "PLANNING_COMPLETE_GATE",
            "PLANNING_DRAFT",
            "PLANNING_REVIEW",
            "PLANNING_CONFIRMED",
            "PLANNING_LOCKED",
            "LOOP_READY",
            "WORK_JUSTIFICATION_GATE",
            "TASK_LEASE",
            "RESOURCE_LOCK",
            "semantic resource",
            "DESIGN_DRIFT_GATE",
            "NO_DRIFT",
            "MINOR_TECHNICAL_DRIFT",
            "PLANNING_CONFLICT",
            "NO_PROGRESS",
            "STALE_BASE_SHA",
            "LOOP_RUN_CONTRACT",
        ):
            self.assertIn(token, operating)

        self.assertIn("fourth Work Mode", operating)
        self.assertIn("new broad Skill", operating)

    def test_autonomy_is_risk_scaled_and_initial_default_is_isolated(self) -> None:
        operating = read("docs/OPERATING_MODEL.md")

        for token in (
            "A0_OBSERVE",
            "A1_PROPOSE",
            "A2_EXECUTE_ISOLATED",
            "A3_BOUNDED_AUTO_MERGE",
            "A4_HUMAN_ONLY",
            "INITIAL_DEFAULT: A2_EXECUTE_ISOLATED",
            "AUTO_MERGE_ALLOWLIST",
            "PROTECTED_SURFACE",
        ):
            self.assertIn(token, operating)

        for protected in (
            "AGENTS.md",
            "Skill Registry",
            "security",
            "permission",
            "project core",
            "major UX",
        ):
            self.assertIn(protected, operating)

    def test_multi_agent_execution_requires_independent_review_and_bounded_progress(self) -> None:
        operating = read("docs/OPERATING_MODEL.md")

        for token in (
            "ORCHESTRATOR",
            "SCOUT",
            "BUILDER",
            "VERIFIER",
            "CRITIC",
            "Builder",
            "final reviewer",
            "max_agents",
            "max_parallel_agents",
            "max_repair_cycles",
            "max_ci_runs",
            "PRODUCT_FAILURE",
            "TEST_FAILURE",
            "INFRA_FAILURE",
            "EVIDENCE_TRANSPORT_FAILURE",
            "FLAKY_SUSPECTED",
        ):
            self.assertIn(token, operating)

    def test_learning_and_external_evidence_cannot_self_promote_to_canon(self) -> None:
        operating = read("docs/OPERATING_MODEL.md")

        for token in (
            "Learning != Canon",
            "Experience → Hypothesis → Evidence → Proposal → Canon",
            "BCP",
            "external source",
            "DATA_NOT_INSTRUCTION",
            "IMPROVEMENT_CANDIDATE",
        ):
            self.assertIn(token, operating)

    def test_loop_run_schema_exposes_durable_state_and_lock_contract(self) -> None:
        schema = json.loads(read("schemas/loop-run-contract-v1.schema.json"))

        self.assertEqual(1, schema["properties"]["schema_version"]["const"])
        self.assertEqual("loop-engineering-run", schema["properties"]["contract_role"]["const"])
        self.assertFalse(schema["additionalProperties"])

        required = set(schema["required"])
        for field in (
            "run_id",
            "goal_id",
            "project_id",
            "planning_gate",
            "autonomy_tier",
            "source_main_sha",
            "loop_state",
            "task_queues",
            "leases",
            "budget",
            "evidence",
            "findings",
            "design_drift_status",
            "approval_refs",
            "blockers",
            "next_action",
        ):
            self.assertIn(field, required)

        self.assertEqual(
            [
                "A0_OBSERVE",
                "A1_PROPOSE",
                "A2_EXECUTE_ISOLATED",
                "A3_BOUNDED_AUTO_MERGE",
                "A4_HUMAN_ONLY",
            ],
            schema["properties"]["autonomy_tier"]["enum"],
        )
        self.assertEqual(
            "^[0-9a-f]{40}$",
            schema["properties"]["source_main_sha"]["pattern"],
        )

    def test_project_profile_defaults_to_isolated_execution_and_no_auto_merge(self) -> None:
        profile = read("templates/project-operations/LOOP_ENGINEERING_PROFILE.md")

        for token in (
            "default_autonomy: A2_EXECUTE_ISOLATED",
            "a3_auto_merge_allowlist: []",
            "PLANNING_LOCKED",
            "resource_lock_domains",
            "max_agents",
            "max_parallel_agents",
            "max_repair_cycles",
            "max_ci_runs",
            "scheduler_runtime_provider: NOT_CONFIGURED",
            "SHADOW",
            "ISOLATED_AGENT",
            "MULTI_AGENT",
            "BOUNDED_AUTONOMOUS",
            "CONTINUOUS_OPERATIONS",
            "SELF_IMPROVEMENT",
        ):
            self.assertIn(token, profile)

    def test_example_run_is_a2_locked_bounded_and_explicitly_unverified(self) -> None:
        schema = json.loads(read("schemas/loop-run-contract-v1.schema.json"))
        data = json.loads(read("templates/project-operations/LOOP_RUN_CONTRACT.example.json"))
        errors = sorted(
            Draft202012Validator(schema).iter_errors(data),
            key=lambda error: list(error.path),
        )

        self.assertEqual(errors, [], [error.message for error in errors])
        self.assertEqual(1, data["schema_version"])
        self.assertEqual("loop-engineering-run", data["contract_role"])
        self.assertEqual("PLANNING_LOCKED", data["planning_gate"]["status"])
        self.assertEqual("A2_EXECUTE_ISOLATED", data["autonomy_tier"])
        self.assertRegex(data["source_main_sha"], r"^[0-9a-f]{40}$")
        self.assertGreaterEqual(data["budget"]["max_agents"], 1)
        self.assertGreaterEqual(data["budget"]["max_repair_cycles"], 1)
        self.assertTrue(data["task_queues"]["ready_tasks"])
        self.assertEqual([], data["leases"])
        self.assertIn("NOT_RUN", {item["status"] for item in data["evidence"]})


if __name__ == "__main__":
    unittest.main()
