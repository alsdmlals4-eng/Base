#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OWNER = "reviewing-and-validating-project-changes"


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def write(path: str, text: str) -> None:
    (ROOT / path).write_text(text, encoding="utf-8")


def insert_test_class(path: str, marker: str, block: str) -> None:
    text = read(path)
    if marker in text:
        return
    anchor = '\n\nif __name__ == "__main__":'
    addition = "\n\n" + block.strip() + "\n"
    if anchor in text:
        text = text.replace(anchor, addition + anchor, 1)
    else:
        text = text.rstrip() + addition
    write(path, text)


def update_consolidated_references() -> None:
    insert_test_class(
        "tests/test_consolidated_skill_references.py",
        "class ClaimIntentConsolidatedReferenceTests",
        '''
class ClaimIntentConsolidatedReferenceTests(unittest.TestCase):
    def test_claim_intent_gate_is_integrated_without_a_duplicate_skill(self) -> None:
        import json

        registry = json.loads((ROOT / "skills/SKILL_REGISTRY.json").read_text(encoding="utf-8"))
        active = [entry for entry in registry["skills"] if entry["status"] == "ACTIVE"]
        self.assertEqual(30, len(active))
        owners = [entry for entry in active if entry["skill_id"] == "reviewing-and-validating-project-changes"]
        self.assertEqual(1, len(owners))
        owner = owners[0]
        for trigger in ("completion-claim", "claim-evidence", "intent-conformance", "hallucination-audit"):
            self.assertIn(trigger, owner["trigger_tags"])

        skill = (ROOT / owner["path"]).read_text(encoding="utf-8")
        reference_path = ROOT / "skills/reviewing-and-validating-project-changes/references/claim-and-intent-verification.md"
        template = (ROOT / "templates/quality/PROJECT_CHANGE_VALIDATION.md").read_text(encoding="utf-8")
        operating = (ROOT / "docs/OPERATING_MODEL.md").read_text(encoding="utf-8")
        routing = (ROOT / "docs/WORK_MODE_AND_SKILL_ROUTING.md").read_text(encoding="utf-8")
        self.assertTrue(reference_path.is_file())
        for token in (
            "`claim-and-intent-verification`",
            "MATERIAL_CLAIM_LEDGER",
            "INTENT_IMPLEMENTATION_FIDELITY_MATRIX",
            "COMPLETION_CLAIM_GATE",
        ):
            self.assertIn(token, skill)
        for token in ("Material Claim Ledger", "Intent–Implementation Fidelity Matrix", "Completion Claim Gate"):
            self.assertIn(token, template)
        for text in (operating, routing):
            self.assertIn("CLAIM_AND_INTENT_VERIFICATION_GATE", text)
            self.assertIn("BLOCKED_UNVERIFIED", text)
''',
    )


def update_behavior_hardening() -> None:
    insert_test_class(
        "tests/test_skill_behavior_evidence_hardening.py",
        "class ClaimIntentBehaviorEvidenceHardeningTests",
        '''
class ClaimIntentBehaviorEvidenceHardeningTests(unittest.TestCase):
    def test_sbe_038_is_unique_fail_closed_and_not_model_run(self) -> None:
        documents = [
            json.loads((ROOT / "skills/SKILL_BEHAVIOR_EVALS.json").read_text(encoding="utf-8")),
            json.loads((ROOT / "skills/SKILL_BEHAVIOR_COVERAGE_EVALS.json").read_text(encoding="utf-8")),
        ]
        cases = [case for document in documents for case in document["cases"] if case["case_id"] == "SBE-038"]
        self.assertEqual(1, len(cases))
        case = cases[0]
        self.assertEqual("REVIEW", case["expected_work_mode"])
        self.assertEqual("reviewing-and-validating-project-changes", case["expected_primary_skill"])
        self.assertIn("claim-and-intent-verification", case["expected_skill_modes"])
        required = "\n".join(case["required_evidence"])
        for token in ("exact-ref", "실제 diff", "미검증", "main readback"):
            self.assertIn(token, required)
        self.assertEqual("NOT_RUN", documents[0]["model_run_status"])
''',
    )


