from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class SkillBehaviorGovernanceIntegrationTests(unittest.TestCase):
    def test_skill_behavior_eval_contract_names_complete_evidence_surfaces(self) -> None:
        skill = (ROOT / "skills/evolving-project-discipline-skills/SKILL.md").read_text(encoding="utf-8")
        for token in (
            "skills/SKILL_BEHAVIOR_COVERAGE_EVALS.json",
            "schemas/skill-behavior-results-v1.schema.json",
            "skills/SKILL_BEHAVIOR_RESULTS.template.json",
            "skills/SKILL_IMPLEMENTATION_EVIDENCE.json",
            "docs/generated/BASE_SKILL_IMPLEMENTATION_EVIDENCE.md",
            "independent reviewer context",
        ):
            self.assertIn(token, skill)

    def test_focused_learning_log_records_truthful_limits(self) -> None:
        log_path = ROOT / "skills/evolving-project-discipline-skills/LEARNING_LOG.md"
        self.assertTrue(log_path.is_file())
        text = log_path.read_text(encoding="utf-8")
        for token in (
            "MODEL_RUN_STATUS: NOT_RUN",
            "active Skill",
            "primary behavior coverage",
            "non-selection behavior coverage",
            "exact commit",
            "independent reviewer",
            "CONTRACT_EVIDENCE",
        ):
            self.assertIn(token, text)

    def test_reference_freshness_couples_behavior_evidence_contract(self) -> None:
        config = json.loads((ROOT / ".github/reference-freshness.json").read_text(encoding="utf-8"))
        rules = {rule["name"]: rule for rule in config["coupled_change_rules"]}
        self.assertIn("skill-behavior-evidence-sync", rules)
        rule = rules["skill-behavior-evidence-sync"]
        for path in (
            "tools/check_skill_behavior_evals.py",
            "tools/build_skill_implementation_evidence.py",
            "skills/SKILL_BEHAVIOR_COVERAGE_EVALS.json",
            "skills/SKILL_IMPLEMENTATION_EVIDENCE.json",
            "schemas/skill-behavior-results-v1.schema.json",
        ):
            self.assertIn(path, rule["when_changed"])
        for path in (
            "tests/test_skill_behavior_evidence_hardening.py",
            "tests/test_skill_implementation_evidence.py",
            "tests/test_skill_behavior_governance_integration.py",
            "docs/generated/BASE_SKILL_IMPLEMENTATION_EVIDENCE.md",
        ):
            self.assertIn(path, rule["require_all_changed"])

    def test_youtube_skill_coupled_change_and_entrypoint_contract_is_explicit(self) -> None:
        config = json.loads((ROOT / ".github/reference-freshness.json").read_text(encoding="utf-8"))
        rules = {rule["name"]: rule for rule in config["coupled_change_rules"]}
        self.assertIn(
            "tests/test_game_development_youtube_skill.py",
            rules["local-skill-contract-learning-test-sync"]["require_any_changed"],
        )
        self.assertIn(
            "tests/test_game_development_youtube_skill.py",
            rules["registry-structure-test-sync"]["require_any_changed"],
        )
        operating = (ROOT / "docs/OPERATING_MODEL.md").read_text(encoding="utf-8")
        self.assertIn("producing-game-development-youtube-videos", operating)
        self.assertIn("HUMAN_NOT_RUN", operating)
        self.assertIn("프로젝트 Adapter가 없으므로 Base shared route를 만들지 않는다", operating)

    def test_skill_body_change_uses_focused_learning_companions(self) -> None:
        config = json.loads((ROOT / ".github/reference-freshness.json").read_text(encoding="utf-8"))
        rules = {rule["name"]: rule for rule in config["coupled_change_rules"]}
        generic = rules["local-skill-contract-learning-test-sync"]
        self.assertIn(
            "skills/evolving-project-discipline-skills/SKILL.md",
            generic["exclude_when_changed"],
        )
        focused = rules["skill-evolution-behavior-evidence-sync"]
        self.assertEqual(
            ["skills/evolving-project-discipline-skills/SKILL.md"],
            focused["when_changed"],
        )
        for path in (
            "skills/evolving-project-discipline-skills/LEARNING_LOG.md",
            "tests/test_skill_behavior_evidence_hardening.py",
            "tests/test_skill_implementation_evidence.py",
            "tests/test_skill_behavior_governance_integration.py",
            "docs/generated/BASE_SKILL_IMPLEMENTATION_EVIDENCE.md",
        ):
            self.assertIn(path, focused["require_all_changed"])

    def test_bcp008_behavior_contract_preserves_truthful_evidence_limits(self) -> None:
        evals = json.loads((ROOT / "skills/SKILL_BEHAVIOR_EVALS.json").read_text(encoding="utf-8"))
        self.assertEqual("NOT_RUN", evals["model_run_status"])
        case_ids = {case["case_id"] for case in evals["cases"]}
        self.assertTrue({"SBE-901", "SBE-902", "SBE-903", "SBE-904"}.issubset(case_ids))
        generated = (ROOT / "docs/generated/BASE_SKILL_IMPLEMENTATION_EVIDENCE.md").read_text(encoding="utf-8")
        self.assertIn("External model behavior run: `NOT_RUN`", generated)
        self.assertIn("tests/test_bcp008_behavior_and_procurement_pilot.py", generated)

    def test_deliberate_work_and_postmerge_cases_are_governed_evidence(self) -> None:
        evals = json.loads((ROOT / "skills/SKILL_BEHAVIOR_EVALS.json").read_text(encoding="utf-8"))
        cases = {case["case_id"]: case for case in evals["cases"]}
        self.assertEqual("managing-project-intake-and-work-contract", cases["SBE-040"]["expected_primary_skill"])
        self.assertEqual("managing-project-intake-and-work-contract", cases["SBE-041"]["expected_primary_skill"])
        self.assertIn("NOT_RUN", "\n".join(cases["SBE-040"]["required_evidence"]))
        self.assertIn("Notion", "\n".join(cases["SBE-041"]["required_evidence"]))

        generated = (ROOT / "docs/generated/BASE_SKILL_IMPLEMENTATION_EVIDENCE.md").read_text(encoding="utf-8")
        self.assertIn("Behavior evaluation case count", generated)
        self.assertIn("Behavior evaluation source SHA-256", generated)


    def test_serial_fiction_skill_coupled_change_and_entrypoint_contract_is_explicit(self) -> None:
        config = json.loads((ROOT / ".github/reference-freshness.json").read_text(encoding="utf-8"))
        rules = {rule["name"]: rule for rule in config["coupled_change_rules"]}
        self.assertIn(
            "tests/test_serial_fiction_discipline.py",
            rules["local-skill-contract-learning-test-sync"]["require_any_changed"],
        )
        self.assertIn(
            "tests/test_serial_fiction_discipline.py",
            rules["registry-structure-test-sync"]["require_any_changed"],
        )
        operating = (ROOT / "docs/OPERATING_MODEL.md").read_text(encoding="utf-8")
        self.assertIn("developing-and-revising-serial-fiction", operating)
        self.assertIn("독자 반응 Evidence", operating)


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

    def test_connector_fallback_fixture_and_generated_evidence_are_connected(self) -> None:
        evals = json.loads((ROOT / "skills/SKILL_BEHAVIOR_EVALS.json").read_text(encoding="utf-8"))
        case = next(case for case in evals["cases"] if case["case_id"] == "SBE-039")
        self.assertEqual("synchronizing-local-and-github-state", case["expected_primary_skill"])
        self.assertIn("github_connector / local_git / gh_cli capability 판정", case["required_evidence"])
        generated = (ROOT / "docs/generated/BASE_SKILL_IMPLEMENTATION_EVIDENCE.md").read_text(encoding="utf-8")
        owner_line = next(
            line
            for line in generated.splitlines()
            if line.startswith("| `synchronizing-local-and-github-state`")
        )
        self.assertIn("tests/test_github_connector_fallback_policy.py", owner_line)
        self.assertIn("External model behavior run: `NOT_RUN`", generated)


if __name__ == "__main__":
    unittest.main()
