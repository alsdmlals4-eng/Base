from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read_text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def read_json(path: str) -> dict:
    return json.loads(read_text(path))


class ClaimAndIntentVerificationContractTests(unittest.TestCase):
    def test_existing_validation_owner_exposes_claim_and_intent_mode(self) -> None:
        skill = read_text("skills/reviewing-and-validating-project-changes/SKILL.md")
        reference_path = ROOT / "skills/reviewing-and-validating-project-changes/references/claim-and-intent-verification.md"

        self.assertTrue(reference_path.is_file(), "claim-and-intent reference must exist")
        for token in (
            "claim-and-intent-verification",
            "MATERIAL_CLAIM_LEDGER",
            "INTENT_IMPLEMENTATION_FIDELITY_MATRIX",
            "COMPLETION_CLAIM_GATE",
            "CLAIM_UNVERIFIED",
            "IMPLEMENTATION_UNVERIFIED",
        ):
            self.assertIn(token, skill)

    def test_reference_is_fail_closed_and_deterministic_first(self) -> None:
        reference = read_text(
            "skills/reviewing-and-validating-project-changes/references/claim-and-intent-verification.md"
        )
        for token in (
            "claim_id",
            "claim_type",
            "authority_source",
            "evidence_locator",
            "freshness",
            "counterevidence",
            "CLAIM_VERIFIED",
            "CLAIM_CONTRADICTED",
            "CLAIM_UNVERIFIED",
            "intent_id",
            "approved_intent_or_acceptance",
            "implementation_paths",
            "observed_behavior",
            "verification_evidence",
            "evidence_ceiling",
            "INTENT_CONFORMANT",
            "MINOR_TECHNICAL_DRIFT",
            "PLANNING_CONFLICT",
            "IMPLEMENTATION_UNVERIFIED",
            "BLOCKED_UNVERIFIED",
            "deterministic-first",
            "exact HEAD",
            "post-merge main readback",
            "VERIFIER",
            "CRITIC",
        ):
            self.assertIn(token, reference)

    def test_repository_fact_requires_exact_ref_readback(self) -> None:
        reference = read_text(
            "skills/reviewing-and-validating-project-changes/references/claim-and-intent-verification.md"
        ).lower()
        self.assertIn("search snippet", reference)
        self.assertIn("exact-ref file readback", reference)
        self.assertIn("claim_unverified", reference)
        self.assertIn("canonical mutation forbidden", reference)

    def test_quality_template_collects_claim_intent_and_completion_evidence(self) -> None:
        template = read_text("templates/quality/PROJECT_CHANGE_VALIDATION.md")
        for token in (
            "원자 주장 원장",
            "의도-구현 충실도",
            "완료 주장 Gate",
            "claim_id",
            "intent_id",
            "authority_source",
            "implementation_paths",
            "exact_head",
            "post_merge_readback",
            "independent_reviewer",
            "evidence_ceiling",
        ):
            self.assertIn(token, template)

    def test_review_workflow_integrates_claim_gate_without_new_work_mode(self) -> None:
        routing = read_text("docs/WORK_MODE_AND_SKILL_ROUTING.md")
        operating = read_text("docs/OPERATING_MODEL.md")
        combined = routing + "\n" + operating
        for token in (
            "CLAIM_AND_INTENT_VERIFICATION_GATE",
            "COMPLETION_CLAIM_GATE",
            "CONCURRENT_CHANGE_PREFLIGHT",
            "producer report",
            "lead, not Evidence",
            "exact-ref",
            "counterevidence",
            "exact-head",
            "post-merge",
        ):
            self.assertIn(token, combined)
        for mode in ("PLAN", "BUILD", "REVIEW"):
            self.assertIn(mode, routing)

    def test_registry_routes_to_existing_owner_and_keeps_30_active_skills(self) -> None:
        registry = read_json("skills/SKILL_REGISTRY.json")
        skills = registry["skills"]
        active = [item for item in skills if item["status"] == "ACTIVE"]
        self.assertEqual(30, len(active))

        owner = next(
            item
            for item in active
            if item["skill_id"] == "reviewing-and-validating-project-changes"
        )
        self.assertEqual("project-change-validation", owner["responsibility_id"])
        tags = set(owner["trigger_tags"])
        self.assertTrue(
            {
                "completion-claim",
                "claim-evidence",
                "intent-conformance",
                "hallucination-audit",
            }.issubset(tags)
        )
        joined = " ".join(owner["use_when"] + owner["review_triggers"])
        for token in ("exact HEAD", "post-merge", "approved intent", "unsupported claim"):
            self.assertIn(token, joined)

    def test_sbe_038_routes_completion_claim_audit_to_review_owner(self) -> None:
        payload = read_json("skills/SKILL_BEHAVIOR_EVALS.json")
        self.assertEqual("NOT_RUN", payload["model_run_status"])
        matches = [case for case in payload["cases"] if case["case_id"] == "SBE-038"]
        self.assertEqual(1, len(matches))
        case = matches[0]
        self.assertEqual("REVIEW", case["expected_work_mode"])
        self.assertEqual(
            "reviewing-and-validating-project-changes",
            case["expected_primary_skill"],
        )
        self.assertIn(
            "claim-and-intent-verification", case["expected_skill_modes"]
        )
        required = set(case["required_evidence"])
        self.assertTrue(
            {
                "claim_id",
                "authority_source",
                "exact_ref_file_readback",
                "intent_id",
                "implementation_paths",
                "verification_evidence",
                "exact_head",
                "post_merge_readback",
                "BLOCKED_UNVERIFIED",
            }.issubset(required)
        )

    def test_learning_log_records_evidence_boundary(self) -> None:
        learning = read_text("skills/SKILL_LEARNING_LOG.md")
        for token in (
            "2026-08-13 — Claim and intent verification gate",
            "BCP-2026-027",
            "SBE-038",
            "search snippet",
            "exact-ref file readback",
            "model_run_status: NOT_RUN",
            "zero hallucinations",
        ):
            self.assertIn(token, learning)

    def test_bcp_lifecycle_links_implementation(self) -> None:
        registry = read_json("[수정제안서]/PROPOSAL_REGISTRY.json")
        entry = next(
            item
            for item in registry["proposals"]
            if item["proposal_id"]
            == "BCP-2026-027-claim-and-intent-verification-gate"
        )
        self.assertIn(entry["status"], {"APPROVED_FOR_IMPLEMENTATION", "IMPLEMENTED"})
        self.assertIsNotNone(entry["approval_ref"])
        self.assertIsNotNone(entry["implementation_pr"])


if __name__ == "__main__":
    unittest.main()