def update_implementation_evidence() -> None:
    index_path = "skills/SKILL_IMPLEMENTATION_EVIDENCE.json"
    index = json.loads(read(index_path))
    owners = [entry for entry in index["entries"] if entry["skill_id"] == OWNER]
    if len(owners) != 1:
        raise RuntimeError(f"expected one evidence owner, found {len(owners)}")
    evidence = owners[0]["evidence"]
    record = {"kind": "TEST", "path": "tests/test_claim_and_intent_verification_contract.py"}
    if record not in evidence:
        evidence.append(record)
    write(index_path, json.dumps(index, ensure_ascii=False, indent=2) + "\n")

    insert_test_class(
        "tests/test_skill_implementation_evidence.py",
        "class ClaimIntentImplementationEvidenceIntegrationTests",
        '''
class ClaimIntentImplementationEvidenceIntegrationTests(unittest.TestCase):
    def test_claim_intent_contract_is_linked_without_claiming_a_model_run(self) -> None:
        index = json.loads((ROOT / "skills/SKILL_IMPLEMENTATION_EVIDENCE.json").read_text(encoding="utf-8"))
        owner = next(entry for entry in index["entries"] if entry["skill_id"] == "reviewing-and-validating-project-changes")
        self.assertIn(
            {"kind": "TEST", "path": "tests/test_claim_and_intent_verification_contract.py"},
            owner["evidence"],
        )
        markdown = load_builder().build_evidence_markdown(ROOT)
        self.assertIn("External model behavior run: `NOT_RUN`", markdown)
        owner_line = next(line for line in markdown.splitlines() if line.startswith("| `reviewing-and-validating-project-changes`"))
        self.assertIn("EXECUTABLE_EVIDENCE", owner_line)
        self.assertIn("tests/test_claim_and_intent_verification_contract.py", owner_line)
''',
    )


def update_governance_integration() -> None:
    insert_test_class(
        "tests/test_skill_behavior_governance_integration.py",
        "class ClaimIntentBehaviorGovernanceIntegrationTests",
        '''
class ClaimIntentBehaviorGovernanceIntegrationTests(unittest.TestCase):
    def test_claim_intent_fixture_reference_and_generated_evidence_are_connected(self) -> None:
        evals = json.loads((ROOT / "skills/SKILL_BEHAVIOR_EVALS.json").read_text(encoding="utf-8"))
        case = next(case for case in evals["cases"] if case["case_id"] == "SBE-038")
        self.assertEqual("reviewing-and-validating-project-changes", case["expected_primary_skill"])
        self.assertIn("claim-and-intent-verification", case["expected_skill_modes"])
        reference = (ROOT / "skills/reviewing-and-validating-project-changes/references/claim-and-intent-verification.md").read_text(encoding="utf-8")
        for token in ("CLAIM_UNVERIFIED", "IMPLEMENTATION_UNVERIFIED", "post-merge main readback"):
            self.assertIn(token, reference)
        generated = (ROOT / "docs/generated/BASE_SKILL_IMPLEMENTATION_EVIDENCE.md").read_text(encoding="utf-8")
        self.assertIn("External model behavior run: `NOT_RUN`", generated)
        self.assertIn("tests/test_claim_and_intent_verification_contract.py", generated)
''',
    )


def update_adversarial_boundaries() -> None:
    insert_test_class(
        "tests/test_skill_behavior_adversarial_boundaries.py",
        "class ClaimIntentAdversarialBoundaryTests",
        '''
class ClaimIntentAdversarialBoundaryTests(unittest.TestCase):
    def test_sbe_038_rejects_search_producer_and_stale_sha_shortcuts(self) -> None:
        evals = json.loads((ROOT / "skills/SKILL_BEHAVIOR_EVALS.json").read_text(encoding="utf-8"))
        case = next(case for case in evals["cases"] if case["case_id"] == "SBE-038")
        prompt = case["prompt"]
        required = "\n".join(case["required_evidence"])
        for token in ("검색 결과", "작업자 설명", "merge SHA", "main readback"):
            self.assertIn(token, prompt + "\n" + required)
        for token in ("exact-ref", "exact HEAD", "CLAIM_UNVERIFIED", "IMPLEMENTATION_UNVERIFIED"):
            self.assertIn(token, required)
        self.assertEqual("NOT_REQUIRED", case["expected_user_decision_state"])
        self.assertTrue(case["forbidden_skills"])
''',
    )


def main() -> int:
    update_consolidated_references()
    update_behavior_hardening()
    update_implementation_evidence()
    update_governance_integration()
    update_adversarial_boundaries()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
