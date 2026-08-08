from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL_ID = "developing-and-revising-serial-fiction"
CONTRACT_TEST = "tests/test_serial_fiction_discipline.py"


def insert_method(path: str, marker: str, method: str) -> None:
    file_path = ROOT / path
    text = file_path.read_text(encoding="utf-8")
    if marker in text:
        return
    needle = '\n\n\nif __name__ == "__main__":\n'
    if needle not in text:
        raise RuntimeError(f"missing insertion marker in {path}")
    text = text.replace(needle, "\n\n" + method.rstrip() + needle, 1)
    file_path.write_text(text, encoding="utf-8")


def main() -> None:
    freshness_path = ROOT / ".github/reference-freshness.json"
    config = json.loads(freshness_path.read_text(encoding="utf-8"))
    rules = {rule["name"]: rule for rule in config["coupled_change_rules"]}
    registry_rule = rules["registry-structure-test-sync"]
    if CONTRACT_TEST not in registry_rule["require_any_changed"]:
        registry_rule["require_any_changed"].append(CONTRACT_TEST)
    freshness_path.write_text(json.dumps(config, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    insert_method(
        "tests/test_skill_behavior_evidence_hardening.py",
        "test_serial_fiction_skill_has_primary_and_non_selection_coverage",
        '''    def test_serial_fiction_skill_has_primary_and_non_selection_coverage(self) -> None:
        evals = self.checker.load_eval_set(ROOT)
        primary = [
            case for case in evals["cases"]
            if case["expected_primary_skill"] == "developing-and-revising-serial-fiction"
        ]
        forbidden = [
            case for case in evals["cases"]
            if "developing-and-revising-serial-fiction" in case["forbidden_skills"]
        ]
        self.assertGreaterEqual(len(primary), 1)
        self.assertGreaterEqual(len(forbidden), 1)
        self.assertEqual([], self.checker.validate_contract(ROOT))
''',
    )

    insert_method(
        "tests/test_skill_implementation_evidence.py",
        "test_serial_fiction_skill_has_executable_repository_evidence",
        '''    def test_serial_fiction_skill_has_executable_repository_evidence(self) -> None:
        builder = load_builder()
        self.assertEqual([], builder.validate_evidence_index(ROOT))
        markdown = builder.build_evidence_markdown(ROOT)
        row = next(
            line for line in markdown.splitlines()
            if line.startswith("| `developing-and-revising-serial-fiction`")
        )
        self.assertIn("PASS", row)
        self.assertIn("EXECUTABLE_EVIDENCE", row)
        self.assertIn("tests/test_serial_fiction_discipline.py", row)
''',
    )

    insert_method(
        "tests/test_skill_behavior_governance_integration.py",
        "test_serial_fiction_skill_coupled_change_and_entrypoint_contract_is_explicit",
        '''    def test_serial_fiction_skill_coupled_change_and_entrypoint_contract_is_explicit(self) -> None:
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
''',
    )

    insert_method(
        "tests/test_skill_behavior_adversarial_boundaries.py",
        "test_serial_fiction_cases_preserve_nonselection_and_evidence_boundaries",
        '''    def test_serial_fiction_cases_preserve_nonselection_and_evidence_boundaries(self) -> None:
        coverage = json.loads(
            (ROOT / "skills/SKILL_BEHAVIOR_COVERAGE_EVALS.json").read_text(encoding="utf-8")
        )
        cases = {case["case_id"]: case for case in coverage["cases"]}
        fiction = cases["SBE-950"]
        self.assertEqual("developing-and-revising-serial-fiction", fiction["expected_primary_skill"])
        self.assertIn("Episode Value", fiction["required_evidence"])
        game = cases["SBE-951"]
        self.assertEqual("analyzing-and-refining-game-concepts", game["expected_primary_skill"])
        self.assertIn("developing-and-revising-serial-fiction", game["forbidden_skills"])
''',
    )


if __name__ == "__main__":
    main()
