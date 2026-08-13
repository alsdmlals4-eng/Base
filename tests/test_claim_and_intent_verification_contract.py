from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_ID = "reviewing-and-validating-project-changes"
REFERENCE = ROOT / "skills" / SKILL_ID / "references" / "claim-and-intent-verification.md"


class ClaimAndIntentVerificationContractTests(unittest.TestCase):
    def test_existing_review_owner_absorbs_claim_and_intent_mode(self) -> None:
        skill = (ROOT / "skills" / SKILL_ID / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("`claim-and-intent-verification`", skill)
        self.assertIn("references/claim-and-intent-verification.md", skill)
        self.assertIn("MATERIAL_CLAIM_LEDGER", skill)
        self.assertIn("INTENT_IMPLEMENTATION_FIDELITY_MATRIX", skill)
        self.assertIn("COMPLETION_CLAIM_GATE", skill)
        self.assertIn("CLAIM_UNVERIFIED", skill)
        self.assertIn("IMPLEMENTATION_UNVERIFIED", skill)

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

    def test_registry_routes_narrowly_without_adding_active_skill(self) -> None:
        registry = json.loads((ROOT / "skills/SKILL_REGISTRY.json").read_text(encoding="utf-8"))
        active = [entry for entry in registry["skills"] if entry["status"] == "ACTIVE"]
        self.assertEqual(30, len(active))
        owners = [entry for entry in active if entry["skill_id"] == SKILL_ID]
        self.assertEqual(1, len(owners))
        owner = owners[0]
        for trigger in (
            "completion-claim",
            "claim-evidence",
            "intent-conformance",
            "hallucination-audit",
        ):
            self.assertIn(trigger, owner["trigger_tags"])
        joined_use_when = "\n".join(owner["use_when"])
        self.assertIn("완료 주장", joined_use_when)
        self.assertIn("승인 의도", joined_use_when)
        self.assertIn("실제 diff", joined_use_when)
        self.assertIn("exact HEAD", joined_use_when)

    def test_template_and_workflow_docs_expose_the_gate(self) -> None:
        template = (ROOT / "templates/quality/PROJECT_CHANGE_VALIDATION.md").read_text(encoding="utf-8")
        for heading in (
            "Material Claim Ledger",
            "Intent–Implementation Fidelity Matrix",
            "Completion Claim Gate",
        ):
            self.assertIn(heading, template)
        for relative in ("docs/WORK_MODE_AND_SKILL_ROUTING.md", "docs/OPERATING_MODEL.md"):
            text = (ROOT / relative).read_text(encoding="utf-8")
            self.assertIn("CLAIM_AND_INTENT_VERIFICATION_GATE", text, relative)
            self.assertIn("BLOCKED_UNVERIFIED", text, relative)

    def test_behavior_eval_sbe_038_routes_to_existing_review_owner(self) -> None:
        evals = json.loads((ROOT / "skills/SKILL_BEHAVIOR_EVALS.json").read_text(encoding="utf-8"))
        cases = [case for case in evals["cases"] if case["case_id"] == "SBE-038"]
        self.assertEqual(1, len(cases))
        case = cases[0]
        self.assertEqual("REVIEW", case["expected_work_mode"])
        self.assertEqual(SKILL_ID, case["expected_primary_skill"])
        self.assertIn("claim-and-intent-verification", case["expected_skill_modes"])
        evidence = "\n".join(case["required_evidence"])
        for marker in ("exact-ref", "실제 diff", "미검증", "main readback"):
            self.assertIn(marker, evidence)

    def test_design_plan_and_learning_record_are_present(self) -> None:
        required = (
            ROOT / "docs/superpowers/specs/2026-08-13-claim-and-intent-verification-design.md",
            ROOT / "docs/superpowers/plans/2026-08-13-claim-and-intent-verification.md",
            ROOT / "skills/SKILL_LEARNING_LOG.md",
        )
        for path in required:
            self.assertTrue(path.is_file(), str(path.relative_to(ROOT)))
        learning = (ROOT / "skills/SKILL_LEARNING_LOG.md").read_text(encoding="utf-8")
        self.assertIn("BCP-2026-027", learning)
        self.assertIn("검색 결과", learning)
        self.assertIn("exact-SHA readback", learning)


if __name__ == "__main__":
    unittest.main()
