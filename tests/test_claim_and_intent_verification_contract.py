from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_ID = "reviewing-and-validating-project-changes"
SKILL_ROOT = ROOT / "skills" / SKILL_ID
REFERENCE = SKILL_ROOT / "references" / "claim-and-intent-verification.md"
EVAL_FIXTURE = SKILL_ROOT / "evals" / "claim-and-intent-verification.json"
LEARNING_LOG = SKILL_ROOT / "LEARNING_LOG.md"
TEMPLATE = ROOT / "templates/quality/PROJECT_CHANGE_VALIDATION.md"


class ClaimAndIntentVerificationContractTests(unittest.TestCase):
    def test_existing_review_owner_absorbs_gate_by_progressive_disclosure(self) -> None:
        skill = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        template = TEMPLATE.read_text(encoding="utf-8")
        self.assertIn("`external-source-review`", skill)
        self.assertIn("실제 diff", skill)
        self.assertIn("templates/quality/PROJECT_CHANGE_VALIDATION.md", skill)
        self.assertIn("BCP-008 Traceability convergence", skill)
        self.assertIn("references/claim-and-intent-verification.md", template)
        self.assertIn("MATERIAL_CLAIM_LEDGER", REFERENCE.read_text(encoding="utf-8"))

    def test_reference_is_fail_closed_and_evidence_bounded(self) -> None:
        self.assertTrue(REFERENCE.is_file(), "claim-and-intent verification reference is missing")
        reference = REFERENCE.read_text(encoding="utf-8")
        for marker in (
            "MATERIAL_CLAIM_LEDGER",
            "authority_source",
            "freshness",
            "counterevidence",
            "CLAIM_VERIFIED",
            "CLAIM_CONTRADICTED",
            "CLAIM_UNVERIFIED",
            "INTENT_IMPLEMENTATION_FIDELITY_MATRIX",
            "INTENT_CONFORMANT",
            "PLANNING_CONFLICT",
            "IMPLEMENTATION_UNVERIFIED",
            "COMPLETION_CLAIM_GATE",
            "deterministic-first",
            "Evidence ceiling",
            "exact HEAD",
            "post-merge main readback",
        ):
            self.assertIn(marker, reference)
        self.assertIn("검색 결과", reference)
        self.assertIn("exact-ref file readback", reference)

    def test_existing_registry_routes_without_adding_active_skill(self) -> None:
        registry = json.loads((ROOT / "skills/SKILL_REGISTRY.json").read_text(encoding="utf-8"))
        active = [entry for entry in registry["skills"] if entry["status"] == "ACTIVE"]
        self.assertEqual(30, len(active))
        owners = [entry for entry in active if entry["skill_id"] == SKILL_ID]
        self.assertEqual(1, len(owners))
        owner = owners[0]
        for existing_trigger in (
            "external-ai-result",
            "contract-check",
            "evidence-report",
        ):
            self.assertIn(existing_trigger, owner["trigger_tags"])
        self.assertNotIn(
            "claim-and-intent-verification",
            [entry["skill_id"] for entry in active],
            "the gate must not create a 31st ACTIVE Skill",
        )

    def test_template_exposes_the_three_gate_contracts(self) -> None:
        template = TEMPLATE.read_text(encoding="utf-8")
        for heading in (
            "Material Claim Ledger",
            "Intent–Implementation Fidelity Matrix",
            "Completion Claim Gate",
        ):
            self.assertIn(heading, template)
        for marker in (
            "CLAIM_UNVERIFIED",
            "IMPLEMENTATION_UNVERIFIED",
            "BLOCKED_UNVERIFIED",
            "exact HEAD",
            "post-merge main readback",
        ):
            self.assertIn(marker, template)

    def test_behavior_eval_sbe_038_routes_to_existing_review_owner(self) -> None:
        self.assertTrue(EVAL_FIXTURE.is_file(), "claim-and-intent behavior fixture is missing")
        evals = json.loads(EVAL_FIXTURE.read_text(encoding="utf-8"))
        cases = [case for case in evals["cases"] if case["case_id"] == "SBE-038"]
        self.assertEqual(1, len(cases))
        case = cases[0]
        self.assertEqual("REVIEW", case["expected_work_mode"])
        self.assertEqual(SKILL_ID, case["expected_primary_skill"])
        self.assertIn("claim-and-intent-verification", case["expected_skill_modes"])
        self.assertEqual(
            ["external-ai-result", "contract-check", "evidence-report"],
            case["existing_registry_trigger_match"],
        )
        evidence = "\n".join(case["required_evidence"])
        for marker in ("exact-ref", "실제 diff", "UNVERIFIED", "main readback"):
            self.assertIn(marker, evidence)

    def test_design_plan_and_owner_learning_record_are_present(self) -> None:
        required = (
            ROOT / "docs/superpowers/specs/2026-08-13-claim-and-intent-verification-design.md",
            ROOT / "docs/superpowers/plans/2026-08-13-claim-and-intent-verification.md",
            LEARNING_LOG,
        )
        for path in required:
            self.assertTrue(path.is_file(), str(path.relative_to(ROOT)))
        learning = LEARNING_LOG.read_text(encoding="utf-8")
        self.assertIn("BCP-2026-027", learning)
        self.assertIn("검색 결과", learning)
        self.assertIn("exact-SHA readback", learning)
        self.assertIn("progressive disclosure", learning)


if __name__ == "__main__":
    unittest.main()
