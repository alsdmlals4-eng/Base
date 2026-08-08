from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BUILDER_PATH = ROOT / "tools/build_skill_implementation_evidence.py"
GENERATED_PATH = ROOT / "docs/generated/BASE_SKILL_IMPLEMENTATION_EVIDENCE.md"


def load_builder():
    spec = importlib.util.spec_from_file_location("build_skill_implementation_evidence", BUILDER_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def active_skill(skill_id: str) -> dict:
    return {
        "skill_id": skill_id,
        "layer": "specialist",
        "discipline": "test-discipline",
        "path": f"skills/{skill_id}/SKILL.md",
        "status": "ACTIVE",
        "load_by_default": False,
        "trigger_tags": [skill_id],
        "use_when": ["test"],
        "do_not_use_when": ["not test"],
        "learning_log": "skills/SKILL_LEARNING_LOG.md",
        "review_triggers": ["failure"],
        "last_reviewed_at": "2026-08-02",
        "last_reviewed_commit": "test",
        "knowledge_state": "OBSERVATION",
    }


def behavior_case(case_id: str, primary: str, forbidden: str) -> dict:
    return {
        "case_id": case_id,
        "case_type": "positive",
        "prompt": f"Concrete evidence request {case_id} without routing labels.",
        "expected_work_mode": "PLAN",
        "expected_primary_skill": primary,
        "expected_supporting_skills": [],
        "expected_skill_modes": ["run"],
        "forbidden_skills": [forbidden],
        "required_evidence": ["evidence"],
        "expected_user_decision_state": "NOT_REQUIRED",
        "rationale": "Focused evidence fixture.",
    }


class SkillImplementationEvidenceTests(unittest.TestCase):
    def test_builder_and_generated_evidence_exist(self) -> None:
        self.assertTrue(BUILDER_PATH.is_file())
        self.assertTrue(GENERATED_PATH.is_file())

    def build_root(
        self,
        include_beta_entry: bool = True,
    ) -> tuple[tempfile.TemporaryDirectory[str], Path]:
        directory = tempfile.TemporaryDirectory()
        root = Path(directory.name)
        write_json(
            root / "skills/SKILL_REGISTRY.json",
            {
                "schema_version": 1,
                "registry_role": "test",
                "routing_policy": {},
                "skills": [active_skill("alpha-skill"), active_skill("beta-skill")],
            },
        )
        write_json(
            root / "skills/SKILL_BEHAVIOR_EVALS.json",
            {
                "schema_version": 1,
                "artifact_role": "BASE_SKILL_BEHAVIOR_EVAL_SET",
                "status": "ACTIVE",
                "model_run_status": "NOT_RUN",
                "source_issue": "https://example.com/1",
                "cases": [
                    behavior_case("SBE-001", "alpha-skill", "beta-skill"),
                    behavior_case("SBE-002", "beta-skill", "alpha-skill"),
                ],
            },
        )
        entries = [
            {
                "skill_id": "alpha-skill",
                "evidence": [
                    {"kind": "TEST", "path": "tests/test_alpha.py"},
                ],
                "pilot_status": "NOT_RUN",
            }
        ]
        if include_beta_entry:
            entries.append(
                {
                    "skill_id": "beta-skill",
                    "evidence": [
                        {"kind": "CONTRACT", "path": "docs/beta.md"},
                    ],
                    "pilot_status": "PARTIAL",
                }
            )
        write_json(
            root / "skills/SKILL_IMPLEMENTATION_EVIDENCE.json",
            {
                "schema_version": 1,
                "artifact_role": "BASE_SKILL_IMPLEMENTATION_EVIDENCE_INDEX",
                "entries": entries,
            },
        )
        for skill_id in ("alpha-skill", "beta-skill"):
            path = root / f"skills/{skill_id}/SKILL.md"
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(f"# {skill_id}\n\nMode: `run`\n", encoding="utf-8")
        (root / "tests").mkdir(exist_ok=True)
        (root / "tests/test_alpha.py").write_text("# test\n", encoding="utf-8")
        (root / "docs").mkdir(exist_ok=True)
        (root / "docs/beta.md").write_text("# contract\n", encoding="utf-8")
        return directory, root

    def test_missing_active_skill_evidence_entry_fails(self) -> None:
        if not BUILDER_PATH.is_file():
            self.skipTest("builder not implemented yet")
        builder = load_builder()
        directory, root = self.build_root(include_beta_entry=False)
        self.addCleanup(directory.cleanup)

        errors = builder.validate_evidence_index(root)

        self.assertIn("missing evidence index entry: beta-skill", errors)

    def test_markdown_distinguishes_executable_and_contract_evidence(self) -> None:
        if not BUILDER_PATH.is_file():
            self.skipTest("builder not implemented yet")
        builder = load_builder()
        directory, root = self.build_root()
        self.addCleanup(directory.cleanup)

        markdown = builder.build_evidence_markdown(root)

        self.assertIn("`alpha-skill`", markdown)
        self.assertIn("EXECUTABLE_EVIDENCE", markdown)
        self.assertIn("`beta-skill`", markdown)
        self.assertIn("CONTRACT_EVIDENCE", markdown)
        self.assertEqual(1, markdown.count("`alpha-skill`"))
        self.assertEqual(1, markdown.count("`beta-skill`"))

    def test_youtube_skill_has_executable_repository_evidence(self) -> None:
        builder = load_builder()
        self.assertEqual([], builder.validate_evidence_index(ROOT))
        markdown = builder.build_evidence_markdown(ROOT)
        row = next(
            line for line in markdown.splitlines()
            if line.startswith("| `producing-game-development-youtube-videos`")
        )
        self.assertIn("PASS", row)
        self.assertIn("EXECUTABLE_EVIDENCE", row)
        self.assertIn("tests/test_game_development_youtube_skill.py", row)

    def test_checked_in_evidence_is_current(self) -> None:
        if not BUILDER_PATH.is_file() or not GENERATED_PATH.is_file():
            self.skipTest("builder not implemented yet")
        builder = load_builder()

        generated = builder.build_evidence_markdown(ROOT)
        checked_in = GENERATED_PATH.read_text(encoding="utf-8")

        self.assertEqual(generated, checked_in)

    def test_bcp008_existing_owners_have_executable_repository_evidence(self) -> None:
        builder = load_builder()
        self.assertEqual([], builder.validate_evidence_index(ROOT))
        markdown = builder.build_evidence_markdown(ROOT)
        expected = {
            "managing-project-intake-and-work-contract": "tests/test_feature_spec_traceability_contract.py",
            "managing-design-documents": "tests/test_feature_spec_traceability_contract.py",
            "reviewing-and-validating-project-changes": "tests/test_feature_spec_traceability_contract.py",
            "running-adversarial-review-and-refinement": "tests/test_cross_discipline_review_lenses.py",
            "auditing-and-refining-ui-art": "tests/test_bcp008_behavior_and_procurement_pilot.py",
        }
        for skill_id, path in expected.items():
            row = next(line for line in markdown.splitlines() if line.startswith(f"| `{skill_id}`"))
            self.assertIn("EXECUTABLE_EVIDENCE", row)
            self.assertIn(path, row)


    def test_serial_fiction_skill_has_executable_repository_evidence(self) -> None:
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


if __name__ == "__main__":
    unittest.main()
